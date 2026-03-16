"""
operations.py - Core podcast transcription workflow
===================================================

Implements:
    - optional chunked WAV transcription with SpeechRecognition
    - deterministic demo transcript fallback when audio transcription is unavailable
    - keyword indexing for searchable transcript segments
    - highlight extraction and run artifact persistence
"""

from __future__ import annotations

import re
import wave
from pathlib import Path

from models import (
    create_highlight,
    create_project_config,
    create_run_summary,
    create_transcript_segment,
)
from storage import save_latest_run, save_latest_transcript


def _load_optional_speech_dependency():
    """Load SpeechRecognition lazily for optional audio transcription.

    Returns:
        module | None: SpeechRecognition module or None when unavailable.
    """
    try:
        import speech_recognition as sr

        return sr
    except ImportError:
        return None


def load_default_keywords() -> list[str]:
    """Return default podcast-search keywords.

    Returns:
        list[str]: Keywords used for indexing and highlights.
    """
    return [
        "ai",
        "model",
        "dataset",
        "feature",
        "training",
        "deployment",
        "evaluation",
    ]


def _normalize_text(value: str) -> str:
    """Normalize text for case-insensitive token matching.

    Parameters:
        value (str): Input text.

    Returns:
        str: Lowercased alphanumeric text with normalized spaces.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", value.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def _word_count(text: str) -> int:
    """Count words in free-form text.

    Parameters:
        text (str): Input text.

    Returns:
        int: Number of whitespace-separated tokens.
    """
    return len([token for token in text.split() if token])


def _create_demo_segments() -> list[dict]:
    """Create a deterministic transcript used when audio STT is unavailable.

    Returns:
        list[dict]: Demo transcript segments with timestamps.
    """
    script_chunks = [
        "Welcome back to the studio. Today we discuss how an ai model moves from idea to deployment in production.",
        "First we collect a dataset and clean noisy records. Better labels always improve training stability and evaluation quality.",
        "Next we extract each feature that captures user behavior. A compact feature set can reduce cost while keeping accuracy high.",
        "During training we track overfitting and tune hyperparameters. Reliable evaluation helps the team compare every experiment.",
        "Finally we publish a deployment checklist with monitoring alerts and rollback plans so the model stays healthy in production.",
    ]

    segments = []
    cursor = 0.0
    for index, text in enumerate(script_chunks, start=1):
        start = cursor
        end = start + 22.0
        cursor = end
        segments.append(
            create_transcript_segment(
                segment_id=f"demo_{index:03d}",
                start_seconds=start,
                end_seconds=end,
                text=text,
                source="demo_script",
                confidence=0.98,
            )
        )
    return segments


def _wav_duration_seconds(wav_path: Path) -> float:
    """Read WAV duration without loading the full signal into memory.

    Parameters:
        wav_path (Path): Path to a WAV audio file.

    Returns:
        float: Duration in seconds.
    """
    with wave.open(str(wav_path), "rb") as reader:
        frame_rate = reader.getframerate()
        frames = reader.getnframes()
    if frame_rate <= 0:
        return 0.0
    return float(frames) / float(frame_rate)


def _transcribe_wav_segments(audio_path: Path, config: dict) -> list[dict]:
    """Transcribe a WAV file in chunks using SpeechRecognition.

    Parameters:
        audio_path (Path): WAV audio path.
        config (dict): Runtime configuration.

    Returns:
        list[dict]: Transcribed segments; empty when transcription fails.
    """
    sr = _load_optional_speech_dependency()
    if sr is None:
        return []

    duration = _wav_duration_seconds(audio_path)
    if duration <= 0.0:
        return []

    recognizer = sr.Recognizer()
    chunk_size = max(1, int(config["chunk_duration_seconds"]))
    segments = []

    with sr.AudioFile(str(audio_path)) as source:
        offset = 0
        segment_index = 0
        while offset < duration and segment_index < config["max_segments"]:
            segment_index += 1
            chunk_audio = recognizer.record(source, duration=chunk_size)
            try:
                text = recognizer.recognize_google(chunk_audio)
            except (sr.UnknownValueError, sr.RequestError):
                text = ""

            if text.strip():
                segments.append(
                    create_transcript_segment(
                        segment_id=f"audio_{segment_index:03d}",
                        start_seconds=offset,
                        end_seconds=min(offset + chunk_size, duration),
                        text=text,
                        source="audio_file",
                    )
                )
            offset += chunk_size

    return segments


def _count_keyword_hits(segments: list[dict], keywords: list[str]) -> dict[str, int]:
    """Count keyword frequencies across transcript segments.

    Parameters:
        segments (list[dict]): Transcript segments.
        keywords (list[str]): Search keywords.

    Returns:
        dict[str, int]: Keyword occurrence table.
    """
    counts = {keyword: 0 for keyword in keywords}
    for segment in segments:
        normalized = " " + _normalize_text(segment["text"]) + " "
        for keyword in keywords:
            token = f" {keyword.lower()} "
            counts[keyword] += normalized.count(token)
    return counts


def _build_highlights(segments: list[dict], keywords: list[str], max_highlights: int) -> list[dict]:
    """Build ranked highlight snippets from transcript segments.

    Parameters:
        segments (list[dict]): Transcript segments.
        keywords (list[str]): Search keywords.
        max_highlights (int): Maximum highlights to return.

    Returns:
        list[dict]: Ranked highlight payloads.
    """
    ranked = []
    for segment in segments:
        normalized = " " + _normalize_text(segment["text"]) + " "
        matched = [kw for kw in keywords if f" {kw.lower()} " in normalized]
        if not matched:
            continue

        score = float(len(matched) * 2 + min(25, _word_count(segment["text"])) / 25.0)
        ranked.append(
            create_highlight(
                segment_id=segment["segment_id"],
                start_seconds=segment["start_seconds"],
                end_seconds=segment["end_seconds"],
                text=segment["text"],
                keywords=matched,
                score=score,
            )
        )

    ranked.sort(key=lambda item: (-item["score"], item["start_seconds"]))
    return ranked[:max_highlights]


def run_core_flow(config: dict | None = None, keywords: list[str] | None = None) -> dict:
    """Execute podcast voice-to-text processing and save a run artifact.

    Parameters:
        config (dict | None): Optional runtime configuration override.
        keywords (list[str] | None): Optional keyword list override.

    Returns:
        dict: Persisted session summary.
    """
    runtime_config = config or create_project_config()
    active_keywords = keywords or load_default_keywords()

    audio_path = Path(runtime_config["audio_input_path"])
    transcript_segments = []
    transcript_source = "demo_script"
    status = "completed_with_fallback"

    if audio_path.exists() and audio_path.suffix.lower() == ".wav":
        transcript_segments = _transcribe_wav_segments(audio_path, runtime_config)
        if transcript_segments:
            transcript_source = "audio_file"
            status = "completed"

    if not transcript_segments:
        transcript_segments = _create_demo_segments()

    transcript_segments = transcript_segments[: runtime_config["max_segments"]]
    total_words = sum(_word_count(segment["text"]) for segment in transcript_segments)
    duration_seconds = transcript_segments[-1]["end_seconds"] if transcript_segments else 0.0
    keyword_hits = _count_keyword_hits(transcript_segments, active_keywords)
    highlights = _build_highlights(
        segments=transcript_segments,
        keywords=active_keywords,
        max_highlights=runtime_config["max_highlights"],
    )

    summary = create_run_summary(
        config=runtime_config,
        total_segments=len(transcript_segments),
        total_words=total_words,
        duration_seconds=duration_seconds,
        transcript_source=transcript_source,
        keyword_hits=keyword_hits,
        highlights=highlights,
        transcript_preview=transcript_segments[:3],
        status=status,
    )
    save_latest_transcript(transcript_segments)
    save_latest_run(summary)
    return summary

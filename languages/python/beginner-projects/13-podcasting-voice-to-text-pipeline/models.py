"""
models.py - Data constructors for podcast transcription session artifacts
========================================================================
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    audio_input_path: str = "data/input/sample_podcast.wav",
    chunk_duration_seconds: int = 20,
    max_segments: int = 120,
    max_highlights: int = 5,
) -> dict:
    """Create the default runtime configuration.

    Parameters:
        audio_input_path (str): WAV file path for speech-to-text input.
        chunk_duration_seconds (int): Duration for each transcription chunk.
        max_segments (int): Maximum number of transcript segments to keep.
        max_highlights (int): Maximum number of highlights in the report.

    Returns:
        dict: Configuration payload.
    """
    return {
        "audio_input_path": audio_input_path,
        "chunk_duration_seconds": int(chunk_duration_seconds),
        "max_segments": int(max_segments),
        "max_highlights": int(max_highlights),
        "created_at": _utc_timestamp(),
    }


def create_transcript_segment(
    segment_id: str,
    start_seconds: float,
    end_seconds: float,
    text: str,
    source: str,
    confidence: float | None = None,
) -> dict:
    """Create one transcript segment with timing metadata.

    Parameters:
        segment_id (str): Unique transcript segment identifier.
        start_seconds (float): Segment start time.
        end_seconds (float): Segment end time.
        text (str): Transcript text for the segment.
        source (str): Source label (audio or demo script).
        confidence (float | None): Optional confidence estimate.

    Returns:
        dict: Transcript segment payload.
    """
    payload = {
        "segment_id": segment_id,
        "start_seconds": round(float(start_seconds), 2),
        "end_seconds": round(float(end_seconds), 2),
        "text": text.strip(),
        "source": source,
    }
    if confidence is not None:
        payload["confidence"] = round(float(confidence), 4)
    return payload


def create_highlight(
    segment_id: str,
    start_seconds: float,
    end_seconds: float,
    text: str,
    keywords: list[str],
    score: float,
) -> dict:
    """Create one highlight snippet from transcript content.

    Parameters:
        segment_id (str): Associated transcript segment identifier.
        start_seconds (float): Highlight start time.
        end_seconds (float): Highlight end time.
        text (str): Highlight text snippet.
        keywords (list[str]): Matched keywords in the snippet.
        score (float): Ranking score for highlight prioritization.

    Returns:
        dict: Highlight payload.
    """
    return {
        "segment_id": segment_id,
        "start_seconds": round(float(start_seconds), 2),
        "end_seconds": round(float(end_seconds), 2),
        "text": text.strip(),
        "keywords": sorted(set(keywords)),
        "score": round(float(score), 4),
    }


def create_run_summary(
    config: dict,
    total_segments: int,
    total_words: int,
    duration_seconds: float,
    transcript_source: str,
    keyword_hits: dict[str, int],
    highlights: list[dict],
    transcript_preview: list[dict],
    status: str,
) -> dict:
    """Create the persistable summary for one pipeline session.

    Parameters:
        config (dict): Runtime configuration.
        total_segments (int): Number of transcript segments captured.
        total_words (int): Number of transcript words.
        duration_seconds (float): Approximate covered duration.
        transcript_source (str): Source type for transcript generation.
        keyword_hits (dict[str, int]): Keyword frequency table.
        highlights (list[dict]): Ranked highlight snippets.
        transcript_preview (list[dict]): Short segment preview.
        status (str): Session outcome indicator.

    Returns:
        dict: Session summary payload.
    """
    return {
        "config": config,
        "total_segments": int(total_segments),
        "total_words": int(total_words),
        "duration_seconds": round(float(duration_seconds), 2),
        "transcript_source": transcript_source,
        "keyword_hits": dict(keyword_hits),
        "highlights": list(highlights),
        "transcript_preview": list(transcript_preview),
        "status": status,
        "saved_at": _utc_timestamp(),
    }

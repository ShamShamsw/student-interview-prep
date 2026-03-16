# Beginner Project 13: Podcasting Voice-To-Text Pipeline

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** chunked transcription, transcript indexing, timestamped highlights, and JSON run artifacts

---

## Why This Project?

Podcast episodes are useful only if listeners can quickly search and revisit key moments.
This project gives you a practical beginner workflow where you can:

- transcribe episode audio into timestamped text segments,
- index transcripts for keyword-based retrieval,
- generate highlight snippets for quick review,
- and save reproducible run artifacts for comparisons over time.

---

## Separate Repository

You can also access this project in a separate repository:

[podcasting voice to text pipeline Repository](https://github.com/ShamShamsw/podcasting-voice-to-text-pipeline.git)

---

## What You Will Build

You will build a command-line podcast transcription pipeline that:

1. Attempts chunked speech-to-text processing for local WAV files.
2. Falls back to a deterministic demo transcript if transcription dependencies/audio are unavailable.
3. Produces timestamped transcript segments.
4. Computes keyword hit counts across the full transcript.
5. Ranks and reports top highlight moments.
6. Saves run metadata and transcript artifacts to JSON.

---

## Requirements

- Python 3.11+
- `SpeechRecognition`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   PODCASTING VOICE-TO-TEXT PIPELINE - SEARCHABLE TRANSCRIPTS
======================================================================

Configuration:
   Audio input path: data/input/sample_podcast.wav
   Chunk duration: 20 seconds
   Max transcript segments: 120
   Max highlights: 5

Tracked keywords:
   ai, model, dataset, feature, training, deployment, evaluation

Processing behavior:
   1) Attempt to transcribe local WAV audio if dependencies are available.
   2) Fall back to an included demo episode script when transcription is unavailable.

Run summary:
   Status: completed_with_fallback
   Transcript source: demo_script
   Segments captured: 5
  Total words: 92
  Transcript duration: 110.0 seconds
  Keyword hits (top): deployment=2, evaluation=2, feature=2, model=2, training=2
  Highlights:
    [0.0s-22.0s] score=6.76 keywords=ai, deployment, model
    [22.0s-44.0s] score=6.72 keywords=dataset, evaluation, training
Saved run artifact: data/runs/latest_podcast_transcription_run.json
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---

## File Responsibilities

- `storage.py`: handles transcript/run artifact persistence in `data/runs/`.
- `models.py`: creates consistent payloads for configuration, transcript segments, highlights, and run summaries.
- `operations.py`: transcription/fallback logic, keyword indexing, highlight ranking, and run persistence.
- `display.py`: formats a readable CLI banner, startup guide, and run summary.
- `main.py`: thin orchestration entry point.

---

## Suggested Reflection Prompts

Add answers in your own notes after running the project:

- Which keywords produced the most useful highlights for review?
- How did transcript quality differ between real audio transcription and fallback/demo mode?
- What metadata would help make this pipeline production-ready for longer podcast episodes?

---

## Stretch Goals

1. Add speaker diarization tags for host and guest turns.
2. Export transcript + highlights into Markdown show notes.
3. Add fuzzy keyword search and phrase-level retrieval.
4. Build a simple web UI for transcript browsing and timestamp jump links.

# Beginner Project 11: Real-Time Webcam Computer Vision Demos

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** webcam capture, live filters, detection overlays, and motion tracking

---

## Why This Project?

Computer vision gets much easier to understand when you can see each step happen live.
This project gives you a practical webcam workflow where you can:

- capture frames from a real camera,
- switch between multiple processing modes,
- compare filtering, detection, and tracking behavior in real time,
- and save reproducible session metadata after each run.

---

## Separate Repository

You can also access this project in a separate repository:

[real time webcam computer vision Repository](https://github.com/ShamShamsw/real-time-webcam-computer-vision.git)

---

## What You Will Build

You will build a command-line webcam demo application that:

1. Opens the default webcam with a beginner-friendly configuration.
2. Displays a live preview feed with an FPS counter.
3. Switches between edge filtering, face detection, and motion tracking modes.
4. Draws overlays directly on the live video stream.
5. Releases the camera and closes the OpenCV window cleanly.
6. Saves run metadata and recent frame metrics to JSON.

---

## Requirements

- Python 3.11+
- `opencv-python`
- `numpy`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
===============================================================
   REAL-TIME WEBCAM COMPUTER VISION DEMOS - LIVE MODES
===============================================================

Startup configuration:
   Camera index: 0
   Frame size: 960x540
   Initial mode: preview

Available modes:
   [1] Preview - raw webcam feed with overlays
   [2] Edges - Canny edge filter for structure outlines
   [3] Faces - Haar cascade face detection overlay
   [4] Motion - background subtraction motion tracking

Controls:
   Press 1-4 to switch modes.
   Press Q or ESC to quit and save the session summary.

Session summary:
   Camera opened: yes
   Frames processed: 842
   Average FPS: 23.91
   Modes visited: preview, faces, motion
   Exit reason: user_exit
   Last detection count: 2
   Last tracked regions: 1
Saved run artifact: data/runs/latest_webcam_demo_run.json
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

- `storage.py`: handles session artifact persistence in `data/runs/`.
- `models.py`: creates consistent record payloads for config, modes, frame metrics, and run summaries.
- `operations.py`: webcam capture, mode switching, computer vision processing, and session saving.
- `display.py`: formats a readable CLI banner, startup guide, and session summary.
- `main.py`: thin orchestration entry point.

---

## Suggested Reflection Prompts

Add answers in your own notes after running the project:

- Which mode felt most stable in real time, and why?
- What changed in FPS when you switched from filtering to detection or tracking?
- What are the limitations of Haar cascades and simple background subtraction in real environments?

---

## Stretch Goals

1. Add a screenshot hotkey that saves the current frame to disk.
2. Record short demo videos for each mode.
3. Replace Haar cascades with a stronger deep-learning detector.
4. Add a notebook or widget-based control panel for mode switching.

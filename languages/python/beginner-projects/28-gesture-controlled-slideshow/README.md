# Beginner Project 28: Gesture-Controlled Slideshow

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Hand pose detection, gesture recognition, debouncing, real-time video processing, and interactive UI controls

---

## Why This Project?

Building hand gesture-controlled systems requires combining computer vision, real-time signal processing, and interactive UI design. Production applications like presentation tools, gaming interfaces, and accessibility software must detect hand movements reliably while filtering noise and implementing responsive controls.

This project teaches a professional gesture recognition pipeline where you can:

- capture continuous video from a webcam in real-time,
- detect hand landmarks and poses using machine learning (MediaPipe),
- extract gesture features (hand position, distance, orientation) from landmarks,
- apply debouncing to filter noisy or rapid gesture detections,
- implement next/previous slide navigation from specific hand gestures,
- provide real-time visual feedback overlay on the live video feed,
- manage a slide deck with metadata and display state,
- handle camera errors and permissions gracefully,
- run on a local machine without cloud dependencies,
- and log gesture events and navigation history for diagnostics.

---

## Separate Repository

You can also access this project in a separate repository:

[Gesture-Controlled Slideshow Repository](https://github.com/placeholder/gesture-controlled-slideshow.git)

---

## What You Will Build

You will build a real-time gesture recognition system that:

1. Initializes a webcam or video input device with appropriate resolution and FPS.
2. Captures video frames and extracts hand landmarks using MediaPipe Hand solution.
3. Detects specific hand gestures (e.g., thumb-up, peace sign, open palm) for control signals.
4. Applies temporal debouncing to prevent multiple triggers from a single gesture.
5. Interprets gestures as navigation commands (go forward slide, go back slide, etc.).
6. Loads and manages a slide deck from a local directory or JSON metadata file.
7. Renders the current slide on screen with gesture hints and status information.
8. Displays real-time visual feedback (bounding boxes, landmark dots, gesture labels) on the video feed.
9. Handles edge cases (multiple hands, no hands, poor lighting) gracefully.
10. Logs all navigation events and gesture detections with timestamps for review.

---

## Requirements

- Python 3.11+
- `mediapipe` (for hand landmark detection)
- `opencv-python` (for video capture and image processing)
- `numpy` (for numerical operations)
- `ipywidgets` (optional, for Jupyter-based interactive UI)
- `pillow` (for image processing)

Install with:

```bash
pip install -r requirements.txt
```

Note: Webcam access must be enabled in your system settings or OS security preferences.

---

## Example Session

```text
======================================================================
   GESTURE-CONTROLLED SLIDESHOW
======================================================================

Configuration:
   Video source:         Webcam (device 0)
   Resolution:           1280x720
   FPS target:           30
   Gesture debounce:     0.5 seconds
   Slides directory:     data/slides/

Startup:
   Data directory:       data/
   Slide deck loaded:    demo_deck.json
   Total slides:         8
   Current slide:        1

---

Video Stream Active:
   [OK] Webcam initialized
   [OK] MediaPipe Hand solution loaded
   Frame resolution:     1280x720
   FPS (actual):         28.3

---

Gesture Recognition (Real-time):

   Timestamp: 2024-03-15 10:45:23.451
   Frame #145
   Hands detected:       2
   
   Hand 1 (Right):
      Landmarks tracked: Yes (21 points)
      Position:          Center screen
      Confidence:        0.98
      Recognized gesture: OPEN_PALM
      Gesture score:     0.91
      
   Hand 2 (Left):
      Landmarks tracked: Yes (21 points)
      Position:          Right side
      Confidence:        0.95
      Recognized gesture: NONE

   Gesture Queue:
      Pending: OPEN_PALM (confidence=0.91, age=0.12s)
      Last action: None (debounce period active)

---

Navigation Events:

   Timestamp: 2024-03-15 10:45:24.102
   [GESTURE]      PEACE_SIGN detected (confidence=0.93)
   [DEBOUNCE]     Passed threshold (0.5s elapsed)
   [ACTION]       NEXT_SLIDE triggered
   [TRANSITION]   Slide 1 -> Slide 2
   [DISPLAY]      Rendering slide 2: "Advanced Features Overview"

   Timestamp: 2024-03-15 10:45:27.845
   [GESTURE]      THUMBS_DOWN detected (confidence=0.89)
   [DEBOUNCE]     Passed threshold (3.7s elapsed)
   [ACTION]       PREV_SLIDE triggered
   [TRANSITION]   Slide 2 -> Slide 1
   [DISPLAY]      Rendering slide 1: "Introduction"

---

Slide Metadata:

   Current Slide: 1
   Title:         Introduction
   Content length: 245 characters
   Image:         data/slides/intro.jpg (1920x1080)
   Speaker notes: "Welcome to the gesture demo. Use hand signs to navigate."

   Slide History:
      - Visited slide 1 at 10:45:20 (02 visits)
      - Visited slide 2 at 10:45:24 (01 visit)

---

Status:
   Session duration: 00:00:47
   Total gestures detected: 24
   Actions triggered: 2
   Error rate: 0.00%
   Avg gesture confidence: 0.91

Artifacts saved:
   Session log:         data/outputs/session_log.json
   Gesture events:      data/outputs/gesture_events.csv
   Navigation history:  data/outputs/navigation_history.json
   Performance report:  data/outputs/performance_report.txt
```

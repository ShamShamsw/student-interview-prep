"""
operations.py - Core webcam demo workflow
=========================================

Implements:
    - webcam capture and graceful release
    - live mode switching
    - edge filtering, face detection, and motion tracking demos
    - FPS estimation and session artifact persistence
"""

from time import perf_counter

from models import (
    create_demo_config,
    create_demo_mode,
    create_frame_metrics,
    create_session_summary,
)
from storage import save_latest_run


def _load_cv_dependencies():
    """Lazily import OpenCV dependencies with a clear error message.

    Returns:
        tuple: Imported cv2 and numpy modules.
    """
    try:
        import cv2
        import numpy as np

        return cv2, np
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependencies: install requirements.txt for this project before running the webcam demos."
        ) from exc


def load_demo_modes() -> list[dict]:
    """Return the supported live demo modes.

    Returns:
        list[dict]: Mode descriptors shown in the CLI and used at runtime.
    """
    return [
        create_demo_mode("preview", "Preview", "raw webcam feed with overlays", "1"),
        create_demo_mode("edges", "Edges", "Canny edge filter for structure outlines", "2"),
        create_demo_mode("faces", "Faces", "Haar cascade face detection overlay", "3"),
        create_demo_mode("motion", "Motion", "background subtraction motion tracking", "4"),
    ]


def _build_mode_lookup(modes: list[dict]) -> dict:
    """Create a dictionary keyed by mode identifier.

    Parameters:
        modes (list[dict]): Supported demo modes.

    Returns:
        dict: Mapping of mode key to mode payload.
    """
    return {mode["key"]: mode for mode in modes}


def _normalize_initial_mode(initial_mode: str, mode_lookup: dict) -> str:
    """Return a safe initial mode key.

    Parameters:
        initial_mode (str): Requested initial mode.
        mode_lookup (dict): Supported mode mapping.

    Returns:
        str: Valid mode key.
    """
    return initial_mode if initial_mode in mode_lookup else "preview"


def _load_face_cascade(cv2):
    """Load the built-in Haar cascade used for face detection.

    Parameters:
        cv2: Imported OpenCV module.

    Returns:
        Any: Cascade classifier or None when unavailable.
    """
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        return None
    return cascade


def _create_processing_state(cv2):
    """Create reusable state shared across frames.

    Parameters:
        cv2: Imported OpenCV module.

    Returns:
        dict: Stateful processing helpers.
    """
    return {
        "face_cascade": _load_face_cascade(cv2),
        "background_subtractor": cv2.createBackgroundSubtractorMOG2(
            history=120,
            varThreshold=32,
            detectShadows=True,
        ),
    }


def _open_camera(config: dict, cv2):
    """Open and configure the webcam capture device.

    Parameters:
        config (dict): Runtime configuration.
        cv2: Imported OpenCV module.

    Returns:
        Any: OpenCV VideoCapture object.
    """
    capture = cv2.VideoCapture(config["camera_index"])
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config["frame_width"])
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config["frame_height"])
    return capture


def _annotate_frame(frame, mode: dict, metrics: dict, cv2) -> None:
    """Draw the runtime HUD onto a processed frame.

    Parameters:
        frame: Processed OpenCV frame.
        mode (dict): Active mode descriptor.
        metrics (dict): Latest frame metrics.
        cv2: Imported OpenCV module.

    Returns:
        None
    """
    overlay_lines = [
        f"Mode: {mode['label']} ({mode['hotkey']})",
        f"FPS: {metrics['fps']:.2f}",
        f"Detections: {metrics['detection_count']}",
        f"Tracked regions: {metrics['tracked_regions']}",
        "Keys: 1-4 switch modes | Q or ESC quits",
    ]

    for index, text in enumerate(overlay_lines):
        cv2.putText(
            frame,
            text,
            (16, 28 + index * 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (32, 240, 160),
            2,
            cv2.LINE_AA,
        )


def _apply_preview_mode(frame):
    """Return the unmodified webcam frame.

    Parameters:
        frame: Raw webcam frame.

    Returns:
        tuple: Processed frame and metrics payload.
    """
    return frame.copy(), {"detection_count": 0, "tracked_regions": 0}


def _apply_edges_mode(frame, cv2):
    """Apply an edge-detection filter to the current frame.

    Parameters:
        frame: Raw webcam frame.
        cv2: Imported OpenCV module.

    Returns:
        tuple: Processed frame and metrics payload.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 60, 150)
    colored_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return colored_edges, {"detection_count": 0, "tracked_regions": 0}


def _apply_face_mode(frame, state: dict, cv2):
    """Run face detection and draw bounding boxes.

    Parameters:
        frame: Raw webcam frame.
        state (dict): Processing state with cascade classifier.
        cv2: Imported OpenCV module.

    Returns:
        tuple: Processed frame and metrics payload.
    """
    output_frame = frame.copy()
    cascade = state["face_cascade"]
    if cascade is None:
        cv2.putText(
            output_frame,
            "Face cascade unavailable in this OpenCV build.",
            (16, output_frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        return output_frame, {"detection_count": 0, "tracked_regions": 0}

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for x, y, width, height in faces:
        cv2.rectangle(output_frame, (x, y), (x + width, y + height), (0, 255, 255), 2)

    return output_frame, {"detection_count": len(faces), "tracked_regions": 0}


def _apply_motion_mode(frame, state: dict, cv2, np):
    """Track moving foreground regions using background subtraction.

    Parameters:
        frame: Raw webcam frame.
        state (dict): Processing state with background subtractor.
        cv2: Imported OpenCV module.
        np: Imported numpy module.

    Returns:
        tuple: Processed frame and metrics payload.
    """
    output_frame = frame.copy()
    subtractor = state["background_subtractor"]
    mask = subtractor.apply(frame)
    _, binary_mask = cv2.threshold(mask, 220, 255, cv2.THRESH_BINARY)

    # Morphological cleanup keeps the demo focused on larger motion instead of sensor noise.
    kernel = np.ones((3, 3), dtype=np.uint8)
    cleaned_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tracked_regions = 0
    for contour in contours:
        if cv2.contourArea(contour) < 1200:
            continue
        x, y, width, height = cv2.boundingRect(contour)
        cv2.rectangle(output_frame, (x, y), (x + width, y + height), (255, 180, 0), 2)
        tracked_regions += 1

    return output_frame, {"detection_count": 0, "tracked_regions": tracked_regions}


def _process_frame(frame, active_mode: str, state: dict, cv2, np):
    """Route a frame through the currently active webcam demo mode.

    Parameters:
        frame: Raw webcam frame.
        active_mode (str): Active mode key.
        state (dict): Shared processing state.
        cv2: Imported OpenCV module.
        np: Imported numpy module.

    Returns:
        tuple: Processed frame and metrics payload.
    """
    if active_mode == "edges":
        return _apply_edges_mode(frame, cv2)
    if active_mode == "faces":
        return _apply_face_mode(frame, state, cv2)
    if active_mode == "motion":
        return _apply_motion_mode(frame, state, cv2, np)
    return _apply_preview_mode(frame)


def _build_summary(
    config: dict,
    modes: list[dict],
    frames_processed: int,
    fps_samples: list[float],
    visited_modes: list[str],
    exit_reason: str,
    status: str,
    camera_opened: bool,
    recent_metrics: list[dict],
) -> dict:
    """Create and persist a session summary.

    Parameters:
        config (dict): Runtime configuration.
        modes (list[dict]): Supported webcam demo modes.
        frames_processed (int): Total processed frames.
        fps_samples (list[float]): Instantaneous FPS readings.
        visited_modes (list[str]): Unique modes visited.
        exit_reason (str): Why the session stopped.
        status (str): Session outcome indicator.
        camera_opened (bool): Whether the webcam opened.
        recent_metrics (list[dict]): Rolling frame metrics history.

    Returns:
        dict: Persisted session summary.
    """
    average_fps = sum(fps_samples) / len(fps_samples) if fps_samples else 0.0
    summary = create_session_summary(
        config=config,
        available_modes=modes,
        frames_processed=frames_processed,
        average_fps=average_fps,
        visited_modes=visited_modes,
        exit_reason=exit_reason,
        status=status,
        camera_opened=camera_opened,
        recent_metrics=recent_metrics,
    )
    save_latest_run(summary)
    return summary


def run_core_flow(config: dict | None = None, modes: list[dict] | None = None) -> dict:
    """Execute the live webcam demo loop and save a session artifact.

    Parameters:
        config (dict | None): Optional runtime configuration override.
        modes (list[dict] | None): Optional supported mode descriptors.

    Returns:
        dict: Persisted session summary.
    """
    cv2, np = _load_cv_dependencies()
    runtime_config = config or create_demo_config()
    available_modes = modes or load_demo_modes()
    mode_lookup = _build_mode_lookup(available_modes)
    active_mode = _normalize_initial_mode(runtime_config["initial_mode"], mode_lookup)
    processing_state = _create_processing_state(cv2)

    capture = None
    camera_opened = False
    fps_samples: list[float] = []
    recent_metrics: list[dict] = []
    visited_modes = [active_mode]
    frames_processed = 0
    exit_reason = "user_exit"
    status = "completed"

    try:
        capture = _open_camera(runtime_config, cv2)
        if not capture.isOpened():
            return _build_summary(
                config=runtime_config,
                modes=available_modes,
                frames_processed=0,
                fps_samples=[],
                visited_modes=visited_modes,
                exit_reason="camera_unavailable",
                status="camera_unavailable",
                camera_opened=False,
                recent_metrics=[],
            )

        camera_opened = True
        last_frame_time = perf_counter()
        hotkey_map = {ord(mode["hotkey"]): mode["key"] for mode in available_modes}

        while True:
            frame_ok, frame = capture.read()
            if not frame_ok:
                exit_reason = "camera_read_failed"
                status = "camera_read_failed"
                break

            frames_processed += 1
            current_time = perf_counter()
            elapsed = max(current_time - last_frame_time, 1e-6)
            last_frame_time = current_time
            fps = 1.0 / elapsed
            fps_samples.append(fps)

            processed_frame, counts = _process_frame(
                frame=frame,
                active_mode=active_mode,
                state=processing_state,
                cv2=cv2,
                np=np,
            )

            metrics = create_frame_metrics(
                frame_index=frames_processed,
                mode_key=active_mode,
                fps=fps,
                detection_count=counts["detection_count"],
                tracked_regions=counts["tracked_regions"],
            )
            recent_metrics.append(metrics)
            recent_metrics = recent_metrics[-runtime_config["max_history"] :]

            _annotate_frame(processed_frame, mode_lookup[active_mode], metrics, cv2)
            cv2.imshow(runtime_config["window_name"], processed_frame)

            pressed_key = cv2.waitKey(1) & 0xFF
            if pressed_key in (ord("q"), 27):
                exit_reason = "user_exit"
                break
            if pressed_key in hotkey_map:
                next_mode = hotkey_map[pressed_key]
                active_mode = next_mode
                if next_mode not in visited_modes:
                    visited_modes.append(next_mode)

        return _build_summary(
            config=runtime_config,
            modes=available_modes,
            frames_processed=frames_processed,
            fps_samples=fps_samples,
            visited_modes=visited_modes,
            exit_reason=exit_reason,
            status=status,
            camera_opened=camera_opened,
            recent_metrics=recent_metrics,
        )
    finally:
        if capture is not None:
            capture.release()
        cv2.destroyAllWindows()

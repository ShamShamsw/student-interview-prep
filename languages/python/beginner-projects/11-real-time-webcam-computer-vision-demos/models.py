"""
models.py - Data constructors for webcam demo session artifacts
===============================================================
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_demo_config(
    camera_index: int = 0,
    frame_width: int = 960,
    frame_height: int = 540,
    initial_mode: str = "preview",
    max_history: int = 20,
    window_name: str = "Project 11 - Real-Time Webcam Computer Vision Demos",
) -> dict:
    """Create the default runtime configuration.

    Parameters:
        camera_index (int): OpenCV camera index.
        frame_width (int): Requested capture width.
        frame_height (int): Requested capture height.
        initial_mode (str): Starting demo mode key.
        max_history (int): Number of recent frame metrics to keep.
        window_name (str): Name of the OpenCV display window.

    Returns:
        dict: Configuration payload.
    """
    return {
        "camera_index": int(camera_index),
        "frame_width": int(frame_width),
        "frame_height": int(frame_height),
        "initial_mode": initial_mode,
        "max_history": int(max_history),
        "window_name": window_name,
        "created_at": _utc_timestamp(),
    }


def create_demo_mode(key: str, label: str, description: str, hotkey: str) -> dict:
    """Create one switchable webcam demo mode descriptor.

    Parameters:
        key (str): Internal mode identifier.
        label (str): Human-readable mode name.
        description (str): Short explanation of the mode.
        hotkey (str): Single-key shortcut used during the live demo.

    Returns:
        dict: Mode descriptor payload.
    """
    return {
        "key": key,
        "label": label,
        "description": description,
        "hotkey": hotkey,
    }


def create_frame_metrics(
    frame_index: int,
    mode_key: str,
    fps: float,
    detection_count: int = 0,
    tracked_regions: int = 0,
) -> dict:
    """Create per-frame metrics captured during the webcam session.

    Parameters:
        frame_index (int): Sequential frame number.
        mode_key (str): Active processing mode.
        fps (float): Instantaneous frames-per-second estimate.
        detection_count (int): Number of detected faces or objects.
        tracked_regions (int): Number of tracked motion regions.

    Returns:
        dict: Frame metrics payload.
    """
    return {
        "frame_index": int(frame_index),
        "mode_key": mode_key,
        "fps": round(float(fps), 2),
        "detection_count": int(detection_count),
        "tracked_regions": int(tracked_regions),
    }


def create_session_summary(
    config: dict,
    available_modes: list[dict],
    frames_processed: int,
    average_fps: float,
    visited_modes: list[str],
    exit_reason: str,
    status: str,
    camera_opened: bool,
    recent_metrics: list[dict],
) -> dict:
    """Create the persistable summary for one webcam session.

    Parameters:
        config (dict): Runtime configuration.
        available_modes (list[dict]): Supported demo modes.
        frames_processed (int): Count of processed frames.
        average_fps (float): Average FPS across the session.
        visited_modes (list[str]): Unique modes visited in order.
        exit_reason (str): Why the session ended.
        status (str): Session outcome indicator.
        camera_opened (bool): Whether the webcam opened successfully.
        recent_metrics (list[dict]): Rolling window of frame metrics.

    Returns:
        dict: Session summary payload.
    """
    return {
        "config": config,
        "available_modes": available_modes,
        "frames_processed": int(frames_processed),
        "average_fps": round(float(average_fps), 2),
        "visited_modes": list(visited_modes),
        "exit_reason": exit_reason,
        "status": status,
        "camera_opened": bool(camera_opened),
        "recent_metrics": list(recent_metrics),
        "saved_at": _utc_timestamp(),
    }

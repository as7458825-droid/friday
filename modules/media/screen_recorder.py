import os
import threading
import time
from datetime import datetime

import cv2
import numpy as np
from PIL import ImageGrab

_recording = False
_recorder_thread = None
_output_path = ""
_fps = 10


def start_recording(filename: str = "") -> str:
    global _recording, _recorder_thread, _output_path
    if _recording:
        return "Already recording. Say stop recording to save."
    if not filename:
        filename = f"screencast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    recordings_dir = os.path.join(os.path.dirname(__file__), "..", "..", "recordings")
    if not os.path.isdir(recordings_dir):
        os.makedirs(recordings_dir, exist_ok=True)
    _output_path = os.path.join(recordings_dir, filename)
    _recording = True
    _recorder_thread = threading.Thread(target=_record_loop, daemon=True)
    _recorder_thread.start()
    return f"Screen recording started. Saving to {filename}"


def stop_recording() -> str:
    global _recording
    if not _recording:
        return "Not recording."
    _recording = False
    if _recorder_thread:
        _recorder_thread.join(timeout=5)
    if _output_path and os.path.isfile(_output_path):
        size_mb = os.path.getsize(_output_path) / (1024 * 1024)
        return f"Recording saved to {_output_path} ({size_mb:.1f} MB)"
    return "Recording stopped but no file saved."


def _record_loop():
    global _recording
    screen_size = (1920, 1080)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(_output_path, fourcc, _fps, screen_size)
    try:
        while _recording:
            img = ImageGrab.grab()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, screen_size)
            out.write(frame)
            time.sleep(1.0 / _fps)
    finally:
        out.release()


def recording_status() -> str:
    return f"{'Recording' if _recording else 'Idle'}. Say start recording or stop recording."

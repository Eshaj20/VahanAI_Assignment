from __future__ import annotations

import subprocess
from pathlib import Path


def probe_audio_duration_seconds(audio_path: str | Path) -> float:
    audio_path = str(audio_path)
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


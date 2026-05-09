from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class TranscriptResult:
    text: str
    latency_seconds: float
    raw_response: str


class ASRModel(Protocol):
    name: str

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        ...

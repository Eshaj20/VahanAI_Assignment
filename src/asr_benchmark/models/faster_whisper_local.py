from __future__ import annotations

import json
import time
from pathlib import Path

from faster_whisper import WhisperModel

from .base import TranscriptResult

# This file defines the FasterWhisperModel class, which is an implementation of an ASR model using the Faster Whisper library. The class initializes with a model name and compute type, and provides a transcribe method that takes an audio file path, performs transcription, and returns a TranscriptResult containing the transcribed text, latency, and raw response information. The transcribe method uses the WhisperModel's transcribe function with specific parameters for beam size, VAD filtering, and conditioning on previous text.
class FasterWhisperModel:
    def __init__(self, alias: str, model_name: str, compute_type: str = "int8") -> None:
        self.alias = alias
        self.model_name = model_name
        self.compute_type = compute_type
        self.name = alias
        self._model: WhisperModel | None = None

    def _get_model(self) -> WhisperModel:
        if self._model is None:
            self._model = WhisperModel(self.model_name, compute_type=self.compute_type)
        return self._model

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        segments, info = self._get_model().transcribe(
            str(audio_path),
            beam_size=5,
            vad_filter=True,
            condition_on_previous_text=False,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        latency = time.perf_counter() - start
        raw = {
            "language": info.language,
            "language_probability": info.language_probability,
            "model_name": self.model_name,
        }
        return TranscriptResult(
            text=text,
            latency_seconds=latency,
            raw_response=json.dumps(raw, ensure_ascii=False),
        )

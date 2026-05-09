from __future__ import annotations

import json
import time
from pathlib import Path

import httpx

from ..config import get_settings
from .base import TranscriptResult

# This file defines the DeepgramModel class, which is an implementation of an ASR model using the Deepgram API. The class initializes with API key, model name, language, and retry settings. The transcribe method sends an audio file to the Deepgram API for transcription, handles retries for transient errors, and returns a TranscriptResult containing the transcribed text, latency, and raw response information. The method uses exponential backoff for retries and raises exceptions if all attempts fail or if the API key is not set.
class DeepgramModel:
    def __init__(self, max_retries: int = 3, request_timeout_seconds: float = 180.0) -> None:
        settings = get_settings()
        if not settings.deepgram_api_key:
            raise ValueError("DEEPGRAM_API_KEY is not set.")
        self.api_key = settings.deepgram_api_key
        self.model = settings.deepgram_model
        self.language = settings.deepgram_language
        self.name = f"deepgram_{self.model}"
        self.max_retries = max_retries
        self.request_timeout_seconds = request_timeout_seconds

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            start = time.perf_counter()
            try:
                with audio_path.open("rb") as handle:
                    response = httpx.post(
                        "https://api.deepgram.com/v1/listen",
                        params={
                            "model": self.model,
                            "language": self.language,
                            "smart_format": "true",
                            "punctuate": "true",
                        },
                        headers={
                            "Authorization": f"Token {self.api_key}",
                            "Content-Type": "application/octet-stream",
                        },
                        content=handle.read(),
                        timeout=self.request_timeout_seconds,
                    )
                latency = time.perf_counter() - start

                if response.status_code in {408, 429, 500, 502, 503, 504} and attempt < self.max_retries:
                    time.sleep(attempt * 2)
                    continue

                response.raise_for_status()
                payload = response.json()
                text = (
                    payload.get("results", {})
                    .get("channels", [{}])[0]
                    .get("alternatives", [{}])[0]
                    .get("transcript", "")
                )
                return TranscriptResult(
                    text=text,
                    latency_seconds=latency,
                    raw_response=json.dumps(payload, ensure_ascii=False),
                )
            except (httpx.TimeoutException, httpx.TransportError, httpx.HTTPStatusError) as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    raise
                time.sleep(attempt * 2)

        if last_error is not None:
            raise last_error
        raise RuntimeError("Deepgram transcription failed without an explicit exception.")

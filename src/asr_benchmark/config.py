from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    deepgram_api_key: str | None = os.getenv("DEEPGRAM_API_KEY")
    deepgram_model: str = os.getenv("DEEPGRAM_MODEL", "nova-2")
    deepgram_language: str = os.getenv("DEEPGRAM_LANGUAGE", "multi")
    fw_small_name: str = os.getenv("FW_SMALL_NAME", "small")
    fw_large_name: str = os.getenv("FW_LARGE_NAME", "large-v3")


def get_settings() -> Settings:
    return Settings()


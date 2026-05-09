from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Sample:
    sample_id: str
    audio_path: Path
    language: str
    condition_tags: tuple[str, ...]
    expected_locality: str
    reference_transcript: str
    notes: str


REQUIRED_COLUMNS = {
    "sample_id",
    "audio_path",
    "language",
    "condition_tags",
    "expected_locality",
    "reference_transcript",
    "notes",
}


def load_samples(dataset_path: str | Path) -> list[Sample]:
    dataset_path = Path(dataset_path)
    repo_root = dataset_path.parents[2] if len(dataset_path.parents) >= 3 else dataset_path.parent
    rows: list[Sample] = []

    with dataset_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Dataset is missing required columns: {missing_list}")

        for row in reader:
            audio_path = Path(row["audio_path"])
            if not audio_path.is_absolute():
                audio_path = (repo_root / audio_path).resolve()

            tags = tuple(tag.strip() for tag in row["condition_tags"].split("|") if tag.strip())
            rows.append(
                Sample(
                    sample_id=row["sample_id"].strip(),
                    audio_path=audio_path,
                    language=row["language"].strip(),
                    condition_tags=tags,
                    expected_locality=row["expected_locality"].strip(),
                    reference_transcript=row["reference_transcript"].strip(),
                    notes=row["notes"].strip(),
                )
            )

    return rows


def validate_samples(samples: list[Sample]) -> list[str]:
    issues: list[str] = []
    seen_ids: set[str] = set()

    for sample in samples:
        if sample.sample_id in seen_ids:
            issues.append(f"Duplicate sample_id: {sample.sample_id}")
        seen_ids.add(sample.sample_id)

        if not sample.audio_path.exists():
            issues.append(f"Missing audio file: {sample.audio_path}")

        if not sample.reference_transcript:
            issues.append(f"Empty reference transcript for sample {sample.sample_id}")

        if not sample.expected_locality:
            issues.append(f"Empty expected locality for sample {sample.sample_id}")

    return issues

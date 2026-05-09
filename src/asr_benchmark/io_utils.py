from __future__ import annotations

import csv
from dataclasses import asdict, is_dataclass
from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_csv(path: str | Path, rows: list[object]) -> None:
    path = Path(path)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    normalized_rows: list[dict[str, object]] = []
    for row in rows:
        if is_dataclass(row):
            normalized_rows.append(asdict(row))
        else:
            normalized_rows.append(dict(row))

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(normalized_rows[0].keys()))
        writer.writeheader()
        writer.writerows(normalized_rows)


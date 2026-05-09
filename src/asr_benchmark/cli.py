from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .benchmark import render_summary, run_benchmark
from .dataset import load_samples, validate_samples
from .io_utils import write_csv
from .metrics import (
    aggregate_by_condition,
    aggregate_predictions,
    char_error_rate,
    locality_exact_match,
    locality_token_recall,
    word_error_rate,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ASR benchmark CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full benchmark")
    run_parser.add_argument("--dataset", required=True, help="Path to metadata CSV")
    run_parser.add_argument("--output-dir", required=True, help="Directory for outputs")
    run_parser.add_argument("--model", action="append", required=True, help="Model name to evaluate")

    validate_parser = subparsers.add_parser("validate", help="Validate dataset CSV and audio files")
    validate_parser.add_argument("--dataset", required=True, help="Path to metadata CSV")

    summary_parser = subparsers.add_parser("summarize", help="Generate summary markdown from predictions.csv")
    summary_parser.add_argument("--predictions", required=True, help="Path to predictions CSV")
    summary_parser.add_argument("--output", required=True, help="Output markdown path")

    rescore_parser = subparsers.add_parser("rescore", help="Recompute metrics from an existing predictions CSV")
    rescore_parser.add_argument("--predictions", required=True, help="Path to predictions CSV")
    rescore_parser.add_argument("--output-dir", required=True, help="Directory for rescored outputs")

    return parser


def command_run(args: argparse.Namespace) -> int:
    outputs = run_benchmark(args.dataset, args.output_dir, args.model)
    for name, path in outputs.items():
        print(f"{name}: {path}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    samples = load_samples(args.dataset)
    issues = validate_samples(samples)
    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"Validation passed for {len(samples)} samples.")
    return 0


def command_summarize(args: argparse.Namespace) -> int:
    prediction_path = Path(args.predictions)
    with prediction_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    Path(args.output).write_text(render_summary(rows), encoding="utf-8")
    print(f"summary: {args.output}")
    return 0


def command_rescore(args: argparse.Namespace) -> int:
    prediction_path = Path(args.predictions)
    with prediction_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    rescored_rows: list[dict[str, object]] = []
    for row in rows:
        rescored = dict(row)
        rescored["wer"] = round(word_error_rate(str(row["reference_transcript"]), str(row["prediction"])), 4)
        rescored["cer"] = round(char_error_rate(str(row["reference_transcript"]), str(row["prediction"])), 4)
        rescored["locality_exact_match"] = round(locality_exact_match(str(row["expected_locality"]), str(row["prediction"])), 4)
        rescored["locality_token_recall"] = round(locality_token_recall(str(row["expected_locality"]), str(row["prediction"])), 4)
        rescored["latency_seconds"] = float(row["latency_seconds"])
        rescored["audio_seconds"] = float(row["audio_seconds"])
        rescored_rows.append(rescored)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "predictions.csv", rescored_rows)
    write_csv(output_dir / "aggregate_metrics.csv", aggregate_predictions(rescored_rows))
    write_csv(output_dir / "condition_metrics.csv", aggregate_by_condition(rescored_rows))
    (output_dir / "summary.md").write_text(render_summary(rescored_rows), encoding="utf-8")
    print(f"rescored: {output_dir}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        return command_run(args)
    if args.command == "validate":
        return command_validate(args)
    if args.command == "summarize":
        return command_summarize(args)
    if args.command == "rescore":
        return command_rescore(args)
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

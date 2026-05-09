from __future__ import annotations

from pathlib import Path

from tqdm import tqdm

from .audio import probe_audio_duration_seconds
from .config import get_settings
from .dataset import Sample, load_samples, validate_samples
from .io_utils import ensure_dir, write_csv
from .metrics import (
    aggregate_by_condition,
    aggregate_predictions,
    char_error_rate,
    locality_exact_match,
    locality_token_recall,
    word_error_rate,
)

# This file contains the main benchmarking logic for evaluating ASR models on a given dataset. It includes functions to build model instances based on specified names, run the benchmark by processing each sample through the models, and render a summary of the results in Markdown format. The score_sample function transcribes audio samples using the provided model and calculates various metrics such as WER, CER, locality exact match, locality token recall, latency, and audio duration. The render_summary function generates a Markdown report summarizing the overall metrics for each model and a breakdown of results by condition tags. The benchmark results are saved as CSV files for predictions, aggregate metrics, and condition-specific metrics, as well as a summary Markdown file.

# The build_models function creates instances of ASR models based on a list of model names. It uses a registry to map model names to their corresponding classes or factory functions. If an unknown model name is provided, it raises a ValueError with a message listing the supported models. 
def build_models(model_names: list[str]):
    settings = get_settings()
    from .models.deepgram_api import DeepgramModel
    from .models.faster_whisper_local import FasterWhisperModel

    registry = {
        "deepgram": DeepgramModel,
        "faster_whisper_small": lambda: FasterWhisperModel("faster_whisper_small", settings.fw_small_name),
        "faster_whisper_large": lambda: FasterWhisperModel("faster_whisper_large", settings.fw_large_name),
    }

    models = []
    for name in model_names:
        if name not in registry:
            raise ValueError(f"Unknown model '{name}'. Supported models: {', '.join(sorted(registry))}")
        models.append(registry[name]())
    return models

# The run_benchmark function orchestrates the entire benchmarking process by loading samples, validating them, building model instances, running predictions, calculating metrics, and saving the results to the specified output directory.
def run_benchmark(dataset_path: str | Path, output_dir: str | Path, model_names: list[str]) -> dict[str, Path]:
    samples = load_samples(dataset_path)
    issues = validate_samples(samples)
    if issues:
        joined = "\n".join(f"- {issue}" for issue in issues)
        raise ValueError(f"Dataset validation failed:\n{joined}")

    models = build_models(model_names)
    output_dir = ensure_dir(output_dir)
    predictions: list[dict[str, object]] = []

    for model in models:
        for sample in tqdm(samples, desc=f"Running {model.name}", leave=False):
            predictions.append(score_sample(model, sample))

    prediction_path = output_dir / "predictions.csv"
    aggregate_path = output_dir / "aggregate_metrics.csv"
    condition_path = output_dir / "condition_metrics.csv"
    summary_path = output_dir / "summary.md"

    write_csv(prediction_path, predictions)
    write_csv(aggregate_path, aggregate_predictions(predictions))
    write_csv(condition_path, aggregate_by_condition(predictions))
    summary_path.write_text(render_summary(predictions), encoding="utf-8")

    return {
        "predictions": prediction_path,
        "aggregate": aggregate_path,
        "conditions": condition_path,
        "summary": summary_path,
    }


#  The score_sample function handles the transcription and metric calculation for a single sample, while the render_summary function generates a Markdown report summarizing the results across all models and conditions.
def score_sample(model, sample: Sample) -> dict[str, object]:
    result = model.transcribe(sample.audio_path)
    audio_seconds = probe_audio_duration_seconds(sample.audio_path)
    return {
        "sample_id": sample.sample_id,
        "model": model.name,
        "audio_path": str(sample.audio_path),
        "language": sample.language,
        "condition_tags": "|".join(sample.condition_tags),
        "expected_locality": sample.expected_locality,
        "reference_transcript": sample.reference_transcript,
        "prediction": result.text,
        "wer": round(word_error_rate(sample.reference_transcript, result.text), 4),
        "cer": round(char_error_rate(sample.reference_transcript, result.text), 4),
        "locality_exact_match": round(locality_exact_match(sample.expected_locality, result.text), 4),
        "locality_token_recall": round(locality_token_recall(sample.expected_locality, result.text), 4),
        "latency_seconds": round(result.latency_seconds, 4),
        "audio_seconds": round(audio_seconds, 4),
        "raw_response": result.raw_response,
    }

# The render_summary function generates a Markdown report summarizing the overall metrics for each model and a breakdown of results by condition tags. It uses the aggregate_predictions and aggregate_by_condition functions to compute the necessary metrics and formats them into Markdown tables for easy visualization.
def render_summary(predictions: list[dict[str, object]]) -> str:
    aggregates = aggregate_predictions(predictions)
    by_condition = aggregate_by_condition(predictions)

    lines = [
        "# Benchmark Summary",
        "",
        "## Overall Metrics",
        "",
        "| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in aggregates:
        lines.append(
            f"| {row.model} | {row.samples} | {row.avg_wer:.3f} | {row.avg_cer:.3f} | "
            f"{row.locality_exact_match_rate:.3f} | {row.locality_token_recall:.3f} | "
            f"{row.avg_latency_seconds:.3f} | {row.realtime_factor:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Condition Breakdown",
            "",
            "| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in by_condition:
        lines.append(
            f"| {row['model']} | {row['condition_tag']} | {row['samples']} | {row['avg_wer']:.3f} | "
            f"{row['locality_exact_match_rate']:.3f} | {row['avg_latency_seconds']:.3f} |"
        )

    return "\n".join(lines) + "\n"

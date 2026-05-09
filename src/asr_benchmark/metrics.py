from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher

from .normalization import normalize_locality, normalize_text

# This file contains functions for calculating evaluation metrics for ASR systems, including Word Error Rate (WER), Character Error Rate (CER), and locality-based metrics. It also includes functions for aggregating results across multiple predictions and conditions.

# The levenshtein_distance function computes the edit distance between two sequences, which is used to calculate WER and CER. The word_error_rate and char_error_rate functions compute the respective error rates based on the normalized reference and hypothesis texts. The locality_exact_match and locality_token_recall functions evaluate how well the predicted transcript captures specific locality information. Finally, the aggregate_predictions and aggregate_by_condition functions summarize results across multiple predictions, grouping by model and condition tags for analysis.
def levenshtein_distance(left: list[str] | str, right: list[str] | str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    previous = list(range(len(right) + 1))
    for i, left_item in enumerate(left, start=1):
        current = [i]
        for j, right_item in enumerate(right, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (0 if left_item == right_item else 1)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]

# The word_error_rate function computes the WER by normalizing the reference and hypothesis texts, splitting them into tokens, and calculating the Levenshtein distance between the token lists. It returns the error rate as a float between 0 and 1, where 0 means a perfect match and 1 means completely different sequences.
def word_error_rate(reference: str, hypothesis: str) -> float:
    ref_tokens = normalize_text(reference).split()
    hyp_tokens = normalize_text(hypothesis).split()
    if not ref_tokens:
        return 0.0 if not hyp_tokens else 1.0
    return levenshtein_distance(ref_tokens, hyp_tokens) / len(ref_tokens)

# The char_error_rate function computes the character-level error rate by normalizing the reference and hypothesis texts, removing spaces, and calculating the Levenshtein distance between the resulting strings. It returns the error rate as a float between 0 and 1, where 0 means a perfect match and 1 means completely different strings.
def char_error_rate(reference: str, hypothesis: str) -> float:
    ref_text = normalize_text(reference).replace(" ", "")
    hyp_text = normalize_text(hypothesis).replace(" ", "")
    if not ref_text:
        return 0.0 if not hyp_text else 1.0
    return levenshtein_distance(ref_text, hyp_text) / len(ref_text)


# The locality_exact_match function checks if the normalized expected locality is present in the normalized hypothesis transcript. If it is, it returns 1.0 for a perfect match. If not, it generates candidate substrings from the hypothesis and calculates the similarity ratio with the expected locality using SequenceMatcher. If any candidate has a similarity ratio of 0.72 or higher, it returns 1.0; otherwise, it returns 0.0.
def locality_exact_match(expected_locality: str, hypothesis: str) -> float:
    locality = normalize_locality(expected_locality)
    transcript = normalize_text(hypothesis)
    if locality in transcript:
        return 1.0

    locality_tokens = locality.split()
    transcript_tokens = transcript.split()
    if not transcript_tokens:
        return 0.0

    window_size = max(1, len(locality_tokens))
    candidates = [
        " ".join(transcript_tokens[i : i + window_size])
        for i in range(max(1, len(transcript_tokens) - window_size + 1))
    ]
    best_similarity = max(
        (SequenceMatcher(None, locality, candidate).ratio() for candidate in candidates),
        default=0.0,
    )
    return 1.0 if best_similarity >= 0.72 else 0.0

# The locality_token_recall function calculates the recall of locality tokens in the hypothesis transcript. It normalizes the expected locality and hypothesis, splits them into tokens, and computes the ratio of correctly predicted locality tokens to the total number of locality tokens. If there are no locality tokens, it returns 0.0.
def locality_token_recall(expected_locality: str, hypothesis: str) -> float:
    locality_tokens = set(normalize_locality(expected_locality).split())
    hyp_tokens = set(normalize_text(hypothesis).split())
    if not locality_tokens:
        return 0.0
    return len(locality_tokens & hyp_tokens) / len(locality_tokens)


@dataclass(frozen=True)
class AggregateRow:
    model: str
    samples: int
    avg_wer: float
    avg_cer: float
    locality_exact_match_rate: float
    locality_token_recall: float
    avg_latency_seconds: float
    avg_audio_seconds: float
    realtime_factor: float

# The aggregate_predictions function takes a list of prediction dictionaries, groups them by model, and calculates average metrics for each model. It returns a sorted list of AggregateRow instances, where the sorting is primarily by average WER (ascending) and secondarily by locality exact match rate (descending).
def aggregate_predictions(predictions: list[dict[str, object]]) -> list[AggregateRow]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in predictions:
        grouped[str(row["model"])].append(row)

    summary: list[AggregateRow] = []
    for model, rows in grouped.items():
        sample_count = len(rows)
        total_latency = sum(float(row["latency_seconds"]) for row in rows)
        total_audio = sum(float(row["audio_seconds"]) for row in rows)
        summary.append(
            AggregateRow(
                model=model,
                samples=sample_count,
                avg_wer=sum(float(row["wer"]) for row in rows) / sample_count,
                avg_cer=sum(float(row["cer"]) for row in rows) / sample_count,
                locality_exact_match_rate=sum(float(row["locality_exact_match"]) for row in rows) / sample_count,
                locality_token_recall=sum(float(row["locality_token_recall"]) for row in rows) / sample_count,
                avg_latency_seconds=total_latency / sample_count,
                avg_audio_seconds=total_audio / sample_count,
                realtime_factor=(total_latency / total_audio) if total_audio else 0.0,
            )
        )

    return sorted(summary, key=lambda row: (row.avg_wer, -row.locality_exact_match_rate))

# The aggregate_by_condition function groups predictions by both model and condition tags, calculating average metrics for each unique combination. It returns a list of dictionaries containing the model, condition tag, sample count, average WER, average CER, locality exact match rate, locality token recall, and average latency in seconds for each group. The results are sorted by model and condition tag for easier analysis.
def aggregate_by_condition(predictions: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in predictions:
        for tag in str(row["condition_tags"]).split("|"):
            clean_tag = tag.strip()
            if clean_tag:
                grouped[(str(row["model"]), clean_tag)].append(row)

    results: list[dict[str, object]] = []
    for (model, tag), rows in sorted(grouped.items()):
        count = len(rows)
        results.append(
            {
                "model": model,
                "condition_tag": tag,
                "samples": count,
                "avg_wer": sum(float(row["wer"]) for row in rows) / count,
                "avg_cer": sum(float(row["cer"]) for row in rows) / count,
                "locality_exact_match_rate": sum(float(row["locality_exact_match"]) for row in rows) / count,
                "locality_token_recall": sum(float(row["locality_token_recall"]) for row in rows) / count,
                "avg_latency_seconds": sum(float(row["latency_seconds"]) for row in rows) / count,
            }
        )

    return results

# ASR Shootout - Intern Assessment

This repository is a reproducible benchmark kit for evaluating ASR systems on Bangalore locality names spoken in natural Hindi, Hinglish, or Kannada sentences.

It is designed to satisfy the assignment deliverables:

1. `data/recordings/` for your self-recorded audio files
2. A Python benchmark pipeline for multiple ASR systems
3. A concise report template in `report/`
4. Walkthrough notes in `report/walkthrough_notes.md`

## Recommended benchmark setup

- Baseline: Deepgram
- Comparator 1: `faster-whisper` small
- Comparator 2: `faster-whisper` large-v3

This gives you one production API baseline plus two open-source local baselines with different quality/speed tradeoffs.

## Project structure

```text
data/
  recordings/              # Put your .wav/.mp3/.m4a files here
  references/
    localities.csv         # Full locality list from the assignment PDF
    metadata_template.csv  # Template to fill with file paths + gold transcripts
report/
  report_template.md
  walkthrough_notes.md
results/                   # Generated benchmark outputs
src/asr_benchmark/
tests/
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For PowerShell in this repo, set:

```powershell
$env:PYTHONPATH = "src"
```

Create a `.env` file from `.env.example`.

## Recordings

This repo preserves all 30 in `data/references/localities.csv`.

- Recorded at least 20 files
- Filled in `data/references/metadata_template.csv`
- Kept the `expected_locality` column aligned to the spoken locality


## Running the benchmark

Deepgram + local Whisper:

```bash
python -m asr_benchmark.cli run ^
  --dataset data/references/metadata_template.csv ^
  --output-dir results/run_01 ^
  --model deepgram ^
  --model faster_whisper_small ^
  --model faster_whisper_large
```

Generate a markdown summary from an existing predictions file:

```bash
python -m asr_benchmark.cli summarize ^
  --predictions results/run_01/predictions.csv ^
  --output results/run_01/summary.md
```

Validate your dataset before a run:

```bash
python -m asr_benchmark.cli validate ^
  --dataset data/references/metadata_template.csv
```

## Outputs

Each run writes:

- `predictions.csv`: one row per sample per model
- `aggregate_metrics.csv`: model-level metrics
- `condition_metrics.csv`: metrics by environment tag
- `summary.md`: report-ready benchmark summary

## Notes

- `faster-whisper` will download models on first run.
- Deepgram requires `DEEPGRAM_API_KEY`.
- You can add more model adapters later without changing the evaluation logic.

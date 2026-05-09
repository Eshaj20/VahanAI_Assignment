# Submission Checklist

- Record at least 20 real audio samples in mixed conditions
- Replace placeholder transcripts in `data/references/metadata_template.csv` with the exact spoken sentences
- Keep `expected_locality` aligned to the target locality
- Create `.env` from `.env.example`
- Install dependencies with `pip install -r requirements.txt`
- Run `python -m asr_benchmark.cli validate --dataset data/references/metadata_template.csv`
- Run the benchmark against `deepgram`, `faster_whisper_small`, and `faster_whisper_large`
- Copy the strongest tables and examples into `report/report_template.md`
- Fill `report/walkthrough_notes.md` with your actual surprises and recommendation
- Double-check that the final submission includes audio, code, and the finished report

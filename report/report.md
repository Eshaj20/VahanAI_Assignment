# ASR Shootout Report

## Objective

Evaluate ASR systems on self-recorded Bangalore locality utterances spoken in natural Hindi, Hinglish, and Kannada-style conditions relevant to a phone-first hiring workflow.

## Benchmark Setup

- Dataset: 20 self-recorded locality utterances
- Conditions: quiet indoor, traffic noise, outdoor noise, rushed speech, whisper, phone-call/compressed audio
- Baseline: Deepgram `nova-2`
- Comparators: `faster-whisper` small and `faster-whisper` large-v3

## Important Evaluation Note

The Whisper models often returned Hindi in Devanagari script, while the references were written in Latin-script Hinglish. To avoid unfairly penalizing those outputs, I rescored the predictions with a lightweight Devanagari-to-Latin normalization step. This makes the comparison closer to the true recognition quality of the models.

## Overall Results

| Model | Samples | Avg WER | Avg CER | Locality EM | Avg Latency (s) | Real-Time Factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Deepgram nova-2 | 20 | 0.921 | 0.864 | 0.20 | 4.40 | 0.98 |
| Faster-Whisper Small | 20 | 0.882 | 0.468 | 0.25 | 12.51 | 2.79 |
| Faster-Whisper Large | 20 | 0.818 | 0.510 | 0.35 | 66.19 | 14.74 |

## Interpretation

- `faster-whisper large` gave the best locality capture and the lowest WER, but it was by far the slowest model.
- `Deepgram` was the fastest system and the only one close to real time on this setup, but its locality recall on this dataset was weak.
- `faster-whisper small` did not justify itself strongly in this run. It was much slower than Deepgram without a large enough quality gain.

## Failure Analysis

### 1. Script mismatch can hide actual ASR quality

Whisper often produced semantically correct Hindi transcripts, but in Devanagari or close phonetic Hindi. The example below is shown in transliterated Latin script for readability:

- Reference: `Haan, main Koramangala mein rehta hoon`
- Whisper Large: `haan, main koramangala mein rahti hoon`

The locality is clearly present, but naive Latin-script scoring marks this as wrong. This was the main reason I rescored the saved predictions.

### 2. Deepgram often returned partial or empty outputs on short clips

Examples:

- `Koramangala`: empty transcript
- `Indiranagar`: empty transcript
- `Whitefield`: `Whitefield side.`
- `Electronic City`: `Electronic city`

This suggests the short, noisy, mixed-language clips were difficult for the baseline in its current configuration.

### 3. Traffic and rushed speech were not the worst case for Whisper Large

For `faster-whisper large`, the strongest locality exact match rates came from:

- `rushed`: `1.0` on 2 samples
- `traffic`: `0.6` on 5 samples

The weaker conditions were:

- `whisper`: `0.0`
- `noise`: `0.0`
- `quiet`: `0.167`

This was surprising. The dataset is small, so I would treat condition-level conclusions as directional rather than definitive.

### 4. Near-miss locality spellings are a real product risk

Even when the model was directionally correct, it often altered the locality:

- `Indiranagar` -> `indra nagar`
- `Marathahalli` -> `marthali`
- `Hebbal` -> `hebal`
- `Koramangala` -> `kor mangla`

For an address-extraction workflow, these near-misses matter because downstream entity matching may fail unless fuzzy normalization is added.

## Recommendation

If I had to choose one production starting point from this benchmark alone for a latency-sensitive telephony workflow, I would start with `Deepgram` for operational simplicity and near-real-time latency. Its speed is attractive for telephony, but locality capture here was not strong enough to treat as solved.

If self-hosting is acceptable and locality accuracy is the top priority, `faster-whisper large` is the stronger model in this benchmark. The tradeoff is severe latency: roughly `14.7x` real time on this machine, which makes direct production use difficult without stronger hardware or asynchronous processing.

In practice, my recommendation would be:

- Use `Deepgram` if low-latency telephony integration and operational simplicity matter more than raw locality accuracy.
- Use `faster-whisper large` if you can tolerate much higher latency and want the best locality accuracy from this benchmark.
- Add fuzzy locality normalization downstream regardless of the ASR choice, because near-miss spellings were common across models.

## What Surprised Me

- The best accuracy model was dramatically slower than the others.
- Deepgram, despite being the production API baseline, produced several empty or partial transcripts on these clips.
- Script mismatch created a misleading first impression until the scoring was corrected.

## Limitations

- Only 20 samples
- Likely single speaker
- No public open-source dataset added yet
- Benchmark is batch ASR, not a full conversational streaming test
- The rescoring normalization is lightweight and not a full Hindi transliteration system

## Next Steps

- Add 2 to 3 more speakers with different accents
- Add a public Hindi or Hindi-English code-switched dataset
- Evaluate fuzzy entity matching downstream from raw ASR
- Test more Deepgram settings and at least one additional API ASR system

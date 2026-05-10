# ASR Shootout Report

## Objective

Evaluate ASR systems on self-recorded Bangalore locality utterances spoken in natural Hindi, Hinglish, and Kannada-style conditions relevant to a phone-first hiring workflow.

## Benchmark Setup

- Dataset: 40 self-recorded locality utterances
- Conditions: 20 quiet indoor clips, 10 traffic/outdoor clips, 10 phone-call/compressed clips
- Baseline: Deepgram `nova-2`
- Comparators: `faster-whisper` small and `faster-whisper` large-v3

## Important Evaluation Note

The Whisper models often returned Hindi in Devanagari script, while the references were written in Latin-script Hinglish. To avoid unfairly penalizing those outputs, I rescored the predictions with a lightweight Devanagari-to-Latin normalization step. This makes the comparison closer to the true recognition quality of the models.

## Overall Results

| Model | Samples | Avg WER | Avg CER | Locality EM | Avg Latency (s) | Real-Time Factor |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Deepgram nova-2 | 40 | 0.924 | 0.884 | 0.15 | 5.49 | 1.26 |
| Faster-Whisper Small | 40 | 0.877 | 0.445 | 0.20 | 24.77 | 5.69 |
| Faster-Whisper Large | 40 | 0.810 | 0.454 | 0.40 | 125.40 | 28.79 |

## Interpretation

- `faster-whisper large` gave the best locality capture and the lowest WER, but it was by far the slowest model.
- `Deepgram` was the fastest system and the only one close to real time on this setup, but its locality recall on this dataset was weak.
- `faster-whisper small` improved on Deepgram's text accuracy, but not enough to become the most attractive tradeoff. It remained substantially slower while still trailing Whisper Large on locality capture.

## Failure Analysis

### 1. Script mismatch can hide actual ASR quality

Whisper often produced semantically correct Hindi transcripts, but in Devanagari or close phonetic Hindi. The example below is shown in transliterated Latin script for readability:

- Reference: `Haan, main Koramangala mein rehti hoon`
- Whisper Large: `haan, main koramangala mein rahti hoon`

The locality is clearly present, but naive Latin-script scoring marks this as wrong. This was the main reason I rescored the saved predictions.

### 2. Deepgram often returned partial or empty outputs on short clips

Examples:

- `Koramangala`: empty transcript
- `Indiranagar`: empty transcript
- `Whitefield`: `Whitefield side.`
- `Electronic City`: `Electronic city`

This pattern remained visible after expanding to 40 samples. It suggests the short, mixed-language clips were difficult for the baseline in its current configuration.

### 3. Traffic and phone-call audio changed the picture in useful ways

On the expanded dataset:

- `Deepgram` performed slightly better on `phonecall|compressed` than on `traffic|outdoor`
  - phonecall locality EM: `0.20`
  - traffic locality EM: `0.00`
- `faster-whisper large` held up better than Deepgram on both added conditions
  - phonecall locality EM: `0.40`
  - traffic locality EM: `0.50`

### 4. Near-miss locality spellings are a real product risk

Even when the model was directionally correct, it often altered the locality:

- `Indiranagar` -> `indra nagar`
- `Marathahalli` -> `marthali`
- `Hebbal` -> `hebal`
- `Koramangala` -> `kor mangla`

For an address-extraction workflow, these near-misses matter because downstream entity matching may fail unless fuzzy normalization is added.

## Recommendation

If I had to choose one production starting point from this benchmark alone for a latency-sensitive telephony workflow, I would still start with `Deepgram` for operational simplicity and lower latency. However, the 40-sample benchmark makes the quality gap more obvious: it was the weakest model on both WER and locality exact match.

If self-hosting is acceptable and locality accuracy is the top priority, `faster-whisper large` is the strongest model in this benchmark. The tradeoff is severe latency: roughly `28.8x` real time on this machine, which makes direct production use difficult without stronger hardware or asynchronous processing.

In practice, my recommendation would be:

- Use `Deepgram` if low-latency telephony integration and operational simplicity matter more than raw locality accuracy.
- Use `faster-whisper large` if you can tolerate much higher latency and want the best locality accuracy from this benchmark.
- Add fuzzy locality normalization downstream regardless of the ASR choice, because near-miss spellings were common across models.

## What Surprised Me

- The best accuracy model was dramatically slower than the others.
- Deepgram, despite being the production API baseline, produced several empty or partial transcripts on these clips.
- Script mismatch created a misleading first impression until the scoring was corrected.
- Adding real traffic and phone-call recordings strengthened the case for condition-aware evaluation instead of relying on a single clean recording set.

## Limitations

- Only 40 samples
- Only a single speaker
- No public open-source dataset added yet
- Benchmark is batch ASR, not a full conversational streaming test
- The rescoring normalization is lightweight and not a full Hindi transliteration system

## Next Steps

- Addition of 2 to 3 more speakers with different accents
- Adding a public Hindi or Hindi-English code-switched dataset
- Evaluating fuzzy entity matching downstream from raw ASR
- Testing more Deepgram settings and at least one additional API ASR system

# ASR Shootout Report

## Objective

Evaluate ASR systems on real-world Bangalore locality utterances spoken in natural Hindi, Hinglish, or Kannada conditions relevant to a phone-first hiring platform.

## Setup

- Dataset: self-recorded locality utterances
- Minimum set evaluated: 20 samples
- Baseline: Deepgram
- Comparators: `faster-whisper` small, `faster-whisper` large-v3
- Conditions covered: quiet indoor, traffic noise, compressed phone-call audio, whispered, rushed

Note: the assignment PDF says "20 samples" but lists 30 locality names. I used 20 as the required minimum and preserved the full 30-name list for traceability.

## Why These Models

- Deepgram is the required baseline and represents a production-grade API system.
- `faster-whisper` small is a lightweight local model that tests the quality floor for cheap deployment.
- `faster-whisper` large-v3 is a stronger open-source checkpoint that tests the quality ceiling achievable without an external API.

This mix lets us compare quality, latency, and deployment tradeoffs rather than just model families.

## Metrics

- Word Error Rate: general transcript accuracy
- Character Error Rate: more sensitive to spelling distortions
- Locality Exact Match: whether the key entity appeared correctly in the transcript
- Locality Token Recall: partial credit for multi-token names like `HSR Layout` and `Electronic City`
- Latency and Real-Time Factor: practical deployment signals for telephony workflows

WER alone is insufficient here because a transcript can have minor function-word errors and still preserve the locality correctly, or look fluent while silently corrupting the entity.

## Key Results

Paste the core table from `results/.../summary.md` here.

| Model | Avg WER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deepgram | TBD | TBD | TBD | TBD | TBD |
| Faster-Whisper Small | TBD | TBD | TBD | TBD | TBD |
| Faster-Whisper Large | TBD | TBD | TBD | TBD | TBD |

## Failure Analysis

Focus on concrete patterns:

- Which names were consistently mangled?
- Did code-switched English locality names inside Hindi sentences confuse the models?
- Did phone-call compression hurt more than street noise?
- Did short utterances or rushed speech reduce locality capture?

Useful examples:

1. Reference: `Mera address HSR Layout mein hai`
   Deepgram: `...`
   Whisper Large: `...`
   Why it matters: `HSR` is short, spelled like letters, and easy to distort.

2. Reference: `Main Electronic City mein kaam karta hoon`
   Deepgram: `...`
   Whisper Small: `...`
   Why it matters: multi-token English place names may be normalized incorrectly.

## Recommendation

Choose one clear production recommendation and one fallback:

- If accuracy on locality extraction is the main priority: `TBD`
- If low infra complexity and fast iteration matter more: `TBD`
- If cost sensitivity dominates and local deployment is acceptable: `TBD`

Example framing:

`I would start with Deepgram for the production baseline because it minimizes deployment overhead and is likely to be more robust on noisy multilingual speech out of the box. If cost or data residency pushes us toward self-hosting, I would test Faster-Whisper Large next, while accepting a latency and compute tradeoff.`

## Limitations

- Small sample size
- Single speaker unless you record multiple speakers
- Locality-heavy task, not full-call ASR
- No rigorous large-scale cost study
- Optional open datasets not included unless explicitly benchmarked

## Next Steps

- Expand to more speakers and accents
- Add a public Hindi code-switched dataset
- Measure streaming performance separately from batch performance
- Evaluate downstream entity extraction, not just raw transcripts

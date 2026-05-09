# 10-Minute Walkthrough Notes

## 1. Problem framing

This is not a generic ASR task. The production problem is whether the system can capture high-value entities like locality names from noisy, code-switched telephony audio.

## 2. Dataset choice

- I created a self-recorded benchmark because the assignment emphasizes realistic candidate speech.
- I varied room noise, traffic, rushed delivery, whispering, and phone-call compression.
- I tracked both full-transcript accuracy and locality capture.

## 3. Model choice

- Deepgram as the required baseline
- Faster-Whisper Small as a cheap deployable open-source baseline
- Faster-Whisper Large as a stronger quality-oriented open-source comparator

## 4. Why these metrics

- WER and CER for transcript quality
- Locality exact match because business value depends on not missing the place name
- Locality token recall for multi-token names
- Latency and real-time factor for deployability

## 5. What surprised me

- `faster-whisper large` was the most accurate model, but it was dramatically slower than the rest.
- Deepgram was the only model close to real time, but it returned several empty or partial transcripts on short mixed-language clips.
- The first pass of scoring made Whisper look worse than it really was because it produced Devanagari output while the references were written in Latin script.

## 6. Recommendation

- Primary recommendation: start with Deepgram only when production latency and integration simplicity matter more than raw locality accuracy.
- Accuracy-oriented backup: use `faster-whisper large` if self-hosting is acceptable and higher latency is tolerable.
- Important product note: add fuzzy locality normalization downstream, because several outputs were close but not exact.

## 7. Limitations

- Small dataset
- Mostly one speaker unless expanded
- Benchmark is batch ASR, not a full conversational streaming test

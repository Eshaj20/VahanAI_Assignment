# Benchmark Summary

## Overall Metrics

| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| faster_whisper_large | 40 | 0.810 | 0.454 | 0.400 | 0.075 | 125.398 | 28.790 |

## Condition Breakdown

| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| faster_whisper_large | compressed | 10 | 0.768 | 0.400 | 136.543 |
| faster_whisper_large | indoor | 20 | 0.818 | 0.350 | 122.062 |
| faster_whisper_large | outdoor | 10 | 0.836 | 0.500 | 120.925 |
| faster_whisper_large | phonecall | 10 | 0.768 | 0.400 | 136.543 |
| faster_whisper_large | quiet | 20 | 0.818 | 0.350 | 122.062 |
| faster_whisper_large | traffic | 10 | 0.836 | 0.500 | 120.925 |

# Benchmark Summary

## Overall Metrics

| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| faster_whisper_large | 20 | 0.818 | 0.504 | 0.350 | 0.050 | 66.188 | 14.739 |

## Condition Breakdown

| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| faster_whisper_large | compressed | 5 | 0.803 | 0.400 | 65.263 |
| faster_whisper_large | indoor | 8 | 0.899 | 0.250 | 68.026 |
| faster_whisper_large | noise | 2 | 0.900 | 0.000 | 63.029 |
| faster_whisper_large | outdoor | 6 | 0.741 | 0.333 | 65.974 |
| faster_whisper_large | phonecall | 5 | 0.803 | 0.400 | 65.263 |
| faster_whisper_large | quiet | 6 | 0.926 | 0.167 | 70.955 |
| faster_whisper_large | rushed | 2 | 0.774 | 1.000 | 59.151 |
| faster_whisper_large | traffic | 5 | 0.672 | 0.600 | 65.434 |
| faster_whisper_large | whisper | 1 | 0.800 | 0.000 | 57.558 |

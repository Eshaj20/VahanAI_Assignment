# Benchmark Summary

## Overall Metrics

| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| faster_whisper_small | 40 | 0.877 | 0.445 | 0.200 | 0.000 | 24.765 | 5.686 |

## Condition Breakdown

| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| faster_whisper_small | compressed | 10 | 0.897 | 0.100 | 22.655 |
| faster_whisper_small | indoor | 20 | 0.882 | 0.200 | 26.199 |
| faster_whisper_small | outdoor | 10 | 0.845 | 0.300 | 24.007 |
| faster_whisper_small | phonecall | 10 | 0.897 | 0.100 | 22.655 |
| faster_whisper_small | quiet | 20 | 0.882 | 0.200 | 26.199 |
| faster_whisper_small | traffic | 10 | 0.845 | 0.300 | 24.007 |

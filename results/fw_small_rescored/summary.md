# Benchmark Summary

## Overall Metrics

| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| faster_whisper_small | 20 | 0.882 | 0.468 | 0.250 | 0.000 | 12.512 | 2.786 |

## Condition Breakdown

| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| faster_whisper_small | compressed | 5 | 0.825 | 0.200 | 11.931 |
| faster_whisper_small | indoor | 8 | 0.957 | 0.250 | 13.610 |
| faster_whisper_small | noise | 2 | 0.817 | 0.500 | 10.602 |
| faster_whisper_small | outdoor | 6 | 0.858 | 0.167 | 11.563 |
| faster_whisper_small | phonecall | 5 | 0.825 | 0.200 | 11.931 |
| faster_whisper_small | quiet | 6 | 1.004 | 0.167 | 14.371 |
| faster_whisper_small | rushed | 2 | 0.774 | 1.000 | 11.541 |
| faster_whisper_small | traffic | 5 | 0.846 | 0.200 | 12.100 |
| faster_whisper_small | whisper | 1 | 0.800 | 0.000 | 11.893 |

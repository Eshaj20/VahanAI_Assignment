# Benchmark Summary

## Overall Metrics

| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| deepgram_nova-2 | 40 | 0.924 | 0.884 | 0.150 | 0.138 | 5.490 | 1.261 |

## Condition Breakdown

| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| deepgram_nova-2 | compressed | 10 | 0.902 | 0.200 | 5.485 |
| deepgram_nova-2 | indoor | 20 | 0.921 | 0.200 | 6.386 |
| deepgram_nova-2 | outdoor | 10 | 0.950 | 0.000 | 3.706 |
| deepgram_nova-2 | phonecall | 10 | 0.902 | 0.200 | 5.485 |
| deepgram_nova-2 | quiet | 20 | 0.921 | 0.200 | 6.386 |
| deepgram_nova-2 | traffic | 10 | 0.950 | 0.000 | 3.706 |

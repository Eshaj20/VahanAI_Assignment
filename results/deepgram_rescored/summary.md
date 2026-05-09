# Benchmark Summary

## Overall Metrics

| Model | Samples | Avg WER | Avg CER | Locality EM | Locality Token Recall | Avg Latency (s) | RTF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| deepgram_nova-2 | 20 | 0.921 | 0.864 | 0.200 | 0.200 | 4.397 | 0.979 |

## Condition Breakdown

| Model | Condition | Samples | Avg WER | Locality EM | Avg Latency (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| deepgram_nova-2 | compressed | 5 | 0.867 | 0.200 | 4.721 |
| deepgram_nova-2 | indoor | 8 | 0.964 | 0.125 | 4.865 |
| deepgram_nova-2 | noise | 2 | 0.900 | 0.500 | 2.611 |
| deepgram_nova-2 | outdoor | 6 | 0.967 | 0.167 | 3.696 |
| deepgram_nova-2 | phonecall | 5 | 0.867 | 0.200 | 4.721 |
| deepgram_nova-2 | quiet | 6 | 0.952 | 0.167 | 4.488 |
| deepgram_nova-2 | rushed | 2 | 0.786 | 0.500 | 6.143 |
| deepgram_nova-2 | traffic | 5 | 0.914 | 0.200 | 4.040 |
| deepgram_nova-2 | whisper | 1 | 1.000 | 0.000 | 2.946 |

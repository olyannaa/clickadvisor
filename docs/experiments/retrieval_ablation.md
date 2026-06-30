# Retrieval Ablation

## Snapshot

- Date: 2026-06-30
- Query set: `20` synthetic benchmark queries with expected rule labels
- KB sample: first `2000` chunks from `data/kb/chunks` out of `8804`
- Metric: `MRR@3`
- Scoring: explicit rule-to-doc gold URL fragments or keyword references
- Command:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

## Results

| Model | Size | Queries | MRR@3 | Time (s) |
|---|---:|---:|---:|---:|
| multilingual-e5-small (current) | 117 MB | 20 | 0.458 | 17.7 |
| all-MiniLM-L6-v2 | 80 MB | 20 | 0.517 | 10.4 |
| paraphrase-multilingual-MiniLM-L12-v2 | 420 MB | 20 | 0.242 | 12.4 |

Results were saved to
`eval/results/retrieval_ablation_20260630T124602Z/`.

## Interpretation

The repaired metric no longer counts an arbitrary high-scoring ClickHouse chunk
as relevant. A retrieved chunk must match an explicit gold reference for one of
the expected rules.

MiniLM-L6 is strongest on this English-heavy KB sample. The default can still
remain multilingual E5 when Russian queries and multilingual KB growth matter
more than this small English ablation.

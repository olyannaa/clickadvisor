# Knowledge Base Layout

`data/kb/` stores raw and processed ClickHouse knowledge base artifacts used by
the retrieval advisory layer in ClickAdvisor.

## Directory structure

- `raw/` stores source captures before conversion
- `markdown/` stores markdown-normalized source documents
- `chunks/` stores chunked markdown files with YAML frontmatter
- `logs/` stores crawl and validation diagnostics such as skipped URLs

The KB pipeline:

1. crawl raw source material into `raw/`
2. convert each source page into markdown in `markdown/`
3. split markdown into retrieval-friendly chunks in `chunks/`
4. validate metadata, duplicates, and links
5. index chunks into embedded Qdrant with `chadvisor index-kb`

## Source coverage

The initial source set is:

- `docs.clickhouse.com`
- `kb.altinity.com`
- `clickhouse.com/blog` with engineering-focused filtering
- `github.com/ClickHouse/ClickHouse/releases`

## How to refresh source material

Manual refresh flow:

```bash
python scripts/kb/crawler.py
python scripts/kb/chunker.py
python scripts/kb/validator.py
```

Filtered source refresh:

```bash
python scripts/kb/crawler.py --source docs.clickhouse.com
python scripts/kb/crawler.py --source github.com/ClickHouse/ClickHouse/releases
```

## How to build the retrieval index

Default multilingual index:

```bash
poetry run chadvisor index-kb
```

Rebuild an existing index:

```bash
poetry run chadvisor index-kb --reindex
```

Choose the embedding model:

```bash
poetry run chadvisor index-kb --embedding-model multilingual-e5-small
poetry run chadvisor index-kb --embedding-model minilm-l6
```

The index is stored in `.qdrant_db` by default and uses collection
`clickadvisor_kb`.

## Embedding models

| Key | Model | Size | Language coverage | Prefixes |
|---|---|---:|---|---|
| `multilingual-e5-small` | `intfloat/multilingual-e5-small` | 117 MB | multilingual | `query:` / `passage:` |
| `minilm-l6` | `sentence-transformers/all-MiniLM-L6-v2` | 80 MB | English-only | none |

`multilingual-e5-small` is the default. `minilm-l6` is available for
English-only installations and had better MRR@3 on the current English-heavy KB.
See `docs/adr/ADR-013-embedding-model-selection.md`.

## Metadata contract

Each chunk file in `chunks/` contains YAML frontmatter with:

- `source`
- `url`
- `topic`
- `ch_version_introduced`
- `last_updated`
- `chunk_index`
- `total_chunks_in_doc`

At indexing time, `ch_version_introduced` is normalized into Qdrant payload field
`ch_version` only if it matches `^\d{1,2}\.\d{1,2}$`. Invalid values such as URLs,
IP-like strings, or patch versions are stored as an empty string.

## Retrieval behavior

The retriever:

- embeds semantic queries built from fired rule IDs, not raw SQL text
- uses score threshold `0.65`
- returns top 3 chunks by default
- applies a score diversity guard: if top-3 scores are effectively identical,
  it logs a warning and returns only the first chunk

Retrieved chunks are converted into findings with `tier="rag"` and are rendered
separately from deterministic rule findings.

## Expected scale

The repository currently contains approximately 8804 KB chunks. The exact number
changes as sources evolve.

Planning estimate by source family:

- `docs.clickhouse.com`: several thousand chunks
- `kb.altinity.com`: hundreds to low thousands of chunks
- `clickhouse.com/blog`: hundreds of chunks
- `github releases`: hundreds of chunks

Ablation experiments may index a subset for speed; the current script uses the
first 2000 chunks and notes that full-index runs are expected to improve MRR@3.

## Notes

- The crawler saves raw HTML for web documents and raw Markdown for GitHub
  release notes so conversion bugs can be debugged without re-fetching.
- The validator should pass before indexing.
- Full refreshes may take time depending on network conditions and source size.

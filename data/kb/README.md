# Knowledge Base Layout

`data/kb/` stores the raw and processed ClickHouse knowledge base artifacts used
to build the retrieval layer for ClickAdvisor.

## Directory structure

- `raw/` stores the source capture before chunking
- `markdown/` stores markdown-normalized source documents
- `chunks/` stores chunked markdown files with YAML frontmatter
- `logs/` stores crawl and validation diagnostics such as skipped URLs

The KB is designed as a staged pipeline:

1. crawl raw source material into `raw/`
2. convert each source page into markdown in `markdown/`
3. split markdown into retrieval-friendly chunks in `chunks/`
4. validate metadata, duplicates, and links before indexing

## Source coverage

The initial source set is:

- `docs.clickhouse.com`
- `kb.altinity.com`
- `clickhouse.com/blog` with engineering-focused filtering
- `github.com/ClickHouse/ClickHouse/releases` for the latest 36 releases

## How to refresh

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

## Metadata contract

Each chunk file in `chunks/` contains YAML frontmatter with:

- `source`
- `url`
- `topic`
- `ch_version_introduced`
- `last_updated`
- `chunk_index`
- `total_chunks_in_doc`

This metadata is used by later retrieval, ranking, and version-aware filtering.

## Version-aware indexing

Chunks derived from `github_releases` carry a frontmatter field `ch_version`.
This makes it possible to filter retrieval results against the known
ClickHouse version of the user so that release-note evidence can be narrowed to
the most relevant engine generation.

In practice, when the analysis pipeline already knows the user's server version,
the retriever can prefer or restrict release-note chunks whose `ch_version`
matches the applicable release window instead of mixing in notes from unrelated
versions.

## Expected scale

The exact numbers change as sources evolve, but a reasonable planning estimate
for a full refresh is:

- `docs.clickhouse.com`: 3,000-5,000 chunks
- `kb.altinity.com`: 700-1,200 chunks
- `clickhouse.com/blog`: 200-500 chunks
- `github releases`: 100-250 chunks

Total expected KB size after chunking: roughly 4,000-7,000 chunks.

## Notes

- The crawler saves raw HTML for web documents and raw Markdown for GitHub
  release notes so that conversion bugs can be debugged without re-fetching the
  source.
- The validator should pass before any indexing job consumes KB content.
- Full refreshes may take hours depending on network conditions and source size.

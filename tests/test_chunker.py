from pathlib import Path

from scripts.kb.chunker import build_chunks, chunk_document, detect_version, split_markdown_blocks


def test_split_markdown_blocks_keeps_code_block_together() -> None:
    markdown = """# Example

Intro paragraph.

```sql
SELECT *
FROM table
WHERE id = 1;
```

After code.
"""
    blocks = split_markdown_blocks(markdown)
    assert any("```sql" in block and "WHERE id = 1" in block for block in blocks)


def test_build_chunks_keeps_table_together() -> None:
    markdown = """# Metrics

| col_a | col_b |
| --- | --- |
| 1 | 2 |
| 3 | 4 |

    """ + ("word " * 900)
    chunks = build_chunks(markdown, token_target=120, overlap=20)
    assert len(chunks) >= 2
    table_chunk = next(chunk for chunk in chunks if "| col_a | col_b |" in chunk)
    assert "| 3 | 4 |" in table_chunk


def test_detect_version_prefers_first_clickhouse_style_version() -> None:
    markdown = "Feature available since ClickHouse 24.8 and updated again in 25.1."
    assert detect_version(markdown) == "24.8"


def test_chunk_document_writes_frontmatter_and_multiple_chunks(tmp_path: Path) -> None:
    input_root = tmp_path / "markdown"
    source_dir = input_root / "docs.clickhouse.com"
    source_dir.mkdir(parents=True)
    output_root = tmp_path / "chunks"
    markdown_path = source_dir / "aggregate-functions.md"
    markdown_path.write_text(
        "# Aggregate Functions\n\n"
        "Canonical URL: https://docs.clickhouse.com/docs/sql-reference/aggregate-functions/\n\n"
        + ("Paragraph text " * 1200),
        encoding="utf-8",
    )

    written = chunk_document(markdown_path, input_root, output_root)
    assert len(written) >= 2
    first_chunk = written[0].read_text(encoding="utf-8")
    assert first_chunk.startswith("---\nsource: docs.clickhouse.com")
    assert "topic: aggregate-functions" in first_chunk

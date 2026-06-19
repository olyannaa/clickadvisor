from pathlib import Path

import pytest

from scripts.kb.validator import deduplicate_chunk_tree, split_frontmatter, validate_chunk_tree


def make_chunk(path: Path, body: str, *, url: str = "https://example.com/page") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"source: docs.clickhouse.com\n"
        f"url: {url}\n"
        "topic: sample-topic\n"
        "ch_version_introduced: auto\n"
        "last_updated: 2026-05-25\n"
        "chunk_index: 1\n"
        "total_chunks_in_doc: 1\n"
        "---\n\n"
        f"{body}\n",
        encoding="utf-8",
    )


def test_split_frontmatter_parses_yaml_and_body() -> None:
    frontmatter, body = split_frontmatter(
        "---\nsource: docs.clickhouse.com\nurl: https://example.com\n"
        "topic: test\nch_version_introduced: auto\nlast_updated: 2026-05-25\n"
        "chunk_index: 1\ntotal_chunks_in_doc: 1\n---\n\nBody text"
    )
    assert frontmatter["source"] == "docs.clickhouse.com"
    assert body == "Body text"


def test_validator_accepts_valid_chunk(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "chunks"
    make_chunk(root / "docs.clickhouse.com" / "sample" / "001.md", "Body with [link](#anchor).")
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert issues == []


def test_validator_reports_duplicate_content(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "chunks"
    make_chunk(root / "a" / "sample" / "001.md", "Same body.")
    make_chunk(root / "b" / "sample" / "002.md", "Same body.")
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert any("duplicate content hash" in issue.message for issue in issues)


def test_validator_reports_broken_local_link(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "chunks"
    make_chunk(root / "docs" / "sample" / "001.md", "Broken [local](missing.md) link.")
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert any("broken local link" in issue.message for issue in issues)


def test_validator_accepts_root_relative_site_link(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = tmp_path / "chunks"
    make_chunk(
        root / "kb.altinity.com" / "sample" / "001.md",
        "Body with [site link](/using-this-knowledgebase/mermaid_example/).",
        url="https://kb.altinity.com/using-this-knowledgebase/",
    )
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert issues == []


def test_validator_accepts_dot_relative_site_link(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = tmp_path / "chunks"
    make_chunk(
        root / "kb.altinity.com" / "sample" / "001.md",
        "Body with [relative](./config-by-provider/).",
        url="https://kb.altinity.com/altinity-kb-setup-and-maintenance/example-page/",
    )
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert issues == []


def test_validator_accepts_parent_relative_site_link(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = tmp_path / "chunks"
    make_chunk(
        root / "kb.altinity.com" / "sample" / "001.md",
        "Body with [parent](../altinity-kb-zookeeper/zookeeper-monitoring/).",
        url="https://kb.altinity.com/altinity-kb-setup-and-maintenance/example-page/",
    )
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert issues == []


def test_validator_accepts_slug_relative_site_link(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = tmp_path / "chunks"
    make_chunk(
        root / "kb.altinity.com" / "sample" / "001.md",
        "Body with [slug](altinity-kb-how-to-test-different-compression-codecs).",
        url="https://kb.altinity.com/altinity-kb-schema-design/example-page/",
    )
    monkeypatch.setattr("scripts.kb.validator.requests.Session", lambda: object())
    issues = validate_chunk_tree(root)
    assert issues == []


def test_dedup_keeps_first_file_in_sorted_order(tmp_path: Path) -> None:
    root = tmp_path / "chunks"
    keep = root / "a" / "001.md"
    drop = root / "b" / "002.md"
    make_chunk(keep, "Duplicate body.")
    make_chunk(drop, "Duplicate body.")

    deleted_count, remaining_count = deduplicate_chunk_tree(root)

    assert deleted_count == 1
    assert remaining_count == 1
    assert keep.exists()
    assert not drop.exists()

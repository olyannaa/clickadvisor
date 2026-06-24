from __future__ import annotations

from clickadvisor.retrieval.indexer import parse_frontmatter, validate_ch_version


def test_validate_ch_version_accepts_clickhouse_version() -> None:
    assert validate_ch_version("24.3") == "24.3"
    assert validate_ch_version("8.12") == "8.12"


def test_validate_ch_version_rejects_urls_ips_and_patch_versions() -> None:
    assert validate_ch_version("https://clickhouse.com/docs/23.8") == ""
    assert validate_ch_version("192.168") == ""
    assert validate_ch_version("24.3.1") == ""
    assert validate_ch_version("") == ""


def test_parse_frontmatter_validates_ch_version() -> None:
    metadata = parse_frontmatter(
        """---
source: docs
url: https://clickhouse.com/docs/24.3/foo
ch_version_introduced: https://clickhouse.com/docs/24.3/foo
---
Body
"""
    )

    assert metadata["ch_version_introduced"] == ""

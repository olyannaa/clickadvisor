from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_DEPRECATED_INDEX_RE = re.compile(
    r"\bINDEX\s+(\w+)\s+.*?\bTYPE\s+(ngrambf_v1|tokenbf_v1)\b",
    re.IGNORECASE | re.DOTALL,
)


class D018DeprecatedNgramBFIndex(Rule):
    rule_id = "D-018"
    name = "deprecated_ngrambf_tokenbf_index"
    tier = "detector"
    ch_version_introduced = "0.720"
    ch_version_deprecated = "26.2"

    def check(self, context: QueryContext) -> Finding | None:
        m = _DEPRECATED_INDEX_RE.search(context.sql)
        if not m:
            return None
        index_name = m.group(1)
        index_type = m.group(2)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="medium",
            description=(
                f"Skip index '{index_name}' использует TYPE {index_type}, "
                "который устарел в ClickHouse >= 26.2. "
                "Замените на text-индекс (инвертированный индекс)."
            ),
            suggestion=(
                f"Замените на: INDEX {index_name} <column> TYPE text GRANULARITY 1. "
                "Text-индекс детерминирован, поддерживает многотерминный поиск "
                "и не требует настройки размера n-gram/токенов."
            ),
            example_before=f"INDEX {index_name} message TYPE {index_type}(4, 1024, 2, 0) GRANULARITY 4",
            example_after=f"INDEX {index_name} message TYPE text GRANULARITY 1",
            explain_why=(
                f"{index_type} использует вероятностный Bloom filter с false positive rate. "
                "Text-индекс (инвертированный) более точен, масштабируется лучше "
                "и поддерживает детерминированный поиск по токенам."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )

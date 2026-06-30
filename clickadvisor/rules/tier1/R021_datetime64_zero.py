from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_DT64_ZERO_RE = re.compile(
    r"`?(\w+)`?\s+DateTime64\s*\(\s*0\s*(?:,\s*'[^']*')?\s*\)",
    re.IGNORECASE,
)


class R021DateTime64ZeroToDateTime(Rule):
    rule_id = "R-021"
    name = "datetime64_zero_to_datetime"
    tier = "1A"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        m = _DT64_ZERO_RE.search(sql)
        if not m:
            return None
        column = m.group(1)
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                f"Колонка '{column}' объявлена как DateTime64(0), "
                "что семантически эквивалентно DateTime. "
                "DateTime занимает 4 байта (UInt32) вместо 8 байт (Int64) DateTime64."
            ),
            suggestion=(
                f"Замените DateTime64(0) на DateTime для колонки '{column}'. "
                "Диапазон DateTime: 1970-01-01 — 2106-02-07 (UInt32 epoch)."
            ),
            example_before=f"CREATE TABLE t ({column} DateTime64(0)) ENGINE = MergeTree ORDER BY {column}",
            example_after=f"CREATE TABLE t ({column} DateTime) ENGINE = MergeTree ORDER BY {column}",
            explain_why=(
                "DateTime64(0) хранит эпох-секунды как Int64 (8 байт). "
                "DateTime хранит как UInt32 (4 байта). При precision=0 семантика совпадает."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )

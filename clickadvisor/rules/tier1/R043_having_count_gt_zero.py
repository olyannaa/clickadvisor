from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# Matches HAVING count() > 0 or HAVING count(*) > 0
_HAVING_COUNT_GT_ZERO_RE = re.compile(
    r"\bHAVING\s+count\s*\(\s*(?:\*|)\s*\)\s*>\s*0\b",
    re.IGNORECASE,
)


class R043HavingCountGtZero(Rule):
    rule_id = "R-043"
    name = "having_count_gt_zero_removal"
    tier = "1A"
    ch_version_introduced = "0.5"

    def check(self, context: QueryContext) -> Finding | None:
        if not _HAVING_COUNT_GT_ZERO_RE.search(context.sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="low",
            description=(
                "HAVING count() > 0 является тавтологией: "
                "после GROUP BY каждая группа содержит минимум одну строку. "
                "Условие никогда не отфильтровывает строки."
            ),
            suggestion="Удалите HAVING count() > 0 — оно не меняет результат",
            example_before="SELECT user_id, count() FROM events GROUP BY user_id HAVING count() > 0",
            example_after="SELECT user_id, count() FROM events GROUP BY user_id",
            explain_why=(
                "По определению GROUP BY: каждая результирующая строка соответствует "
                "хотя бы одной строке источника. Поэтому count() >= 1 всегда."
            ),
            confidence="provable",
            ch_version_introduced=self.ch_version_introduced,
        )

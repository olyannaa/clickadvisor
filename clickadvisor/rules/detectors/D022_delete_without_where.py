from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

# DELETE FROM table without WHERE
# Matches: DELETE FROM tablename (with optional whitespace at end)
_DELETE_NO_WHERE_RE = re.compile(
    r"\bDELETE\s+FROM\s+[\w.`\"]+\s*(?:;|\Z)",
    re.IGNORECASE,
)
# Also check that no WHERE follows
_DELETE_FROM_RE = re.compile(r"\bDELETE\s+FROM\s+[\w.`\"]+", re.IGNORECASE)
_WHERE_RE = re.compile(r"\bWHERE\b", re.IGNORECASE)


class D022DeleteWithoutWhere(Rule):
    rule_id = "D-022"
    name = "delete_from_without_where"
    tier = "detector"
    ch_version_introduced = "22.8"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql.strip()
        if not _DELETE_FROM_RE.search(sql):
            return None
        if _WHERE_RE.search(sql):
            return None
        # DELETE FROM without WHERE found
        m = _DELETE_FROM_RE.search(sql)
        table = m.group(0).replace("DELETE FROM", "").strip() if m else "table"
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                f"DELETE FROM {table} без WHERE-условия удаляет ВСЕ строки таблицы. "
                "Это деструктивная и медленная операция для ClickHouse."
            ),
            suggestion=(
                f"Если цель — очистить таблицу, используйте TRUNCATE TABLE {table} "
                "(намного быстрее — удаляет все parts метаданных). "
                "Если DELETE задуман для части строк, добавьте WHERE-предикат."
            ),
            example_before=f"DELETE FROM {table}",
            example_after=f"TRUNCATE TABLE {table}  -- если нужно очистить всё",
            explain_why=(
                "DELETE FROM без WHERE помечает все строки как deleted. "
                "Фактическое удаление происходит при merge. "
                "TRUNCATE TABLE мгновенно удаляет все parts и несравнимо быстрее."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )

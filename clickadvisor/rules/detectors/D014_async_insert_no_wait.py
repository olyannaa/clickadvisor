from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_INSERT_RE = re.compile(r"\bINSERT\b", re.IGNORECASE)
_ASYNC_INSERT_RE = re.compile(r"\basync_insert\s*=\s*1\b", re.IGNORECASE)
_WAIT_FLAG_RE = re.compile(r"\bwait_for_async_insert\s*=\s*1\b", re.IGNORECASE)


class D014AsyncInsertNoWait(Rule):
    rule_id = "D-014"
    name = "async_insert_without_wait_flag"
    tier = "detector"
    ch_version_introduced = "22.6"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _INSERT_RE.search(sql):
            return None
        if not _ASYNC_INSERT_RE.search(sql):
            return None
        if _WAIT_FLAG_RE.search(sql):
            return None
        return Finding(
            rule_id=self.rule_id,
            rule_name=self.name,
            tier=self.tier,
            severity="high",
            description=(
                "INSERT использует async_insert=1 без wait_for_async_insert=1. "
                "Клиент не получит подтверждения записи на диск."
            ),
            suggestion=(
                "Добавьте wait_for_async_insert=1 в блок SETTINGS, "
                "либо используйте синхронный INSERT, если потеря данных недопустима."
            ),
            example_before="INSERT INTO events SETTINGS async_insert=1 VALUES (1, 'click')",
            example_after="INSERT INTO events SETTINGS async_insert=1, wait_for_async_insert=1 VALUES (1, 'click')",
            explain_why=(
                "Без wait_for_async_insert=1 данные попадают в буфер, "
                "и при сбое сервера или переполнении буфера они будут потеряны без уведомления."
            ),
            confidence="advisory",
            ch_version_introduced=self.ch_version_introduced,
        )

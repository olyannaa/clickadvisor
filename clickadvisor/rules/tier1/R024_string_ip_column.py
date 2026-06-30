from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule

_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_STRING_COL_RE = re.compile(
    r"`?(\w+)`?\s+String\b",
    re.IGNORECASE,
)
_IP_NAME_PARTS = frozenset(
    ["ip", "addr", "address", "host", "peer", "remote", "client", "server",
     "src", "dst", "source", "destination"]
)

# Exact column names that strongly indicate IP
_IP_EXACT_SUFFIXES = ("_ip", "_addr", "_address", "_host", "_peer")
_IP_EXACT_NAMES = frozenset(
    ["ip", "remote_addr", "client_ip", "server_ip", "src_ip", "dst_ip",
     "ip_address", "remote_host", "peer_address", "client_address",
     "source_ip", "destination_ip"]
)


def _is_ip_name(name: str) -> bool:
    low = name.lower()
    if low in _IP_EXACT_NAMES:
        return True
    if any(low.endswith(s) for s in _IP_EXACT_SUFFIXES):
        return True
    parts = set(low.split("_"))
    # Require "ip" or "addr" in parts to avoid false positives
    return bool({"ip", "addr"}.intersection(parts))


class R024StringIPColumn(Rule):
    rule_id = "R-024"
    name = "string_ip_column_to_ipv4"
    tier = "1B"
    ch_version_introduced = "116.253"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if not _CREATE_TABLE_RE.search(sql):
            return None
        for m in _STRING_COL_RE.finditer(sql):
            column = m.group(1)
            if _is_ip_name(column):
                return Finding(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    tier=self.tier,
                    severity="low",
                    description=(
                        f"Колонка '{column}' объявлена как String, "
                        "но по имени предположительно хранит IP-адрес. "
                        "Тип IPv4 хранит адрес в 4 байтах (UInt32) вместо ~15 байт строки."
                    ),
                    suggestion=(
                        f"Замените String на IPv4 для '{column}' если это IPv4-адрес, "
                        "или IPv6 если это IPv6. Проверьте реальный формат значений."
                    ),
                    example_before=f"CREATE TABLE t ({column} String) ENGINE = MergeTree ORDER BY tuple()",
                    example_after=f"CREATE TABLE t ({column} IPv4) ENGINE = MergeTree ORDER BY tuple()",
                    explain_why=(
                        "IPv4 хранит адрес как UInt32 (4 байта). "
                        "Строка '192.168.1.1' занимает ~11 байт. "
                        "IPv4 поддерживает нативные функции IPv4CIDRToRange, toIPv4."
                    ),
                    confidence="advisory",
                    ch_version_introduced=self.ch_version_introduced,
                )
        return None

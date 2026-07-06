from __future__ import annotations

import time

import httpx
import pytest

from clickadvisor.core.models import QueryContext
from clickadvisor.core.pipeline import analyze_query
from clickadvisor.core.version import detect_version

CLICKHOUSE_URL = "http://localhost:8123"
CLICKHOUSE_USER = "default"
CLICKHOUSE_PASSWORD = "clickadvisor"


def _query_clickhouse(sql: str) -> str:
    response = httpx.post(
        CLICKHOUSE_URL,
        params={
            "query": sql,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        timeout=5.0,
    )
    response.raise_for_status()
    return response.text


@pytest.fixture(scope="module")
def live_ch_version() -> str:
    version = None
    for _ in range(30):
        version = detect_version(
            CLICKHOUSE_URL,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
        )
        if version is not None:
            break
        time.sleep(1)

    assert version is not None

    _query_clickhouse("DROP TABLE IF EXISTS events")
    _query_clickhouse("DROP TABLE IF EXISTS users")
    _query_clickhouse(
        """
        CREATE TABLE events
        (
            event_time DateTime,
            event_date Date,
            user_id String,
            country String,
            message String
        )
        ENGINE = MergeTree
        ORDER BY (event_time, user_id)
        """
    )
    _query_clickhouse(
        """
        CREATE TABLE users
        (
            id UInt64,
            name String
        )
        ENGINE = MergeTree
        ORDER BY id
        """
    )
    return version


@pytest.mark.parametrize(
    ("sql", "expected_rule_ids"),
    [
        (
            "SELECT COUNT(DISTINCT user_id) FROM events",
            {"R-001", "R-002"},
        ),
        (
            "SELECT * FROM events FINAL WHERE message LIKE '%timeout%'",
            {"D-003", "D-004", "D-005", "D-007", "R-102"},
        ),
        (
            "SELECT event_date FROM events WHERE toDate(event_time) = '2026-01-01'",
            {"R-005", "D-004"},
        ),
        (
            "SELECT e.user_id FROM events AS e JOIN users AS u ON toUInt64(e.user_id) = u.id",
            {"D-011", "R-008", "D-004"},
        ),
        (
            "SELECT country, count() FROM events GROUP BY country ORDER BY count() DESC",
            {"R-014"},
        ),
    ],
)
def test_live_clickhouse_queries_fire_expected_rules(
    live_ch_version: str,
    sql: str,
    expected_rule_ids: set[str],
) -> None:
    _query_clickhouse(f"EXPLAIN SYNTAX {sql}")

    report = analyze_query(QueryContext(sql=sql, ch_version=live_ch_version))

    actual_rule_ids = {finding.rule_id for finding in report.findings}
    assert expected_rule_ids <= actual_rule_ids

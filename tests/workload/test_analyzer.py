from __future__ import annotations

import csv
from pathlib import Path

from typer.testing import CliRunner

from clickadvisor.cli.main import app
from clickadvisor.workload.analyzer import (
    analyze_query_log_csv,
    clickhouse_query_log_sql,
    normalize_sql,
    parse_since,
)


def test_normalize_sql_replaces_literals() -> None:
    left = normalize_sql("SELECT * FROM events WHERE user_id = 42 AND status = 'paid'")
    right = normalize_sql("select * from events where user_id = 99 and status = 'trial'")

    assert left == right
    assert "42" not in left
    assert "paid" not in left


def test_analyze_query_log_groups_and_prioritizes(tmp_path: Path) -> None:
    path = tmp_path / "query_log.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "query",
                "query_duration_ms",
                "read_rows",
                "read_bytes",
                "memory_usage",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "query": "SELECT * FROM events FINAL WHERE message LIKE '%timeout%'",
                "query_duration_ms": "1000",
                "read_rows": "1000000",
                "read_bytes": "200000000",
                "memory_usage": "300000000",
            }
        )
        writer.writerow(
            {
                "query": "SELECT * FROM events FINAL WHERE message LIKE '%error%'",
                "query_duration_ms": "500",
                "read_rows": "800000",
                "read_bytes": "180000000",
                "memory_usage": "100000000",
            }
        )
        writer.writerow(
            {
                "query": "SELECT count() FROM events LIMIT 10",
                "query_duration_ms": "5",
                "read_rows": "10",
                "read_bytes": "80",
                "memory_usage": "1000",
            }
        )

    report = analyze_query_log_csv(path, top_n=5)

    assert report.rows_read == 3
    assert report.rows_used == 3
    assert report.group_count == 2
    top = report.groups[0]
    assert top.executions == 2
    assert top.total_duration_ms == 1500
    assert "D-007" in top.rule_ids
    assert top.priority_label in {"medium", "high"}


def test_parse_since_and_build_live_query() -> None:
    assert parse_since("24h") == (24, "HOUR")
    assert parse_since("7d") == (7, "DAY")

    query = clickhouse_query_log_sql("15m")

    assert "FROM system.query_log" in query
    assert "INTERVAL 15 MINUTE" in query
    assert "FORMAT CSVWithNames" in query


def test_workload_cli_outputs_markdown(tmp_path: Path) -> None:
    query_log = tmp_path / "query_log.csv"
    query_log.write_text(
        "\n".join(
            [
                "query,query_duration_ms,read_rows,read_bytes,memory_usage",
                "\"SELECT * FROM events FINAL\",100,1000,10000,100000",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        app,
        [
            "workload",
            "--query-log",
            str(query_log),
            "--output-format",
            "markdown",
        ],
    )

    assert result.exit_code == 0
    assert "ClickAdvisor Workload Report" in result.output
    assert "D-007" in result.output

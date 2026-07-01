from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from scripts.ml.prepare_local_clickhouse import DEFAULT_PASSWORD, DEFAULT_URL, DEFAULT_USER

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_MANIFEST_PATH = Path("data/ml/expert_dataset/manifest.json")
DEFAULT_MAX_EXECUTION_SECONDS = 5
DEFAULT_MAX_ROWS_TO_READ = 2_000_000
DEFAULT_MAX_MEMORY_USAGE = 1_500_000_000
DEFAULT_DATABASE = "chadvisor"
READONLY_PREFIXES = ("SELECT", "WITH")


class ClickHouse:
    def __init__(self, url: str, user: str, password: str, database: str) -> None:
        self.url = url
        self.auth = (user, password)
        self.database = database

    def execute(
        self,
        sql: str,
        *,
        query_id: str | None = None,
        default_format: str | None = None,
        timeout: int = 30,
    ) -> requests.Response:
        params = {"query": sql, "database": self.database}
        if query_id:
            params["query_id"] = query_id
        if default_format:
            params["default_format"] = default_format
        return requests.post(self.url, auth=self.auth, params=params, timeout=timeout)

    def query_json_each_row(self, sql: str, *, timeout: int = 60) -> list[dict[str, Any]]:
        response = self.execute(f"{sql} FORMAT JSONEachRow", timeout=timeout)
        response.raise_for_status()
        rows: list[dict[str, Any]] = []
        for line in response.text.splitlines():
            if line.strip():
                payload = json.loads(line)
                if isinstance(payload, dict):
                    rows.append(payload)
        return rows

    def query_text(self, sql: str, *, timeout: int = 30) -> str:
        response = self.execute(sql, timeout=timeout)
        response.raise_for_status()
        return response.text.strip()


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    client = ClickHouse(args.url, args.user, args.password, args.database)
    client.query_text("SELECT 1")

    run_id = args.run_id or datetime.now(UTC).strftime("replay_%Y%m%dT%H%M%SZ")
    replayed = replay_records(records, client, run_id, args)
    write_records(args.dataset, records)
    update_manifest(args.manifest, run_id, replayed, args)
    print_summary(replayed)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay expert dataset queries against local ClickHouse.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--database", default=DEFAULT_DATABASE)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--max-execution-seconds", type=int, default=DEFAULT_MAX_EXECUTION_SECONDS)
    parser.add_argument("--max-rows-to-read", type=int, default=DEFAULT_MAX_ROWS_TO_READ)
    parser.add_argument("--max-memory-usage", type=int, default=DEFAULT_MAX_MEMORY_USAGE)
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_records(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def replay_records(
    records: list[dict[str, Any]],
    client: ClickHouse,
    run_id: str,
    args: argparse.Namespace,
) -> Counter[str]:
    counters: Counter[str] = Counter()
    replayed = 0
    for index, record in enumerate(records, start=1):
        sql = str(record.get("sql") or "")
        if not is_readonly_query(sql):
            record["measured_metrics"] = skipped_metrics(run_id, "not_readonly_select")
            counters["skipped"] += 1
            continue
        if args.limit is not None and replayed >= args.limit:
            record["measured_metrics"] = skipped_metrics(run_id, "outside_replay_limit")
            counters["skipped"] += 1
            continue

        query_id = f"chadvisor_{run_id}_{index:05d}"
        replayed += 1
        response = execute_for_metrics(client, sql, query_id, args)
        time.sleep(0.002)
        if response.ok:
            counters["executed_ok"] += 1
        else:
            counters["executed_error"] += 1
        record["measured_metrics"] = {
            "status": "pending_query_log",
            "run_id": run_id,
            "query_id": query_id,
            "http_status": response.status_code,
            "error": None if response.ok else trim_error(response.text),
        }

    client.query_text("SYSTEM FLUSH LOGS", timeout=60)
    query_log_rows = fetch_query_log(client, run_id)
    for record in records:
        metrics = record.get("measured_metrics")
        if not isinstance(metrics, dict):
            continue
        query_id = metrics.get("query_id")
        if not isinstance(query_id, str):
            continue
        log_row = query_log_rows.get(query_id)
        if log_row is None:
            metrics["status"] = "query_log_missing"
            counters["query_log_missing"] += 1
            continue
        metrics.update(
            {
                "status": "ok" if log_row["type"] == "QueryFinish" else "error",
                "type": log_row["type"],
                "query_duration_ms": int(log_row["query_duration_ms"]),
                "read_rows": int(log_row["read_rows"]),
                "read_bytes": int(log_row["read_bytes"]),
                "memory_usage": int(log_row["memory_usage"]),
                "result_rows": int(log_row["result_rows"]),
                "result_bytes": int(log_row["result_bytes"]),
                "exception_code": int(log_row["exception_code"]),
                "exception": log_row["exception"],
            }
        )
    return counters


def is_readonly_query(sql: str) -> bool:
    prefix = sql.lstrip().split(None, 1)[0].upper() if sql.strip() else ""
    return prefix in READONLY_PREFIXES


def execute_for_metrics(
    client: ClickHouse,
    sql: str,
    query_id: str,
    args: argparse.Namespace,
) -> requests.Response:
    replay_sql = (
        f"{sql.rstrip().rstrip(';')} "
        "SETTINGS "
        "readonly = 1, "
        "log_queries = 1, "
        f"max_execution_time = {args.max_execution_seconds}, "
        "timeout_before_checking_execution_speed = 0, "
        f"max_rows_to_read = {args.max_rows_to_read}, "
        f"max_memory_usage = {args.max_memory_usage}"
    )
    try:
        return client.execute(
            replay_sql,
            query_id=query_id,
            default_format="Null",
            timeout=args.max_execution_seconds + 10,
        )
    except requests.RequestException as error:
        response = requests.Response()
        response.status_code = 599
        response._content = str(error).encode("utf-8")
        return response


def fetch_query_log(client: ClickHouse, run_id: str) -> dict[str, dict[str, Any]]:
    rows = client.query_json_each_row(
        """
        SELECT
            query_id,
            type,
            query_duration_ms,
            read_rows,
            read_bytes,
            memory_usage,
            result_rows,
            result_bytes,
            exception_code,
            exception
        FROM system.query_log
        WHERE startsWith(query_id, {prefix:String})
          AND type IN ('QueryFinish', 'ExceptionBeforeStart', 'ExceptionWhileProcessing')
        ORDER BY event_time_microseconds DESC
        """.replace("{prefix:String}", f"'{clickhouse_escape('chadvisor_' + run_id)}'")
    )
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        query_id = str(row.get("query_id") or "")
        if query_id and query_id not in result:
            result[query_id] = row
    return result


def skipped_metrics(run_id: str, reason: str) -> dict[str, Any]:
    return {
        "status": "skipped",
        "run_id": run_id,
        "skip_reason": reason,
        "query_id": None,
        "query_duration_ms": None,
        "read_rows": None,
        "read_bytes": None,
        "memory_usage": None,
    }


def trim_error(text: str) -> str:
    normalized = " ".join(text.strip().split())
    return normalized[:600]


def clickhouse_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def update_manifest(
    path: Path,
    run_id: str,
    counters: Counter[str],
    args: argparse.Namespace,
) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["measured_metrics_replay"] = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "url": args.url,
        "max_execution_seconds": args.max_execution_seconds,
        "max_rows_to_read": args.max_rows_to_read,
        "max_memory_usage": args.max_memory_usage,
        "counts": dict(sorted(counters.items())),
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def print_summary(counters: Counter[str]) -> None:
    parts = ", ".join(f"{key}={value}" for key, value in sorted(counters.items()))
    print(f"Replay complete: {parts}")


if __name__ == "__main__":
    main()

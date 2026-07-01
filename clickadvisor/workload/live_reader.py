"""
clickadvisor/workload/live_reader.py

Reads query_log directly from a running ClickHouse instance via HTTP API.
Produces the same row format as CSV import so analyzer.py stays unchanged.
"""

from __future__ import annotations

import csv
import io
import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import httpx

logger = logging.getLogger(__name__)

# Columns we need — matches query_log_sample.csv schema
_QUERY = """
SELECT
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage,
    toString(event_time)  AS event_time,
    user,
    query_kind,
    exception_code,
    result_rows
FROM system.query_log
WHERE
    type = 'QueryFinish'
    AND event_time >= '{since}'
    AND query_kind IN ('Select', 'AsyncInsertFlush')
    AND query NOT ILIKE '%system.query_log%'
    AND query NOT ILIKE '%system.processes%'
ORDER BY query_duration_ms DESC
LIMIT {limit}
FORMAT CSVWithNames
""".strip()


@dataclass
class LiveReaderConfig:
    url: str                  # e.g. http://localhost:8123
    user: str = "default"
    password: str = ""
    since_hours: int = 24
    limit: int = 10_000
    timeout: float = 30.0


class ClickHouseLiveReader:
    """Minimal HTTP client for system.query_log extraction."""

    def __init__(self, config: LiveReaderConfig) -> None:
        self.config = config
        self._base_url = config.url.rstrip("/")

    def fetch(self) -> list[dict[str, str]]:
        """
        Returns list of row-dicts with the same keys as query_log_sample.csv.
        Raises httpx.HTTPStatusError on ClickHouse errors.
        """
        since_dt = datetime.now(tz=UTC) - timedelta(hours=self.config.since_hours)
        since_str = since_dt.strftime("%Y-%m-%d %H:%M:%S")

        sql = _QUERY.format(since=since_str, limit=self.config.limit)

        logger.info(
            "Fetching query_log from %s (since %s, limit %d)",
            self._base_url,
            since_str,
            self.config.limit,
        )

        response = httpx.post(
            self._base_url,
            content=sql.encode(),
            params={"user": self.config.user, "password": self.config.password},
            headers={"Content-Type": "text/plain; charset=utf-8"},
            timeout=self.config.timeout,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # ClickHouse puts the error message in the body
            logger.error("ClickHouse returned error:\n%s", response.text[:2000])
            raise exc

        rows = list(csv.DictReader(io.StringIO(response.text)))
        logger.info("Fetched %d rows from query_log", len(rows))
        return rows

    def check_connection(self) -> bool:
        """Quick ping — returns True if ClickHouse responds."""
        try:
            r = httpx.get(f"{self._base_url}/ping", timeout=5.0)
            return r.status_code == 200 and r.text.strip() == "Ok."
        except Exception:
            return False

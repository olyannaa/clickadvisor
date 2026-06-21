from __future__ import annotations

import logging
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)


def parse_version(version_str: str) -> tuple[int, int]:
    parts = version_str.strip().split(".")
    if len(parts) < 2:
        raise ValueError(f"invalid ClickHouse version: {version_str!r}")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise ValueError(f"invalid ClickHouse version: {version_str!r}") from exc


def normalize_version(version_str: str) -> str:
    major, minor = parse_version(version_str)
    return f"{major}.{minor}"


def version_gte(v1: str, v2: str) -> bool:
    return parse_version(v1) >= parse_version(v2)


def _build_http_target(connect_url: str) -> str | None:
    parsed = urlparse(connect_url)
    if parsed.scheme not in {"http", "https", "clickhouse"}:
        logger.warning("Unsupported ClickHouse connection scheme: %s", parsed.scheme)
        return None

    if parsed.scheme == "clickhouse":
        host = parsed.hostname or "localhost"
        port = parsed.port or 8123
        return f"http://{host}:{port}/"

    return f"{parsed.scheme}://{parsed.netloc}/"


def detect_version(
    connect_url: str,
    user: str = "default",
    password: str = "",
) -> str | None:
    base_url = _build_http_target(connect_url)
    if base_url is None:
        return None

    try:
        response = httpx.get(
            base_url,
            params={
                "query": "SELECT version()",
                "user": user,
                "password": password,
            },
            timeout=5.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("Failed to detect ClickHouse version from %s: %s", connect_url, exc)
        return None

    raw_version = response.text.strip()
    try:
        return normalize_version(raw_version)
    except ValueError:
        logger.warning("Could not parse ClickHouse version from response: %r", raw_version)
        return None

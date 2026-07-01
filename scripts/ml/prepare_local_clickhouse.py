from __future__ import annotations

import argparse
import time
from dataclasses import dataclass

import requests

DEFAULT_URL = "http://localhost:18123"
DEFAULT_USER = "default"
DEFAULT_PASSWORD = "clickadvisor"
DEFAULT_ROWS = 1_000_000


@dataclass(frozen=True, slots=True)
class ClickHouse:
    url: str
    user: str
    password: str

    def query(self, sql: str, *, query_id: str | None = None) -> str:
        params = {"query": sql}
        if query_id is not None:
            params["query_id"] = query_id
        response = requests.post(
            self.url,
            auth=(self.user, self.password),
            params=params,
            timeout=120,
        )
        response.raise_for_status()
        return response.text.strip()


def main() -> None:
    args = parse_args()
    client = ClickHouse(args.url, args.user, args.password)
    wait_until_ready(client)
    create_schema(client, rows=args.rows)
    verify_query_log(client)
    version = client.query("SELECT version()")
    print(f"ClickHouse {version} is ready at {args.url}; benchmark rows={args.rows}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare local ClickHouse for ClickAdvisor replay.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    return parser.parse_args()


def wait_until_ready(client: ClickHouse) -> None:
    deadline = time.monotonic() + 120
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            client.query("SELECT 1")
            return
        except requests.RequestException as error:
            last_error = error
            time.sleep(1)
    raise RuntimeError(f"ClickHouse did not become ready: {last_error}")


def create_schema(client: ClickHouse, *, rows: int) -> None:
    client.query("CREATE DATABASE IF NOT EXISTS chadvisor")
    client.query("DROP TABLE IF EXISTS chadvisor.hits")
    client.query("DROP TABLE IF EXISTS chadvisor.events")
    client.query("DROP TABLE IF EXISTS chadvisor.users")

    client.query(
        """
        CREATE TABLE chadvisor.hits
        (
            EventDate Date,
            EventTime DateTime,
            UserID UInt64,
            WatchID UInt64,
            CounterID UInt32,
            AdvEngineID UInt8,
            RegionID UInt32,
            SearchEngineID UInt8,
            SearchPhrase String,
            MobilePhone UInt8,
            MobilePhoneModel String,
            URL String,
            Title String,
            Referer String,
            ClientIP UInt32,
            ResolutionWidth UInt16,
            IsRefresh UInt8,
            DontCountHits UInt8,
            IsLink UInt8,
            IsDownload UInt8,
            TraficSourceID Int8,
            RefererHash UInt64,
            URLHash UInt64,
            WindowClientWidth UInt16,
            WindowClientHeight UInt16
        )
        ENGINE = MergeTree
        PARTITION BY toYYYYMM(EventDate)
        ORDER BY (CounterID, EventDate, UserID)
        """
    )
    client.query(
        f"""
        INSERT INTO chadvisor.hits
        SELECT
            toDate('2013-07-01') + toIntervalDay(number % 31),
            toDateTime('2013-07-01 00:00:00') + toIntervalSecond(number % 2678400),
            cityHash64(number),
            number,
            toUInt32(number % 128),
            toUInt8(number % 5),
            toUInt32(number % 1000),
            toUInt8(number % 12),
            if(number % 7 = 0, concat('search_', toString(number % 10000)), ''),
            toUInt8(number % 2),
            concat('model_', toString(number % 50)),
            concat('https://example.com/page/', toString(number % 200000), if(number % 13 = 0, '?q=google', '')),
            concat('Title ', toString(number % 100000), if(number % 17 = 0, ' Google', '')),
            concat('https://ref.example/', toString(number % 4000)),
            toUInt32(number % 4294967295),
            toUInt16(800 + number % 1600),
            toUInt8(number % 11 = 0),
            toUInt8(number % 19 = 0),
            toUInt8(number % 23 = 0),
            toUInt8(number % 29 = 0),
            toInt8((number % 8) - 1),
            cityHash64(number, 17),
            cityHash64(number, 23),
            toUInt16(320 + number % 1600),
            toUInt16(240 + number % 1200)
        FROM numbers({rows})
        """
    )

    client.query(
        """
        CREATE TABLE chadvisor.events
        (
            event_time DateTime,
            user_id UInt64,
            country LowCardinality(String),
            status LowCardinality(String),
            revenue Decimal(12, 2),
            message String
        )
        ENGINE = ReplacingMergeTree
        PARTITION BY toYYYYMM(event_time)
        ORDER BY (country, event_time, user_id)
        """
    )
    client.query(
        f"""
        INSERT INTO chadvisor.events
        SELECT
            toDateTime('2024-01-01 00:00:00') + toIntervalSecond(number % 7776000),
            cityHash64(number % 250000),
            ['RU','KZ','BY','US','DE','IN'][1 + number % 6],
            ['paid','trial','failed','free'][1 + number % 4],
            toDecimal64((number % 100000) / 100, 2),
            if(number % 97 = 0, 'timeout while processing request', concat('message_', toString(number % 1000)))
        FROM numbers({rows})
        """
    )

    client.query(
        """
        CREATE TABLE chadvisor.users
        (
            id UInt64,
            country LowCardinality(String),
            created_at DateTime
        )
        ENGINE = MergeTree
        ORDER BY id
        """
    )
    client.query(
        f"""
        INSERT INTO chadvisor.users
        SELECT
            cityHash64(number),
            ['RU','KZ','BY','US','DE','IN'][1 + number % 6],
            toDateTime('2023-01-01 00:00:00') + toIntervalSecond(number % 31536000)
        FROM numbers({max(rows // 4, 1)})
        """
    )


def verify_query_log(client: ClickHouse) -> None:
    query_id = f"chadvisor_prepare_{int(time.time())}"
    client.query("SELECT count() FROM chadvisor.hits SETTINGS log_queries = 1", query_id=query_id)
    client.query("SYSTEM FLUSH LOGS")
    count = int(
        client.query(
            "SELECT count() FROM system.query_log "
            f"WHERE query_id = '{query_id}' AND type = 'QueryFinish'"
        )
    )
    if count < 1:
        raise RuntimeError("system.query_log did not record the verification query")


if __name__ == "__main__":
    main()

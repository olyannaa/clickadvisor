from __future__ import annotations

import argparse
import random
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_OUTPUT_DIR = Path("benchmark/cases/synthetic_expanded")
DEFAULT_SPLIT_PATH = Path("benchmark/splits/synthetic_expanded_v1.yaml")
DEFAULT_SEED = 42
TRAIN_RATIO = 0.8


@dataclass(frozen=True, slots=True)
class RuleTemplate:
    label: str
    rules: tuple[str, ...]
    severity: str
    issue_type: str
    description: str
    sql_variants: tuple[str, ...]
    severities: tuple[str, ...] | None = None


TEMPLATES: tuple[RuleTemplate, ...] = (
    RuleTemplate(
        label="r001",
        rules=("R-001", "R-002"),
        severity="high",
        issue_type="count_distinct_specialization",
        description="COUNT(DISTINCT ...) можно заменить точным uniqExact и advisory-вариантом uniq.",
        sql_variants=(
            "SELECT COUNT(DISTINCT user_id) FROM events",
            "SELECT COUNT(DISTINCT session_id) FROM logs",
            "SELECT COUNT(DISTINCT order_id) FROM orders WHERE status = 'paid'",
            "SELECT COUNT(DISTINCT visitor_id) FROM sessions WHERE event_date >= toDate('2024-01-01')",
            "SELECT COUNT(DISTINCT account_id) FROM payments",
            "SELECT COUNT(DISTINCT device_id) FROM events WHERE country = 'RU'",
            "SELECT COUNT(DISTINCT campaign_id) FROM impressions",
            "SELECT COUNT(DISTINCT product_id) FROM views WHERE event_type = 'view'",
        ),
    ),
    RuleTemplate(
        label="r003",
        rules=("R-003",),
        severity="medium",
        issue_type="exact_quantile_candidate",
        description="quantileExact требует точный state; approximate quantile может быть быстрее при допустимой погрешности.",
        sql_variants=(
            "SELECT quantileExact(0.95)(response_time) FROM requests",
            "SELECT quantileExact(0.99)(latency_ms) FROM logs",
            "SELECT quantileExact(0.50)(duration_ms) FROM sessions",
            "SELECT quantileExact(0.90)(load_time_ms) FROM page_views WHERE browser = 'Chrome'",
            "SELECT quantileExact(0.75)(queue_time_ms) FROM jobs",
            "SELECT quantileExact(0.95)(bytes_sent) FROM network_logs",
            "SELECT quantileExact(0.99)(cpu_time_ms) FROM query_log",
            "SELECT quantileExact(0.80)(checkout_ms) FROM orders",
        ),
    ),
    RuleTemplate(
        label="r004",
        rules=("R-004",),
        severity="high",
        issue_type="count_star_distinct_subquery",
        description="COUNT(*) поверх SELECT DISTINCT можно свернуть в специализированный uniqExact.",
        sql_variants=(
            "SELECT COUNT(*) FROM (SELECT DISTINCT user_id FROM events)",
            "SELECT COUNT(*) FROM (SELECT DISTINCT session_id FROM logs)",
            "SELECT COUNT(*) FROM (SELECT DISTINCT order_id FROM orders WHERE status = 'paid')",
            "SELECT COUNT(*) FROM (SELECT DISTINCT visitor_id FROM sessions)",
            "SELECT COUNT(*) FROM (SELECT DISTINCT account_id FROM payments)",
            "SELECT COUNT(*) FROM (SELECT DISTINCT product_id FROM views)",
        ),
    ),
    RuleTemplate(
        label="r005",
        rules=("R-005", "R-020"),
        severity="high",
        issue_type="function_on_datetime_filter",
        description="toDate(column) в фильтре мешает sparse primary key pruning.",
        sql_variants=(
            "SELECT count() FROM events WHERE toDate(created_at) = '2024-01-15'",
            "SELECT count() FROM logs WHERE toDate(ts) = '2024-02-10'",
            "SELECT count() FROM orders WHERE toDate(paid_at) = '2024-03-05'",
            "SELECT count() FROM sessions WHERE toDate(started_at) = '2024-04-20'",
            "SELECT count() FROM requests WHERE toDate(request_time) = '2024-05-01'",
            "SELECT count() FROM payments WHERE toDate(processed_at) = '2024-06-12'",
        ),
    ),
    RuleTemplate(
        label="r006",
        rules=("R-006",),
        severity="high",
        issue_type="date_part_filter_to_range",
        description="Функция date-part над колонкой в WHERE лучше выражается range-предикатом.",
        sql_variants=(
            "SELECT count() FROM events WHERE toYYYYMM(event_date) = 202401",
            "SELECT count() FROM logs WHERE toYYYYMMDD(ts) = 20240210",
            "SELECT count() FROM orders WHERE toMonth(order_date) = 3",
            "SELECT count() FROM sessions WHERE toStartOfMonth(started_at) = '2024-04-01'",
            "SELECT count() FROM requests WHERE toYYYYMM(created_at) = 202405",
            "SELECT count() FROM payments WHERE toYYYYMM(processed_at) = 202406",
        ),
    ),
    RuleTemplate(
        label="r007",
        rules=("R-007",),
        severity="high",
        issue_type="interval_start_filter_to_range",
        description="toStartOf* в фильтре по времени лучше заменить диапазоном по исходной колонке.",
        sql_variants=(
            "SELECT count() FROM logs WHERE toStartOfHour(ts) = '2024-01-15 14:00:00'",
            "SELECT count() FROM events WHERE toStartOfDay(created_at) = '2024-02-10 00:00:00'",
            "SELECT count() FROM requests WHERE toStartOfFifteenMinutes(request_time) = '2024-03-05 12:15:00'",
            "SELECT count() FROM sessions WHERE toStartOfHour(started_at) = '2024-04-20 09:00:00'",
            "SELECT count() FROM query_log WHERE toStartOfDay(event_time) = '2024-05-01 00:00:00'",
            "SELECT count() FROM payments WHERE toStartOfHour(processed_at) = '2024-06-12 18:00:00'",
        ),
    ),
    RuleTemplate(
        label="r008",
        rules=("R-008", "R-020"),
        severity="medium",
        issue_type="redundant_cast_on_filter",
        description="CAST над колонкой в фильтре может быть избыточным и блокировать использование индекса.",
        sql_variants=(
            "SELECT count() FROM users WHERE CAST(user_id AS UInt64) = 12345",
            "SELECT count() FROM events WHERE toUInt64(account_id) = 42",
            "SELECT count() FROM orders WHERE CAST(order_id AS UInt32) = 777",
            "SELECT count() FROM sessions WHERE toInt32(region_id) = 10",
            "SELECT count() FROM logs WHERE CAST(status_code AS UInt16) = 500",
            "SELECT count() FROM payments WHERE toUInt32(merchant_id) = 123",
        ),
    ),
    RuleTemplate(
        label="r009",
        rules=("R-009",),
        severity="high",
        issue_type="singleton_in_predicate",
        description="IN с одним значением эквивалентен equality-предикату.",
        sql_variants=(
            "SELECT count() FROM events WHERE country IN ('RU')",
            "SELECT count() FROM logs WHERE status IN ('error')",
            "SELECT count() FROM orders WHERE order_id IN (42)",
            "SELECT count() FROM sessions WHERE browser IN ('Safari')",
            "SELECT count() FROM users WHERE user_id IN (1001)",
            "SELECT count() FROM payments WHERE currency IN ('EUR')",
        ),
    ),
    RuleTemplate(
        label="r010",
        rules=("R-010",),
        severity="high",
        issue_type="disjunction_chain_to_in",
        description="OR-цепочку равенств по одной колонке можно канонизировать в IN.",
        sql_variants=(
            "SELECT count() FROM events WHERE country = 'RU' OR country = 'BY' OR country = 'KZ'",
            "SELECT count() FROM logs WHERE level = 'warn' OR level = 'error' OR level = 'fatal'",
            "SELECT count() FROM orders WHERE status = 'paid' OR status = 'shipped' OR status = 'closed'",
            "SELECT count() FROM sessions WHERE browser = 'Chrome' OR browser = 'Safari' OR browser = 'Firefox'",
            "SELECT count() FROM users WHERE plan = 'pro' OR plan = 'team' OR plan = 'enterprise'",
            "SELECT count() FROM payments WHERE currency = 'USD' OR currency = 'EUR' OR currency = 'GBP'",
        ),
    ),
    RuleTemplate(
        label="r011",
        rules=("R-011",),
        severity="high",
        issue_type="having_without_aggregate",
        description="Условие без агрегатов в HAVING следует применять раньше через WHERE.",
        sql_variants=(
            "SELECT user_id, COUNT(*) FROM events GROUP BY user_id HAVING country = 'RU' AND COUNT(*) > 100",
            "SELECT account_id, COUNT(*) FROM logs GROUP BY account_id HAVING level = 'error' AND COUNT(*) > 10",
            "SELECT order_id, SUM(amount) FROM orders GROUP BY order_id HAVING status = 'paid' AND SUM(amount) > 1000",
            "SELECT session_id, COUNT(*) FROM sessions GROUP BY session_id HAVING browser = 'Chrome' AND COUNT(*) > 5",
            "SELECT merchant_id, SUM(amount) FROM payments GROUP BY merchant_id HAVING currency = 'USD' AND SUM(amount) > 100",
            "SELECT project_id, COUNT(*) FROM requests GROUP BY project_id HAVING region = 'eu' AND COUNT(*) > 50",
        ),
    ),
    RuleTemplate(
        label="r012",
        rules=("R-012",),
        severity="high",
        issue_type="constant_predicate",
        description="Константный TRUE/1=1 предикат не влияет на результат и засоряет фильтр.",
        sql_variants=(
            "SELECT count() FROM events WHERE TRUE AND user_id = 5",
            "SELECT count() FROM logs WHERE 1 = 1 AND level = 'error'",
            "SELECT count() FROM orders WHERE status = 'paid' AND TRUE",
            "SELECT count() FROM sessions WHERE TRUE AND browser = 'Chrome'",
            "SELECT count() FROM users WHERE 1=1 AND plan = 'pro'",
            "SELECT count() FROM payments WHERE TRUE AND currency = 'USD'",
        ),
    ),
    RuleTemplate(
        label="r013",
        rules=("R-013",),
        severity="high",
        issue_type="length_empty_predicate",
        description="length(s)=0/>0 лучше выразить через empty/notEmpty.",
        sql_variants=(
            "SELECT count() FROM comments WHERE length(body) > 0",
            "SELECT count() FROM users WHERE length(email) != 0",
            "SELECT count() FROM logs WHERE length(message) = 0",
            "SELECT count() FROM orders WHERE length(comment) > 0",
            "SELECT count() FROM sessions WHERE length(referrer) != 0",
            "SELECT count() FROM events WHERE length(event_type) > 0",
        ),
    ),
    RuleTemplate(
        label="r014",
        rules=("R-014",),
        severity="medium",
        issue_type="groupby_string_hash_candidate",
        description="GROUP BY по потенциально длинной строке может выиграть от хэширования при подтверждении типа и длины.",
        sql_variants=(
            "SELECT url, COUNT(*) FROM logs GROUP BY url",
            "SELECT path, COUNT(*) FROM page_views GROUP BY path",
            "SELECT name, COUNT(*) FROM requests GROUP BY name",
            "SELECT title, COUNT(*) FROM sessions GROUP BY title",
            "SELECT city, COUNT(*) FROM users GROUP BY city",
            "SELECT message, COUNT(*) FROM logs GROUP BY message",
        ),
    ),
    RuleTemplate(
        label="r015",
        rules=("R-015",),
        severity="high",
        issue_type="distinct_after_groupby",
        description="DISTINCT после GROUP BY по тем же ключам не меняет результат.",
        sql_variants=(
            "SELECT DISTINCT a, b FROM (SELECT a, b, COUNT(*) AS cnt FROM events GROUP BY a, b) LIMIT 100",
            "SELECT DISTINCT user_id, country FROM (SELECT user_id, country, COUNT(*) AS cnt FROM events GROUP BY user_id, country) LIMIT 100",
            "SELECT DISTINCT account_id, status FROM (SELECT account_id, status, SUM(amount) AS total FROM orders GROUP BY account_id, status) LIMIT 100",
            "SELECT DISTINCT session_id, browser FROM (SELECT session_id, browser, COUNT(*) AS cnt FROM sessions GROUP BY session_id, browser) LIMIT 100",
            "SELECT DISTINCT product_id, category FROM (SELECT product_id, category, COUNT(*) AS cnt FROM views GROUP BY product_id, category) LIMIT 100",
            "SELECT DISTINCT merchant_id, currency FROM (SELECT merchant_id, currency, SUM(amount) AS total FROM payments GROUP BY merchant_id, currency) LIMIT 100",
        ),
    ),
    RuleTemplate(
        label="r016",
        rules=("R-016",),
        severity="medium",
        issue_type="orderby_without_limit_in_subquery",
        description="ORDER BY внутри подзапроса без LIMIT обычно не влияет на внешний агрегат и создаёт лишнюю сортировку.",
        sql_variants=(
            "SELECT COUNT(*) FROM (SELECT * FROM events ORDER BY created_at)",
            "SELECT COUNT(*) FROM (SELECT * FROM logs ORDER BY ts)",
            "SELECT COUNT(*) FROM (SELECT * FROM orders ORDER BY order_date)",
            "SELECT COUNT(*) FROM (SELECT * FROM sessions ORDER BY started_at)",
            "SELECT COUNT(*) FROM (SELECT * FROM requests ORDER BY request_time)",
            "SELECT COUNT(*) FROM (SELECT * FROM payments ORDER BY processed_at)",
        ),
    ),
    RuleTemplate(
        label="r017",
        rules=("R-017", "D-003", "D-004"),
        severity="medium",
        issue_type="subquery_filter_pushdown",
        description="Внешний фильтр можно объединить с фильтром простого подзапроса.",
        sql_variants=(
            "SELECT * FROM (SELECT * FROM events WHERE status = 'active') WHERE user_id = 42",
            "SELECT * FROM (SELECT * FROM logs WHERE level = 'error') WHERE account_id = 7",
            "SELECT * FROM (SELECT * FROM orders WHERE status = 'paid') WHERE customer_id = 11",
            "SELECT * FROM (SELECT * FROM sessions WHERE browser = 'Chrome') WHERE user_id = 101",
            "SELECT * FROM (SELECT * FROM requests WHERE region = 'eu') WHERE project_id = 5",
            "SELECT * FROM (SELECT * FROM payments WHERE currency = 'USD') WHERE merchant_id = 9",
        ),
    ),
    RuleTemplate(
        label="r018",
        rules=("R-018",),
        severity="medium",
        issue_type="union_without_all",
        description="UNION выполняет дедупликацию; если источники не пересекаются, UNION ALL дешевле.",
        sql_variants=(
            "SELECT user_id FROM events_2023 UNION SELECT user_id FROM events_2024",
            "SELECT order_id FROM orders_2023 UNION SELECT order_id FROM orders_2024",
            "SELECT session_id FROM sessions_mobile UNION SELECT session_id FROM sessions_web",
            "SELECT product_id FROM views_jan UNION SELECT product_id FROM views_feb",
            "SELECT account_id FROM payments_eu UNION SELECT account_id FROM payments_us",
            "SELECT request_id FROM logs_a UNION SELECT request_id FROM logs_b",
        ),
    ),
    RuleTemplate(
        label="r019",
        rules=("R-019",),
        severity="low",
        issue_type="oversized_uint_type_narrowing",
        description="Широкий Int64/UInt64 для статусных или типовых колонок может быть избыточен.",
        sql_variants=(
            "CREATE TABLE events (event_type UInt64, user_id UInt64) ENGINE = MergeTree() ORDER BY user_id",
            "CREATE TABLE orders (order_status Int64, order_id UInt64) ENGINE = MergeTree() ORDER BY order_id",
            "CREATE TABLE logs (log_level UInt64, ts DateTime) ENGINE = MergeTree() ORDER BY ts",
            "CREATE TABLE sessions (session_type UInt64, session_id UInt64) ENGINE = MergeTree() ORDER BY session_id",
            "CREATE TABLE users (account_status Int64, user_id UInt64) ENGINE = MergeTree() ORDER BY user_id",
            "CREATE TABLE payments (payment_type UInt64, payment_id UInt64) ENGINE = MergeTree() ORDER BY payment_id",
        ),
    ),
    RuleTemplate(
        label="r020",
        rules=("R-020", "R-008", "D-004"),
        severity="medium",
        issue_type="unsafe_cast_without_default",
        description="CAST/toUInt* над сырой колонкой может падать на некорректных значениях; OrDefault-вариант безопаснее.",
        sql_variants=(
            "SELECT CAST(raw_value AS UInt32) FROM events",
            "SELECT toUInt32(raw_status) FROM logs",
            "SELECT CAST(raw_amount AS UInt64) FROM payments",
            "SELECT toInt32(raw_region_id) FROM sessions",
            "SELECT CAST(raw_user_id AS UInt64) FROM users",
            "SELECT toUInt16(raw_code) FROM requests",
        ),
    ),
    RuleTemplate(
        label="r057",
        rules=("R-057",),
        severity="low",
        issue_type="extract_month_to_tomonth",
        description="EXTRACT(MONTH FROM ts) эквивалентна toMonth(ts) в ClickHouse.",
        sql_variants=(
            "SELECT EXTRACT(MONTH FROM ts) AS mon FROM events LIMIT 100",
            "SELECT EXTRACT(MONTH FROM created_at) AS mon FROM orders LIMIT 100",
            "SELECT EXTRACT(MONTH FROM started_at) AS mon FROM sessions LIMIT 100",
            "SELECT EXTRACT(MONTH FROM request_time) AS mon FROM requests LIMIT 100",
            "SELECT EXTRACT(MONTH FROM processed_at) AS mon FROM payments LIMIT 100",
            "SELECT EXTRACT(MONTH FROM event_time) AS mon FROM query_log LIMIT 100",
        ),
    ),
    RuleTemplate(
        label="r058",
        rules=("R-058",),
        severity="low",
        issue_type="extract_day_to_todayofmonth",
        description="EXTRACT(DAY FROM ts) эквивалентна toDayOfMonth(ts) в ClickHouse.",
        sql_variants=(
            "SELECT EXTRACT(DAY FROM ts) AS day_num FROM events LIMIT 100",
            "SELECT EXTRACT(DAY FROM created_at) AS day_num FROM orders LIMIT 100",
            "SELECT EXTRACT(DAY FROM started_at) AS day_num FROM sessions LIMIT 100",
            "SELECT EXTRACT(DAY FROM request_time) AS day_num FROM requests LIMIT 100",
            "SELECT EXTRACT(DAY FROM processed_at) AS day_num FROM payments LIMIT 100",
            "SELECT EXTRACT(DAY FROM event_time) AS day_num FROM query_log LIMIT 100",
        ),
    ),
    RuleTemplate(
        label="r059",
        rules=("R-059",),
        severity="low",
        issue_type="extract_hour_to_tohour",
        description="EXTRACT(HOUR FROM ts) эквивалентна toHour(ts) в ClickHouse.",
        sql_variants=(
            "SELECT EXTRACT(HOUR FROM ts) AS hr FROM events LIMIT 100",
            "SELECT EXTRACT(HOUR FROM created_at) AS hr FROM orders LIMIT 100",
            "SELECT EXTRACT(HOUR FROM started_at) AS hr FROM sessions LIMIT 100",
            "SELECT EXTRACT(HOUR FROM request_time) AS hr FROM requests LIMIT 100",
            "SELECT EXTRACT(HOUR FROM processed_at) AS hr FROM payments LIMIT 100",
            "SELECT EXTRACT(HOUR FROM event_time) AS hr FROM query_log LIMIT 100",
        ),
    ),
    RuleTemplate(
        label="d003",
        rules=("D-003",),
        severity="medium",
        issue_type="select_star_on_wide_table",
        description="SELECT * читает все колонки; для column-store лучше перечислить нужные поля.",
        sql_variants=(
            "SELECT * FROM events LIMIT 10",
            "SELECT * FROM logs WHERE level = 'error' LIMIT 20",
            "SELECT * FROM orders WHERE status = 'paid' LIMIT 50",
            "SELECT * FROM sessions WHERE browser = 'Chrome' LIMIT 10",
            "SELECT * FROM users WHERE plan = 'pro' LIMIT 100",
            "SELECT * FROM payments WHERE currency = 'USD' LIMIT 25",
        ),
    ),
    RuleTemplate(
        label="d004",
        rules=("D-004",),
        severity="medium",
        issue_type="missing_limit_on_unbounded_result",
        description="SELECT без LIMIT и без top-level агрегата может вернуть неограниченное число строк.",
        sql_variants=(
            "SELECT user_id, event_type, created_at FROM events WHERE status = 'active'",
            "SELECT ts, level, message FROM logs WHERE level = 'error'",
            "SELECT order_id, customer_id, status FROM orders WHERE status = 'paid'",
            "SELECT session_id, user_id, browser FROM sessions WHERE browser = 'Chrome'",
            "SELECT user_id, plan, country FROM users WHERE plan = 'pro'",
            "SELECT payment_id, merchant_id, amount FROM payments WHERE currency = 'USD'",
        ),
    ),
    RuleTemplate(
        label="d007",
        rules=("D-007",),
        severity="medium",
        issue_type="final_modifier_usage",
        description="FINAL мержит parts на чтении и может быть дорогой операцией.",
        sql_variants=(
            "SELECT count() FROM events FINAL WHERE user_id = 1",
            "SELECT count() FROM orders FINAL WHERE status = 'paid'",
            "SELECT count() FROM sessions FINAL WHERE session_id = 42",
            "SELECT count() FROM users FINAL WHERE user_id = 100",
            "SELECT count() FROM payments FINAL WHERE merchant_id = 5",
            "SELECT count() FROM logs FINAL WHERE level = 'error'",
        ),
    ),
    RuleTemplate(
        label="d014",
        rules=("D-014",),
        severity="high",
        issue_type="async_insert_without_wait_flag",
        description="async_insert без wait_for_async_insert может скрывать ошибки вставки от клиента.",
        sql_variants=(
            "INSERT INTO events SETTINGS async_insert=1 VALUES (1, 'click')",
            "INSERT INTO logs SETTINGS async_insert=1 VALUES (now(), 'error')",
            "INSERT INTO orders SETTINGS async_insert=1 VALUES (42, 'paid')",
            "INSERT INTO sessions SETTINGS async_insert=1 VALUES (100, 'Chrome')",
            "INSERT INTO users SETTINGS async_insert=1 VALUES (7, 'pro')",
            "INSERT INTO payments SETTINGS async_insert=1 VALUES (9, 10.5)",
        ),
    ),
)

RULE_METADATA: dict[str, tuple[str, str, str]] = {
    "R-001": ("exact_count_distinct_specialization", "high", "COUNT(DISTINCT ...) имеет точный specialized rewrite через uniqExact."),
    "R-002": ("approx_count_distinct_advisory", "medium", "Для approximate cardinality можно предложить uniq(...) как opt-in advisory."),
    "R-003": ("exact_quantile_candidate", "medium", "quantileExact может быть заменён approximate quantile только при явном согласии."),
    "R-004": ("count_star_distinct_subquery", "high", "COUNT(*) поверх SELECT DISTINCT сворачивается в uniqExact по ключу."),
    "R-005": ("function_on_datetime_filter", "high", "toDate(column) в фильтре мешает sparse primary key pruning."),
    "R-006": ("date_part_filter_to_range", "high", "Функция date-part над колонкой в WHERE лучше выражается range-предикатом."),
    "R-007": ("interval_start_filter_to_range", "high", "toStartOf* в фильтре по времени лучше заменить диапазоном по исходной колонке."),
    "R-008": ("redundant_cast_on_filter", "medium", "CAST/toType вокруг колонки в фильтре может блокировать использование индекса."),
    "R-009": ("singleton_in_predicate", "high", "IN с одним значением эквивалентен equality-предикату."),
    "R-010": ("disjunction_chain_to_in", "high", "OR-цепочку равенств по одной колонке можно канонизировать в IN."),
    "R-011": ("having_without_aggregate", "high", "Условие без агрегатов в HAVING следует применять раньше через WHERE."),
    "R-012": ("constant_predicate", "high", "Константный TRUE/1=1 предикат не влияет на результат."),
    "R-013": ("length_empty_predicate", "high", "length(s)=0/>0 лучше выразить через empty/notEmpty."),
    "R-014": ("groupby_string_hash_candidate", "medium", "GROUP BY по потенциально длинной строке является advisory-кандидатом на hash strategy."),
    "R-015": ("distinct_after_groupby", "high", "DISTINCT после GROUP BY по тем же ключам не меняет результат."),
    "R-016": ("orderby_without_limit_in_subquery", "medium", "ORDER BY внутри подзапроса без LIMIT обычно создаёт лишнюю сортировку."),
    "R-017": ("subquery_filter_pushdown", "medium", "Внешний фильтр можно объединить с фильтром простого подзапроса."),
    "R-018": ("union_without_all", "medium", "UNION выполняет дедупликацию; UNION ALL дешевле при непересекающихся источниках."),
    "R-019": ("oversized_uint_type_narrowing", "low", "Широкий Int64/UInt64 для статусных или типовых колонок может быть избыточен."),
    "R-020": ("unsafe_cast_without_default", "medium", "CAST/toType над сырой колонкой может падать на некорректных значениях."),
    "R-057": ("extract_month_to_tomonth", "low", "EXTRACT(MONTH FROM ts) эквивалентна toMonth(ts) в ClickHouse."),
    "R-058": ("extract_day_to_todayofmonth", "low", "EXTRACT(DAY FROM ts) эквивалентна toDayOfMonth(ts) в ClickHouse."),
    "R-059": ("extract_hour_to_tohour", "low", "EXTRACT(HOUR FROM ts) эквивалентна toHour(ts) в ClickHouse."),
    "D-003": ("select_star_on_wide_table", "medium", "SELECT * читает все колонки; для column-store лучше перечислить нужные поля."),
    "D-004": ("missing_limit_on_unbounded_result", "medium", "SELECT без LIMIT и без top-level агрегата может вернуть неограниченное число строк."),
    "D-007": ("final_modifier_usage", "medium", "FINAL мержит parts на чтении и может быть дорогой операцией."),
    "D-014": ("async_insert_without_wait_flag", "high", "async_insert без wait_for_async_insert может скрывать ошибки вставки от клиента."),
}


NEGATIVE_SQL: tuple[str, ...] = (
    "SELECT count() FROM events WHERE created_at >= '2024-01-15 00:00:00' AND created_at < '2024-01-16 00:00:00'",
    "SELECT user_id, count() FROM events WHERE country IN ('RU', 'BY') GROUP BY user_id",
    "SELECT avg(response_time) FROM requests WHERE response_time > 0",
    "SELECT user_id, event_type FROM events WHERE status = 'active' LIMIT 100",
    "SELECT count() FROM (SELECT * FROM events ORDER BY created_at LIMIT 10)",
    "SELECT user_id FROM events_2023 UNION ALL SELECT user_id FROM events_2024",
    "SELECT COUNT(session_id) FROM logs",
    "SELECT url FROM logs LIMIT 20",
    "SELECT COUNT(*) FROM (SELECT user_id FROM events)",
    "SELECT user_id, COUNT(*) FROM events GROUP BY user_id HAVING COUNT(*) > 10",
    "SELECT count() FROM comments WHERE score > 0",
    "SELECT accurateCastOrDefault(raw_value, 'UInt32', 0) FROM events LIMIT 10",
    "CREATE TABLE payments (amount UInt64) ENGINE = MergeTree() ORDER BY amount",
    "INSERT INTO events SETTINGS async_insert=1, wait_for_async_insert=1 VALUES (1, 'click')",
    "SELECT count() FROM users WHERE user_id = 1001",
    "SELECT count() FROM logs WHERE level = 'error'",
    "SELECT region_id, count() FROM events GROUP BY region_id",
    "SELECT user_id, event_type FROM events LIMIT 100",
    "SELECT count() FROM events WHERE user_id > 0",
    "SELECT empty(body) FROM comments LIMIT 10",
)


def build_positive_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for template in TEMPLATES:
        for index, sql in enumerate(template.sql_variants, start=1):
            case_id = f"synthetic_expanded_{template.label}_{index:03d}"
            known_issues = []
            for issue_index, rule_id in enumerate(template.rules, start=1):
                issue_type, severity, description = RULE_METADATA.get(
                    rule_id,
                    (template.issue_type, template.severity, template.description),
                )
                known_issues.append(
                    {
                        "issue_id": f"I-{issue_index}",
                        "type": issue_type,
                        "detected_by_rule": rule_id,
                        "severity": severity,
                        "description": description,
                    }
                )
            cases.append(
                {
                    "status": "validated",
                    "case_id": case_id,
                    "source": "synthetic",
                    "sql": sql,
                    "schema_files": [],
                    "known_issues": known_issues,
                    "expected_rules_to_fire": list(template.rules),
                    "expected_findings_count": len(template.rules),
                    "expected_improvement": None,
                    "synthetic_explain_path": None,
                    "notes": f"Generated positive synthetic case for {', '.join(template.rules)}.",
                }
            )
    return cases


def build_negative_cases() -> list[dict[str, Any]]:
    return [
        {
            "status": "validated",
            "case_id": f"synthetic_expanded_negative_{index:03d}",
            "source": "synthetic",
            "sql": sql,
            "schema_files": [],
            "known_issues": [],
            "expected_rules_to_fire": [],
            "expected_findings_count": 0,
            "expected_improvement": None,
            "synthetic_explain_path": None,
            "notes": "Generated negative synthetic case; no implemented rule should fire.",
        }
        for index, sql in enumerate(NEGATIVE_SQL, start=1)
    ]


def build_cases() -> list[dict[str, Any]]:
    return build_positive_cases() + build_negative_cases()


def build_split(case_ids: list[str], seed: int = DEFAULT_SEED) -> dict[str, Any]:
    rng = random.Random(seed)
    shuffled = list(case_ids)
    rng.shuffle(shuffled)
    train_size = int(len(shuffled) * TRAIN_RATIO)
    train_case_ids = sorted(shuffled[:train_size])
    test_case_ids = sorted(shuffled[train_size:])
    return {
        "dataset": "synthetic_expanded_v1",
        "seed": seed,
        "strategy": "deterministic random 80/20 split over generated case IDs",
        "train_case_ids": train_case_ids,
        "test_case_ids": test_case_ids,
        "counts": {
            "total": len(case_ids),
            "train": len(train_case_ids),
            "test": len(test_case_ids),
        },
    }


def write_cases(cases: list[dict[str, Any]], output_dir: Path, overwrite: bool) -> None:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(f"{output_dir} already exists; pass --overwrite")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for case in cases:
        path = output_dir / f"{case['case_id']}.yaml"
        path.write_text(yaml.safe_dump(case, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_split(cases: list[dict[str, Any]], split_path: Path, seed: int) -> None:
    split_path.parent.mkdir(parents=True, exist_ok=True)
    split = build_split([case["case_id"] for case in cases], seed=seed)
    split_path.write_text(yaml.safe_dump(split, allow_unicode=True, sort_keys=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic synthetic benchmark cases.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--split-path", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = build_cases()
    write_cases(cases, args.output_dir, overwrite=args.overwrite)
    write_split(cases, args.split_path, seed=args.seed)
    print(f"Generated {len(cases)} synthetic cases in {args.output_dir}")
    print(f"Wrote split metadata to {args.split_path}")


if __name__ == "__main__":
    main()

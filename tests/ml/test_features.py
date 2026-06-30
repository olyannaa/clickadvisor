"""Tests for FeatureExtractor using real SQL from synthetic_expanded benchmark.

Coverage strategy:
- 1 positive test per template (23 templates = 23 tests)
- 3 negative-case tests (no features should fire for clean SQL)
- 2 parse-error resilience tests
"""
from __future__ import annotations

import logging

import pytest

from clickadvisor.ml.features import FeatureExtractor, QueryFeatures

_fx = FeatureExtractor()


def extract(sql: str) -> QueryFeatures:
    return _fx.extract(sql)


# ---------------------------------------------------------------------------
# R-001 / R-002: exact_count_distinct_specialization + approx_count_distinct
# ---------------------------------------------------------------------------
def test_r001_count_distinct():
    f = extract("SELECT COUNT(DISTINCT user_id) FROM events")
    assert f.has_count_distinct is True


def test_r001_to_vector_bool_is_int():
    f = extract("SELECT COUNT(DISTINCT user_id) FROM events")
    v = f.to_vector()
    assert v["has_count_distinct"] == 1
    assert isinstance(v["has_count_distinct"], int)


# ---------------------------------------------------------------------------
# R-003: exact_quantile_candidate
# ---------------------------------------------------------------------------
def test_r003_quantile_exact():
    f = extract("SELECT quantileExact(0.95)(response_time) FROM requests")
    assert f.has_quantile_exact is True


# ---------------------------------------------------------------------------
# R-004: count_star_distinct_subquery
# ---------------------------------------------------------------------------
def test_r004_count_star_distinct_subquery():
    f = extract("SELECT COUNT(*) FROM (SELECT DISTINCT user_id FROM events)")
    assert f.has_subquery is True
    # COUNT(*) over subquery – no count_distinct at the outer level
    assert f.has_count_distinct is False


# ---------------------------------------------------------------------------
# R-005: function_on_datetime_filter (toDate equality)
# ---------------------------------------------------------------------------
def test_r005_todate_equality():
    f = extract("SELECT count() FROM events WHERE toDate(created_at) = '2024-01-15'")
    assert f.has_function_on_filter_column is True


# ---------------------------------------------------------------------------
# R-006: date_part_filter_to_range (toYYYYMM equality)
# ---------------------------------------------------------------------------
def test_r006_toyyyymm_equality():
    f = extract("SELECT count() FROM events WHERE toYYYYMM(event_date) = 202401")
    assert f.has_function_on_filter_column is True


# ---------------------------------------------------------------------------
# R-007: interval_start_filter_to_range (toStartOfHour equality)
# ---------------------------------------------------------------------------
def test_r007_tostartofhour_equality():
    f = extract("SELECT count() FROM logs WHERE toStartOfHour(ts) = '2024-01-15 14:00:00'")
    assert f.has_function_on_filter_column is True


# ---------------------------------------------------------------------------
# R-008: redundant_cast_on_filter
# ---------------------------------------------------------------------------
def test_r008_redundant_cast():
    f = extract("SELECT count() FROM users WHERE CAST(user_id AS UInt64) = 12345")
    assert f.has_cast is True
    assert f.has_function_on_filter_column is True


# ---------------------------------------------------------------------------
# R-009: singleton_in_predicate
# ---------------------------------------------------------------------------
def test_r009_singleton_in():
    f = extract("SELECT count() FROM events WHERE country IN ('RU')")
    assert f.has_in_with_single_value is True


# ---------------------------------------------------------------------------
# R-010: disjunction_chain_to_in
# ---------------------------------------------------------------------------
def test_r010_or_chain():
    f = extract(
        "SELECT count() FROM events WHERE country = 'RU' OR country = 'BY' OR country = 'KZ'"
    )
    assert f.has_or_chain_same_column is True


# ---------------------------------------------------------------------------
# R-011: having_without_aggregate
# ---------------------------------------------------------------------------
def test_r011_having_without_aggregate():
    f = extract(
        "SELECT user_id, COUNT(*) FROM events GROUP BY user_id "
        "HAVING country = 'RU' AND COUNT(*) > 100"
    )
    assert f.has_having is True
    assert f.has_having_without_aggregate is True
    assert f.has_group_by is True


# ---------------------------------------------------------------------------
# R-012: constant_predicate (WHERE TRUE)
# ---------------------------------------------------------------------------
def test_r012_constant_predicate():
    f = extract("SELECT count() FROM events WHERE TRUE AND user_id = 5")
    assert f.has_constant_predicate is True


# ---------------------------------------------------------------------------
# R-013: length_empty_predicate
# ---------------------------------------------------------------------------
def test_r013_length_zero_check():
    f = extract("SELECT count() FROM comments WHERE length(body) > 0")
    assert f.has_length_zero_check is True


# ---------------------------------------------------------------------------
# R-014: groupby_string_hash_candidate
# ---------------------------------------------------------------------------
def test_r014_groupby_string_column():
    f = extract("SELECT url, COUNT(*) FROM logs GROUP BY url")
    assert f.has_group_by is True
    assert f.has_group_by_string_column is True


# ---------------------------------------------------------------------------
# R-015: distinct_after_groupby
# ---------------------------------------------------------------------------
def test_r015_distinct_after_groupby():
    f = extract(
        "SELECT DISTINCT a, b FROM (SELECT a, b, COUNT(*) AS cnt FROM events GROUP BY a, b) LIMIT 100"
    )
    assert f.has_subquery is True
    assert f.has_group_by is True
    assert f.has_limit is True


# ---------------------------------------------------------------------------
# R-016: orderby_without_limit_in_subquery
# ---------------------------------------------------------------------------
def test_r016_orderby_no_limit_subquery():
    f = extract("SELECT COUNT(*) FROM (SELECT * FROM events ORDER BY created_at)")
    assert f.has_subquery_with_orderby_no_limit is True
    assert f.has_subquery is True


# ---------------------------------------------------------------------------
# R-017: subquery_filter_pushdown
# ---------------------------------------------------------------------------
def test_r017_subquery_filter_pushdown():
    f = extract(
        "SELECT * FROM (SELECT * FROM events WHERE status = 'active') WHERE user_id = 42"
    )
    assert f.has_nested_subquery_filter is True
    assert f.has_subquery is True


# ---------------------------------------------------------------------------
# R-018: union_without_all
# ---------------------------------------------------------------------------
def test_r018_union_not_all():
    f = extract("SELECT user_id FROM events_2023 UNION SELECT user_id FROM events_2024")
    assert f.has_union is True
    assert f.has_union_all is False


def test_r018_union_all_no_flag():
    f = extract("SELECT user_id FROM events_2023 UNION ALL SELECT user_id FROM events_2024")
    assert f.has_union is True
    assert f.has_union_all is True


# ---------------------------------------------------------------------------
# R-019: oversized_uint_type_narrowing (CREATE TABLE context)
# ---------------------------------------------------------------------------
def test_r019_create_table():
    f = extract(
        "CREATE TABLE events (event_type UInt64, user_id UInt64) ENGINE = MergeTree() ORDER BY event_type"
    )
    # No SELECT-level features should fire
    assert f.has_count_distinct is False
    assert f.has_select_star is False
    assert f.has_no_limit is False
    assert f.query_length_chars > 0


# ---------------------------------------------------------------------------
# R-020: unsafe_cast_without_default
# ---------------------------------------------------------------------------
def test_r020_throwing_cast():
    f = extract("SELECT CAST(raw_value AS UInt32) FROM events")
    assert f.has_cast is True
    assert f.has_cast_without_default is True


def test_r020_safe_cast_ordefault():
    f = extract("SELECT toUInt32OrDefault(raw_value) FROM events")
    assert f.has_cast is True
    assert f.has_cast_without_default is False


# ---------------------------------------------------------------------------
# D-003: select_star_on_wide_table
# ---------------------------------------------------------------------------
def test_d003_select_star():
    f = extract("SELECT * FROM events LIMIT 10")
    assert f.has_select_star is True
    assert f.has_limit is True
    assert f.has_no_limit is False


# ---------------------------------------------------------------------------
# D-004: missing_limit_on_unbounded_result
# ---------------------------------------------------------------------------
def test_d004_missing_limit():
    f = extract("SELECT user_id, event_type, created_at FROM events WHERE status = 'active'")
    assert f.has_no_limit is True
    assert f.has_limit is False


# ---------------------------------------------------------------------------
# D-007: final_modifier_usage
# ---------------------------------------------------------------------------
def test_d007_final_modifier():
    f = extract("SELECT count() FROM events FINAL WHERE user_id = 1")
    assert f.has_final_modifier is True


# ---------------------------------------------------------------------------
# D-014: async_insert_without_wait_flag
# ---------------------------------------------------------------------------
def test_d014_async_insert_no_wait():
    f = extract("INSERT INTO events SETTINGS async_insert=1 VALUES (1, 'click')")
    assert f.has_async_insert_setting is True
    assert f.has_async_insert_without_wait is True


def test_d014_async_insert_with_wait_ok():
    f = extract(
        "INSERT INTO events SETTINGS async_insert=1, wait_for_async_insert=1 VALUES (1, 'click')"
    )
    assert f.has_async_insert_setting is True
    assert f.has_async_insert_without_wait is False


# ---------------------------------------------------------------------------
# Negative cases: clean queries should produce all-False features
# ---------------------------------------------------------------------------
def test_negative_simple_count():
    """Simple timestamp-range query – no problematic patterns."""
    sql = (
        "SELECT count() FROM events "
        "WHERE created_at >= '2024-01-15 00:00:00' AND created_at < '2024-01-16 00:00:00'"
    )
    f = extract(sql)
    assert f.has_count_distinct is False
    assert f.has_select_star is False
    assert f.has_final_modifier is False
    assert f.has_function_on_filter_column is False
    assert f.has_quantile_exact is False
    assert f.has_async_insert_without_wait is False


def test_negative_aggregate_no_limit():
    """Aggregate query – missing_limit rule should NOT fire."""
    f = extract("SELECT COUNT(*) FROM events WHERE event_type = 'click'")
    assert f.has_no_limit is False


def test_negative_union_all_clean():
    """UNION ALL is fine – union_without_all should be False."""
    f = extract("SELECT id FROM a UNION ALL SELECT id FROM b LIMIT 100")
    assert f.has_union is True
    assert f.has_union_all is True


# ---------------------------------------------------------------------------
# Parse error resilience
# ---------------------------------------------------------------------------
def test_parse_error_returns_features(caplog):
    """Badly malformed SQL must not raise – fallback path returns QueryFeatures."""
    bad_sql = "SELECT @@@ BROKEN SQL @@@ FROM"
    with caplog.at_level(logging.WARNING, logger="clickadvisor.ml.features"):
        f = extract(bad_sql)
    assert isinstance(f, QueryFeatures)
    assert f.query_length_chars == len(bad_sql)


def test_parse_error_logs_warning(caplog):
    """A warning must be emitted when AST parsing fails."""
    with caplog.at_level(logging.WARNING):
        _fx.extract("SELECT FROM WHERE ??? !!!")
    assert any("AST parse failed" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# Numeric fields
# ---------------------------------------------------------------------------
def test_numeric_fields_basic():
    f = extract("SELECT user_id, event_type FROM events WHERE status = 'active'")
    assert f.table_count >= 1
    assert f.column_count_in_select == 2
    assert f.query_length_chars > 0


def test_where_clause_depth_increases_with_nesting():
    simple = extract("SELECT count() FROM events WHERE x = 1")
    nested = extract(
        "SELECT count() FROM events WHERE (a = 1 AND (b = 2 OR (c = 3 AND d = 4)))"
    )
    assert nested.where_clause_depth > simple.where_clause_depth


def test_to_vector_keys_match_fields():
    """to_vector() must return exactly the same set of field names as the dataclass."""
    import dataclasses
    f = extract("SELECT count() FROM events")
    vector = f.to_vector()
    field_names = {field.name for field in dataclasses.fields(QueryFeatures)}
    assert set(vector.keys()) == field_names

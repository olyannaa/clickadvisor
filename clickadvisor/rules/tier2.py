from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule


def _env(context: QueryContext, section: str) -> Mapping[str, Any]:
    if not context.environment:
        return {}
    value = context.environment.get(section)
    return value if isinstance(value, Mapping) else {}


def _flag(context: QueryContext, section: str, key: str) -> bool:
    value = _env(context, section).get(key)
    return bool(value) if isinstance(value, bool) else False


def _num(context: QueryContext, section: str, key: str) -> float | None:
    value = _env(context, section).get(key)
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _finding(rule: Rule, severity: str, description: str, suggestion: str) -> Finding:
    return Finding(
        rule_id=rule.rule_id,
        rule_name=rule.name,
        tier=rule.tier,
        severity=severity,
        description=description,
        suggestion=suggestion,
        confidence="advisory",
        ch_version_introduced=rule.ch_version_introduced,
    )


class R101OrderByKeyRedesign(Rule):
    rule_id = "R-101"
    name = "order_by_key_redesign"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        schema = context.schema_ddl or ""
        if not schema or not re.search(r"\bENGINE\s*=\s*MergeTree", schema, re.I):
            return None
        if not re.search(r"\bORDER\s+BY\s+tuple\s*\(\s*\)", schema, re.I):
            return None
        return _finding(self, "high", "MergeTree table uses ORDER BY tuple(), so data skipping is weak.", "Redesign ORDER BY around frequent filters and high-selectivity dimensions.")


class R102SkipIndexRecommendation(Rule):
    rule_id = "R-102"
    name = "skip_index_recommendation"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not re.search(r"\bLIKE\s+['\"]%", context.sql, re.I):
            return None
        return _finding(self, "medium", "Substring search can benefit from a token/ngram skip index.", "Consider tokenbf_v1 or ngrambf_v1 on the searched text column.")


class R103ProjectionRecommendation(Rule):
    rule_id = "R-103"
    name = "projection_recommendation"
    tier = "2"
    ch_version_introduced = "21.6"

    def check(self, context: QueryContext) -> Finding | None:
        if not (_flag(context, "workload", "repeated_group_by") or _flag(context, "workload", "repeated_query_shape")):
            return None
        if "GROUP BY" not in context.sql.upper():
            return None
        return _finding(self, "medium", "Repeated GROUP BY query shape may benefit from a projection.", "Evaluate a projection for this aggregation pattern and verify with EXPLAIN.")


class R104PrimaryKeyRefinement(Rule):
    rule_id = "R-104"
    name = "primary_key_refinement"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        schema = context.schema_ddl or ""
        if not schema or "PRIMARY KEY" in schema.upper():
            return None
        if "ORDER BY" not in schema.upper() or "WHERE" not in context.sql.upper():
            return None
        return _finding(self, "medium", "Table has ORDER BY but no explicit PRIMARY KEY while queries filter selectively.", "Consider a shorter PRIMARY KEY prefix aligned with frequent filters.")


class R105PartitionStrategyAdjustment(Rule):
    rule_id = "R-105"
    name = "partition_strategy_adjustment"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        parts = _num(context, "system_metrics", "active_parts")
        partitions = _num(context, "system_metrics", "active_partitions")
        if parts is None or partitions is None or partitions <= 0 or parts / partitions <= 100:
            return None
        return _finding(self, "high", "Table has many active parts per partition.", "Review partition key granularity and insert batching.")


class R106LowCardinalityConversion(Rule):
    rule_id = "R-106"
    name = "lowcardinality_conversion"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        schema = context.schema_ddl or context.sql
        if " String" not in schema:
            return None
        if not (_flag(context, "workload", "low_cardinality_strings") or re.search(r"\b(status|type|category|country)\s+String\b", schema, re.I)):
            return None
        return _finding(self, "medium", "Low-cardinality String columns can be stored more efficiently.", "Consider LowCardinality(String) after checking cardinality and mutation cost.")


class R107CodecRecommendation(Rule):
    rule_id = "R-107"
    name = "codec_recommendation"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        schema = context.schema_ddl or ""
        if not schema or "CODEC" in schema.upper():
            return None
        if not _flag(context, "workload", "compression_sensitive"):
            return None
        return _finding(self, "low", "Schema has compressible columns without explicit CODEC.", "Evaluate codecs such as Delta/ZSTD for time or numeric columns.")


class R108PrewhereInjection(Rule):
    rule_id = "R-108"
    name = "prewhere_injection"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if "WHERE" not in context.sql.upper() or "PREWHERE" in context.sql.upper():
            return None
        if not _flag(context, "workload", "wide_table"):
            return None
        return _finding(self, "medium", "Wide table query filters in WHERE only.", "Consider PREWHERE for selective predicates after verifying with EXPLAIN.")


class R109JoinReorderSmallOnRight(Rule):
    rule_id = "R-109"
    name = "join_reorder_small_on_right"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if "JOIN" not in context.sql.upper() or not _flag(context, "workload", "right_table_larger_than_left"):
            return None
        return _finding(self, "medium", "JOIN appears to put the larger table on the right side.", "Place the smaller build-side table on the right where possible.")


class R110JoinAlgorithmChoice(Rule):
    rule_id = "R-110"
    name = "join_algorithm_choice"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if "JOIN" not in context.sql.upper() or not _flag(context, "workload", "large_join"):
            return None
        return _finding(self, "medium", "Large JOIN needs explicit algorithm review.", "Evaluate join_algorithm=auto, grace_hash or partial_merge based on memory and table size.")


class R111MaterializedViewRecommendation(Rule):
    rule_id = "R-111"
    name = "materialized_view_recommendation"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not _flag(context, "workload", "repeated_expensive_query"):
            return None
        if "GROUP BY" not in context.sql.upper():
            return None
        return _finding(self, "medium", "Repeated expensive aggregation may benefit from a materialized view.", "Consider an AggregatingMergeTree materialized view after validating freshness requirements.")


class R112GroupByMultipassSplit(Rule):
    rule_id = "R-112"
    name = "groupby_multipass_split"
    tier = "2"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if "GROUP BY" not in context.sql.upper() or not _flag(context, "workload", "high_cardinality_group_by"):
            return None
        return _finding(self, "medium", "High-cardinality GROUP BY may exceed memory in one pass.", "Consider splitting aggregation into stages or using external aggregation settings.")

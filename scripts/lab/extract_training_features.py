from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sqlglot
import sqlglot.expressions as exp

from clickadvisor.core.sql_parser import SQLParser
from clickadvisor.ml.features import QueryFeatureExtractor

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_OUTPUT_DIR = Path("data/ml/expert_dataset/features")
SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}
TIER_ORDER = {"none": 0, "rag": 1, "detector": 2, "1A": 3, "1B": 4, "1C": 5, "2": 6}
AGGREGATION_FUNCTIONS = {
    "avg",
    "avgif",
    "count",
    "countif",
    "groupbitmap",
    "max",
    "maxif",
    "min",
    "minif",
    "quantile",
    "quantileexact",
    "sum",
    "sumif",
    "uniq",
    "uniqcombined",
    "uniqexact",
    "uniqhll12",
}


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    rule_vocabulary = sorted(
        {str(rule_id) for record in records for rule_id in record.get("rule_ids") or []}
    )
    rows = build_feature_rows(records, rule_vocabulary)
    write_outputs(rows, rule_vocabulary, args)
    print(
        "Extracted training features: "
        f"records={len(rows)}, rules={len(rule_vocabulary)}, output={args.output_dir}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build risk-label training feature rows.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_feature_rows(
    records: list[dict[str, Any]],
    rule_vocabulary: list[str],
) -> list[dict[str, Any]]:
    extractor = QueryFeatureExtractor()
    parser = SQLParser()
    rows: list[dict[str, Any]] = []
    for record in records:
        sql = str(record.get("sql") or "")
        normalized_sql = normalize_sql(sql)
        base_features = extractor.extract(sql).features
        structural_features = structural_features_for(sql, parser)
        rule_features = rule_features_for(record, rule_vocabulary)
        numeric_features = {
            **{f"base_{key}": value for key, value in base_features.items()},
            **structural_features,
            **rule_features,
        }
        rows.append(
            {
                "id": record["id"],
                "source": record.get("source"),
                "family": record.get("family"),
                "group_id": group_id_for(record),
                "sql_hash": record.get("sql_hash"),
                "normalized_sql": normalized_sql,
                "target": record.get("final_risk_label"),
                "rule_risk_label": record.get("rule_risk_label"),
                "measured_risk_label": record.get("measured_risk_label"),
                "label_source": record.get("label_source"),
                "rule_ids": record.get("rule_ids") or [],
                "features": numeric_features,
            }
        )
    return rows


def group_id_for(record: dict[str, Any]) -> str:
    origin = record.get("origin") if isinstance(record.get("origin"), dict) else {}
    parent_hash = origin.get("parent_sql_hash") or record.get("sql_hash")
    return "::".join(
        [
            str(record.get("source") or "unknown"),
            str(record.get("family") or "unknown"),
            str(parent_hash or record.get("id")),
        ]
    )


def normalize_sql(sql: str) -> str:
    text = re.sub(r"'(?:''|[^'])*'", " __str__ ", sql)
    text = re.sub(r'"(?:""|[^"])*"', " __str__ ", text)
    text = re.sub(r"\b0x[0-9a-f]+\b", " __num__ ", text, flags=re.I)
    text = re.sub(r"\b\d+(?:\.\d+)?\b", " __num__ ", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def structural_features_for(sql: str, parser: SQLParser) -> dict[str, float]:
    features = regex_structural_features(sql)
    try:
        ast = parser.parse(sql)
    except sqlglot.errors.ParseError:
        features["struct_parse_error"] = 1.0
        return features

    features["struct_parse_error"] = 0.0
    features.update(
        {
            "has_select_star": float(parser.has_top_level_select_star(ast)),
            "has_final": float(parser.has_final_modifier(ast)),
            "has_limit": float(any(True for _ in ast.find_all(exp.Limit))),
            "has_prewhere": float(bool(re.search(r"\bPREWHERE\b", sql, re.I))),
            "has_order_by": float(any(True for _ in ast.find_all(exp.Order))),
            "has_group_by_high_card": float(high_cardinality_group_by(ast, parser)),
            "join_count": float(sum(1 for _ in ast.find_all(exp.Join))),
            "subquery_count": float(sum(1 for _ in ast.find_all(exp.Subquery))),
            "function_on_filter": float(function_on_filter(ast, parser)),
            "distinct_count": float(distinct_count(ast, sql)),
            "aggregation_count": float(aggregation_count(ast)),
        }
    )
    return features


def regex_structural_features(sql: str) -> dict[str, float]:
    return {
        "sql_char_length": float(len(sql)),
        "sql_token_length": float(len(re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[^\s]", sql))),
        "has_select_star": float(bool(re.search(r"\bSELECT\s+\*", sql, re.I))),
        "has_final": float(bool(re.search(r"\bFINAL\b", sql, re.I))),
        "has_limit": float(bool(re.search(r"\bLIMIT\b", sql, re.I))),
        "has_prewhere": float(bool(re.search(r"\bPREWHERE\b", sql, re.I))),
        "has_order_by": float(bool(re.search(r"\bORDER\s+BY\b", sql, re.I))),
        "has_group_by_high_card": float(bool(re.search(r"\bGROUP\s+BY\b", sql, re.I))),
        "join_count": float(len(re.findall(r"\b(?:ANY|ALL|ASOF|GLOBAL|INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b", sql, re.I))),
        "subquery_count": float(max(0, len(re.findall(r"\bSELECT\b", sql, re.I)) - 1)),
        "function_on_filter": float(
            bool(re.search(r"\bWHERE\b[^;]*(?:toDate|toYYYY|toStartOf|lower|upper|CAST)\s*\(", sql, re.I | re.S))
        ),
        "distinct_count": float(len(re.findall(r"\bDISTINCT\b", sql, re.I))),
        "aggregation_count": float(
            len(re.findall(r"\b(?:count|sum|avg|min|max|uniq|quantile)[A-Za-z0-9_]*\s*\(", sql, re.I))
        ),
        "struct_parse_error": 1.0,
    }


def high_cardinality_group_by(ast: sqlglot.Expression, parser: SQLParser) -> bool:
    if parser.has_groupby_string_candidate(ast):
        return True
    for select in ast.find_all(exp.Select):
        group = select.args.get("group")
        if isinstance(group, exp.Group) and len(group.expressions) >= 3:
            return True
    return False


def function_on_filter(ast: sqlglot.Expression, parser: SQLParser) -> bool:
    return (
        parser.has_todate_equality(ast)
        or parser.has_date_part_equality(ast)
        or parser.has_interval_start_equality(ast)
        or parser.has_redundant_cast(ast)
    )


def distinct_count(ast: sqlglot.Expression, sql: str) -> int:
    count = sum(1 for node in ast.walk() if isinstance(node, exp.Distinct))
    if count:
        return count
    return len(re.findall(r"\bDISTINCT\b", sql, re.I))


def aggregation_count(ast: sqlglot.Expression) -> int:
    count = 0
    for node in ast.walk():
        if isinstance(node, exp.Count | exp.Sum | exp.Avg | exp.Min | exp.Max):
            count += 1
        elif isinstance(node, exp.Anonymous) and node.name.lower() in AGGREGATION_FUNCTIONS:
            count += 1
    return count


def rule_features_for(
    record: dict[str, Any],
    rule_vocabulary: list[str],
) -> dict[str, float]:
    rule_ids = {str(rule_id) for rule_id in record.get("rule_ids") or []}
    features = {
        "rule_findings_count": float(record.get("rule_findings_count") or 0),
        "rule_max_severity": float(SEVERITY_ORDER.get(str(record.get("rule_max_severity")), 0)),
        "rule_max_tier": float(TIER_ORDER.get(str(record.get("rule_max_tier")), 0)),
    }
    for rule_id in rule_vocabulary:
        safe_rule_id = rule_id.lower().replace("-", "_")
        features[f"rule_present_{safe_rule_id}"] = float(rule_id in rule_ids)
    return features


def write_outputs(
    rows: list[dict[str, Any]],
    rule_vocabulary: list[str],
    args: argparse.Namespace,
) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    features_path = args.output_dir / "features.jsonl"
    with features_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    label_counts = Counter(str(row["target"]) for row in rows)
    label_source_counts = Counter(str(row.get("label_source")) for row in rows)
    feature_names = sorted({name for row in rows for name in row["features"]})
    group_sizes = Counter(str(row["group_id"]) for row in rows)
    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/extract_training_features.py",
        "dataset_path": str(args.dataset),
        "features_path": str(features_path),
        "record_count": len(rows),
        "feature_count": len(feature_names),
        "feature_groups": {
            "sql_text": ["normalized_sql", "sql_char_length", "sql_token_length"],
            "structural": [
                "has_select_star",
                "has_final",
                "has_limit",
                "has_prewhere",
                "has_order_by",
                "has_group_by_high_card",
                "join_count",
                "subquery_count",
                "function_on_filter",
                "distinct_count",
                "aggregation_count",
            ],
            "rule_derived": [
                "rule_findings_count",
                "rule_max_severity",
                "rule_max_tier",
                "rule_present_*",
            ],
        },
        "feature_names": feature_names,
        "rule_vocabulary": rule_vocabulary,
        "label_counts": dict(label_counts.most_common()),
        "label_source_counts": dict(label_source_counts.most_common()),
        "group_count": len(group_sizes),
        "max_group_size": max(group_sizes.values(), default=0),
        "methodology_note": (
            "Most labels are rule_only, so baselines estimate a triage layer over the "
            "rule engine plus measured metric signal rather than replacing deterministic rules."
        ),
    }
    (args.output_dir / "feature_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

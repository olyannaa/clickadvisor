from __future__ import annotations

import logging
import re
from collections.abc import Mapping
from dataclasses import asdict, dataclass

import sqlglot
import sqlglot.expressions as exp

from clickadvisor.core.sql_parser import SQLParser

FeatureMap = dict[str, float]

_ASYNC_INSERT_RE = re.compile(r"\basync_insert\s*=\s*1\b", re.IGNORECASE)
_WAIT_FLAG_RE = re.compile(r"\bwait_for_async_insert\s*=\s*1\b", re.IGNORECASE)
_INSERT_RE = re.compile(r"\bINSERT\b", re.IGNORECASE)
_CREATE_TABLE_RE = re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE)
_UINT64_COL_RE = re.compile(r"`?(\w+)`?\s+(?:UInt64|Int64)\b", re.IGNORECASE)
_LOW_CARDINALITY_PARTS = frozenset(
    ["type", "status", "category", "flag", "level", "kind", "state", "mode", "priority", "rank", "class"]
)
_TO_TYPE_PREFIXES = (
    "touint", "toint", "tofloat", "tostring", "todecimal",
    "todate", "todatetime", "tofixedstring", "touuid",
)
_OR_SAFE_SUFFIXES = ("orzero", "ornull", "ordefault")


@dataclass(slots=True)
class QueryFeatures:
    """Structured AST/text feature vector for a single SQL query.

    Boolean fields map 1-to-1 to patterns from the deterministic rule engine
    but are computed independently so the classifier can generalise beyond
    exact rule boundaries.
    """

    # --- count / distinct ---
    has_count_distinct: bool
    # --- projection ---
    has_select_star: bool
    # --- table modifiers ---
    has_final_modifier: bool
    # --- set operators ---
    has_union: bool
    has_union_all: bool
    # --- grouping ---
    has_group_by: bool
    has_group_by_string_column: bool
    # --- having ---
    has_having: bool
    has_having_without_aggregate: bool
    # --- filter functions ---
    has_function_on_filter_column: bool
    # --- subquery ---
    has_subquery: bool
    has_subquery_with_orderby_no_limit: bool
    has_nested_subquery_filter: bool
    # --- predicate patterns ---
    has_or_chain_same_column: bool
    has_in_with_single_value: bool
    # --- quantile ---
    has_quantile_exact: bool
    # --- cast ---
    has_cast: bool
    has_cast_without_default: bool
    # --- async insert ---
    has_async_insert_setting: bool
    has_async_insert_without_wait: bool
    # --- limit ---
    has_limit: bool
    has_no_limit: bool
    # --- misc predicates ---
    has_constant_predicate: bool
    has_length_zero_check: bool
    # --- numeric shape features ---
    table_count: int
    column_count_in_select: int
    where_clause_depth: int
    query_length_chars: int

    def to_vector(self) -> dict[str, float | int]:
        """Convert to numeric dict for model input. Bools become 0/1."""
        result: dict[str, float | int] = {}
        for field, value in asdict(self).items():
            result[field] = int(value) if isinstance(value, bool) else value
        return result


def _node_depth(node: exp.Expression) -> int:
    """Recursively compute maximum AST depth below *node*."""
    children: list[exp.Expression] = []
    for val in node.args.values():
        if isinstance(val, exp.Expression):
            children.append(val)
        elif isinstance(val, list):
            children.extend(c for c in val if isinstance(c, exp.Expression))
    if not children:
        return 0
    return 1 + max(_node_depth(c) for c in children)


def _where_depth(ast: sqlglot.Expression) -> int:
    max_depth = 0
    for where in ast.find_all(exp.Where):
        max_depth = max(max_depth, _node_depth(where.this))
    return max_depth


def _has_cast_without_default(ast: sqlglot.Expression) -> bool:
    """True when a throwing CAST (no OrDefault/OrZero/OrNull) is present."""
    for cast in ast.find_all(exp.Cast):
        if isinstance(cast.this, exp.Column):
            return True
    for fn in ast.find_all(exp.Anonymous):
        name = fn.name.lower()
        if name.endswith(_OR_SAFE_SUFFIXES):
            continue
        if name.startswith(_TO_TYPE_PREFIXES):
            if fn.expressions and isinstance(fn.expressions[0], exp.Column):
                return True
    return False


def _has_cast(ast: sqlglot.Expression) -> bool:
    """True when any cast or type-conversion function is present."""
    if any(True for _ in ast.find_all(exp.Cast)):
        return True
    for fn in ast.find_all(exp.Anonymous):
        if fn.name.lower().startswith(_TO_TYPE_PREFIXES):
            return True
    return False


def _has_async_insert_without_wait(sql: str) -> bool:
    return bool(
        _INSERT_RE.search(sql)
        and _ASYNC_INSERT_RE.search(sql)
        and not _WAIT_FLAG_RE.search(sql)
    )


def _has_oversized_uint_candidate(sql: str) -> bool:
    if not _CREATE_TABLE_RE.search(sql):
        return False
    for match in _UINT64_COL_RE.finditer(sql):
        col = match.group(1).lower()
        parts = col.split("_")
        if _LOW_CARDINALITY_PARTS.intersection(parts):
            return True
    return False


class FeatureExtractor:
    """Extract QueryFeatures from raw SQL via sqlglot AST with regex fallback."""

    def __init__(self) -> None:
        self._parser = SQLParser()

    def extract(self, sql: str) -> QueryFeatures:
        """Parse *sql* via sqlglot (clickhouse dialect) and extract all features.

        If sqlglot raises ParseError the regex fallback path is used and a
        warning is logged. The returned QueryFeatures will have False/0 for any
        field that cannot be derived from text alone.
        """
        try:
            ast = self._parser.parse(sql)
        except sqlglot.errors.ParseError:
            logging.warning(
                "AST parse failed for SQL (len=%d), using regex fallback",
                len(sql),
            )
            return self._regex_fallback(sql)
        return self._from_ast(ast, sql)

    def _from_ast(self, ast: sqlglot.Expression, sql: str) -> QueryFeatures:
        p = self._parser
        top = ast if isinstance(ast, exp.Select) else None

        has_union = any(True for _ in ast.find_all(exp.Union))
        has_union_all = any(
            u.args.get("distinct") is False for u in ast.find_all(exp.Union)
        )
        has_having = any(True for _ in ast.find_all(exp.Having))
        has_subquery = any(True for _ in ast.find_all(exp.Subquery))
        has_limit = any(True for _ in ast.find_all(exp.Limit))
        # GROUP BY anywhere in the query tree (including subqueries)
        has_group_by = any(
            s.args.get("group") is not None for s in ast.find_all(exp.Select)
        )

        col_count = len(top.expressions) if top is not None else 0
        t_count = sum(1 for _ in ast.find_all(exp.Table))

        return QueryFeatures(
            has_count_distinct=p.has_count_distinct(ast),
            has_select_star=p.has_top_level_select_star(ast),
            has_final_modifier=p.has_final_modifier(ast),
            has_union=has_union,
            has_union_all=has_union_all,
            has_group_by=has_group_by,
            has_group_by_string_column=p.has_groupby_string_candidate(ast),
            has_having=has_having,
            has_having_without_aggregate=p.has_having_without_agg(ast),
            has_function_on_filter_column=(
                p.has_todate_equality(ast)
                or p.has_date_part_equality(ast)
                or p.has_interval_start_equality(ast)
                or p.has_redundant_cast(ast)
            ),
            has_subquery=has_subquery,
            has_subquery_with_orderby_no_limit=p.has_orderby_without_limit_in_subquery(ast),
            has_nested_subquery_filter=p.has_subquery_filter_pushdown(ast),
            has_or_chain_same_column=p.has_disjunction_chain(ast),
            has_in_with_single_value=p.has_in_singleton(ast),
            has_quantile_exact=p.has_quantile_exact(ast),
            has_cast=_has_cast(ast),
            has_cast_without_default=_has_cast_without_default(ast),
            has_async_insert_setting=bool(_ASYNC_INSERT_RE.search(sql)),
            has_async_insert_without_wait=_has_async_insert_without_wait(sql),
            has_limit=has_limit,
            has_no_limit=p.has_missing_limit(ast),
            has_constant_predicate=p.has_constant_predicate(ast),
            has_length_zero_check=p.has_length_empty_pattern(ast),
            table_count=t_count,
            column_count_in_select=col_count,
            where_clause_depth=_where_depth(ast),
            query_length_chars=len(sql),
        )

    def _regex_fallback(self, sql: str) -> QueryFeatures:
        has_union = bool(re.search(r"\bUNION\b", sql, re.I))
        has_union_all = bool(re.search(r"\bUNION\s+ALL\b", sql, re.I))
        has_limit = bool(re.search(r"\bLIMIT\b", sql, re.I))
        has_cast = bool(
            re.search(r"\bCAST\s*\(", sql, re.I)
            or any(re.search(rf"\b{p}", sql, re.I) for p in _TO_TYPE_PREFIXES)
        )
        return QueryFeatures(
            has_count_distinct=bool(re.search(r"COUNT\s*\(\s*DISTINCT", sql, re.I)),
            has_select_star=bool(re.search(r"\bSELECT\s+\*", sql, re.I)),
            has_final_modifier=bool(re.search(r"\bFINAL\b", sql, re.I)),
            has_union=has_union,
            has_union_all=has_union_all,
            has_group_by=bool(re.search(r"\bGROUP\s+BY\b", sql, re.I)),
            has_group_by_string_column=False,
            has_having=bool(re.search(r"\bHAVING\b", sql, re.I)),
            has_having_without_aggregate=False,
            has_function_on_filter_column=bool(
                re.search(r"\btoDate\s*\(|\btoYYYYMM\s*\(|\btoStartOf", sql, re.I)
            ),
            has_subquery=bool(re.search(r"\bSELECT\b.*\bSELECT\b", sql, re.I | re.DOTALL)),
            has_subquery_with_orderby_no_limit=False,
            has_nested_subquery_filter=False,
            has_or_chain_same_column=False,
            has_in_with_single_value=bool(re.search(r"\bIN\s*\(\s*'[^']*'\s*\)", sql, re.I)),
            has_quantile_exact=bool(re.search(r"\bquantileExact\b", sql, re.I)),
            has_cast=has_cast,
            has_cast_without_default=has_cast,
            has_async_insert_setting=bool(_ASYNC_INSERT_RE.search(sql)),
            has_async_insert_without_wait=_has_async_insert_without_wait(sql),
            has_limit=has_limit,
            has_no_limit=False,
            has_constant_predicate=bool(
                re.search(r"\bWHERE\b.*\bTRUE\b", sql, re.I | re.DOTALL)
                or re.search(r"\b1\s*=\s*1\b", sql, re.I)
            ),
            has_length_zero_check=bool(re.search(r"\blength\s*\(", sql, re.I)),
            table_count=0,
            column_count_in_select=0,
            where_clause_depth=0,
            query_length_chars=len(sql),
        )


# ---------------------------------------------------------------------------
# Legacy classes — kept for backward compatibility with clickadvisor/ml/dataset.py
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FeatureVector:
    sql: str
    features: FeatureMap


class QueryFeatureExtractor:
    """Extract deterministic AST/text features for classical ML baselines."""

    def __init__(self) -> None:
        self.parser = SQLParser()

    def extract(self, sql: str) -> FeatureVector:
        features = self._base_text_features(sql)
        try:
            ast = self.parser.parse(sql)
        except sqlglot.errors.ParseError:
            features["parse_error"] = 1.0
            features.update(self._regex_features(sql))
            return FeatureVector(sql=sql, features=features)

        features["parse_error"] = 0.0
        features.update(self._ast_shape_features(ast))
        features.update(self._rule_pattern_features(ast, sql))
        return FeatureVector(sql=sql, features=features)

    def _base_text_features(self, sql: str) -> FeatureMap:
        normalized = sql.strip()
        return {
            "sql_length_chars": float(len(normalized)),
            "sql_line_count": float(max(1, normalized.count("\n") + 1)),
            "contains_comment": float("--" in normalized or "/*" in normalized),
            "contains_settings_clause": float(bool(re.search(r"\bsettings\b", normalized, re.I))),
        }

    def _ast_shape_features(self, ast: sqlglot.Expression) -> FeatureMap:
        top_level_select = isinstance(ast, exp.Select)
        group = ast.args.get("group") if top_level_select else None
        return {
            "is_select": float(top_level_select),
            "is_insert": float(isinstance(ast, exp.Insert)),
            "is_create": float(isinstance(ast, exp.Create)),
            "select_count": float(sum(1 for _ in ast.find_all(exp.Select))),
            "table_count": float(sum(1 for _ in ast.find_all(exp.Table))),
            "join_count": float(sum(1 for _ in ast.find_all(exp.Join))),
            "subquery_count": float(sum(1 for _ in ast.find_all(exp.Subquery))),
            "where_count": float(sum(1 for _ in ast.find_all(exp.Where))),
            "having_count": float(sum(1 for _ in ast.find_all(exp.Having))),
            "order_count": float(sum(1 for _ in ast.find_all(exp.Order))),
            "limit_count": float(sum(1 for _ in ast.find_all(exp.Limit))),
            "groupby_key_count": float(len(group.expressions) if isinstance(group, exp.Group) else 0),
            "function_call_count": float(self._function_call_count(ast)),
            "aggregate_call_count": float(self._aggregate_call_count(ast)),
            "literal_count": float(sum(1 for _ in ast.find_all(exp.Literal))),
        }

    def _rule_pattern_features(self, ast: sqlglot.Expression, sql: str) -> FeatureMap:
        return {
            "has_count_distinct": float(self.parser.has_count_distinct(ast)),
            "has_quantile_exact": float(self.parser.has_quantile_exact(ast)),
            "has_count_star_distinct_subquery": float(
                self.parser.has_count_star_distinct_subquery(ast)
            ),
            "has_todate_equality": float(self.parser.has_todate_equality(ast)),
            "has_date_part_equality": float(self.parser.has_date_part_equality(ast)),
            "has_interval_start_equality": float(self.parser.has_interval_start_equality(ast)),
            "has_function_on_filter_column": float(self._has_function_on_filter_column(ast)),
            "has_redundant_cast": float(self.parser.has_redundant_cast(ast)),
            "has_singleton_in": float(self.parser.has_in_singleton(ast)),
            "has_disjunction_chain": float(self.parser.has_disjunction_chain(ast)),
            "has_having_without_aggregate": float(self.parser.has_having_without_agg(ast)),
            "has_constant_predicate": float(self.parser.has_constant_predicate(ast)),
            "has_length_empty_pattern": float(self.parser.has_length_empty_pattern(ast)),
            "has_groupby_string_candidate": float(self.parser.has_groupby_string_candidate(ast)),
            "has_distinct_after_groupby": float(self.parser.has_distinct_after_groupby(ast)),
            "has_orderby_without_limit_subquery": float(
                self.parser.has_orderby_without_limit_in_subquery(ast)
            ),
            "has_subquery_filter_pushdown": float(self.parser.has_subquery_filter_pushdown(ast)),
            "has_top_level_select_star": float(self.parser.has_top_level_select_star(ast)),
            "has_missing_limit": float(self.parser.has_missing_limit(ast)),
            "has_union_not_all": float(self.parser.has_union_not_all(ast)),
            "has_final_modifier": float(self.parser.has_final_modifier(ast)),
            "has_throwing_cast": float(self._has_throwing_cast(ast)),
            "has_async_insert_without_wait": float(self._has_async_insert_without_wait(sql)),
            "has_oversized_int_candidate": float(self._has_oversized_int_candidate(sql)),
        }

    def _regex_features(self, sql: str) -> FeatureMap:
        return {
            "has_async_insert_without_wait": float(self._has_async_insert_without_wait(sql)),
            "has_oversized_int_candidate": float(self._has_oversized_int_candidate(sql)),
        }

    def _function_call_count(self, ast: sqlglot.Expression) -> int:
        function_types = (exp.Anonymous, exp.Cast, exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max)
        return sum(1 for node in ast.walk() if isinstance(node, function_types))

    def _aggregate_call_count(self, ast: sqlglot.Expression) -> int:
        aggregate_types = (exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max)
        return sum(1 for node in ast.walk() if isinstance(node, aggregate_types))

    def _has_function_on_filter_column(self, ast: sqlglot.Expression) -> bool:
        return (
            self.parser.has_todate_equality(ast)
            or self.parser.has_date_part_equality(ast)
            or self.parser.has_interval_start_equality(ast)
            or self.parser.has_redundant_cast(ast)
        )

    def _has_throwing_cast(self, ast: sqlglot.Expression) -> bool:
        for cast in ast.find_all(exp.Cast):
            if isinstance(cast.this, exp.Column):
                return True
        for function in ast.find_all(exp.Anonymous):
            name = function.name.lower()
            if name.endswith(("orzero", "ornull", "ordefault")):
                continue
            if name.startswith(("touint", "toint", "tofloat", "tostring", "todecimal", "todate")):
                return bool(function.expressions and isinstance(function.expressions[0], exp.Column))
        return False

    def _has_async_insert_without_wait(self, sql: str) -> bool:
        return bool(
            re.search(r"\binsert\b", sql, re.I)
            and re.search(r"\basync_insert\s*=\s*1\b", sql, re.I)
            and not re.search(r"\bwait_for_async_insert\s*=\s*1\b", sql, re.I)
        )

    def _has_oversized_int_candidate(self, sql: str) -> bool:
        if not re.search(r"\bcreate\s+table\b", sql, re.I):
            return False
        return bool(
            re.search(
                r"\b(?:event_type|order_status|log_level|session_type|account_status|payment_type)\s+U?Int64\b",
                sql,
                re.I,
            )
        )


def ordered_feature_names(rows: list[Mapping[str, float]]) -> list[str]:
    names: set[str] = set()
    for row in rows:
        names.update(row)
    return sorted(names)

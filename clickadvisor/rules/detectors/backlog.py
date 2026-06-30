from __future__ import annotations

import re

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule


def _finding(
    rule: Rule,
    severity: str,
    description: str,
    suggestion: str,
    *,
    confidence: str = "advisory",
) -> Finding:
    return Finding(
        rule_id=rule.rule_id,
        rule_name=rule.name,
        tier=rule.tier,
        severity=severity,
        description=description,
        suggestion=suggestion,
        confidence=confidence,
        ch_version_introduced=rule.ch_version_introduced,
    )


def _schema_text(context: QueryContext) -> str:
    return context.schema_ddl or context.sql


class D001FullScanOnPartitionedTable(Rule):
    rule_id = "D-001"
    name = "full_scan_on_partitioned_table"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        schema = context.schema_ddl
        if not schema or "PARTITION BY" not in schema.upper():
            return None
        match = re.search(r"\bPARTITION\s+BY\s+(.+?)(?:\s+ORDER\s+BY|\s+PRIMARY\s+KEY|\s+SETTINGS|$)", schema, re.I | re.S)
        if not match:
            return None
        partition_expr = match.group(1).strip()
        identifiers = {item.lower() for item in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", partition_expr)}
        functions = {"toyyyymm", "todate", "tostartofmonth", "tostartofday", "tostartofyear"}
        partition_cols = identifiers - functions
        where_match = re.search(r"\bWHERE\b(.+?)(?:\bGROUP\b|\bORDER\b|\bLIMIT\b|$)", context.sql, re.I | re.S)
        where_text = where_match.group(1).lower() if where_match else ""
        if partition_cols and any(col in where_text for col in partition_cols):
            return None
        return _finding(
            self,
            "high",
            f"Таблица партиционирована по {partition_expr}, но запрос не фильтрует partition key.",
            "Добавьте фильтр по partition-колонке или временной функции партиционирования.",
        )


class D002CrossJoinRisk(Rule):
    rule_id = "D-002"
    name = "cross_join_risk"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        if re.search(r"\bCROSS\s+JOIN\b", sql, re.I):
            return _finding(self, "high", "Запрос содержит CROSS JOIN.", "Проверьте, что декартово произведение намеренное.")
        for match in re.finditer(r"\bJOIN\b(?P<body>.*?)(?=\bJOIN\b|\bWHERE\b|\bGROUP\b|\bORDER\b|\bLIMIT\b|$)", sql, re.I | re.S):
            body = match.group("body")
            on_match = re.search(r"\bON\b(.+)", body, re.I | re.S)
            if not on_match or "=" not in on_match.group(1):
                return _finding(self, "high", "JOIN не содержит equality-условия.", "Добавьте ON с equality-ключами соединения.")
        return None


class D005LeadingWildcardLike(Rule):
    rule_id = "D-005"
    name = "leading_wildcard_like"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not re.search(r"\bLIKE\s+['\"]%", context.sql, re.I):
            return None
        return _finding(
            self,
            "medium",
            "LIKE с leading wildcard не может эффективно использовать индекс.",
            "Рассмотрите ngram/token skip-index или другой способ поиска по подстроке.",
        )


class D006ArrayJoinBeforeFilter(Rule):
    rule_id = "D-006"
    name = "arrayjoin_before_filter"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        sql = context.sql
        array_pos = sql.lower().find("arrayjoin")
        where_pos = sql.lower().find("where")
        if array_pos < 0 or where_pos < 0 or array_pos > where_pos:
            return None
        return _finding(
            self,
            "high",
            "arrayJoin встречается до WHERE и может резко увеличить промежуточную кардинальность.",
            "Отфильтруйте строки до arrayJoin или вынесите arrayJoin в более поздний этап.",
        )


class D008SampleWithoutSampleBy(Rule):
    rule_id = "D-008"
    name = "sample_without_sample_by"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not re.search(r"\bSAMPLE\b", context.sql, re.I):
            return None
        if context.schema_ddl and re.search(r"\bSAMPLE\s+BY\b", context.schema_ddl, re.I):
            return None
        return _finding(
            self,
            "low",
            "Запрос использует SAMPLE, но schema DDL не содержит SAMPLE BY.",
            "Добавьте SAMPLE BY в MergeTree DDL или используйте явную sampling-логику.",
        )


class D009NullableWithoutNeed(Rule):
    rule_id = "D-009"
    name = "nullable_without_need"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        text = _schema_text(context)
        match = re.search(r"\b([A-Za-z_][A-Za-z0-9_]*)\s+Nullable\s*\(", text, re.I)
        if not match:
            return None
        env = context.environment or {}
        null_counts = env.get("null_counts")
        if isinstance(null_counts, dict) and null_counts.get(match.group(1), 1) != 0:
            return None
        return _finding(
            self,
            "low",
            f"Колонка {match.group(1)} объявлена Nullable; это добавляет NULL bitmap.",
            "Если NULL-значений нет, рассмотрите non-nullable тип.",
        )


class D010UnusedColumnsInSelect(Rule):
    rule_id = "D-010"
    name = "unused_columns_in_select"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        match = re.search(
            r"SELECT\s+(?P<outer>[A-Za-z0-9_,\s]+)\s+FROM\s*\(\s*SELECT\s+(?P<inner>[A-Za-z0-9_,\s]+)\s+FROM\b",
            context.sql,
            re.I | re.S,
        )
        if not match:
            return None
        outer = {part.strip().lower() for part in match.group("outer").split(",")}
        inner = {part.strip().lower() for part in match.group("inner").split(",")}
        unused = sorted(inner - outer)
        if not unused:
            return None
        return _finding(
            self,
            "low",
            f"Подзапрос проектирует неиспользуемые колонки: {', '.join(unused)}.",
            "Оставьте во внутреннем SELECT только колонки, используемые внешним уровнем.",
        )


class D011ImplicitTypeCoercionInJoin(Rule):
    rule_id = "D-011"
    name = "implicit_type_coercion_in_join"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        if not re.search(r"\bJOIN\b.*\bON\b", context.sql, re.I | re.S):
            return None
        cast_pattern = r"\b(?:CAST|to(?:U?Int(?:8|16|32|64)?|String|UUID|Date(?:Time)?))\s*\([^)]*\)\s*="
        if re.search(cast_pattern, context.sql, re.I):
            return _finding(
                self,
                "high",
                "JOIN ON содержит явное приведение типа, что обычно указывает на несовпадение типов ключей.",
                "Выровняйте типы JOIN-ключей в схеме или подготовительном слое.",
            )
        return None


class D012WindowFunctionWithoutPartition(Rule):
    rule_id = "D-012"
    name = "window_function_without_partition"
    tier = "detector"
    ch_version_introduced = "21.1"

    def check(self, context: QueryContext) -> Finding | None:
        if not re.search(r"\bOVER\s*\((?![^)]*\bPARTITION\s+BY\b)", context.sql, re.I | re.S):
            return None
        return _finding(
            self,
            "medium",
            "Window function без PARTITION BY может требовать память на весь набор строк.",
            "Добавьте PARTITION BY, если расчёт можно разбить по ключу.",
        )


class D013DeeplyNestedSubqueries(Rule):
    rule_id = "D-013"
    name = "deeply_nested_subqueries"
    tier = "detector"
    ch_version_introduced = "1.0"

    def check(self, context: QueryContext) -> Finding | None:
        depth = 0
        max_depth = 0
        for char in context.sql:
            if char == "(":
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ")":
                depth = max(0, depth - 1)
        select_count = len(re.findall(r"\bSELECT\b", context.sql, re.I))
        if max_depth <= 3 or select_count < 4:
            return None
        return _finding(
            self,
            "low",
            f"Запрос содержит глубокую вложенность подзапросов: depth={max_depth}.",
            "Рассмотрите CTE через WITH ... AS для читаемости и предсказуемости оптимизации.",
        )

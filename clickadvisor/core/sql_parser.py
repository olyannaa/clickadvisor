from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import datetime, timedelta

import sqlglot
import sqlglot.expressions as exp


class SQLParser:
    def parse(self, sql: str) -> sqlglot.Expression:
        try:
            return sqlglot.parse_one(sql, dialect="clickhouse")
        except sqlglot.errors.ParseError:
            normalized = self._normalize_union_syntax(sql)
            if normalized == sql:
                raise
            return sqlglot.parse_one(normalized, dialect="clickhouse")

    def find_all(
        self,
        ast: sqlglot.Expression,
        node_type: type[exp.Expression],
    ) -> list[exp.Expression]:
        return list(ast.find_all(node_type))

    def has_count_distinct(self, ast: sqlglot.Expression) -> bool:
        return self.get_count_distinct(ast) is not None

    def has_quantile_exact(self, ast: sqlglot.Expression) -> bool:
        return self.get_quantile_exact(ast) is not None

    def has_todate_equality(self, ast: sqlglot.Expression) -> bool:
        return self._find_todate_equality(ast) is not None

    def has_date_part_equality(self, ast: sqlglot.Expression) -> bool:
        return self.get_date_part_equality(ast) is not None

    def has_interval_start_equality(self, ast: sqlglot.Expression) -> bool:
        return self.get_interval_start_equality(ast) is not None

    def has_disjunction_chain(self, ast: sqlglot.Expression) -> bool:
        return self._find_disjunction_chain(ast) is not None

    def has_count_star_distinct_subquery(self, ast: sqlglot.Expression) -> bool:
        return self.get_count_star_distinct_subquery(ast) is not None

    def has_top_level_select_star(self, ast: sqlglot.Expression) -> bool:
        if not isinstance(ast, exp.Select):
            return False
        return any(isinstance(expression, exp.Star) for expression in ast.expressions)

    def has_union_not_all(self, ast: sqlglot.Expression) -> bool:
        for union in ast.find_all(exp.Union):
            if union.args.get("distinct") is not False:
                return True
        return False

    def has_having_without_agg(self, ast: sqlglot.Expression) -> bool:
        for having in ast.find_all(exp.Having):
            if self._having_contains_non_aggregate_predicate(having.this):
                return True
        return False

    def has_orderby_without_limit_in_subquery(self, ast: sqlglot.Expression) -> bool:
        return self.get_orderby_without_limit_subquery(ast) is not None

    def has_subquery_filter_pushdown(self, ast: sqlglot.Expression) -> bool:
        return self.get_subquery_filter_pushdown(ast) is not None

    def has_final_modifier(self, ast: sqlglot.Expression) -> bool:
        return any(isinstance(node, exp.Final) for node in ast.walk())

    def has_redundant_cast(self, ast: sqlglot.Expression) -> bool:
        return self.get_redundant_cast(ast) is not None

    def has_in_singleton(self, ast: sqlglot.Expression) -> bool:
        return self.get_in_singleton(ast) is not None

    def has_constant_predicate(self, ast: sqlglot.Expression) -> bool:
        return self.get_constant_predicate(ast) is not None

    def has_length_empty_pattern(self, ast: sqlglot.Expression) -> bool:
        return self.get_length_empty_pattern(ast) is not None

    def has_groupby_string_candidate(self, ast: sqlglot.Expression) -> bool:
        return self.get_groupby_string_candidate(ast) is not None

    def has_distinct_after_groupby(self, ast: sqlglot.Expression) -> bool:
        return self.get_distinct_after_groupby(ast) is not None

    def has_missing_limit(self, ast: sqlglot.Expression) -> bool:
        if not isinstance(ast, exp.Select):
            return False
        if ast.args.get("limit") is not None:
            return False
        return not self.has_top_level_aggregation(ast)

    def has_top_level_aggregation(self, ast: sqlglot.Expression) -> bool:
        if not isinstance(ast, exp.Select):
            return False
        for expression in ast.expressions:
            if self._contains_aggregate(expression) or self._contains_uniq_function(expression):
                return True
        return False

    def get_count_distinct(self, ast: sqlglot.Expression) -> str | None:
        for count in ast.find_all(exp.Count):
            if isinstance(count.this, exp.Distinct):
                if count.this.expressions:
                    return str(count.this.expressions[0].sql(dialect="clickhouse"))
                return str(count.this.sql(dialect="clickhouse"))
        return None

    def get_quantile_exact(self, ast: sqlglot.Expression) -> tuple[str, str] | None:
        for agg in ast.find_all(exp.ParameterizedAgg):
            if str(agg.this).lower() != "quantileexact":
                continue
            level = agg.expressions[0].sql(dialect="clickhouse") if agg.expressions else "0.95"
            params = agg.args.get("params") or []
            if not params:
                continue
            return level, params[0].sql(dialect="clickhouse")
        return None

    def get_todate_equality(self, ast: sqlglot.Expression) -> tuple[str, str] | None:
        return self._find_todate_equality(ast)

    def get_date_part_equality(
        self,
        ast: sqlglot.Expression,
    ) -> tuple[str, str, str] | None:
        function_names = {"toyyyymm", "toyyyymmdd", "tomonth", "tostartofmonth"}
        for eq in ast.find_all(exp.EQ):
            match = self._match_function_equality(eq, function_names)
            if match is not None:
                return match
        return None

    def get_interval_start_equality(
        self,
        ast: sqlglot.Expression,
    ) -> tuple[str, str, str] | None:
        function_names = {"tostartofhour", "tostartofday", "tostartoffifteenminutes"}
        for eq in ast.find_all(exp.EQ):
            match = self._match_function_equality(eq, function_names)
            if match is not None:
                return match
        return None

    def get_disjunction_chain(self, ast: sqlglot.Expression) -> tuple[str, list[str]] | None:
        return self._find_disjunction_chain(ast)

    def get_select_star_tables(self, ast: sqlglot.Expression) -> list[str]:
        tables: list[str] = []
        for select in ast.find_all(exp.Select):
            if any(isinstance(expression, exp.Star) for expression in select.expressions):
                from_clause = select.args.get("from")
                if from_clause is None:
                    continue
                for table in from_clause.find_all(exp.Table):
                    tables.append(table.name)
        return tables

    def get_count_star_distinct_subquery(
        self,
        ast: sqlglot.Expression,
    ) -> tuple[str, str] | None:
        if not isinstance(ast, exp.Select):
            return None
        if len(ast.expressions) != 1:
            return None

        count_expr = ast.expressions[0]
        if not isinstance(count_expr, exp.Count) or not isinstance(count_expr.this, exp.Star):
            return None

        from_clause = ast.args.get("from")
        if from_clause is None or not isinstance(from_clause.this, exp.Subquery):
            return None

        inner = from_clause.this.this
        if not isinstance(inner, exp.Select) or not inner.args.get("distinct"):
            return None
        if len(inner.expressions) != 1:
            return None
        inner_expr = inner.expressions[0]
        if not isinstance(inner_expr, exp.Column):
            return None

        inner_from = inner.args.get("from")
        if inner_from is None or not isinstance(inner_from.this, exp.Table):
            return None

        return inner_expr.sql(dialect="clickhouse"), inner_from.this.name

    def get_having_without_agg_predicates(self, ast: sqlglot.Expression) -> list[str]:
        matches: list[str] = []
        for having in ast.find_all(exp.Having):
            for predicate in self._split_conjunction(having.this):
                if not self._contains_aggregate(predicate):
                    matches.append(predicate.sql(dialect="clickhouse"))
        return matches

    def get_orderby_without_limit_subquery(self, ast: sqlglot.Expression) -> exp.Subquery | None:
        for subquery in ast.find_all(exp.Subquery):
            inner = subquery.this
            if not isinstance(inner, exp.Select):
                continue
            if inner.args.get("order") is None or inner.args.get("limit") is not None:
                continue
            return subquery
        return None

    def get_subquery_filter_pushdown(
        self,
        ast: sqlglot.Expression,
    ) -> tuple[str, str, str] | None:
        if not isinstance(ast, exp.Select):
            return None
        outer_where = ast.args.get("where")
        outer_from = ast.args.get("from")
        if outer_where is None or outer_from is None:
            return None
        if not isinstance(outer_from.this, exp.Subquery):
            return None

        inner = outer_from.this.this
        if not isinstance(inner, exp.Select):
            return None
        if inner.args.get("limit") is not None or inner.args.get("distinct"):
            return None
        if inner.args.get("group") is not None or inner.args.get("having") is not None:
            return None
        if inner.args.get("windows") is not None:
            return None
        if any(self._contains_aggregate(expression) for expression in inner.expressions):
            return None
        if any(isinstance(expression, exp.Window) for expression in inner.walk()):
            return None

        inner_where = inner.args.get("where")
        inner_from = inner.args.get("from")
        if inner_where is None or inner_from is None or not isinstance(inner_from.this, exp.Table):
            return None

        table_name = inner_from.this.name
        return (
            table_name,
            inner_where.this.sql(dialect="clickhouse"),
            outer_where.this.sql(dialect="clickhouse"),
        )

    def get_redundant_cast(self, ast: sqlglot.Expression) -> tuple[str, str] | None:
        for cast in ast.find_all(exp.Cast):
            if isinstance(cast.this, exp.Column) and cast.to is not None:
                return cast.this.sql(dialect="clickhouse"), cast.to.sql(dialect="clickhouse")

        cast_prefixes = (
            "touint",
            "toint",
            "tofloat",
            "todecimal",
            "tostring",
        )
        for function in ast.find_all(exp.Anonymous):
            if not function.expressions:
                continue
            if not isinstance(function.expressions[0], exp.Column):
                continue
            if function.name.lower().startswith(cast_prefixes):
                return function.expressions[0].sql(dialect="clickhouse"), function.name
        return None

    def get_in_singleton(self, ast: sqlglot.Expression) -> tuple[str, str] | None:
        for in_expr in ast.find_all(exp.In):
            if isinstance(in_expr.this, exp.Column) and len(in_expr.expressions) == 1:
                return (
                    in_expr.this.sql(dialect="clickhouse"),
                    in_expr.expressions[0].sql(dialect="clickhouse"),
                )
        return None

    def get_constant_predicate(self, ast: sqlglot.Expression) -> str | None:
        for where in ast.find_all(exp.Where):
            for predicate in self._split_conjunction(where.this):
                if isinstance(predicate, exp.Boolean) and predicate.this is True:
                    return predicate.sql(dialect="clickhouse")
                if isinstance(predicate, exp.EQ) and self._is_same_literal_comparison(predicate):
                    return predicate.sql(dialect="clickhouse")
        return None

    def get_length_empty_pattern(
        self,
        ast: sqlglot.Expression,
    ) -> tuple[str, str] | None:
        for node_type in (exp.EQ, exp.GT, exp.NEQ):
            for expression in ast.find_all(node_type):
                left = expression.left
                right = expression.right
                if not isinstance(left, exp.Length):
                    continue
                if not isinstance(right, exp.Literal) or right.this != "0":
                    continue
                if not isinstance(left.this, exp.Column):
                    continue
                return left.this.sql(dialect="clickhouse"), expression.key
        return None

    def get_groupby_string_candidate(self, ast: sqlglot.Expression) -> str | None:
        if not isinstance(ast, exp.Select):
            return None
        group = ast.args.get("group")
        if group is None:
            return None
        likely_string_names = {
            "url",
            "path",
            "name",
            "title",
            "city",
            "country",
            "comment",
            "body",
            "message",
        }
        for expression in group.expressions:
            if isinstance(expression, exp.Column):
                column_name = expression.name.lower()
                if column_name in likely_string_names:
                    return expression.sql(dialect="clickhouse")
        return None

    def get_distinct_after_groupby(self, ast: sqlglot.Expression) -> list[str] | None:
        if not isinstance(ast, exp.Select) or not ast.args.get("distinct"):
            return None
        from_clause = ast.args.get("from")
        if from_clause is None or not isinstance(from_clause.this, exp.Subquery):
            return None
        inner = from_clause.this.this
        if not isinstance(inner, exp.Select) or inner.args.get("group") is None:
            return None
        outer_columns = [expression.sql(dialect="clickhouse") for expression in ast.expressions]
        group_keys = [
            expression.sql(dialect="clickhouse") for expression in inner.args["group"].expressions
        ]
        if outer_columns == group_keys:
            return outer_columns
        return None

    def monthly_range_from_literal(self, function_name: str, literal: str) -> tuple[str, str] | None:
        name = function_name.lower()
        if name == "toyyyymm" and literal.isdigit() and len(literal) == 6:
            start = datetime.strptime(literal, "%Y%m")
            year = start.year + (start.month // 12)
            month = (start.month % 12) + 1
            end = datetime(year, month, 1)
            return self._format_range(start, end)
        if name == "toyyyymmdd" and literal.isdigit() and len(literal) == 8:
            start = datetime.strptime(literal, "%Y%m%d")
            return self._format_range(start, start + timedelta(days=1))
        if name == "tostartofmonth":
            start = datetime.strptime(literal, "%Y-%m-%d")
            year = start.year + (start.month // 12)
            month = (start.month % 12) + 1
            end = datetime(year, month, 1)
            return self._format_range(start, end)
        return None

    def interval_range_from_literal(self, function_name: str, literal: str) -> tuple[str, str] | None:
        name = function_name.lower()
        start = datetime.strptime(literal, "%Y-%m-%d %H:%M:%S")
        if name == "tostartofhour":
            return self._format_range(start, start + timedelta(hours=1))
        if name == "tostartofday":
            return self._format_range(start, start + timedelta(days=1))
        if name == "tostartoffifteenminutes":
            return self._format_range(start, start + timedelta(minutes=15))
        return None

    def _find_todate_equality(self, ast: sqlglot.Expression) -> tuple[str, str] | None:
        for eq in ast.find_all(exp.EQ):
            left = eq.left
            right = eq.right
            if self._is_todate_call(left) and isinstance(right, exp.Literal) and right.is_string:
                return left.expressions[0].sql(dialect="clickhouse"), right.this
            if self._is_todate_call(right) and isinstance(left, exp.Literal) and left.is_string:
                return right.expressions[0].sql(dialect="clickhouse"), left.this
        return None

    def _find_disjunction_chain(self, ast: sqlglot.Expression) -> tuple[str, list[str]] | None:
        for where in ast.find_all(exp.Where):
            flattened = self._flatten_or(where.this)
            if len(flattened) < 3:
                continue

            column_name: str | None = None
            values: list[str] = []
            valid = True

            for predicate in flattened:
                if not isinstance(predicate, exp.EQ):
                    valid = False
                    break

                left = predicate.left
                right = predicate.right
                if isinstance(left, exp.Column) and isinstance(right, exp.Literal):
                    candidate_column = left.sql(dialect="clickhouse")
                    literal = right.sql(dialect="clickhouse")
                elif isinstance(right, exp.Column) and isinstance(left, exp.Literal):
                    candidate_column = right.sql(dialect="clickhouse")
                    literal = left.sql(dialect="clickhouse")
                else:
                    valid = False
                    break

                if column_name is None:
                    column_name = candidate_column
                elif column_name != candidate_column:
                    valid = False
                    break
                values.append(literal)

            if valid and column_name is not None:
                return column_name, values
        return None

    def _flatten_or(self, expression: exp.Expression) -> list[exp.Expression]:
        if isinstance(expression, exp.Or):
            return [*self._flatten_or(expression.left), *self._flatten_or(expression.right)]
        return [expression]

    def _is_todate_call(self, expression: exp.Expression) -> bool:
        return isinstance(expression, exp.Anonymous) and expression.name.lower() == "todate"

    def _is_named_function(self, expression: exp.Expression, names: set[str]) -> bool:
        return (
            isinstance(expression, exp.Anonymous)
            and expression.name.lower() in names
            and len(expression.expressions) == 1
            and isinstance(expression.expressions[0], exp.Column)
        )

    def _match_function_equality(
        self,
        expression: exp.EQ,
        function_names: set[str],
    ) -> tuple[str, str, str] | None:
        left = expression.left
        right = expression.right
        if self._is_named_function(left, function_names) and isinstance(right, exp.Literal):
            return left.name, left.expressions[0].sql(dialect="clickhouse"), right.this
        if self._is_named_function(right, function_names) and isinstance(left, exp.Literal):
            return right.name, right.expressions[0].sql(dialect="clickhouse"), left.this
        return None

    def _having_contains_non_aggregate_predicate(self, expression: exp.Expression | None) -> bool:
        if expression is None:
            return False
        predicates = self._split_conjunction(expression)
        return any(not self._contains_aggregate(predicate) for predicate in predicates)

    def _split_conjunction(self, expression: exp.Expression) -> list[exp.Expression]:
        if isinstance(expression, exp.And):
            return [
                *self._split_conjunction(expression.left),
                *self._split_conjunction(expression.right),
            ]
        return [expression]

    def _contains_aggregate(self, expression: exp.Expression) -> bool:
        aggregates: Iterable[type[exp.Expression]] = (
            exp.Avg,
            exp.Count,
            exp.Max,
            exp.Min,
            exp.ParameterizedAgg,
            exp.Sum,
        )
        return any(expression.find(aggregate) is not None for aggregate in aggregates)

    def _contains_uniq_function(self, expression: exp.Expression) -> bool:
        for function in expression.find_all(exp.Anonymous):
            if function.name.lower().startswith("uniq"):
                return True
        return False

    def _is_same_literal_comparison(self, expression: exp.EQ) -> bool:
        return (
            isinstance(expression.left, exp.Literal)
            and isinstance(expression.right, exp.Literal)
            and expression.left.this == expression.right.this
        )

    def _format_range(self, start: datetime, end: datetime) -> tuple[str, str]:
        return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")

    def _normalize_union_syntax(self, sql: str) -> str:
        return re.sub(r"\bUNION\b(?!\s+(ALL|DISTINCT)\b)", "UNION DISTINCT", sql)

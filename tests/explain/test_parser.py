from __future__ import annotations

from clickadvisor.explain.parser import EstimateResult, ExplainEstimateParser


def test_parse_text_tabular_output() -> None:
    parser = ExplainEstimateParser()
    output = "database\ttable\tparts\trows\tmarks\ndefault\tevents\t3\t1000\t64\n"

    results = parser.parse(output)

    assert results == [
        EstimateResult(database="default", table="events", parts=3, rows=1000, marks=64)
    ]


def test_parse_text_pretty_output() -> None:
    parser = ExplainEstimateParser()
    output = """
┌─database─┬─table──┬─parts─┬─rows─┬─marks─┐
│ default  │ events │ 3     │ 1000 │ 64    │
└──────────┴────────┴───────┴──────┴───────┘
"""

    results = parser.parse(output)

    assert results == [
        EstimateResult(database="default", table="events", parts=3, rows=1000, marks=64)
    ]


def test_parse_json_output() -> None:
    parser = ExplainEstimateParser()
    output = """
{
  "meta": [],
  "data": [
    {"database": "default", "table": "events", "parts": 2, "rows": 500, "marks": 32}
  ]
}
"""

    results = parser.parse(output)

    assert results == [
        EstimateResult(database="default", table="events", parts=2, rows=500, marks=32)
    ]


def test_parse_empty_output_returns_empty_list() -> None:
    assert ExplainEstimateParser().parse("") == []


def test_aggregate_multiple_results() -> None:
    parser = ExplainEstimateParser()
    results = [
        EstimateResult(database="default", table="events", parts=2, rows=100, marks=10),
        EstimateResult(database="default", table="users", parts=3, rows=200, marks=20),
    ]

    aggregate = parser.aggregate(results)

    assert aggregate == EstimateResult(
        database="default",
        table="multiple",
        parts=5,
        rows=300,
        marks=30,
    )

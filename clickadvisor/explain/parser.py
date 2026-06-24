from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class EstimateResult:
    database: str = ""
    table: str = ""
    parts: int = 0
    rows: int = 0
    marks: int = 0

    def is_empty(self) -> bool:
        return self.rows == 0 and self.marks == 0


class ExplainEstimateParser:
    def parse(self, explain_output: str) -> list[EstimateResult]:
        """Парсит вывод EXPLAIN ESTIMATE, возвращает список результатов."""
        explain_output = explain_output.strip()
        if not explain_output:
            return []

        if explain_output.startswith("{") or explain_output.startswith("["):
            return self._parse_json(explain_output)

        return self._parse_text(explain_output)

    def _parse_json(self, text: str) -> list[EstimateResult]:
        try:
            data = json.loads(text)
            if isinstance(data, dict) and "data" in data:
                rows = data["data"]
            elif isinstance(data, list):
                rows = data
            else:
                rows = [data]

            results = []
            for row in rows:
                if not isinstance(row, dict):
                    continue
                results.append(_row_to_estimate(row))
            return results
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return []

    def _parse_text(self, text: str) -> list[EstimateResult]:
        results = []

        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("-") or line.startswith("┌"):
                continue
            if line.startswith("└") or line.startswith("├") or line.startswith("╞"):
                continue
            if "database" in line.lower() and "table" in line.lower():
                continue

            parts_line = re.split(r"\t|│", line)
            parts_line = [part.strip() for part in parts_line if part.strip()]

            if len(parts_line) >= 5:
                try:
                    results.append(
                        EstimateResult(
                            database=parts_line[0],
                            table=parts_line[1],
                            parts=int(parts_line[2]),
                            rows=int(parts_line[3]),
                            marks=int(parts_line[4]),
                        )
                    )
                except (ValueError, IndexError):
                    continue

        return results

    def aggregate(self, results: list[EstimateResult]) -> EstimateResult:
        """Суммирует результаты по всем таблицам."""
        if not results:
            return EstimateResult()
        return EstimateResult(
            database=results[0].database,
            table=results[0].table if len(results) == 1 else "multiple",
            parts=sum(result.parts for result in results),
            rows=sum(result.rows for result in results),
            marks=sum(result.marks for result in results),
        )


def _row_to_estimate(row: dict[str, Any]) -> EstimateResult:
    return EstimateResult(
        database=str(row.get("database", "")),
        table=str(row.get("table", "")),
        parts=int(row.get("parts", 0)),
        rows=int(row.get("rows", 0)),
        marks=int(row.get("marks", 0)),
    )

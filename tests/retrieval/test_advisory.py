from __future__ import annotations

from clickadvisor.core.models import QueryContext
from clickadvisor.retrieval.advisory import RetrievalAdvisor


class EmptyRetriever:
    def build_query_from_context(self, sql: str, findings: list[object]) -> str:
        return "query"

    def retrieve(
        self,
        query: str,
        top_k: int,
        ch_version: str | None,
        score_threshold: float,
    ) -> list[object]:
        return []


def test_generate_advisory_returns_empty_for_empty_kb() -> None:
    advisor = RetrievalAdvisor.__new__(RetrievalAdvisor)
    advisor.retriever = EmptyRetriever()

    findings = advisor.generate_advisory(
        QueryContext(sql="SELECT count() FROM events"),
        existing_findings=[],
    )

    assert findings == []

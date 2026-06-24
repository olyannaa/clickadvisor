from __future__ import annotations

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.retrieval.retriever import KBRetriever


class RetrievalAdvisor:
    def __init__(self, db_path: str = ".qdrant_db") -> None:
        self.retriever = KBRetriever(db_path=db_path)

    def generate_advisory(
        self,
        context: QueryContext,
        existing_findings: list[Finding],
    ) -> list[Finding]:
        query = self.retriever.build_query_from_context(context.sql, existing_findings)
        chunks = self.retriever.retrieve(
            query=query,
            top_k=3,
            ch_version=context.ch_version,
            score_threshold=0.65,
        )

        findings = []
        for index, chunk in enumerate(chunks):
            suggestion = chunk.text[:500]
            if chunk.url:
                suggestion += f"\n\nИсточник: {chunk.url}"

            findings.append(
                Finding(
                    rule_id=f"RAG-{index + 1:03d}",
                    rule_name="retrieval_advisory",
                    tier="rag",
                    severity="low",
                    description=f"Релевантный контекст из документации (score: {chunk.score:.2f})",
                    suggestion=suggestion,
                    confidence="retrieved",
                    ch_version_introduced=chunk.ch_version or "unknown",
                )
            )

        return findings

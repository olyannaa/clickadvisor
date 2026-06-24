from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from clickadvisor.core.models import Finding
from clickadvisor.retrieval import retriever
from clickadvisor.retrieval.retriever import KBRetriever


class FakeEmbedder:
    def embed_query(self, query: str) -> np.ndarray:
        return np.ones(384, dtype=np.float32)


class FakeQdrantClient:
    scores = [0.77]

    def __init__(self, path: str) -> None:
        self.path = path

    def get_collections(self) -> SimpleNamespace:
        return SimpleNamespace(
            collections=[SimpleNamespace(name=retriever.COLLECTION_NAME)],
        )

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int,
        score_threshold: float,
        query_filter: object | None,
    ) -> list[SimpleNamespace]:
        assert collection_name == retriever.COLLECTION_NAME
        assert len(query_vector) == 384
        assert score_threshold == 0.65
        assert query_filter is None
        return [
            SimpleNamespace(
                payload={
                    "text": "Use approximate uniq functions for large distinct counts.",
                    "source": "docs",
                    "url": "https://clickhouse.com/docs/",
                    "ch_version": "22.8",
                },
                score=score,
            )
            for score in self.scores[:limit]
        ]


def test_retrieve_maps_qdrant_results(monkeypatch) -> None:
    monkeypatch.setattr("clickadvisor.retrieval.retriever.QdrantClient", FakeQdrantClient)
    monkeypatch.setattr("clickadvisor.retrieval.retriever.Embedder", FakeEmbedder)

    chunks = KBRetriever(db_path="fake").retrieve("count distinct", top_k=1)

    assert len(chunks) == 1
    assert chunks[0].score == 0.77
    assert chunks[0].url == "https://clickhouse.com/docs/"


def test_retrieve_returns_only_first_when_top_scores_are_identical(monkeypatch, caplog) -> None:
    FakeQdrantClient.scores = [0.89, 0.89, 0.89]
    monkeypatch.setattr("clickadvisor.retrieval.retriever.QdrantClient", FakeQdrantClient)
    monkeypatch.setattr("clickadvisor.retrieval.retriever.Embedder", FakeEmbedder)

    chunks = KBRetriever(db_path="fake").retrieve("count distinct", top_k=3)

    assert len(chunks) == 1
    assert "nearly identical" in caplog.text
    FakeQdrantClient.scores = [0.77]


def test_build_query_from_context_uses_rule_semantics_not_raw_sql(monkeypatch) -> None:
    monkeypatch.setattr("clickadvisor.retrieval.retriever.QdrantClient", FakeQdrantClient)
    retriever_instance = KBRetriever(db_path="fake")
    findings = [
        Finding(
            rule_id="R-005",
            rule_name="toDate equality",
            tier="tier1",
            severity="high",
            description="date function on column",
            suggestion="Use range predicate",
        ),
        Finding(
            rule_id="R-001",
            rule_name="count distinct",
            tier="tier1",
            severity="medium",
            description="count distinct",
            suggestion="Use uniqExact",
        ),
    ]

    query = retriever_instance.build_query_from_context(
        "SELECT secret_raw_column FROM table WHERE toDate(ts) = today()",
        findings,
    )

    assert query == retriever.RULE_QUERIES["R-005"]
    assert "secret_raw_column" not in query


def test_build_query_from_context_falls_back_without_rule_findings(monkeypatch) -> None:
    monkeypatch.setattr("clickadvisor.retrieval.retriever.QdrantClient", FakeQdrantClient)
    retriever_instance = KBRetriever(db_path="fake")

    query = retriever_instance.build_query_from_context("SELECT * FROM t", [])

    assert query == "ClickHouse query optimization performance"

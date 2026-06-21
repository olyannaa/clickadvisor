from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from clickadvisor.retrieval import retriever
from clickadvisor.retrieval.retriever import KBRetriever


class FakeEmbedder:
    def embed_query(self, query: str) -> np.ndarray:
        return np.ones(384, dtype=np.float32)


class FakeQdrantClient:
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
        assert limit == 1
        assert score_threshold == 0.5
        assert query_filter is None
        return [
            SimpleNamespace(
                payload={
                    "text": "Use approximate uniq functions for large distinct counts.",
                    "source": "docs",
                    "url": "https://clickhouse.com/docs/",
                    "ch_version": "22.8",
                },
                score=0.77,
            )
        ]


def test_retrieve_maps_qdrant_results(monkeypatch) -> None:
    monkeypatch.setattr("clickadvisor.retrieval.retriever.QdrantClient", FakeQdrantClient)
    monkeypatch.setattr("clickadvisor.retrieval.retriever.Embedder", FakeEmbedder)

    chunks = KBRetriever(db_path="fake").retrieve("count distinct", top_k=1)

    assert len(chunks) == 1
    assert chunks[0].score == 0.77
    assert chunks[0].url == "https://clickhouse.com/docs/"

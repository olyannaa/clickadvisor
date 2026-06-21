from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol, cast

from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from clickadvisor.retrieval.embedder import Embedder

COLLECTION_NAME = "clickadvisor_kb"


@dataclass(slots=True)
class RetrievedChunk:
    text: str
    source: str
    url: str
    score: float
    ch_version: str


class SearchResult(Protocol):
    payload: dict[str, Any] | None
    score: float


class KBRetriever:
    def __init__(self, db_path: str = ".qdrant_db") -> None:
        self.client = QdrantClient(path=db_path)
        self.embedder = Embedder()

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        ch_version: str | None = None,
        score_threshold: float = 0.5,
    ) -> list[RetrievedChunk]:
        if not self._collection_exists():
            return []

        query_vector = self.embedder.embed_query(query)
        query_filter = None
        if ch_version:
            query_filter = None

        results = self._search(
            query_vector=query_vector.tolist(),
            top_k=top_k,
            score_threshold=score_threshold,
            query_filter=query_filter,
        )

        chunks = []
        for result in results:
            payload = result.payload or {}
            chunks.append(
                RetrievedChunk(
                    text=str(payload.get("text", "")),
                    source=str(payload.get("source", "")),
                    url=str(payload.get("url", "")),
                    score=float(result.score),
                    ch_version=str(payload.get("ch_version", "")),
                )
            )
        return chunks

    def build_query_from_context(self, sql: str, findings: Sequence[object]) -> str:
        found_types = [
            str(getattr(finding, "description", ""))[:100]
            for finding in findings
            if getattr(finding, "description", "")
        ]
        sql_preview = sql[:200].replace("\n", " ")

        query_parts = [f"ClickHouse query optimization: {sql_preview}"]
        if found_types:
            query_parts.append("Issues found: " + "; ".join(found_types[:3]))

        return " ".join(query_parts)

    def _collection_exists(self) -> bool:
        collections = self.client.get_collections().collections
        return any(collection.name == COLLECTION_NAME for collection in collections)

    def _search(
        self,
        query_vector: list[float],
        top_k: int,
        score_threshold: float,
        query_filter: Filter | None,
    ) -> list[SearchResult]:
        if hasattr(self.client, "search"):
            return cast(
                list[SearchResult],
                self.client.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=top_k,
                    score_threshold=score_threshold,
                    query_filter=query_filter,
                ),
            )

        response = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=query_filter,
        )
        return cast(list[SearchResult], list(response.points))

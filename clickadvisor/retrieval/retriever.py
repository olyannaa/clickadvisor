from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol, cast

from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from clickadvisor.retrieval.embedder import Embedder

COLLECTION_NAME = "clickadvisor_kb"
logger = logging.getLogger(__name__)

RULE_QUERIES = {
    "R-001": "ClickHouse COUNT DISTINCT optimization uniqExact aggregation performance",
    "R-002": "ClickHouse uniq HyperLogLog approximate distinct count",
    "R-003": "ClickHouse quantileExact quantileTDigest approximate quantile",
    "R-004": "ClickHouse COUNT DISTINCT subquery collapse optimization",
    "R-005": "ClickHouse toDate datetime range predicate sargable primary key index",
    "R-006": "ClickHouse toYYYYMM date range filter index pruning",
    "R-007": "ClickHouse toStartOfHour toStartOfDay range predicate optimization",
    "R-008": "ClickHouse CAST redundant type conversion primary key",
    "R-009": "ClickHouse IN singleton equality optimization",
    "R-010": "ClickHouse OR disjunction IN clause optimization",
    "R-011": "ClickHouse HAVING WHERE predicate pushdown aggregation",
    "R-012": "ClickHouse constant predicate elimination WHERE TRUE",
    "R-013": "ClickHouse length empty string function optimization",
    "R-014": "ClickHouse GROUP BY string cityHash64 hash optimization",
    "R-015": "ClickHouse DISTINCT after GROUP BY redundant",
    "R-016": "ClickHouse ORDER BY subquery without LIMIT remove",
    "R-017": "ClickHouse subquery filter pushdown WHERE",
    "R-018": "ClickHouse UNION UNION ALL distinct performance",
    "D-003": "ClickHouse SELECT star columnar storage IO all columns",
    "D-004": "ClickHouse SELECT without LIMIT unbounded result",
    "D-007": "ClickHouse FINAL modifier performance MergeTree",
}


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
        score_threshold: float = 0.65,
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
        results = self._apply_score_diversity_guard(results)

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
        rule_queries = []
        for finding in findings:
            rule_id = str(getattr(finding, "rule_id", ""))
            tier = str(getattr(finding, "tier", ""))
            if rule_id in RULE_QUERIES and tier != "rag":
                rule_queries.append(RULE_QUERIES[rule_id])

        if rule_queries:
            high_findings = [
                finding
                for finding in findings
                if getattr(finding, "severity", "") == "high"
                and str(getattr(finding, "rule_id", "")) in RULE_QUERIES
                and str(getattr(finding, "tier", "")) != "rag"
            ]
            primary_queries = [
                RULE_QUERIES[str(getattr(finding, "rule_id", ""))]
                for finding in high_findings[:2]
            ]
            return " | ".join(primary_queries) if primary_queries else rule_queries[0]

        return "ClickHouse query optimization performance"

    def _apply_score_diversity_guard(self, results: list[SearchResult]) -> list[SearchResult]:
        if len(results) < 3:
            return results

        top_scores = [float(result.score) for result in results[:3]]
        if max(top_scores) - min(top_scores) < 0.001:
            logger.warning(
                "Retrieval top-3 scores are nearly identical (%s); returning only first result",
                ", ".join(f"{score:.4f}" for score in top_scores),
            )
            return results[:1]
        return results

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

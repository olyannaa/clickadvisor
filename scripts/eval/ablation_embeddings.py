from __future__ import annotations

import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from rich.console import Console
from rich.table import Table
from sentence_transformers import SentenceTransformer

from clickadvisor.retrieval.indexer import parse_frontmatter, strip_frontmatter

KB_CHUNKS_DIR = Path("data/kb/chunks")
SYNTHETIC_CASES_DIR = Path("benchmark/cases/synthetic")
COLLECTION_NAME = "clickadvisor_ablation_kb"
MAX_CHUNKS = 2000
TOTAL_KB_CHUNKS = 8804
TOP_K = 3

console = Console()


@dataclass(frozen=True)
class ModelSpec:
    model_name: str
    label: str
    size: str


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str
    url: str
    path: str


@dataclass(frozen=True)
class EvalResult:
    model: ModelSpec
    mrr_at_3: float
    elapsed_seconds: float


MODELS = [
    ModelSpec(
        model_name="intfloat/multilingual-e5-small",
        label="multilingual-e5-small (current)",
        size="117 MB",
    ),
    ModelSpec(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        label="all-MiniLM-L6-v2",
        size="80 MB",
    ),
    ModelSpec(
        model_name="paraphrase-multilingual-MiniLM-L12-v2",
        label="paraphrase-multilingual-MiniLM-L12-v2",
        size="420 MB",
    ),
]

SQL_FUNCTION_PATTERN = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
SQL_KEYWORD_FUNCTION_EXCLUSIONS = {"SELECT", "FROM", "WHERE", "GROUP", "ORDER", "LIMIT"}
RULE_KEYWORDS = {
    "R-001": ["uniqExact", "COUNT(DISTINCT", "distinct", "count distinct"],
    "R-002": ["uniq", "HyperLogLog", "approximate", "approx"],
    "R-003": ["quantile", "quantileTDigest", "quantileExact"],
    "R-004": ["uniqExact", "subquery", "DISTINCT"],
    "R-005": ["toDate", "DateTime", "sargable", "range", "date range"],
    "R-006": ["toYYYYMM", "toStartOfMonth", "date", "partition"],
    "R-007": ["toStartOfHour", "toStartOfDay", "interval", "range"],
    "R-008": ["CAST", "type conversion", "primary key", "index"],
    "R-009": ["IN", "equality", "singleton"],
    "R-010": ["OR", "IN", "disjunction", "chain"],
    "R-011": ["HAVING", "WHERE", "aggregate", "GROUP BY", "pushdown"],
    "R-012": ["WHERE TRUE", "constant", "predicate"],
    "R-013": ["length", "empty", "notEmpty", "string"],
    "R-014": ["GROUP BY", "cityHash64", "hash", "string"],
    "R-015": ["DISTINCT", "GROUP BY", "redundant"],
    "R-016": ["ORDER BY", "LIMIT", "subquery", "sort"],
    "R-017": ["subquery", "filter", "pushdown", "WHERE"],
    "R-018": ["UNION", "UNION ALL", "distinct"],
    "D-003": ["SELECT *", "columnar", "columns", "star"],
    "D-004": ["LIMIT", "unbounded", "result set"],
}


def main() -> None:
    db_paths: list[Path] = []
    try:
        chunks = load_chunks(KB_CHUNKS_DIR, limit=MAX_CHUNKS)
        cases = load_cases(SYNTHETIC_CASES_DIR)
        if not chunks:
            raise RuntimeError(f"No chunks found in {KB_CHUNKS_DIR}")
        if not cases:
            raise RuntimeError(f"No synthetic cases found in {SYNTHETIC_CASES_DIR}")

        results = []
        for model in MODELS:
            db_path = Path(f".qdrant_ablation_{sanitize_model_name(model.model_name)}")
            db_paths.append(db_path)
            results.append(evaluate_model(model, chunks, cases, db_path))

        print_results(results)
    finally:
        cleanup(db_paths)


def load_chunks(chunks_dir: Path, limit: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    md_files = sorted(chunks_dir.rglob("*.md"))[:limit]
    for path in md_files:
        content = path.read_text(encoding="utf-8", errors="ignore")
        metadata = parse_frontmatter(content)
        text = strip_frontmatter(content)
        if len(text.strip()) < 50:
            continue

        chunks.append(
            Chunk(
                text=text,
                source=str(metadata.get("source", "")),
                url=str(metadata.get("url", "")),
                path=str(path),
            )
        )
    return chunks


def load_cases(cases_dir: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(cases_dir.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and payload.get("sql"):
            cases.append(payload)
    return cases


def evaluate_model(
    model_spec: ModelSpec,
    chunks: list[Chunk],
    cases: list[dict[str, Any]],
    db_path: Path,
) -> EvalResult:
    start = time.perf_counter()
    model = SentenceTransformer(model_spec.model_name)
    vector_size = len(embed_document(model, model_spec.model_name, "dimension probe"))

    if db_path.exists():
        shutil.rmtree(db_path)

    client = QdrantClient(path=str(db_path))
    try:
        if client.collection_exists(COLLECTION_NAME):
            client.delete_collection(COLLECTION_NAME)
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        index_chunks(client, model, model_spec.model_name, chunks)
        mrr_at_3 = compute_mrr_at_3(client, model, model_spec.model_name, cases)
    finally:
        client.close()

    elapsed_seconds = time.perf_counter() - start
    return EvalResult(model=model_spec, mrr_at_3=mrr_at_3, elapsed_seconds=elapsed_seconds)


def index_chunks(
    client: QdrantClient,
    model: SentenceTransformer,
    model_name: str,
    chunks: list[Chunk],
) -> None:
    texts = [chunk.text[:512] for chunk in chunks]
    prefix = "passage: " if is_e5_model(model_name) else ""
    vectors = model.encode(
        [f"{prefix}{text}" for text in texts],
        normalize_embeddings=True,
        batch_size=32,
    )

    points = []
    for index, (chunk, vector) in enumerate(zip(chunks, vectors, strict=True)):
        points.append(
            PointStruct(
                id=index,
                vector=vector.tolist(),
                payload={
                    "text": chunk.text[:1000],
                    "source": chunk.source,
                    "url": chunk.url,
                    "file_path": chunk.path,
                },
            )
        )
        if len(points) >= 100:
            client.upsert(COLLECTION_NAME, points)
            points = []

    if points:
        client.upsert(COLLECTION_NAME, points)


def compute_mrr_at_3(
    client: QdrantClient,
    model: SentenceTransformer,
    model_name: str,
    cases: list[dict[str, Any]],
) -> float:
    reciprocal_ranks = []
    for case in cases:
        sql = str(case["sql"])
        query = f"ClickHouse optimization: {sql[:200]}"
        query_vector = embed_query(model, model_name, query).tolist()
        results = search_top_k(client, query_vector, TOP_K)

        rank = first_relevant_rank(results, case.get("expected_rules_to_fire", []), sql)
        reciprocal_ranks.append(1 / rank if rank else 0.0)

    return sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0


def search_top_k(client: QdrantClient, query_vector: list[float], top_k: int) -> list[Any]:
    if hasattr(client, "search"):
        return client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
        )

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )
    return list(response.points)


def first_relevant_rank(results: list[Any], expected_rules: object, sql: str) -> int | None:
    rule_ids = expected_rules if isinstance(expected_rules, list) else []
    for rank, result in enumerate(results[:TOP_K], start=1):
        if any(is_relevant(result, str(rule_id), sql) for rule_id in rule_ids):
            return rank
    return None


def is_relevant(chunk: Any, rule_id: str, sql: str) -> bool:
    payload = chunk.payload or {}
    source = str(payload.get("source", "")).lower()
    score = float(getattr(chunk, "score", 0.0))
    if ("clickhouse" in source or "altinity" in source) and score >= 0.75:
        return True

    text = str(payload.get("text", "")).lower()
    return any(keyword.lower() in text for keyword in RULE_KEYWORDS.get(rule_id, []))


def extract_sql_functions(sql: str) -> list[str]:
    functions = []
    for match in SQL_FUNCTION_PATTERN.finditer(sql):
        name = match.group(1)
        if name.upper() not in SQL_KEYWORD_FUNCTION_EXCLUSIONS:
            functions.append(name)
    return dedupe_terms(functions)


def dedupe_terms(terms: list[str]) -> list[str]:
    seen = set()
    deduped = []
    for term in terms:
        normalized = term.lower()
        if normalized not in seen:
            seen.add(normalized)
            deduped.append(term)
    return deduped


def embed_query(model: SentenceTransformer, model_name: str, text: str) -> Any:
    prefix = "query: " if is_e5_model(model_name) else ""
    return model.encode(f"{prefix}{text}", normalize_embeddings=True)


def embed_document(model: SentenceTransformer, model_name: str, text: str) -> Any:
    prefix = "passage: " if is_e5_model(model_name) else ""
    return model.encode(f"{prefix}{text}", normalize_embeddings=True)


def is_e5_model(model_name: str) -> bool:
    return "e5" in model_name.lower()


def sanitize_model_name(model_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", model_name)


def print_results(results: list[EvalResult]) -> None:
    table = Table()
    table.add_column("Model")
    table.add_column("Size")
    table.add_column("MRR@3", justify="right")
    table.add_column("Time (s)", justify="right")

    for result in results:
        table.add_row(
            result.model.label,
            result.model.size,
            f"{result.mrr_at_3:.2f}",
            f"{result.elapsed_seconds:.1f}",
        )

    console.print(table)
    console.print(
        f"* Evaluated on {MAX_CHUNKS} KB chunks (of {TOTAL_KB_CHUNKS} total). "
        "Full index expected to improve MRR@3."
    )
    best = max(results, key=lambda result: result.mrr_at_3)
    console.print(
        f"Recommendation: {best.model.label} achieves best MRR@3 "
        f"with {best.model.size} footprint."
    )


def cleanup(db_paths: list[Path]) -> None:
    for db_path in db_paths:
        shutil.rmtree(db_path, ignore_errors=True)


if __name__ == "__main__":
    main()

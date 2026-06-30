from __future__ import annotations

import json
import re
import shutil
import time
from dataclasses import dataclass
from datetime import UTC, datetime
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
RESULTS_DIR = Path("eval/results")

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
    query_count: int
    elapsed_seconds: float


@dataclass(frozen=True)
class RuleGoldReference:
    rule_id: str
    url_fragments: tuple[str, ...]
    keywords: tuple[str, ...]


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
RULE_GOLD_REFERENCES = {
    "R-001": RuleGoldReference(
        "R-001",
        ("uniqexact", "count-distinct", "aggregate-functions/reference/uniq"),
        ("uniqExact", "COUNT(DISTINCT"),
    ),
    "R-002": RuleGoldReference(
        "R-002",
        ("uniq", "aggregate-functions/reference/uniq"),
        ("uniq", "approximate"),
    ),
    "R-003": RuleGoldReference(
        "R-003",
        ("quantile", "quantiletdigest"),
        ("quantileExact", "quantileTDigest"),
    ),
    "R-004": RuleGoldReference(
        "R-004",
        ("distinct", "uniqexact"),
        ("SELECT DISTINCT", "uniqExact"),
    ),
    "R-005": RuleGoldReference(
        "R-005",
        ("todate", "datetime", "primary-key"),
        ("toDate", "range"),
    ),
    "R-006": RuleGoldReference(
        "R-006",
        ("toyyyymm", "partition", "date-time-functions"),
        ("toYYYYMM", "partition"),
    ),
    "R-007": RuleGoldReference(
        "R-007",
        ("tostartof", "date-time-functions"),
        ("toStartOf", "range"),
    ),
    "R-008": RuleGoldReference(
        "R-008",
        ("cast", "type-conversion-functions"),
        ("CAST", "type conversion"),
    ),
    "R-009": RuleGoldReference("R-009", ("in", "operators"), ("IN", "single value")),
    "R-010": RuleGoldReference("R-010", ("in", "operators"), ("OR", "IN")),
    "R-011": RuleGoldReference("R-011", ("having", "where"), ("HAVING", "WHERE")),
    "R-012": RuleGoldReference("R-012", ("where", "operators"), ("constant", "predicate")),
    "R-013": RuleGoldReference(
        "R-013",
        ("empty", "notempty", "string-functions"),
        ("empty", "notEmpty"),
    ),
    "R-014": RuleGoldReference(
        "R-014",
        ("group-by", "cityhash64", "hash-functions"),
        ("GROUP BY", "hash"),
    ),
    "R-015": RuleGoldReference("R-015", ("distinct", "group-by"), ("DISTINCT", "GROUP BY")),
    "R-016": RuleGoldReference("R-016", ("order-by", "limit"), ("ORDER BY", "LIMIT")),
    "R-017": RuleGoldReference("R-017", ("where", "subquery"), ("subquery", "filter")),
    "R-018": RuleGoldReference("R-018", ("union", "union-all"), ("UNION ALL", "UNION")),
    "R-019": RuleGoldReference("R-019", ("uint", "data-types", "integer"), ("UInt64", "Int64")),
    "R-020": RuleGoldReference(
        "R-020",
        ("cast", "ordefault", "type-conversion-functions"),
        ("OrDefault", "CAST"),
    ),
    "D-003": RuleGoldReference("D-003", ("select", "columnar"), ("SELECT *", "columns")),
    "D-004": RuleGoldReference("D-004", ("limit", "result"), ("LIMIT", "unbounded")),
    "D-007": RuleGoldReference("D-007", ("final", "replacingmergetree"), ("FINAL", "MergeTree")),
    "D-014": RuleGoldReference(
        "D-014",
        ("async-insert", "wait_for_async_insert"),
        ("async_insert", "wait_for_async_insert"),
    ),
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
        output_dir = write_results(results)
        console.print(f"Saved retrieval ablation results to {output_dir}")
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
        mrr_at_3, query_count = compute_mrr_at_3(client, model, model_spec.model_name, cases)
    finally:
        client.close()

    elapsed_seconds = time.perf_counter() - start
    return EvalResult(
        model=model_spec,
        mrr_at_3=mrr_at_3,
        query_count=query_count,
        elapsed_seconds=elapsed_seconds,
    )


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
) -> tuple[float, int]:
    reciprocal_ranks = []
    for case in cases:
        gold_refs = gold_references_for_case(case)
        if not gold_refs:
            continue
        sql = str(case["sql"])
        query = f"ClickHouse optimization: {sql[:200]}"
        query_vector = embed_query(model, model_name, query).tolist()
        results = search_top_k(client, query_vector, TOP_K)

        rank = first_relevant_rank(results, gold_refs)
        reciprocal_ranks.append(1 / rank if rank else 0.0)

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
    return mrr, len(reciprocal_ranks)


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


def first_relevant_rank(results: list[Any], gold_refs: list[RuleGoldReference]) -> int | None:
    for rank, result in enumerate(results[:TOP_K], start=1):
        if any(is_relevant(result, gold_ref) for gold_ref in gold_refs):
            return rank
    return None


def gold_references_for_case(case: dict[str, Any]) -> list[RuleGoldReference]:
    expected_rules = case.get("expected_rules_to_fire", [])
    if not isinstance(expected_rules, list):
        return []
    return [
        RULE_GOLD_REFERENCES[rule_id]
        for rule_id in expected_rules
        if isinstance(rule_id, str) and rule_id in RULE_GOLD_REFERENCES
    ]


def is_relevant(chunk: Any, gold_ref: RuleGoldReference) -> bool:
    payload = chunk.payload or {}
    url = str(payload.get("url", "")).lower()
    path = str(payload.get("file_path", "")).lower()
    text = str(payload.get("text", "")).lower()

    if any(
        fragment.lower() in url or fragment.lower() in path
        for fragment in gold_ref.url_fragments
    ):
        return True

    return any(keyword.lower() in text for keyword in gold_ref.keywords)


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
    table.add_column("Queries", justify="right")
    table.add_column("MRR@3", justify="right")
    table.add_column("Time (s)", justify="right")

    for result in results:
        table.add_row(
            result.model.label,
            result.model.size,
            str(result.query_count),
            f"{result.mrr_at_3:.2f}",
            f"{result.elapsed_seconds:.1f}",
        )

    console.print(table)
    console.print(
        f"* Evaluated on {MAX_CHUNKS} KB chunks (of {TOTAL_KB_CHUNKS} total). "
        "MRR@3 uses explicit rule-to-doc gold URL/keyword references only."
    )
    best = max(results, key=lambda result: result.mrr_at_3)
    console.print(
        f"Recommendation: {best.model.label} achieves best MRR@3 "
        f"with {best.model.size} footprint."
    )


def write_results(results: list[EvalResult]) -> Path:
    output_dir = RESULTS_DIR / f"retrieval_ablation_{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "model": result.model.label,
            "model_name": result.model.model_name,
            "size": result.model.size,
            "query_count": result.query_count,
            "mrr_at_3": result.mrr_at_3,
            "elapsed_seconds": result.elapsed_seconds,
            "max_chunks": MAX_CHUNKS,
            "total_kb_chunks": TOTAL_KB_CHUNKS,
        }
        for result in results
    ]
    (output_dir / "metrics.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "metadata.json").write_text(
        json.dumps(
            {
                "experiment": "retrieval_ablation",
                "cases_dir": str(SYNTHETIC_CASES_DIR),
                "kb_chunks_dir": str(KB_CHUNKS_DIR),
                "top_k": TOP_K,
                "scoring": "explicit rule gold URL fragments or keywords",
                "created_at": datetime.now(UTC).isoformat(),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (output_dir / "summary.md").write_text(markdown_summary(results), encoding="utf-8")
    return output_dir


def markdown_summary(results: list[EvalResult]) -> str:
    lines = [
        "# Retrieval Ablation",
        "",
        "| Model | Size | Queries | MRR@3 | Time (s) |",
        "|---|---:|---:|---:|---:|",
    ]
    for result in results:
        lines.append(
            "| "
            f"{result.model.label} | "
            f"{result.model.size} | "
            f"{result.query_count} | "
            f"{result.mrr_at_3:.3f} | "
            f"{result.elapsed_seconds:.1f} |"
        )
    lines.append("")
    return "\n".join(lines)


def cleanup(db_paths: list[Path]) -> None:
    for db_path in db_paths:
        shutil.rmtree(db_path, ignore_errors=True)


if __name__ == "__main__":
    main()

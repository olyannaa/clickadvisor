from __future__ import annotations

import re
from pathlib import Path
from typing import Any, cast

import yaml
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from clickadvisor.retrieval.embedder import Embedder

COLLECTION_NAME = "clickadvisor_kb"
VECTOR_SIZE = 384
CH_VERSION_PATTERN = re.compile(r"^\d{1,2}\.\d{1,2}$")


class KBIndexer:
    def __init__(
        self,
        db_path: str = ".qdrant_db",
        embedding_model: str = Embedder.DEFAULT_MODEL,
    ) -> None:
        self.client = QdrantClient(path=db_path)
        self.embedder = Embedder(model_key=embedding_model)

    def is_indexed(self) -> bool:
        collections = self.client.get_collections().collections
        return any(collection.name == COLLECTION_NAME for collection in collections)

    def index_kb(self, chunks_dir: str = "data/kb/chunks") -> int:
        self.client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )

        chunks_path = Path(chunks_dir)
        md_files = sorted(chunks_path.rglob("*.md"))

        indexed_count = 0
        points: list[PointStruct] = []
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            metadata = parse_frontmatter(content)
            text_body = strip_frontmatter(content)

            if len(text_body.strip()) < 50:
                continue

            vector = self.embedder.embed_document(text_body[:512])
            point = PointStruct(
                id=indexed_count,
                vector=vector.tolist(),
                payload={
                    "text": text_body[:1000],
                    "source": metadata.get("source", "unknown"),
                    "url": metadata.get("url", ""),
                    "ch_version": validate_ch_version(
                        str(metadata.get("ch_version_introduced", ""))
                    ),
                    "topic": metadata.get("topic", ""),
                    "file_path": str(md_file),
                },
            )
            points.append(point)
            indexed_count += 1

            if len(points) >= 100:
                self.client.upsert(COLLECTION_NAME, points)
                points = []

        if points:
            self.client.upsert(COLLECTION_NAME, points)

        return indexed_count

    def reindex(self, chunks_dir: str = "data/kb/chunks") -> int:
        """Удаляет старый индекс и создаёт новый."""
        try:
            self.client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        return self.index_kb(chunks_dir)

    def get_stats(self) -> dict[str, int | None]:
        info = self.client.get_collection(COLLECTION_NAME)
        vectors_count = getattr(info, "vectors_count", None)
        if vectors_count is None:
            vectors_count = getattr(info, "points_count", None)
        return {"vectors_count": cast(int | None, vectors_count)}


def parse_frontmatter(content: str) -> dict[str, Any]:
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1])
            except yaml.YAMLError:
                return {}
            if isinstance(metadata, dict):
                parsed = cast(dict[str, Any], metadata)
                if "ch_version_introduced" in parsed:
                    parsed["ch_version_introduced"] = validate_ch_version(
                        str(parsed["ch_version_introduced"])
                    )
                return parsed
    return {}


def strip_frontmatter(content: str) -> str:
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


def validate_ch_version(v: str) -> str:
    if v and CH_VERSION_PATTERN.match(str(v)):
        return str(v)
    return ""

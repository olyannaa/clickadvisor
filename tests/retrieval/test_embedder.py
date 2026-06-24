from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest

from clickadvisor.retrieval import embedder
from clickadvisor.retrieval.embedder import Embedder


class FakeSentenceTransformer:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.calls: list[tuple[str, bool]] = []

    def encode(
        self,
        text: str,
        normalize_embeddings: bool,
        batch_size: int | None = None,
    ) -> np.ndarray:
        self.calls.append((text, normalize_embeddings))
        return np.zeros(384, dtype=np.float32)


def test_embed_query_returns_384_vector(monkeypatch) -> None:
    embedder.SentenceTransformer = None
    monkeypatch.setitem(
        __import__("sys").modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=FakeSentenceTransformer),
    )

    active_embedder = Embedder()
    vector = active_embedder.embed_query("SELECT count() FROM events")

    assert vector.shape == (384,)
    assert active_embedder.model.calls[0][0] == "query: SELECT count() FROM events"


def test_minilm_model_does_not_use_e5_prefix(monkeypatch) -> None:
    embedder.SentenceTransformer = None
    monkeypatch.setitem(
        __import__("sys").modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=FakeSentenceTransformer),
    )

    active_embedder = Embedder(model_key="minilm-l6")
    active_embedder.embed_document("ClickHouse docs")

    assert active_embedder.model.model_name == "sentence-transformers/all-MiniLM-L6-v2"
    assert active_embedder.model.calls[0][0] == "ClickHouse docs"


def test_unknown_model_key_raises_helpful_error() -> None:
    with pytest.raises(ValueError, match="Unknown embedding model"):
        Embedder(model_key="missing-model")

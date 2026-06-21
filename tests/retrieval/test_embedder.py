from __future__ import annotations

from types import SimpleNamespace

import numpy as np

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
    monkeypatch.setitem(
        __import__("sys").modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=FakeSentenceTransformer),
    )

    vector = Embedder().embed_query("SELECT count() FROM events")

    assert vector.shape == (384,)

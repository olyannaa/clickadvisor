from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer as SentenceTransformerType
else:
    SentenceTransformer: Any = None


class Embedder:
    MODEL_NAME = "intfloat/multilingual-e5-small"

    def __init__(self) -> None:
        self._model: SentenceTransformerType | None = None

    @property
    def model(self) -> SentenceTransformerType:
        global SentenceTransformer
        if self._model is None:
            if SentenceTransformer is None:
                from sentence_transformers import SentenceTransformer as LoadedTransformer

                SentenceTransformer = LoadedTransformer

            self._model = SentenceTransformer(self.MODEL_NAME)
        return self._model

    def embed_query(self, text: str) -> np.ndarray:
        return self.model.encode(f"query: {text}", normalize_embeddings=True)

    def embed_document(self, text: str) -> np.ndarray:
        return self.model.encode(f"passage: {text}", normalize_embeddings=True)

    def embed_batch(self, texts: list[str], is_query: bool = False) -> np.ndarray:
        prefix = "query: " if is_query else "passage: "
        prefixed = [f"{prefix}{text}" for text in texts]
        return self.model.encode(prefixed, normalize_embeddings=True, batch_size=32)

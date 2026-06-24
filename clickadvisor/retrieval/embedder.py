from __future__ import annotations

from typing import Any, cast

import numpy as np

SentenceTransformer: Any = None


class Embedder:
    AVAILABLE_MODELS = {
        "multilingual-e5-small": {
            "name": "intfloat/multilingual-e5-small",
            "size_mb": 117,
            "languages": "multilingual",
            "use_prefix": True,
        },
        "minilm-l6": {
            "name": "sentence-transformers/all-MiniLM-L6-v2",
            "size_mb": 80,
            "languages": "english-only",
            "use_prefix": False,
        },
    }
    DEFAULT_MODEL = "multilingual-e5-small"

    def __init__(self, model_key: str = DEFAULT_MODEL) -> None:
        if model_key not in self.AVAILABLE_MODELS:
            available = ", ".join(sorted(self.AVAILABLE_MODELS))
            raise ValueError(f"Unknown embedding model '{model_key}'. Available: {available}")
        self.model_key = model_key
        self.model_config = self.AVAILABLE_MODELS[model_key]
        self._model: Any | None = None

    @property
    def model(self) -> Any:
        global SentenceTransformer
        if self._model is None:
            if SentenceTransformer is None:
                from sentence_transformers import SentenceTransformer as LoadedTransformer

                SentenceTransformer = LoadedTransformer

            self._model = SentenceTransformer(self.model_config["name"])
        return self._model

    def embed_query(self, text: str) -> np.ndarray:
        if self.model_config["use_prefix"]:
            text = f"query: {text}"
        return cast(np.ndarray, self.model.encode(text, normalize_embeddings=True))

    def embed_document(self, text: str) -> np.ndarray:
        if self.model_config["use_prefix"]:
            text = f"passage: {text}"
        return cast(np.ndarray, self.model.encode(text, normalize_embeddings=True))

    def embed_batch(self, texts: list[str], is_query: bool = False) -> np.ndarray:
        prefixed = texts
        if self.model_config["use_prefix"]:
            prefix = "query: " if is_query else "passage: "
            prefixed = [f"{prefix}{text}" for text in texts]
        return cast(
            np.ndarray,
            self.model.encode(prefixed, normalize_embeddings=True, batch_size=32),
        )

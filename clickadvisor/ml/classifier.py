from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer

from clickadvisor.ml.dataset import BenchmarkExample
from clickadvisor.ml.features import ordered_feature_names

try:  # CatBoost is optional for library imports, but used by the ablation script when available.
    from catboost import CatBoostClassifier
except ImportError:  # pragma: no cover - exercised only in lean environments.
    CatBoostClassifier = None


class EstimatorProtocol(Protocol):
    def fit(self, x: np.ndarray, y: np.ndarray) -> Any: ...

    def predict(self, x: np.ndarray) -> np.ndarray: ...


@dataclass(frozen=True, slots=True)
class DatasetMatrix:
    x: np.ndarray
    y: np.ndarray
    case_ids: list[str]
    feature_names: list[str]
    label_names: list[str]


@dataclass(frozen=True, slots=True)
class ClassifierMetrics:
    model: str
    train_f1_macro: float
    train_f1_micro: float
    test_f1_macro: float
    test_f1_micro: float
    test_precision_macro: float
    test_recall_macro: float
    test_precision_micro: float
    test_recall_micro: float
    train_cases: int
    test_cases: int
    labels: int

    def as_row(self) -> dict[str, str | float | int]:
        return {
            "model": self.model,
            "train_f1_macro": self.train_f1_macro,
            "train_f1_micro": self.train_f1_micro,
            "test_f1_macro": self.test_f1_macro,
            "test_f1_micro": self.test_f1_micro,
            "test_precision_macro": self.test_precision_macro,
            "test_recall_macro": self.test_recall_macro,
            "test_precision_micro": self.test_precision_micro,
            "test_recall_micro": self.test_recall_micro,
            "train_cases": self.train_cases,
            "test_cases": self.test_cases,
            "labels": self.labels,
        }


def build_label_binarizer(examples: Sequence[BenchmarkExample]) -> MultiLabelBinarizer:
    label_names = sorted({label for example in examples for label in example.labels})
    return MultiLabelBinarizer(classes=label_names)


def vectorize_examples(
    examples: Sequence[BenchmarkExample],
    *,
    feature_names: Sequence[str] | None = None,
    label_binarizer: MultiLabelBinarizer | None = None,
) -> DatasetMatrix:
    rows: list[Mapping[str, float]] = [example.features for example in examples]
    names = list(feature_names or ordered_feature_names(rows))
    labels = label_binarizer or build_label_binarizer(examples)
    if not hasattr(labels, "classes_"):
        labels.fit([example.labels for example in examples])

    x = np.array(
        [[float(example.features.get(feature_name, 0.0)) for feature_name in names] for example in examples],
        dtype=float,
    )
    y = labels.transform([example.labels for example in examples]).astype(int)
    return DatasetMatrix(
        x=x,
        y=y,
        case_ids=[example.case_id for example in examples],
        feature_names=names,
        label_names=list(labels.classes_),
    )


def make_classifiers(random_state: int = 42) -> dict[str, EstimatorProtocol]:
    classifiers: dict[str, EstimatorProtocol] = {
        "logistic_regression": OneVsRestClassifier(
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                solver="liblinear",
                random_state=random_state,
            )
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=250,
            max_depth=None,
            min_samples_leaf=1,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        ),
    }
    if CatBoostClassifier is not None:
        classifiers["catboost"] = MultiOutputClassifier(
            CatBoostClassifier(
                iterations=120,
                depth=4,
                learning_rate=0.08,
                loss_function="Logloss",
                random_seed=random_state,
                verbose=False,
                allow_writing_files=False,
            )
        )
    return classifiers


def evaluate_classifier(
    model_name: str,
    estimator: EstimatorProtocol,
    train: DatasetMatrix,
    test: DatasetMatrix,
) -> ClassifierMetrics:
    estimator.fit(train.x, train.y)
    train_pred = _normalize_predictions(estimator.predict(train.x))
    test_pred = _normalize_predictions(estimator.predict(test.x))

    return ClassifierMetrics(
        model=model_name,
        train_f1_macro=f1_score(train.y, train_pred, average="macro", zero_division=0),
        train_f1_micro=f1_score(train.y, train_pred, average="micro", zero_division=0),
        test_f1_macro=f1_score(test.y, test_pred, average="macro", zero_division=0),
        test_f1_micro=f1_score(test.y, test_pred, average="micro", zero_division=0),
        test_precision_macro=precision_score(test.y, test_pred, average="macro", zero_division=0),
        test_recall_macro=recall_score(test.y, test_pred, average="macro", zero_division=0),
        test_precision_micro=precision_score(test.y, test_pred, average="micro", zero_division=0),
        test_recall_micro=recall_score(test.y, test_pred, average="micro", zero_division=0),
        train_cases=len(train.case_ids),
        test_cases=len(test.case_ids),
        labels=len(train.label_names),
    )


def evaluate_classifiers(
    train_examples: Sequence[BenchmarkExample],
    test_examples: Sequence[BenchmarkExample],
    *,
    random_state: int = 42,
    model_names: Iterable[str] | None = None,
) -> list[ClassifierMetrics]:
    all_examples = [*train_examples, *test_examples]
    label_binarizer = build_label_binarizer(all_examples)
    label_binarizer.fit([example.labels for example in all_examples])
    all_feature_rows: list[Mapping[str, float]] = [example.features for example in all_examples]
    feature_names = ordered_feature_names(all_feature_rows)

    train = vectorize_examples(
        train_examples,
        feature_names=feature_names,
        label_binarizer=label_binarizer,
    )
    test = vectorize_examples(
        test_examples,
        feature_names=feature_names,
        label_binarizer=label_binarizer,
    )

    classifiers = make_classifiers(random_state=random_state)
    selected = set(model_names) if model_names is not None else set(classifiers)
    return [
        evaluate_classifier(name, estimator, train, test)
        for name, estimator in classifiers.items()
        if name in selected
    ]


def _normalize_predictions(predictions: np.ndarray) -> np.ndarray:
    array = np.asarray(predictions)
    if array.ndim == 3 and array.shape[-1] == 1:
        array = array[:, :, 0]
    return (array > 0).astype(int)

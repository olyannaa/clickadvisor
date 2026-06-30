from __future__ import annotations

from pathlib import Path

from clickadvisor.ml.classifier import evaluate_classifiers
from clickadvisor.ml.dataset import build_examples, load_benchmark_cases, load_split, split_examples


def test_logistic_regression_classifier_ablation_smoke() -> None:
    cases = load_benchmark_cases(Path("benchmark/cases/synthetic_expanded"))
    examples = build_examples(cases)
    train, test = split_examples(
        examples,
        load_split(Path("benchmark/splits/synthetic_expanded_v1.yaml")),
    )

    metrics = evaluate_classifiers(train, test, model_names=["logistic_regression"])

    assert len(metrics) == 1
    result = metrics[0]
    assert result.model == "logistic_regression"
    assert result.train_cases == 144
    assert result.test_cases == 36
    assert result.labels >= 20
    assert 0.0 <= result.test_f1_macro <= 1.0

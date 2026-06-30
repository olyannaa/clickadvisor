from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from clickadvisor.ml.features import FeatureMap, QueryFeatureExtractor


@dataclass(frozen=True, slots=True)
class BenchmarkExample:
    case_id: str
    sql: str
    labels: tuple[str, ...]
    features: FeatureMap


def load_benchmark_cases(cases_dir: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(cases_dir.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            cases.append(payload)
    return cases


def load_split(split_path: Path) -> dict[str, set[str]]:
    payload = yaml.safe_load(split_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("split metadata must be a YAML object")
    return {
        "train": set(_as_string_list(payload.get("train_case_ids"), "train_case_ids")),
        "test": set(_as_string_list(payload.get("test_case_ids"), "test_case_ids")),
    }


def build_examples(
    cases: Iterable[dict[str, Any]],
    extractor: QueryFeatureExtractor | None = None,
) -> list[BenchmarkExample]:
    feature_extractor = extractor or QueryFeatureExtractor()
    examples: list[BenchmarkExample] = []
    for case in cases:
        case_id = _required_string(case, "case_id")
        sql = _required_string(case, "sql")
        labels = tuple(_as_string_list(case.get("expected_rules_to_fire"), "expected_rules_to_fire"))
        features = feature_extractor.extract(sql).features
        examples.append(BenchmarkExample(case_id=case_id, sql=sql, labels=labels, features=features))
    return examples


def split_examples(
    examples: Iterable[BenchmarkExample],
    split: dict[str, set[str]],
) -> tuple[list[BenchmarkExample], list[BenchmarkExample]]:
    train_ids = split["train"]
    test_ids = split["test"]
    train: list[BenchmarkExample] = []
    test: list[BenchmarkExample] = []
    for example in examples:
        if example.case_id in train_ids:
            train.append(example)
        elif example.case_id in test_ids:
            test.append(example)
    return train, test


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _as_string_list(value: Any, key: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings")
    return value

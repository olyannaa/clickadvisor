from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold

DEFAULT_FEATURES_PATH = Path("data/ml/expert_dataset/features/features.jsonl")
DEFAULT_OUTPUT_PATH = Path("data/ml/expert_dataset/splits/risk_split_v1.json")
LABELS = ("low", "medium", "high")


def main() -> None:
    args = parse_args()
    rows = load_rows(args.features)
    split = build_split(
        rows,
        features_path=args.features,
        test_size=args.test_size,
        holdout_size=args.holdout_size,
        random_state=args.random_state,
        folds=args.folds,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(split, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "Created risk ML split: "
        f"train={len(split['train_ids'])}, test={len(split['test_ids'])}, "
        f"holdout={len(split['holdout_ids'])}, folds={len(split['folds'])}, output={args.output}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create group-aware train/test/holdout splits.")
    parser.add_argument("--features", type=Path, default=DEFAULT_FEATURES_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--test-size", type=float, default=0.15)
    parser.add_argument("--holdout-size", type=float, default=0.15)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_split(
    rows: list[dict[str, Any]],
    *,
    features_path: Path,
    test_size: float,
    holdout_size: float,
    random_state: int,
    folds: int,
) -> dict[str, Any]:
    ids = np.array([str(row["id"]) for row in rows], dtype=object)
    labels = np.array([str(row["target"]) for row in rows], dtype=object)
    groups = np.array([str(row["group_id"]) for row in rows], dtype=object)
    dummy_x = np.zeros((len(rows), 1))

    train_test_idx, holdout_idx = next(
        GroupShuffleSplit(
            n_splits=1,
            test_size=holdout_size,
            random_state=random_state,
        ).split(dummy_x, labels, groups)
    )
    remaining_rows = dummy_x[train_test_idx]
    remaining_labels = labels[train_test_idx]
    remaining_groups = groups[train_test_idx]
    relative_test_size = test_size / (1.0 - holdout_size)
    train_rel_idx, test_rel_idx = next(
        GroupShuffleSplit(
            n_splits=1,
            test_size=relative_test_size,
            random_state=random_state + 1,
        ).split(remaining_rows, remaining_labels, remaining_groups)
    )
    train_idx = train_test_idx[train_rel_idx]
    test_idx = train_test_idx[test_rel_idx]

    cv = StratifiedGroupKFold(
        n_splits=folds,
        shuffle=True,
        random_state=random_state,
    )
    fold_rows: list[dict[str, Any]] = []
    train_x = dummy_x[train_idx]
    train_labels = labels[train_idx]
    train_groups = groups[train_idx]
    for fold_index, (fold_train_rel, fold_valid_rel) in enumerate(
        cv.split(train_x, train_labels, train_groups),
        start=1,
    ):
        fold_train_idx = train_idx[fold_train_rel]
        fold_valid_idx = train_idx[fold_valid_rel]
        fold_rows.append(
            {
                "fold": fold_index,
                "train_ids": sorted(ids[fold_train_idx].tolist()),
                "valid_ids": sorted(ids[fold_valid_idx].tolist()),
                "train_label_counts": counts_for(labels[fold_train_idx]),
                "valid_label_counts": counts_for(labels[fold_valid_idx]),
                "train_group_count": unique_count(groups[fold_train_idx]),
                "valid_group_count": unique_count(groups[fold_valid_idx]),
            }
        )

    return {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/create_ml_splits.py",
        "features_path": str(features_path),
        "strategy": {
            "outer_splitter": "GroupShuffleSplit",
            "cv_splitter": "StratifiedGroupKFold",
            "group_key": "source::family::origin.parent_sql_hash_or_sql_hash",
            "test_size": test_size,
            "holdout_size": holdout_size,
            "folds": folds,
            "random_state": random_state,
        },
        "record_count": len(rows),
        "train_ids": sorted(ids[train_idx].tolist()),
        "test_ids": sorted(ids[test_idx].tolist()),
        "holdout_ids": sorted(ids[holdout_idx].tolist()),
        "folds": fold_rows,
        "summary": {
            "all_label_counts": counts_for(labels),
            "train_label_counts": counts_for(labels[train_idx]),
            "test_label_counts": counts_for(labels[test_idx]),
            "holdout_label_counts": counts_for(labels[holdout_idx]),
            "all_group_count": unique_count(groups),
            "train_group_count": unique_count(groups[train_idx]),
            "test_group_count": unique_count(groups[test_idx]),
            "holdout_group_count": unique_count(groups[holdout_idx]),
            "group_leakage": leakage_summary(groups, train_idx, test_idx, holdout_idx),
        },
    }


def counts_for(values: np.ndarray) -> dict[str, int]:
    counts = Counter(str(value) for value in values)
    return {label: counts.get(label, 0) for label in LABELS}


def unique_count(values: np.ndarray) -> int:
    return len({str(value) for value in values})


def leakage_summary(
    groups: np.ndarray,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
    holdout_idx: np.ndarray,
) -> dict[str, int]:
    train_groups = {str(value) for value in groups[train_idx]}
    test_groups = {str(value) for value in groups[test_idx]}
    holdout_groups = {str(value) for value in groups[holdout_idx]}
    return {
        "train_test_overlap": len(train_groups & test_groups),
        "train_holdout_overlap": len(train_groups & holdout_groups),
        "test_holdout_overlap": len(test_groups & holdout_groups),
    }


if __name__ == "__main__":
    main()

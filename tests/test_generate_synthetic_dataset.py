from scripts.benchmark.generate_synthetic_dataset import build_cases, build_split


def test_generated_synthetic_dataset_has_expected_size_and_negatives() -> None:
    cases = build_cases()
    negative_cases = [case for case in cases if not case["expected_rules_to_fire"]]
    assert len(cases) >= 150
    assert len(negative_cases) >= 20
    assert all(case["status"] == "validated" for case in cases)


def test_generated_synthetic_split_is_deterministic() -> None:
    case_ids = [case["case_id"] for case in build_cases()]
    split_a = build_split(case_ids, seed=42)
    split_b = build_split(case_ids, seed=42)
    assert split_a == split_b
    assert split_a["counts"]["train"] + split_a["counts"]["test"] == len(case_ids)

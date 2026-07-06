from __future__ import annotations

import pytest

from scripts.lab.run_risk_baseline_ladder import features_for_policy


def test_no_rule_derived_policy_removes_explicit_rule_features() -> None:
    features = {
        "rule_findings_count": 2.0,
        "rule_present_r_001": 1.0,
        "base_has_count_distinct": 1.0,
        "sql_token_length": 12.0,
    }

    filtered = features_for_policy(features, "no_rule_derived")

    assert "rule_findings_count" not in filtered
    assert "rule_present_r_001" not in filtered
    assert filtered["base_has_count_distinct"] == 1.0
    assert filtered["sql_token_length"] == 12.0


def test_leakage_aware_policy_keeps_only_neutral_shape_features() -> None:
    features = {
        "rule_present_r_001": 1.0,
        "base_has_count_distinct": 1.0,
        "has_final": 1.0,
        "sql_token_length": 12.0,
        "base_function_call_count": 3.0,
    }

    filtered = features_for_policy(features, "leakage_aware")

    assert filtered == {
        "base_function_call_count": 3.0,
        "sql_token_length": 12.0,
    }


def test_unknown_feature_policy_raises() -> None:
    with pytest.raises(ValueError, match="unknown feature policy"):
        features_for_policy({}, "unknown")

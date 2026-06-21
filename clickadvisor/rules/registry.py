from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from clickadvisor.rules.base import Rule
from clickadvisor.rules.detectors import D003SelectStar, D004MissingLimit, D007FinalModifier
from clickadvisor.rules.tier1 import (
    R001CountDistinct,
    R002CountDistinctApprox,
    R003QuantileExact,
    R004CountStarDistinctSubquery,
    R005ToDateEquality,
    R006ToYYYYMMRange,
    R007ToStartOfIntervalRange,
    R008RedundantCast,
    R009InSingleton,
    R010DisjunctionToIn,
    R011HavingToWhere,
    R012ConstantPredicate,
    R013LengthToEmpty,
    R014GroupByStringHash,
    R015DistinctAfterGroupBy,
    R016OrderByWithoutLimit,
    R017SubqueryFilterPushdown,
    R018UnionToUnionAll,
)

DEFAULT_CARDS_DIR = Path("docs/rules/cards")
RULES = [
    R001CountDistinct(),
    R002CountDistinctApprox(),
    R003QuantileExact(),
    R004CountStarDistinctSubquery(),
    R005ToDateEquality(),
    R006ToYYYYMMRange(),
    R007ToStartOfIntervalRange(),
    R008RedundantCast(),
    R009InSingleton(),
    R010DisjunctionToIn(),
    R011HavingToWhere(),
    R012ConstantPredicate(),
    R013LengthToEmpty(),
    R014GroupByStringHash(),
    R015DistinctAfterGroupBy(),
    R016OrderByWithoutLimit(),
    R017SubqueryFilterPushdown(),
    R018UnionToUnionAll(),
    D003SelectStar(),
    D004MissingLimit(),
    D007FinalModifier(),
]
RULE_REGISTRY: dict[str, Rule] = {rule.rule_id: rule for rule in RULES}


def register_rule(rule: Rule) -> Rule:
    rule_id = getattr(rule, "rule_id", "")
    if not rule_id:
        raise ValueError("rule instances must define rule_id")
    if rule_id in RULE_REGISTRY:
        raise ValueError(f"rule already registered: {rule_id}")
    RULE_REGISTRY[rule_id] = rule
    RULES.append(rule)
    return rule


def get_registered_rule(rule_id: str) -> Rule | None:
    return RULE_REGISTRY.get(rule_id)


def get_all_rules() -> list[Rule]:
    return list(RULES)


def load_rule_cards(cards_dir: Path = DEFAULT_CARDS_DIR) -> dict[str, dict[str, Any]]:
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(cards_dir.rglob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        rule_id = payload.get("id")
        if isinstance(rule_id, str):
            cards[rule_id] = payload
    return cards


def get_applicable_rules(
    ch_version: str | None,
    include_skipped: bool = False,
) -> list[Rule] | tuple[list[Rule], list[str]]:
    applicable: list[Rule] = []
    skipped: list[str] = []

    for rule in RULES:
        if ch_version is None:
            applicable.append(rule)
            continue

        if rule.is_applicable_for_version(ch_version):
            applicable.append(rule)
        else:
            skipped.append(rule.rule_id)

    if include_skipped:
        return applicable, sorted(skipped)
    return applicable

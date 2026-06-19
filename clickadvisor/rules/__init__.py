from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from clickadvisor.rules.base import Rule

RULE_REGISTRY: dict[str, type[Rule]] = {}
DEFAULT_CARDS_DIR = Path("docs/rules/cards")


def register_rule(rule_class: type[Rule]) -> type[Rule]:
    rule_id = getattr(rule_class, "rule_id", "")
    if not rule_id:
        raise ValueError("rule classes must define rule_id")
    if rule_id in RULE_REGISTRY:
        raise ValueError(f"rule already registered: {rule_id}")
    RULE_REGISTRY[rule_id] = rule_class
    return rule_class


def get_registered_rule(rule_id: str) -> type[Rule] | None:
    return RULE_REGISTRY.get(rule_id)


def load_rule_cards(cards_dir: Path = DEFAULT_CARDS_DIR) -> dict[str, dict[str, Any]]:
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(cards_dir.rglob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            continue
        rule_id = raw.get("id")
        if isinstance(rule_id, str):
            cards[rule_id] = raw
    return cards


def iter_rule_catalog(cards_dir: Path = DEFAULT_CARDS_DIR) -> list[dict[str, Any]]:
    return list(load_rule_cards(cards_dir).values())


__all__ = [
    "DEFAULT_CARDS_DIR",
    "RULE_REGISTRY",
    "Rule",
    "get_registered_rule",
    "iter_rule_catalog",
    "load_rule_cards",
    "register_rule",
]

from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D007_final_modifier import D007FinalModifier


def test_d007_matches_final_modifier() -> None:
    rule = D007FinalModifier()
    context = QueryContext(sql="SELECT * FROM events FINAL")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "D-007"


def test_d007_does_not_match_without_final() -> None:
    rule = D007FinalModifier()
    context = QueryContext(sql="SELECT * FROM events")
    finding = rule.check(context)
    assert finding is None

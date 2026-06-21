from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R009_in_singleton import R009InSingleton


def test_r009_matches_singleton_in() -> None:
    rule = R009InSingleton()
    finding = rule.check(QueryContext(sql="SELECT * FROM events WHERE country IN ('RU')"))
    assert finding is not None
    assert finding.rule_id == "R-009"


def test_r009_does_not_match_multi_value_in() -> None:
    rule = R009InSingleton()
    finding = rule.check(QueryContext(sql="SELECT * FROM events WHERE country IN ('RU', 'BY')"))
    assert finding is None

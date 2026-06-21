from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R012_constant_predicate import R012ConstantPredicate


def test_r012_matches_constant_predicate() -> None:
    rule = R012ConstantPredicate()
    finding = rule.check(QueryContext(sql="SELECT * FROM events WHERE TRUE AND user_id = 5"))
    assert finding is not None
    assert finding.rule_id == "R-012"


def test_r012_does_not_match_normal_filter() -> None:
    rule = R012ConstantPredicate()
    finding = rule.check(QueryContext(sql="SELECT * FROM events WHERE user_id = 5"))
    assert finding is None

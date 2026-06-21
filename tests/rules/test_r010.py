from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R010_disjunction_to_in import R010DisjunctionToIn


def test_r010_matches_disjunction_chain() -> None:
    rule = R010DisjunctionToIn()
    context = QueryContext(
        sql="SELECT * FROM events WHERE country = 'RU' OR country = 'BY' OR country = 'KZ'"
    )
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-010"
    assert "IN ('RU', 'BY', 'KZ')" in finding.suggestion


def test_r010_does_not_match_short_disjunction() -> None:
    rule = R010DisjunctionToIn()
    context = QueryContext(sql="SELECT * FROM events WHERE country = 'RU' OR country = 'BY'")
    finding = rule.check(context)
    assert finding is None

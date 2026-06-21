from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R011_having_to_where import R011HavingToWhere


def test_r011_matches_having_without_aggregate() -> None:
    rule = R011HavingToWhere()
    context = QueryContext(
        sql="SELECT user_id, COUNT(*) FROM events GROUP BY user_id HAVING country = 'RU' AND COUNT(*) > 100"
    )
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-011"


def test_r011_does_not_match_pure_aggregate_having() -> None:
    rule = R011HavingToWhere()
    context = QueryContext(
        sql="SELECT user_id, COUNT(*) FROM events GROUP BY user_id HAVING COUNT(*) > 100"
    )
    finding = rule.check(context)
    assert finding is None

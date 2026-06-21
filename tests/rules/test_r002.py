from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R002_count_distinct_approx import R002CountDistinctApprox


def test_r002_matches_count_distinct() -> None:
    rule = R002CountDistinctApprox()
    finding = rule.check(QueryContext(sql="SELECT COUNT(DISTINCT session_id) FROM logs"))
    assert finding is not None
    assert finding.rule_id == "R-002"


def test_r002_does_not_match_simple_count() -> None:
    rule = R002CountDistinctApprox()
    finding = rule.check(QueryContext(sql="SELECT COUNT(session_id) FROM logs"))
    assert finding is None

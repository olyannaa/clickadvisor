from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R003_quantile_exact import R003QuantileExact


def test_r003_matches_quantile_exact() -> None:
    rule = R003QuantileExact()
    finding = rule.check(
        QueryContext(sql="SELECT quantileExact(0.95)(response_time) FROM requests")
    )
    assert finding is not None
    assert finding.rule_id == "R-003"


def test_r003_does_not_match_other_aggregate() -> None:
    rule = R003QuantileExact()
    finding = rule.check(QueryContext(sql="SELECT avg(response_time) FROM requests"))
    assert finding is None

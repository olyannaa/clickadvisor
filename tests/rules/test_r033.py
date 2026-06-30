from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R033_max_case_to_maxif import R033MaxCaseToMaxIf


def test_r033_triggers_on_max_case() -> None:
    rule = R033MaxCaseToMaxIf()
    ctx = QueryContext(
        sql="SELECT MAX(CASE WHEN status = 'active' THEN score END) AS max_score FROM users"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-033"
    assert "maxIf" in finding.suggestion


def test_r033_no_trigger_on_plain_max() -> None:
    rule = R033MaxCaseToMaxIf()
    ctx = QueryContext(sql="SELECT MAX(score) FROM users")
    finding = rule.check(ctx)
    assert finding is None

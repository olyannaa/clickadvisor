from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R024_string_ip_column import R024StringIPColumn


def test_r024_triggers_on_string_client_ip() -> None:
    rule = R024StringIPColumn()
    ctx = QueryContext(
        sql="CREATE TABLE access_log (request_id UInt64, client_ip String) ENGINE = MergeTree ORDER BY request_id"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "R-024"
    assert "client_ip" in finding.description


def test_r024_no_trigger_on_string_username() -> None:
    rule = R024StringIPColumn()
    ctx = QueryContext(
        sql="CREATE TABLE users (user_id UInt64, username String) ENGINE = MergeTree ORDER BY user_id"
    )
    finding = rule.check(ctx)
    assert finding is None

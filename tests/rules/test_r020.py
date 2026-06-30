from clickadvisor.core.models import QueryContext
from clickadvisor.rules.tier1.R020_cast_or_default import R020CastOrDefault


def test_r020_triggers_on_cast_column() -> None:
    rule = R020CastOrDefault()
    context = QueryContext(sql="SELECT CAST(raw_value AS UInt32) FROM events")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-020"
    assert "accurateCastOrDefault" in finding.suggestion


def test_r020_triggers_on_toUInt32_column() -> None:
    rule = R020CastOrDefault()
    context = QueryContext(sql="SELECT toUInt32(raw_value) FROM events")
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "R-020"


def test_r020_no_trigger_on_safe_variant() -> None:
    rule = R020CastOrDefault()
    context = QueryContext(sql="SELECT toUInt32OrZero(raw_value) FROM events")
    finding = rule.check(context)
    assert finding is None


def test_r020_no_trigger_on_cast_literal() -> None:
    rule = R020CastOrDefault()
    context = QueryContext(sql="SELECT CAST('123' AS UInt32) FROM events")
    finding = rule.check(context)
    assert finding is None

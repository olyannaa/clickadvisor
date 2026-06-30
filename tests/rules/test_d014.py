from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D014_async_insert_no_wait import D014AsyncInsertNoWait


def test_d014_triggers_on_async_insert_without_wait() -> None:
    rule = D014AsyncInsertNoWait()
    context = QueryContext(
        sql="INSERT INTO events SETTINGS async_insert=1 VALUES (1, 'click')"
    )
    finding = rule.check(context)
    assert finding is not None
    assert finding.rule_id == "D-014"
    assert finding.severity == "high"


def test_d014_no_trigger_when_wait_flag_present() -> None:
    rule = D014AsyncInsertNoWait()
    context = QueryContext(
        sql="INSERT INTO events SETTINGS async_insert=1, wait_for_async_insert=1 VALUES (1, 'click')"
    )
    finding = rule.check(context)
    assert finding is None


def test_d014_no_trigger_on_select() -> None:
    rule = D014AsyncInsertNoWait()
    context = QueryContext(sql="SELECT * FROM events WHERE async_insert = 1")
    finding = rule.check(context)
    assert finding is None


def test_d014_no_trigger_when_no_async_insert() -> None:
    rule = D014AsyncInsertNoWait()
    context = QueryContext(sql="INSERT INTO events VALUES (1, 'click')")
    finding = rule.check(context)
    assert finding is None

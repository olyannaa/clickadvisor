from clickadvisor.core.models import QueryContext
from clickadvisor.rules.detectors.D018_deprecated_ngrambf_tokenbf_index import (
    D018DeprecatedNgramBFIndex,
)


def test_d018_triggers_on_ngrambf_v1() -> None:
    rule = D018DeprecatedNgramBFIndex()
    ctx = QueryContext(
        sql="ALTER TABLE logs ADD INDEX idx_msg message TYPE ngrambf_v1(4, 1024, 2, 0) GRANULARITY 4"
    )
    finding = rule.check(ctx)
    assert finding is not None
    assert finding.rule_id == "D-018"
    assert finding.severity == "medium"
    assert "ngrambf_v1" in finding.description


def test_d018_no_trigger_on_text_index() -> None:
    rule = D018DeprecatedNgramBFIndex()
    ctx = QueryContext(
        sql="ALTER TABLE logs ADD INDEX idx_msg message TYPE text GRANULARITY 1"
    )
    finding = rule.check(ctx)
    assert finding is None

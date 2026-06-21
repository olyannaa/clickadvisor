from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.core.version import version_gte


class Rule(ABC):
    rule_id: str
    name: str
    tier: str
    ch_version_introduced: str = "1.0"
    ch_version_deprecated: Optional[str] = None

    def __init__(self, mode: str = "diagnose") -> None:
        self.mode = mode

    def is_applicable_for_version(self, ch_version: str) -> bool:
        if not version_gte(ch_version, self.ch_version_introduced):
            return False
        if self.ch_version_deprecated is None:
            return True
        return not version_gte(ch_version, self.ch_version_deprecated)

    @abstractmethod
    def check(self, context: QueryContext) -> Optional[Finding]:
        """Return a finding when the rule matches, otherwise ``None``."""

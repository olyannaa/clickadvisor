from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Rule(ABC):
    """Abstract runtime contract for ClickAdvisor rules."""

    rule_id: str

    @abstractmethod
    def check_preconditions(self, context: Any) -> bool:
        """Return whether the rule is applicable for the supplied analysis context."""

    @abstractmethod
    def apply(self, query: Any) -> Any:
        """Return a transformed query or recommendation artifact."""

    @abstractmethod
    def generate_proof(self) -> str | dict[str, Any]:
        """Return rule proof metadata or a placeholder proof artifact."""

    @abstractmethod
    def get_metadata(self) -> dict[str, Any]:
        """Return machine-readable metadata for reporting and registry use."""

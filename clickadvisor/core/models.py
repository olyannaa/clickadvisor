from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class QueryContext:
    sql: str
    explain_output: Optional[str] = None
    schema_ddl: Optional[str] = None
    ch_version: Optional[str] = None


@dataclass(slots=True)
class Finding:
    rule_id: str
    rule_name: str
    tier: str
    severity: str
    description: str
    suggestion: str
    example_before: Optional[str] = None
    example_after: Optional[str] = None
    explain_why: Optional[str] = None
    confidence: str = "provable"
    ch_version_introduced: Optional[str] = None


@dataclass(slots=True)
class Report:
    query_context: QueryContext
    findings: list[Finding] = field(default_factory=list)
    rules_skipped_version: list[str] = field(default_factory=list)

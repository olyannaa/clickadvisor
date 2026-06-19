from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisContext:
    sql: str
    dialect: str = "clickhouse"
    llm_mode: str = "none"
    metadata_sources: list[str] = field(default_factory=list)

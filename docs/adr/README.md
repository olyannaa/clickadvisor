# ADR Index

- [ADR-001: CLI as Primary Interface; Web as Optional Thin Wrapper](./ADR-001-cli-primary.md) - Establishes the Typer-based CLI as the main product surface and limits web delivery to an optional wrapper over the same core.
- [ADR-002: ClickHouse Only in MVP; PostgreSQL in Backlog](./ADR-002-clickhouse-only-mvp.md) - Fixes the first implementation window on deep ClickHouse support rather than split-engine breadth.
- [ADR-003: Three-Tier Rule System](./ADR-003-three-tier-rules.md) - Defines the confidence model for optimization advice through formal, cost-based, and advisory rule tiers.
- [ADR-004: Hybrid LLM Architecture (`none` / `local` / `remote`)](./ADR-004-hybrid-llm-modes.md) - Documents the three LLM backends and the intentional requirement that the product remains useful without any LLM.
- [ADR-005: Cost-Model Evaluation Instead of Sample-Based Verification](./ADR-005-cost-model-over-sampling.md) - Chooses planner- and metadata-based estimation over replay or sample execution as the main validation path.
- [ADR-006: Versioned Knowledge Base with Automatic Refresh](./ADR-006-versioned-knowledge-base.md) - Defines the continuously rebuilt knowledge base and its source/version metadata contract.
- [ADR-007: Quality Metrics as Precision/Recall Plus DBA User Study](./ADR-007-quality-metrics-benchmark-user-study.md) - Sets benchmark detection quality and user-study diagnosis speed as the main measures of product success.
- [ADR-008: Security Model and Zero Data Egress](./ADR-008-zero-data-egress.md) - Freezes the security boundary around SQL, metadata, redaction, and read-only runtime behavior.
- [ADR-009: Technology Stack Selection Rationale](./ADR-009-technology-stack.md) - Records the chosen implementation stack and the tradeoffs versus the main alternatives.
- [ADR-010: Version-Aware Rule Filtering](./ADR-010-version-aware-rules.md) - Makes ClickHouse version detection mandatory and filters catalog rules by their applicability window.
- [ADR-011: MCP Server as Secondary Interface](./ADR-011-mcp-server-interface.md) - Adds an MCP server as a thin second interface over the same core while keeping the CLI primary.
- [ADR-012: Educational `explain` Mode](./ADR-012-explain-why-mode.md) - Introduces a separate explanation-first mode and requires explain templates in Tier 1 rule cards.

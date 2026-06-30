# ClickAdvisor

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![ClickHouse](https://img.shields.io/badge/ClickHouse-SQL%20advisor-ffcc01)
![Rules](https://img.shields.io/badge/rule%20cards-119%2F119-brightgreen)

[Русский](README.md) | [English](README.en.md)

ClickAdvisor is a local-first CLI and MCP server for ClickHouse SQL analysis.
It uses deterministic rules, optional ML evaluation surfaces, and local
retrieval over ClickHouse documentation. SQL is not sent to external LLM APIs.

The full project documentation is maintained in Russian in [README.md](README.md).

Current repository status:

- 119 valid rule cards
- 119 registered implementations
- 0 backlog rule cards
- 222 `synthetic_expanded` benchmark cases
- strict benchmark precision / recall / F1: `1.000 / 1.000 / 1.000`

Quick start:

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor analyze --sql query.sql
```

Enterprise note: ClickAdvisor is designed for environments where SQL, DDL,
EXPLAIN output, and cluster settings must stay inside the organization for
compliance reasons.

# ADR-014: No Generative LLM in the Critical Path

## Status

Accepted

## Context

ClickAdvisor is evaluated as a local-first SQL advisor whose primary findings
come from deterministic rules, structured AST/SQL features, and retrieval over a
local knowledge base. Earlier product notes mentioned `--llm=none`,
`--llm=local`, and `--llm=remote`, but those modes are not part of the MVP
implementation.

## Decision

Generative LLMs are not allowed to select rules, change severities, rewrite
preconditions, or produce the trusted finding set in the MVP critical path.

The production path is:

```text
SQL -> parser -> deterministic rules -> optional ML evaluation surface
    -> optional local retrieval -> report
```

AI agents may call ClickAdvisor through MCP, and Codex/Claude may assist
development, documentation, and manual review. Those tools are outside the
trusted analysis path.

## Consequences

The product story is narrower but easier to audit: each primary recommendation
has a rule id, tier, and reproducible matcher. Retrieval can add source context,
and ML classifiers can be evaluated as experiments, but neither replaces the
deterministic rule engine.

Future generated explanations may be reconsidered only downstream of validated
findings and only if they cannot alter rule selection or confidence.

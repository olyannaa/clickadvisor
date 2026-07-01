# AI And MCP Workflow

ClickAdvisor uses AI agents as an interface and development workflow aid, not as
the trusted source of production recommendations.

## Runtime Workflow

```text
Engineer / DBA / AI client
        |
        v
Local MCP tool call
        |
        v
ClickAdvisor rule engine
        |
        v
Structured findings with rule_id, tier, severity, confidence
```

The agent can ask ClickAdvisor to analyze SQL, list rules, or detect the
ClickHouse version. The answer comes from deterministic local code, not from a
generative model guessing a rewrite.

## Example Agent Instruction

Use this instruction in an MCP-capable client:

```text
When reviewing ClickHouse SQL, call the local ClickAdvisor MCP tool first.
Do not invent optimization advice. Summarize the returned rule_id, severity,
tier, and suggestion. If no finding is returned, say that ClickAdvisor found no
deterministic issue and list any remaining manual checks separately.
```

## Why This Reduces Hallucination Risk

- The analyzer returns registered `rule_id` values.
- Each finding has severity, tier, confidence, and explanation fields.
- MCP reuses the same pipeline as the CLI.
- JSON output excludes retrieval-only RAG findings for deterministic automation.
- The AI client can format and explain results, but the rule engine supplies the
  trusted finding set.

## DS And Research Workflow

AI agents are useful outside the trusted runtime path:

- collecting public sources and candidate SQL cases;
- drafting synthetic variants;
- running validators and benchmark scripts;
- summarizing EDA and error analysis;
- turning metrics into product decisions.

The DS artifacts created for the risk-label experiment follow that pattern:
dataset preparation, rule labeling, measured replay, feature extraction,
baseline ladder, and holdout error analysis are all script-backed and
reproducible.

## Safety Rule

If a recommendation is not backed by a ClickAdvisor finding, measured workload
evidence, or explicit documentation context, present it as a manual hypothesis,
not as a product recommendation.

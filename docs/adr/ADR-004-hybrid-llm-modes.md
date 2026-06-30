# ADR-004: No Generative LLM in the Critical Path

## Status

Accepted

## Context

Early project materials described three product LLM modes: `--llm=none`,
`--llm=local`, and `--llm=remote`. That design no longer matches the current
implementation or the trust model of ClickAdvisor.

The core user promise is that ClickAdvisor gives reproducible ClickHouse advice
based on explicit rules, version-aware metadata, optional planner estimates, and
retrieval over a local knowledge base. A generative LLM in the recommendation
path would introduce a new failure mode: it could phrase a recommendation more
fluently while weakening or distorting the preconditions that make the advice
safe.

At the same time, ClickAdvisor should still work well inside AI-agent workflows.
DBAs and developers increasingly use Claude Desktop, Cursor, Continue, and
other MCP-capable tools. For those users, the right integration point is not a
hidden LLM backend inside ClickAdvisor, but a tool interface that lets an agent
call the same deterministic analyzer.

## Decision

ClickAdvisor MVP does not include generative LLM execution in the product
critical path.

The product exposes:

- deterministic rule findings;
- optional retrieval context from the local Qdrant knowledge base;
- optional `EXPLAIN ESTIMATE` impact summaries;
- a stdio MCP server for AI agents and LLM clients.

The MCP server is an interface, not a decision-making layer. Claude, Cursor, or
another agent may call ClickAdvisor through MCP, but ClickAdvisor itself still
returns findings produced by the same rule engine and retrieval components used
by the CLI.

There is no `--llm=none`, `--llm=local`, or `--llm=remote` CLI mode in the MVP.
Future generative explanation features may be reconsidered only if they are
strictly downstream of validated findings and cannot change rule selection,
severity, confidence, or rewrite preconditions.

## Consequences

This removes a major documentation/code mismatch and makes the technical story
simpler to defend. The product no longer needs unused dependencies for Anthropic,
Ollama, or local LLM serving in the MVP.

The AI story becomes more precise: ClickAdvisor is MCP-compatible and can be
used by AI agents, while its recommendations remain deterministic and auditable.
This is stronger for enterprise and DBA use cases than a generic RAG chatbot,
because every primary finding still has a rule id, tier, and explicit
preconditions.

The tradeoff is that ClickAdvisor will not generate fully free-form natural
language advice through an internal model. Educational output must come from
curated `explain_template` fields, rule metadata, retrieval snippets, and report
formatting. That is acceptable for the MVP because correctness is more important
than stylistic variation.

## Alternatives Considered

### Keep the three LLM modes as planned

Rejected because the modes were documented but not implemented. Keeping them
would preserve exactly the kind of claim/code mismatch that weakens technical
review.

### Add a quick Anthropic or Ollama wrapper

Rejected because it would add complexity without solving the core evaluation
problem. The project needs stronger datasets, baselines, and classifier
experiments before it needs generated prose.

### Remove all AI-agent integration

Rejected because MCP is valuable and already implemented. The right boundary is
not “no AI tools”; it is “no generative model changes the trusted analysis
result.”

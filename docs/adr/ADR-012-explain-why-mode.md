# ADR-012: Educational `explain` Mode

## Status

Accepted

## Context

Customer development surfaced a second use case that is adjacent to diagnosis
but not identical to it. In one scenario, a DBA wants the tool to tell them
what is wrong with a query and what to change. In another, the DBA already has a
working intuition about the fix but needs help explaining that intuition to a
developer, teammate, or reviewer who does not understand how ClickHouse behaves
internally. These are related workflows, but they optimize for different output.

Diagnostic output is action-oriented. It can be concise, recommendation-heavy,
and structured around “problem → fix → expected effect.” That is ideal when the
user already trusts the tool and simply wants to move quickly. Educational
output is different. It must explain the engine principle that makes the query
expensive or semantically awkward. It answers “why does ClickHouse behave this
way?” rather than only “what should I change?”

Without an explicit educational mode, the product risks underserving this use
case in both directions. If it always stays terse and fix-oriented, it becomes
less useful as a teaching aid. If it always expands every recommendation into a
mini-lesson, it slows down expert users who just want a crisp diagnosis. The
tool therefore needs a user-selectable output mode that changes the explanation
style without changing the underlying analysis logic.

This is also strategically valuable. ClickAdvisor is not only a remediation
engine; it can become a transfer-of-knowledge layer between DBA and developers.
That makes the product useful in query reviews, onboarding, internal education,
and postmortem discussions. Those contexts often reward explanation quality as
much as recommendation quality.

The project already has the raw ingredients for this direction. Tier 1 rule
cards contain statements, proofs, and examples. The knowledge base contains
engine documentation that can support richer explanations. What is missing is a
formal output mode that tells the system to prioritize principle explanation
instead of only patch-style advice.

## Decision

ClickAdvisor adds a CLI mode flag:

- `--mode=diagnose` — default
- `--mode=explain`

In `diagnose` mode, output remains concise and operational. The tool prioritizes
findings, rewrites, evidence, and expected improvement with minimal extra prose.

In `explain` mode, the tool produces educational output that explains the
ClickHouse principle behind the recommendation instead of only presenting the
fix. For example, rather than saying only “replace `COUNT(DISTINCT)` with
`uniqExact`,” the tool explains how ClickHouse executes distinct aggregation and
why the specialized aggregate is cheaper.

To support this mode, Tier 1 rule cards are extended with an
`explain_template` field. This field contains a compact, beginner-friendly
principle explanation that describes the relevant ClickHouse behavior in simple
language. The template is not a free-form marketing string; it is a structured
knowledge asset that can be rendered directly in CLI, Markdown, JSON, and MCP outputs. Retrieval snippets may add supporting documentation, but the core explanation remains curated and versionable.

## Consequences

The first consequence is output bifurcation with shared analysis. The tool now
has two user-facing modes, but they are intentionally built on the same rule
evaluation pipeline. That means a user can switch between “tell me what to do”
and “help me explain why” without receiving a different underlying diagnosis.
This is important for trust and consistency.

Another consequence is catalog enrichment. Rule authors now need to think not
only about proof and fix, but also about explanation. For Tier 1 especially,
that means expressing the engine principle in language a developer without deep
ClickHouse background can understand. This increases authoring effort, but it
creates durable educational assets that can be reused across CLI output, docs,
and future interfaces.

There is a UX consequence as well: users must be able to predict what kind of
output a mode change implies. `diagnose` should stay compact. `explain` should
be noticeably richer and more didactic. The difference must be large enough to
justify the extra mode rather than feeling like a trivial verbosity toggle.

The final consequence is strategic. This mode makes ClickAdvisor more useful in
human collaboration settings, not only in direct optimization tasks. A tool that
helps a DBA teach a developer why a query is costly can become sticky inside an
organization even before it is fully trusted as an automated fixer.

## Alternatives Considered

### Keep a single output mode with adjustable verbosity

This was rejected because verbosity alone does not capture the difference
between diagnosis and education. A longer diagnostic report is not the same as
an explanation of underlying ClickHouse behavior. The product needs a semantic
mode distinction, not just a text-length slider.

### Always emit educational explanations

This was rejected because it would slow down expert workflows and dilute the
product’s usefulness as a fast operational advisor. Many users want the shortest
path from finding to action. Making every run educational would punish the
default path for the sake of a secondary use case.

### Leave explanations to a generative LLM

This was rejected because it would make educational quality too dependent on model recall and too weakly anchored in curated rule knowledge. The system needs stored principle explanations in the catalog so that educational output remains consistent, versionable, and reviewable.

# ADR-006: Versioned Knowledge Base with Automatic Refresh

## Status

Accepted

## Context

ClickAdvisor needs a knowledge source that goes beyond static hand-written rule
descriptions. Even though the product’s core is not a retrieval chatbot, it
still benefits from having a structured body of ClickHouse-specific reference
material available for explanation support, contextual grounding, release-aware
behavior, and future model improvement workflows. Documentation in this domain
changes continuously: new ClickHouse versions add features, change defaults,
deprecate behaviors, and refine best practices. A knowledge base frozen at
project start would quickly drift away from the reality users are operating in.

The project also needs version awareness. Advice that is sensible for one
ClickHouse release may be irrelevant, unavailable, or even misleading in
another. If the knowledge base is going to contribute to explanations or future
retrieval-assisted workflows, each chunk needs metadata that makes version and
source traceable. Otherwise the system risks offering modern guidance to a user
running an older cluster or failing to distinguish between legacy and current
engine behavior.

There is a second reason to formalize the knowledge base early: feedback loops.
The CLI will eventually expose usage patterns, accepted/rejected advice signals,
and confusion points that can help improve both retrieval quality and LLM
behavior. If the project waits too long to define a structured knowledge layer,
it will lose the opportunity to connect real operator feedback to the materials
that informed an answer. A versioned KB creates a clean substrate for later
fine-tuning or retrieval refinement without turning the MVP into a data
collection product.

The source set matters as well. ClickHouse knowledge is distributed across
official docs, release notes, Altinity’s technical knowledge base, and the
ClickHouse blog. No single source captures all of the operational nuance the
product wants to reflect. The KB therefore needs a disciplined ingest process
rather than a one-time manual curation pass.

## Decision

ClickAdvisor will maintain a versioned knowledge base that is automatically
rebuilt by CI on a weekly cadence.

The initial upstream sources are:

- `docs.clickhouse.com`
- official ClickHouse release notes
- Altinity knowledge base material
- ClickHouse blog content relevant to engine behavior and optimization

The CI refresh process is responsible for collecting, normalizing, chunking, and
indexing content into a KB artifact suitable for retrieval and reference use.

Each chunk in the KB must carry, at minimum, the following metadata:

- `ch_version_introduced`
- `source`
- `last_updated`

Additional metadata may be added later, but these fields are mandatory because
they anchor version-aware reasoning and source traceability.

The KB is not the source of truth for formal rule validity. Rules remain defined
in the product’s own rule system. The knowledge base exists to support
explanations, contextual enrichment, retrieval-augmented advisory workflows, and
future model-improvement loops.

The CLI is expected to become part of a future feedback loop. User interactions,
accepted advice patterns, rejected suggestions, and confusion hotspots can later
inform KB prioritization, retrieval tuning, and eventual fine-tuning workflows.
This does not change the MVP into a training-data product today, but it fixes
the path by which real usage can improve the system.

## Consequences

The first consequence is freshness. A weekly CI rebuild means the project avoids
manual drift as ClickHouse evolves. That is especially important for versioned
features, changed planner behaviors, and new best-practice guidance that could
affect advisory explanations or support material.

The second consequence is traceability. Because each chunk includes source and
update metadata, future explanations can reference where a retrieved idea came
from and what version context it belongs to. This is important both for user
trust and for internal debugging when the system appears to cite stale or
unexpected guidance.

There is also an architectural benefit. By separating the KB from the formal
rule catalog, the project avoids conflating documentation retrieval with proof.
A documentation chunk can support an explanation or contextual suggestion, but
it does not automatically authorize a Tier 1 claim. This keeps the trust model
clean.

The feedback-loop implication is strategically important. If the CLI later
captures which outputs were useful, ignored, or confusing, the team will have a
structured way to connect those signals back to KB content and retrieval
behavior. That creates a credible path toward future fine-tuning or ranking
improvement based on real operator interaction rather than synthetic prompt
experiments.

The decision does create ongoing maintenance obligations. Source ingestion logic
must be resilient to upstream content changes, and weekly refreshes require
monitoring so the KB does not silently degrade. That is acceptable because stale
knowledge would be more damaging than the operational cost of keeping the
refresh pipeline healthy.

## Alternatives Considered

### Static manually maintained knowledge base

This was rejected because it would go stale quickly and would not scale with
ClickHouse release cadence or the diversity of relevant sources. Manual updates
would also make it harder to reason about freshness and provenance.

### No dedicated knowledge base

This was rejected because the product would lose a structured foundation for
explanation support, retrieval, and future learning loops. It would also force
documentation knowledge to remain trapped in human memory or scattered notes,
which is fragile and hard to evolve.

### Unversioned retrieval corpus

This was rejected because version-agnostic retrieval is particularly risky in a
fast-evolving engine ecosystem. Without chunk-level version metadata, the system
could not reliably distinguish guidance that applies only to newer or older
ClickHouse releases.

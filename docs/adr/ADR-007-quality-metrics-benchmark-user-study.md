# ADR-007: Quality Metrics as Precision/Recall Plus DBA User Study

## Status

Accepted

## Context

A product like ClickAdvisor needs a quality model that matches what it actually
does. Its purpose is not to be a benchmark harness for running rewritten queries
until one happens to be faster on a given setup. Its purpose is to identify the
type of optimization issue, recommend a better path with clear trust semantics,
and help operators arrive at a correct diagnosis faster. If the evaluation
metric does not reflect that mission, the product will optimize itself toward
the wrong behavior.

The most tempting metric in query-tuning products is average speedup. It is easy
to market, easy to summarize, and superficially intuitive. For this project,
however, it is deeply misleading. The measured runtime effect of a rewrite is
too dependent on environment, data distribution, cache warmth, and harness
choices to serve as the main quality objective. A system can look strong on a
small replay corpus while still giving untrustworthy advice in real environments.

The project needs two complementary evaluation lenses. First, it needs a
structured benchmark that measures whether the system correctly identifies the
problem class and routes the case toward the right recommendation family.
Second, it needs a human-centered measure of whether the tool actually helps a
DBA understand and resolve performance issues faster. A product can score well
on internal classification tasks and still fail to reduce operator effort if its
reports are confusing or its trust semantics are unclear.

A curated benchmark is especially important because ClickAdvisor’s rule catalog
and classifier will evolve incrementally. Without a fixed body of cases, it
would be difficult to distinguish real improvement from accidental drift. The
benchmark therefore has to be hand-curated, representative of meaningful
ClickHouse performance pathologies, and stable enough to support regression
tracking across iterations.

## Decision

ClickAdvisor’s primary quality metrics are:

- precision, recall, and F1 on problem-type detection over a curated benchmark
  of approximately 100 cases
- time-to-diagnosis in a user study involving DBA participants

The benchmark is intended to measure whether the system correctly identifies the
kind of issue present in a case and routes it toward the appropriate analytical
and recommendation path. The main reporting metric is F1 for detection quality,
supported by precision and recall to expose tradeoffs between over-triggering
and under-detection.

The user study is intended to measure practical usefulness. The primary human
metric is time-to-diagnosis: how quickly a DBA can arrive at a sound
understanding of the optimization issue and the likely remediation path when
using ClickAdvisor versus a baseline workflow.

Average speedup is explicitly not a primary product metric. It may appear in
research notes or illustrative case studies, but it is not the scoreboard by
which the product evaluates itself.

## Consequences

This decision aligns evaluation with the actual problem the product is trying to
solve. A good ClickAdvisor result is not merely “a query became faster in one
test.” It is “the system identified the right issue, expressed it with the right
confidence semantics, and helped the user get to the right diagnosis faster.”
Precision/recall and time-to-diagnosis reflect that mission directly.

The benchmark requirement will impose discipline on case curation. The team must
decide what constitutes a distinct problem type, how ground truth is represented,
and how edge cases are labeled. This is beneficial because it converts vague
claims of optimizer intelligence into concrete regression targets.

The user-study component forces attention to report usability and trust
communication. If the product identifies the right issue but buries it in noisy
or confusing output, time-to-diagnosis will not improve. That feedback is
important because the project’s differentiation depends not only on technical
correctness, but also on presenting different confidence tiers in a way that
operators can act on quickly.

Rejecting average speedup as the main metric also protects the team from chasing
benchmark theater. It reduces the temptation to overfit the system to a replay
environment or to cherry-pick examples where a rewritten query looks dramatic in
one execution setting. Instead, the team is pushed to improve diagnostic quality
and operator utility.

There is a tradeoff in communication. Investors, reviewers, or casual users may
still ask for a single performance number. The product will need a disciplined
explanation for why detection F1 and time-to-diagnosis are more credible and
more stable measures at this stage. That is acceptable because those metrics are
better aligned with the product’s real contract.

## Alternatives Considered

### Average speedup as the main KPI

This was rejected because runtime speedup is too environment-dependent to be a
trustworthy global metric for this product. It also incentivizes the wrong kind
of demo optimization and obscures whether the system actually diagnosed the
problem correctly.

### Pure offline classifier accuracy only

This was rejected because a strong offline benchmark score does not guarantee
that real DBA find the tool helpful. Without a user-study measure such as
time-to-diagnosis, the project would miss the human side of the value
proposition.

### User satisfaction surveys only

This was rejected because subjective satisfaction without benchmark grounding is
too soft to guide system evolution. The product needs both objective detection
metrics and operator-centered usability evidence.

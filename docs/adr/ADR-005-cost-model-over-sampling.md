# ADR-005: Cost-Model Evaluation Instead of Sample-Based Verification

## Status

Accepted

## Context

A query advisor needs a way to estimate whether a recommendation is beneficial.
The most obvious instinct is to execute the original query and the rewritten
query, measure runtimes, and report a speedup. That approach is attractive in a
demo because numbers look concrete. In practice, for the environments
ClickAdvisor targets, it is often the wrong measurement model.

The first problem is realism. Enterprise ClickHouse workloads are shaped by data
distribution, storage layout, cache state, cluster topology, settings, and table
growth over time. Replaying a query in a local sandbox or benchmark harness
rarely reproduces those conditions faithfully. Even if it were technically
possible to run both variants, the observed difference would be sensitive to the
test environment in ways that are hard to normalize. This makes “measured
speedup” sound more authoritative than it actually is.

The second problem is compliance and access. ClickAdvisor is designed to avoid
touching customer data directly. If evaluation required copying or replaying
production-scale data into a sandbox, the product would immediately violate the
operational simplicity and compliance posture it is supposed to support. A
full-fidelity replay environment is not just difficult to build; in many cases
it is organizationally impossible.

A weaker alternative is sample-based verification: run the queries on a reduced
dataset or sample table and use the results as a proxy. That also breaks down in
the ClickHouse context. Plans and cardinality behavior can change materially when
data is sampled or reshaped. A sample that is convenient to move around may no
longer preserve the distributional properties that determined the original read
pattern, pruning effectiveness, or aggregation cost. This is especially
problematic for a columnar engine where layout-sensitive effects matter.

The project already has a more defensible source of evidence available: the
database’s own planning and metadata surfaces. `EXPLAIN ESTIMATE` exposes the
planner’s view of expected work without requiring `ANALYZE`, and `system.parts`
provides storage-level facts relevant to cost reasoning. These are not perfect
predictors of runtime, but they are aligned with the actual engine’s internal
model and avoid the false precision of contrived replay metrics.

## Decision

ClickAdvisor will not execute queries for the purpose of measuring optimization
speedup.

Instead, it will estimate recommendation value through a cost-model-oriented
approach grounded in:

- `EXPLAIN ESTIMATE`
- `system.parts`
- schema and storage metadata
- relevant settings and hardware characteristics

The principal outcome metric attached to a recommendation is estimated cost
reduction according to the database-oriented cost model, not measured runtime
speedup from query replay.

This applies both to product behavior and to evaluation framing. The system is
allowed to say that a recommendation is estimated to reduce read volume, improve
pruning, or reduce expected work according to planner and metadata evidence. It
is not allowed to claim a concrete speedup percentage derived from contrived or
partial replay unless a separate, explicit validation setup exists outside the
core product.

Sample-based verification is also rejected as a primary mechanism. Sampled
execution may be used in isolated research contexts, but it is not part of the
MVP product contract and must not be treated as authoritative evidence for user
facing recommendations.

## Consequences

This decision keeps the product aligned with its zero-data-egress and
local-first posture. Users can supply SQL, plans, metadata, and configuration
context without needing to provision replay datasets or grant execution access
for optimizer benchmarking. That substantially lowers operational friction and
makes the tool more plausible for enterprise use.

The decision also improves epistemic honesty. Estimated cost reduction is not a
weaker story than measured speedup in this context; it is often the more honest
one. The product is explicit that it is reasoning from planner and metadata
signals rather than pretending that a laboratory run on a sampled or synthetic
dataset proves production benefit.

For implementation, this choice concentrates effort on richer metadata modeling
instead of on benchmark orchestration. The team can invest in understanding
`EXPLAIN ESTIMATE`, `system.parts`, settings, and storage-level indicators. That
is more aligned with the product’s differentiator than building a replay
framework that still would not mirror real enterprise environments.

There is a communication cost. Some users may initially expect a single “your
query will be 3.2x faster” number because that framing is common in tuning
marketing. The product must resist that temptation and educate users that the
advisor reports estimated reductions in expected work rather than synthetic
runtime claims.

Another consequence is that evaluation discipline moves to benchmark design and
precision/recall rather than to live execution theater. That is a positive
constraint because it encourages reproducibility and clearer reasoning about why
a recommendation is considered good.

## Alternatives Considered

### Full sandbox replay

This was rejected as unrealistic for the target environments. It would require
moving or reconstructing enterprise-scale data, reproducing production-like
settings and topology, and accepting significant compliance overhead. Even then,
the resulting measurements could still diverge materially from the user’s real
environment.

### Sample-based verification

This was rejected because sampled data often changes the very planner and
cardinality properties that determine optimization behavior. A query that looks
cheaper on a sample may not remain cheaper against the real distribution, and
vice versa. Using sample execution as the main truth metric would create false
confidence and conflict with the product’s emphasis on trustworthy guidance.

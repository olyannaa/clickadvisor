---
source: blog
url: https://launchdarkly.com/
topic: how-clickhouse-cloud-enabled-launchdarkly-to-build-and-ship-features-faster
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 8
---

as needs evolve. ## Unlocking new features and capabilities [\#](/blog/launch-darkly#unlocking-new-features-and-capabilities) ClickHouse has changed the way LaunchDarkly builds, both in terms of the individual features the team can deliver and how it thinks about data as a product foundation.

One of the early breakthroughs, Joe says, was seeing “how well ClickHouse handles high\-cardinality data.” Earlier systems forced the team to limit dimensionality. Pushing large volumes of distinct values into relational databases wasn’t practical, so features had to be simplified or avoided entirely. With ClickHouse, that constraint disappeared. “We could suddenly support far more dimensions and much finer granularity without performance issues.”

That shift unlocked “features we simply couldn’t have built before,” including richer filtering, arbitrary dimensions for evaluations, autocomplete powered by distinct attribute discovery, and LaunchDarkly’s new audience feature, which identifies who saw which flag and when at a per\-user level. “That level of detail was out of reach in other databases,” Joe adds.

Today, LaunchDarkly has seven features running in production on ClickHouse, including its entire Observability offering and major parts of its Product Analytics capabilities. Several more are in active development or prototyping, and ClickHouse now underpins a significant portion of LaunchDarkly’s analytics and data\-driven product functionality. “At this point, nearly any analytics component in the UI that involves time\-series or evaluating behavior over time is backed by ClickHouse,” Joe says.

Importantly, all of those datasets now live together. By storing feature flag evaluations, product analytics, and observability signals in the same system, LaunchDarkly can correlate them directly, paving the way for workflows like regression detection and automatic rollbacks. “This aligns strongly with the broader vision of putting product analytics, observability, and warehouse\-style data in one place so teams can reason across them,” Joe says.

## Learnings (or unlearnings) along the way [\#](/blog/launch-darkly#learnings-or-unlearnings-along-the-way)

One of the team’s biggest lessons has been the importance of getting schema design right early. In their first months with ClickHouse, they made decisions based on assumptions that later proved incorrect. “For example, we tried to coarsen our ORDER BY keys because we thought high granularity would hurt performance,” Matt says. “Later, we learned that ClickHouse is perfectly happy ordering by full timestamps.” By the time that became clear, adoption had grown quickly enough that changing schemas was no longer trivial.

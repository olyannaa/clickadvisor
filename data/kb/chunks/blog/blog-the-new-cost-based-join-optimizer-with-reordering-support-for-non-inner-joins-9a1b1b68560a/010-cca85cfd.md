---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"The
topic: the-new-cost-based-join-optimizer-with-reordering-support-for-non-inner-joins-clickhouse
ch_version_introduced: '10.1145'
last_updated: '2026-11-09'
chunk_index: 10
total_chunks_in_doc: 14
---

is what makes the detector complete: it rejects a plan only when a conflict actually applies to it. The validity test is applied every time the enumerator considers joining a set of tables S₁ with a set S₂:

```
1required_left ⊆ S₁  ∧  required_right ⊆ S₂   (or mirrored, with LEFT ↔ RIGHT)
2∧  every conflict rule of the operator is obeyed by S₁ ∪ S₂
```
Copy command
If the test passes, the operator applied at that split decides the kind and strictness of the resulting join. The test is a few bitmask operations, so it adds almost nothing to the enumeration.

### Fitting it into DPsub \#

DPsub enumerates subsets of tables as bitmasks and, for every subset, finds the cheapest way to build it from two smaller connected subsets. With the detector in place, the whole join tree reaches DPsub as one graph of tables: both sides of every outer, semi and anti join, and `FULL` joins too. A few more pieces were needed:

- **Cross products.** A `CROSS JOIN` joins on nothing, so it adds no edge to the graph. We link its two sides explicitly, as a join of selectivity 1, so the graph stays connected and DPsub can move the cross product to wherever it is cheapest, while it is still executed and reported as a `CROSS JOIN`.
- **The build side.** DPsub's cost model charges a join the same whichever way round its inputs go, so after the search we put the smaller input on the build side of the hash join, mirroring outer joins `LEFT` ↔ `RIGHT`, but never for `ANY`, `SEMI` and `ANTI` joins, whose meaning depends on the side.
- **Bounded search.** DPsub with the detector plans join trees of up to 12 tables, semi, anti and outer joins included. A larger join tree is left to the greedy optimizer.

## Validation I: against the theory \#

A detector that is wrong even once returns wrong results, so we validated it the way the paper does. For a given number of tables *n*, a harness:

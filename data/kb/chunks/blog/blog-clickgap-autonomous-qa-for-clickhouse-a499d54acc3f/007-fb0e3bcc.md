---
source: blog
url: 'https://schema.org","@type":"BlogPosting","headline":"ClickGap:'
topic: clickgap-autonomous-qa-for-clickhouse-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 7
total_chunks_in_doc: 15
---

The list grows from evidence. A separate process has analyzed nearly 2000 confirmed ClickHouse bugs and converted their lessons into memories for future reviews. When a bug matches no existing pattern, the system drafts a new checklist entry.

**Third, coverage gaps are measured rather than inferred.** LLVM line coverage identifies the exact changed lines that no test executes. Even then, an uncovered line counts only if the analyst can name a mutation that the proposed test would kill and explain the user\-visible risk.

**Fourth, economics favors breadth.** Hypotheses are cheap, a complete review costs a couple of dollars in model usage, and local validation takes minutes. The analyst can explore many candidates for each pull request and retain only those whose executed tests disagree with expected behavior. Every review also begins with roughly thirty recalled lessons from prior findings.

Detection itself is continuously tested. The benchmark starts with real bugs that ClickGap previously found and maintainers confirmed. For each one, the repository is rewound to the moment the reviewed pull request merged, while the defect was still present, and the analyst reviews that state again from scratch. The question is binary: does it rediscover the bug?

Every proposed efficiency change, such as shortening the prompt, runs against the same corpus under both the old and new configurations. If the cheaper configuration misses bugs the existing one catches, it does not ship.

## Cheap on purpose, measured for it \#

A couple of dollars per pull request reviewed. The recall benchmark above is its guardrail: a cost reduction that weakens bug detection does not ship. A cheap reviewer that catches nothing is not efficient; it is merely lower\-cost noise. Within that constraint, savings come from four places.

**Plain code consumes no model time.** Work with an exact contract runs as ordinary code: repairing issue bodies to match the upstream template, detecting duplicate filings by comparing files and overlapping titles against ClickGap’s history, and rendering the self\-review checklist. These operations cost no tokens and cannot drift.

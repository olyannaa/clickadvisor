---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Meet
topic: meet-groeneai-our-autonomous-contributor-to-clickhouse-clickhouse
ch_version_introduced: auto
last_updated: '2026-11-02'
chunk_index: 7
total_chunks_in_doc: 16
---

checks the source and existing fixes, and writes an approach with a reproduction procedure. A separate model reviews the plan. Work can stop here if the report is a duplicate, cannot be reproduced, or needs a maintainer's decision.

An implementation worker then makes the change in the task's checkout. Its instructions require evidence that the regression test fails without the patch and passes with it. If the plan's assumptions do not hold, the worker records what it ran and returns the task to planning.

A fresh review session examines the code before it reads the implementer's validation narrative. It must inspect the changed functions, their callers, and related implementations, then compare the tests with the proposed pull request description. GroeneAI uses Claude for its main worker sessions and Codex for separate reviews of the approach and the resulting change. The reviewer builds its own explanation of the patch and compares it with the implementation evidence. An accepted substantive finding becomes a correction for implementation. A disputed finding needs code or test evidence that explains the disagreement.

The workflow also checks which revision was reviewed. The ordinary pre\-push path requires a completed second\-model review recorded against the proposed commit, tree, or complete patch identity. Findings still require adjudication, and a review of an earlier version must not silently authorize a later code change.

## August: the process at work \#

Two changes from August show that process at work, beginning to truly shine autonomously. The first is a planner optimization that GroeneAI had to prove safe before a maintainer would merge it, and the second repairs a CI report that engineers read when they judge somebody else's change.

Let’s see how the robot did:

### The first, making UNION DISTINCT use parallel work \#

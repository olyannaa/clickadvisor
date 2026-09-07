---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"The
topic: the-future-of-observability-won-t-be-one-proprietary-ai-agent-it-will-be-thousands-built-by-teams-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 8
---

flexibility that there's an opportunity for us to build on top of that. As long as it works with enough of our internal tooling, that's the sweet spot." > > > > > Sushant Hiray, AI Leader, RingCentral

The most successful observability platforms will not be the ones that force everyone into a single way of working. They will be the ones that provide a shared foundation upon which thousands of different agents can be built.

## Agents need shared context \#

If every team or even individual builds and adapts their own agents, investigations will not happen in one place. One engineer may start in an IDE, another in a notebook, another in an internal chat interface, and another through a custom incident workflow. Agents may run in different harnesses, use different models, and follow different investigation paths, even when they are all trying to understand the same production issue.

This creates a collaboration problem. Investigation output cannot remain trapped inside transient chat sessions or private agent traces. Teams need durable, inspectable artifacts that show what was queried, what evidence was found, which hypotheses were explored, and why a conclusion was reached. This matters for humans reviewing an incident, but it also matters for future agents that need to learn from previous investigations instead of starting from scratch every time.

Loading video...As a result, agentic observability will require some form of persistent investigation surface where humans and agents can collaborate. A place where investigations can be shared, reviewed, rerun, refined, and built upon over time. Whether an investigation begins in an IDE, a notebook, a chat interface, or a custom workflow is ultimately less important than having a common place where the results can be preserved and reused.

These investigation artifacts become more than a record of what happened. They become a growing body of operational knowledge that future engineers and future agents can draw upon when similar problems arise.

## Humans will still be the control plane \#

All of this assumes that humans remain in the control plane, at least for now.

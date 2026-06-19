---
source: blog
url: https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog
topic: clickhouse-at-the-nyc-ai-agents-hackathon-building-agentic-ai-on-real-time-data
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 6
---

large share of them chose ClickHouse as their real‑time backbone. ![1.jpg](/uploads/1_105ae81507.jpg) ![2.jpg](/uploads/2_92880a2537.jpg) ### Get started today Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
### **First Place \- VitalSignal** [\#](/blog/nyc-ai-agents-hackathon#first-place---vitalsignal)

**What they built**

**VitalSignal** is an autonomous AI agent that delivers **personalized global disease outbreak alerts**. It continuously monitors health‑related signals, runs multi‑factor risk analysis by region and user profile, and pushes timely, tailored alerts to people who might be affected.

The core problem: in a world of constant health crises, it’s hard to know **what matters to you and your loved ones** until it’s already mainstream news, often too late.

**How it works**

ClickHouse sits at the **center of the architecture**, storing:

- User profiles and preferences
- Scraped and streamed JSON alerts
- Metadata from other tools (e.g., images and structured outputs)
- Sponsor tools like **Airia**, **Structify**, and **PhenoML** help extract and structure signals before they land in ClickHouse.
- An autonomous agent layer continuously evaluates new events, calculates risk scores, and triggers notifications.

Because ClickHouse can ingest diverse data types and query them in real time, the builder could experiment quickly without worrying about infrastructure limits.

**Inspiration**

The idea came from a mix of the hackathon prompt and a deeply personal frustration:

“I have family in different parts of the world and often find out about health crises in their area only once it hits mainstream news. I wanted an agent that makes this information accessible sooner, in a way that’s actually personalized.”

Health as a “live data source that’s critically important but overwhelming” turned out to be the perfect canvas for an agentic build.

**Build approach**

The VitalSignal creator treated the hackathon like a deployment day, not a brainstorming session:

**Decisions first, hacking second**:

- Chose ClickHouse as the database early.
- Pre‑created accounts and API keys for sponsor tools.

**Docs‑driven development**:

- Used an LLM for a quick overview of each tool.
- Relied on official docs for actual implementation details.

**Stable core, then integrations**:

- Built the simplest end‑to‑end workflow first.
- Iteratively layered in more tools and features once the base was solid.

**The hardest part (and how they solved it)**

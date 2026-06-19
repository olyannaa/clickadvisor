---
source: blog
url: https://seemplicity.io/
topic: how-seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 5
---

# How Seemplicity scaled real\-time security analytics with Postgres CDC and ClickHouse

\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Seemplicity scaled real\-time security analytics with Postgres CDC and ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 29, 2025 · 8 minutes readToday’s security teams face a paradox: more tools, more data, and yet less clarity. With dozens of scanners, posture managers, and alerting systems in play, the average enterprise team spends more time triaging findings than actually fixing them.

[Seemplicity](https://seemplicity.io/) solves this by acting as the nerve center for remediation. As the industry’s leading RemOps platform, it aggregates findings from over 150 tools—spanning application security, cloud security, vulnerability management, pen testing, and more—and enriches them with internal business context and threat intelligence to help teams take action faster.

“Instead of getting alerts and vulnerabilities from different tools and manually tracking them in spreadsheets or emails, Seemplicity ingests all security findings into a centralized transactional system and then leverages Postgres CDC to seamlessly replicate data into ClickHouse for high\-performance analytics,” says Chief Architect Tal Shargal. “This allows us to quickly prioritize vulnerabilities and automatically generate actionable tasks for the right teams. You can think of it as a smart security workflow platform powered by rapid analytics.”

But scaling always brings challenges. As Seemplicity grew and onboarded larger customers, the limits of its architecture became clear. Postgres couldn’t keep up with the volume of incoming data or the performance demands of their customer\-facing dashboards. The team needed a new foundation—something fast, reliable, and made for real\-time analytics at scale.

We caught up with Tal to hear how Seemplicity rebuilt its backend with [ClickHouse Cloud](https://clickhouse.com/cloud) and PeerDB (now part of [ClickPipes](https://clickhouse.com/cloud/clickpipes)), why visibility matters just as much as speed, and how moving to a modern data stack helped the team grow without losing control.

## Hitting the Postgres bottleneck (and why CDC matters) [\#](/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse#hitting-the-postgres-bottleneck-and-why-cdc-matters)

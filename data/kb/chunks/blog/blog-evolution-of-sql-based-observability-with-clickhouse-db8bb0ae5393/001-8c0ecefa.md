---
source: blog
url: https://clickhouse.com/blog/the-state-of-sql-based-observability
topic: the-evolution-of-sql-based-observability
ch_version_introduced: '40.77'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 18
---

# The evolution of SQL\-based observability

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The evolution of SQL\-based observability

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid) and [Ryadh Dahimene](/authors/ryadh-dahimene)Nov 11, 2024 · 32 minutes read## Introduction [\#](/blog/evolution-of-sql-based-observability-with-clickhouse#introduction)

Almost one year ago, we blogged about the [state of SQL\-based observability](https://clickhouse.com/blog/the-state-of-sql-based-observability), exploring two parallel backgrounds of two established paradigms: SQL and observability. We explained how they had collided and together created a new array of opportunities in the field of observability while attempting to answer "When is SQL\-based observability applicable to my use case?" This blog post garnered significant attention and has proved useful in discussing ClickHouse and its role within the observability space to new users.

Although the general themes of the original blog post remain true, a year is a long time in ClickHouse development! As well as multiple new features which we believe will further move ClickHouse to the position as the de\-facto database for observability data, the eco\-system surrounding ClickHouse has matured, simplifying the adoption for new users.

In this post, we'll explore some of these new features as well as give a glimpse into some experimental work which we hope will form the basis for ClickHouse's use in the less explored pillar of metrics within observability.

## The state of SQL\-based observability in 2023 [\#](/blog/evolution-of-sql-based-observability-with-clickhouse#the-state-of-sql-based-observability-in-2023)

Our original post proposed that observability is just another data problem, to which SQL and [OLAP based systems](https://clickhouse.com/engineering-resources/oltp-vs-olap), such as ClickHouse, are well suited to addressing. We explored the history of centralized logging, and how solutions such as Splunk and the ELK stack had emerged from the both syslog and NoSQL era. Despite the popularization of the former, SQL’s unique strengths have sustained its relevance, making it the [third most widely adopted language](https://survey.stackoverflow.co/2023/#most-popular-technologies-language-prof) for structured data management, even amidst the NoSQL boom.

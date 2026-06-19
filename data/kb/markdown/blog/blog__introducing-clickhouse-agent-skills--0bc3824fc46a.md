# Introducing ClickHouse Agent Skills


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing ClickHouse Agent Skills

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U09_LQAXRNKS_74b24858f49d_512_b30a5f8faf.jpeg&w=96&q=75)[Al Brown](/authors/al-brown) and [Doneyli De Jesus](/authors/doneyli-de-jesus)Feb 5, 2026 · 3 minutes readWe’re releasing the official [ClickHouse Agent Skills](https://github.com/ClickHouse/agent-skills): a set of open\-source, packaged skills encoded with ClickHouse best practices learned by our engineers and community.


These skills provide your AI assistant with 28 prioritized rules for schema design, query optimization, and data ingestion. It helps your agent go from a general\-purpose LLM to a ClickHouse power user.


[The repo is open and Apache licensed for everyone to contribute to](https://github.com/ClickHouse/agent-skills), so if you've got some hard\-won lessons about how to best use ClickHouse, we'd love for you to share.

Loading video...## Get started [\#](/blog/introducing-clickhouse-agent-skills#get-started)


You can add these skills to your local environment in seconds:



```
npx skills add clickhouse/agent-skills

```

The CLI will detect which agentic interfaces you have installed and drop the instructions in the right place.


Agents that support skills should start to use them automatically when appropriate, but you can also manually invoke them (for example, in Claude Code, you can use `/clickhouse-best-practices`).


## Why we built this [\#](/blog/introducing-clickhouse-agent-skills#why-we-built-this)


LLMs are a great accelerator, and we believe that they are only going to become more common in developer workflows as we build towards [agentic analytics](https://clickhouse.com/blog/agent-facing-analytics). But, they don't (yet?) always get specialised systems like ClickHouse exactly right.


We’ve seen some developers hit walls when LLMs make functional, but less\-than\-perfect, choices:


- Choosing the wrong ORDER BY or data types.
- Writing JOINs that don't scale or failing to batch inserts.
- Missing out on Materialized Views or specialized indexes.


These choices can lead to friction later down the line when you reach production, or need to scale. We want to support developers using AI, and while our docs contain a wealth of information on how to do these things correctly, LLMs don’t always find the right information at the right time.


## What’s in the box? [\#](/blog/introducing-clickhouse-agent-skills#whats-in-the-box)


We’ve built these skills using the [Agent Skills](https://agentskills.io/) specification recently released by Anthropic. It’s a lightweight, agent\-agnostic format that allows us to encode deep domain knowledge into a format that LLMs can invoke when they actually need it.


The initial release focuses on the high\-impact best practices that are relevant to almost all ClickHouse users:


- **Schema design**
	- Primary Key selection
	- Data Types
- **Query performance**
	- JOIN optimization
	- Mutation avoidance
- **Data ingestion**
	- Insert batching
	- Async inserts
- **Advanced tools**
	- Materialized Views
	- Partitioning strategies


## What's next? [\#](/blog/introducing-clickhouse-agent-skills#whats-next)


This is just the start. We’re going to keep expanding this with deeper knowledge on cluster configurations, engine\-specific optimizations, complex data pipeline patterns, and more.


Check out the [repo](https://github.com/ClickHouse/agent-skills) and [join us in Slack](http://clickhouse.com/slack) to let us know what rules we should add next.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

# Intelligent security at ClickHouse speed: How Cogent Security built an AI\-native vulnerability management platform


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Intelligent security at ClickHouse speed: How Cogent Security built an AI\-native vulnerability management platform

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 24, 2026 · 12 minutes read## Summary

Cogent Security uses ClickHouse to serve billions of security findings at sub\-second speeds, powering an AI\-native vulnerability management platform. Migrating from Postgres to ClickHouse reduced P90 query latency from 5 seconds to less than 1 second at 100 million rows, without caching. Cogent's Chart Agent went from 40% to 94% accuracy by combining an agentic loop architecture with ClickHouse projections.

As AI makes it faster and easier to exploit software vulnerabilities, enterprise security teams are falling behind, hamstrung by point solutions that are often hard to deploy and clunky to use.


"Our goal is to make sure enterprises are able to keep up as the threat landscape changes rapidly with AI," says [Cogent Security](https://www.cogent.com/) founding engineer Karan Gugle.


Just six months since the platform's launch, Karan says two things are already clear: enterprises are understaffed and dealing with millions or even hundreds of millions of findings; and the road to actually remediating these findings requires a huge amount of organizational context and a deep understanding of the systems on which they were found.


"Users need to filter through their findings, ask questions about their data, and start remediating their risk—all actions that need to feel instant, accurate, and magical on Cogent's platform to really stand out," Karan says. "This applies even more to agents, who crunch massive amounts of data for users who may be hunting for the latest threats in their environment, generating compliance reports, or remediating a vulnerability on their most critical assets."


At a March 2026 ClickHouse meetup in San Francisco, Karan and machine learning engineer Sagar Maheshwari shared how Cogent built its data platform on ClickHouse, and what that unlocks for agentic vulnerability management.


## The growing threat gap [\#](/blog/cogent-security#the-growing-threat-gap)


The vulnerability management problem is getting measurably worse. The National Vulnerability Database currently tracks over 320,000 CVEs, a figure that has grown fivefold in just the last decade. And with the rise of LLM\-powered toolkits, the threat is accelerating in a new way.


"The floor of knowledge required to try to exploit has gone from a seasoned systems engineer to anyone with intent and access to a coding agent," Karan says.


The numbers bear this out. In 2018, the mean time\-to\-exploit (TTE)—the window between a vulnerability being disclosed and being actively exploited—was around 2\.3 years. In 2026, that number has collapsed to just 1\.6 days.


![](/uploads/cogentsecurity_mar2026_image1_dcb11c08b5.png)
*Since 2018, mean time\-to\-exploit (TTE) has dropped from 2\.3 years to 1\.6 days.*


On the defender side, security teams are chronically understaffed, while the "scan → contextualize → prioritize → remediate" loop is slow, manual, and full of friction. Most teams are nowhere near meeting their own internal SLAs, and 50% of the most critical vulnerabilities remain unresolved after two months. "That's a pretty scary reality," Karan says.


Once a vulnerability is found, remediation—communicating to engineering why it matters and finding the right owners to actually fix it—is, as Karan puts it, like "walking a tightrope," an organizational and process challenge as much as a technical one.


"Everything in this loop needs to be done at machine speed to counter AI\-enabled attackers," he says. "That's exactly what we're trying to solve."


## Security data at scale [\#](/blog/cogent-security#security-data-at-scale)


Fortune 500 customers can generate more than 10 billion data points in just 90 days, with up to 100 million changelog events per day. To serve that data reliably across charts, filters, agent queries, and backend APIs, Cogent gives each customer their own [ClickHouse](https://clickhouse.com/resources/engineering/what-is-columnar-database) database with over 100 tables optimized for different product surfaces.


Data arrives from over 50 sources, including cloud providers, vulnerability scanners, and business tools like Slack, Confluence, and Jira. Because these sources are disconnected, Cogent's platform first performs entity resolution, finding the right join keys between a customer's data sources to produce a unified view of their environment. The result is a Knowledge Graph that enables graph\-like traversals across the data.


From there, dbt projects denormalized tables into [Iceberg](https://clickhouse.com/resources/engineering/apache-iceberg)—pre\-joined, pre\-aggregated views of the Knowledge Graph. Those projections are then loaded into ClickHouse via the [ClickHouse Spark Connector](https://clickhouse.com/docs/integrations/apache-spark/spark-native-connector), which provides cheap, tunable, and highly scalable compute for the load path. All table schema and layout decisions are defined using the ClickHouse dbt library.


![](/uploads/cogentsecurity_mar2026_image2_5f4b32e866.png)
*Cogent's data pipeline, from ingestion through to the ClickHouse\-powered serving layer.*


"This is great because we can co\-locate the Iceberg dbt transformation pipelines with the ClickHouse optimizations we need," Karan explains. "For example, setting up the right indexes, ClickHouse projections, compression types, and so on." The result is a clean hot/cold [data lakehouse](https://clickhouse.com/resources/engineering/data-lakehouse) architecture with Iceberg on S3 as the source of truth, and ClickHouse as the serving engine.


## Designing for speed [\#](/blog/cogent-security#designing-for-speed)


Before presenting results, Karan shared the five design principles that underpin Cogent's approach to making reads fast at scale.


The first is query\-driven design. "This is probably the single biggest mindset shift coming from a traditional relational world," he says. "You don't start with your entity model. You start with the queries your product needs to run, and you design your tables backwards from there."


The second principle is to [denormalize everything](https://clickhouse.com/docs/data-modeling/denormalization). Cogent's dbt projections pre\-join and pre\-aggregate data before it reaches ClickHouse, eliminating expensive JOIN operations at query time.


Third is the use of [projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection) and [indexes](https://clickhouse.com/docs/primary-indexes). "This is one of ClickHouse's superpowers," Karan says. "You're essentially trading minor insert amplification and additional storage for dramatically better filter performance." Every projection is an additional physical sort order on the same data, enabling completely different query patterns to be served from a single table.


Fourth is choosing the right [compression codec](https://clickhouse.com/docs/data-compression/compression-in-clickhouse) for each column type—Delta for timestamps, LZ4 for strings, ZSTD for cold data—to reduce read I/O and storage footprint.


Finally, [benchmark everything](https://clickhouse.com/resources/engineering/clickhouse-query-optimisation-definitive-guide). "[system.query\_log](https://clickhouse.com/docs/operations/system-tables/query_log) is your friend," Karan says.


## Sub\-second performance [\#](/blog/cogent-security#sub-second-performance)


The gap between Cogent's old Postgres\-based setup and where they are now shows what the right infrastructure can do for a product where speed is a massive differentiator.


"I want to underscore how important this is—not just as a benchmark exercise, but to our product and customers," Karan says. "Security tools routinely crumble under this kind of load. When you're a security engineer trying to triage millions of findings across your org, the last thing you need is a 25\-second page load."




|  | P50 | P90 | P99 |
| --- | --- | --- | --- |
| Postgres | 2 seconds | 5 seconds | 25 seconds |
| ClickHouse (100M rows) | 0\.3 seconds | 0\.9 seconds | 2\.5 seconds |
| ClickHouse (500M rows) | 0\.6 seconds | 1\.8 seconds | 4\.2 seconds |
| Goal | 0\.5s | 1s | 3s |


Today, 98\.7% of queries complete in under three seconds at 100 million rows, while 86\.3% do so at 500 million rows. And as Karan adds, "That's without any sort of backend or even database\-level caching."


## Making reporting conversational [\#](/blog/cogent-security#making-reporting-conversational)


With the infra story told, Sagar took the mic to walk through what Cogent built on top of it.


"Almost every customer we work with needs charts and dashboards to monitor current and historical risk posture," he says, "whether it's for GRC, board presentations, SLA tracking, day\-to\-day observability, you name it." Traditionally, meeting those needs has meant exporting CSVs from data silos, manually configuring BI tools, and scrambling to pull data together before meetings. That's days of analyst time for what should be a quick answer.


Cogent's approach is to make reporting conversational. Their Chart Agent takes a natural language request and generates the ClickHouse SQL needed to render a chart, querying Change Data Capture logs in [real time](https://clickhouse.com/resources/engineering/what-is-real-time-analytics). "If you can say what you want, we can create the chart," Sagar says. "Overall, we want reporting to be possible in seconds, not days, all without sacrificing accuracy."


The first version used a single\-shot approach—stuff all context into the system prompt, send the user request, and, as Sagar puts it, "pray we get the right SQL back." On a golden dataset of around 100 text\-to\-SQL examples, this achieved 40% accuracy. The failure modes were clear: without the ability to run queries to validate its assumptions, the LLM "confidently writes incorrect SQL" and also gets distracted by irrelevant context.


The solution was an agentic loop with three key components: agentic RAG to search the data model and pull relevant context on demand; a live SQL execution tool to run queries directly against ClickHouse and see actual data; and interleaved thinking to reason between tool calls rather than planning everything upfront and becoming obstinate when intermediate results suggested a different approach. The result: 94% accuracy on the same dataset where single\-shot got 40%.


## Iterating toward accuracy [\#](/blog/cogent-security#iterating-toward-accuracy)


Since the Chart Agent's SQL is non\-deterministic, evaluation is tricky but not impossible. Cogent uses two complementary evaluation approaches. Trace evaluations use an LLM\-as\-a\-judge to assess whether the agent behaved correctly—pulling relevant schemas, running intermediate queries, validating SQL.


SQL output validation is the harder eval. Given the same dataset, it checks whether the agent's generated SQL produces the same data output as the expected SQL. Cogent evaluates data output equality rather than SQL string equivalence, using a small language model to map expected columns to generated columns. And each test case runs three times with majority voting. "It's not enough to get it right once," Sagar says. "It needs to be consistent."


When it came time to iterate, adding tools to dynamically explore the data model and run queries—the first agentic version—pushed accuracy to 58%. A curated query bank of golden SQL patterns brought it to 75%, freeing the agent to anchor on proven patterns rather than devising query logic from scratch. A tenant memory bank, letting the agent reference lessons from past runs, took it to 82%.


The most notable jump came not from changes to the agent, but from the data. "Rather than force the agent to construct these from scratch each time, we created pre\-computed aggregations in ClickHouse, which we call projections," Sagar explains. "Just by simplifying the queries the agent had to write, we saw the accuracy jump to 94%."


## One source of truth [\#](/blog/cogent-security#one-source-of-truth)


Underpinning all of this is a piece of infrastructure Cogent built in\-house: the Ontology Service.


"When the data model changes, the agent hits a 'WTF' moment because it's confused by discrepancies between its context and the actual data," Sagar says. The Ontology Service solves this by co\-locating the data model and its semantics—descriptions, enums, relationships—directly with the physical schema. As Sagar puts it, "One source of truth, no drift."


Enterprise security adds another layer of complexity. "Customers always have unique environments," Sagar explains. "Without an ontology service, the agent has a really tough time trying to understand custom fields and their semantics." Per\-tenant overlays in the Ontology Service ensure agents automatically see each customer's full effective schema.


"Making the data model agent\-friendly is a new paradigm," Sagar says, "that I think will shift how the industry thinks about data modeling going forward."


## A virtuous cycle [\#](/blog/cogent-security#a-virtuous-cycle)


"The key thing that ClickHouse unlocks for AI is speed," Karan says.


At Cogent, that speed propagates benefits at every level. Sub\-second queries enable iterative agentic loops that simply don't work if the database can't keep up. Low latency per query compounds across an entire agent run. And fast eval loops let the team ship improvements to customers faster; running 100 data output comparisons, each with three\-run majority voting, needs a database that doesn't turn iteration into a slog.


The virtuous cycle Cogent has found is straightforward: a fast database enables more tool calls, more tool calls produce better accuracy, and better accuracy unlocks more sophisticated agentic patterns. For a company racing to help enterprises keep up with AI\-accelerated attackers, that cycle is the foundation everything else is built on.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-224-get-started-today-sign-up&utm_blogctaid=224)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

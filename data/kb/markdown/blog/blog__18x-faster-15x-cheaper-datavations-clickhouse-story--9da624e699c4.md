# 18x faster, 15x cheaper: How Datavations rebuilt its pipeline with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# 18x faster, 15x cheaper: How Datavations rebuilt its pipeline with ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 6, 2025 · 6 minutes read[Datavations](https://www.datavations.com/) is building what it calls the most accurate and actionable data and optimization platform for the home improvement industry. Founded in New York City in 2020, the company helps manufacturers figure out what to stock, how much inventory to carry, and how much to charge, so they can win shelf space at major retailers like Home Depot and Lowe’s.


At the heart of Datavations’ platform is a proprietary web aggregation system that scrapes massive volumes of store\-level data, from inventory counts and best\-seller ranks to pricing, attributes, and product specifications. That data is processed by machine learning algorithms designed to reconstruct sales metrics with over 90% correlation to actual in\-store results across more than 1,000 categories. “Our data is super accurate and actionable for our clients to use,” says co\-founder and Head of Engineering Jacob Lucas.


At a [July 2025 ClickHouse meetup in New York](https://clickhouse.com/videos/meetupny_July_2025), Jacob shared how Datavations—fresh off a [$17 million Series A](https://www.datavations.ai/press-releases/datavations-raises-17-million-in-series-a-funding-round-led-by-forestay-capital) and growing quickly—rebuilt its data architecture around ClickHouse, cutting costs, improving performance, and giving clients faster, more actionable insights.


## Outgrowing the old stack [\#](/blog/18x-faster-15x-cheaper-datavations-clickhouse-story#outgrowing-the-old-stack)


In the early days, Datavations ran on a fairly standard data stack. Raw signals collected by its aggregation system were dumped into S3, then processed and transformed using Databricks. From there, the data was written back to S3, crawled by AWS Glue, and queried through Athena in Tableau for internal and client\-facing dashboards.


![datavations_img_1.png](/uploads/datavations_img_1_ceca1da454.png)
*Datavations’ original pipeline, built around S3, Databricks, Athena, and Tableau*
The architecture worked well for a while. “Databricks is a pretty good data science tool,” Jacob says. “It was easy to onboard new hires and make changes when something broke.” But as the company scaled and data volumes grew, its limitations became hard to ignore.


The first major pain was cost. Between Databricks licensing fees and the EC2 servers powering the clusters, cloud expenses stacked up fast. “You’re essentially paying double,” Jacob points out. “It was not friendly to the wallet, especially as a startup strapped for cash.”


Performance also became a drag. Pipeline latency made it hard to monitor data quality in real time, and analysts often found themselves waiting minutes for clusters to spin up or queries to return. “It created a huge lag in our data quality insights,” Jacob says. “Our analysts were becoming pretty inefficient with their time.”


## Rebuilding the pipeline with ClickHouse [\#](/blog/18x-faster-15x-cheaper-datavations-clickhouse-story#rebuilding-the-pipeline-with-clickhouse)


Jacob knew Datavations needed something faster, leaner, and better equipped to handle the company’s growing demands. That’s when they decided to adopt ClickHouse.


The new architecture reimagines the pipeline from the ground up. Instead of “just dumping data straight into an S3 bucket,” Jacob explains, Datavations now streams it in through Amazon Kinesis Firehose. AWS Glue sets the schema, and ClickHouse’s native [S3 table engine](https://clickhouse.com/docs/engines/table-engines/integrations/s3) ingests the data directly into the warehouse.


![datavations_img_2.png](/uploads/datavations_img_2_c5e5bf3fc0.png)
*Datavations’ new ClickHouse\-powered pipeline with separate processing and analytics instances*
From there, the pipeline splits across two dedicated ClickHouse instances. The processing instance (self\-hosted on EC2\) handles all transformations using dbt, orchestrated via AWS Batch. A subset of that processed data is copied to the analytics instance, which is optimized for fast queries. This setup keeps transformation and end\-user workloads separate, so internal teams (e.g. data scientists, analytics engineers) can explore data without interfering with production jobs or client\-facing performance.


The frontend is equally modular. Internal teams use Hex, a real\-time analytics notebook that connects directly to ClickHouse. Most clients access the data through Retool, which includes a built\-in Postgres layer. That layer gives non\-technical users the ability to apply brand overrides, manage subscriptions, and push those changes back into ClickHouse to drive downstream logic.


Some clients still pull raw data from S3, but most now use the ClickHouse\-based pipeline for richer insights, faster performance, and a lot less complexity behind the scenes.


## A faster, cheaper, smarter architecture [\#](/blog/18x-faster-15x-cheaper-datavations-clickhouse-story#a-faster-cheaper-smarter-architecture)


Since adopting ClickHouse, Datavations has seen huge improvements across its entire data operation. The biggest and most immediate was cost savings. “We saw a 15x cost reduction in all of our cloud expenses,” Jacob says.


Processing speed is now 18 times faster, with analysts reporting a 5x efficiency uplift thanks to fresher data, quicker feedback loops, and less time waiting for jobs to complete. Clusters spin up instantly now, and datasets load fast enough that the team can explore and iterate in real time. “We’re essentially able to do five times more analysis,” Jacob says.


Storage efficiency has been another win. Datavations’ processing instance holds nearly 42 TB of uncompressed data, which ClickHouse compresses down to just 1\.66 TB. The analytics instance shrinks 2 TB to only 155 GB. That kind of footprint not only improves query performance but keeps infrastructure lean and affordable.


And data quality operations have gotten a lot faster, too. “It went from days for an SLA to just hours,” Jacob says. “We’re able to catch things quicker and fix them if there are issues.”


## What’s next for Datavations and ClickHouse [\#](/blog/18x-faster-15x-cheaper-datavations-clickhouse-story#whats-next-for-datavations-and-clickhouse)


With the new architecture running smoothly, Datavations is focused on its next set of improvements, starting with a move to [ClickHouse Cloud](https://clickhouse.com/cloud). The team currently self\-hosts its processing instance on EC2, but with Cloud now supporting parallel processing, they’re ready to migrate. “We feel more comfortable making that switch,” Jacob says.


They’ve also begun experimenting with [ClickHouse’s MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp) to explore AI\-native workflows. Using the open\-source MCP server and Claude Desktop, the team built a simple local integration that lets users query ClickHouse data using natural language. “It probably took half an hour or so,” Jacob says. The goal is to eventually productionize the MCP server, opening the door to new product possibilities and smarter ways to serve clients.


From an expensive, multi\-step pipeline to a streamlined, high\-performance stack, Datavations has changed the way it delivers insights. As the business keeps growing, ClickHouse will be at the center of that transformation, powering real\-time analytics, reducing overhead, and unlocking new possibilities for Jacob and the team.


Ready to transform your team’s data operations? [Try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

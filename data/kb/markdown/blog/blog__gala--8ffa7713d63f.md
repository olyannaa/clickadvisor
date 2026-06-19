# Gala supercharges analytics performance with ClickHouse on AWS


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Gala supercharges analytics performance with ClickHouse on AWS

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 4, 2026 · 5 minutes read## Benefits

- 3x increase in data analytics capacity
- 30% reduction in costs
- Query times reduced from minutes to sub\-second
[Gala](https://games.gala.com/) runs a blockchain\-powered platform where users can enjoy their favorite games and other media and access a range of decentralized finance products. The company is reliant on analytics to improve game performance, identify new development opportunities, and support marketing planning. But its existing data platform was struggling to cope with the amount of data it needed to ingest and process. After an assessment of the solutions on the market, Gala chose AWS Partner [ClickHouse](https://clickhouse.com/) to deliver the robust data infrastructure that it needed. Built on Amazon Web Services (AWS), the platform offers faster ingestion and has delivered insights that have led to improved productivity for the Gala engineering and marketing teams, better gaming experiences for players, and reduced costs.


## Scaling a growing mountain of data [\#](/blog/gala#scaling-a-growing-mountain-of-data)


Gala was formed in 2019 by Zynga co\-founder Eric Schiermeyer and offers popular multi\-player games like Spider Tanks and GRIT, along with music and video content. The company was built on a blockchain platform to give users transparent ownership of assets and purchases and to encourage greater buy\-in and engagement with the gaming ecosystem. The company also created a decentralized exchange to allow users to trade with each other without an intermediary.


Data is critical for product development. The company’s fast\-paced games generate huge amounts of telemetry data from user interactions, which is crucial for understanding player behavior, optimizing monetization, experimenting, and improving the overall gaming experience. But as the company’s games portfolio expanded and its user base grew, its existing data infrastructure struggled with the volume of data.


In addition to product development, the company’s marketing teams needed analytics data to help direct effective campaigns and strategies. Meanwhile, its engineering teams were spending an increasing amount of time managing the data infrastructure rather than focusing on more strategic initiatives. This needed to change if the business was going to continue to grow. The leadership team at Gala decided to review the data platform market for a suitable replacement for its existing Databricks system.


## A quick migration to a ‘Rocket\-Fast’ data platform [\#](/blog/gala#a-quick-migration-to-a-rocket-fast-data-platform)


After an investigation of leading data platforms, the company chose to migrate to ClickHouse. The platform was chosen for the scalability and performance improvements it offered and for its lower costs.


The initial workload was ingesting its blockchain data from Kafka, but the team quickly recognized the performance and cost benefits possible by powering their analytical dashboards on AWS. Gala has since expanded data sources to include Airbyte, [Amazon S3](https://aws.amazon.com/s3), and Fivetran for continuous ingestion of data.


After the team had completed the ingestion of multiple data sources into ClickHouse, the next stage was the optimization of queries, resources, and connectors, with a focus on further reducing costs and improving efficiency. “ClickHouse is well known as one of the fastest database systems out there,” says Mike Rexford, lead data analyst at Gala. “And that has proven itself out, especially when you’re using its features to their fullest. It is rocket fast.”


Another early catalyst for change was to make analytics and business intelligence (BI) capabilities available to the broader company and make data products more accessible to employees without the relevant technical skills. The company wanted to use Metabase, a user\-friendly, open\-source BI and data visualization tool, to enable this but its previous system couldn’t serve the necessary data at the required speed. ClickHouse was able to support the rollout of Metabase and enable business teams across the company to run their own queries and analytics on the tool. This was enabled by using ClickHouse’s ability to save queries and run API endpoints directly to those saved queries. This change helped remove technical barriers to its analytics.


Gala found the support from ClickHouse “super responsive” despite being in distant time zones. Technical support was particularly helpful for system\-based concerns relating to early data ingestion issues. The company’s small internal technical team appreciated that, if there was a criticism or a problem, ClickHouse listened and fixed the problem or removed it in the next release.


## Sub\-second performance and a 30% cost reduction [\#](/blog/gala#sub-second-performance-and-a-30-cost-reduction)


Performance has improved significantly. “We did have a few unoptimized tables in our previous platform we were struggling with. We had query times in the minutes,” says Keith Cook, data engineer at Gala. “Once we switched over to ClickHouse, we got the indexing correct from the get\-go and ended up with sub\-second query times on the same tables.”


Using ClickHouse on AWS has enabled the company to increase the amount of data available for analysis, rising from 3 TB at the start of the project in February 2024 to 9 TB by the completion of the migration in December 2024, when it decommissioned its old system. The initial costs for working in ClickHouse were 30 percent lower than on its previous data platform. The next steps are to use the ClickHouse ClickPipes data\-processing pipeline to build an even more efficient extract, load, transform (ELT) function.


In addition to faster performance and scalability, ClickHouse has delivered greater reliability, which means that Gala’s engineers spend less time in maintenance mode. “We just don’t think about our data infrastructure as much anymore,” says Rexford. “If something is running slowly and people are wondering what is causing the bottleneck, we know for sure it’s not the database.”

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

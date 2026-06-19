# How Silverflow simplified its data platform and cut end\-to\-end latency by 95% with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Silverflow simplified its data platform and cut end\-to\-end latency by 95% with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 4, 2026 · 8 minutes read## Summary

Silverflow uses ClickHouse Cloud to power near\-real\-time analytics on global payment events, supporting dashboards, alerting, and operational decision\-making. By streaming events directly into ClickHouse, insights that once took 20 minutes to appear in Grafana now arrive in 65 seconds—a 95% reduction in end\-to\-end latency. ClickHouse’s dynamic JSON ingestion and ClickPipes replaced dozens of ETL pipelines, reducing engineering costs while keeping analytics SQL\-based.

[Silverflow](https://www.silverflow.com/) was founded with a clear ambition: replace legacy card\-processing infrastructure with a cloud\-native platform that lets customers connect directly to card networks through a single, unified API. Since its launch in 2019, that promise has carried the company far beyond its Amsterdam roots. Today, Silverflow operates across Europe, the U.S., and Asia\-Pacific, with offices in London and New York and a growing roster of global customers.


But that kind of growth also brings challenges, with every new region, feature, and customer adding volume, variety, and urgency to the stream of events flowing through the platform. “Rapid growth means that data volume and complexity increase quite a lot,” says Roberta Gismondi, a software engineer at Silverflow. “And for us at this stage, it’s crucial to be able to gather the insights we need to optimize and to scale from this data.”


Roberta joined us at our [Open House 2025 roadshow in Amsterdam](https://clickhouse.com/openhouse/amsterdam), where she shared how Silverflow rebuilt its data platform on [ClickHouse Cloud](https://clickhouse.com/cloud), unlocking faster analytics, reducing engineering overhead, and turning payments data into something teams can rely on for real\-time dashboards, alerting, and day\-to\-day decisions.


## The old system’s bottlenecks [\#](/blog/silverflow#the-old-systems-bottlenecks)


As Silverflow grew and expanded into new regions, it also broadened its product offerings, shipping new features quickly. “That means we have a lot of systems, a lot of components, a lot of event types that are emitted by our feature teams,” Roberta says. “And that’s without counting system events.”


For a time, Silverflow’s original data architecture did what it needed to do. Events were published to a central bus, archived, and processed through scheduled ETL jobs. From there, data landed in an S3\-backed data lake and could be queried using Athena, with dashboards built in Grafana and other BI tools.


“This served us well,” Roberta says. “But as we scaled, we encountered a few bottlenecks, mostly around latency and the engineering cost to maintain all of this.”


Data freshness was a major problem—or rather, the lack of it. Some of Silverflow’s most important operational data took up to 20 minutes to become available for querying. Once it was, interactive queries took several seconds just to start, and 10 to 20 seconds to complete. “When the data is supposed to inform time\-sensitive decisions—things like anomaly detection, monitoring, alerting—this is clearly less than ideal,” Roberta says.


At the same time, the cost of maintaining the system kept rising. “Our ETL pipelines were cumbersome, required a lot of maintenance, and in turn, that became quite expensive for our engineers,” Roberta explains. Each event type and version required its own ingestion logic, and those pipelines had to be updated constantly as the platform evolved. As Silverflow’s six feature teams moved quickly and events changed just as fast, pressure on the data engineering team grew. “It was just very hard for us to keep up with all of that,” she says.


## A new approach to events [\#](/blog/silverflow#a-new-approach-to-events)


In early 2025, several members of the Silverflow team, including data engineer David Forbes (who Roberta calls “the main mind behind our data platform”), attended the Data Innovation Summit in Stockholm. They returned to Amsterdam with pages of notes and one idea circled at the top: *ClickHouse’s new approach to JSON.*


“We’re very conservative with headings at Silverflow,” Roberta jokes. “So I was definitely intrigued.”


Within months, the team had stood up its first ClickHouse cluster. Rather than re\-architecting everything at once, they started by integrating [ClickHouse Cloud](https://clickhouse.com/cloud) directly into their existing event architecture. Events published by feature teams continued to flow through Kinesis, but instead of being fanned out into dozens of pipelines, they streamed straight into ClickHouse using [ClickPipes](https://clickhouse.com/cloud/clickpipes), the database’s native ingestion service.


All events now land in a single, dynamically typed table. From there, the team maintains a small number of [materialized views](https://clickhouse.com/docs/materialized-views) to accelerate the most important queries and aggregations. Dashboards still live in Grafana, but the data powering them, and how quickly it arrives, has fundamentally changed.


## Breaking the latency barrier [\#](/blog/silverflow#breaking-the-latency-barrier)


ClickHouse immediately addressed Silverflow’s latency bottleneck. As a [columnar database](https://clickhouse.com/resources/engineering/what-is-columnar-database) designed for analytical workloads, it reads only the data needed for each query. “It turns out being column\-oriented comes in pretty handy when querying things,” Roberta says. “Our events are very big, so being able to strip that down and reduce I/O improves performance quite a lot. This is crucial for analytical workloads.”


The ingestion path saw a major boost, too. Streaming events directly from Kinesis into ClickHouse eliminated multiple buffering and transformation steps. “That meant events were faster to query, but also that they were there to be queried much faster,” Roberta says. Insights that once took 20 minutes to appear in Grafana now arrive in just over a minute end to end—a roughly 95% reduction in data freshness latency.


That shift unlocked new use cases almost overnight. Real\-time dashboards became a reality, alerting is timely rather than retrospective, and product and account teams can rely on data to reflect what’s happening *now*, not what happened half an hour ago. “This made a lot of non\-engineers very happy,” Roberta says, “to be able to gather all those insights so easily.”


## Fewer pipelines, less friction [\#](/blog/silverflow#fewer-pipelines-less-friction)


The second win was just as important, even if it was less visible on a dashboard.


Thanks to [ClickHouse’s ability to work directly with semi\-structured JSON](https://clickhouse.com/docs/integrations/data-formats/json/overview), Silverflow collapsed its entire ingestion layer into a much simpler model. Now, instead of maintaining one pipeline per event type and version, everything flows into a single table. Materialized views handle optimization, rather than bespoke ETL code.


“That pretty much replaced our whole ingestion pipeline,” Roberta says. For the data team, that means fewer moving parts to maintain and far less coordination overhead with feature teams. For analysts and engineers across the company, it means they can continue using familiar SQL\-based tools without learning a new stack.


ClickHouse became, in Roberta’s words, a “drop\-in replacement” for much of the existing query layer, only faster, simpler, and easier to operate. The result is a dramatic reduction in infrastructure complexity and a major shift in how teams interact with data.


## Looking ahead with ClickHouse [\#](/blog/silverflow#looking-ahead-with-clickhouse)


Silverflow’s move to ClickHouse is still unfolding. In the near term, the team plans to migrate more workloads onto the new platform and make historical event data easier for non\-technical users to explore. Over time, they expect to fully decommission their legacy ETL pipelines and standardize on ClickHouse as the foundation of their analytics stack.


There are also strategic considerations on the horizon. Data residency requirements in the U.S. have the team thinking about [regional deployments](https://clickhouse.com/docs/cloud/reference/supported-regions) and [cross\-cluster queries](https://clickhouse.com/docs/engines/table-engines/special/distributed), capabilities that fit naturally into ClickHouse’s architecture.


For Roberta, the journey so far is less about a single technology choice than about removing friction and reclaiming momentum. “This has been a good outcome for the experiment,” she says. “And we want to experiment more.”


At a company built to move fast, the ability to see what’s happening clearly and quickly has become a competitive advantage in its own right. With ClickHouse Cloud, Silverflow has turned its growing stream of payment events into something closer to real\-time understanding, and established a strong foundation for whatever comes next.

### Looking to scale your team’s data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-52-looking-to-scale-your-team-s-data-operations-sign-up&utm_blogctaid=52)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

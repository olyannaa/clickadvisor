# Powering self\-driving vehicle analytics at Avride with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Powering self\-driving vehicle analytics at Avride with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 11, 2026 · 11 minutes read## Summary

- Avride uses ClickHouse Cloud as the data backbone for its autonomous vehicle and delivery robot fleet, powering indexing, metrics, and analytics company\-wide.
- After migrating from Apache Iceberg, index lookup latency dropped from 20 seconds to under 100 milliseconds, and ingestion latency fell from hours or days to seconds.
- Despite deep ClickHouse experience, Avride chose ClickHouse Cloud over self\-hosting for its operational simplicity and separation of storage and compute.
In any given minute, one of [Avride](https://www.avride.ai/)’s self\-driving vehicles generates thousands of data points, from cameras and lidar to temperature sensors and autopilot processes. Capturing, storing, and making that data available to engineers quickly is a daily challenge that plays out across a growing fleet of autonomous passenger vehicles and delivery robots.


In December 2025, the company [launched a commercial robotaxi service](https://www.forbes.com/sites/alanohnsman/2025/12/03/uber-launches-robotaxi-service-in-dallas-with-waymo-rival-avride/) in downtown Dallas, bookable through the Uber app, making it one of the first companies in the world operating an autonomous ride\-hailing service. To date, Avride’s robots have completed hundreds of thousands of orders through Uber Eats and Grubhub across the United States.


ClickHouse sits at the center of Avride’s data infrastructure, powering the index layer for all ride data, the analytics data warehouse, and a range of internal tooling used across the company. The story of how it got there is one of outgrowing a legacy system, solving a tricky engineering problem, and building something the entire company now depends on.


We caught up with Andrey Mironov, Dmitry Kaluzhny, and Kirill Konchenko from Avride’s data and analytics teams to learn how they made the move—and why, despite having more collective ClickHouse experience than almost any team on the planet, they still chose to run it on [ClickHouse Cloud](https://clickhouse.com/cloud) on AWS.


## A foundation for fleet data [\#](/blog/avride#a-foundation-for-fleet-data)


Avride’s data pipeline starts at the vehicle. Cars and delivery robots generate sensor readings, hardware telemetry, and event streams that are continuously uploaded to object storage.


From there, data flows through a simulation pipeline that replays and analyzes rides in a virtual environment, and a processing pipeline that extracts real\-world metrics from what actually happened on the road. The two paths produce offline and online metrics, respectively, which feed into [Grafana](https://clickhouse.com/docs/integrations/grafana) and other visualization tools.


![](/uploads/Avride_Customer_Story_5e25270be8.jpg)
*Avride’s data pipeline, with ClickHouse used for indexing and metrics.*


Today, ClickHouse appears at nearly every stage of the architecture—as the index layer that tracks where all ride data lives, and as the data warehouse storing the metrics that flow from it. It’s a choice with deep roots: Andrey, Dmitry, and Kirill have all worked with ClickHouse for the better part of a decade, dating back to their time at Yandex, where both ClickHouse and Avride’s technology originated.


It wasn’t always that way, however. When the team needed a new foundation for their data infrastructure, ClickHouse was the logical solution.


## The Iceberg problem [\#](/blog/avride#the-iceberg-problem)


For several years, Avride used [Apache Iceberg](https://clickhouse.com/resources/engineering/apache-iceberg) as the metadata and indexing layer over its [Parquet](https://clickhouse.com/resources/engineering/columnar-storage-formats) files. Each index query—by rover and timestamp—had to find the exhaustive set of parquet files containing data for a specific rover at a given timestamp. Given that much of the company's legacy infrastructure was built around Spark, PyArrow, and AWS, Andrey says, “It was natural to pick what we already knew worked for us.”


But as Avride’s fleet grew, the setup began to show its limits. “The pain wasn’t that Iceberg couldn’t do analytics,” Andrey says. “The pain was that our metadata layer started to limit the whole company’s ability to grow and find data quickly.” Behind the scenes for their robotics fleet, Avride needed to improve latency to perform ML training, simulation replay, and debugging for engineers, which is why they turned to ClickHouse.


The core problem was that Iceberg’s ingestion model assumed data would be written sequentially, not in parallel. “Iceberg uses a model called optimistic concurrency,” Andrey explains, “which assumes that no one inserts data in parallel—but usually you do, and it doesn’t scale.” The ClickHouse’s consensus model, by contrast, handles parallel writes natively. As more vehicles came online and more engineers needed to query the index simultaneously, ingestion became a bottleneck. Data that should have been available for analysis within minutes was taking hours, sometimes days.


Lookup performance was also painful. Finding the data for a specific rover in a specific time window (what the team calls a “scene”) could take anywhere from 10 to 20 seconds. That might sound manageable in isolation, but multiplied across an engineering organization where dozens of teams need to query ride data constantly, the latency added up. Teams responded by building their own caching layers on top of the index, “each of them slightly different and each with its own maintenance tax,” Andrey says. The result was a fragmented, hard\-to\-manage landscape that was only going to get worse with fleet growth.


There was also a structural problem with how Iceberg handled data ownership. Because Iceberg takes full custody of any data added to it, and because Avride wanted to preserve originals independently, the only solution was to duplicate everything. Every new rover meant more data, and under Iceberg, that data had to be stored twice. At petabyte scale, the cost of that duplication was compounding with every vehicle Avride put on the road.


## A scalable solution in ClickHouse [\#](/blog/avride#a-scalable-solution-in-clickhouse)


The question of what to replace Iceberg with was, as Andrey puts it, “a no\-brainer and the obvious choice.”


Dmitry notes that the decision wasn’t simply to adopt ClickHouse wholesale. Avride built a custom indexing solution using ClickHouse as its storage and query engine, backed by [S3](https://clickhouse.com/docs/integrations/data-ingestion/s3) for the underlying object storage. “We replaced Iceberg with our own solution built on top of ClickHouse and object storage,” Dmitry says.


With the new setup, “worst\-case” index lookups that previously took 10 to 20 seconds now return in under one second—and on a warm connection, under 100 milliseconds. The caching layers that teams built as workarounds have become mostly unnecessary. “It’s orders of magnitude faster than it was before,” Andrey says.


Ingestion latency—the time between data being produced and becoming usable—“dropped dramatically,” Andrey says, “from hours or even days with Iceberg, to just seconds with ClickHouse.” For an engineering organization where teams are constantly querying ride data, all those hours saved add up quickly.


ClickHouse also eliminated the duplication problem. Because it doesn’t take custody of the underlying payloads the way Iceberg did, Avride can maintain a single source of truth for metadata and indexing without duplicating the raw data in object storage. Those savings compound with every new vehicle added to the fleet.


One additional benefit was multi\-location support. Under Iceberg, Avride had to query separate table installations for each storage location to find where a given piece of data lived. With ClickHouse, the index is unified. “Now we can answer immediately: where is the data stored?” Andrey says. “It might be stored in multiple places, and you can pick one that’s geographically closer to you, or one that makes more sense on other criteria.”


## Why Avride chose ClickHouse Cloud [\#](/blog/avride#why-avride-chose-clickhouse-cloud)


Andrey, Dmitry, and Kirill know what it takes to run ClickHouse at scale—between them, they have around three decades of hands\-on ClickHouse experience. That’s what makes their choice to use [ClickHouse Cloud](https://clickhouse.com/cloud) rather than self\-host so compelling.


When Andrey was at Yandex, they had an entire team of DevOps engineers responsible for maintaining clusters. “Running ClickHouse at scale is a formidable challenge,” he says. “That’s just not sustainable for a company of our size.” At Avride, the engineering capacity that would go into managing clusters is better spent on the problems that actually differentiate the business. “I'm just glad there are people who can do it better,” he adds.


Beyond reducing operational overhead, two technical features made ClickHouse Cloud particularly attractive. The first was the [separation of storage and compute](https://clickhouse.com/docs/guides/separation-storage-compute)—something that wasn’t possible when running ClickHouse on a single server. As more vehicles and data sources come online and query load grows, Avride can scale the two independently, optimizing for cost and performance without being locked into fixed capacity.


The second was the [ClickHouse Cloud SQL console](https://clickhouse.com/docs/integrations/sql-clients/sql-console). “The web UI is really good,” Kirill says. “I use it every day personally, and many developers use it every day just to look things up.” For a data tool that spans the entire company, that ease of use matters. The lower the barrier to querying, the more value teams can extract.


## Impact from engineers to executives [\#](/blog/avride#impact-from-engineers-to-executives)


Today, ClickHouse is used by virtually every team at Avride. Engineering teams across perception, motion planning, localization, and mapping all query ride data through the ClickHouse\-backed index. The simulation team runs offline metrics through it. The operations team uses it to monitor fleet health in real time. From sales and marketing in the Business Development team to Avride’s CEO, decisions are powered by insights that ultimately trace back to ClickHouse.


“It’s hard to think of a team that doesn’t use ClickHouse at some point,” Kirill says.


Some of the most interesting use cases go well beyond standard analytics. Avride has an internal tool called Aviz that lets engineers replay portions of a ride to debug vehicle behavior—essentially a time machine for what the car experienced at a given moment. Scheduling data for ride and delivery assignments is stored and queried there too, allowing teams to reconstruct the full lifecycle of any order.


One of the most distinctive use cases is C\+\+ performance profiling. Every operation running on Avride’s vehicles generates execution traces, recording which code paths were entered, when, and for how long. That data flows into ClickHouse, where pipeline developers query it to identify performance regressions and debug latency issues in the autopilot. It’s an unconventional use case, but one that benefits from the same properties—fast ingestion, fast lookup, and a [columnar storage](https://clickhouse.com/resources/engineering/what-is-columnar-database) format that handles high\-cardinality data efficiently.


Across all these use cases, the volume of data is significant. Each vehicle produces thousands of data points per minute, from hardware sensor readings to autopilot events to scheduling updates, with some metrics collected multiple times per second. Multiplied across a growing fleet operating in multiple cities, all that data adds up quickly.


## The default choice for growth [\#](/blog/avride#the-default-choice-for-growth)


Looking forward, the team has plans to introduce query quotas to protect production workloads as usage grows. The fleet is expanding, which means more data, more engineers querying it, and more pressure on the systems that underpin it all.


With ClickHouse Cloud, the foundation is ready for that growth. What started as a targeted fix for a metadata and ingestion problem has become the go\-to data platform for an entire company, trusted with everything from real\-time fleet operations to C\+\+ profiling to executive dashboards. As new challenges and use cases emerge, Avride has a familiar partner to ensure speed, reliability, and scalability. As Dmitry puts it, “ClickHouse is our default choice.”

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

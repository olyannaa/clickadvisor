# How SolarWinds uses ClickHouse BYOC for real\-time observability at scale


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How SolarWinds uses ClickHouse BYOC for real\-time observability at scale

![](/_next/image?url=%2Fuploads%2Ftony_burke_fb4882ba26.jpg&w=96&q=75)Tony Burke, SolarWindsMar 11, 2025 · 7 minutes readWhen software engineer Tony Burke joined SolarWinds in 2023, he brought nearly three decades of experience solving complex technical issues and architecting solutions for cloud and SaaS companies. But even with Tony’s expertise, the scale and high\-stakes nature of SolarWinds’ data operations posed a series of unique challenges.


For over 25 years, the Austin\-based company has been a leader in observability and IT management, serving more than 300,000 customers around the world. Its simple but powerful tools help IT teams monitor everything from servers and applications to Kubernetes clusters in real time, providing the insights they need to act quickly when systems falter.


Behind the scenes, SolarWinds processes 3 million telemetry messages per second, averaging 550 megabytes per second and peaking at bursts of a gigabyte. This relentless flow powers the real\-time dashboards and alerts that IT teams depend on to keep their infrastructure running smoothly. One of Tony’s first major tasks upon joining SolarWinds’ platform engineering team: make sure it could scale to meet demand without sacrificing performance.


At a [September 2024 meetup in Austin](https://www.youtube.com/watch?v=YB12NLAQG5U), Tony described how he and the team turned to ClickHouse to tackle these challenges. By fine\-tuning their system and optimizing queries for time\-sensitive metrics, SolarWinds built a data platform capable of scaling with speed and precision, handling millions of real\-time messages without missing a beat.



## The heat is on [\#](/blog/how-solarwinds-uses-clickhouse-for-realtime-observability-at-scale#the-heat-is-on)


As Tony explains, managing "hot query data" — the most recent 60 minutes of incoming telemetry — is one of the most demanding aspects of SolarWinds’ operations. This data is the backbone of real\-time alerts and troubleshooting, where every second counts. IT teams depend on these insights to pinpoint issues and act fast, making any delay unacceptable.


The sheer volume and speed of this data, however, creates unique engineering challenges. Incoming telemetry flows into ClickHouse’s [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) engine, which organizes data into small chunks called parts. Over time, these parts merge into larger ones for efficiency. But with data arriving so quickly, these merges don’t always keep up, causing slowdowns when querying the freshest data.


For Tony and the platform engineering team, the goal was straightforward, if technically demanding: optimize ClickHouse to deliver near\-instantaneous query performance for this mission\-critical data. Even small gains in speed could mean the difference between quick fixes and prolonged downtime for SolarWinds’ customers.


## Learning ClickHouse from scratch [\#](/blog/how-solarwinds-uses-clickhouse-for-realtime-observability-at-scale#learning-clickhouse-from-scratch)


When Tony first joined SolarWinds, he was new to ClickHouse. Tasked with optimizing its performance, he first had to familiarize himself with the database and how it worked. "You can’t really tune something you don’t know the mechanics of," he says. "Being new to ClickHouse, I needed to understand its physical layout and how it stores and manages data."


He began by building a deep understanding of the columnar database’s architecture and mechanics, focusing on how ClickHouse organizes data and resolves queries. He also studied ClickHouse’s [sparse indexing system](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes), which is designed to only index a subset of rows, reducing storage requirements while maintaining query efficiency.


This foundational knowledge helped Tony identify areas where ClickHouse could be adjusted to meet SolarWinds’ unique data needs. With a clear picture of the database’s inner workings, he turned his attention to key elements like the primary key structure and index granularity, kicking off a series of experiments geared at optimizing performance.


## Unlocking speed with granularity [\#](/blog/how-solarwinds-uses-clickhouse-for-realtime-observability-at-scale#unlocking-speed-with-granularity)


Through his research, Tony discovered that tweaking the primary key would have little effect on performance. "Our primary key columns — tenant, namespace, and hour — already have high cardinality," he explains. “Improving that wouldn’t really reduce the marks selected.”


Instead, he turned to a different lever: index granularity. Index granularity determines how many rows are grouped together under a single index entry. Reducing the granularity would mean fewer rows read per query, potentially leading to faster response times. To test this idea, Tony mirrored SolarWinds’ metrics table into a new one with reduced granularity and used their internal query routing service (known as “Chainsaw”) to A/B test the results.


The results were significant. For a five\-minute time window, query times dropped from 76 milliseconds to just 28 milliseconds in a test environment — an improvement of more than 60%. The number of rows read per query also plummeted, showing the efficiency gains of reduced granularity. For SolarWinds’ customers, this meant faster dashboards, more responsive alerts, and quicker action during critical moments.


![sparse_indices.png](/uploads/sparse_indices_dark_eed5e57942.png)
## Balancing gains and tradeoffs [\#](/blog/how-solarwinds-uses-clickhouse-for-realtime-observability-at-scale#balancing-gains-and-tradeoffs)


As effective as the optimizations were, they came with a few tradeoffs. Reducing granularity increased the size of the primary key and column mark files, requiring more memory. Tony notes that memory usage for the primary key index could grow from 10 GB to as much as 320 GB with reduced granularity. Merge times also rose by nearly 50% due to the higher number of smaller parts created, requiring extra monitoring to avoid bottlenecks.


Beyond these adjustments, Tony and the team discovered another opportunity for optimization: filesystem reads. ClickHouse’s default `pread_threadpool` setting, which routes file reads through a thread pool, was creating inefficiencies. By switching to `pread`, they bypassed the thread pool, taking advantage of SolarWinds’ fast SSDs and improving query performance.


These tradeoffs show the complexity of fine\-tuning a high\-performance database like ClickHouse. "You have to track metrics like memory usage and merge durations carefully to ensure stability," Tony says. At the same time, the results highlight ClickHouse’s adaptability, allowing the team to tailor their setup without sacrificing reliability.


## Adopting ClickHouse BYOC (Bring Your Own Cloud) [\#](/blog/how-solarwinds-uses-clickhouse-for-realtime-observability-at-scale#adopting-clickhouse-byoc-bring-your-own-cloud)


To streamline management of its ClickHouse deployments, SolarWinds adopted the [Bring Your Own Cloud (BYOC) deployment model on AWS](https://clickhouse.com/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws). This lets them deploy ClickHouse clusters within their own AWS Virtual Private Cloud (VPC), giving them greater control over security, network configurations, and data compliance. This architecture ensures that all data remains within SolarWinds’ VPC, facilitating compliance with strict data governance and residency requirements.


By leveraging ClickHouse’s shared\-storage architecture with Amazon S3 for durable storage and employing compute\-compute separation, SolarWinds can independently scale compute resources, which enables greater resource isolation for high\-concurrency workloads and more fine\-grained compute resource allocation, resulting in [infrastructure cost savings](/resources/engineering/observability-cost-optimization-playbook). SolarWinds also benefits from simplified maintenance and automated upgrades, resulting in reduced operational overhead compared to the previous self\-managed ClickHouse deployment.


![byoc.png](/uploads/byoc_9aff7a38e4.png)
## Powering the future of observability [\#](/blog/how-solarwinds-uses-clickhouse-for-realtime-observability-at-scale#powering-the-future-of-observability)


For SolarWinds, ClickHouse isn’t just a database — it’s the foundation of their real\-time observability platform. Its scalability and flexibility make it an ideal fit for processing millions of queries every day, giving IT teams and professionals the ability to troubleshoot faster, respond smarter, and maintain system reliability.


Tony’s work, in particular, shows what ClickHouse unlocks for engineering teams. By making it easy for engineers to experiment with optimizations and dig deep into performance bottlenecks, ClickHouse helps companies like SolarWinds stay ahead of surging data demands.


At its core, real\-time observability at SolarWinds is about empowering IT teams to act with speed, precision, and confidence. ClickHouse gives them the data architecture to make this possible, even in the face of new and complex data challenges.


To learn more about ClickHouse and see how it can transform your team’s data operations, try [ClickHouse Cloud](https://clickhouse.com/cloud) free for 30 days.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

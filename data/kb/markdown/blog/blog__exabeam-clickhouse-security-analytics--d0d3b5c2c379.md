# How Exabeam uses ClickHouse for scalable, searchable security analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Exabeam uses ClickHouse for scalable, searchable security analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Sep 11, 2025 · 8 minutes readIn cybersecurity, you're racing the clock. When a threat hits, the time it takes to detect and respond can be the difference between a routine alert and a full\-blown breach.


At [Exabeam](https://www.exabeam.com/), a security operations platform that uses AI and machine learning to deliver end\-to\-end threat detection, investigation, and response, that time is measured as mean time to detection, or MTTD. Bringing that number down took more than fast infrastructure; they needed a real\-time analytics engine that could handle millions of events per second, surface anomalies right away, and support complex searches across petabytes of log data.


At [ClickHouse's Open House user conference in May 2025](https://clickhouse.com/openhouse#video-exabeam), Exabeam VP of Engineering Vinayak Saokar and Senior Software Engineer Arunmozhi (Arun) RA shared how they're using [ClickHouse Cloud](https://clickhouse.com/cloud) to power their platform across 10 global regions. From sub\-second search speeds to a custom ingestion pipeline, they've fine\-tuned every part of the system to make investigations faster, while keeping compute costs under control.


## The four pillars of smart security [\#](/blog/exabeam-clickhouse-security-analytics#the-four-pillars-of-smart-security)


Exabeam's SecOps platform is built on four pillars: ingestion, threat detection, investigation, and response. Together, they help security teams make sense of the noise and act quickly.


It starts with ingestion. Exabeam pulls in data from a wide range of sources, including cloud workloads, SaaS apps, endpoints, firewalls, and more. As that data flows through the pipeline, it's enriched with extra context so analysts aren't starting from scratch. Instead of raw logs, they're working with information they can actually use.


From there, Exabeam's threat detection engine kicks in. Powered by AI and machine learning, it combines user and entity behavior analytics (UEBA), risk scoring, correlation, and a library of over 2,000 detection rules and 750 behavioral models to flag anything suspicious. "This is where we can surface real threats quickly while minimizing noise," Vinayak says.


If something looks off, analysts can dig in using rich event timelines and an AI co\-pilot that provides readable threat summaries. As Vinayak explains, "It takes all the detections and runs them through generative AI to give you a nice, deep insight into the threat."


And when it's time to act, Exabeam supports rapid response through customizable playbooks and integrations with third\-party tools, helping teams contain and resolve threats faster.


"You can see why we need our real\-time analytics database to be very performant," Vinayak says. "ClickHouse has helped us lower mean time to detection."


## Built for speed and scale [\#](/blog/exabeam-clickhouse-security-analytics#built-for-speed-and-scale)


As Vinayak explained at Open House, Exabeam runs its platform across 10 global regions, all powered by ClickHouse Cloud. At peak, they're ingesting 1\.2 million events per second per region, adding up to more than 80 billion events daily.


In just a few months, Exabeam has already stored over 1 trillion events. That's about 3\.5 petabytes of raw data, or 200 TiB after compression. To manage that scale, the system is optimized for time\-series log data and structured using a common information model with more than 1,000 fields. Customers can also add custom fields, making it flexible enough for multi\-tenant use without sacrificing performance.


To keep queries fast and costs predictable, Exabeam uses hot\-cold storage tiering. Events from the past 14 days are kept "hot," so analysts can get fast answers when they need them most. "Mean time to detection is very critical," Vinayak says. "I want faster, lower\-cost queries so I can do the detections and surface it to the security analysts."


They've also built in extra storage capacity to handle future growth. The result is a real\-time analytics engine that's lightning\-fast, flexible, and ready to scale.


## Exabeam's ClickHouse\-based architecture [\#](/blog/exabeam-clickhouse-security-analytics#exabeams-clickhouse-based-architecture)


Handling 1\.2 million events per second is a tall order. Exabeam needed an architecture that could keep ingestion fast, queries responsive, and merges stable, even under heavy load.


"Certain workloads are very, very read\-heavy," Arun explains. "We didn't want those to affect the writes and merges." So the team implemented [compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud), splitting write, merge, and read operations into their own dedicated instances.


In this setup, data flows from a custom ClickHouse ingestor service into write nodes, which focus solely on ingestion. Merge nodes handle background merges to keep data compact and performant, while read nodes deliver fast, concurrent query responses to downstream applications.


![How Exabeam uses ClickHouse for scalable, searchable security analytics 2.png](/uploads/How_Exabeam_uses_Click_House_for_scalable_searchable_security_analytics_2_26f8075d52.png)
Exabeam’s ClickHouse architecture separates reads, writes, and merges for real\-time analytics.
Schema changes are managed via Liquibase, and everything runs over [GCP Private Service Connect](https://clickhouse.com/docs/manage/security/gcp-private-service-connect), keeping egress low, latency light, and all data inside Google Cloud.


## A raft of ClickHouse optimizations [\#](/blog/exabeam-clickhouse-security-analytics#a-raft-of-clickhouse-optimizations)


Vinayak, Arun, and the team didn't simply plug ClickHouse into their platform. They engineered around it, tweaking everything from schema design to ingestion mechanics to increase throughput, reduce query times, and cut infrastructure costs.


One of the first big wins came from consolidating fields. Instead of scanning hundreds of separate columns, they created a single wide column that holds all the commonly queried data. This cut query latency from over 8 seconds (when scanning 180\+ columns) to under 1 second when hitting the consolidated field alone.


Next, they tackled column sprawl. The original schema had more than 1,150 fields, many of them sparsely populated. By compressing those rare fields into a single key\-value column, they shrank the schema down to just 250 columns, making merges lighter and ingestion faster. "This helped us scale from 100,000 to 250,000 events per second on a three\-node cluster," Arun explains. Fewer columns also meant less memory usage and faster inserts.


Finally, they reworked the ingestor pipeline for speed and efficiency. Switching from Gson to Jackson sped up JSON parsing by 60%, and increasing the buffer size on their Gzip reader improved file read performance by 20%. They also optimized how events were serialized and sent to ClickHouse, reducing transmission time for 100,000 events from 20 seconds to just one, and cutting per\-pod memory usage from 7 GB to 4 GB.


![exabeam-3.png](/uploads/exabeam_3_0803394731.png)
Optimizing the ingestor reduced memory usage by 45% and boosted throughput to 20K\+ events/sec.
## Solving problems along the way [\#](/blog/exabeam-clickhouse-security-analytics#solving-problems-along-the-way)


Running ClickHouse at Exabeam’s scale hasn’t been without challenges. Early in production, the team found that inserting 100,000 events per batch was creating too many part files across too many partitions. Most of the data landed in the recent partition, but a small fraction—around 3\-5%—was backdated and ended up scattered across dozens of older ones.


“That’s not optimal, because ClickHouse has to merge all those parts in the background,” Arun explains. “And if writes are using a lot of memory at the same time, those merges will be aborted due to memory issues.”


To fix this, Exabeam split ingestion into two pipelines: real\-time and backlog. The real\-time ingestor handles fresh data, while older events are routed to a backlog topic, where a separate process batches them more efficiently. “This reduced the number of part files and helped bring down our operational overhead with ClickHouse,” Arun says.


![How Exabeam uses ClickHouse for scalable, searchable security analytics 01.png](/uploads/How_Exabeam_uses_Click_House_for_scalable_searchable_security_analytics_01_6df06deb76.png)
Dual\-pipeline design separates real\-time and backlog ingestion to reduce part files and overhead.
![exabeam-4.png](/uploads/exabeam_4_0e8077e03a.png)
Backlog ingestion (bottom) tapers off as real\-time pipeline (top) holds steady near 1M events/sec.
The team also ran into issues with N\-gram indexes, which they initially used for regex and IP searches. While effective, these indexes were resource\-intensive. “It requires more hardware, because ClickHouse needs to do background matches,” Arun says. “With every background match, it has to recreate the index, which gets expensive.”


Since regex queries make up less than 1% of workloads, they switched to a leaner tokenization approach, breaking text into individual tokens for faster lookup. This reduced index size, lowered hardware requirements, and made searches more efficient overall.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Fast, flexible, and built to scale [\#](/blog/exabeam-clickhouse-security-analytics#fast-flexible-and-built-to-scale)


With ClickHouse Cloud, Exabeam has transformed how it delivers security analytics, ingesting data at massive scale across 10 regions, compressing trillions of events, and enabling sub\-second search on complex, high\-dimensional datasets.


“By leveraging ClickHouse, we’re able to deliver high\-speed, low\-latency, and cost\-efficient search capabilities,” Arun says.


From reducing column sprawl to rethinking ingestion and indexing, Exabeam has steadily pushed performance higher and MTTD lower, all in pursuit of their north star: getting the right information to security teams as quickly as possible.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

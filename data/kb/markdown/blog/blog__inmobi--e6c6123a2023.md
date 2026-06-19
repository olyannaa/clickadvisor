# How InMobi achieved 20x faster queries and 80% cost savings with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How InMobi achieved 20x faster queries and 80% cost savings with ClickHouse

![](/_next/image?url=%2Fuploads%2FAmber_Vaid_In_Mobi_2debffad77.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2FAnand_Tirthgirikar_7451d01526.png&w=96&q=75)Amber Vaid \& Anand TirthgirikarFeb 25, 2026 · 11 minutes read## Summary


div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

InMobi uses ClickHouse to power real\-time ad reporting APIs, serving key metrics (e.g. impressions, clicks) under strict latency and availability SLAs. Migrating from a serverless warehouse to ClickHouse cut P99 latency from 60s to under 3s and reduced monthly spend by 80% (from $40K to $8K). The system now handles 400K\+ daily queries across 10 TB of data and serves as a reusable analytics platform for new use cases across InMobi.

If you’re like most consumers, you probably open a mobile app, see an ad, decide whether to tap, and then move on. Out of sight, out of mind…


But for publishers, that split\-second moment is anything but forgettable. It’s a real\-time verdict on whether their inventory is performing across devices, geographies, and millions of users, every minute of the day. And they rely on ad\-tech leaders like [InMobi](https://www.inmobi.com/) not just to deliver those ads, but to turn those moments into trustworthy, immediate insight.


Founded in India in 2007, InMobi connects 30,000\+ brands and publishers to more than 2 billion people across 150\+ countries, handling roughly 250 billion ad requests and 30 billion events every single day. All told, the platform ingests over 240 TB of data daily.


At our [Open House Roadshow in Bangalore](https://clickhouse.com/videos/open-house-bangalore-inmobi), InMobi engineers Anand Tirthgirikar and Amber Vaid shared the story of “Project Velocity”—their effort to redesign publisher\-facing reporting and make it fast enough for real\-time decisions, reliable enough to meet strict SLAs, and cost\-efficient enough to keep up with InMobi’s growth.


As Anand puts it, “This is the story of how we’ve adopted ClickHouse to build a fast, reliable, and cost\-efficient solution for one of our most important use cases.”



## The old system: too slow and expensive [\#](/blog/inmobi#the-old-system-too-slow-and-expensive)


For thousands of publishers, InMobi’s APIs are a window into what’s happening with their inventory. As Anand puts it, “They want to know, on a real\-time basis, how many impressions and clicks are happening across different dimensions like OS, device type, and geography.”


Those APIs are bound by SLAs that require P99 latency of 10 seconds or less. Over time, however, that commitment became harder to keep. “With our previous setup, we were facing issues where during peak hours it was crossing one minute,” Anand says.


And the load wasn’t small. The system was handling more than 400,000 requests per day, with query volume ranging from 200 to 600 queries per minute depending on the hour.


Then there was what the team calls “the cost problem.” InMobi’s existing stack relied on a serverless warehouse reading directly from blob storage. “The licensing cost was about $40,000 dollars per month,” Anand says. “And the cost model was such that if traffic increased, it meant a linear increase in cost as well.”


## A successful POC with ClickHouse [\#](/blog/inmobi#a-successful-poc-with-clickhouse)


It was clear something had to give. The team needed sub\-second performance, a way to tame costs, and an analytics platform that could keep pace with InMobi’s growth.


So they held a bake\-off, testing multiple databases against the same publisher\-reporting workload and evaluating them on query latency, compression, and infra requirements.


“ClickHouse worked the best for us,” Anand says. It delivered “3x faster query performance as compared to our current setup,” plus a 5:1 compression ratio. “And for every query that was getting fired, we observed 70% fewer rows scanned,” he adds.


The infrastructure comparison was just as striking. The old serverless warehouse routinely autoscaled from 56 to 448 vCPUs and 0\.5 to 3\.5 TB of RAM just to stay afloat. ClickHouse handled the same workload on a fixed 60 vCPUs and 240 GB of RAM.


“That explains why we could see 80% cost savings,” Anand says.


## InMobi’s ClickHouse\-based architecture [\#](/blog/inmobi#inmobis-clickhouse-based-architecture)


In the new ClickHouse\-based production architecture, data still flows from cloud storage and refreshes on an hourly cadence, but ingestion now runs through Spark jobs that write into ClickHouse instead of the old warehouse.


![InMobi User Story Issue 1230 (1).jpg](/uploads/In_Mobi_User_Story_Issue_1230_1_1c9c42ca93.jpg)
*InMobi’s ClickHouse\-based architecture with hourly Spark ingestion and isolated reader/writer services.*


Using ClickHouse managed instances, they’ve adopted a parent\-child service pattern for reads and writes. “The reader service is meant for our backend to have a dedicated resource to serve all the API requests,” Anand explains. “And the writer service is an ephemeral service that we spawn up every hour to ingest the data and then shut down.”


Both services share the same distributed storage, but their compute is cleanly isolated. “This way, our reader service remains intact and doesn’t face any latency issues,” he says.


When it comes to storage, the transformation was dramatic: more than 10 TB uncompressed became 2\.5 TB in Parquet—and roughly 500 GB in ClickHouse.


## Go\-live challenges and solutions [\#](/blog/inmobi#go-live-challenges-and-solutions)


Of course, turning a promising architecture diagram into a battle\-tested production system meant solving a few hard problems. Amber walked through the biggest challenges the team faced—and how they engineered their way through each of them.


## Challenge \#1 \- Atomic ingestion at scale [\#](/blog/inmobi#challenge-1---atomic-ingestion-at-scale)


Fault tolerance is great… until it breaks your data guarantees. As Amber explains, “While Spark is fault tolerant, if any of the executors dies or any task fails, it retriggers the pipeline, causing deduplication at the target layer.” For publisher\-facing metrics, this wasn’t acceptable.


![InMobi User Story Issue 1230.jpg](/uploads/In_Mobi_User_Story_Issue_1230_b711389f2c.jpg)
*ClickHouse staging\-to\-production pipeline using validation and partition moves for atomic ingestion.*


So the team introduced a staging → validation → production pattern. Spark writes each hourly batch into a staging table, and the system validates row counts and KPIs against expectations. Only after validation passes does it promote data into the production table using ClickHouse’s [MOVE PARTITION](https://clickhouse.com/docs/sql-reference/statements/alter/partition#move-partitionpart) command. If anything fails, the promotion doesn’t happen, keeping the production view clean and atomic.


## Challenge \#2 \- Concurrency and connection limits [\#](/blog/inmobi#challenge-2---concurrency-and-connection-limits)


During the POC, the team took a simple “fire and forget” approach to querying ClickHouse. “The POC numbers were very tempting and very good, and it looked like we could move forward,” Amber says. “But once we productionized it, we faced a small issue, which was max\_concurrent\_connections.”


In the production environment, the application layer kept sessions open with ClickHouse, and each session carried its own memory overhead. “Because of that memory overhead,” he explains, “it choked our cluster and caused out\-of\-memory exceptions.”


The fix was to rethink concurrency. The team adopted gevent with greenlets for lightweight concurrency, rewrote the serving platform to use asynchronous patterns correctly, and reduced the per\-connection footprint. After the change, P99 latency stayed below 6 seconds even during peak traffic. “And we haven’t faced any OOM issues since,” Amber says.


## Challenge \#3 \- Fallback during downtime [\#](/blog/inmobi#challenge-3---fallback-during-downtime)


Given the stakes involved, InMobi’s reporting API has to be rock\-solid. “We have external publishers querying this table, so we can’t afford to have downtime,” Amber says.


As a fallback, the team wired Grafana dashboards to ClickHouse server metrics and defined a simple rule: “If we notice more than 2% of failures in a 5\-minute window, we automatically route traffic back to the serverless platform,” he explains. “That’s how we provide reliability.”


## Challenge \#4 \- Step\-function cost scaling [\#](/blog/inmobi#challenge-4---step-function-cost-scaling)


InMobi projects its data volumes to grow by 5x over the next two years. Their stress tests showed that each additional ClickHouse node or replica can handle 30% more traffic.


Now, with cost growth as a step function rather than a straight line, costs rise only when the team deliberately adds capacity, not with every incremental uptick in queries. As Amber puts it, “We can just increase the replica and serve more traffic over time.”


## 20x faster, 80% cheaper with ClickHouse [\#](/blog/inmobi#20x-faster-80-cheaper-with-clickhouse)


With ingestion, concurrency, reliability, and cost all under control, the system was ready for full\-scale production—and ClickHouse more than delivered.


As Amber says, “Our P99 latency, which was previously more than a minute, has been reduced down to less than three seconds during our peak hours.” The platform now comfortably serves more than 400,000 queries per day across over 10 TB of uncompressed data (roughly 500 GB compressed in ClickHouse).


Monthly costs, meanwhile, have fallen from $40,000 to $8,000—an 80% reduction. “This was a major win for us,” Amber says, adding that “the cost of our serverless platform was growing exponentially, but now we know how much it will be in the next two years.”


Reliability has improved, too. Atomic ingestion, proper connection management, and automated fallback mean the team can meet SLAs without firefighting. And publishers get faster insights through more responsive reporting APIs.


The benefits weren’t limited to improving one workload. Instead of treating Project Velocity as a one\-off fix for publisher reporting, the Data Platform team turned it into a company\-wide analytics pattern. “Our main target was to provide these APIs to every developer at InMobi and make it as generic as possible,” Amber says.


The team built tooling that analyzes query history and suggests optimized [CREATE TABLE](https://clickhouse.com/docs/sql-reference/statements/create/table) definitions, including index options. A generic ingestion pipeline handles [type conversion](https://clickhouse.com/docs/sql-reference/functions/type-conversion-functions) and syncing from Delta or blob storage into ClickHouse. For developers across InMobi who don’t live and breathe ClickHouse internals, Project Velocity abstracts away the complexity and offers a ready\-made, battle\-tested foundation for new analytics use cases.


## Lessons learned and looking ahead [\#](/blog/inmobi#lessons-learned-and-looking-ahead)


Looking back on their progress, Anand and Amber point to a handful of lessons that now guide how they design data systems at InMobi.


The first: ingestion is about *correctness*, not just speed. With Spark retries and hourly batches, partial and duplicate writes were inevitable. The staging\-and\-validation model ensures that “whatever data we’re reporting to our customers is correct and validated,” Anand says.


Next, async connection management is “crucial for APIs.” Simply pointing your application at a fast database isn’t enough. The concurrency model, and the way connections are created, reused, and cleaned up, is what ensures reliability and a zero\-failure platform.


The team also learned that predictability is as valuable as performance. Moving from a linear cost curve to a step\-function model with ClickHouse has allowed them to forecast spend as traffic grows. And as Anand puts it, "Predictability is gold at InMobi scale.”


Finally, guardrails—validation on ingestion, automated fallback to a secondary system, and error thresholds in monitoring—are essential. Each layer reduces operational risk when external customers are hitting your endpoints.


In the end, Project Velocity began with a simple mandate: make publisher reporting faster and cheaper. ClickHouse delivered that and more. It gave InMobi a foundation for building analytics that are fast, reliable, and economically smart at terabyte scale.


“We adopted ClickHouse for speed,” Anand says. “It ended up delivering not just speed, but helping us build a platform that’s fast, reliable, and predictable on a cost basis. That's what Project Velocity stands for at InMobi.”

### Ready to scale your data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-76-ready-to-scale-your-data-operations-sign-up&utm_blogctaid=76)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

# Tekion adopts ClickHouse Cloud to power application performance and metrics monitoring


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Tekion adopts ClickHouse Cloud to power application performance and metrics monitoring

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 26, 2024 · 8 minutes readFounded in 2016 by ex\-Tesla CIO Jay Vijayan and using technologies ranging from big data and artificial intelligence to IoT, [Tekion](https://tekion.com/) solves a variety of problems for their automotive customers.


Tekion rolled out their dealer management software, Automotive Retail Cloud (ARC), in 2020\. An end\-to\-end cloud platform designed to seamlessly connect an entire auto dealer’s business, ARC brought new levels of simplicity, efficiency and connectivity to both dealers and manufacturers. As VP, Engineering, Platform \& Architecture, at Tekion, Ved Surtani explains: “In the past, it was not unusual for dealerships to be using more than 100 point solutions to run their business. Tekion gets it down to just four.”


ClickHouse Cloud has been a game\-changer and the Tekion team has enjoyed advantages, including optimization, improved performance, and cost efficiency, for several of their key use cases.


## Tekion internal observability stack [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#tekion-internal-observability-stack)


Tekion’s business relies on an internally\-built observability stack, which includes application performance monitoring (APM) and custom metrics analytics. This stack is critical to fast execution on Tekion’s distinguished array of SaaS products for the automotive industry – if these tools are not working, engineers and data scientists are unable to effectively develop and ship new applications. Running previously on a well\-known search provider, this stack became no longer performant, expensive, and difficult to maintain, as data volumes increased.


Tekion’s **Dataplatform APM** is an in\-house platform for application performance monitoring (APM), analyzing the performance of software applications to ensure they are running efficiently and meeting performance objectives: “By measuring the quality of our own performance through customized dashboards, we've harnessed ClickHouse capabilities to improve our decision\-making processes and its efficiency and scalability are becoming indispensable”. Another inhouse platform, **Dataplatform Custom Metrics** allows users, applications, jobs, and tools to send metrics from diverse sources and create custom metrics. Tekion can capture, track, monitor and report on unique aspects of performance or behavior and to identify anomalies or issues, so appropriate action can be taken.


## Challenges with scale and cost prompts a search for alternatives [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#challenges-with-scale-and-cost-prompts-a-search-for-alternatives)


As Tekion grew and its engineering operations expanded, its internal observability stack started facing challenges around ingestion speed and efficiency, query performance, and spiraling costs: “As our data continued to expand, the limitations around scalability, speed and cost effectiveness of our existing tech became increasingly apparent,” says Surtani. Tekion considered storing only aggregate data, assuming it would address most user needs. However, the inability to drill down into individual transactions for debugging purposes remained a persistent challenge: “Previously, the idea of ingesting raw records and attaining detailed transaction information seemed daunting. While it's theoretically possible to achieve impressive outcomes by investing substantial financial resources into building a large cluster. Such an approach is neither practical nor financially sustainable,” Surtani explains.


In the previous architecture, data streams from applications were ingested via Kafka and processed through custom services into the datastore. This approach facilitated the execution of custom Spark jobs to uncover complex patterns and alerts. While effective for analysis, consumption was hindered by slow search performance and limitations in dashboarding capabilities.


Tekion evaluated various options, including Delta Lake and HBase, in search of faster data retrieval mechanisms: “We were looking for a solution which could ingest fast as well as allow us to retrieve individual transactions at a faster pace,” says Surtani. They found ClickHouse: “We saw the potential to revolutionize our data management processes,” he adds.


## Proof of concept: Open\-Source or ClickHouse Cloud? [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#proof-of-concept-open-source-or-clickhouse-cloud)


For the proof of concept (POC) evaluation, Tekion kicked off with open\-source ClickHouse and then transitioned to ClickHouse Cloud. Opting for open\-source initially is part of standard practice at Tekion, enabling the team to assess performance and cost\-effectiveness before committing to a cloud\-based solution: “This approach provides valuable insights into the benefits of migrating and bakes in informed decision\-making,” says Surtani. The POC uncovered exciting results – it found ClickHouse to be superior in handling large volumes of data: “We realized how good it was and the potential during basic POC, so expectations were high,” says Surtani, prompting Tekion to explore ClickHouse Cloud.


The ability to scale clusters without compromising performance or incurring additional overhead was compelling. While Tekion is more than capable of managing infrastructure independently, the team decided to focus team efforts on product development for customers, leaving the maintenance to ClickHouse (via ClickHouse Cloud). Plus, explains Surtani, “ClickHouse Cloud offers premium features above the open\- source route, such as dynamic scaling of clusters on the fly without the need for manual indexing, enhancing operational efficiency and scalability.” Ultimately, the combination of expert support, advanced features, and cost efficiency made ClickHouse Cloud the best choice for driving the organization forward.



> "ClickHouse Cloud has provided the capability to exceed performance objectives in a cost\-effective way."
> 
> Ved Surtani, VP, Engineering, Platform \& Architecture at Tekion


## ClickHouse Cloud at Tekion [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#clickhouse-cloud-at-tekion)


Tekion has successfully integrated ClickHouse Cloud into both platforms mentioned above. In summer 2023 the system was handling approximately 200\+ terabytes of data, a number that continues to grow at pace with the customer base. Within the APM solution, ClickHouse Cloud is used for processing application metrics generated by containers. ClickHouse Cloud streamlines the ingestion process and enables computation of metrics and alerts, including custom metrics tailored to Tekion’s requirements. Tekion can retrieve individual transactions at a much faster pace, comprehensively debug, and analyze data in real\-time.


Additionally, they’ve started to integrate ClickHouse Cloud into custom workflows, which are highly specialized and often lack predefined thresholds. These workflows handle critical operations, where swift detection and response to anomalies is the goal. By transitioning these workflows to ClickHouse Cloud, developers can ingest custom metrics directly which means prompt identification of irregularities and unexpected occurrences, plus a more rapid response time. “Despite the complexity involved we’ve adapted swiftly, and the transition has been smooth. We deactivated ATMs to only store data from a single day,” Surtani explains.



> "ClickHouse has proved to be a game\-changer, propelling us towards greater efficiency and effectiveness in managing our data infrastructure."
> 
> Ved Surtani, VP, Engineering, Platform \& Architecture at Tekion


## Top Benefits of using ClickHouse [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#top-benefits-of-using-clickhouse)


## Storage Optimization [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#storage-optimization)


ClickHouse drastically reduced Tekion storage requirements due to its market\-leading data compression capabilities. The data size for a two\-month period has been minimized from 27TB to just 2\.5TB \- a 10x reduction in storage.


## Ingestion Performance [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#ingestion-performance)


Now, even during peak throughput of 1\.2 million records per minute with ClickHouse, Tekion can ingest without lag. They've eliminated instances where, previously and despite best efforts, a significant number of events were not successfully processed or recorded. What's more, the Spark resources required has reduced by 25% resulting in substantial cost savings. This means faster job execution times, and the ability to process larger datasets with the same infrastructure due to more efficient utilization of resources.


## Query Performance [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#query-performance)


ClickHouse performance allows for significantly faster query execution and retrieval of data even for large datasets, resulting in truly real\-time, interactive experience for the users. Query latency dropped by more than a factor of 10 while lookback doubled \- it’s now at 500 milliseconds when querying up to 14 days, while in the previous set\-up, queries took 8 seconds and then timed\-out after a 7\-day window. Users can now query data over extended time frames and analyze raw data in real\-time, rather than relying on pre\-aggregated formats. It means deeper insights, enabling Tekion to adapt to evolving customer needs and market trends.


## Conclusion [\#](/blog/tekion-adopts-clickhouse-cloud-to-power-application-performance-and-metrics-monitoring#conclusion)


Optimizing observability data stack is an ongoing journey, and a culture of continuous improvement is in Tekion’s DNA. While the team started with migrating APM and Metrics to ClickHouse Cloud, logging, audit reporting, and internal planning dashboards are in consideration for future opportunities to consolidate. Ved closes with: “We really love ClickHouse, and the team talks very highly about support. We'll keep partnering. It's a very interesting technology, it already makes a huge difference and in future we hope to use it more widely.”

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

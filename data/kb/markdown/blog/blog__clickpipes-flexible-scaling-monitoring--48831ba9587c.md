# New: Flexible scaling and enhanced monitoring for streaming ClickPipes


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# New: Flexible scaling and enhanced monitoring for streaming ClickPipes

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[The ClickPipes Team](/authors/clickpipes-team)Jul 30, 2025 · 6 minutes read## Introduction [\#](/blog/clickpipes-flexible-scaling-monitoring#introduction)


Data ingestion workloads come in all shapes and sizes, with more or less predictable patterns. When we built [ClickPipes](https://clickhouse.com/cloud/clickpipes), we wanted to enable customers to handle any throughput, data size and topologies from the most common building blocks of data infrastructure: object storage, message brokers, and databases. Today, hundreds of customers rely on ClickPipes as a cost\-effective solution to manage real\-time data ingestion into ClickHouse Cloud at scale, including [Property Finder](https://clickhouse.com/blog/how-property-finder-migrated-to-clickhouse), [Flock Safety](https://clickhouse.com/blog/why-flock-safety-turned-to-clickhouse), and [Seemplicity](https://clickhouse.com/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse).


As the product evolves, one of the most common requests has been to provide greater flexibility in configuring streaming ClickPipes to better suit the specific needs of these diverse ingestion workloads. In response, we’re introducing **new scaling options** that allow you to control both **horizontal and vertical scaling** for your streaming ClickPipes! You can now choose the number of replicas and replica sizes directly, along with improved monitoring to help you track resource usage over time.


### How does sizing work in streaming ClickPipes? [\#](/blog/clickpipes-flexible-scaling-monitoring#how-does-sizing-work-in-streaming-clickpipes)



> **Note**: database and object storage ClickPipes have a different architecture, which doesn’t require direct control over compute allocation. This new feature applies exclusively to streaming ClickPipes to give customers more control over the cost\-performance ratio per ClickPipe.


ClickPipes works by deploying replica(s) within ClickHouse Cloud, each acting as a consumer of your Kafka or Kinesis streaming data source. By default, ClickPipes starts with a single Extra Small replica (0\.125 vCPU, 512 MiB RAM) to process your data streams. These replicas fetch data in parallel, process and transform it as needed, commit stream offsets, and write the results directly into your ClickHouse service. This architecture enables high\-throughput, scalable ingestion with fault tolerance, and efficient load distribution across replicas.


![unnamed.png](/uploads/unnamed_357981c8a1.png)
### What are replicas? [\#](/blog/clickpipes-flexible-scaling-monitoring#what-are-replicas)


In the context of ClickPipes, replicas are instances of your data processing pipeline that work in parallel to handle the incoming data streams. Each replica acts as a consumer of your Kafka or Kinesis stream, allowing the system to scale efficiently and maintain performance as data volumes grow. Replicas can be scaled both vertically and horizontally to match the specific needs of your workload.


## Flexible scaling options [\#](/blog/clickpipes-flexible-scaling-monitoring#flexible-scaling-options)


We've introduced two new scaling options to provide you with finer control over the topology of streaming ClickPipes: number of replicas (*horizontal scaling*) and replica size (*vertical scaling*). These scaling options can be selected in the UI (shown below) when creating a new ClickPipe or editing an existing one. Scaling is also supported via [OpenAPI](https://clickhouse.com/docs/cloud/manage/api/swagger#tag/ClickPipes/paths/~1v1~1organizations~1%7BorganizationId%7D~1services~1%7BserviceId%7D~1clickpipes~1%7BclickPipeId%7D~1scaling/patch) and [Terraform](https://github.com/ClickHouse/terraform-provider-clickhouse/blob/619ba02fc70e5d672e221f424a9aeedc43fa2d0a/examples/clickpipe/multiple_pipes_example/main.tf).


![unnamed.gif](/uploads/unnamed_8240b37fa9.gif)
### Vertical scaling [\#](/blog/clickpipes-flexible-scaling-monitoring#vertical-scaling)


Vertical scaling, or *scaling up*, involves increasing the resources (CPU and memory) allocated to individual replicas within your ClickPipe. This is ideal for workloads that require more processing power per replica, such as Kafka or Kinesis streams with large payloads or complex schemas. Vertical scaling supports the following configurations:




| Replica size | CPU | Memory |
| --- | --- | --- |
| Extra Small (default) | 0\.125 Cores | 512 Mb |
| Small | 0\.25 Cores | 1 Gb |
| Medium | 0\.5 Cores | 2 Gb |
| Large | 1 Core | 4 Gb |
| Extra Large | 2 Cores | 8 Gb |


### Benchmarks for sizing [\#](/blog/clickpipes-flexible-scaling-monitoring#benchmarks-for-sizing)


Below is a sample performance benchmark for a Large\-sized ClickPipe replica (1 vCPU / 4 GB) ingesting data from a Kafka stream. You can use these benchmarks as a reference point when choosing the appropriate replica size for your workload. For more details and additional sizing guidance, refer to the documentation.




| Replica Size | Message Size | Data Format | Throughput |
| --- | --- | --- | --- |
| Large | 1\.6 kb | JSON | 63 mb/s |
| Large | 1\.6 kb | AVRO | 99 mb/s |


### Horizontal scaling [\#](/blog/clickpipes-flexible-scaling-monitoring#horizontal-scaling)


Horizontal scaling, or *scaling out*, involves adding more replicas to your ClickPipe. This is highly effective for distributing workloads across multiple replicas, allowing your system to handle a higher volume of data concurrently. Kafka and Kinesis efficiently handle horizontal scaling by spreading data across multiple partitions and shards, respectively, which ClickPipes can handle by horizontally scaling proportionally.


## Enhanced resource monitoring [\#](/blog/clickpipes-flexible-scaling-monitoring#enhanced-resource-monitoring)


The details page for each ClickPipe now includes per\-replica CPU and memory usage, showing average resource utilization across replicas. Additionally, the charts show the replicas CPU and memory limits — including *scale up* and *scale out* events — for easier tracking of utilization over time. This helps you better understand your workloads and plan resizing operations with confidence.


![unnamed (1).png](/uploads/unnamed_1_301ef80db2.png)
## How does flexible scaling affect pricing? [\#](/blog/clickpipes-flexible-scaling-monitoring#how-does-flexible-scaling-affect-pricing)


Previously, streaming ClickPipes were priced at a flat rate of $0\.05 per hour for each replica (by default, size Medium). With the introduction of configurable replica sizes, we're making Extra Small the default replica size, and updating our pricing model for streaming ClickPipes: the price now depends on both the replica size and the number of replicas you choose; starting at $0\.0125\. For full pricing details, refer to our [ClickPipes pricing documentation](https://clickhouse.com/docs/cloud/manage/billing/overview#clickpipes-pricing).




| Replica Size | Compute Units | RAM | vCPU | Price/hour (per replica) |
| --- | --- | --- | --- | --- |
| Extra Small | 0\.0625 | 512 MiB | 0\.125 | $0\.0125 |
| Small | 0\.125 | 1 GiB | 0\.25 | $0\.025 |
| Medium | 0\.25 | 2 GiB | 0\.5 | $0\.05 |
| Large | 0\.5 | 4 GiB | 1\.0 | $0\.10 |
| Extra Large | 1\.0 | 8 GiB | 2\.0 | $0\.20 |



> **Note**: In addition to compute charges, ClickPipes incurs a data ingestion cost of $0\.04 per GB. For full pricing details, refer to our [ClickPipes pricing documentation](https://clickhouse.com/docs/cloud/manage/billing/overview#clickpipes-pricing).


## Next Steps [\#](/blog/clickpipes-flexible-scaling-monitoring#next-steps)


With flexible scaling and enhanced resource monitoring, you now have full control over the cost\-performance ratio of your streaming ClickPipes, and can better prepare for changes in your data ingestion workloads. Head over to the [documentation](https://clickhouse.com/docs/integrations/clickpipes) to learn more about how to manage the deployment lifecycle of streaming ClickPipes.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

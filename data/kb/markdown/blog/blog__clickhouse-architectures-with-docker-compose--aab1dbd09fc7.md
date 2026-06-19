# Deploying ClickHouse: Examples from Support Services


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Deploying ClickHouse: Examples from Support Services

![](/_next/image?url=%2Fuploads%2Fantonio_bonuccelli_dd10256481.jpg&w=96&q=75)[Tony Bonuccelli](/authors/tony-bonuccelli)May 2, 2023 · 4 minutes read![Architecture.1S_2R_ReplicatedMergeTree_5-nodes.3.CH.Keeper.nodes.2.CH.nodes.png](/uploads/Architecture_1_S_2_R_Replicated_Merge_Tree_5_nodes_3_CH_Keeper_nodes_2_CH_nodes_eff30f0b05.png)
## Introduction [\#](/blog/clickhouse-architectures-with-docker-compose#introduction)


At ClickHouse Support, we face every day an incredible variety of technical challenges, from query performance reviews to troubleshooting all the possible combinations of configurations that ClickHouse can support.


While ClickHouse Cloud takes the pain out of managing these complex configurations and lets you focus on the fun part of analyzing your datasets, we still understand that running ClickHouse on\-premise is necessary for several reasons, which often depend on which stage of the ClickHouse journey you are at.


As support engineers, we must keep up with all of the features to provide world\-class support to our users. To assist with this, we use docker compose files to quickly replicate specific architectures and configurations. Today, in the spirit of open\-source, we are providing these docker\-compose files to give our users a head start and give you confidence that you are using a tested architecture.


Note: If you are getting started, you can still run a single command to download the ClickHouse binary. For more details, see the [Quick Start](https://clickhouse.com/docs/en/getting-started/quick-start).


The examples described here are for production deployments of ClickHouse beyond a simple single server installation. If you are looking for Docker compose files for multi\-server deployments or guides to go beyond the quick start and, for example, to separate compute and storage or replicate data across two data centers for fault tolerance, continue reading.


## Terminology [\#](/blog/clickhouse-architectures-with-docker-compose#terminology)


The terminology details are in the documentation, but here is the short form:


**Replica**: A replica is a copy of your data. You always have at least one. When you create a table, the initial instance of that table data is the first replica. To survive the loss of a server, a network outage, or other problems, you might want a second replica on a second server.


**Shard**: A shard is a portion of your table data. You also always have at least one shard. We recommend having only one shard until your server is not keeping up with the query load and you cannot scale vertically.


**1S\_2R**: If you look at the diagram at the top of this post, you will see that the cluster is named **cluster\_1S\_2R**. This means that the cluster has one shard and two replicas. **1S\_2R** is a common shorthand used within the ClickHouse community.


### Deployment considerations [\#](/blog/clickhouse-architectures-with-docker-compose#deployment-considerations)


If you are setting up a ClickHouse server to import data for analysis, but the authoritative record is an OLTP database or a set of data files, then you probably only need one shard and one replica (so a single ClickHouse server).


If your data only lives in ClickHouse, and the data can not be recreated or regenerated, then you probably need one shard and two replicas (so two ClickHouse Servers).


The common question is, “How many shards do I need?”. Our answer is, “One until you exceed the capacity of the current hardware and cannot scale your hardware vertically.”


## Details [\#](/blog/clickhouse-architectures-with-docker-compose#details)


The documentation for a single shard with two replicas and for two shards with one replica is at <https://clickhouse.com/docs/en/architecture/introduction>


To separate storage and compute, see [using S3 object storage](https://clickhouse.com/docs/en/integrations/s3#s3-multi-region) and [the same using GCS](https://clickhouse.com/docs/en/integrations/gcs#gcs-multi-region).


More examples are in the [ClickHouse/examples](https://github.com/ClickHouse/examples/blob/main/docker-compose-recipes/README.md) GitHub repo with all of the configuration and Docker compose files. For example:


- Using S3/MinIO object storage with ClickHouse
- ClickHouse and Grafana
- ClickHouse and Vector
- ClickHouse Proxy
- Replication
- Sharding


## More examples [\#](/blog/clickhouse-architectures-with-docker-compose#more-examples)


We always want to hear what the community is experiencing; if you have created an exciting deployment design, please consider opening a pull request in the [ClickHouse documentation repo](https://github.com/ClickHouse/clickhouse-docs/pulls). If pull requests are not your thing or you have a question, [open an issue](https://github.com/ClickHouse/clickhouse-docs/issues) or talk to the [community on Slack](https://clickhouse.com/slack). We look forward to hearing from you!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

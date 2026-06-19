# The Evolution of ClickPipes: Revamped UI/UX, ClickPipes API and Terraform Provider, Prometheus metrics, and more!


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The Evolution of ClickPipes: Revamped UI/UX, ClickPipes API and Terraform Provider, Prometheus metrics, and more!

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[The ClickPipes Team](/authors/clickpipes-team)May 22, 2025 · 6 minutes readSince its inception, ClickPipes has simplified the process of setting up robust continuous data pipelines to ClickHouse Cloud, allowing users to connect sources like Apache Kafka, Amazon S3, Google Cloud Storage, Amazon Kinesis, PostgreSQL, and now MySQL with just a few clicks.


This has enabled organizations to focus more on deriving insights from their data rather than managing complex ingestion processes. As of today, ClickPipes has successfully moved more than **20 trillion rows** to ClickHouse Cloud.


![0_clickpipes.png](/uploads/0_clickpipes_8ccd16e87f.png)
Today, we are introducing a new set of features designed to make ClickPipes a first\-class tool in every developer's toolkit. These capabilities are built to support scale, automation, security, and observability in modern data architectures.


But first, let’s start with usability improvements:


## Revamped UI [\#](/blog/evolution-of-clickpipes#revamped-ui)


The ClickPipes user interface has been redesigned for greater clarity and efficiency. From configuring sources to monitoring pipeline health, every task is now more intuitive and discoverable, with polished UI animations and transitions.


![1_clickpipes.gif](/uploads/1_clickpipes_3969a2a564.gif)
## ClickPipes Editing [\#](/blog/evolution-of-clickpipes#clickpipes-editing)


With support for editing, users can now modify running ClickPipes pipelines without deleting and recreating them. This includes updating ClickPipes names, schema mappings, and connection settings, allowing teams to iterate quickly while maintaining continuity of service.


![2_clickpipes.gif](/uploads/2_clickpipes_9f72aebfd0.gif)
## ClickPipes API and Terraform Provider [\#](/blog/evolution-of-clickpipes#clickpipes-api-and-terraform-provider)


ClickPipes now includes dedicated API endpoints, part of the [ClickHouse Cloud OpenAPI](https://clickhouse.com/docs/cloud/manage/api/api-overview), and a Terraform provider.
These tools support automated management of pipeline configurations and simplify integration into CI/CD pipelines.



```

```
1{
2  "name": "???? I was created using API!",
3  "source": {
4    "kafka": {
5      "type": "confluent",
6      "format": "JSONEachRow",
7      "authentication": "PLAIN",
8      "credentials": {
9        "username": "xxx",
10        "password": "xxx"
11      },
12      "brokers": "{{kafka_broker_url_and_port}}",
13      "topics": "cell_towers"
14    }
15  },
16  "destination": {
17    "database": "default",
18    "table": "my_table",
19    "managedTable": true,
20    "tableDefinition": {
21      "engine": {
22        "type": "MergeTree"
23      }
24    },
25    "columns": [
26      {
27        "name": "area",
28        "type": "Int64"
29      },
30      {
31        "name": "averageSignal",
32        "type": "Int64"
33      }
34    ]
35  }
36}
```

```

With infrastructure as code, teams can consistently deploy and manage ingestion workflows across environments and version pipelines, improving collaboration and automation.
The ClickPipes Terraform provider is available in our official Terraform [registry entry](https://registry.terraform.io/providers/ClickHouse/clickhouse/3.2.0-alpha1/docs/resources/clickpipe) (part of the 3\.2\.0\-alpha1 version at the time of writing).



```

```
1resource "clickhouse_clickpipe" "kafka_clickpipe" {
2  name           = "My Kafka ClickPipe"
3  description    = "Data pipeline from Kafka to ClickHouse"
4
5  service_id     = "e9465b4b-f7e5-4937-8e21-8d508b02843d"
6
7  scaling {
8    replicas = 1
9  }
10
11  state = "Running"
12
13  source {
14    kafka {
15      type = "confluent"
16      format = "JSONEachRow"
17      brokers = "my-kafka-broker:9092"
18      topics = "my_topic"
19
20      consumer_group = "clickpipe-test"
21
22      credentials {
23        username = "user"
24        password = "***"
25      }
26    }
27  }
28
29  destination {
30    table    = "my_table"
31    managed_table = true
32
33    tableDefinition {
34      engine {
35        type = "MergeTree"
36      }
37    }
38
39    columns {
40      name = "my_field1"
41      type = "String"
42    }
43
44    columns {
45      name = "my_field2"
46      type = "UInt64"
47    }
48  }
49
50  field_mappings = [
51    {
52      source_field = "my_field"
53      destination_field = "my_field1"
54    }
55  ]
56}
```

```

**NOTE:** The Terraform Provider is currently not available for Postgres and MySQL CDC ClickPipes.
However, you can manage these ClickPipes via [OpenAPI](https://clickhouse.com/docs/integrations/clickpipes/postgres/faq#can-clickpipe-creation-be-automated-or-done-via-api-or-cli), which is available in Beta.
Terraform support for CDC ClickPipes is planned for later in 2025\.


## AWS PrivateLink Self\-Service [\#](/blog/evolution-of-clickpipes#aws-privatelink-self-service)


We introduced support for AWS PrivateLink within ClickPipes, enabling customers to securely ingest data into ClickHouse Cloud using private network paths.
With this set of features, users can create private endpoints that facilitate direct communication between their AWS Virtual Private Clouds (VPCs) and ClickHouse Cloud.
Additionally, ClickPipes now supports reverse private endpoints, which allow ClickHouse Cloud to securely initiate connections to private customer resources.


![3_clickpipes.png](/uploads/3_clickpipes_810c9f5005.png)
![4_clickpipes.png](/uploads/4_clickpipes_7d6644e2b3.png)
The integration supports popular AWS services, including Amazon RDS, Amazon MSK, and other VPC\-based resources. Configuration is designed to be straightforward, with documentation available to guide users through the setup process. To learn more and get started, refer to the full guide on [AWS PrivateLink for ClickPipes.](https://clickhouse.com/docs/integrations/clickpipes/aws-privatelink)


## Notifications [\#](/blog/evolution-of-clickpipes#notifications)


A built\-in notification system provides real\-time alerts about pipeline activity.
Users can stay updated on ingestion health, failure events, and operational changes.


![5_clickpipes.png](/uploads/5_clickpipes_d4bd32b519.png)
This feature reduces operational blind spots and enables proactive issue resolution. We support receiving notifications through email, ClickHouse Cloud UI, and Slack. More details can be found on the notifications [documentation page](https://clickhouse.com/docs/cloud/notifications).


![6_clickpipes.png](/uploads/6_clickpipes_d207817c7b.png)
## Prometheus Exporter for Observability [\#](/blog/evolution-of-clickpipes#prometheus-exporter-for-observability)


ClickPipes now produces Prometheus metrics, part of the [ClickHouse Cloud Prometheus integration](https://clickhouse.com/docs/integrations/prometheus), making ingestion metrics available for dashboards in Grafana, Datadog, and other observability tools.


![7_clickpipes.png](/uploads/7_clickpipes_7acf55e924.png)
Metrics include ingestion volume (bytes or number of rows) and error counts, giving engineering teams the insight needed to maintain performance. The documentation includes integration guides for [Grafana](https://clickhouse.com/docs/integrations/prometheus#integrating-with-grafana) and [Datadog](https://clickhouse.com/docs/integrations/prometheus#integrating-with-datadog).


## System Tables Centralization [\#](/blog/evolution-of-clickpipes#system-tables-centralization)


Finally, a centralized system table aggregates ClickPipes\-related logs, making it possible to monitor Kafka/Kinesis/S3 pipelines from a single SQL interface, the same way users monitor all the ClickHouse services activity, like merges and queries.


![8_clickpipes.png](/uploads/8_clickpipes_7ef2bbaec6.png)
This design enables users to query pipeline status and health using familiar SQL syntax, build dashboards, and create custom alerts using third\-party tooling. The feature is currently in private preview and will soon be generalized to Kafka/Kinesis/S3 ClickPipes users.


## Why This Matters? [\#](/blog/evolution-of-clickpipes#why-this-matters)


These new capabilities help complete the feature landscape of ClickPipes, taking numerous steps towards a complete ingestion platform for ClickHouse Cloud. Together, they provide:


- A streamlined experience with the revamped UI
- Flexibility with editable pipelines
- Automation through the ClickPipes API and Terraform
- Secure, private connectivity via AWS PrivateLink
- Visibility and alerts through notifications
- Observability with Prometheus and the upcoming centralized system tables


We look forward to hearing your feedback and continuing to evolve ClickPipes to meet your needs.
This release is a major step toward a more automated, observable, and developer\-friendly ingestion experience.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

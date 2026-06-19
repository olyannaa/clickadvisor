---
source: blog
url: https://en.wikipedia.org/wiki/Catalan_Atlas
topic: the-state-of-sql-based-observability
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 13
---

than one visualization tool to offer self\-service visualization capabilities in addition to classic dashboarding. ![img09.png](/uploads/img09_4566662115.png) > We recently estimated the cost savings ratio of LogHouse vs. a leading commercial SaaS observability provider to be a factor of 300

We deployed the stack above at ClickHouse as the centralized logging platform for ClickHouse Cloud code\-named "LogHouse"." It is a multi\-region ClickHouse Cloud deployment that leverages the OpenTelemetry Kubernetes integration for collection, ClickHouse Cloud for storage, and Grafana for dashboarding and log exploration. It currently manages more than 10 Petabytes of telemetry data compressed down to just 600 Terabytes in Clickhouse (an x16 compression ratio!) and successfully serves our logging requirements for all the services we manage. We recently estimated the cost savings ratio of LogHouse vs. a leading commercial SaaS observability provider to be a factor of 300\.

Similarly, many users running large\-scale use cases have already successfully implemented SQL\-based observability pipelines. Examples include:

- [OLAP for Monitoring with ClickHouse on Kubernetes](https://innovation.ebayinc.com/tech/engineering/ou-online-analytical-processing/), at eBay
- [HTTP Analytics for 6M requests per second using ClickHouse](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse/?utm_source=linkedin&utm_medium=social&utm_campaign=blog), at Cloudflare
- [A cost\-effective logging platform using Clickhouse for petabyte scale](https://blog.zomato.com/building-a-cost-effective-logging-platform-using-clickhouse-for-petabyte-scale), at Zomato
- [Fast and Reliable Schema\-Agnostic Log Analytics Platform](https://www.uber.com/en-ES/blog/logging/), at Uber
- [ClickHouse for Observability](https://about.gitlab.com/handbook/engineering/development/ops/monitor/observability/#clickhouse-datastore), at Gitlab
- [LLM Monitoring](https://clickhouse.com/blog/helicones-migration-from-postgres-to-clickhouse-for-advanced-llm-monitoring), at Helicone
- [ClickHouse for OpenTelemetry Traces](https://clickhouse.com/blog/how-we-used-clickhouse-to-store-opentelemetry-traces), at Resmo

ClickHouse is also used as a backend for some of the most popular [Observability SaaS providers](https://clickhouse.com/use-cases/logging-and-metrics) including:

- [Signoz.io](https://clickhouse.com/blog/signoz-observability-solution-with-clickhouse-and-open-telemetry)
- [Highlight.io](https://clickhouse.com/blog/overview-of-highlightio)
- [Qryn](https://qryn.metrico.in/#/)
- [BetterStack](https://betterstack.com/)

## OK, now what’s the catch? [\#](/blog/the-state-of-sql-based-observability#ok-now-whats-the-catch)

While there are the advantages listed in detail in the previous section, the user embarking on the SQL\-based observability journey must be aware of the current limitations to make an informed decision (as of December 2023\).

Observability is traditionally organized into three pillars: Logging, Metrics, and Traces. Based on our experience running ClickHouse for observability at scale for ourselves and with customers, we believe that at the current level of maturity of the ecosystem, Logging and Traces are the two pillars that are the most straightforward to address. We documented these use cases extensively in two previous posts: [logs](https://clickhouse.com/blog/storing-log-data-in-clickhouse-fluent-bit-vector-open-telemetry) and [traces](https://clickhouse.com/blog/storing-traces-and-spans-open-telemetry-in-clickhouse).

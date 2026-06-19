---
source: blog
url: https://clickhouse.com/blog/working-with-time-series-data-and-functions-ClickHouse
topic: building-an-observability-solution-with-clickhouse-part-2-traces
ch_version_introduced: '35.081853291'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 23
---

# Building an Observability Solution with ClickHouse \- Part 2 \- Traces

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building an Observability Solution with ClickHouse \- Part 2 \- Traces

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Mar 29, 2023 · 42 minutes read## Introduction [\#](/blog/storing-traces-and-spans-open-telemetry-in-clickhouse#introduction)

Here at ClickHouse, we consider [Observability to be just another real\-time analytics problem](/resources/engineering/observability-cost-optimization-playbook). As a high\-performance real\-time analytics database, ClickHouse is used for many use cases, including real\-time analytics for [time series](https://clickhouse.com/blog/working-with-time-series-data-and-functions-ClickHouse) data. Its diversity of use cases has helped drive a huge range of [analytical functions](https://clickhouse.com/docs/en/sql-reference/functions/), which assist in querying most data types. These query features and high compression rates have increasingly led users to utilize ClickHouse to store Observability data. This data takes three common forms: logs, metrics, and traces. In this blog, the [second in an Observability series](https://clickhouse.com/blog/storing-log-data-in-clickhouse-fluent-bit-vector-open-telemetry), we explore how trace data can be collected, stored, and queried in ClickHouse.

We have focused this post on using [OpenTelemetry](https://clickhouse.com/engineering-resources/opentelemetry-otel) to collect trace data for storage in ClickHouse. When combined with Grafana, and recent developments in the [ClickHouse plugin](https://github.com/grafana/clickhouse-datasource/pull/329), traces are easily visualized and can be combined with logs and metrics to obtain a deep understanding of your system behavior and performance when detecting and diagnosing issues.

We have attempted to ensure that any examples can be reproduced, and while this post focuses on data collection and visualization basics, we have included some tips on schema optimization. For example purposes, we have forked the [official OpenTelemetry Demo](https://opentelemetry.io/ecosystem/demo/), adding support for ClickHouse and including an OOTB Grafana dashboard for visualizing traces.

## What are Traces? [\#](/blog/storing-traces-and-spans-open-telemetry-in-clickhouse#what-are-traces)

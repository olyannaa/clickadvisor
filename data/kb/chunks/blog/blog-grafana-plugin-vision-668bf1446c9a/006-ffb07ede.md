---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Our
topic: our-vision-for-the-clickhouse-grafana-plugin-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 8
---

editor with your current query pre\-filled. The theme is simple: the common path is simple and intuitive, while more advanced workflows remain close at hand. Nothing is hidden, just kept out of the way until you need it.

Building on this theme, even selecting and working with data sources in Explore today introduces unnecessary friction. Users are required to specify whether they’re working with logs or traces at query time, with a data source capable of supporting either. In most cases, however, users are searching the same type of data.This adds an extra, repetitive step that slows down exploration.

To simplify this, we’re planning a single\-table datasource mode. Configure a datasource for a table with logs, and opening Explore drops you straight into the log search experience with no mode selector or table picker required. Just open Explore, select your datasource, and start searching and analyzing.

## Out of the box dashboards \#

Today, if you deploy the [OpenTelemetry Collector with the ClickHouse exporter](https://clickhouse.com/docs/use-cases/observability/clickstack/ingesting-data/opentelemetry) your data lands in ClickHouse, but you still have to build dashboards from scratch in Grafana. To make the getting started experience simpler, we plan to ship out\-of\-the\-box dashboards for OpenTelemetry and Kubernetes observability use cases that should work immediately with standard schemas.

![](/_next/image?url=%2Fuploads%2Fgrafana_plugin_apr2026_image7_d1806d97b0.png&w=2048&q=75)

The initial set should cover the core observability workflows: a logs dashboard showing volume by severity with a per\-service breakdown; and a trace dashboard with duration distribution and service dependency mapping, per\-service RED metrics (request rate, error rate, duration) and visibility into top spans. Dashboard would also showcase usage of variables and annotations.

![](/_next/image?url=%2Fuploads%2Fgrafana_plugin_apr2026_image4_67b76c885a.png&w=2048&q=75)

The goal is that a team deploying ClickHouse for observability should be able to go from data ingestion to usable dashboards in minutes, not hours, with users able to simply import the dashboards of interest when configuring the datasource.

## Metrics exploration without raw SQL \#

The ClickHouse OpenTelemetry exporter already supports ingesting metrics such as CPU usage, memory, network I/O, and other infrastructure signals from OTel agents and Kubernetes.

The challenge is that exploring this data visually in Grafana often requires writing SQL aggregation queries by hand, which isn’t the experience users expect from metrics\-native data sources.

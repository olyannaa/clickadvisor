---
source: blog
url: http://Buildkite
topic: how-buildkite-transformed-test-analytics-and-cut-costs-with-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 7
---

green light from legal, risk, and finance, they became a paying customer. From there, the team quickly moved from prototyping to rolling out their first ClickHouse\-powered features—marking the start of a transformation in how Test Engine handled analytics.

## Six months later: From pilot to production [\#](/blog/buildkite-test-analytics#six-months-later-from-pilot-to-production)

The first production use case was narrow but powerful: enable real\-time analytics over tagged test events without relying on pre\-computed reports. With ClickHouse Cloud, customers could do things like group P50 test durations by instance type, architecture, or cloud provider and identify patterns like “this newer VM family runs 25% faster for the same price.”

“We were amazed by the query performance,” Gordon says. “That success gave us confidence to shift more of our workloads to ClickHouse, to unlock more analytical capability for our customers, and to bring more consistency to our back end.”

By the time of [Gordon’s Melbourne talk in September 2025](https://clickhouse.com/videos/melbourne-meetup-buildkite-20sep25), ClickHouse had become the analytical backbone of Test Engine’s operation, replacing a patchwork of pre\-aggregations and storage systems with a single, real\-time analytics layer.

![Buildkite User Story Issue 1214.jpg](/uploads/Buildkite_User_Story_Issue_1214_a6c8e7b420.jpg)
Test results flow from customer CI/CD pipelines into ClickHouse Cloud for real\-time analytics.

In the current setup, customers send test results from their CI/CD pipelines, Kafka buffers and propagates those events, Flink handles stateful processing, and the majority of that data lands in ClickHouse Cloud. The Test Engine UI still runs inside Buildkite’s monolithic Ruby on Rails application backed by Postgres, but almost every analytical query now targets ClickHouse.

The numbers tell the story. When Gordon first spoke in February, Test Engine was ingesting around 3 billion test executions per month. Six months later, that had quadrupled to 12 billion, with sustained peaks above 25,000 events per second. “At the moment, we have about 70 billion records in ClickHouse, and that’s just since the beginning of this year,” he says, noting they haven’t even needed [TTL\-based pruning](https://clickhouse.com/docs/guides/developer/ttl) yet.

Importantly, ClickHouse handles both sides of the equation. On the write path, ingesting 25,000 events per second into Postgres was “just not possible really, unless you did a lot of tuning,” Gordon says. “With ClickHouse, it was pretty easy.”

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-musinsa-scaled-its-audience-engine-with-clickhouse-cloud-and-reduced-tco-by-71-4-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 6
---

their 30s,” “people who abandoned a cart in the last seven days”), either by hand or by letting machine learning expand a group to similar users, and reach them through channels like paid ads and targeted push notifications.

In January 2026, Musinsa expanded its CDP with MAI, an AI assistant that lets marketers get statistical data instantly by asking in natural language. The agent also shows the methods and criteria used for data analysis, so users can see how a number was derived rather than just getting the figure.

At [AWS Summit Seoul 2026](https://summitseoul.awslivestream.com/sel-prt103-s/live/), backend engineer Byeonggil Park and data engineer Minyoung Choi shared how Musinsa built the Audience Engine behind its CDP, why the growth it created outpaced their self\-hosted ClickHouse setup, and how migrating to [ClickHouse Cloud](https://clickhouse.com/cloud) on AWS drove benefits across storage, compute, and the company’s real\-time data pipeline.

## The challenges of self\-hosting \#

The Audience Engine is the “most important component of the CDP,” Byeonggil says, the part that takes a condition a marketer enters and returns the group of users who match it.

To make that work, the team stores data in an exploded format, mapping each user to each audience they belong to as a separate row. At Musinsa’s scale, with over 16 million users and 2,500 audiences, that adds up to roughly 1\.1 billion cohort\-to\-user mappings. In the worst case, adding just one audience could mean adding up to 16 million new rows. “Since the data grows exponentially,” Byeonggil says, “we had to think about how to scale both the data and our computing resources.”

For a while, that growth ran on self\-hosted ClickHouse, but keeping it running became increasingly hard to sustain. “With self\-hosted ClickHouse,” Byeonggil explains, “EBS storage and compute were tied to the same node, which made scaling difficult.” Because the specs were fixed, heavy queries strained the system. “There were times when we had to rely on external computing resources,” Minyoung adds. The self\-hosted setup also meant a single cluster had to run multiple workloads at once; with business logic and batch jobs competing for the same resources, an expensive query in one place could drag down everything else.

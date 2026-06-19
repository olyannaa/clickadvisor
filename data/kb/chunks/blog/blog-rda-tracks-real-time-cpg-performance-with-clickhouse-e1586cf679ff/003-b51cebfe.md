---
source: blog
url: https://rda.team/
topic: how-rapid-delivery-analytics-tracks-real-time-cpg-performance-with-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 5
---

paired with TimescaleDB. But it was ultimately built for transactional (OLTP) workloads, not the kind of analytical (OLAP) queries RDA needed to run across billions of rows. “We needed a better way to run OLAP queries,” he says.

Several team members were already familiar with ClickHouse, so they started with a self\-hosted deployment. The results were positive: faster queries, better compression, and a structure that fit their high\-volume, time\-based metrics. They also tested Amazon Redshift as part of the evaluation, but it didn’t stick. “We didn’t find anything that caught our eye,” Andrey says.

While ClickHouse met their performance needs, running it themselves introduced new challenges. Their workloads weren’t static: some jobs required short bursts of intense compute, while others needed to stay lean. “That’s where ClickHouse Cloud entered the chat, so to speak,” Andrey says. “We needed the API to upscale and downscale really fast, so we could run a lot of aggregations, then downscale again.”

ClickHouse Cloud’s flexibility helped unlock new efficiencies. “It’s about cost savings,” Andrey explains. “And it’s about having the extra capacity available anytime, which is really, really helpful when we have something important to do with this amount of data.”

## Real\-time analytics at scale [\#](/blog/rda-tracks-real-time-cpg-performance-with-clickhouse#real-time-analytics-at-scale)

Today, ClickHouse Cloud powers the core of RDA’s analytics engine, from data ingestion and aggregation to the dashboards brands rely on for daily decisions. The platform ingests more than 500 GB of raw data per day, covering 40\+ apps, hundreds of thousands of delivery zones, and billions of product listings. “The amount of data is insane, to be honest,” Andrey says.

ClickHouse plays a central role in processing and aggregating that data efficiently. RDA uses it to calculate key metrics on a daily basis, storing the results in a format optimized for fast access by both internal teams and external users. For clients who need direct access, RDA exports data from ClickHouse to S3, Postgres, or other downstream systems.

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Appcues
topic: appcues-delivers-personalized-customer-engagement-with-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 7
---

outcomes. > “It’s very important that all this information is aggregated and delivered quickly for over a billion user profiles. Page load time has to be practically instant.” > > > — Chris Brookins, VP of Engineering, Appcues

Appcues had spent years running its analytics platform on a stack that included Airflow and Snowflake. While Snowflake remains a strong solution for BI and reporting, delivering the real\-time product analytics experience that customers increasingly expect requires a different approach. At our Boston meetup, Chris shared the journey that ultimately led them to [ClickHouse Cloud](https://clickhouse.com/cloud) on AWS.

## Challenges to delivering a delightful product experience \#

From the beginning, the platform ran on two main databases. DynamoDB handled the sub\-second work of matching live visitors to segments, so Appcues could decide, before the next page load, which experiences to show. Snowflake powered analytics, including dashboards, performance graphs, NPS results, and the reporting customers rely on to tell whether their experiences are actually working.

“Our aim is to create a delightful product experience for our customers,” Chris says. However, as Appcues scaled to ingest more and more data, query times went up to 20 seconds and costs became a challenge to manage as their previous stack wasn’t meant for low\-latency analytics at scale.

To increase query speeds, Appcues relied on Airflow. Every five to 10 minutes, jobs would roll up and pre\-process data before writing it back. This delivered the product experience they were looking for, but it added costs and meant maintaining a growing web of jobs and servers. This setup also meant that customers were limited to looking at data in 10 minute windows.

When the team decided to introduce email, Chris' team knew they needed a new solution that was highly performant for real\-time analytics and cost efficient. “That was a whole new channel with all sorts of new events and extra segmentation needs,” Chris says. Historically, Appcues was optimized to answer a direct, real\-time question: *Which segments does this user belong to*? But with email, they needed to calculate, very quickly, *all the users in a segment*, across hundreds of segments per customer, with complex conditions based on historical behavior and even negative logic like “hasn’t been seen in 30 days.”

## Putting ClickHouse to the test \#

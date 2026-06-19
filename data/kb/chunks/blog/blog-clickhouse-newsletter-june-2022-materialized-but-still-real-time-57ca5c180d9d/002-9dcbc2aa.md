---
source: blog
url: https://clickhouse.com/company/events/v22-6-release-webinar/
topic: clickhouse-newsletter-june-2022-materialized-but-still-real-time
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 5
---

compliant! 5. Lastly, we’ve also added a new setting which (when turned on) causes “inevitable, unavoidable, fatal and life\-threatening performance degradation”. We’ll leave it up to you to find out what it is. Don’t use it in production.

Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.5/), the [recording](https://youtu.be/jkXmXrmjaKQ?t=469) and please upgrade (unless you want to stay on an LTS release).

## **Query of the Month: Materialized, but still real\-time** [\#](/blog/clickhouse-newsletter-june-2022-materialized-but-still-real-time#query-of-the-month-materialized-but-still-real-time)

ClickHouse is often used to store high frequency time series data. For example, financial tick data (prices of stocks, bonds, crypto, etc.) or sensor data.

One of the characteristics of this kind of data is that to get a complete and accurate picture it is often necessary to look potentially far back. For example, not every tick record for a stock is going to have all information needed to display a real\-time summary of a stock on a financial website or mobile app – usually that’s at least the current price as well as most recent open, low/high, 52\-week low/high price and the volume. This is for a variety of reasons, but mostly it’s because much of this data does not change – the open price is the same throughout the day, so there is no reason to include it in every record.

Similarly, an IoT device or sensor might report a variety of metrics, e.g. several temperature values in different places, pressure, voltage, flow rate and/or many other things. This data can often be incomplete at a given point in time – data arrives late, devices go temporarily or permanently offline, not all information is measured all of the time, etc.

To still be able to get an accurate picture of the data using ClickHouse it is often necessary to employ “point\-in\-time queries” that start at a given timestamp – this could be the current time, or at some meaningful point in the past. A common way to write queries in ClickHouse that will find the most recent values for different metrics stored as separate columns is to use the `argMax(arg, val)` function. For a given column `val` it will find the maximum value and return the corresponding `arg` column. With a time series dataset this would be something like `argMax(temp, timestamp)` finding the most recent temperature reading.

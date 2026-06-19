---
source: blog
url: https://supabase.com/blog/postgres-foreign-data-wrappers-rust
topic: adding-real-time-analytics-to-a-supabase-application-with-clickhouse
ch_version_introduced: '0.022'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 13
---

detailed viewing. For this, an OLTP database is perfect. With some familiarity with Postgres and not waiting to host a database ourselves, Supabase was the perfect solution for our application data \- specifically, our current properties for sale.

[Supabase](https://supabase.com) offers a real\-time database that allows developers to store and sync data across multiple devices in real time. Simply put an OSS Firebase alternative. It also provides various backend services, including a serverless platform for running functions and hosting static assets.

With a rich set of clients that don’t require the [user to write SQL](https://supabase.com) (SQL\-injection concerns addressed), as well as row\-level security to limit anonymous users to read access, this provided the perfect solution to storing our current list of around 1000 properties for sale.

With our historical data loaded in ClickHouse Cloud for analytics, we next simply need to choose a web framework. With a basic familiarity of React and not wanting to spend significant time researching possible stacks, I yielded to advice from those at ClickHouse who do web development for more than creating fake estate agency businesses \- NextJS with Tailwinds seemed to be the general recommendation. With three days assigned, I needed to find some actual properties for sale…

## Generating data [\#](/blog/adding-real-time-analytics-to-a-supabase-application#generating-data)

While the historical house price dataset provides us with some basic information regarding the address, price, and date a house was sold, it lacked the information we needed to build a rich, engaging estate agency website \- missing titles, descriptions, and images.

```
SELECT *
FROM uk_price_paid
LIMIT 1
FORMAT Vertical

Row 1:
──────
price: 	1
date:  	1998-06-22 00:00:00
postcode1: CW11
postcode2: 1GS
type:  	detached
is_new:	0
duration:  leasehold
addr1: 	15
addr2:
street:	PENDA WAY
locality:
town:  	SANDBACH
district:  CHESHIRE EAST
county:	CHESHIRE EAST

1 row in set. Elapsed: 0.022 sec. Processed 57.34 thousand rows, 4.31 MB (2.64 million rows/s., 198.59 MB/s.)

```

Selecting 1000 random properties, we projected a 2023 valuation based on their original date of sale and price using the price increase for their property type in their respective postcode \- adding a little variance to ensure some houses seemed better deals than others.

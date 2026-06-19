# ClickHouse Release 23\.6


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 23\.6

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 3, 2023 · 9 minutes readThe release train keeps on rolling.


We are super excited to share a bevy of amazing features in 23\.6\.


And, we already have a date for the 23\.7 release, please [register now](https://clickhouse.com/company/events/v23-7-community-release-call) to join the community call on July 27th at 9 AM (PDT) / 6 PM (CEST).


## Release Summary [\#](/blog/clickhouse-release-23-06#release-summary)


10 new features.
12 performance optimisations.
31 bug fixes.


A small subset of highlighted features are below. But it is worth noting that several features are now production ready or have been enabled by default. You can find those at the end of this post.



## Mongo 6\.x Support [\#](/blog/clickhouse-release-23-06#mongo-6x-support)


If there is one data store that is almost ubiquitous in modern web application stacks, it's MongoDB. MongoDB is a document\-oriented database designed to store and retrieve JSON\-like data. Thanks to its focus on JSON and ease of use, Mongo has proven itself as a Swiss army knife for data storage since its inception in 2009 and a common component in web applications for state storage.


While ClickHouse has supported MongoDB with a table function for some time, Mongo v5\.1 introduced protocol changes that required this integration to be updated. We are now pleased to announce support for Mongo up to the latest v6\.


For users not familiar with ClickHouse table functions, these provide the ability to query external data sources. This is useful for data migration tasks, where data is pulled from a data source and inserted into ClickHouse via an `INSERT INTO SELECT` command, as well as for [populating dictionaries](https://clickhouse.com/docs/en/sql-reference/dictionaries) in ClickHouse. Alternatively, equivalent table engines can be used to expose tables in ClickHouse backed by external stores, which can in turn, be joined with data residing in MergeTree tables.


The [Mongo sample datasets](https://www.mongodb.com/docs/atlas/sample-data/) provide some useful examples to test this feature. Assuming you've [loaded these](https://www.mongodb.com/docs/atlas/sample-data/) into your Mongo or Atlas instance, querying them then becomes trivial with the table function. In the example below, we query the [Airbnb listings dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-airbnb/#sample-airbnb-listings-dataset) (sampling a subset of fields for purposes of brevity), specifying the 'sample\_airbnb' database and 'listingsAndReviews' collection:


*Tip: If querying Mongo Atlas, users need to include the settings `connectTimeoutMS=10000&ssl=true&authSource=admin` as shown below. The connection endpoint exposed for Atlas is also not a valid hostname. The hostname for a database can be determined using the atlas cli and command `atlas process list -o json`.*



```
SELECT listing_url, name, summary
FROM mongodb('<host>:27017', 'sample_airbnb', 'listingsAndReviews', 'default', '<password>', 'listing_url String, name String, summary String, space String, description String, room_type UInt32, bed_type UInt32, minimum_nights UInt32, maximum_nights UInt32, bedrooms UInt16, beds UInt16,number_of_reviews UInt16, amenities Array(String)', 'connectTimeoutMS=10000&ssl=true&authSource=admin')
LIMIT 1
FORMAT Vertical

Row 1:
──────
listing_url: https://www.airbnb.com/rooms/10006546
name:    	Ribeira Charming Duplex
summary: 	Fantastic duplex apartment with three bedrooms, located in the historic area of Porto, Ribeira (Cube) - UNESCO World Heritage Site. Centenary building fully rehabilitated, without losing their original character.

1 row in set. Elapsed: 0.483 sec.

```

*Note: the Decimal128 field in Mongo is currently not supported, preventing us from using the price here. This will be addressed in future releases, along with schema inference.*


This same function can be used to compute aggregations over Mongo, where filters are pushed down to minimize data transfer. In the example below, we compute the average number of beds by room type and number of bedrooms.



```
SELECT room_type, bedrooms, round(avg(beds), 2) AS avg_beds
FROM mongodb('<host>:27017', 'sample_airbnb', 'listingsAndReviews', 'default', '<password>', 'listing_url String, name String, summary String, space String, description String, room_type String, bed_type UInt32, minimum_nights UInt32, maximum_nights UInt32, bedrooms UInt16, beds UInt16,number_of_reviews UInt16, amenities Array(String)', 'connectTimeoutMS=10000&ssl=true&socketTimeoutMS=10000&authSource=admin')
GROUP BY 1, 2
ORDER BY room_type ASC, bedrooms ASC

┌─room_type───────┬─bedrooms─┬─avg_beds─┐
│ Entire home/apt │    	0    │ 	   1.34 │
│ Entire home/apt │    	1    │ 	   1.53 │
│ Entire home/apt │    	2    │ 	   2.81 │
│ Entire home/apt │    	3    │ 	   4.13 │
│ Entire home/apt │    	4    │ 	   5.56 │
│ Entire home/apt │    	5    │ 	   6.26 │
│ Entire home/apt │    	6    │ 	   8.14 │
│ Entire home/apt │    	7    │      8.5 │
│ Entire home/apt │    	8    │ 	   8.67 │
│ Entire home/apt │    	9    │ 	   15.5 │
│ Entire home/apt │   	10   │ 	   14.5 │
│ Private room	  │    	0    │ 	   1.23 │
│ Private room	  │    	1    │ 	   1.25 │
│ Private room	  │    	2    │ 	   2.45 │
│ Private room	  │    	3    │  	2.3 │
│ Private room	  │    	4    │ 	   3.62 │
│ Private room	  │    	5    │  	7.5 │
│ Private room	  │    	6    │    	  7 │
│ Private room	  │    	7    │    	  1 │
│ Private room	  │   	15   │    	  2 │
│ Private room	  │   	20   │   	 25 │
│ Shared room 	  │    	1    │ 	   2.53 │
└─────────────────┴──────────┴──────────┘

22 rows in set. Elapsed: 0.760 sec. Processed 5.55 thousand rows, 149.26 KB (7.31 thousand rows/s., 196.32 KB/s.)

```

The above query can be simplified if we create a table engine for a Mongo instance. This allows us to expose our Mongo collection as a table in ClickHouse. In the example below, we use this to load the dataset into a Mergetree table engine.



```
CREATE TABLE listings_mongo
(
	`listing_url` String,
	`name` String,
	`summary` String,
	`space` String,
	`description` String,
	`room_type` String,
	`bed_type` UInt32,
	`minimum_nights` UInt32,
	`maximum_nights` UInt32,
	`bedrooms` UInt16,
	`beds` UInt16,
	`number_of_reviews` UInt16,
	`amenities` Array(String)
)
ENGINE = MongoDB('<host>:27017', 'sample_airbnb', 'listingsAndReviews', 'default', '<password>', 'connectTimeoutMS=10000&ssl=true&socketTimeoutMS=10000&authSource=admin')

— simpler syntax now possible
SELECT room_type, bedrooms, round(avg(beds), 2) AS avg_beds
FROM listings_mongo
GROUP BY 1, 2
ORDER BY room_type ASC, bedrooms ASC

— migrate data to ClickHouse
CREATE TABLE listings_merge
ENGINE = MergeTree
ORDER BY listing_url AS
SELECT *
FROM listings

Ok.

0 rows in set. Elapsed: 1.369 sec. Processed 5.55 thousand rows, 11.42 MB (4.06 thousand rows/s., 8.34 MB/s.)

```

Finally, Mongo datasets are commonly used as sources for dictionaries. See [here](https://clickhouse.com/docs/en/sql-reference/dictionaries#mongodb) for further details.


## Transform function [\#](/blog/clickhouse-release-23-06#transform-function)


A common problem in data processing is the need to map values \- often codes to something meaningful. This task is best performed in SQL using the [transform function](https://clickhouse.com/docs/en/sql-reference/functions/other-functions#transform). This function has been supported in ClickHouse for some time for numbers, dates, and strings (provided the source and destination values were the same type), with it even used to load the popular UK house price dataset, as shown below. Here we map codes for house types to more readable values at insert time.



```
CREATE TABLE uk_price_paid
(
	price UInt32,
	date Date,
	postcode1 LowCardinality(String),
	postcode2 LowCardinality(String),
	type Enum8('terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4, 'other' = 0),
	is_new UInt8,
	duration Enum8('freehold' = 1, 'leasehold' = 2, 'unknown' = 0),
	addr1 String,
	addr2 String,
	street LowCardinality(String),
	locality LowCardinality(String),
	town LowCardinality(String),
	district LowCardinality(String),
	county LowCardinality(String)
)
ENGINE = MergeTree
ORDER BY (postcode1, postcode2, addr1, addr2);

INSERT INTO uk_price_paid
WITH
   splitByChar(' ', postcode) AS p
SELECT
	toUInt32(price_string) AS price,
	parseDateTimeBestEffortUS(time) AS date,
	p[1] AS postcode1,
	p[2] AS postcode2,
	transform(a, ['T', 'S', 'D', 'F', 'O'], ['terraced', 'semi-detached', 'detached', 'flat', 'other']) AS type,
	b = 'Y' AS is_new,
	transform(c, ['F', 'L', 'U'], ['freehold', 'leasehold', 'unknown']) AS duration, addr1, addr2, street, locality, town, district, county
FROM url(
'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv', 'CSV','uuid_string String, price_string String, time String, postcode String, a String, b String, c String, addr1 String, addr2 String, street String, locality String, town String, district String, county String, d String, e String'
) SETTINGS max_http_get_redirects=10;

```

In 23\.6, we have added support to this function for all data types. The transform function can now be used to transform columns to other types. Types such as DateTime64 and Decimal are also supported, as well as the ability to handle Null values. For a simple example, contrast the differences in the responses below for 23\.5 and 23\.6:



```
--23.5
SELECT transform(number, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], NULL) AS numbers
FROM system.numbers
LIMIT 10

┌─numbers─┐
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
│ ᴺᵁᴸᴸ	  │
└─────────┘

10 rows in set. Elapsed: 0.003 sec.

--23.6
SELECT transform(number, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], NULL) AS numbers
FROM system.numbers
LIMIT 10

┌─numbers─┐
│ zero	  │
│ one 	  │
│ two 	  │
│ three   │
│ four	  │
│ five	  │
│ six 	  │
│ seven   │
│ eight   │
│ nine	  │
└─────────┘

10 rows in set. Elapsed: 0.001 sec.

```

## Sorting Almost Sorted Data [\#](/blog/clickhouse-release-23-06#sorting-almost-sorted-data)


ClickHouse loves sorted data. As a column\-oriented database, sorting data on insert is fundamental to query performance and one of the early concepts users encounter when needing to specify an [`ORDER BY`](https://clickhouse.com/docs/en/sql-reference/statements/select/order-by) clause when creating a table. This clause specifies a list of columns by which data will be sorted on disk, which should align with user access patterns to ensure optimal query performance. While these ordering keys are the first tool for every ClickHouse user to tune performance, it remains unrealistic to specify all columns here. Despite this, some columns are naturally sorted and aligned with these sorting keys.


In 23\.6, ClickHouse will now exploit any natural sorting patterns in the data to improve query performance. This is particularly in cases where a column is known to be monotonically increasing in most cases but is not part of the ordering key.


## New Contributors [\#](/blog/clickhouse-release-23-06#new-contributors)


A special welcome to all the new contributors to 23\.6! ClickHouse's popularity is, in large part, due to the efforts of the community who contributes. Seeing that community grow is always humbling.


If you see your name here, please reach out to us...but we will be finding you on twitter, etc as well.



> Chang Chen, Dmitry Kardymon, Hongbin Ma, Julian Maicher, Thomas Panetti, YalalovSM, kevinyhzou, tpanetti, 郭小龙

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

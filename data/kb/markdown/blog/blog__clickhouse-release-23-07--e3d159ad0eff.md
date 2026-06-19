# ClickHouse Release 23\.7


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 23\.7

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 29, 2023 · 9 minutes readThe release train keeps on rolling.


We are super excited to share a bevy of amazing features in 23\.7


And, we already have a date for the 23\.8 release, please [register now](https://clickhouse.com/company/events/v23-8-community-release-call) to join the community call on August 31st at 9 AM (PDT) / 6 PM (CEST).


## Release Summary [\#](/blog/clickhouse-release-23-07#release-summary)


31 new features.   

16 performance optimisations.   

47 bug fixes.


A small subset of highlighted features are below. But it is worth noting that several features are now production ready or have been enabled by default. You can find those at the end of this post.


## New Contributors [\#](/blog/clickhouse-release-23-07#new-contributors)


A special welcome to all the new contributors to 23\.7! ClickHouse's popularity is, in large part, due to the efforts of the community who contributes. Seeing that community grow is always humbling.


If you see your name here, please reach out to us...but we will be finding you on twitter, etc as well.



> Alex Cheng, AlexBykovski, Chen768959, John Spurlock, Mikhail Koviazin, Rory Crispin, Samuel Colvin, Sanjam Panda, Song Liyong, StianBerger, Vitaliy Pashkov, Yarik Briukhovetskyi, Zach Naimon, chen768959, dheerajathrey, lcjh, pedro.riera, therealnick233, timfursov, velavokr, xiao, xiaolei565, xuelei, yariks5s



## Parquet writing improvements (Michael Kolupaev) [\#](/blog/clickhouse-release-23-07#parquet-writing-improvements-michael-kolupaev)


Recent months have seen numerous read improvements for the Parquet file format in ClickHouse. As well as parallelizing [reads across row groups](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups#parallelized-reads) and [utilizing metadata for filtering](https://github.com/ClickHouse/ClickHouse/pull/52951), we’ve even taken the time to ensure queries on [Hugging Face datasets are optimized](https://github.com/ClickHouse/ClickHouse/pull/53281). We understand that this file format is ubiquitous and often fundamental for tasks such as local analysis using clickhouse\-local and data migrations. Our continued commitment to improving our Parquet support and obsession with speed, has paid dividends and been reflected in the recent improvements in our [public benchmarks](https://benchmark.clickhouse.com/#eyJzeXN0ZW0iOnsiQXRoZW5hIChwYXJ0aXRpb25lZCkiOmZhbHNlLCJBdGhlbmEgKHNpbmdsZSkiOmZhbHNlLCJBdXJvcmEgZm9yIE15U1FMIjpmYWxzZSwiQXVyb3JhIGZvciBQb3N0Z3JlU1FMIjpmYWxzZSwiQnlDb25pdHkiOmZhbHNlLCJCeXRlSG91c2UiOmZhbHNlLCJjaERCIjpmYWxzZSwiQ2l0dXMiOmZhbHNlLCJDbGlja0hvdXNlIChkYXRhIGxha2UsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsIkNsaWNrSG91c2UgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6dHJ1ZSwiQ2xpY2tIb3VzZSAoUGFycXVldCwgc2luZ2xlKSI6dHJ1ZSwiQ2xpY2tIb3VzZSAod2ViKSI6ZmFsc2UsIkNsaWNrSG91c2UiOmZhbHNlLCJDbGlja0hvdXNlICh0dW5lZCkiOmZhbHNlLCJDbGlja0hvdXNlICh6c3RkKSI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQgKEFXUykiOmZhbHNlLCJDbGlja0hvdXNlIENsb3VkIChHQ1ApIjpmYWxzZSwiQ3JhdGVEQiI6ZmFsc2UsIkRhdGFiZW5kIjpmYWxzZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgc2luZ2xlKSI6dHJ1ZSwiQXBhY2hlIERvcmlzIjpmYWxzZSwiRHJ1aWQiOmZhbHNlLCJEdWNrREIgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6dHJ1ZSwiRHVja0RCIjpmYWxzZSwiRWxhc3RpY3NlYXJjaCI6ZmFsc2UsIkVsYXN0aWNzZWFyY2ggKHR1bmVkKSI6ZmFsc2UsIkdyZWVucGx1bSI6ZmFsc2UsIkhlYXZ5QUkiOmZhbHNlLCJIeWRyYSI6ZmFsc2UsIkluZm9icmlnaHQiOmZhbHNlLCJLaW5ldGljYSI6ZmFsc2UsIk1hcmlhREIgQ29sdW1uU3RvcmUiOmZhbHNlLCJNYXJpYURCIjpmYWxzZSwiTW9uZXREQiI6ZmFsc2UsIk1vbmdvREIiOmZhbHNlLCJNeVNRTCAoTXlJU0FNKSI6ZmFsc2UsIk15U1FMIjpmYWxzZSwiUGlub3QiOmZhbHNlLCJQb3N0Z3JlU1FMICh0dW5lZCkiOmZhbHNlLCJQb3N0Z3JlU1FMIjpmYWxzZSwiUXVlc3REQiAocGFydGl0aW9uZWQpIjpmYWxzZSwiUXVlc3REQiI6ZmFsc2UsIlJlZHNoaWZ0IjpmYWxzZSwiU2VsZWN0REIiOmZhbHNlLCJTaW5nbGVTdG9yZSI6ZmFsc2UsIlNub3dmbGFrZSI6ZmFsc2UsIlNRTGl0ZSI6ZmFsc2UsIlN0YXJSb2NrcyI6ZmFsc2UsIlRpbWVzY2FsZURCIChjb21wcmVzc2lvbikiOmZhbHNlLCJUaW1lc2NhbGVEQiI6ZmFsc2V9LCJ0eXBlIjp7InN0YXRlbGVzcyI6dHJ1ZSwibWFuYWdlZCI6dHJ1ZSwiSmF2YSI6dHJ1ZSwiY29sdW1uLW9yaWVudGVkIjp0cnVlLCJDKysiOnRydWUsIk15U1FMIGNvbXBhdGlibGUiOnRydWUsInJvdy1vcmllbnRlZCI6dHJ1ZSwiQyI6dHJ1ZSwiUG9zdGdyZVNRTCBjb21wYXRpYmxlIjp0cnVlLCJDbGlja0hvdXNlIGRlcml2YXRpdmUiOnRydWUsImVtYmVkZGVkIjp0cnVlLCJzZXJ2ZXJsZXNzIjp0cnVlLCJhd3MiOnRydWUsImdjcCI6dHJ1ZSwiUnVzdCI6dHJ1ZSwic2VhcmNoIjp0cnVlLCJkb2N1bWVudCI6dHJ1ZSwidGltZS1zZXJpZXMiOnRydWV9LCJtYWNoaW5lIjp7InNlcnZlcmxlc3MiOnRydWUsIjE2YWN1Ijp0cnVlLCJjNmEuNHhsYXJnZSwgNTAwZ2IgZ3AyIjp0cnVlLCJMIjp0cnVlLCJNIjp0cnVlLCJTIjp0cnVlLCJYUyI6dHJ1ZSwiYzZhLm1ldGFsLCA1MDBnYiBncDIiOnRydWUsImM1bi40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsImM1LjR4bGFyZ2UsIDUwMGdiIGdwMiI6dHJ1ZSwiMTkyR0IiOnRydWUsIjI0R0IiOnRydWUsIjM2MEdCIjp0cnVlLCI0OEdCIjp0cnVlLCI3MjBHQiI6dHJ1ZSwiOTZHQiI6dHJ1ZSwiNzA4R0IiOnRydWUsIm01ZC4yNHhsYXJnZSI6dHJ1ZSwibTZpLjMyeGxhcmdlIjp0cnVlLCJjNmEuNHhsYXJnZSwgMTUwMGdiIGdwMiI6dHJ1ZSwiZGMyLjh4bGFyZ2UiOnRydWUsInJhMy4xNnhsYXJnZSI6dHJ1ZSwicmEzLjR4bGFyZ2UiOnRydWUsInJhMy54bHBsdXMiOnRydWUsIlMyIjp0cnVlLCJTMjQiOnRydWUsIjJYTCI6dHJ1ZSwiM1hMIjp0cnVlLCI0WEwiOnRydWUsIlhMIjp0cnVlfSwiY2x1c3Rlcl9zaXplIjp7IjEiOnRydWUsIjIiOnRydWUsIjQiOnRydWUsIjgiOnRydWUsIjE2Ijp0cnVlLCIzMiI6dHJ1ZSwiNjQiOnRydWUsIjEyOCI6dHJ1ZSwic2VydmVybGVzcyI6dHJ1ZSwidW5kZWZpbmVkIjp0cnVlfSwibWV0cmljIjoiaG90IiwicXVlcmllcyI6W3RydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWVdfQ==).


![benchmark_23_7.png](/uploads/benchmark_23_7_21ca5bbf57.png)
Of course reading Parquet is only half the story. Users invariably need to write ClickHouse data to Parquet, often as part of a reverse ETL workflow or need to share the results of a data analysis. We’re therefore delighted to announce Parquet writing is now up to 6x faster as of 23\.7\.


Let's consider an example using the [UK house price data](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid) to illustrate. Below we use `clickhouse-local` and import the data from an existing publically S3 hosted Parquet file.



```
CREATE TABLE uk_house_price
ENGINE = MergeTree
ORDER BY (postcode1, postcode2, addr1, addr2)
SETTINGS allow_nullable_key = 1 AS
SELECT *
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/uk-house-prices/parquet/house_prices.parquet')

0 rows in set. Elapsed: 40.550 sec. Processed 28.28 million rows, 4.67 GB (697.33 thousand rows/s., 115.15 MB/s.)

```

Exporting this dataset with 23\.6 is still impressively fast at almost 1\.5million row/sec.



```
SELECT *
FROM uk_house_price
INTO OUTFILE 'london-prices.parquet'

28276228 rows in set. Elapsed: 19.901 sec. Processed 28.20 million rows, 4.66 GB (1.42 million rows/s., 233.98 MB/s.)

```

Exporting the same dataset using 23\.7 shows a dramatic improvement, almost halving the total time! Your mileage will vary here, with improvements seen up to 6x.



```
SELECT *
FROM uk_house_price
INTO OUTFILE 'london-prices.parquet'
28276228 rows in set. Elapsed: 11.649 sec. Processed 28.24 million rows, 4.66 GB (2.42 million rows/s., 400.39 MB/s.)

```

## Sparse columns enabled by default (Anton Popov) [\#](/blog/clickhouse-release-23-07#sparse-columns-enabled-by-default-anton-popov)


Sparse columns have been a feature of ClickHouse [for some time](https://clickhouse.com/blog/whats-new-in-clickhouse-22-1#sparse-encoding-for-columns), but prior to 23\.7 needed to be explicitly enabled. This optimization aims to reduce the total data written for a column, by dynamically changing the encoded format when a high number of default values are detected. As well as improving compression, this has the advantage of improving query performance and memory efficiency.


With 23\.7 this feature is enabled by default. Users should see immediate improvements in compression and performance where this encoding can be applied.


When writing a data part (at either insert or merge time), ClickHouse computes the ratio of default values for each column. If this exceeds the configured threshold, only the non\-default values for the column are written. To preserve which rows have a default value, a separate stream is written containing an encoding of the offsets. This information is combined at query time, ensuring the optimization is completely transparent to the user. The following diagram shows an example of this:


![sparse_columns.png](/uploads/sparse_columns_b0922ab125.png)
*For a ① column `s` containing sparse values, ClickHouse only writes the non\-default values into ② a column file on disk, together with ③ an additional file containing a sparse encoding of the non\-default value offsets: For each non\-default value, we store how many default values are present directly before the non\-default value. At query time, we create an ④ in\-memory representation with direct offsets from this encoding. The sparse encoded on\-storage variant contains data with repeated values.*
Prior to 23\.7, users were required to explicitly enable Sparse columns by modifying the setting that controls the required threshold for the Sparse column encoding to be used \- [ratio\_of\_defaults\_for\_sparse\_serialization](https://clickhouse.com/docs/zh/operations/settings/merge-tree-settings#ratio_of_defaults_for_sparse_serialization). This defaulted to a value of 1\.0, which effectively disabled the feature. In 23\.7, this value defaults to 0\.9375\.


While we expect sparse columns to benefit even highly structured data, we expect larger improvements for use cases where users insert data with less strict schemas e.g. JSON with highly variable keys. In these cases, users will pay almost no overhead for having a column which only has values for a few rows \- potentially allowing significant space savings.


While we expected improvements in our public ClickBench benchmarks, the scale of the benefits from enabling this optimization by default was [a pleasant surprise](https://pastila.nl/?00c2279f/0f8724ee7e39d8abfcb76ebad2f7f382.html).


![benchmark_2_23_7.png](/uploads/benchmark_2_23_7_3af0e4b9ea.png)
## Experimental support for PRQL (János Benjamin Antal) [\#](/blog/clickhouse-release-23-07#experimental-support-for-prql-j%C3%A1nos-benjamin-antal)


At ClickHouse, we hold the conviction that SQL stands as the godfather among all query languages, with the power to tackle virtually any data problem. Throughout time, numerous languages have vied to rival or supplant SQL, yielding varied degrees of success. Fresh query languages emerge rapidly, but often fade away just as quickly. The endurance of SQL and its incorporation into many data storage systems across successive versions stands as a testament to its lasting significance. Nevertheless, we also acknowledge the importance of engaging users on familiar ground and recognize that some languages are better suited to use cases than others. If we see sufficient adoption and demand for a query language we can consider adding support and always welcome community PRs! Thanks to such a community contribution, PRQL is now supported in ClickHouse as an experimental feature.


[PRQL](https://prql-lang.org/) (Pipelined Relational Query Language) pronounced “Prequel”, positions itself as “a simple, powerful, pipelined SQL replacement”. The pipeline nature of the [syntax has proved popular](https://github.com/PRQL/prql), with a growing community of contributors. By chaining transformations to form pipelines, otherwise complex SQL queries can be elegantly composed. At ClickHouse we can see how this style of query construction has some potentially interesting applications, especially in use cases where users conduct search and discovery exercises \- Observability maybe?


As well as being [well documented](https://prql-lang.org/book/), users can experiment with a [public playground](https://prql-lang.org/playground/). Let's consider a few simple examples using the UK house price dataset. Suppose wish to highest districts in in London



```
from uk_house_price

filter town == 'LONDON'
group district (              	
  aggregate {                    	
	avg_price = average price
  }
)
sort {-avg_price}
take 1..10


SELECT
	district,
	AVG(price) AS avg_price
FROM uk_house_price
WHERE town = 'LONDON'
GROUP BY district
ORDER BY avg_price DESC
LIMIT 10

┌─district───────────────┬──────────avg_price─┐
│ CITY OF LONDON     	 │  2016389.321229964 │
│ CITY OF WESTMINSTER	 │  1107261.809839673 │
│ KENSINGTON AND CHELSEA │ 1105730.3371717487 │
│ CAMDEN             	 │  752077.7613715645 │
│ RICHMOND UPON THAMES   │  644835.3877018511 │
│ HAMMERSMITH AND FULHAM │  590308.6679440506 │
│ HOUNSLOW           	 │  574833.3599378078 │
│ ISLINGTON          	 │   531522.146523729 │
│ HARLOW             	 │         	   500000 │
│ WANDSWORTH         	 │  464798.7692006684 │
└────────────────────────┴────────────────────┘

10 rows in set. Elapsed: 0.079 sec.

```

As shown, ClickHouse provides us with the equivalent SQL statement that the PRQL query has been compiled to.


A query which might be more challenging for less experienced SQL users is to find the highest row, for a specific column, per group. For example, below we find the most expensive house per postcode in the UK sorted by price.



```
from uk_house_price
filter town == 'LONDON'
filter postcode1 != ''
select {  
  postcode1, street, price
}
group postcode1 (     		 
  sort {-price}
  take 1
)		 
sort {-price}
take 1..10

WITH table_0 AS
	(
    	SELECT
        	postcode1,
        	street,
        	price
    	FROM uk_house_price
    	WHERE (town = 'LONDON') AND (postcode1 != '')
    	ORDER BY
        	postcode1 ASC,
        	price DESC
    	LIMIT 1 BY postcode1
	)
SELECT
	postcode1,
	street,
	price
FROM table_0
ORDER BY price DESC
LIMIT 10

┌─postcode1─┬─street──────────┬─────price─┐
│ W1U   	│ BAKER STREET	  │ 594300000 │
│ W1J   	│ STANHOPE ROW	  │ 569200000 │
│ SE1   	│ SUMNER STREET   │ 448500000 │
│ E1    	│ BRAHAM STREET   │ 421364142 │
│ EC2V  	│ GRESHAM STREET  │ 411500000 │
│ SE10  	│ WATERVIEW DRIVE │ 400000000 │
│ EC1Y  	│ MALLOW STREET   │ 372600000 │
│ SW1H  	│ BROADWAY    	  │ 370000000 │
│ W1S   	│ NEW BOND STREET │ 366180000 │
│ EC4V  	│ CARTER LANE 	  │ 337000000 │
└───────────┴─────────────────┴───────────┘

10 rows in set. Elapsed: 0.498 sec. Processed 25.32 million rows, 574.02 MB (50.83 million rows/s., 1.15 GB/s.)
Peak memory usage: 60.70 MiB.

```

The brevity of the above query vs the equivalent SQL is quite compelling.


As a language which compiles to SQL, we’re excited to see how PRQL develops and the use cases it's applied to with ClickHouse. Let us know if you’ve found the PRQL useful and the problems it has allowed you to solve!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

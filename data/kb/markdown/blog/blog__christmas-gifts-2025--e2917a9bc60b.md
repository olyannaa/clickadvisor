# Christmas gifts from the ClickHouse engineering team


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Christmas gifts from the ClickHouse engineering team

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Jan 20, 2026 · 9 minutes readAt the end of every year, the ClickHouse engineering team works on some features that we call [Christmas gifts](https://github.com/ClickHouse/ClickHouse/pulls?q=is:pr+label:%22%F0%9F%8E%85+%F0%9F%8E%81+gift%F0%9F%8E%84%22+is:closed%20). These are features with a clear visible improvement, usability features, or long\-awaited things.


In this blog post, we’re going to go through some of our favorites.



> And don’t forget, you can see release posts for every release in 2025 via the links below:  
> 
> [25\.1](https://clickhouse.com/blog/clickhouse-release-25-01), [25\.2](https://clickhouse.com/blog/clickhouse-release-25-02), [25\.3 LTS](https://clickhouse.com/blog/clickhouse-release-25-03), [25\.4](https://clickhouse.com/blog/clickhouse-release-25-04), [25\.5](https://clickhouse.com/blog/clickhouse-release-25-05), [25\.6](https://clickhouse.com/blog/clickhouse-release-25-06), [25\.7](https://clickhouse.com/blog/clickhouse-release-25-07), [25\.8 LTS](https://clickhouse.com/blog/clickhouse-release-25-08), [25\.9](https://clickhouse.com/blog/clickhouse-release-25-09), [25\.10](https://clickhouse.com/blog/clickhouse-release-25-10), [25\.11](https://clickhouse.com/blog/clickhouse-release-25-11), [25\.12](https://clickhouse.com/blog/clickhouse-release-25-12)


## Highlight digit groups inside numbers in the query prompt [\#](/blog/christmas-gifts-2025#highlight-digit-groups-inside-numbers-in-the-query-prompt)


### Contributed by Alexey Milovidov [\#](/blog/christmas-gifts-2025#contributed-by-alexey-milovidov)


Digit groups inside numbers in query prompts are now highlighted in a similar way that numbers are formatted in results.


You can see an example of how this works in the video below:

Loading video...## Numeric hint when last column and enough horizontal space [\#](/blog/christmas-gifts-2025#numeric-hint-when-last-column-and-enough-horizontal-space)


### Contributed by Cole Smith [\#](/blog/christmas-gifts-2025#contributed-by-cole-smith)


Since [ClickHouse 24\.2](https://clickhouse.com/blog/clickhouse-release-24-02#pretty-format-is-even-prettier), when you return a single numerical column, if the value in that column is bigger than 1 million, the readable quantity will be displayed as a comment alongside the value itself.



```

```
1SELECT 277282240574747
```

```


```
┌─arrayJoin([277282240574747])─┐
│              277282240574747 │ -- 277.28 trillion
└──────────────────────────────┘

```

But if we returned multiple values, it wouldn’t show the numeric hint:



```

```
1SELECT arrayJoin([
2 277282240574747, 
3 2772822, 
4 1543210
5]);
```

```


```
┌─arrayJoin([2⋯, 1543210])─┐
│          277282240574747 │
│                  2772822 │
│                  1543210 │
└──────────────────────────┘

```

Now we’ll get the numeric hint for every row as long as there’s enough horizontal space:



```
┌─arrayJoin([2⋯, 1543210])─┐
│          277282240574747 │ -- 277.28 trillion
│                  2772822 │ -- 2.77 million
│                  1543210 │ -- 1.54 million
└──────────────────────────┘

```

## Optimize distinctJSONPaths aggregate function [\#](/blog/christmas-gifts-2025#optimize-distinctjsonpaths-aggregate-function)


### Contributed by Pavel Kruglov [\#](/blog/christmas-gifts-2025#contributed-by-pavel-kruglov)


The [distinctJSONPaths](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/distinctjsonpaths) function returns the set of unique JSON paths present in a JSON column.


Starting with ClickHouse 25\.12, this function is significantly optimized. Instead of scanning and decoding the [full internal JSON column representation](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#true-columnar-json-storage), ClickHouse now relies on metadata that is already maintained at data\-part level.


Each data part tracks the set of JSON paths it contains. When distinctJSONPaths is executed, ClickHouse simply reads and merges this metadata across parts, without accessing the JSON column data itself.


Let’s see the performance impact using the BlueSky dataset. The following query ingests 10 million rows into a table:



```

```
1CREATE TABLE bluesky
2ORDER BY ()
3AS
4SELECT *
5FROM s3(
6  'https://clickhouse-public-datasets.s3.amazonaws.com' ||
7  '/bluesky/file_{0001..0010}.json.gz',
8  'JSONAsObject'
9)
10SETTINGS
11    input_format_allow_errors_num = 100,
12    input_format_allow_errors_ratio = 1;
```

```

We’re going to compute the distinct JSON paths in this dataset by running the following query:



```

```
1SELECT length(distinctJSONPaths(json)) 
2FROM bluesky;
```

```

If we run this query three times in ClickHouse 25\.11:



```
┌─length(disti⋯aths(json))─┐
│                      224 │
└──────────────────────────┘

1 row in set. Elapsed: 4.978 sec. Processed 9.97 million rows, 21.21 GB (2.00 million rows/s., 4.26 GB/s.)
Peak memory usage: 1.24 GiB.

1 row in set. Elapsed: 4.563 sec. Processed 9.99 million rows, 21.26 GB (2.19 million rows/s., 4.66 GB/s.)
Peak memory usage: 1.26 GiB.

1 row in set. Elapsed: 4.926 sec. Processed 9.94 million rows, 21.14 GB (2.02 million rows/s., 4.29 GB/s.)
Peak memory usage: 1.24 GiB.

```

And then three times in ClickHouse 25\.12:



```
┌─length(disti⋯aths(json))─┐
│                      224 │
└──────────────────────────┘

1 row in set. Elapsed: 0.082 sec.

1 row in set. Elapsed: 0.099 sec.

1 row in set. Elapsed: 0.100 sec.

```

Our fastest result goes from 4\.563 seconds to 82 milliseconds, an improvement of more than 50 times.


## Optimize DISTINCT transform for LowCardinality Columns [\#](/blog/christmas-gifts-2025#optimize-distinct-transform-for-lowcardinality-columns)


### Contributed by Nihal Z. Miaji [\#](/blog/christmas-gifts-2025#contributed-by-nihal-z-miaji)


[LowCardinality](https://clickhouse.com/docs/sql-reference/data-types/lowcardinality) columns store values using [**dictionary encoding**](https://en.wikipedia.org/wiki/Dictionary_coder): each distinct value is stored once in a dictionary, and rows reference it by a small integer ID.


Starting with ClickHouse 25\.12, `DISTINCT` queries on LowCardinality columns are optimized to **exploit this dictionary representation**.


Instead of scanning all rows and comparing full values, ClickHouse operates directly on the **dictionary IDs**:


- It tracks which dictionary entries have already been seen
- Each dictionary value is returned at most once
- The scan can stop early once all dictionary entries are encountered


As a result, the cost of DISTINCT depends primarily on the **dictionary size**, not the number of rows.


Let’s have a look at the effect with the [UK property prices dataset](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid). This dataset has the following columns with the `LowCardinality` type:



```
postcode1 LowCardinality(String)
postcode2 LowCardinality(String)
street LowCardinality(String)
locality LowCardinality(String)
town LowCardinality(String)
district LowCardinality(String)
county LowCardinality(String)

```

We’re going to run the following query three times against each column:



```

```
1SELECT DISTINCT 
2FROM uk.uk_price_paid
3FORMAT NULL;
```

```

For each of the fields on 25\.11 and 25\.12, record the fastest time. You can see the results in the table below:




| Field | Unique values | 25\.11 | 25\.12 |
| --- | --- | --- | --- |
| postcode1 | 2,392 | 0\.017 sec | 0\.033 sec |
| postcode2 | 4,005 | 0\.121 sec | 0\.043 sec |
| street | 334,642 | 0\.186 sec | 0\.084 sec |
| locality | 24,001 | 0\.149 sec | 0\.070 sec |
| town | 1,172 | 0\.141 sec | 0\.046 sec |
| district | 467 | 0\.144 sec | 0\.046 sec |
| county | 132 | 0\.141 sec | 0\.023 sec |


We can see that the optimization results in a faster query for every column except `postcode1`.


The sorting key for this table is `(postcode1, postcode2, addr1, addr2)`, which explains why the optimization isn’t as effective on the `postcode1` column.


The "early exit" optimization assumes you'll discover all unique values early. But when doing `DISTINCT` on `postcode1`, the unique values are spread from beginning to end by definition. We have to scan (almost) everything.


Therefore, for `postcode1`, we pay the overhead of tracking dictionary indices while still scanning nearly the full column, making it slower than the previous approach of scanning all rows.


## Use equivalent sets to push down filter for SEMI JOIN [\#](/blog/christmas-gifts-2025#use-equivalent-sets-to-push-down-filter-for-semi-join)


### Contributed by Dmitry Novik [\#](/blog/christmas-gifts-2025#contributed-by-dmitry-novik)


A semi join is a way of filtering a rowset based on the existence of its rows in another rowset.


A `LEFT SEMI JOIN` returns rows from the left table where matching rows exist in the right table. A `RIGHT SEMI JOIN` returns rows from the right table where matching rows exist in the left table.



> You can read a more detailed explanation in [part 1 of our series on ClickHouse joins](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1#left--right-semi-join).


Let’s have a look at an example of each type of semi join, starting with `LEFT SEMI JOIN`:



```

```
1-- Return users who have orders
2SELECT * FROM users 
3LEFT SEMI JOIN orders ON users.id = orders.user_id
```

```

And `RIGHT SEMI JOIN`:



```

```
1-- Return orders that have matching users
2SELECT * FROM users 
3RIGHT SEMI JOIN orders ON users.id = orders.user_id
```

```

ClickHouse 25\.12 optimizes `SEMI JOIN` queries by pushing filters down earlier in the query execution. This means that when you have a SEMI JOIN with filter conditions, the optimizer can now push those filters down to the table scan level using "equivalent column sets" \- columns that are known to be equal through the join condition.


Without filter pushdown, you might scan the entire right (or left) table before filtering. With this optimization, you filter first, then check existence against a smaller dataset.


Let’s have a look at how this optimization works with help from the UK property prices dataset. The following query finds 2023 sales where the property also sold in 2022



```

```
1SELECT DISTINCT street, town, postcode1, date, price
2  FROM uk_price_paid p1
3  LEFT SEMI JOIN uk_price_paid p2
4    ON p1.addr1 = p2.addr1
5    AND p1.street = p2.street
6    AND p1.postcode1 = p2.postcode1
7    AND p2.date BETWEEN '2022-01-01' AND '2022-12-31'
8  WHERE p1.date BETWEEN '2023-01-01' AND '2023-12-31'
9  ORDER BY p1.price DESC
10  LIMIT 10;
```

```


```
┌─street────────────┬─town─────────┬─postcode1─┬───────date─┬────price─┐
│ MOULSECOOMB WAY   │ BRIGHTON     │ BN2       │ 2023-05-03 │ 97483948 │
│ GLEBE PLACE       │ LONDON       │ SW3       │ 2023-10-18 │ 68250000 │
│ THREE QUEENS LANE │ BRISTOL      │ BS1       │ 2023-12-28 │ 55859292 │
│ MARGATE ROAD      │ BROADSTAIRS  │ CT10      │ 2023-04-20 │ 54077847 │
│ BATH ROAD         │ WEST DRAYTON │ UB7       │ 2023-10-20 │ 54000000 │
│ PARK STREET       │ LONDON       │ W1K       │ 2023-09-07 │ 52625000 │
│ LINKS ROAD        │ MORPETH      │ NE65      │ 2023-02-28 │ 50090677 │
│ BILTON WAY        │ ENFIELD      │ EN3       │ 2023-08-18 │ 50017255 │
│ OLYMPIC WAY       │ WEMBLEY      │ HA9       │ 2023-08-04 │ 43096020 │
│ BLACKACRE ROAD    │ IPSWICH      │ IP6       │ 2023-11-14 │ 36990000 │
└───────────────────┴──────────────┴───────────┴────────────┴──────────┘

```

If we run this query against 25\.11:



```
10 rows in set. Elapsed: 1.134 sec. Processed 59.22 million rows, 1.22 GB (52.22 million rows/s., 1.08 GB/s.)

10 rows in set. Elapsed: 1.295 sec. Processed 57.69 million rows, 1.18 GB (44.56 million rows/s., 913.69 MB/s.)

10 rows in set. Elapsed: 1.320 sec. Processed 60.90 million rows, 1.26 GB (46.13 million rows/s., 952.93 MB/s.)

```

And against 25\.12:



```
10 rows in set. Elapsed: 0.818 sec. Processed 60.18 million rows, 940.56 MB (73.55 million rows/s., 1.15 GB/s.)

10 rows in set. Elapsed: 0.800 sec. Processed 60.90 million rows, 953.67 MB (76.12 million rows/s., 1.19 GB/s.)

10 rows in set. Elapsed: 0.741 sec. Processed 55.61 million rows, 856.55 MB (75.02 million rows/s., 1.16 GB/s.)

```

If we take the quickest runs for each, the query runs about 30% faster in ClickHouse 25\.12\. We can also see that about 30% less data is read from disk.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

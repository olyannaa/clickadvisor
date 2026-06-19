# An introduction to Ibis


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# An introduction to Ibis

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Aug 5, 2024 · 9 minutes readIbis is an open\-source data frame library designed to work with any data system. It supports 20\+ backends, including Polars, DataFusion, and ClickHouse. It provides a Pythonic interface that supports relational operations translated to SQL and executed on the underlying database.


In this blog post, we will learn how to use [Ibis](https://ibis-project.org/) with ClickHouse.



## The Composable Data ecosystem [\#](/blog/introduction-to-ibis#the-composable-data-ecosystem)


Ibis is part of what’s known as [the composable data ecosystem](https://ibis-project.org/concepts/composable-ecosystem). A diagram is shown below:


![Intro to Ibis.png](/uploads/Intro_to_Ibis_996e3e461f.png)
In the diagram, Ibis is the user interface. Unlike most other DataFrame libraries, Ibis uses SQL as its intermediate representation language, making it easier to communicate with different backends.


## Installing Ibis and ClickHouse [\#](/blog/introduction-to-ibis#installing-ibis-and-clickhouse)


Let’s start by installing Ibis, its examples, and ClickHouse.



```
pip install 'ibis-framework[clickhouse,examples]'

```

We’ll start a ClickHouse Server if we don’t already have one running:



```
curl https://clickhouse.com/ | sh
./clickhouse server

```

Once ClickHouse is running, we’re ready to begin!


## Importing an Ibis example dataset into ClickHouse [\#](/blog/introduction-to-ibis#importing-an-ibis-example-dataset-into-clickhouse)


Ibis comes with various example datasets. We’re going to import the `nycflights13_flights` dataset into ClickHouse.


We’ll first import Ibis and create a connection to ClickHouse:



```
import ibis
from ibis import _

con = ibis.connect("clickhouse://")

```

If we wanted to use a ClickHouse server running elsewhere, we could provide the URL and any credentials as part of the connection string. The next step is to create the table:



```
con.create_table(
    "flights",
    ibis.examples.nycflights13_flights.fetch().to_pyarrow(), 
    overwrite=True
)

```

This command imports the dataset into a table called `flights` and replaces the table if it already exists.


In another tab, let’s connect to ClickHouse to see what this command has done:



```
./clickhouse client -m

ClickHouse client version 24.7.1.2215 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 24.7.1.

```

Once it’s connected, we can get a list of the tables:



```
SHOW TABLES

   ┌─name────┐
1. │ flights │
   └─────────┘

1 row in set. Elapsed: 0.002 sec.

```

## Exploring the Ibis flights dataset [\#](/blog/introduction-to-ibis#exploring-the-ibis-flights-dataset)


Let’s have a look at what fields we’ve got in that `flights` table:



```
DESCRIBE TABLE flights
SETTINGS describe_compact_output = 1

Query id: 7d497dee-ea8d-4b07-8b32-3f32f775ca32

    ┌─name───────────┬─type────────────────────┐
 1. │ year           │ Nullable(Int64)         │
 2. │ month          │ Nullable(Int64)         │
 3. │ day            │ Nullable(Int64)         │
 4. │ dep_time       │ Nullable(String)        │
 5. │ sched_dep_time │ Nullable(Int64)         │
 6. │ dep_delay      │ Nullable(String)        │
 7. │ arr_time       │ Nullable(String)        │
 8. │ sched_arr_time │ Nullable(Int64)         │
 9. │ arr_delay      │ Nullable(String)        │
10. │ carrier        │ Nullable(String)        │
11. │ flight         │ Nullable(Int64)         │
12. │ tailnum        │ Nullable(String)        │
13. │ origin         │ Nullable(String)        │
14. │ dest           │ Nullable(String)        │
15. │ air_time       │ Nullable(String)        │
16. │ distance       │ Nullable(Int64)         │
17. │ hour           │ Nullable(Int64)         │
18. │ minute         │ Nullable(Int64)         │
19. │ time_hour      │ Nullable(DateTime64(6)) │
    └────────────────┴─────────────────────────┘

```

So far, so good. Let’s return to our Python REPL and explore the `flight` data more thoroughly. First, we’ll create a reference to the table:



```
flights = con.table("flights")
flights.schema()

```


```
ibis.Schema {
  year            int64
  month           int64
  day             int64
  dep_time        string
  sched_dep_time  int64
  dep_delay       int64
  arr_time        string
  sched_arr_time  int64
  arr_delay       int64
  carrier         string
  flight          int64
  tailnum         string
  origin          string
  dest            string
  air_time        string
  distance        int64
  hour            int64
  minute          int64
  time_hour       timestamp(6)
}

```

And now, let’s have a look at one row of the table:



```
flights.head(n=1).to_pandas().T

```


```

                                  0
year                           2013
month                             1
day                               1
dep_time                        517
sched_dep_time                  515
dep_delay                         2
arr_time                        830
sched_arr_time                  819
arr_delay                        11
carrier                          UA
flight                         1545
tailnum                      N14228
origin                          EWR
dest                            IAH
air_time                        227
distance                       1400
hour                              5
minute                           15
time_hour       2013-01-01 10:00:00

```

The `dep_delay` and `arr_delay` have numeric data despite having the `string` data type. We can fix that in Ibis by casting those fields to the `int` type.



> Keep in mind that this won’t change the underlying type in the database.



```
flights = (flights.mutate(
  dep_delay = _.dep_delay.cast(int).coalesce(0), 
  arr_delay = _.arr_delay.cast(int).coalesce(0)
))

```

Next, let’s try to write some queries against the `flights` table. We’re going to put Ibis in interactive mode before we do this by setting the following parameter:



```
ibis.options.interactive = True

```

[This parameter](https://ibis-project.org/reference/options) does the following:



> Show the first few rows of computing an expression when in a REPL.


Let’s start by working out which airport has the most incoming flights:



```
(flights
  .group_by(flights.dest)
  .count()
  .order_by(ibis.desc("CountStar()"))
.limit(5)
)

```


```
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ dest   ┃ CountStar(flights) ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ string │ int64              │
├────────┼────────────────────┤
│ ORD    │              17283 │
│ ATL    │              17215 │
│ LAX    │              16174 │
│ BOS    │              15508 │
│ MCO    │              14082 │
└────────┴────────────────────┘

```

Chicago O’Hare wins on this metric. We could rewrite this query using the `agg` function to read like this:



```
(flights.group_by(flights.dest)
  .agg(flightCount = _.count())
  .order_by(ibis.desc(_.flightCount))
  .limit(5)
)

```

Or we can simplify it by using the `topk` function:



```
flights.dest.topk(k=5)

```

The `topk` function only works if we want to group by a single column. If we're going to group by multiple columns, we still need to use the `agg` function.


If we want to see the underlying SQL executed when we run this code, we can use the `ibis.to_sql` function:



```
print(ibis.to_sql(flights.dest.topk(k=5)))

```


```
SELECT
  *
FROM (
  SELECT
    "t1"."dest",
    COUNT(*) AS "CountStar()"
  FROM (
    SELECT
      "t0"."year",
      "t0"."month",
      "t0"."day",
      "t0"."dep_time",
      "t0"."sched_dep_time",
      COALESCE(CAST("t0"."dep_delay" AS Nullable(Int64)), 0) AS "dep_delay",
      "t0"."arr_time",
      "t0"."sched_arr_time",
      COALESCE(CAST("t0"."arr_delay" AS Nullable(Int64)), 0) AS "arr_delay",
      "t0"."carrier",
      "t0"."flight",
      "t0"."tailnum",
      "t0"."origin",
      "t0"."dest",
      "t0"."air_time",
      "t0"."distance",
      "t0"."hour",
      "t0"."minute",
      "t0"."time_hour"
    FROM "flights" AS "t0"
  ) AS "t1"
  GROUP BY
    "t1"."dest"
) AS "t2"
ORDER BY
  "t2"."CountStar()" DESC
LIMIT 5

```

This is more complicated than we’d write by hand and has too many sub\-queries for my liking, but I guess it does the job!


## Composing Ibis expressions [\#](/blog/introduction-to-ibis#composing-ibis-expressions)


Ibis expressions are evaluated lazily, meaning we can store an expression in a variable and then apply other operations later in our program.


For example, let’s say we create a variable called `routes_by_carrier` that groups flights by `dest`, `origin`, and `carrier` and counts the number of rows for each grouping key:



```
routes_by_carrier = (flights
  .group_by([flights.dest,flights.origin, flights.carrier])
  .agg(flightCount = _.count())
)
routes_by_carrier

```


```
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ dest   ┃ origin ┃ carrier ┃ flightCount ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
│ string │ string │ string  │ int64       │
├────────┼────────┼─────────┼─────────────┤
│ BNA    │ JFK    │ MQ      │         365 │
│ MKE    │ LGA    │ 9E      │         132 │
│ SBN    │ LGA    │ EV      │           6 │
│ CLE    │ LGA    │ EV      │         419 │
│ AVL    │ EWR    │ EV      │         265 │
│ FLL    │ EWR    │ B6      │        1386 │
│ IAH    │ JFK    │ AA      │         274 │
│ SAV    │ EWR    │ EV      │         736 │
│ DFW    │ EWR    │ UA      │        1094 │
│ BZN    │ EWR    │ UA      │          36 │
│ …      │ …      │ …       │           … │
└────────┴────────┴─────────┴─────────────┘

```

We might decide later that we’d like to find flights with American Airlines or Delta Airlines as the `carrier`. We could do that with the following code:



```
(routes_by_carrier
  .filter(_.carrier.isin(["AA", "DL"]))
  .group_by([_.origin, _.dest])
  .agg(flightCount = _.flightCount.sum())
  .order_by(ibis.desc(_.flightCount))
  .limit(5)
)

```


```
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
┃ origin ┃ dest   ┃ flightCount ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━┩
│ string │ string │ int64       │
├────────┼────────┼─────────────┤
│ LGA    │ MIA    │        5781 │
│ JFK    │ LAX    │        5718 │
│ LGA    │ ORD    │        5694 │
│ LGA    │ ATL    │        5544 │
│ LGA    │ DFW    │        4836 │
└────────┴────────┴─────────────┘

```

We can also combine Ibis tables. For example, let’s say we’ve created separate variables for outgoing flights from each of the airports in New York:



```
jfk_flights = flights.filter(_.origin == "JFK")
lga_flights = flights.filter(_.origin == "LGA")
ewr_flights = flights.filter(_.origin == "EWR")

```

We can build further expressions on each of those tables, but we could also combine them using the `union` function and then apply some other operations. If we wanted to compute the average departure delay across the three airports, we could do this:



```
(jfk_flights
  .union(lga_flights, ewr_flights)
  .agg(avgDepDelay = _.dep_delay.mean())
)

```


```
┏━━━━━━━━━━━━━┓
┃ avgDepDelay ┃
┡━━━━━━━━━━━━━┩
│ float64     │
├─────────────┤
│   12.329263 │
└─────────────┘

```

We can also find the average delay by airport:



```
(jfk_flights
  .union(lga_flights, ewr_flights)
  .group_by(_.origin)
  .agg(avgDepDelay = _.dep_delay.mean())
)

```


```
┏━━━━━━━━┳━━━━━━━━━━━━━┓
┃ origin ┃ avgDepDelay ┃
┡━━━━━━━━╇━━━━━━━━━━━━━┩
│ string │ float64     │
├────────┼─────────────┤
│ EWR    │   14.702983 │
│ JFK    │   11.909381 │
│ LGA    │   10.035170 │
└────────┴─────────────┘

```

And then, if we want to return only the airports with the biggest average delay and the smallest average delay, we can write the following code:



```
(jfk_flights
  .union(lga_flights, ewr_flights)
  .group_by(_.origin)
  .agg(avgDepDelay = _.dep_delay.mean())
).agg(
  minDelayOrigin = _.origin.argmin(_.avgDepDelay),
  minDelay = _.avgDepDelay.min(),
  maxDelayOrigin = _.origin.argmax(_.avgDepDelay),
  maxDelay = _.avgDepDelay.max()
)

```


```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ minDelayOrigin ┃ minDelay ┃ maxDelayOrigin ┃ maxDelay  ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ string         │ float64  │ string         │ float64   │
├────────────────┼──────────┼────────────────┼───────────┤
│ LGA            │ 10.03517 │ EWR            │ 14.702983 │
└────────────────┴──────────┴────────────────┴───────────┘

```

## Connecting Ibis to an existing ClickHouse table [\#](/blog/introduction-to-ibis#connecting-ibis-to-an-existing-clickhouse-table)


We can also connect Ibis to existing ClickHouse tables. We have a hosted Playground of datasets at `play.clickhouse.com`, so let’s create a new connection:



```
remote_con = ibis.connect(
  "clickhouse://play:clickhouse@play.clickhouse.com:443?secure=True"
)

```

We can then list the tables on that server:



```
remote_con.tables

```


```
Tables
------
- actors
- all_replicas_metric_log
- benchmark_results
- benchmark_runs
- cell_towers
- checks
- cisco_umbrella
- covid
- dish
- dns
- dns2
- github_events
- hackernews
- hackernews_changes_items
- hackernews_changes_profiles
- hackernews_changes_to_history
- hackernews_history
- hackernews_top
- lineorder
- loc_stats
- menu
- menu_item
- menu_item_denorm
- menu_page
- minicrawl
- newswire
- ontime
- opensky
- pypi
- query_metrics_v2
- rdns
- recipes
- repos
- repos_history
- repos_raw
- run_attributes_v1
- stock
- tranco
- trips
- uk_price_paid
- uk_price_paid_updater
- wikistat
- workflow_jobs

```

Let’s look at the `uk_price_paid` table, which contains the prices of houses sold in the UK. We’ll create a reference to that table and then return the schema:



```
uk_price_paid = remote_con.table("uk_price_paid")
uk_price_paid.schema()

```


```
ibis.Schema {
  price      !uint32
  date       !date
  postcode1  !string
  postcode2  !string
  type       !string
  is_new     !uint8
  duration   !string
  addr1      !string
  addr2      !string
  street     !string
  locality   !string
  town       !string
  district   !string
  county     !string
}

```

We can write the following query to find the places in the UK with the highest house prices:



```
(uk_price_paid
  .group_by([_.postcode1, _.postcode2])
  .agg(
    maxPrice = _.price.max(),
    avgPrice = _.price.mean().cast(int)
  )
  .order_by(ibis.desc(_.maxPrice))
  .limit(5)
)

```


```
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ postcode1 ┃ postcode2 ┃ maxPrice  ┃ avgPrice  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ !string   │ !string   │ !uint32   │ int64     │
├───────────┼───────────┼───────────┼───────────┤
│ TN23      │ 7HE       │ 900000000 │ 100115111 │
│ CV33      │ 9FR       │ 620000000 │ 206978541 │
│ W1U       │ 8EW       │ 594300000 │ 297192000 │
│ W1J       │ 7BT       │ 569200000 │  82508532 │
│ NW5       │ 2HB       │ 542540820 │  22848445 │
└───────────┴───────────┴───────────┴───────────┘

```

## Summary [\#](/blog/introduction-to-ibis#summary)


Hopefully, this blog post gives a good overview of Ibis and how it works. Ibis recently introduced [Ibis ML](https://github.com/ibis-project/ibis-ml), and in a future post, we’ll learn how to use it with ClickHouse data.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

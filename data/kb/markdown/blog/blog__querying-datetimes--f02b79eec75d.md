# Querying DateTimes in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Querying DateTimes in ClickHouse

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Mar 20, 2026 · 10 minutes readIn this post we're going to look at some of the most useful ClickHouse functions for querying and filtering by dates and datetimes \- things like rounding to the nearest hour or 15\-minute window, filtering by time of day, and computing durations between two timestamps.


If you're working with raw date strings or timestamps that need converting first, check out another post that I wrote about [parsing dates and datetimes in ClickHouse](https://clickhouse.com/blog/parsing-dates-datetimes). This post picks up from there and focuses on what to do once your data is already in a `DateTime` column.



## Importing the New York City taxi dataset [\#](/blog/querying-datetimes#importing_the_new_york_city_taxi_dataset)


Our dataset of choice is the [New York City taxi dataset](https://clickhouse.com/docs/getting-started/example-datasets/nyc-taxi), so let's get that set up in ClickHouse. First we'll create a database:



```

```
1CREATE DATABASE nyc_taxi;
```

```

And a table:



```

```
1CREATE TABLE nyc_taxi.trips_small (
2    trip_id             UInt32,
3    pickup_datetime     DateTime,
4    dropoff_datetime    DateTime,
5    pickup_longitude    Nullable(Float64),
6    pickup_latitude     Nullable(Float64),
7    dropoff_longitude   Nullable(Float64),
8    dropoff_latitude    Nullable(Float64),
9    passenger_count     UInt8,
10    trip_distance       Float32,
11    fare_amount         Float32,
12    extra               Float32,
13    tip_amount          Float32,
14    tolls_amount        Float32,
15    total_amount        Float32,
16    payment_type        Enum('CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4, 'UNK' = 5),
17    pickup_ntaname      LowCardinality(String),
18    dropoff_ntaname     LowCardinality(String)
19)
20ENGINE = MergeTree
21PRIMARY KEY (pickup_datetime, dropoff_datetime);
```

```

We can then run the following command to import the data:



```

```
1INSERT INTO nyc_taxi.trips_small
2SELECT
3    trip_id,
4    pickup_datetime,
5    dropoff_datetime,
6    pickup_longitude,
7    pickup_latitude,
8    dropoff_longitude,
9    dropoff_latitude,
10    passenger_count,
11    trip_distance,
12    fare_amount,
13    extra,
14    tip_amount,
15    tolls_amount,
16    total_amount,
17    payment_type,
18    pickup_ntaname,
19    dropoff_ntaname
20FROM s3(
21    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{0..2}.gz',
22    'TabSeparatedWithNames'
23);
```

```

This query imports just over 3 million records, as we can see in the output below:



```
3000317 rows in set. Elapsed: 32.077 sec. Processed 3.00 million rows, 256.38 MB (93.53 thousand rows/s., 7.99 MB/s.)
Peak memory usage: 536.51 MiB.

```

We can adjust the `{0..2}` in the URI to include more files if we want to import more data.


Now that we're loaded the data, it's time to write some queries.
We'll be working with the `pickup_datetime` and `dropoff_datetime` columns:


## Trips by hour [\#](/blog/querying-datetimes#trips_by_hour)


Let's start by exploring taxi journeys taken on July 1st, 2015\. We'll use [`toStartOfHour`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#tostartofhour) to round datetimes down to the nearest hour, [`toDate`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#todate) to filter to a single day, and [`toHour`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#tohour) to restrict to morning hours:



```

```
1SELECT
2  toStartOfHour(pickup_datetime) as hour,
3  count() as trips,
4  round(avg(passenger_count), 1) as avg_passengers
5FROM nyc_taxi.trips_small
6WHERE toDate(pickup_datetime) = '2015-07-01'
7AND toHour(pickup_datetime) < 13
8GROUP BY hour
9ORDER BY hour;
```

```


```
┌────────────────hour─┬─trips─┬─avg_passengers─┐
│ 2015-07-01 00:00:00 │   663 │            1.7 │
│ 2015-07-01 01:00:00 │   381 │            1.6 │
│ 2015-07-01 02:00:00 │   249 │            1.8 │
│ 2015-07-01 03:00:00 │   155 │            1.6 │
│ 2015-07-01 04:00:00 │   159 │            1.5 │
│ 2015-07-01 05:00:00 │   197 │            1.5 │
│ 2015-07-01 06:00:00 │   530 │            1.6 │
│ 2015-07-01 07:00:00 │   849 │            1.6 │
│ 2015-07-01 08:00:00 │  1034 │            1.6 │
│ 2015-07-01 09:00:00 │  1033 │            1.7 │
│ 2015-07-01 10:00:00 │   898 │            1.7 │
│ 2015-07-01 11:00:00 │   900 │            1.6 │
│ 2015-07-01 12:00:00 │   961 │            1.7 │
└─────────────────────┴───────┴────────────────┘

```

It was quiet overnight, trips start to pick up around 6am, and peak around 8–9am. But was July 1st typical? Let's remove the date filter and look across all days. To do that we cast `toStartOfHour` down to a `Time` type using [`::Time`](https://clickhouse.com/docs/en/sql-reference/data-types/time) \- that strips out the date and leaves just the time, so all days are grouped together:



```

```
1SELECT
2  toStartOfHour(pickup_datetime)::Time as hour,
3  count() as trips,
4  round(avg(passenger_count), 1) as avg_passengers
5FROM nyc_taxi.trips_small
6WHERE toHour(pickup_datetime) < 13
7GROUP BY hour
8ORDER BY hour;
```

```


```
┌─────hour─┬──trips─┬─avg_passengers─┐
│ 00:00:00 │ 118268 │            1.7 │
│ 01:00:00 │  86495 │            1.7 │
│ 02:00:00 │  65246 │            1.7 │
│ 03:00:00 │  47377 │            1.7 │
│ 04:00:00 │  34840 │            1.7 │
│ 05:00:00 │  32328 │            1.6 │
│ 06:00:00 │  68644 │            1.6 │
│ 07:00:00 │ 107494 │            1.6 │
│ 08:00:00 │ 132596 │            1.6 │
│ 09:00:00 │ 136228 │            1.6 │
│ 10:00:00 │ 134286 │            1.7 │
│ 11:00:00 │ 137561 │            1.7 │
│ 12:00:00 │ 145282 │            1.7 │
└──────────┴────────┴────────────────┘

```

When we look across all days we still see a reduction in journeys over night, but the increase starts a couple of hours earlier, from 6am to 7am. The number of trips then stays reasonably stable for the next four hours.


## Rush hour in 15\-minute windows [\#](/blog/querying-datetimes#rush_hour)


When exactly does the morning rush start? Let's zoom in using [`toStartOfFifteenMinutes`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#tostartoffifteenminutes) to bucket by 15\-minute intervals, and [`formatDateTime`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#formatdatetime) to make the output readable. In the `WHERE` clause we cast `pickup_datetime` to `Time` to filter just by time of day \- no date needed:



```

```
1SELECT
2  formatDateTime(toStartOfFifteenMinutes(pickup_datetime), '%r') AS timeWindow,
3  count() as trips,
4  round(avg(trip_distance), 2) as avgDistance
5FROM nyc_taxi.trips_small
6WHERE pickup_datetime::Time BETWEEN '06:00:00'::Time AND '09:59:59'::Time
7AND trip_distance > 0
8GROUP BY timeWindow
9ORDER BY timeWindow;
```

```


```
┌─timeWindow─┬─trips─┬─avgDistance─┐
│ 06:00 AM   │ 11601 │        4.47 │
│ 06:15 AM   │ 14645 │        3.97 │
│ 06:30 AM   │ 19033 │        3.67 │
│ 06:45 AM   │ 22795 │         3.2 │
│ 07:00 AM   │ 23179 │        3.27 │
│ 07:15 AM   │ 25465 │        3.12 │
│ 07:30 AM   │ 28350 │        3.04 │
│ 07:45 AM   │ 29914 │        2.89 │
│ 08:00 AM   │ 30444 │           3 │
│ 08:15 AM   │ 32063 │        2.91 │
│ 08:30 AM   │ 34293 │         2.8 │
│ 08:45 AM   │ 35116 │        2.63 │
│ 09:00 AM   │ 33776 │        2.74 │
│ 09:15 AM   │ 33800 │        2.72 │
│ 09:30 AM   │ 33694 │        2.73 │
│ 09:45 AM   │ 34235 │        2.63 │
└────────────┴───────┴─────────────┘

```

The surge begins at 6:30, accelerates until 7:30, and peaks at 8:45\.


## What does rush hour feel like? [\#](/blog/querying-datetimes#rush_hour_speed)


We know when rush hour starts \- but what does it feel like if you're in a taxi? We can use [`dateDiff`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#datediff) to compute journey duration in minutes, which lets us calculate average speed. We also use `dateDiff` in the `WHERE` clause to filter out zero\-duration trips (bad data):



```

```
1WITH buckets AS (
2  SELECT
3    formatDateTime(toStartOfFifteenMinutes(pickup_datetime), '%r') AS timeWindow,
4    count() as trips,
5    round(avg(trip_distance), 2) as avgDist,
6    round(avg(dateDiff('minute', pickup_datetime, dropoff_datetime)), 1) AS avgDuration,
7    round(avg(
8      trip_distance /
9      (dateDiff('minute', pickup_datetime, dropoff_datetime) / 60)
10    ), 1) AS avgSpeed
11  FROM nyc_taxi.trips_small
12  WHERE pickup_datetime::Time BETWEEN '06:00:00'::Time AND '09:59:59'::Time
13  AND trip_distance > 0
14  AND dateDiff('minute', pickup_datetime, dropoff_datetime) > 0
15  GROUP BY timeWindow
16  ORDER BY timeWindow
17)
18SELECT timeWindow, trips, avgDuration, avgDist, avgSpeed,
19       bar(avgSpeed, 0, (SELECT max(avgSpeed) FROM buckets), 20) AS speedBar
20FROM buckets
21ORDER BY timeWindow ASC;
```

```


```
┌─timeWindow─┬─trips─┬─avgDuration─┬─avgDist─┬─avgSpeed─┬─speedBar─────────────┐
│ 06:00 AM   │ 11562 │        13.2 │    4.48 │     19.3 │ ████████████████████ │
│ 06:15 AM   │ 14609 │        13.1 │    3.98 │     18.2 │ ██████████████████▊  │
│ 06:30 AM   │ 18993 │        12.5 │    3.67 │     17.3 │ █████████████████▉   │
│ 06:45 AM   │ 22754 │        11.5 │    3.21 │     16.1 │ ████████████████▋    │
│ 07:00 AM   │ 23139 │        12.3 │    3.27 │     15.4 │ ███████████████▉     │
│ 07:15 AM   │ 25428 │        12.7 │    3.12 │     14.3 │ ██████████████▊      │
│ 07:30 AM   │ 28313 │        13.9 │    3.04 │     13.5 │ █████████████▉       │
│ 07:45 AM   │ 29873 │        13.8 │    2.89 │     12.7 │ █████████████▏       │
│ 08:00 AM   │ 30411 │        14.2 │       3 │       12 │ ████████████▍        │
│ 08:15 AM   │ 32017 │        15.2 │    2.91 │     11.5 │ ███████████▉         │
│ 08:30 AM   │ 34258 │        15.4 │     2.8 │       11 │ ███████████▍         │
│ 08:45 AM   │ 35071 │        14.9 │    2.64 │     10.8 │ ███████████▏         │
│ 09:00 AM   │ 33718 │        15.3 │    2.74 │     10.9 │ ███████████▎         │
│ 09:15 AM   │ 33754 │        15.3 │    2.72 │     10.8 │ ███████████▏         │
│ 09:30 AM   │ 33657 │        15.4 │    2.73 │     10.8 │ ███████████▏         │
│ 09:45 AM   │ 34188 │        14.8 │    2.63 │     10.9 │ ███████████▎         │
└────────────┴───────┴─────────────┴─────────┴──────────┴──────────────────────┘

```

The [`bar`](https://clickhouse.com/docs/en/sql-reference/functions/other-functions#bar) function draws an ASCII bar chart scaled to the max value \- a handy way to visualize relative values inline.


At 6am taxis are moving at just over 19 mph. By 8am that's down to around 12 mph \- slow, but pretty standard for a big city during rush hour. It keeps getting slower as the morning wears on.


## Weekdays vs weekends [\#](/blog/querying-datetimes#weekdays_vs_weekends)


We've confirmed rush hour exists \- but does it happen on weekends too? We can split weekday and weekend trips using [`countIf`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-if) with [`toDayOfWeek`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#todayofweek): values 1–5 are weekdays, 6–7 are weekends. We then use the [`lag`](https://clickhouse.com/docs/en/sql-reference/window-functions) window function to compute the percentage change in trips between each 15\-minute window:



```

```
1WITH trips AS (
2  SELECT
3    formatDateTime(toStartOfFifteenMinutes(pickup_datetime), '%r') AS timeWindow,
4    countIf(toDayOfWeek(pickup_datetime) <= 5) as wdTrips,
5    countIf(toDayOfWeek(pickup_datetime) > 5) as weTrips
6  FROM nyc_taxi.trips_small
7  WHERE trip_distance > 0
8  AND pickup_datetime::Time BETWEEN '06:00:00'::Time AND '09:59:59'::Time
9  GROUP BY timeWindow
10  ORDER BY timeWindow
11)
12SELECT timeWindow, wdTrips,
13  round((
14    (wdTrips - lag(wdTrips) OVER (ORDER BY timeWindow)) /
15    lag(wdTrips) OVER (ORDER BY timeWindow)) * 100,
16  1) as wdPctChange,
17  weTrips,
18  round(
19    ((weTrips - lag(weTrips) OVER (ORDER BY timeWindow)) /
20    lag(weTrips) OVER (ORDER BY timeWindow)) * 100,
21  1) as wePctChange
22FROM trips
23ORDER BY timeWindow;
```

```


```
┌─timeWindow─┬─wdTrips─┬─wdPctChange─┬─weTrips─┬─wePctChange─┐
│ 06:00 AM   │    9398 │         inf │    2203 │         inf │
│ 06:15 AM   │   12254 │        30.4 │    2391 │         8.5 │
│ 06:30 AM   │   16106 │        31.4 │    2927 │        22.4 │
│ 06:45 AM   │   19727 │        22.5 │    3068 │         4.8 │
│ 07:00 AM   │   20285 │         2.8 │    2894 │        -5.7 │
│ 07:15 AM   │   22129 │         9.1 │    3336 │        15.3 │
│ 07:30 AM   │   24494 │        10.7 │    3856 │        15.6 │
│ 07:45 AM   │   25681 │         4.8 │    4233 │         9.8 │
│ 08:00 AM   │   26259 │         2.3 │    4185 │        -1.1 │
│ 08:15 AM   │   27509 │         4.8 │    4554 │         8.8 │
│ 08:30 AM   │   28891 │           5 │    5402 │        18.6 │
│ 08:45 AM   │   29154 │         0.9 │    5962 │        10.4 │
│ 09:00 AM   │   27872 │        -4.4 │    5904 │          -1 │
│ 09:15 AM   │   27268 │        -2.2 │    6532 │        10.6 │
│ 09:30 AM   │   26426 │        -3.1 │    7268 │        11.3 │
│ 09:45 AM   │   26070 │        -1.3 │    8165 │        12.3 │
└────────────┴─────────┴─────────────┴─────────┴─────────────┘

```

Weekdays show a sharp spike at 6:15–6:30, a second (smaller) increase around 7:15–7:30, and peak at 8:45 before leveling off. Weekends are different: the increase at 6:30 is gentler, and trips keep growing steadily well into the morning.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-255-get-started-today-sign-up&utm_blogctaid=255)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

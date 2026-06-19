# New functions you might have missed in 2025


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# New functions you might have missed in 2025

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Dec 23, 2025 · 12 minutes readMy colleague, Tom Schreiber, and I write a blog post after each ClickHouse release, focusing on the significant changes in each release, such as new data lake catalogs or improvements in join performance.


But in each release, there are often new functions that we don’t get around to covering. In this blog post, I will highlight some of the new functions introduced in 2025 that you may have overlooked.


## How many functions were introduced in 2025? [\#](/blog/new-functions-2025#how-many-functions-were-introduced-in-2025)


First up, did you know that you can find out how many functions were introduced in 2025 by running the following query:



```

```
1select count() 
2FROM system.functions 
3WHERE introduced_in LIKE '25%';
```

```


```
┌─count()─┐
│     119 │
└─────────┘

```

We can also count how many were introduced in each version. To do that, we’re going to borrow [a user\-defined function that sorts semantic versions](https://clickhouse.com/blog/semantic-versioning-udf):



```

```
1CREATE FUNCTION sortableSemVer AS version -> 
2  arrayMap(
3    x -> toUInt32OrZero(x), 
4    splitByChar('.', extract(version, '(d+(.d+)+)'))
5  );
```

```

And then, we can write the following query:



```

```
1SELECT introduced_in, count()
2FROM system.functions
3WHERE introduced_in LIKE '25%'
4GROUP BY ALL
5ORDER BY sortableSemVer(introduced_in);
```

```


```
┌─introduced_in─┬─count()─┐
│ 25.1          │       2 │
│ 25.2          │       2 │
│ 25.3          │       3 │
│ 25.4          │       7 │
│ 25.5          │      18 │
│ 25.6          │      17 │
│ 25.7          │      25 │
│ 25.8          │      18 │
│ 25.9          │       8 │
│ 25.10         │      10 │
│ 25.11         │       7 │
│ 25.12         │       2 │
└───────────────┴─────────┘

```

We can get a list of the functions by running the following query:



```

```
1SELECT
2    name,
3    introduced_in AS version,
4    if(length(description) > 80,
5       substring(description, 1, 80) || '...',
6       description) AS description
7FROM system.functions
8WHERE introduced_in LIKE '25%'
9ORDER BY sortableSemVer(introduced_in);
```

```

The results are limited to ten rows for brevity:



```
Row 1:
──────
name:        variantElement
version:     25.2
description:
Extracts a column with specified type from a `Variant` column.


Row 2:
──────
name:        numericIndexedVectorPointwiseMultiply
version:     25.7
description:
Performs pointwise multiplication between a numericIndexedVector and either ano...

Row 3:
──────
name:        __patchPartitionID
version:     25.5
description:
Internal function. Receives the name of a part and a hash of patch part's colum...

Row 4:
──────
name:        readWKBPolygon
version:     25.5
description:
                Parses a Well-Known Binary (WKB) representation of a Polygon ge...

Row 5:
──────
name:        initialQueryStartTime
version:     25.4
description:
Returns the start time of the initial current query.
`initialQueryStartTime` re...

```

Let’s take a look at some of the new functions!


## mapContainsValueLike [\#](/blog/new-functions-2025#mapcontainsvaluelike)


[mapContainsValueLike](https://clickhouse.com/docs/sql-reference/functions/tuple-map-functions#mapcontainsvaluelike) was added in ClickHouse 25\.5 and checks whether a map contains a value that matches the specified pattern using the `LIKE` operator.


So, imagine we have the following query, which returns company names and use case details:



```

```
1SELECT
2        'Netflix' AS company,
3        map('use_case', 'streaming analytics', 'scale', '5 petabytes daily') AS details
4    UNION ALL
5    SELECT
6        'Tesla',
7        map('use_case', 'observability platform', 'scale', 'quadrillion rows', 'feature', 'vector search')
8    UNION ALL
9    SELECT
10        'Anthropic',
11        map('use_case', 'AI observability', 'scale', 'billions of events')
12    UNION ALL
13    SELECT
14        'Uber',
15        map('use_case', 'ride analytics', 'scale', 'petabyte scale')
16FORMAT Vertical;
```

```


```
Row 1:
──────
company: Netflix
details: {'use_case':'streaming analytics','scale':'5 petabytes daily'}

Row 2:
──────
company: Tesla
details: {'use_case':'observability platform','scale':'quadrillion rows','feature':'vector search'}

Row 3:
──────
company: Anthropic
details: {'use_case':'AI observability','scale':'billions of events'}

Row 4:
──────
company: Uber
details: {'use_case':'ride analytics','scale':'petabyte scale'}

```

We could then write the following query to check whether any of the values in the maps contain the terms `obser`, `petabyte`, or `vector`:



```

```
1WITH useCases AS (
2    SELECT
3        'Netflix' AS company,
4        map('use_case', 'streaming analytics', 'scale', '5 petabytes daily') AS details
5    UNION ALL
6    SELECT
7        'Tesla',
8        map('use_case', 'observability platform', 'scale', 'quadrillion rows', 'feature', 'vector search')
9    UNION ALL
10    SELECT
11        'Anthropic',
12        map('use_case', 'AI observability', 'scale', 'billions of events')
13    UNION ALL
14    SELECT
15        'Uber',
16        map('use_case', 'ride analytics', 'scale', 'petabyte scale')
17)
18SELECT
19    company,
20    details,
21    mapContainsValueLike(details, '%observ%') AS is_observability,
22    mapContainsValueLike(details, '%petabyte%') AS petabyte_scale,
23    mapContainsValueLike(details, '%vector%') AS has_vector_search
24FROM useCases
25FORMAT Vertical;
```

```

And we’ll get back the following:



```
Row 1:
──────
company:           Netflix
details:           {'use_case':'streaming analytics','scale':'5 petabytes daily'}
is_observability:  0
petabyte_scale:    1
has_vector_search: 0

Row 2:
──────
company:           Tesla
details:           {'use_case':'observability platform','scale':'quadrillion rows','feature':'vector search'}
is_observability:  1
petabyte_scale:    0
has_vector_search: 1

Row 3:
──────
company:           Anthropic
details:           {'use_case':'AI observability','scale':'billions of events'}
is_observability:  1
petabyte_scale:    0
has_vector_search: 0

Row 4:
──────
company:           Uber
details:           {'use_case':'ride analytics','scale':'petabyte scale'}
is_observability:  0
petabyte_scale:    1
has_vector_search: 0

```

## perimeterCartesian [\#](/blog/new-functions-2025#perimetercartesian)


[`perimeterCartesian`](https://clickhouse.com/docs/sql-reference/functions/geo/geometry#perimetercartesian) was added in ClickHouse 25\.10 and calculates the perimeter of the given Geometry object in the Cartesian (flat) coordinate system.


Let’s have a look at how it works when computing the perimeter of a square:



```

```
1SELECT perimeterCartesian(readWKT('POLYGON((0 0,1 0,1 1,0 1,0 0))'));
```

```


```
┌─perimeterCar⋯ 1,0 0))'))─┐
│                        4 │
└──────────────────────────┘

```

We also have [`perimeterSpherical`](https://clickhouse.com/docs/sql-reference/functions/geo/geometry#perimeterspherical), which calculates the perimeter of a Geometry object on the surface of a sphere. So, if we want to compute the perimeter of the M25 motorway that goes around London, we can use `perimeterSpherical` instead:



```

```
1WITH
2    readWKT('POLYGON((0.13870239257812503 51.2968127854147, 0.16342163085937503 51.37403072457134, 0.212860107421875 51.41516045575089, 0.27053833007812506 51.483627853536014, 0.27328491210937506 51.54686881000932, 0.25405883789062506 51.633894901713354, 0.13870239257812503 51.67308742846449, 0.08102416992187501 51.695224736990404, -0.023345947265625003 51.68500886266592, -0.12222290039062501 51.69352225137908, -0.29525756835937506 51.71224607096211, -0.37490844726562506 51.71905281158759, -0.44631958007812506 51.68330599278565, -0.49850463867187506 51.64412230646439, -0.5259704589843751 51.55028473901506, -0.5039978027343751 51.51440469156115, -0.5369567871093751 51.44255973575031, -0.5177307128906251 51.37403072457134, -0.41061401367187506 51.30883300776494, -0.29525756835937506 51.30539897974217, -0.15243530273437503 51.272762896039936, 0.04531860351562501 51.272762896039936, 0.13870239257812503 51.2968127854147))') AS m25,
3    perimeterSpherical(m25) AS per_rad
4SELECT
5    per_rad,
6    per_rad * 6371000 AS per_meters,
7    per_rad * 6371 AS per_km;
```

```

This function returns the length in radians on a unit sphere, so we need to multiply by the Earth’s radius to get a result in meters or kilometers:



```
┌──────────────per_rad─┬─────────per_meters─┬─────────────per_km─┐
│ 0.027954722202348813 │ 178099.53515116428 │ 178.09953515116428 │
└──────────────────────┴────────────────────┴────────────────────┘

```

This motorway is actually 188 km in diameter, so we’re not too far off \- we’ll put the difference down to my poor polygon drawing.


## HMAC [\#](/blog/new-functions-2025#hmac)


[HMAC](https://clickhouse.com/docs/sql-reference/functions/encryption-functions) (Hash\-based Message Authentication Code) is a cryptographic construction used to verify the integrity and authenticity of a message simultaneously. ClickHouse 25\.12 adds this function.


Let’s have a look at how to use it by generating a signature for the word ‘ClickHouse’. The result is returned in hexadecimal format, so we’ll use the [`hex`](https://clickhouse.com/docs/sql-reference/functions/encoding-functions#hex) function to return it as a string:



```

```
1SELECT hex(HMAC('sha256', 'ClickHouse', 'mySecretKey'))
```

```


```
┌─hex(HMAC('sha256', 'ClickHouse', 'mySecretKey'))─────────────────┐
│ 5A79F3AA2874164CFD9811F9D1DBCEBE428C9BC52A7F57303EC6BAFCD6C9377B │
└──────────────────────────────────────────────────────────────────┘

```

The message 'ClickHouse' and its signature can then be sent to another party. The recipient can verify the message's authenticity by computing the HMAC with their copy of the secret key and comparing it to the provided signature.


## argAndMin and argAndMax [\#](/blog/new-functions-2025#argandmin-and-argandmax)


ClickHouse 25\.11 introduced the [argAndMax](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/argandmax) and [argandMin](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/argandmin) functions. Let’s explore these functions using the [UK property prices dataset](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid).


Let’s say we want to get the most expensive property sold in 2025\. We could write this query:



```

```
1SELECT max(price) 
2FROM uk_price_paid 
3WHERE toYear(date) = 2025;
```

```


```
┌─max(price)─┐
│  127700000 │ -- 127.70 million
└────────────┘

```

What about getting the town corresponding to the maximum price? We can use the `argMax` function to do this:



```

```
1SELECT argMax(town, price) 
2FROM uk_price_paid 
3WHERE toYear(date) = 2025;
```

```


```
┌─argMax(town, price)─┐
│ PURFLEET-ON-THAMES  │
└─────────────────────┘

```

The `argAndMax` function lets us get the town as well as the corresponding maximum price:



```

```
1SELECT argAndMax(town, price) 
2FROM uk_price_paid 
3WHERE toYear(date) = 2025;
```

```


```
┌─argAndMax(town, price)───────────┐
│ ('PURFLEET-ON-THAMES',127700000) │
└──────────────────────────────────┘

```

We can do the same with `argAndMin` to find the town and the corresponding minimum price:



```

```
1SELECT argAndMin(town, price) 
2FROM uk_price_paid 
3WHERE toYear(date) = 2025;
```

```


```
┌─argAndMin(town, price)─┐
│ ('CAMBRIDGE',100)      │
└────────────────────────┘

```

That looks like bad data, as it’s fairly unlikely that a property was sold for £100 in 2025!


## sparseGrams [\#](/blog/new-functions-2025#sparsegrams)


[`sparseGrams`](https://clickhouse.com/docs/sql-reference/functions/string-functions#sparseGrams) was added in ClickHouse 25\.5, and finds all substrings of a given string that have a length of at least `n`, where the hashes of the `(n-1)` \-grams at the borders of the substring are strictly greater than those of any `(n-1)`\-gram inside the substring. It uses CRC32 as a hash function.



Let’s see how it works:



```

```
1SELECT sparseGrams('ClickHouse') FORMAT Vertical;
```

```


```
Row 1:
──────
sparseGrams('ClickHouse'): ['Cli','lic','ick','lick','ckH','kHo','ckHo','lickHo','Hou','ous','Hous','use']

```

The GitHub team invented this function, which can serve as a suitable replacement for n\-grams when building search indexes.


## stringBytesUniq [\#](/blog/new-functions-2025#stringbytesuniq)


Introduced in ClickHouse 25\.6, [`stringBytesUniq`](https://clickhouse.com/docs/sql-reference/functions/string-functions#stringBytesUniq) counts the number of unique bytes in a string. Let’s have a look at some examples:



```

```
1SELECT
2    stringBytesUniq('ClickHouse') AS ch,
3    stringBytesUniq('Alexey Milovidov') AS alexey,
4    stringBytesUniq('AAAAA') AS a;
```

```


```
┌─ch─┬─alexey─┬─a─┐
│ 10 │     11 │ 1 │
└────┴────────┴───┘

```

## financialInternalRateOfReturn [\#](/blog/new-functions-2025#financialinternalrateofreturn)


Introduced in ClickHouse 25\.7, [`financialInternalRateOfReturn`](https://clickhouse.com/docs/sql-reference/functions/financial-functions) tells us the rate of return (on, for example, an investment) if it were computed annually.


So, imagine we buy Apple stock at $113 in 2020, do nothing in 2021, 2022, 2023, and 2024, and then sell at $231 in 2025\. We can work out the internal rate of return by running the following query:



```

```
1SELECT financialInternalRateOfReturn([-113, 0, 0, 0, 0, 231])
```

```


```
┌─financialInt⋯0, 0, 231])─┐
│      0.15373669910090634 │
└──────────────────────────┘

```

This is equivalent to making a 15% return for every year between 2020 and 2025\. We can check the logic by running the following query:



```

```
1SELECT 113 * power(1.15373669910090634, 5);
```

```


```
┌─multiply(113⋯009064, 5))─┐
│       230.99999999999997 │
└──────────────────────────┘

```

There’s also a sister function, [`financialInternalRateOfReturnExtended`](https://clickhouse.com/docs/sql-reference/functions/financial-functions#financialInternalRateOfReturnExtended), which we can use to compute our rate of return when the cash flows occur at irregular intervals, i.e., on specific dates.


So we can use our same example of Apple stocks, but this time using the exact dates that we bought and sold the stock:



```

```
1SELECT financialInternalRateOfReturnExtended(
2  [-113, 231],
3  [toDate('2020-09-11'), toDate('2025-03-05')]
4);
```

```


```
┌─financialInt⋯5-03-05')])─┐
│      0.17295574412431242 │
└──────────────────────────┘

```

This time our rate of return is just over 17%.


## toInterval [\#](/blog/new-functions-2025#tointerval)


Introduced in ClickHouse 25\.4, [`toInterval`](https://clickhouse.com/docs/sql-reference/functions/type-conversion-functions#toInterval) creates an interval value from a numeric value and a unit string.


We already have individual functions to perform this task (e.g., toIntervalSecond, toIntervalMinute, toIntervalDay, etc.), but this consolidates them under a single function.


Let’s see how to use it:



```

```
1SELECT
2    toInterval(5, 'second') AS seconds,
3    toTypeName(seconds) AS secType,
4    toInterval(3, 'day') AS days,
5    toTypeName(days) AS daysType,
6    toInterval(2, 'month') AS months,
7    toTypeName(months) AS monthsType;
```

```


```

┌─seconds─┬─secType────────┬─days─┬─daysType────┬─months─┬─monthsType────┐
│       5 │ IntervalSecond │    3 │ IntervalDay │      2 │ IntervalMonth │
└─────────┴────────────────┴──────┴─────────────┴────────┴───────────────┘

```

We can also use this function to add to an existing DateTime, as shown below:



```

```
1WITH toDateTime('2025-12-17 12:32:12') AS currentTime
2SELECT
3    currentTime,
4    currentTime + toInterval(7, 'day') + toInterval(23, 'hour') AS nextWeek;
```

```


```
┌─────────currentTime─┬────────────nextWeek─┐
│ 2025-12-17 12:32:12 │ 2025-12-25 11:32:12 │
└─────────────────────┴─────────────────────

```

## timeSeriesRange [\#](/blog/new-functions-2025#timeseriesrange)


Introduced in version 25\.8, [`timeSeriesRange`](https://clickhouse.com/docs/sql-reference/functions/time-series-functions#timeSeriesRange) allows us to generate a range of timestamps. It’s like the range function, but for DateTimes.


It returns an array of values, but we can use the `arrayJoin` function to explode the array into individual rows:



```

```
1SELECT arrayJoin(
2  timeSeriesRange(
3    '2025-06-01 00:00:00'::DateTime, 
4    '2025-06-01 00:01:00'::DateTime, 
5    10
6)) AS ts;
```

```


```
┌──────────────────ts─┐
│ 2025-06-01 00:00:00 │
│ 2025-06-01 00:00:10 │
│ 2025-06-01 00:00:20 │
│ 2025-06-01 00:00:30 │
│ 2025-06-01 00:00:40 │
│ 2025-06-01 00:00:50 │
│ 2025-06-01 00:01:00 │
└─────────────────────┘

```

We could then work out how long it’s been since each of those times



```

```
1WITH toDateTime('2025-12-17 12:32:12') AS currentTime
2SELECT arrayJoin(
3  timeSeriesRange(
4    '2025-06-01 00:00:00'::DateTime, 
5    '2025-06-01 00:01:00'::DateTime, 
6    10
7)) AS ts,
8  formatReadableTimeDelta(now() - ts) AS timeAgo;
```

```


```
┌──────────────────ts─┬─timeAgo────────────────────────────────────────────────┐
│ 2025-06-01 00:00:00 │ 6 months, 16 days, 14 hours, 10 minutes and 41 seconds │
│ 2025-06-01 00:00:10 │ 6 months, 16 days, 14 hours, 10 minutes and 31 seconds │
│ 2025-06-01 00:00:20 │ 6 months, 16 days, 14 hours, 10 minutes and 21 seconds │
│ 2025-06-01 00:00:30 │ 6 months, 16 days, 14 hours, 10 minutes and 11 seconds │
│ 2025-06-01 00:00:40 │ 6 months, 16 days, 14 hours, 10 minutes and 1 second   │
│ 2025-06-01 00:00:50 │ 6 months, 16 days, 14 hours, 9 minutes and 51 seconds  │
│ 2025-06-01 00:01:00 │ 6 months, 16 days, 14 hours, 9 minutes and 41 seconds  │
└─────────────────────┴────────────────────────────────────────────────────────┘

```
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

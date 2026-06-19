# Semantic Versioning UDF in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Semantic Versioning UDF in ClickHouse

![](/_next/image?url=%2Fuploads%2FJuan_Carrillo_profile_1f4aa99e38.jpeg&w=96&q=75)Juan S. CarrilloOct 9, 2024 · 7 minutes readI work at [Embrace](https://embrace.io/), where we build the only user\-focused mobile app observability solution based on OpenTelemetry (OTel). We use ClickHouse to power our time series analytics products.


One of the most important sorting categories for Embrace users is app version. App versions often use [semantic versioning](https://semver.org/), where the version will be described in the format `<MAJOR>.<MINOR>.<PATCH>`. You increment them according to the following rules:


1. MAJOR version when you make incompatible API changes
2. MINOR version when you add functionality in a backward compatible manner
3. PATCH version when you make backward compatible bug fixes


We want to be able to sort app versions such that 2\.1\.0, 2\.1\.2, and 2\.1\.10 would appear in that order, rather than 2\.1\.0, 2\.1\.10, and 2\.1\.2, which happens when you sort in lexicographic order.


ClickHouse doesn’t provide a way to sort for semantic versioning right out of the box. However, you can use User\-Defined Functions (UDFs), which were introduced in ClickHouse [v21\.10](https://clickhouse.com/blog/click-house-v2110-released), to solve this.


The final UDF we use can be found below. Please read on if you want to see how we built it, and the improvements we made in our querying and in our reasoning.



```
CREATE FUNCTION sortableSemVer AS version -> 
  arrayMap(
    x -> toUInt32OrZero(x), 
    splitByChar('.', extract(version, '(\\d+(\\.\\d+)+)'))
  )

```

## Versions as ints in strings [\#](/blog/semantic-versioning-udf#versions-as-ints-in-strings)


Versions are most commonly stored as strings in databases. As many of you may know, sorting version strings using lexicographical order will not work as expected.



```
SELECT *
FROM
(
    SELECT ['1.0', '2.0', '3.0.0', '10.0'] AS versions
)
ARRAY JOIN versions
ORDER BY versions DESC

┌─versions─┐
│ 3.0.0    │
│ 2.0      │
│ 10.0     │ << ???
│ 1.0      │
└──────────┘

```

The basic idea is that we will use int arrays and sort those instead. If we rewrite our semantic versions as arrays of ints, sorting works as expected. It even works for versions with different lengths!



```
SELECT *
FROM
(
    SELECT [[1, 0], [2, 0], [3, 0, 0], [10, 0]] AS versions
)
ARRAY JOIN versions
ORDER BY versions DESC

┌─versions─┐
│ [10,0]   │
│ [3,0,0]  │
│ [2,0]    │
│ [1,0]    │
└──────────┘

```

Let’s write a lambda function to transform a version string into an array of ints.



```
SELECT
    version,
    arrayMap(x -> toUInt32(x), splitByChar('.', version)) AS sem_ver_arr
FROM
(
    SELECT ['1.0', '2.0', '3.0.0', '10.0'] AS version
)
ARRAY JOIN version
ORDER BY sem_ver_arr DESC

┌─version─┬─sem_ver_arr─┐
│ 10.0    │ [10,0]      │
│ 3.0.0   │ [3,0,0]     │
│ 2.0     │ [2,0]       │
│ 1.0     │ [1,0]       │
└─────────┴─────────────┘

```

Let’s break that down:


1. `splitByChar('.', version)` splits the version string into an array of strings on the period `.`, transforming `10.0` into `['10', '0']`.
2. `arrayMap(x -> toUInt32(x), arr)` converts each number string into an int32


We can save some typing by defining a UDF:



```
CREATE FUNCTION sortableSemVer AS version -> 
  arrayMap(x -> toUInt32(x), splitByChar('.', version));

```

Let’s use it!



```
SELECT
    version,
    sortableSemVer(version) AS sem_ver_arr
FROM
(
    SELECT ['1.0', '2.0', '3.0.0', '10.0'] AS version
)
ARRAY JOIN version
ORDER BY sem_ver_arr DESC

┌─version─┬─sem_ver_arr─┐
│ 10.0    │ [10,0]      │
│ 3.0.0   │ [3,0,0]     │
│ 2.0     │ [2,0]       │
│ 1.0     │ [1,0]       │
└─────────┴─────────────┘

```

You can even exclude the sem\_ver\_arr column all together and only use the `sortableSemVer` in the `ORDER BY` clause.



```
SELECT version
FROM
(
    SELECT ['1.0', '2.0', '3.0.0', '10.0'] AS version
)
ARRAY JOIN version
ORDER BY sortableSemVer(version) DESC

┌─version─┐
│ 10.0    │
│ 3.0.0   │
│ 2.0     │
│ 1.0     │
└─────────┘

```

Assuming you have well formed semantic versions, you can use the function as is and call it a day. If your version strings look something like this `my-app-1.2.3(456)-alpha-45dbbdf9ab`, read on.


## Versions as complex strings [\#](/blog/semantic-versioning-udf#versions-as-complex-strings)


Let’s continue with a simpler example: `1.2.3.production`. Our previous function will fail because `production` is not a valid number.



```
select arrayMap(x -> toUInt32(x), splitByChar('.', '1.2.3.production'));

Received exception from server (version 23.8.15):
Code: 6. DB::Exception: Received from localhost:9000. DB::Exception: Cannot parse string 'production' as UInt32: syntax error at begin of string. Note: there are toUInt32OrZero and toUInt32OrNull functions, which returns zero/NULL instead of throwing exception.: while executing 'FUNCTION toUInt32(x :: 0) -> toUInt32(x) UInt32 : 1': while executing 'FUNCTION arrayMap(__lambda :: 1, splitByChar('.', '1.2.3.production') :: 0) -> arrayMap(lambda(tuple(x), toUInt32(x)), splitByChar('.', '1.2.3.production')) Array(UInt32) : 2'. (CANNOT_PARSE_TEXT)

```

We can replace `toUInt32` with `toUInt32OrZero` , which will default to 0 for non\-numerical strings. In fact, this also allows us to handle strings that don’t have anything that looks like a number.



```
SELECT
    version,
    arrayMap(x -> toUInt32OrZero(x), splitByChar('.', version)) AS sem_ver_arr
FROM
(
    SELECT [
        '1.0', '2.0', '3.0.0', 
        '10.0', 'production', '1.2.3.production'
        ] AS version
)
ARRAY JOIN version
ORDER BY sem_ver_arr DESC

┌─version──────────┬─sem_ver_arr─┐
│ 10.0             │ [10,0]      │
│ 3.0.0            │ [3,0,0]     │
│ 2.0              │ [2,0]       │
│ 1.2.3.production │ [1,2,3,0]   │
│ 1.0              │ [1,0]       │
│ production       │ [0]         │
└──────────────────┴─────────────┘

```

Of course, we will miss the patch version if the version was `1.2.3-production`, since we are splitting on periods. We can extract anything that looks like a semantic version using the `extract` function with a regex. This one will grab the semantic version at the start of a string.



```
SELECT extract('1.2.3-production', '^\\d+\\.\\d+\\.\\d+')

┌─extract('1.2.3-production', '^\\d+\\.\\d+\\.\\d+')─┐
│ 1.2.3                                              │
└────────────────────────────────────────────────────┘

```

We can tweak the regex further to allow semantic versions that appear in other places in the string.



```
SELECT extract('my-app1.2.3-production', '\\d+\\.\\d+\\.\\d+')

┌─extract('my-app1.2.3-production', '\\d+\\.\\d+\\.\\d+')─┐
│ 1.2.3                                                   │
└─────────────────────────────────────────────────────────┘

```

Let’s change it further to allow semantic versions containing 2 or more subsections.



```
SELECT extract('1.2.3.4.5.6.7-production', '(\\d+(\\.\\d+)+)')

┌─extract('1.2.3.4.5.6.7-production', '(\\d+(\\.\\d+)+)')─┐
│ 1.2.3.4.5.6.7                                           │
└─────────────────────────────────────────────────────────┘

```

Note that we wrap the entire regex in parentheses to capture the entire version instead of the repeating second group. Otherwise you only capture the last part of the regex.



```
SELECT extract('1.2.3.4.5.6.7-production', '\\d+(\\.\\d+)+')

┌─extract('1.2.3.4.5.6.7-production', '\\d+(\\.\\d+)+')─┐
│ .7                                                    │
└───────────────────────────────────────────────────────┘

^--- Where did the rest of it go?!?

```

Let’s modify our original UDF to include the new regex functionality!



```
--- Drop the previous definition
DROP FUNCTION IF EXISTS sortableSemVer;

--- Create the new definition
CREATE FUNCTION sortableSemVer AS version -> 
  arrayMap(
    x -> toUInt32OrZero(x), 
    splitByChar('.', extract(version, '(\\d+(\\.\\d+)+)'))
  );

```

Let’s add more version strings to see how it behaves.



```
SELECT
    version,
    sortableSemVer(version) AS sem_ver_arr
FROM
(
    SELECT [
        '1.0', '2.0', '3.0.0', '10.0', 'production', '1.2.3.production', 
        'my-app-1.2.3-prod', '3.5.0(ac22da)-test', '1456', '1.2.3.45', ''
        ] AS version
)
ARRAY JOIN version
ORDER BY sem_ver_arr DESC

```

![Screenshot 2024-09-30 at 11.27.13.png](/uploads/Screenshot_2024_09_30_at_11_27_13_84fd01a82e.png)
Of course, this won’t work for everything. Version strings like this aren’t parsed correctly:



```
SELECT sortableSemVer('100.731a9bd8-5edbc015-SNAPSHOT') AS sem_ver_arr

┌─sem_ver_arr─┐
│ [100,731]   │
└─────────────┘

```

There’s also no way to correctly sort by suffixes, since these are removed:



```
SELECT
    version,
    sortableSemVer(version) AS sem_ver_arr
FROM
(
    SELECT ['1.2.3-prod', '1.2.3', '1.2.3-stg'] AS version
)
ARRAY JOIN version
ORDER BY sem_ver_arr DESC

┌─version────┬─sem_ver_arr─┐
│ 1.2.3-prod │ [1,2,3]     │
│ 1.2.3      │ [1,2,3]     │
│ 1.2.3-stg  │ [1,2,3]     │
└────────────┴─────────────┘

```

Different versioning schemas will also tie:



```
SELECT
    version,
    sortableSemVer(version) AS sem_ver_arr
FROM
(
    SELECT [
        'my-app-1.2.3-prod', 
        '1.2.3', 
        '1.2.3(af012342)-ALPHA'
        ] AS version
)
ARRAY JOIN version
ORDER BY sem_ver_arr DESC

Query id: 5bce759d-8ddb-4327-8e84-6f682b71b022

┌─version───────────────┬─sem_ver_arr─┐
│ my-app-1.2.3-prod     │ [1,2,3]     │
│ 1.2.3                 │ [1,2,3]     │
│ 1.2.3(af012342)-ALPHA │ [1,2,3]     │
└───────────────────────┴─────────────┘

```

However, this is not typically an issue since customers tend to use the same versioning schema. ClickHouse’s UDFs are a powerful way to use lambdas to process your data. Play around with the ones in this guide to best suit your needs. For our purposes, we’ve found that this works well enough.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

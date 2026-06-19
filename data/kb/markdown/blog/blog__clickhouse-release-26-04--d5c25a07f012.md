# ClickHouse Release 26\.4


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 26\.4

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)ClickHouseMay 8, 2026 · 13 minutes readAnother month goes by, which means it’s time for another release!


The ClickHouse 26\.4 release contains 39 new features 🌷 45 performance optimizations 🐇 238 bug fixes 🐝


This release sees more features become SQL compatible, faster COUNT DISTINCT, even prettier EXPLAIN, and more!


## New contributors [\#](/blog/clickhouse-release-26-04#new-contributors)


A special welcome to all the new contributors in 26\.4! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.


Below are the names of the new contributors:


*Alexander Kuleshov, Alsu, Anton Frost, Aruj Bansal, Asya, ClickGap AI Bot, Denys Melnyk, Diego Gomes Tome, Dustin Healy, Evgeny Kuzin, Farid Adam, Francisco Garcia Florez, Gagan Dhakrey, Gleb Popov, Groene AI, Ivan Mantova, Jaap Elst, Jack Knudson, James Cunningham, JingYanchao, K, Kc Balusu, Matheus Nerone, Michael Russell, MukundaKatta, Nikita Semenov, Pavel Kravtsov, Peng, RenzoMXD, Sergey Veletskiy, Takumi Hara, Timothy Kurniawan, Wenyu Chen, XiaoBinMu, Yuri Fedoseev, ashrithb, asyablue22, dwagner\-decix, egor romanov, groeneai, liuguangliang, manerone, nerve\-bot, simonhammes, sourcelliu, xiaobin*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/2026-release-26.4/).


## SQL compatibility: VALUES as table expression, EXTRACT, SET TIME ZONE [\#](/blog/clickhouse-release-26-04#sql-compatibility-values-as-table-expression-extract-set-time-zone)


The 26\.4 release sees more features become [compatible with standard SQL syntax](https://presentations.clickhouse.com/2026-release-26.4/?full#16). We’ll look at just a few of them, but you can see the [presentation slide deck](https://presentations.clickhouse.com/2026-release-26.4/?full#16) for more.



### VALUES as a table expression [\#](/blog/clickhouse-release-26-04#values-as-a-table-expression)


#### Contributed by Desel72 [\#](/blog/clickhouse-release-26-04#contributed-by-desel72)


First up, `VALUES`. Before this release, you could call it like this:



```

```
1SELECT * 
2FROM VALUES((1, 'a'), (2, 'b'), (3, 'c'));
```

```


```
   ┌─c1─┬─c2─┐
1. │  1 │ a  │
2. │  2 │ b  │
3. │  3 │ c  │
   └────┴────┘

```

Whereas now, we can also call it as a table expression, as shown below:



```

```
1SELECT * 
2FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c'));
```

```


```
   ┌─c1─┬─c2─┐
1. │  1 │ a  │
2. │  2 │ b  │
3. │  3 │ c  │
   └────┴────┘

```

We can now also alias columns, which is useful when using `VALUES` in a join query. For example, instead of the following:



```

```
1SELECT
2    c.c2,
3    o.c2
4FROM VALUES((1, 'Alice'), (2, 'Bob')) AS c
5INNER JOIN VALUES((1, 250), (2, 100), (1, 75)) AS o 
6ON c.c1 = o.c1;
```

```


```
   ┌─c2────┬─o.c2─┐
1. │ Alice │  250 │
2. │ Alice │   75 │
3. │ Bob   │  100 │
   └───────┴──────┘

```

We can name the columns, which makes the query easier to understand:



```

```
1SELECT c.name, o.amount
2  FROM (VALUES (1, 'Alice'), (2, 'Bob')) AS c(id, name)
3  JOIN (VALUES (1, 250), (2, 100), (1, 75)) AS o(customer_id, amount)
4  ON c.id = o.customer_id;
```

```


```
   ┌─name──┬─amount─┐
1. │ Alice │    250 │
2. │ Alice │     75 │
3. │ Bob   │    100 │
   └───────┴────────┘

```

### EXTRACT [\#](/blog/clickhouse-release-26-04#extract)


#### Contributed by Alexey Milovidov [\#](/blog/clickhouse-release-26-04#contributed-by-alexey-milovidov)


The `EXTRACT` operator (used when working with dates) now supports PostgreSQL\-style units, as shown in the following query:



```

```
1SELECT
2  EXTRACT(EPOCH      FROM now())   AS epoch,
3  EXTRACT(DOW        FROM today()) AS dayOfWeek,
4  EXTRACT(DOY        FROM today()) AS dayOfYear,
5  EXTRACT(ISODOW     FROM today()) AS isoDOW,
6  EXTRACT(ISOYEAR    FROM today()) AS isoYear,
7  EXTRACT(WEEK       FROM today()) AS isoWeek,
8  EXTRACT(CENTURY    FROM today()) AS century,
9  EXTRACT(DECADE     FROM today()) AS decade,
10  EXTRACT(MILLENNIUM FROM today()) AS millennium;
```

```


```
Row 1:
──────
epoch:      1777992683
dayOfWeek:  2
dayOfYear:  125
isoDOW:     2
isoYear:    2026
isoWeek:    19
century:    21
decade:     202
millennium: 3

```

### SET TIME ZONE [\#](/blog/clickhouse-release-26-04#set-time-zone)


#### Contributed by phulv94 [\#](/blog/clickhouse-release-26-04#contributed-by-phulv94)


There is also a new SQL standard alias for setting the time zone. First, let’s check my current time zone:



```

```
1SELECT timezone(), formatDateTime(now(), '%Y-%m-%d %H:%M:%S %z');
```

```


```
   ┌─timezone()────┬─formatDateTim⋯H:%M:%S %z')─┐
1. │ Europe/London │ 2026-05-05 15:May:47 +0100 │
   └───────────────┴────────────────────────────┘

```

And now, we’ll set it to be Amsterdam instead:



```

```
1SET TIME ZONE 'Europe/Amsterdam';
```

```

And if we re\-run the above query:



```
   ┌─timezone()───────┬─formatDateTim⋯H:%M:%S %z')─┐
1. │ Europe/Amsterdam │ 2026-05-05 16:May:59 +0200 │
   └──────────────────┴────────────────────────────┘

```

### Other compatibility improvements [\#](/blog/clickhouse-release-26-04#other-compatibility-improvements)


And that’s not all \- there is also now support for [NATURAL JOIN](https://presentations.clickhouse.com/2026-release-26.4/?full#17), [OVERLAY](https://presentations.clickhouse.com/2026-release-26.4/?full#18) is drop\-in compatible, [compound INTERVAL literals](https://presentations.clickhouse.com/2026-release-26.4/?full#22) are supported, and more!


## LIKE uses text index [\#](/blog/clickhouse-release-26-04#like-uses-text-index)


### Contributed by Elmi Ahmadov [\#](/blog/clickhouse-release-26-04#contributed-by-elmi-ahmadov)


From ClickHouse 25\.4, when a `LIKE`/`ILIKE` query pattern is `%<alpha-numeric-characters-without-spaces>%` and the text index tokenizer is `splitByNonAlpha`, ClickHouse uses the [inverted index](https://clickhouse.com/blog/clickhouse-full-text-search-object-storage) to speed up those queries. It does this by scanning the inverted index dictionary rather than performing a full\-table scan to find the matching pattern.


Let’s have a look at how this works with our trusty HackerNews dataset, first using [clickhousectl](https://clickhouse.com/blog/getting-started-clickhousectl) to get ClickHouse 26\.4 running on my laptop:



```

```
1chctl local install 26.4
```

```

And then we’ll start it up:



```

```
1chctl local server start --version 26.4
```

```

And connect using the ClickHouse client:



```

```
1chctl local client --name default -mn
```

```

Next, we’ll create our HackerNews table:



```

```
1CREATE TABLE hackernews
2(
3    `id` Int64,
4    `deleted` Int64,
5    `type` String,
6    `by` String,
7    `time` DateTime64(9),
8    `text` String,
9    `dead` Int64,
10    `parent` Int64,
11    `poll` Int64,
12    `kids` Array(Int64),
13    `url` String,
14    `score` Int64,
15    `title` String,
16    `parts` Array(Int64),
17    `descendants` Int64
18    GRANULARITY 128
19)
20ORDER BY time;
```

```

We’ll then insert the data:



```

```
1INSERT INTO hackernews 
2SELECT *
3FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.csv.gz', 'CSVWithNames')
```

```

And next, we’ll add a text index on the `text` column using the `splitByNonAlpha` tokenizer:



```

```
1ALTER TABLE hackernews
2ADD INDEX text_tokens_idx text 
3TYPE text(tokenizer='splitByNonAlpha') 
4GRANULARITY 1;
```

```

And materialize that index:



```

```
1ALTER TABLE hackernews
2(MATERIALIZE INDEX text_tokens_idx)
3SETTINGS mutations_sync = 1;
```

```

This optimization is already enabled in 26\.4, but can be controlled using the `use_text_index_like_evaluation_by_dictionary_scan` setting. The following query counts how many Hacker News posts mentioned Kubernetes:



```

```
1SELECT count()
2FROM hackernews
3WHERE text LIKE '%Kubernetes%'
4SETTINGS use_text_index_like_evaluation_by_dictionary_scan=0;
```

```


```
   ┌─count()─┐
1. │   20070 │
   └─────────┘

1 row in set. Elapsed: 0.832 sec. Processed 18.25 million rows, 6.29 GB (21.93 million rows/s., 7.56 GB/s.)
Peak memory usage: 88.18 MiB.

1 row in set. Elapsed: 0.624 sec. Processed 18.25 million rows, 6.29 GB (29.23 million rows/s., 10.08 GB/s.)
Peak memory usage: 87.93 MiB.

1 row in set. Elapsed: 0.638 sec. Processed 18.25 million rows, 6.29 GB (28.60 million rows/s., 9.86 GB/s.)
Peak memory usage: 86.01 MiB.

```

And now using the optimization:



```

```
1SELECT count()
2FROM hackernews
3WHERE text LIKE '%Kubernetes%'
4SETTINGS use_text_index_like_evaluation_by_dictionary_scan=1;
```

```


```
   ┌─count()─┐
1. │   20070 │
   └─────────┘

1 row in set. Elapsed: 0.208 sec. Processed 18.25 million rows, 18.25 MB (87.53 million rows/s., 87.53 MB/s.)
Peak memory usage: 2.07 MiB.

1 row in set. Elapsed: 0.225 sec. Processed 18.25 million rows, 18.25 MB (80.98 million rows/s., 80.98 MB/s.)
Peak memory usage: 2.07 MiB.

1 row in set. Elapsed: 0.234 sec. Processed 18.25 million rows, 18.25 MB (77.83 million rows/s., 77.83 MB/s.)
Peak memory usage: 2.07 MiB.

```

The number of rows processed is the same, but the query using the optimization has a best runtime of 208 milliseconds, compared to 624 milliseconds, a little over 3 times faster.


If we compare the query plans, we can see that the one using the optimization scans more than 1,000 fewer granules.


No use of inverted index:



```
    ┌─explain─────────────────────────────────────────────────────────┐
 1. │ Output: count()                                                 │
 2. │                                                                 │
 3. │ Aggregating                                                     │
 4. │ └──Filter ((WHERE + Change column names to column identifiers)) │
 5. │    └──ReadFromMergeTree (default.hackernews)                    │
 6. │          Indexes:                                               │
 7. │            PrimaryKey                                           │
 8. │              Condition: true                                    │
 9. │              Parts: 6/6                                         │
10. │              Granules: 3533/3533                                │
11. │            Skip                                                 │
12. │              Name: text_tokens_idx                              │
13. │              Description: text GRANULARITY 100000000            │
14. │              Condition: (mode: All; tokens: [])                 │
15. │              Parts: 6/6                                         │
16. │              Granules: 3533/3533                                │
17. │            Ranges: 6                                            │
    └─────────────────────────────────────────────────────────────────┘

```

Uses inverted index:



```
    ┌─explain──────────────────────────────────────────────┐
 1. │ Output: count()                                      │
 2. │                                                      │
 3. │ Aggregating                                          │
 4. │ └──Filter                                            │
 5. │    └──ReadFromMergeTree (default.hackernews)         │
 6. │          Indexes:                                    │
 7. │            PrimaryKey                                │
 8. │              Condition: true                         │
 9. │              Parts: 6/6                              │
10. │              Granules: 3533/3533                     │
11. │            Skip                                      │
12. │              Name: text_tokens_idx                   │
13. │              Description: text GRANULARITY 100000000 │
14. │              Condition: (mode: All; tokens: [])      │
15. │              Parts: 6/6                              │
16. │              Granules: 2247/3533                     │
17. │            Ranges: 190                               │
    └──────────────────────────────────────────────────────┘

```

## Faster COUNT DISTINCT [\#](/blog/clickhouse-release-26-04#faster-count-distinct)


### Contributed by Jiebin Sun [\#](/blog/clickhouse-release-26-04#contributed-by-jiebin-sun)


There are a couple of improvements to `uniqExact` (used by `COUNT(DISTINCT ...)`) on high\-core\-count machines:


- ClickHouse no longer spawns redundant threads during the merge phase. uniqExact uses a two\-level hash table with 256 buckets, but previously, ClickHouse would spawn up to `max_threads` threads regardless, and many of them would have nothing to do and exit immediately.
- When merging N intermediate hash tables (one per aggregation thread), the thread pool was initialized N times, causing `O(N × threads)` total thread spawns and severe lock contention. Now, all N hash tables are merged in a single pass \- each thread processes one bucket across all hash tables at once, reducing thread pool initializations from `O(N)` to `O(1)`.


In some of our benchmarks, we saw speedups of 3 to 15 times on a 288\-core machine.


This, however, is very much an optimization for machines with many cores \- I tried it out on the HackerNews dataset on my Mac M2 Max (which has 12 cores) and didn’t see any improvement!


## Even prettier EXPLAIN [\#](/blog/clickhouse-release-26-04#even-prettier-explain)


### Contributed by Kirill Kopnev [\#](/blog/clickhouse-release-26-04#contributed-by-kirill-kopnev)


`EXPLAIN PLAN pretty=1` now prints expressions in a human\-readable form, shows top\-level output columns and per\-step output columns, and labels JOINs with estimated row counts and locality.


Let’s see how this works with the following query:



```

```
1EXPLAIN pretty = 1
2SELECT by, count()
3FROM hackernews
4WHERE (text LIKE '%OpenAI%') AND (text LIKE '%Google%')
5GROUP BY ALL
6ORDER BY count() DESC, by
7LIMIT 10;
```

```

26\.3



```

   ┌─explain────────────────────────────────────────────────────────────────────────────┐
1. │ Expression (Project names)                                                         │
2. │ └──Limit (preliminary LIMIT)                                                       │
3. │    └──Sorting (Sorting for ORDER BY)                                               │
4. │       └──Expression ((Before ORDER BY + Projection))                               │
5. │          └──Aggregating                                                            │
6. │             └──Expression (Before GROUP BY)                                        │
7. │                └──Expression ((WHERE + Change column names to column identifiers)) │
8. │                   └──ReadFromMergeTree (default.hackernews)                        │
   └────────────────────────────────────────────────────────────────────────────────────┘

```

26\.4



```
    ┌─explain─────────────────────────────────────────────────────┐
 1. │ Output: by, count()                                         │
 2. │                                                             │
 3. │ Expression (Project names)                                  │
 4. │ └──Limit (preliminary LIMIT)                                │
 5. │    └──Sorting (Sorting for ORDER BY)                        │
 6. │       └──Expression ((Before ORDER BY + Projection))        │
 7. │          └──Aggregating                                     │
 8. │             └──Expression (Before GROUP BY)                 │
 9. │                └──Expression                                │
10. │                   └──ReadFromMergeTree (default.hackernews) │
    └─────────────────────────────────────────────────────────────┘

```

## JSONAllValues \+ text index [\#](/blog/clickhouse-release-26-04#jsonallvalues--text-index)


### Contributed by Anton Popov [\#](/blog/clickhouse-release-26-04#contributed-by-anton-popov)


ClickHouse 26\.4 adds the `JSONAllValues`, which returns every leaf value of a JSON column as `Array(String)`. We can create a text index on top of this, enabling more efficient filtering on JSON subcolumns.


Let’s have a look at how this works with help from the [StatsBomb dataset](https://github.com/statsbomb/open-data/tree/master). Let’s get a subset of the data on our machine by running the following:



```

```
1git clone --filter=blob:none --sparse https://github.com/statsbomb/open-data.git
2cd open-data
3git sparse-checkout set data/events
```

```

We’ll create the following table using clickhouse\-local:



```

```
1CREATE TABLE events (
2      match_id UInt32,
3      json JSON(id String, index UInt32),
4      INDEX vals JSONAllValues(json) TYPE text(tokenizer = 'ngrams') GRANULARITY 1
5  )
6  ENGINE = MergeTree
7  ORDER BY (match_id, json.index);
```

```

And then insert the data:



```

```
1INSERT INTO events
2SELECT
3  toUInt32(replaceRegexpOne(_file, '\\.json$', '')) AS match_id,
4  json
5FROM file('open-data/data/events/*.json', JSONAsObject);
```

```


```
12188949 rows in set. Elapsed: 1275.404 sec. Processed 12.19 million rows, 10.48 GB (9.56 thousand rows/s., 8.22 MB/s.)
Peak memory usage: 1.87 GiB.

```

Just for our understanding of how the index works, let’s have a look at what the `JSONAllValues` function returns:



```

```
1SELECT JSONAllValues(json) FROM events LIMIT 1
2FORMAT Vertical;
```

```


```
JSONAllValues(json): ['[36.4,21.7]','1.013174','000000b5-8156-429d-9088-e62a6ac2ea0d','2529','[36.8,20]','60','2','4','From Throw In','10958','Chris Smalling','5','Left Center Back','123','39','Manchester United','[\'5fbbde9b-74ab-48e9-9873-ef956db384de\',\'fd43cc18-c37b-438a-8a40-a8bb50e59469\']','18','39','Manchester United','00:15:18.727','43','Carry']

```

The dataset has just over 12 million records, which isn’t really enough to see the impact of the index, so we’ll duplicate the data a bunch of times:



```

```
1ALTER TABLE events
2ATTACH PARTITION ID 'all'
3FROM events;
```

```


```
0 rows in set. Elapsed: 3.892 sec.
0 rows in set. Elapsed: 7.957 sec.
0 rows in set. Elapsed: 15.894 sec.
0 rows in set. Elapsed: 33.655 sec.
0 rows in set. Elapsed: 68.870 sec.

```

And now we’ve got a lot more records:



```

```
1SELECT count()
2FROM events;
```

```


```
   ┌───count()─┐
1. │ 390046368 │ -- 390.05 million
   └───────────┘

```

The following query returns the number of rows related to Lionel Messi:



```

```
1SELECT count()
2FROM events
3WHERE json.player.name = 'Lionel Andrés Messi Cuccittini'
4SETTINGS use_skip_indexes = 1;
```

```

We can disable the text index by setting `use_skip_indexes = 0`. Running this query gives us the following result:



```
   ┌─count()─┐
1. │ 4268960 │ -- 4.27 million
   └─────────┘

```

We’ll run it three times without the index:



```
1 row in set. Elapsed: 1.505 sec. Processed 390.05 million rows, 13.87 GB (259.20 million rows/s., 9.22 GB/s.)
Peak memory usage: 48.23 MiB.

1 row in set. Elapsed: 1.666 sec. Processed 390.05 million rows, 13.87 GB (234.12 million rows/s., 8.32 GB/s.)
Peak memory usage: 48.23 MiB.

1 row in set. Elapsed: 1.668 sec. Processed 390.05 million rows, 13.87 GB (233.88 million rows/s., 8.32 GB/s.)
Peak memory usage: 48.23 MiB.

```

And three times with the index:



```
1 row in set. Elapsed: 1.139 sec. Processed 80.64 million rows, 3.23 GB (70.80 million rows/s., 2.84 GB/s.)
Peak memory usage: 69.25 MiB.

1 row in set. Elapsed: 1.096 sec. Processed 80.64 million rows, 3.23 GB (73.61 million rows/s., 2.95 GB/s.)
Peak memory usage: 68.93 MiB.

1 row in set. Elapsed: 1.087 sec. Processed 80.64 million rows, 3.23 GB (74.21 million rows/s., 2.97 GB/s.)
Peak memory usage: 74.13 MiB.

```

From the processed rows, we can see that the index reduces the amount of data to scan by almost 5 times. The best time without the index is 1,505 milliseconds, compared to 1,087 milliseconds with the index, an improvement of around 50%.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-556-get-started-today-sign-up&utm_blogctaid=556)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

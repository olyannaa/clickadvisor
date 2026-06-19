# ClickHouse Release 22\.12


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 22\.12

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 19, 2022 · 11 minutes readIt’s a holiday bonanza.


The delivery of 11 months of regular releases wasn’t enough for the team. Neither was the Early Access, Beta, and GA of ClickHouse Cloud. Speaking of which, if you want the easiest way to run ClickHouse in production (or for development) start a free trial of [ClickHouse Cloud](https://clickhouse.cloud/signUp&loc=blog) today.


As a holiday gift, we are pleased to introduce 22\.12\.


## Release Summary [\#](/blog/clickhouse-release-22-12#release-summary)


17 new features. 8 performance optimisations. 39 bug fixes.


If that’s not enough to get you interested in trying it out. Check out some of the headline items:


- `grace_hash` JOINs
- password complexity rules
- BSON support
- `GROUP BY ALL` support
- Addition of a Prometheus endpoint for ClickHouse Keeper


And, of course, a host of performance improvements.


## Helpful Links [\#](/blog/clickhouse-release-22-12#helpful-links)


- [22\.12 Release Changelog](https://clickhouse.com/docs/en/whats-new/changelog/)
- [22\.12 Release Presentation](https://presentations.clickhouse.com/release_22.12)
- [ClickHouse 22\.12 Release Webinar](https://www.youtube.com/watch?v=sREupr6uc2k)



## Grace Hopper Hash Join (Sergei Skvortsov \+ Vladimir Cherkasov) [\#](/blog/clickhouse-release-22-12#grace-hopper-hash-join-sergei-skvortsov--vladimir-cherkasov)


Historically, in ClickHouse, users had a few choices with respect to joins: either use the `hash` method, which is fast but memory\-bound or revert to using the `partial_merge` algorithm. The latter relies on sorting data and dumping it to disk, often overcoming memory at the expense of performance. While this at least allowed users to execute large joins, it often suffered from slow performance. With this release, we introduce an exciting non\-memory bound addition to the join algorithms, which overcomes some of the performance challenges of partial merge: The Grace Hash.


The [Grace Hash algorithm](https://en.wikipedia.org/wiki/Hash_join#Grace_hash_join) utilizes a two\-phased approach to joining the data. Our implementation differs slightly from the [classic algorithmic description](https://www.youtube.com/watch?v=GRONctC_Uh0) in order to fit our query pipeline.


Our first phase reads the right table and splits it into N buckets depending on the hash value of key columns (initially, N is `grace_hash_join_initial_buckets`). This is done in a way to ensure that each bucket can be processed independently. Rows from the first bucket are added to an in\-memory hash table while the others are saved to disk. If the hash table grows beyond the memory limit (e.g., as set by `max_bytes_in_join`), we increase the number of buckets and recompute the assigned bucket for each row. Any rows which don’t belong to the current bucket are flushed and reassigned.


![right-side-grace.png](/uploads/right_side_grace_8054638766.png)
The left table is then read. Rows corresponding to the first bucket are joined (as the hash table is in memory), with others being flushed to their appropriate disk\-based bucket. The key in both of these steps is that the hash function will consistently assign values to the same bucket, thereby effectively partitioning the data and solving the problem by decomposition.


![left-side-grace.png](/uploads/left_side_grace_c09fcd9258.png)
After we finish reading the left table, we must process the remaining buckets on disk. These are processed sequentially. We build the hash table for each bucket from the right table data. Again, if we run out of memory, we must increase the number of buckets. Once a hash table has been built from a right bucket, we stream the left bucket and complete the join for this pair. Note that during this step, we may get some rows that belong to another bucket other than the current due to them being saved before the number of buckets was increased. In this case, we save them to the new actual buckets and process them further. This process is repeated for all of the remaining buckets.


![grace-final-step.png](/uploads/grace_final_step_8424107c1a.png)
This approach of partitioning data ensures that we can both limit memory and the number of times we need to scan each table. Both sides of the table are scanned twice \- once for partitioning the data and again for the join stage. While not as fast as a hash join, the performance benefits can be appreciable compared to the `partial_merge`.


**Now let's take a practical example.**


In our [play.clickhouse.com](https://sql.clickhouse.com?query_id=GEFQJZTCMQPSB8ZMDCHJWK), we maintain an anonymized [web analytics dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/metrica) in the table `hits`. Every row in this table represents a website click, recording details such as the browser agent and url. The dataset also includes a `Referer` column (also a URL), indicating the previous location from which the visitor arrived for each URL. Suppose we identify the previous two pages visited prior to a URL, not just the immediate referer. We could solve this with a sort by time, but let's make it deliberately more tricky and solve it with graph analysis. This requires us to effectively do graph navigation of depth 2, as shown below:


![url-self-join.png](/uploads/url_self_join_511e5fc0c9.png)
This can be realized in SQL as a self\-join, where we join the `hits` table to itself by looking for pairs of rows that share a common URL and Referer value.



```

SELECT
	UserID,
	h1.Referer,
	h1.URL,
	h2.URL
FROM hits AS h1
INNER JOIN hits AS h2 ON h1.UserID = h2.UserID AND h1.URL = h2.Referer
WHERE h1.URL != '' AND h2.URL != '' AND h1.Referer != '' AND h2.Referer != ''
ORDER BY UserID ASC
LIMIT 10


```


While the results to this query aren’t particularly interesting, we note the performance and memory overhead for the `hash`, `parallel_hash`, `partial_merge` and `grace_join` algorithms below.


![hash-algorithms.png](/uploads/hash_algorithms_061cca0703.png)
![hash-join-results.png](/uploads/hash_join_results_ee7184297b.png)
Note: the `parallel_hash` is a variation of a `hash` join that splits the data into buckets and builds several hash tables concurrently, instead of one, to speed up the join at the expense of higher memory overhead.


The results here are quite clear. Grace offers improved performance over `partial_merge` at the expense of more memory overhead. While hash, and more so `parallel_hash`, are considerably faster, you pay an overhead and rely on having sufficient memory. The choice here is up to the user. Note that these results will vary depending on your data and query.


Note the Grace Hash test here was run with the setting `grace_hash_join_initial_buckets=128`. The primary benefit of selecting a “correct” value for `grace_hash_join_initial_buckets` is it avoids the re\-bucketing we described earlier \- potentially speeding up the JOIN. For now, this is left to the user to tune manually.


## Enforce password complexity rules (Nikolay Degterinsky) [\#](/blog/clickhouse-release-22-12#enforce-password-complexity-rules-nikolay-degterinsky)


ClickHouse considers security to be a first\-class citizen. Prior to 22\.12, users could create passwords with no enforcement of complexity. While we trust our users to be responsible, mistakes and oversights happen, and weak passwords could be created. We needed to close this for our own needs with ClickHouse Cloud, but also something our community needed.


Password enforcement can be set by adding a `password_complexity` config key to your server configuration. An example of 4 rules enforcing a strong standard:



```

$ cat /etc/clickhouse-server/config.d/rules.yaml
password_complexity:
  - rule:
    pattern: '.{12}'
    message: 'be at least 12 characters long'
  - rule:
    pattern: '\p{N}'
    message: contain at least 1 numeric character
  - rule:
    pattern: '\p{Lu}'
    message: contain at least 1 uppercase character
  - rule:
    pattern: '[^\p{L}\p{N}]'
    message: contain at least 1 special character


```


Attempts to violate this policy now result in an error e.g.,



```

clickhouse-cloud:) CREATE USER vasyan IDENTIFIED WITH sha256_password BY 'qwerty123'

DB::Exception: Invalid password. The password should: be at least 12 characters long, contain at least 1 uppercase character, contain at least 1 special character.


```


We always recommend users create users and set passwords using `clickhouse-client`. As well as confirming the password satisfies the rules on the client side, it also ensures plain text passwords are never transmitted to the server.


## BSON Support (Pavel Kruglov, Mark Polokhov) [\#](/blog/clickhouse-release-22-12#bson-support-pavel-kruglov-mark-polokhov)


BSON (Binary Javascript Object Notation) is a binary\-encoded Javascript Object Notation (JSON) format used for data storage and network transfer in MongoDB. Whilst based on JSON, it has a few advantages: specifically, it supports additional types such as dates and binary data as well as being faster to build and scan due to length and array indexing being encoded into the format. We expect most users to find this useful when interacting with dumps created by the [mongodump](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump) tool.


The [Mongo sample datasets](https://www.mongodb.com/docs/atlas/sample-data/) provide some useful examples to test this feature. Assuming you’ve [loaded these](https://www.mongodb.com/docs/atlas/sample-data/) into your Mongo or Atlas instance, exporting and querying with ClickHouse couldn’t be simpler. Below we use [clickhouse\-local](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local/) and query the [comments from the movies dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#sample_mflix.comments).



```

mongodump --uri="/sample_mflix" --username=default --db=sample_mflix --collection=comments --out=comments

clickhouse-local

SELECT count()
FROM file('comments/sample_mflix/comments.bson', BSONEachRow)

┌─count()─┐
│   41079 │
└─────────┘

1 row in set. Elapsed: 0.236 sec. Processed 36.86 thousand rows, 21.18 MB (156.37 thousand rows/s., 89.84 MB/s.)


SELECT
    name,
    text
FROM file('comments/sample_mflix/comments.bson', BSONEachRow)
LIMIT 1
FORMAT Vertical

Query id: 7d522673-f124-4598-bdff-86b12f2905d1

Row 1:
──────
name: Mercedes Tyler
text: Eius veritatis vero facilis quaerat fuga temporibus. Praesentium expedita sequi repellat id. Corporis minima enim ex. Provident fugit nisi dignissimos nulla nam ipsum aliquam.

1 row in set. Elapsed: 0.048 sec.


```


## ClickHouse Keeper \- Prometheus Endpoint (Antonio Andelic) [\#](/blog/clickhouse-release-22-12#clickhouse-keeper---prometheus-endpoint-antonio-andelic)


We have considered ClickHouse Keeper to be production ready for some time and would encourage all of our users to migrate from Zookeeper where possible. For some users, however, the ability to monitor ClickHouse Keeper in their deployments using the same approach as their legacy Zookeeper instances represented a blocker to migration. As well as improving write performance at high request rates with this release, we have therefore also added a Prometheus endpoint to ClickHouse Keeper to allow monitoring of this critical piece of software in your ClickHouse cluster. Hopefully, this unblocks some migrations and more users can benefit from more stable cluster coordination under load.



```

$ cat /etc/clickhouse-keeper/config.d/prometheus.yaml
prometheus:
	port: 9369
	endpoint: /metrics


```


## GROUP BY ALL (TaoFengLiu) [\#](/blog/clickhouse-release-22-12#group-by-all-taofengliu)


New users of ClickHouse, coming from OLTP databases such as Postgres, quickly find ClickHouse differs from ANSI SQL in a few ways. This is often deliberate as we feel these differences make analytical queries simpler and more succinct to write. In a few cases, however, we just have a few functional gaps which we’re eager to close. One of these is the ability to use the `ALL` clause in a GROUP BY. This simple feature means the user doesn’t need to repeat the columns from their SELECT clause, which aren’t aggregate functions, making queries even shorter and faster to write. Since we love speed, you can now utilize this feature in 22\.12 [thanks to a community contribution](https://github.com/ClickHouse/ClickHouse/pull/42265).



```

SELECT
	county,
	town,
	district,
	street,
	median(price) AS med_price,
	count() AS c
FROM uk_price_paid
WHERE toYear(date) = 2022
GROUP BY county, town, district, street
ORDER BY count() DESC
LIMIT 10

// and even simpler with ALL

SELECT
	county,
	town,
	district,
	street,
	median(price) AS med_price,
	count() AS c
FROM uk_price_paid
WHERE toYear(date) = 2022
GROUP BY ALL
ORDER BY count() DESC
LIMIT 10


```

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

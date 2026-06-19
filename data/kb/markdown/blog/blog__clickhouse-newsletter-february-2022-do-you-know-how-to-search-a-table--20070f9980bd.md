# ClickHouse Newsletter February 2022: Do you know how to search a table?


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter February 2022: Do you know how to search a table?

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Feb 10, 2022 · 8 minutes read
Happy (Lunar) New Year! 2021 was a big year for us; we founded a company and brought you 12 new releases. Looking to catch up now that we’re all back from the holiday season?


Our favorite features are below, along with an invite to this month’s webinar, this month’s query tips, and more. Welcome to your monthly dose of ClickHouse goodness.


## **Top 5 New Features in ClickHouse from 2021** [\#](/blog/clickhouse-newsletter-february-2022-do-you-know-how-to-search-a-table#top-5-new-features-in-clickhouse-from-2021)


Across 12 monthly releases, the ClickHouse team and our community of amazing contributors have released hundreds of features and improvements. These are our favorites:


1. **[ClickHouse Keeper](https://clickhouse.com/docs/en/operations/clickhouse-keeper/)**, our alternative to Apache ZooKeeper, is feature complete! Now ClickHouse is a “true” single binary and you don’t need anything else to get going. Keeper is fully protocol\-compatible with the original ZooKeeper — so you can also use it for your Hadoop or Kafka deployments.
2. **[Asynchronous insert](https://clickhouse.com/docs/en/operations/settings/settings/#async-insert)** mode now makes it possible to make many small INSERTs to your ClickHouse cluster without running into the dreaded “Too many parts” error. Turn it on using the `async_insert` setting.
3. **[User\-defined functions (UDF)](https://clickhouse.com/docs/en/sql-reference/functions/#user-defined-functions)** allows you to extend ClickHouse with any extra functionality you need! You can define UDFs as lambda expressions or call external scripts in any programming language. The latter makes it especially useful for any ML/AI/NLP use cases you have. Check out the tutorial [here](https://clickhouse.com/learn/lessons/whatsnew-clickhouse-21.10/#3--creating-user-defined-functions-udfs).
4. **New data types: [Map](https://clickhouse.com/docs/en/sql-reference/data-types/map/), [Bool](https://github.com/ClickHouse/ClickHouse/issues/30684), [UInt128](https://clickhouse.com/docs/en/sql-reference/data-types/int-uint/)** make it even easier to ingest all your data into ClickHouse. And the [Nested](https://clickhouse.com/docs/en/sql-reference/data-types/nested-data-structures/nested/) data type now supports arbitrary levels of nesting.
5. **[Positional arguments](https://clickhouse.com/docs/en/operations/settings/settings/#enable-positional-arguments)** are now supported! A small but useful feature for users familiar with other databases, you can turn it on with the `​​enable_positional_arguments` setting.


For more information about what we’ve added to your favorite database in the last year, catch up on our [blog](https://clickhouse.com/blog/en/), watch the recordings of our release webinars on our [YouTube channel](https://www.youtube.com/c/ClickHouseDB), or get into the (deep) details by checking out the [changelog](https://clickhouse.com/docs/en/whats-new/changelog/2021/).


## **Upcoming Release v22\.2** [\#](/blog/clickhouse-newsletter-february-2022-do-you-know-how-to-search-a-table#upcoming-release-v222)


Our next monthly release is just around the corner! We’re expecting to add text classification functions and flexible memory limits. As always, we’ll be hosting a release webinar where you’ll have the opportunity to ask and get answers to your questions live.


**When**: 9 a.m. PST / 5 p.m. GMT, February 17th


**How to join**: Add the **[invite to your calendar](https://www.google.com/calendar/render?action=TEMPLATE&text=ClickHouse+v22.2+Release+Webinar&details=Join+from+a+PC%2C+Mac%2C+iPad%2C+iPhone+or+Android+device%3A%0A%C2%A0+%C2%A0+Please+click+this+URL+to+join.%C2%A0%0Ahttps%3A%2F%2Fzoom.us%2Fj%2F92785669470%3Fpwd%3DMkpCMU9KSmpNTGp6WmZmK2JqV0NwQT09%0A%0A%C2%A0+%C2%A0+Passcode%3A+139285%0A%0A%C2%A0Description%3A+Connect+with+ClickHouse+experts+and+test+out+the+newest+features+and+performance+gains+in+the+v22.2+release.%0A%0AOr+One+tap+mobile%3A%0A%C2%A0+%C2%A0+%2B12532158782%2C%2C92785669470%23%2C%2C%2C%2C%2A139285%23+US+%28Tacoma%29%0A%C2%A0+%C2%A0+%2B13462487799%2C%2C92785669470%23%2C%2C%2C%2C%2A139285%23+US+%28Houston%29%0A%0AOr+join+by+phone%3A%0A%C2%A0+%C2%A0+Dial%28for+higher+quality%2C+dial+a+number+based+on+your+current+location%29%3A%0A%C2%A0+%C2%A0+%C2%A0+%C2%A0+US%3A+%2B1+253+215+8782+or+%2B1+346+248+7799+or+%2B1+669+900+9128+or+%2B1+301+715+8592+or+%2B1+312+626+6799+or+%2B1+646+558+8656%C2%A0%0A%C2%A0+%C2%A0%C2%A0%0A%C2%A0+%C2%A0+Webinar+ID%3A+927+8566+9470%0A%C2%A0+%C2%A0+Passcode%3A+139285%0A%C2%A0+%C2%A0+International+numbers+available%3A+https%3A%2F%2Fzoom.us%2Fu%2FalqvP0je9&location=https%3A%2F%2Fzoom.us%2Fj%2F92785669470%3Fpwd%3DMkpCMU9KSmpNTGp6WmZmK2JqV0NwQT09&dates=20220217T170000Z%2F20220217T180000Z)**, or **[click this link](https://zoom.us/j/92785669470)** on February 17th.


## **Query of the Month: Full\-text search a table** [\#](/blog/clickhouse-newsletter-february-2022-do-you-know-how-to-search-a-table#query-of-the-month-full-text-search-a-table)


Ever wondered how you can search all the columns of a table at once, like with a search engine? You can do it with ClickHouse! There are a few options and they use some neat features in ClickHouse that you might not (yet) know.


**Option 1:**



```
SELECT * FROM hackernews WHERE formatRow('TSV', *) ILIKE '%i love clickhouse%'

```

This query uses the [formatRow](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions/#formatrow) function to concatenate all columns into a long tab\-separated string and searches through it using `ILIKE`.


**Option 2:**



```
SELECT * FROM hackernews WHERE concat(* APPLY x -> concat(toString(x), '<<>>')) ILIKE '%i love clickhouse%'

```

In this query, we also concatenate all columns, but instead of using tabs as separators we can specify the separator ourselves, in this case `<<>>`. [APPLY](https://clickhouse.com/docs/en/sql-reference/statements/select/#apply-modifier) is a wonderful modifier that allows us to invoke a function (in this case, a [higher\-order lambda expression](https://clickhouse.com/docs/en/sql-reference/functions/#higher-order-functions)) on any expression (all columns in this case, but we could have specified a subset of columns using the handily named [COLUMNS expression](https://clickhouse.com/docs/en/sql-reference/statements/select/#columns-expression)).


**Option 3:**



```
SELECT * FROM hackernews WHERE (arrayExists(x -> positionCaseInsensitiveUTF8(x, 'i love clickhouse') > 0, array(* APPLY x -> toString(x))))

```

Have you noticed what can happen when using the first two options? Because all columns are simply concatenated into one big string it is possible to search across columns if one (knowingly or accidentally) searches for the column separator. The last query here eliminates the problem by gathering all columns into an array instead and using the [arrayExists](https://clickhouse.com/docs/en/sql-reference/functions/array-functions/#arrayexistsfunc-arr1) function to check if there is any one element that contains the phrase we are searching for.


When running any of these queries on the [Hacker News dataset](https://github.com/ClickHouse/ClickHouse/issues/29693) they all find the comment “I love clickhouse: it’s simple yet flexible enough and free software.” Aw shucks, we love ClickHouse too!


Have you written an interesting query recently that you think others could learn from? [Let us know on twitter](https://twitter.com/clickhousedb), we’d love to hear from you!


## **Reading Corner** [\#](/blog/clickhouse-newsletter-february-2022-do-you-know-how-to-search-a-table#reading-corner)


What we’ve been reading at the start of the year:


1. [What’s New in ClickHouse 22\.1](https://clickhouse.com/blog/en/2022/clickhouse-v22.1-released/) – our v22\.1 release blog post, announcing automatic schema inference, parallel query processing on multiple replicas, a new diagnostic tool for your ClickHouse and more!
2. [Admixer Aggregates Over 1 Billion Unique Users a Day using ClickHouse](https://clickhouse.com/blog/en/2022/a-mixer-aggregates-over-1-billion-unique-users-a-day-using-clickhouse/) – Adtech platform Admixer moved from MSSQL and Azure Table Storage to ClickHouse and is ingesting over 1M rows per second.
3. [Migrating Your Reporting Queries From MongoDB to ClickHouse](https://vkontech.com/migrating-your-reporting-queries-from-a-general-purpose-db-mongodb-to-a-data-warehouse-clickhouse-performance-overview/) – Benchmarking MongoDB versus ClickHouse for analytics queries. Spoiler alert: ClickHouse is faster!
4. ​​[Historical Traffic Analysis at Scale: Using ClickHouse with ntopng](https://www.ntop.org/ntop/historical-traffic-analysis-at-scale-using-clickhouse-with-ntopng/) – high\-speed flow collection and storage with ClickHouse.
5. [How ClickHouse, Inc. Is Building a Best\-in\-Class Engineering Culture](https://www.indexventures.com/perspectives/how-clickhouse-inc-is-building-a-best-in-class-engineering-culture/) – learn a bit about how we are building our engineering team at ClickHouse from our very own Yury Izrailevsky. (Spoiler: It is not about telling people what to do every day.)


[New ClickHouse Adopters](https://clickhouse.com/docs/en/introduction/adopters/): ntop, Superwall, Muse, and NLMK. Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team


Photo by [Fabien Maurin](https://unsplash.com/@fabienmaurin?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

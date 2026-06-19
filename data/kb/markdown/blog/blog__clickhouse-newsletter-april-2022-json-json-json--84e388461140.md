# ClickHouse Newsletter April 2022: JSON, JSON, JSON


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter April 2022: JSON, JSON, JSON

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Apr 14, 2022 · 7 minutes read
Greetings from Amsterdam, where tulips are in full bloom this time of year. Here is your April newsletter for all things ClickHouse. We have a new release with a really, really, really exciting feature (Is this maybe too much excitement? We don’t think so!), new content on the ClickHouse website and more. Let’s dive in!


Also, the next release is rapidly approaching and we invite you to join the [Release Webinar](https://clickhouse.com/company/events/v22-4-release-webinar/) to hear about the new features, on the day of release, directly from the ClickHouse team.


## **ClickHouse Cloud waitlist is now open!** [\#](/blog/clickhouse-newsletter-april-2022-json-json-json#clickhouse-cloud-waitlist-is-now-open)


Those of you that have talked to us at ClickHouse Inc. know that we have been hard at work developing the world’s first serverless managed cloud offering of ClickHouse. As many of you know, getting started with ClickHouse is easy (it’s a single binary, so you just download and run it wherever), but running ClickHouse at scale with replication and sharding is not quite so straightforward.


We’re developing ClickHouse Cloud as a “serverless” service, meaning that you don’t have to configure any instances and choose CPU, memory and storage configurations. It’s all taken care of for you in the background. If this sounds interesting to you, sign up for the waitlist for ClickHouse Cloud [here](https://clickhouse.com/cloud/).


## **Getting Started with ClickHouse** [\#](/blog/clickhouse-newsletter-april-2022-json-json-json#getting-started-with-clickhouse)


Speaking of new website content take a look at this 25\-minute video on Getting Started with ClickHouse. ClickHouse is getting increasingly popular with many newcomers using it for the first time. To help them, we’ve tried to condense all the important information you need to know to get going with ClickHouse into one video the length of a coffee break (that is, unless you only drink espresso). Have a listen [here](https://clickhouse.com/company/events/getting-started-with-clickhouse/) and send it to your friends that don’t know ClickHouse yet!


## **ClickHouse v22\.3** [\#](/blog/clickhouse-newsletter-april-2022-json-json-json#clickhouse-v223)


On March 17, we released ClickHouse 22\.3 LTS with lots of new features (especially one that we are very excited about). It is also a Long Term Support (LTS) release, so you can use it for the next year and we’ll keep the bug fixes coming. If you’re not planning to upgrade your ClickHouse monthly with the newest available version you should be on an LTS release!


What’s in 22\.3:


1. [JSON](https://presentations.clickhouse.com/release_22.3/) is a new data type that allows you to ingest any JSON documents directly into a column. Under the hood, ClickHouse will create dynamic subcolumns to store the data, so access is still fast.


Historically, when storing JSON documents in ClickHouse you would create table columns for each field. This works well if you know beforehand what your data is going to look like. But with JSON this is often not the case, especially if it is logs from different applications and services, for example. To get this kind of “semi\-structured” data into ClickHouse, it was often necessary to develop [sophisticated data schemas](https://eng.uber.com/logging/) involving arrays and materialized columns.


No longer! Now it can all just go into one column of type JSON. It’s a really powerful feature and we’re very excited about it, so give it a go and let us know what you think.
2. **ARM** builds are now available [as Docker images](https://hub.docker.com/r/clickhouse/clickhouse-server/tags)! For example, you can run ClickHouse on macOS using Docker with `docker run clickhouse/clickhouse-server`. All functional tests are now passing for ARM builds in our CI. In addition you can now obtain deb, rpm, apk, and binary packages.
3. **[S3 disks](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree/#table_engine-mergetree-s3)** as storage for ClickHouse are now fully tested as well. You can configure using S3 for storage in the `<storage_configuration>` section of the ClickHouse configuration file. Note: There are still some performance issues that we are working on.
4. The **[Hive table function](https://github.com/ClickHouse/ClickHouse/pull/34946)** allows you to read data from Apache Hive tables directly and combine it with data in ClickHouse. Or insert the data into ClickHouse using `INSERT INTO clickhouse_table SELECT * FROM hive(...)`.


For more details including live demos have a look at the release webinar recording [here](https://www.youtube.com/watch?v=GzeANZzPras). Also, [register](https://clickhouse.com/company/events/v22-4-release-webinar/) for the April release webinar of version 22\.4 on Thursday, April 21 @ 9 am PST / 5 pm GMT.


We hope you enjoy this release and please upgrade!


## **Query of the Month: JSON, JSON, JSON** [\#](/blog/clickhouse-newsletter-april-2022-json-json-json#query-of-the-month-json-json-json)


Let’s take the new JSON data type for a spin:



```
SET allow_experimental_object_type = 1;
CREATE TABLE json (o JSON) ENGINE = Memory
INSERT INTO json VALUES ('{"a": 1, "b": { "c": 2, "d": [1, 2, 3] }}')
SELECT o.a, o.b.c, o.b.d[3] FROM json

```

The select statement will return 1, 2, 3 and you can see how JSON objects in ClickHouse support nested objects and arrays and how neat the query syntax is.


You might already have JSON data in a file somewhere. To insert it into a JSON column ClickHouse, you can run something like:



```
CREATE TABLE logs (message JSON) ENGINE = MergeTree ORDER BY tuple()
INSERT INTO logs SELECT json FROM file(log.json.gz', JSONAsString)

```

Note how we use the `JSONAsString` format to prevent ClickHouse treating each JSON field as its own column (and even with the new JSON data type, if your data is structured and the fields are known, you should still consider doing that).


Note also that we cannot sort the MergeTree table by anything in the data, because with JSON, we do not yet know the structure of the data beforehand. For large datasets, not having a sorting key is bad! In practice, we will often want to extract at least some important and common fields from a JSON document into their own columns. For example, the timestamp:



```
CREATE TABLE logs (
	timestamp DateTime,
	message JSON
) ENGINE = MergeTree ORDER BY timestamp


INSERT INTO logs
SELECT parseDateTimeBestEffort(JSONExtractString(json, 'timestamp')), json
FROM file('access.json.gz', JSONAsString)

```

Lastly, when displaying a JSON column ClickHouse only shows the field values by default (because internally, it is represented as a tuple). You can display the field names as well like this:



```
SELECT message FROM logs FORMAT JSONEachRow
SETTINGS output_format_json_named_tuples_as_objects = 1

```

Give this new data type a try and let us know what you think!


## **Reading Corner** [\#](/blog/clickhouse-newsletter-april-2022-json-json-json#reading-corner)


What we’ve been reading:


1. [Building a Paste Service With ClickHouse](https://clickhouse.com/blog/building-a-paste-service-with-clickhouse/): Alexey explores building a Pastebin\-style service using many ClickHouse anti\-patterns (the post was published on April 1, but it’s only half in jest and the service actually works!).
2. [International Women’s Day @ ClickHouse](https://clickhouse.com/blog/stories-of-difference-inspiration-courage-and-empathy-international-womens-day-2022/): Read stories of the women that bring ClickHouse to you every month and some of their experiences as women in tech.
3. [Fast Indexing for Data Streams](https://clickhouse.com/blog/fast-indexing-for-data-streams-benocs-telco/): BENOCS is using ClickHouse to collect and visualize network traffic for large telcos worldwide.
4. [ClickHouse 22\.3 release blog post](https://clickhouse.com/blog/clickhouse-22-3-lts-released/) – learn more about our 22\.3 release and what’s in it.
5. [New ClickHouse Adopters](https://clickhouse.com/docs/en/introduction/adopters/): Welcome [Swetrix Analytics](https://swetrix.com/). Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team


Photo by [Matthew Waring](https://unsplash.com/@matthewwaring?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

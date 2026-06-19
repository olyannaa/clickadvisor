# chDB joins the ClickHouse family


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# chDB joins the ClickHouse family

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)![TanyaBragin.jpeg](/_next/image?url=%2Fuploads%2FTanya_Bragin_84bf5232c3.jpeg&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov) and [Tanya Bragin](/authors/tanya-bragin)Mar 6, 2024 · 6 minutes readToday, we are pleased to announce that [chDB](https://doc.chdb.io/#/), an embedded SQL OLAP engine powered by ClickHouse, is now part of ClickHouse. chDB’s creator and main contributor, Auxten, [is joining forces with us](https://auxten.com/chdb-is-joining-clickhouse) to focus on evolving chDB and integrating it even more closely with the ClickHouse ecosystem.


## What is chDB and how did we get here? [\#](/blog/chdb-joins-clickhouse-family#what-is-chdb-and-how-did-we-get-here)


ClickHouse is best known as a scalable analytics database that uses a client\-server architecture, but we’ve actually always had ClickHouse Local, a CLI tool that contains ClickHouse.


People [became aware of ClickHouse Local at the beginning of 2023](https://news.ycombinator.com/item?id=34265206) and they loved it, but we also got feedback that they wanted to be able to integrate ClickHouse Local with the other tools they were using both in their data pipelines and for data analysis.


Around this same time, Auxten had started working on chDB with the goal of being able to use ClickHouse as an “out of the box” Python module.


You can use chDB to do in\-memory analysis of data that lives locally or remotely in all the formats and sources supported by ClickHouse. You can also choose to persist data in a local ClickHouse instance and chDB uses the same storage format as ClickHouse Local, which means their databases are interchangeable. The diagram below shows how chDB works in comparison to other ClickHouse variants.


![chDB Image 4 updated 2.png](/uploads/ch_DB_Image_4_updated_2_6fd7ed2265.png)
We were really impressed with chDB and contacted Auxten to tell him that we loved his work and wanted to help promote it. This resulted in Alexey mentioning chDB in the [23\.7 release call](https://www.youtube.com/live/TI1kONfON18?si=OhCU6_R58iByNXVQ&t=1872), as well as a subsequent [introductory blog post about chDB](https://clickhouse.com/blog/welcome-chdb-to-clickhouse) in August 2023\. A few weeks later Auxten wrote [chDB \- A Rocket Engine on a Bicycle](https://clickhouse.com/blog/chdb-embedded-clickhouse-rocket-engine-on-a-bicycle), in which he went through chDB’s design decisions and implementation details


In the months since then, [we’ve seen more interest in chDB](https://clickpy.clickhouse.com/dashboard/chdb), have been working closely with Auxten, and gradually saw an opportunity to take our collaboration to the next level.


## What does the news mean if I’m a chDB user? [\#](/blog/chdb-joins-clickhouse-family#what-does-the-news-mean-if-im-a-chdb-user)


If you’re an existing user of chDB, this is great news for you. Auxten will now be working full\-time on chDB rather than only in his spare time. This means we’ll be able to fix bugs/issues more quickly as well as adding new features and integrations.


chDB will soon be integrated into ClickHouse’s continuous integration pipeline, which will allow us to have chDB closely follow the release schedule of ClickHouse.


We’ll be moving the chdB documentation to live alongside the ClickHouse documentation and will make chDB more prominent in our getting started guides.


We’ll also be looking at ways that we can better integrate chDB with the rest of the data engineering ecosystem, so let us know if you have any opinions about where we should start!


## What happens next? [\#](/blog/chdb-joins-clickhouse-family#what-happens-next)


Our goal is to create a seamless experience whether you’re analyzing Parquet files on your laptop, creating data pipelines with other tools in the Python ecosystem, or building a real\-time data warehouse to serve data products to your users.


We want to get to the point where it takes minimal effort to switch between the different flavors of ClickHouse.


We don’t know exactly what this will look like and we’d like your help figuring this out. Below are some of the things at the top of our todo list for what to do next:


1. Better performance, especially on Pandas DataFrame and Arrow Buffer
2. Keep up with latest ClickHouse release
3. Better integration with more programming languages and data sources


But maybe you have better ideas! We’d love to hear your thoughts on the [chDB Github Discussions](https://github.com/orgs/chdb-io/discussions).


## Get started with chDB today [\#](/blog/chdb-joins-clickhouse-family#get-started-with-chdb-today)


In the meantime, if you’re not yet familiar with chDB, we thought we’d include a little example to whet your appetite. chDB is [published on PyPi](https://pypi.org/project/chdb/) and can be installed with the pip package manager. We’ll also install Pandas and pyarrow as we'll be using those too:



```
pip install chdb pandas pyarrow

```

Once that’s installed we can open a Python REPL, Jupyter notebook, or similar and import the following module:



```
import chdb

```

Let’s now look at how to query the Hugging Face [midjourney\-messages](https://huggingface.co/datasets/vivym/midjourney-messages) dataset, which contains metadata about images generated by the Mid Journey Generative AI service over several months in 2023\. This dataset contains 55 million rows spread over 55 Parquet files.


The following query returns the count of images as well as the minimum/maximum size, width, and height:



```
chdb.query("""
FROM url('https://huggingface.co/datasets/vivym/midjourney-messages/resolve/main/data/0000{00..55}.parquet')
SELECT count(), COLUMNS(width, height, size) APPLY(max), COLUMNS(width, height, size) APPLY(min)
SETTINGS max_http_get_redirects=1
""", "Vertical")

Row 1:
──────
count():     55082563
max(width):  18928
max(height): 16128
max(size):   24498571
min(width):  32
min(height): 56
min(size):   312

```

If we want to persist the data from those Parquet files, we can do that as well.



```
from chdb import session as chs

sess = chs.Session("midjourney.chdb")
sess.query("CREATE DATABASE MidJourney")
sess.query("""
CREATE TABLE MidJourney.images
Engine = MergeTree
ORDER BY (size, height, width)
AS
SELECT *
FROM url('https://huggingface.co/datasets/vivym/midjourney-messages/resolve/main/data/0000{00..55}.parquet')
SETTINGS max_http_get_redirects=1, schema_inference_make_columns_nullable=0
""")

```

That will take around 4 minutes to pull down the data and ingest it into ClickHouse. We can then repeat the above query:



```
sess.query("""
FROM MidJourney.images
SELECT count(), COLUMNS(width, height, size) APPLY(max), COLUMNS(width, height, size) APPLY(min)
""", "Vertical")

```

Hopefully that’s given you an idea of what you can do with chDB, but [check out the](https://doc.chdb.io/#/) documentation for even more examples. We look forward to learning what you do with this compact yet powerful way to use ClickHouse in your local projects!


Read more about the history of chDB, and the creator Auxten's perspective, [in his post](https://auxten.com/chdb-is-joining-clickhouse).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

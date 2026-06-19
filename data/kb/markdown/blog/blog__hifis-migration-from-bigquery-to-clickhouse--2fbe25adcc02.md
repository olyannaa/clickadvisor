# HIFI’s migration from BigQuery to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# HIFI’s migration from BigQuery to ClickHouse

![](/_next/image?url=%2Fuploads%2Fhifi_logo_92694123cf.jpg&w=96&q=75)HIFIJan 9, 2023 · 10 minutes read*We would like to welcome HIFI as a guest to our blog. Read on to hear from [John Funge](https://www.linkedin.com/in/funge/) (CTO) and [Akash Saha](https://www.linkedin.com/in/akash-saha-118975139/) (Principal Full Stack Engineer) to find out why they switched from BigQuery to ClickHouse to aggregate royalties data from disparate revenue streams.*


Music royalties flow through dozens of opaque and fragmented sources, making it difficult for artists to track and manage their income. This lack of transparency has created an environment of confusion and disillusionment for music creators. HIFI is building innovative technologies that provide critical financial and business insights for its members to help them make better decisions that drive their careers forward.


One of the products we offer is HIFI Enterprise, which brings intelligent revenue processing to sophisticated businesses handling music royalty data at scale, including companies and funds acquiring music rights and business managers who work with the most notable artists in the world. To make this more concrete, here’s a screenshot of a royalties dashboard in HIFI Enterprise:


![hifi_dashboard.png](/uploads/hifi_dashboard_a2577c71aa.png)
Behind the scenes at HIFI, we ingest a lot of royalty data. For example, a single HIFI Enterprise account can easily have half a gigabyte of associated royalty data representing over 25 million rows of streaming and other transaction data. All that royalty data needs to load into the UI as soon as possible after a customer logs in and there can obviously be multiple customers logging in at the same time. In the past, it could take as long as 30 seconds to load the data and would sometimes not load at all because of timeouts. About a year ago, we started using ClickHouse to help store and organize the royalty data. For those who are unaware, ClickHouse is a fast open\-source column\-oriented database management system that allows for generating analytical data reports in real\-time using SQL queries. According to the website:



> ClickHouse’s performance exceeds all other column\-oriented database management systems. It processes billions of rows and tens of gigabytes of data per server per second.


And from what we’ve seen, it is indeed amazingly fast! Now, even with caching turned off, the largest of our datasets loads in under a few seconds. Our customers are really happy with the user experience and we are confident in our ability to scale as we add more customers and roll out new products.


The speed of ClickHouse is also a huge benefit when calculating internal metrics such as the total royalties we have in the system as well as indicators like the total royalties paid out in the last year. However, if you have a background in traditional relational database management systems, the speed of ClickHouse comes with some surprises! Operations, like joins, do not necessarily work as expected. If that sounds like you, or you're just interested in learning more about ClickHouse in general, then this blog post is for you.


## Before ClickHouse [\#](/blog/hifis-migration-from-bigquery-to-clickhouse#before-clickhouse)


Before we switched to ClickHouse, we stored royalty data in Google Cloud (GCP) using [BigQuery](https://cloud.google.com/bigquery) (BQ). The major challenge with BQ was the pricing structure. This [Quora](https://www.quora.com/Is-Googles-BigQuery-expensive) post captures the problem well:



> It \[BQ] discourages data usage. Instead of encouraging analysts to query the database in any and all ways they can imagine you’ll end up worrying about needing to limit them and come up with processes for controlling the volume of data being used. As a data\-driven company, this notion contradicted our company values.


Google’s solution to this problem is to purchase BQ slots (a dedicated pool) ahead of time, so you don’t need to worry about increasing costs for BQ consumption. For a big established company, with well defined and predictable usage patterns, this makes sense. But for a startup, patterns can change dramatically week to week. We simply don’t want the hassle of trying to figure out in advance of how many BQ slots to purchase \- what a headache!


The other option we considered was just putting royalty data in GCP [Cloud SQL](https://cloud.google.com/sql/postgresql) for PostgreSQL (PG). That’s not really what PG was designed for and from our testing it didn’t seem like a viable long\-term option. We did also look at recent developments like [AlloyDB for PostgreSQL](https://cloud.google.com/blog/products/databases/alloydb-for-postgresql-columnar-engine) which looks interesting, but we didn’t want to be tied to GCP’s proprietary technology.


## Joins in ClickHouse [\#](/blog/hifis-migration-from-bigquery-to-clickhouse#joins-in-clickhouse)


ClickHouse is a unique technology and works differently than other databases. If you’re coming from a more traditional OLTP world, you need to be mindful of these differences for the best experience. This first challenge we came across was that joins require a little more understanding of how ClickHouse works to make them performant. Before going into details, first some background. We store music royalty data from artist royalty statements in a ClickHouse table called `normalized`. Each statement line is stored as a row in the table with the `timesStatement` column representing the date of the statement and `resourceFileName` representing the name of the statement file. Sometimes the dates for specific statements are incorrect and we want to fix them manually.


Since each statement contains thousands of rows (and in some cases hundreds of thousands), we want to simply update the `timesStatement` column with the correct date by joining with a separate table that contains just two columns `statementDate` (correct dates) and `resourceFileName` (the name of the file for which the date should be updated). In traditional relational databases, you would simply join two tables and update table1 with data from table2\. While this is possible in ClickHouse, we found we could achieve better performance using a JOIN engine table. Here’s how we updated the `timesStatement` column in the normalized table:


1. Imported data with the new statement dates into a new table `temp_statementDates`
2. Created the join engine table



```
CREATE TABLE statementDates_join as temp_statementDates Engine = Join(ANY, LEFT, resourceFileName);

```

3. Populated the join engine table



```
INSERT INTO statementDates_join 
SELECT *
from temp_statementDates;

```

4. Updated `normalized` using the join engine table



```
ALTER TABLE normalized
UPDATE timesStatement = joinGet('statementDates_join', 'statementDate', resourceFileName)
WHERE jobId = '055c45fb-6251-4050-b699-4223efae5a14'

```

5. Cleaned up temp tables



```
DROP TABLE statementDates_join
DROP TABLE temp_statementDates

```

By using a ClickHouse specific approach, we’re able to update records more efficiently.


## Joining ClickHouse and PostgreSQL Data [\#](/blog/hifis-migration-from-bigquery-to-clickhouse#joining-clickhouse-and-postgresql-data)


We still use PG for non\-royalty data such as customer account data and metadata. Fortunately, ClickHouse makes it relatively easy to [connect to](https://clickhouse.com/blog/migrating-data-between-clickhouse-postgres) PG databases. However, if you're trying to LEFT join from PG data to a big ClickHouse table, you may encounter a memory limit exception error if you don’t construct your query carefully. For example, we have a table in PG called `vendor_job` that contains a list of data vendor jobs that we run and its associated metadata. The `normalized` table in ClickHouse has a column called `jobId` that refers to the id of the `vendor_job` table in PG. To identify which `vendor_jobs` in PG don’t have an entry in the ClickHouse table, we could write the query as below:



```
SELECT COUNT(vj.id) AS no_of_vendor_jobs
FROM hifi.vendor_job AS vj
LEFT JOIN normalized AS n ON toUUID(vj.id) = n.jobId
WHERE n.jobId IS NULL
SETTINGS join_use_nulls = 1

```

But the query is slow and we can easily get a memory limit exceeded error. This is the result of the right side of the join being streamed into memory for the default join algorithm hash. In this case, the entire ClickHouse table. Without this understanding of ClickHouse internals, its easy to write a naive query such as this:


![HIFI_query.png](/uploads/HIFI_query_5ecef24eb5.png)
Without increasing the memory limit, one way to do the same sort of query more efficiently is as follows:



```
SELECT COUNT(vj.id) AS no_of_vendor_jobs
FROM hifi.vendor_job AS vj
LEFT JOIN
(
  SELECT
    jobId
  FROM normalized
  GROUP BY jobId
) AS n ON toUUID(vj.id) = n.jobId
WHERE n.jobId IS NULL
SETTINGS join_use_nulls = 1

```

This avoids using lots of memory, by limiting the right side to the list of job ids, and finishes in under 1 second!


![HIFI_vendor_jobs.png](/uploads/HIFI_vendor_jobs_1c427f689b.png)
Note that ClickHouse has recently released newer JOIN algorithms to help assist with memory intensive joins. For example, the recently added [Grace Hash join](https://clickhouse.com/blog/clickhouse-release-22-12) would potentially have allowed the original query to complete without exhausting memory. However, the optimized query still likely represents a more efficient solution.


## Library Issues [\#](/blog/hifis-migration-from-bigquery-to-clickhouse#library-issues)


Another challenge we faced was not with ClickHouse itself, but with the library support in various programming languages. At the time of our development, the recently released [official Node JS library](https://github.com/ClickHouse/clickhouse-js) was not available. As such, we used the popular [NodeJS client for ClickHouse](https://github.com/TimonKK/clickhouse) but quickly discovered it was inserting empty strings into the table even though the actual raw value passed to the library is NULL. The library also exposes a `query` method which inserts the NULLs as expected. So the bug is only with the `insert` method of the library.


Digging deeper into the source code of the library, the bug seems to be in the `insert` method of the library. Specifically, we managed to pinpoint the exact line in the source code of the library which replaces NULL values with empty strings:


![hifi_js.png](/uploads/hifi_js_0b41d65a1d.png)
By updating the code as below (which we plan to submit in a pull request back to the original library), we store NULLs in our normalized table as expected:



```
static mapRowAsObject(fieldList, row) {
    return fieldList
      .map(f => {
        return encodeValue(false, row[f] != null ? row[f] : null, 'TabSeparated'); 
      })
      .join('\t');

```

We have a few minor challenges remaining around ClickHouse support in some third party tools we use. For example, [Appsmith](https://www.appsmith.com/) has an outstanding [request](https://github.com/appsmithorg/appsmith/issues/12153) to add native ClickHouse support, but the workaround is to use the [ClickHouse HTTP interface](https://clickhouse.com/docs/en/interfaces/http/).


Beyond that, we need to consider what to do when we’re ready to deploy our own [ClickHouse cluster](https://clickhouse.com/docs/ru/getting-started/tutorial/#cluster-deployment). Running a cluster seems like more devops work than we would like to take on, so we’ve decided that as soon as support for GCP is added we’ll switch to the [ClickHouse Cloud](https://clickhouse.cloud/) managed version. The pricing structure has recently been simplified to only charge for compute and storage. That makes it a no\-brainer to switch from our hosted solution so that we no longer have to worry about scaling, backups, upgrades, etc.


## About HIFI [\#](/blog/hifis-migration-from-bigquery-to-clickhouse#about-hifi)


Backed by top VCs and chart\-topping creators across the globe, [HIFI](https://hi.fi) is a team of pioneering technologists and domain experts building the financial rights organization for the music industry.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

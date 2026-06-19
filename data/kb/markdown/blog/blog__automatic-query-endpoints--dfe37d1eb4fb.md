# Automatic Query Endpoints: Creating APIs from SQL Queries


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Automatic Query Endpoints: Creating APIs from SQL Queries

![](/_next/image?url=%2Fuploads%2FZach_Naimon_2f4cfc668e.jpeg&w=96&q=75)[Zach Naimon](/authors/zach-naimon)May 17, 2024 · 7 minutes read[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-header&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. To learn more about our volume\-based discounts, [contact us](/company/contact?loc=blog-cta-header) or visit our [pricing page](/pricing?loc=blog-cta-header).

Building interactive data\-driven applications requires not only a fast database, well\-structured data, and optimized queries. Your front\-end and microservices also need an easy way to consume the data returned by those queries, preferably via well\-structured APIs.


Today, we are happy to announce the new Automatic Query Endpoints feature, which makes this possible. With just a few clicks, you can create an API endpoint directly from any saved SQL query in the ClickHouse Cloud Console.



## Why did we build this? [\#](/blog/automatic-query-endpoints#why-did-we-build-this)


At ClickHouse, we believe that a truly ‘managed’ database\-as\-a\-service product shouldn’t just abstract away infrastructural complexity, it should also provide a best\-in\-class experience for developers and analysts who work with data every day. We recently overhauled the ClickHouse Cloud Console experience to support this, drastically shortening the distance between ClickHouse Cloud services and our control plane UI. This new UI should make ad\-hoc data imports, querying, and visualization relatively simple and painless for many analyst users.


However, whereas our SQL console UI has become an integral part of many analysts’ daily workstreams, it still lacks a few critical features to provide a truly great experience for developers, who are typically more concerned with programmatic ingestion and consumption of data. For developers, then, the Cloud Console UI primarily serves as a source of truth for their data (i.e. does the data exist in table(s), what volume of data is stored, are queries properly optimized, etc.) and a centralized place to create, modify, and monitor ingestion/consumption services.


![overview.png](/uploads/overview_62d00cd613.png)
In support of this developer\-focused use case, we launched ClickPipes—our ClickHouse Cloud\-native ingestion platform last year. ClickPipes initially supported Kafka stream ingestion, but we’ve since implemented support for Redpanda, WarpStream, Azure Event Hub, S3/GCS, Kinesis (most recently), and many other data sources in the near term. In other words, the development of developer\-focused tooling around data ingestion is already well underway, so the one remaining piece of functionality is a delightful developer experience around programmatic data consumption.


As we see things, query\-based API endpoints represent a simple and flexible framework for programmatic data consumption (and potentially ingestion as well) because they solve two key challenges:


### Challenge \#1: Wrangling language clients/drivers [\#](/blog/automatic-query-endpoints#challenge-1-wrangling-language-clientsdrivers)


ClickHouse maintains clients for most major programming languages, and most are relatively straightforward to set up. However, deeper functionality that may be immediately useful to developers (connection pooling, keep\-alive configuration, compression, streaming, parameterization, etc.) can take some time to figure out.


Alternatively, it is also fairly easy to hit ClickHouse’s HTTP interface using (for example) the fetch() API in Javascript, but this poses the same set of initial challenges as can be found in language clients—the complexity just moves from client configuration to HTTP header configuration.


A query\-based API endpoints solution can abstract away much of this complexity.


### Challenge \#2: Authentication and access control [\#](/blog/automatic-query-endpoints#challenge-2-authentication-and-access-control)


Even though ClickHouse supports several authentication methods for both Native and HTTP interfaces, in practice, basic auth is (alarmingly) still widely used. In our experience, many organizations opt for basic auth because it represents the path of least resistance when setting up most language clients/vanilla HTTP requests. While database\-level RBAC can mitigate some of the risks around basic auth, defining the correct user/role grants can often be challenging—especially for new users to ClickHouse


Our query\-based API endpoint solution sidesteps this challenge by leveraging our existing Cloud API key/secret authentication pattern. Since each API endpoint effectively represents a single query, access is narrowly scoped to that exact query.


## How it works [\#](/blog/automatic-query-endpoints#how-it-works)


To begin, we’ll need a Cloud API key. API keys can be created and managed from the `API keys` page in the organization\-level settings:


![00_api-keys.png](/uploads/00_api_keys_c545e11bfb.png)
Now that we’ve got our key, we can head to the SQL console and create a new query. For this demo, we’ll use the `youtube` dataset, which contains approximately 4\.5 billion records. As an example query, we’ll return the top 10 uploaders by average views per video in a user\-inputted year:



```
with sum(view_count) as view_sum,
    round(view_sum / num_uploads, 2) as per_upload
select
    uploader,
    count() as num_uploads,
    formatReadableQuantity(view_sum) as total_views,
    formatReadableQuantity(per_upload) as views_per_video
from
    youtube
where
    toYear(upload_date) = {year: UInt16}
group by uploader
order by per_upload desc
limit 10

```

Note that this query contains a parameter (year). The SQL console query editor automatically detects ClickHouse query parameter expressions and provides an input for each parameter. Let’s quickly run this query to make sure that it works:


![02_sql-console.png](/uploads/02_sql_console_7d45049f54.png)
Next step, we’ll go ahead and save the query:


![01_save-query-as.png](/uploads/01_save_query_as_88e398ab56.png)
Once the query is saved, we can create an API endpoint for it by clicking the ‘Share’ button and selecting ‘API Endpoint’. We’ll be prompted to specify which API key(s) should be able to access the endpoint:


![03_share_query.png](/uploads/03_share_query_f13e8e3e2f.png)
After selecting an API key, we’ll be good to go! An example `curl` command demonstrates how we can build requests to the endpoint:


![04_api_endpoint.png](/uploads/04_api_endpoint_b6a4230117.png)
Now, we can try to curl the endpoint:


![endpoints-curltest.png](/uploads/endpoints_curltest_11cc268ccb.png)
Now that we’ve verified that the endpoint works let’s go back to the SQL console. A new button should appear immediately to the right of the ‘share’ button. Clicking it will open a flyout containing monitoring data about the query:


![06_insights.png](/uploads/06_insights_30915a022a.png)
### How we built it [\#](/blog/automatic-query-endpoints#how-we-built-it)


To release an initial version of this feature as quickly as possible, we built upon existing functionality in our Cloud Console:


- Saved Queries
- Query parameterization
- Passwordless DB Authentication using certificates
- Server\-side query execution
- Existing Cloud API keys as the endpoint authentication method


In other words, the foundational elements necessary for building query API Endpoints have already been battle\-tested in production for months to years. Implementation primarily required stringing these components together in a new way and extending our SQL console saved queries UI to give users an easy and seamless way to configure and monitor their endpoints.


### What we’re building next [\#](/blog/automatic-query-endpoints#what-were-building-next)


While OpenAPI keys are functional, they are still in Beta—primarily because the current functionality does not provide an optimal solution for direct endpoint calls from a user interface within a webpage. To enhance this user experience, we plan to introduce authentication/authorization via JWT (your own JWT). This will allow these API endpoints to be the building blocks for any developer to construct an analytics application backend.


A frontend developer would only require two key skills to build their next analytics application: the ability to create a query in ClickHouse (with assistance from our copilot/Gen AI if needed) and proficiency in their preferred web framework.


We also plan to add support for a streaming API, letting you pull all your data via API endpoints without memory constraints.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

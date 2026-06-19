# March 2024 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# March 2024 Newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 20, 2024 · 4 minutes readWelcome to the March ClickHouse newsletter where we round up what’s been happening in real\-time data warehouses in the last month.


This month, we have the 24\.2 release with useful features for data ingestion, Rill dashboards for ClickHouse, and 10x faster materialized views using aggregation states.


## Inside this issue [\#](/blog/newsletter-march-2024#inside-this-issue)


- [Featured community member](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#featured-community-member)
- [24\.2 release](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#242-release)
- [Rill dashboards for ClickHouse](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#rill-dashboards-for-clickhouse)
- [The One Trillion Row Challenge](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#the-one-trillion-row-challenge)
- [10x Faster Materialized Views with Aggregation States](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#10x-faster-materialized-views-with-aggregation-states)
- [chDB joins the ClickHouse family](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#chdb-joins-the-clickhouse-family)
- [Post of the month](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#post-of-the-month)
- [Upcoming events](/blog/newsletter-march-2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter#upcoming-events)


## Featured community member [\#](/blog/newsletter-march-2024#featured-community-member)


This month's featured community member is Steve Flitcroft, VP of R\&D at iVendi.


![202403-community-member.png](/uploads/202403_community_member_9cabc4e707.png)
Steve is perhaps better known as redsquare on the [ClickHouse Community Slack](/slack), where he has helped a lot of users solve problems that they’ve encountered when using ClickHouse.


Whether it’s questions about refreshable materialized views, how to speed up a query, or understanding ClickHouse’s table engines, Steve has got you covered!


[Follow Steve on LinkedIn](https://www.linkedin.com/in/steveflitcroft/)


 


## 24\.2 release [\#](/blog/newsletter-march-2024#242-release)


![24.2.2.png](/uploads/24_2_2_b7ee0b202f.png)
The 24\.2 release added some useful features for data ingestion. Adaptive asynchronous inserts make data batching smarter \& more efficient. Plus, ClickHouse is now smarter at detecting file formats even if the file extension is missing or wrong. We’ve also vectorized distance functions, speeding up vector search in RAG applications.


[Read the release post](/blog/clickhouse-release-24-02?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter)


 


## Rill dashboards for ClickHouse [\#](/blog/newsletter-march-2024#rill-dashboards-for-clickhouse)


![clickhouse-rill.png](/uploads/clickhouse_rill_7699d6f965.png)
Rill is a Business Intelligence tool that lets you build fast operational dashboards with sub\-second performance. Having bumped into Alexey, ClickHouse’s Co\-founder and CTO, at FOSDEM, this month they added a ClickHouse connector. In a blog post, Nishant Bangarwa explains how the connector works and gives step\-by\-step instructions to get your first Rill/ClickHouse dashboard up and running.


[Read the blog post](https://www.rilldata.com/blog/operational-bi-embedded-dashboards-for-clickhouse?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter)


 


## The One Trillion Row Challenge [\#](/blog/newsletter-march-2024#the-one-trillion-row-challenge)


![1trillion_row_challenge.png](/uploads/1trillion_row_challenge_37514baf99.png)
At the start of February, Dask launched the [1 trillion row challenge](https://medium.com/coiled-hq/one-trillion-row-challenge-5bfd4c3b8aef?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter), which requires entrants to query 1 trillion rows of data stored across 100,000 Parquet files in S3\. Dale McDiarmid, our resident challenge expert, set to work and got the query running in under 3 minutes for $0\.56 in AWS spot instances. In the blog post, Dale explains how he optimized query performance, including bottleneck detection and working out the best size of AWS machine to use. 


[Read the blog post](/blog/clickhouse-1-trillion-row-challenge?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter)


 


## 10x Faster Materialized Views with Aggregation States [\#](/blog/newsletter-march-2024#10x-faster-materialized-views-with-aggregation-states)


![query.png](/uploads/query_b6bfa62d41.png)
Sayed Alesawy has written a blog post in which he takes us through various techniques to improve the performance of queries on observability data. An initial query on 26 million rows takes 693 seconds to run, which is reduced to 11 seconds with a materialized view. But sub\-second response time is needed and this is achieved by storing [aggregation states](/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states#working-with-aggregation-states?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter) instead of scalar values. 


[Read the blog post](https://sayedalesawy.hashnode.dev/how-to-use-clickhouse-aggregation-states-to-boost-materialized-views-performance-by-more-than-10-times?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter)


 


## chDB joins the ClickHouse family [\#](/blog/newsletter-march-2024#chdb-joins-the-clickhouse-family)


![Option 6.png](/uploads/Option_6_cff43ad3dc.png)
The biggest news of the month is that chDB, an embedded SQL OLAP engine powered by ClickHouse, is now part of ClickHouse. chDB’s creator and main contributor, Auxten, is joining forces with us to focus on evolving chDB and integrating it even more closely with the ClickHouse ecosystem. We’d love to know what you’d like us to work on next, which you can do via the [chDB GitHub discussion board](https://github.com/orgs/chdb-io/discussions?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter).


[Read the announcement](/blog/chdb-joins-clickhouse-family?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter)


 


## Post of the month [\#](/blog/newsletter-march-2024#post-of-the-month)


![tweet-1765785275014557831 (2).png](/uploads/tweet_1765785275014557831_2_0f58e6ad0e.png)
My favorite tweet this month was by [Michael E. Driscoll](https://twitter.com/medriscoll) (Founder of Rill Data) about chDB joining ClickHouse. [See it here](https://twitter.com/medriscoll/status/1765785275014557831)


 


## Upcoming events [\#](/blog/newsletter-march-2024#upcoming-events)


- [v24\.3 ClickHouse Community Call](https://clickhouse.com/company/events/v24-3-community-release-call?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter) \- March 26th
- [FREE ClickHouse Training](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter) \- March 27th \& 28th
- [Bangalore Meetup](https://www.meetup.com/clickhouse-bangalore-user-group/events/299479850/) \- March 23rd
- [AWS Summit Paris](https://clickhouse.com/company/events/2024-03-aws-summit-paris?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter) \- April 3rd
- [AWS Summit Amsterdam](https://clickhouse.com/company/events/2024-04-aws-summit-amsterdam?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter) \- April 9th
- [Zurich Meetup](https://www.meetup.com/clickhouse-switzerland-meetup-group/events/299628922/) \- April 16th
- [Copenhagen Meetup](https://www.meetup.com/clickhouse-denmark-meetup-group/events/299629133/) \- April 23rd
- [v24\.4 ClickHouse Community Call](https://clickhouse.com/company/events/v24-4-community-release-call?utm_source=clickhouse&utm_medium=web&utm_campaign=202403-newsletter) \- April 30th
- [Stockholm Meetup](https://www.meetup.com/clickhouse-stockholm-user-group/events/299752651/) \- May 22nd
- [Dubai Meetup](https://www.meetup.com/clickhouse-dubai-meetup-group/events/299629189/) \- May 28th
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

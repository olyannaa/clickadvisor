# August 2024 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# August 2024 newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 22, 2024 · 5 minutes readWelcome to the August ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.


This month, we have exciting news about PeerDB joining ClickHouse, downsampling time series data, join performance improvements in the 24\.7 release, and more!


 


## Alexey, ClickHouse creator and CTO, goes on tour! [\#](/blog/202408-newsletter#alexey-clickhouse-creator-and-cto-goes-on-tour)


![Banner Alexey the rockstar.png](/uploads/Banner_Alexey_the_rockstar_ea3688418f.png)
We are excited to share that **Alexey Milovidov, creator and CTO of ClickHouse**, will be delivering a series of technical talks around the world. Please join these events in person to hear him speak and a chance to ask him ANY question about ClickHouse! Space is limited, register below:


- Sun, Aug 25 \- China Meetup, Guangzhou \- [Register](https://mp.weixin.qq.com/s/GSvo-7xUoVzCsuUvlLTpCw)
- Tues, Aug 27 \- VLDB Talk, Guangzhou \- [Schedule](https://vldb.org/2024/?program-schedule)
- Thur, Sept 5 \- San Francisco Meetup (Cloudflare) \- [Register](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/302540575)
- Mon, Sept 9 \- Raleigh Meetup (Deutsche Bank) \- [Register](https://www.meetup.com/clickhouse-nc-meetup-group/events/302557230)
- Tues, Sept 10 \- New York Meetup (Rokt) \- [Register](https://www.meetup.com/clickhouse-new-york-user-group/events/302575342)
- Thur, Sept 12 \- Chicago Fireside Chat (Jump Capital) \- [Register](https://lu.ma/43tvmrfw)
- Wed, Sept 18 \- Warsaw AWS Cloud Day \- [Register](https://aws.amazon.com/events/cloud-days/warsaw/)


 


## Inside this issue [\#](/blog/202408-newsletter#inside-this-issue)


- [Featured community member: Chase Richards](https://clickhouse.com/blog/202408-newsletter#featured-community-member-chase-richards)
- [Upcoming events](https://clickhouse.com/blog/202408-newsletter#upcoming-events)
- [ClickHouse welcomes PeerDB](https://clickhouse.com/blog/202408-newsletter#clickhouse-welcomes-peerdb)
- [Downsampling time series data](https://clickhouse.com/blog/202408-newsletter#downsampling-time-series-data)
- [24\.7 release](https://clickhouse.com/blog/202408-newsletter#247-release)
- [How Maxilect transferred ClickHouse between geographically distant data centers](https://clickhouse.com/blog/202408-newsletter#how-maxilect-transferred-clickhouse-between-geographically-distant-data-centers)
- [Java Client… the SEQUEL?!](https://clickhouse.com/blog/202408-newsletter#java-client-the-sequel)
- [Quick reads](https://clickhouse.com/blog/202408-newsletter#quick-reads)
- [Post of the month](https://clickhouse.com/blog/202408-newsletter#post-of-the-month)


 


## Featured community member: Chase Richards [\#](/blog/202408-newsletter#featured-community-member-chase-richards)


This month's featured community member is Chase Richards, VP of Engineering at Corsearch.


![202408-featured.png](/uploads/202408_featured_697afc61da.png)
Chase Richards previously led engineering efforts at Marketly from a 2011 start\-up through its acquisition in 2020 by Corsearch.


Chase recently [presented at the Bellevue meetup](/videos/how-corsearch-uses-clickhouse-today) about his experience replacing MySQL with ClickHouse as the backing database for a client\-facing report interface for their search engine protection service. Having done this in 2018, Chase earned his status as a trailblazer in the community.


More recently, Chase and his team have [added vector\-based analytics](/blog/corsearch-replaces-mysql-with-clickhouse-for-content-and-brand-protection) to their fraud detection model. They’re also using ClickHouse to monitor their search engine scraping setup.


[Follow Chase on LinkedIn](https://www.linkedin.com/in/chasesrichards/)


 


## Upcoming events [\#](/blog/202408-newsletter#upcoming-events)


- [ClickHouse Guangzhou Meetup](https://mp.weixin.qq.com/s/GSvo-7xUoVzCsuUvlLTpCw) \- Aug 25
- [ClickHouse \+ Melbourne Data Engineering Meetup](https://www.meetup.com/clickhouse-australia-user-group/events/302732666) \- Aug 27
- [ClickHouse Meetup in Bellevue](https://www.meetup.com/clickhouse-seattle-user-group/events/302518075) \- Aug 27
- [ClickHouse Developer Training](/company/events/202409-clickhouse-developer?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 3
- [ClickHouse Meetup in Zurich](https://www.meetup.com/clickhouse-switzerland-meetup-group/events/302267429) \- Sep 5
- [ClickHouse \+ Sydney Data Engineering Meetup](https://www.meetup.com/clickhouse-australia-user-group/events/302862966/) \- Sep 5
- [ClickHouse Meetup @ Cloudflare \- San Francisco](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/302540575/) \- Sep 5
- [Kubernetes Community Days \- Sydney](/company/events/202409-kcd-sydney?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 5\-6
- [ClickHouse Meetup in Raleigh](https://www.meetup.com/clickhouse-nc-meetup-group/events/302557230/) \- Sep 9
- [ClickHouse Meetup @ Shopify \- Toronto](https://www.meetup.com/clickhouse-toronto-user-group/events/301490855/) \- Sep 10
- [ClickHouse Admin Workshop](/company/events/202409-apj-clickhouse-admin-workshop?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 10
- [AWS Summit Toronto](/company/events/202409-amer-awssummit-toronto) \- Sep 10
- [ClickHouse Meetup @ Rokt \- NYC](https://www.meetup.com/clickhouse-new-york-user-group/events/302575342/) \- Sep 10
- [Coffee with ClickHouse \- Amsterdam](/company/events/202409-emea-coffee-with-clickhouse?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 11
- [ClickHouse Fundamentals](/company/events/clickhouse-fundamentals?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 11
- [ClickHouse Meetup @ Jump Capital](https://lu.ma/43tvmrfw) \- Sep 12
- [ClickHouse Meetup \- Austin](https://www.meetup.com/clickhouse-austin-user-group/events/302558689/) \- Sep 17
- [ClickHouse Meetup in London](https://www.meetup.com/clickhouse-london-user-group/events/302977267) \- Sep 17
- [AWS Cloud Day \- Warsaw](/company/events/202409-emea-awscloudday-warsaw?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 18
- [In\-person ClickHouse Fundamentals training \- Amsterdam](/company/events/202409-emea-inperson-clickhouse-fundamentals?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 18\-19
- [Big Data LDN (London)](/company/events/202409-emea-bigdataldn?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 18\-19
- [ClickHouse Cloud Live Update](/company/events/202409-cloud-update-live?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 24
- [DataEngBytes \- Sydney](/company/events/202409-dataengbytes-sydney?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 24
- [DataEngBytes \- Perth](/company/events/202409-dataengbytes-perth?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Sep 27
- [DataEngBytes \- Melbourne](/company/events/202410-dataengbytes-melbourne?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Oct 1
- [DataEngBytes \- Auckland](/company/events/202410-dataengbytes-auckland?utm_campaign=202408-newsletter&utm_source=clickhouse&utm_medium=web) \- Oct 4


 


## ClickHouse welcomes PeerDB [\#](/blog/202408-newsletter#clickhouse-welcomes-peerdb)


![peerdb-nl.png](/uploads/peerdb_nl_55c48390c4.png)
A couple of weeks ago, we were thrilled to announce today that ClickHouse joined forces with PeerDB, a Change Data Capture (CDC) provider focused on Postgres.


Now, users have an easy button to sync their data from the number one transactional database to the number one analytical database.


[Read the announcement](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database)


 


## Downsampling time series data [\#](/blog/202408-newsletter#downsampling-time-series-data)


![timeseries.png](/uploads/timeseries_561276ed91.png)
Phare is a platform for website monitoring, incident management, status pages, analytics, security, and alerting. They wanted to create a chart showing 90 days of monitoring data. As they collect one data point per minute, this meant that the chart needed to render 130,000 data points, which was both slow to do and difficult to interpret.


Enter the [largestTriangleThreeBuckets](/docs/en/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets) function, added to ClickHouse at the end of 2023\. Using this function, they could remove redundant data points, making the chart quicker to create and easier to interpret.


[Read the blog post](https://docs.phare.io/articles/downsampling-time-series-data)


 


## 24\.7 release [\#](/blog/202408-newsletter#247-release)


![356555235-1fd960de-35b0-4e39-b0d2-283cd1a49bd2.png](/uploads/356555235_1fd960de_35b0_4e39_b0d2_283cd1a49bd2_b865c512ae.png)
The 24\.7 release includes many performance improvements. These include a full sorting merge algorithm for ASOF joins, a faster parallel hash join algorithm, and improvements to the “read in order” algorithm when running queries with a high\-selectivity filter.


We also have deduplication In Materialized Views, automatic named tuples, and the percent\_rank window function.


[Read the release post](/blog/clickhouse-release-24-07)


 


## How Maxilect transferred ClickHouse between geographically distant data centers [\#](/blog/202408-newsletter#how-maxilect-transferred-clickhouse-between-geographically-distant-data-centers)


![maxilect.png](/uploads/maxilect_6e6a847ec9.png)
Maxilect, an IT solutions provider for the Adtech and Fintech industries, has written an experience report on moving a ClickHouse cluster from a data center in Miami to another in Detroit.


In this blog post, Igor Ivanov and Denis Palaguta explain how they did this using the clickhouse\-copier tool while keeping the service up and serving user requests.


[Read the blog post](https://maxilect-company.medium.com/how-we-transferred-the-clickhouse-database-between-geographically-distant-data-centers-ad3c853dce3f)


 


## Java Client… the SEQUEL?! [\#](/blog/202408-newsletter#java-client-the-sequel)


![javasequel.png](/uploads/javasequel_2ba3c969de.png)
We recently started work on revamping the ClickHouse Java client. The new version has a more intuitive, self\-documenting API, and we’ve added more usage examples to the documentation.


It’s still in alpha, but we’d love for you to try it and send us your thoughts.


[Read the blog post](/blog/java-client-sequel)


 


## Quick reads [\#](/blog/202408-newsletter#quick-reads)


- Vladimir Ivoninskii shares his [best techniques for effectively running a production ClickHouse cluster](https://dzone.com/articles/7-essential-tips-for-a-production-clickhouse).
- Denys Golotiuk shows how to [do image similarity search](https://datachild.net/machinelearning/image-similarity-search-with-embeddings-based-on-sentence-transformers) using vector embeddings in ClickHouse with the L2Distance function.
- Joe Zhou explores [integrating ClickHouse with Dragonfly](https://www.dragonflydb.io/blog/using-dragonfly-as-a-table-engine-for-clickhouse?hss_channel=tw-1535352010421063680), an ultra\-high\-throughput, Redis\-compatible in\-memory data store.


 


## Post of the month [\#](/blog/202408-newsletter#post-of-the-month)


Our [favorite post this month](https://www.linkedin.com/posts/y-combinator_congrats-to-the-team-at-peerdb-yc-s23-on-activity-7224096453613301763-M0b5/) was by Y Combinator about PeerDB joining ClickHouse.


![ln-post202408.png](/uploads/ln_post202408_c07e584d11.png)
 

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

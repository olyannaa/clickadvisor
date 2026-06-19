# NYC Meetup Report: Large Scale Financial Market Analytics with ClickHouse (Bloomberg)


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# NYC Meetup Report: Large Scale Financial Market Analytics with ClickHouse (Bloomberg)

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Dec 6, 2022 · 5 minutes read
  

On December 6, 2022, Baudouin Giard, Engineering Team Lead on the Structured Products team at Bloomberg, presented his team's use case for ClickHouse at the NYC meetup. 
The financial sector requires advanced data management and analysis capabilities to provide accurate and timely information to institutional investors. Bloomberg, as a leading data provider for financial markets, faces unique challenges when it comes to optimizing data ingestion and query performance. ClickHouse's columnar storage, ease of use, and ability to write complex calculations with simple mathematics make it an excellent choice for Bloomberg’s use case.


Bloomberg's products include the Bloomberg Terminal and some enterprise APIs that provide the best data continuously to institutional investors. The company's challenge is to optimize for a relatively small number of people querying about a hundred million securities all at once.


"What I have to optimize for is not a hundred million people connecting to Bloomberg all at once. What I have to optimize for is one single person querying data, about a hundred million securities all at once. And what if then a thousand people do the same thing?” said Giard. “People want to get a big view over the entirety of the market, and they want to compare what they're doing to the average of the market.”


Giard's team has been using ClickHouse for two years, and the specific application on the Bloomberg Terminal leveraging ClickHouse is one of their most worked\-on projects. The data set is relatively small, with only 5 billion rows and 100 columns, and the usage pattern is pretty basic. Users filter and group columns, and the columns are selected to perform interactive queries that require them to iterate on their queries and perform somewhat complex calculations.


![Bloomberg  highlights.png](/uploads/Bloomberg_highlights_20550cb2f5.png)
Giard explained that ClickHouse is an excellent choice for their use case because of its columnar storage, which allows users to query only the necessary columns and not use excessive memory.


“The columnar storage is a very big asset when you have a data set like this one with a hundred columns. You quickly find out that people are only interested in probably 10 of them, but every now and then there is a person who wants to query the hundredth one. So you want to have it available, but you don't want to have a full memory data store that's going to use a ton of memory for all these columns that people use once in a blue moon,” said Giard.


Additionally, ClickHouse is easy to use and allows users to write complex calculations with simple mathematics.


![Bloomberg strengths.png](/uploads/Bloomberg_strengths_8b34ba7132.png)
The team's approach to optimizing data ingestion, rather than the speed of data queries, has helped them ingest four terabytes of data in under an hour. Giard created a new ClickHouse table every time they needed to make changes to the data, such as when adding a new column. The use of a buffer table helped to ensure that all the data was in memory, making the process extremely flexible.


Data quality is crucial, and Giard emphasized the importance of updating the data quickly to ensure that clients get accurate data. The use of buffer tables and creating a new table for every change made the process flexible, allowing for quick data updates and accurate data for clients.


“It's very important to me because when you are in the data business, and especially financial data, your edge, what makes you good, is the quality of your data,” said Giard.


Giard also discussed how ClickHouse works with immutable files through the merge tree table, which allows users to clone a table instantly when appending new data to it. However, every query that the client performs puts stress on ZooKeeper, which could cause the entire application to go down if ZooKeeper goes down. Therefore, the team has been testing disaster recovery simulations to ensure that the process works.


Bloomberg currently uses ClickHouse on\-premises on the default setup of the machine provided by the company, and they use local storage for data serving to clients. However, Giard would like to experiment with deploying ClickHouse on Kubernetes clusters, using their internal S3 backend as storage, and trying ClickHouse Keeper.


Baudouin Giard's presentation on Bloomberg's unique use case for ClickHouse provides valuable insights for other companies in the financial sector. Giard's team's approach to optimizing data ingestion, rather than the speed of data queries, has helped them efficiently ingest vast amounts of data while ensuring data quality. ClickHouse's columnar storage, ease of use, and ability to write complex calculations with simple mathematics make it an excellent choice for this use case.


## More Details [\#](/blog/nyc-meetup-report-large-scale-financial-market-analytics-with-clickhouse#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-new-york-user-group/events/289403909/) in NYC on December 6, 2022
- The presentation materials are available on [GitHub](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup67/ClickHouse%20for%20Financial%20Analytics%20-%20Bloomberg.pdf)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

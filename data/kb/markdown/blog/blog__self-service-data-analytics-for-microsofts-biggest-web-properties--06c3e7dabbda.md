# Seattle Meetup Report: Self\-Service Data Analytics for Microsoft’s Biggest Web Properties with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Seattle Meetup Report: Self\-Service Data Analytics for Microsoft’s Biggest Web Properties with ClickHouse

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Jan 18, 2023 · 6 minutes read
  

On January 18th, 2023 Microsoft hosted a ClickHouse community meetup where the WebXT team presented two of their analytics products using ClickHouse: Titan and Microsoft Clarity. The team shared how they are able to analyze petabytes of data in seconds and create custom dashboards with just a few clicks.


Satish Manivannan, Senior Director of Data and Analytics, introduced the products and discussed the vision of Titan, which aims to provide self\-service analytics to thousands of employees across Microsoft.


## Titan: Self\-Service Analytics Tool for Microsoft [\#](/blog/self-service-data-analytics-for-microsofts-biggest-web-properties#titan-self-service-analytics-tool-for-microsoft)


WebXT is home to some of the biggest web properties for Microsoft, including Edge Browser, Bing search, MSN, Microsoft Advertising, Maps and more. These web properties generate petabytes of data, and analytics is crucial for its success.


The WebXT team developed Titan, an internal data analytics tool which enables self\-serve interactive data analysis in an efficient and flexible manner. Titan has been in development for two and a half years and is used by over 2,500 people on a monthly basis, receiving over 100,000 queries daily.


The team chose ClickHouse to power their analytics solution, combined with Apache Superset as the data visualization tool. Both ClickHouse and Superset are open source technologies and Manivannan explained how they see this is a competitive advantage. “We not only contribute to Microsoft technology, we are very much embracing the open source community, so that we can best compete with our fierce competitors. Of course that's where I think we struck gold with ClickHouse among other solutions”, said Manivannan.


Historically the team had been using a combination of in\-house and third party analytics tools. Switching to ClickHouse saves the team millions of dollars in license fees. “We had Adobe Analytics, and we also had Interana, which is called Scuba.” Manivannan explained that the tools worked well however their demands continued to increase. “We needed something we could build in\-house, so that we could innovate faster and keep up with the innovation that the team is doing.”


![image 1.png](/uploads/image_1_968291e4d8.png)
*Titan provides interactive analytics to thousands of Microsoft employees, replacing 3rd party tools such as Adobe Analytics, saving millions of dollars.*
## High\-Level Requirements for Titan [\#](/blog/self-service-data-analytics-for-microsofts-biggest-web-properties#high-level-requirements-for-titan)


The key goal for Titan was to provide self\-service analytics with response times within seconds. This would allow people to interactively slice and dice data and save it as dashboards. The tool needed to also allow for the customization of metrics, filters, and columns. Advanced analytics such as user analytics, cohort analysis, A/B testing and flexible data retention were also important requirements. Manivannan discussed the challenges of freeform analysis of queries and emphasized the need for scalable, performant, and highly available infrastructure.


![Microsoft Titan image 2.png](/uploads/image_2_f073986f73.png)
*ClickHouse was chosen for Titan as it met all of the high level requirements.*
Manivannan explained that ClickHouse was an excellent choice for many of these requirements because of its speed and cost\-effectiveness. “ClickHouse fits a lot of these boxes. Definitely it is fast. We also did some custom optimization. So our main tagline is, faster and cheaper … ClickHouse plays a big part and meets a lot of our diverse set of data needs.”


He also highlighted the inbuilt telemetry in ClickHouse, which makes monitoring data usage and storage more accessible.


![Microsoft Titan image 3.png](/uploads/image_3_bb933869cc.png)
*Titan platform includes thousands of dashboards for tracking KPIs, custom issue builds, user analytics features, and A/B testing capabilities.*
## ClickHouse as the Data Engine for Titan [\#](/blog/self-service-data-analytics-for-microsofts-biggest-web-properties#clickhouse-as-the-data-engine-for-titan)


Lin Tang, Principal Software Engineering Manager on the WebXT Team presented the high\-level overview of the Titan architecture, which consists of a data source engine, API, and interactive visualization powered by Superset. The data source engine has three main inputs: Cosmos, Azure, and real\-time streaming scenarios.


Bing, which has a lot of diverse and expensive queries, has clusters with hundreds of machines set up to support query requirements. ClickHouse is used as the data engine, and they have multiple clusters set up, with ZooKeeper used for ClickHouse cluster management.


![Microsoft Titan image 4.png](/uploads/Microsoft_Titan_image_4_8e9ae8f7a0.png)
*Titan architecture which consists of a data source engine, API, and interactive visualization powered by Superset.*
The API was built to provide authentication and to avoid flooding the backend database with requests. They also query Microsoft internal APIs to get information on experimentation scenarios. To avoid sending every query to the backend database, caching has been implemented, pre\-caching data during low load times and showing data right away on custom dashboards.


Tang then discussed how they customized Superset with query builders and visualizations, including a sampling feature that allowed users to switch easily between sampled and raw data.


## Optimization Techniques for ClickHouse [\#](/blog/self-service-data-analytics-for-microsofts-biggest-web-properties#optimization-techniques-for-clickhouse)


The talk also covered optimization around ClickHouse, including a near real\-time pipeline to collect signals from their production service and a query optimizer built\-in to improve query performance. The Joiner Optimizer was implemented to address the challenge of big data joins, resulting in a 10x query improvement. The condition optimizer pre\-selected the condition by doing a "where" first, reducing the data size and improving processing time. The time zone optimizer selected the data range first and then applied the timestamp, leading to a good improvement in query performance.


![Microsoft Titan image 5.png](/uploads/Microsoft_Titan_image_5_14cd6743c6.png)
*Near real\-time data pipeline for Titan using ClickHouse.*
Storage efficiency was also discussed, with the need to optimize storage to improve performance. Tang explained that Titan uses role\-based return and deletion to keep track of the data that needs to be deleted, ensuring efficient deletion without impacting system performance. ClickHouse's rich encoding options were also discussed, with ZSTD found to provide a 50% savings for some tables despite slower query performance.


The ClickHouse community meetup at Microsoft provided insights into the successful implementation of Titan and Microsoft Clarity, both based on ClickHouse. The event highlighted the importance of data in the success of Microsoft and demonstrated how self\-serve analytics provides value to the organization.


## More Details [\#](/blog/self-service-data-analytics-for-microsofts-biggest-web-properties#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-seattle-user-group/events/290310025/) at the Microsoft office in Redmond on January 18, 2023
- Learn more about how ClickHouse is used within Microsoft Clarity, the free behavior analytics product for website owners in our [meetup report](https://www.clickhouse.com/blog/petabyte-scale-website-behavior-analytics-using-clickhouse).
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

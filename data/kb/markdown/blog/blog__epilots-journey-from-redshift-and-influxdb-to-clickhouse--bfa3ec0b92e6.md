# epilot's Journey: from Redshift and InfluxDB to ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# epilot's Journey: from Redshift and InfluxDB to ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Sep 24, 2024 · 5 minutes read![epilot_quote.png](/uploads/epilot_quote_2e698d1ddd.png)
## Background [\#](/blog/epilots-journey-from-redshift-and-influxdb-to-clickhouse#background)


[epilot](https://www.epilot.cloud/en) is a SaaS platform specializing in the energy sector, offering comprehensive solutions to help utilities and grid operators set up and manage their businesses online. It is the 360° platform for the energy transition. epilot allows its users to digitalize their sales, service \& grid processes from initial customer inquiries to ongoing support for more efficient processes, flexible market launches and happier customers.


## Challenge [\#](/blog/epilots-journey-from-redshift-and-influxdb-to-clickhouse#challenge)


As epilot scaled, it faced challenges with its existing data infrastructure. The company initially used AWS Redshift and S3 for data storage and processing. However, these tools presented limitations in performance and real\-time analytics, crucial for epilot’s needs in providing a seamless and responsive platform for its clients.


One of the significant pain points was the lack of a centralized data platform, which made it difficult for different teams within epilot to access and analyze data cohesively. Easy data access to allow all teams to build products on top of the data was a key goal. Additionally, the costs associated with Redshift were becoming a concern, especially as the company anticipated increasing data volumes with the expansion of new features and use cases.


## Solution [\#](/blog/epilots-journey-from-redshift-and-influxdb-to-clickhouse#solution)


To address these challenges, epilot explored alternative database solutions, eventually choosing ClickHouse as their central data storage layer. Suresh Sivasankaran, Principal Engineer at epilot, was familiar with ClickHouse from previous projects and recognized its potential to meet their needs. ClickHouse Cloud on AWS was particularly appealing due to epilot’s preference for a serverless infrastructure aligning with their existing tech stack.


The switch to ClickHouse offered several advantages:


1. **Performance and Scalability**: ClickHouse’s ability to handle large volumes of data with low latency was a game\-changer. It allowed epilot to provide real\-time analytics and insights, essential for their clients in the energy sector who need up\-to\-date information to make informed decisions.
2. **Cost Efficiency**: Compared to other solutions like Redshift and Rockset, ClickHouse offered a more cost\-effective option. This was particularly important for epilot, which aimed to balance performance needs with budget considerations.
3. **Flexibility and Integration**: ClickHouse’s support for complex queries and integration capabilities with BI tools enabled epilot to create a more unified data environment. This integration was crucial for generating dashboards and reports that could be easily accessed and used by various teams within the company.


## Implementation and Impact [\#](/blog/epilots-journey-from-redshift-and-influxdb-to-clickhouse#implementation-and-impact)


The implementation of ClickHouse at epilot began with a proof of concept, which proved successful, leading to a broader rollout. Initially, the focus was on internal dashboards and metrics, but the use of ClickHouse quickly expanded to other areas, including a data lake feature that allows customers to connect their BI tools and build custom reports.


One of the immediate benefits was the improvement in query performance and the ability to handle real\-time analytics. This improvement was particularly evident in new features like an end\-customer facing portal, which generated substantial data points. With ClickHouse, epilot could manage and analyze these data sets efficiently, enabling better service delivery and customer insights.


Suresh said:



> "With the integration of ClickHouse, our dashboards now provide real\-time metrics instead of relying on cached data and on\-demand updates. Additionally, the data load speed for our data lake offering, used by our customers, has significantly improved, reducing the time to transfer data from ClickHouse to BI tools from over 30 minutes to under 3 minutes."


Moreover, ClickHouse’s capabilities allowed epilot to consolidate data from different sources, providing a central data foundation for the entire platform. This consolidation made it easier for teams to collaborate and innovate, leveraging data to enhance product offerings and optimize internal processes and effectively build products faster on top of the data foundation.


![360 Data platform - clickhouse.png](/uploads/360_Data_platform_clickhouse_033c806945.png)
## Future Directions [\#](/blog/epilots-journey-from-redshift-and-influxdb-to-clickhouse#future-directions)


Looking ahead, epilot plans to expand its use of ClickHouse further. As they onboard more customers and develop new features, the company expects data volumes to grow significantly. ClickHouse’s scalability and performance will be critical in supporting this growth, enabling epilot to continue delivering high\-quality, data\-driven services.


One exciting area of development is using ClickHouse in conjunction with AWS Bedrock for AI and machine learning applications. This integration will allow epilot to refine its models based on data stored in ClickHouse, enhancing features like automated summaries and customer engagement tools.


This transition away from a [purpose\-built time\-series database](https://clickhouse.com/resources/engineering/what-is-time-series-database) like InfluxDB reflects a key insight for modern data architectures. Suresh added:



> “We've transitioned from Redshift and InfluxDB to ClickHouse in our engineering stack to achieve greater scalability and performance. Moving forward, we plan to leverage ClickHouse as the core of our data infrastructure across a wider range of use cases, particularly as we advance toward building Vertical AI solutions for the energy market.”


## Conclusion [\#](/blog/epilots-journey-from-redshift-and-influxdb-to-clickhouse#conclusion)


epilot’s journey with ClickHouse illustrates the transformative impact of choosing the right data infrastructure. By adopting ClickHouse, epilot not only improved performance and reduced costs but also laid a solid foundation for future growth and innovation. The partnership between epilot and ClickHouse demonstrates how advanced data technologies can empower companies to meet complex industry demands, drive efficiency, and unlock new business opportunities.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

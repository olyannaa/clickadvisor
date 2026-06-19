# Ongage's Strategic Shift to ClickHouse for Real\-time Email Marketing


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Ongage's Strategic Shift to ClickHouse for Real\-time Email Marketing

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Aug 24, 2023 · 10 minutes readReal\-time insights can make or break a digital marketing campaign. As an automation marketing company based in Israel, [Ongage](https://www.ongage.com/) recognized this need. Revolutionizing the email marketing industry, they manage data for customers with hundreds of millions of contacts, executing campaigns on a huge scale across channels such as email and SMS.


However, Ongage faced a challenge. The data warehouse they used couldn't offer the real\-time capabilities they were seeking. Processing around half a billion messages per day – from customer email feedback to user behavior metrics – required a robust solution. This blog post provides an in\-depth look at how Ongage navigated this challenge and enhanced their analytical capabilities and operational efficiency by transitioning to ClickHouse.


## The Evolution of Ongage's Database Technology: From Limitations to Real\-Time Analytics [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#the-evolution-of-ongages-database-technology-from-limitations-to-real-time-analytics)


In the early stages of Ongage's technology journey, the team found themselves working with a blend of MongoDB, MySQL, and Redshift. Each database served its unique purpose, but the absence of real\-time capabilities soon became a clear bottleneck. According to Roman Raslin, VP of R\&D at Ongage, “Our existing data warehouse lacked the real\-time capabilities we needed. This was particularly important for our analytics and automation operations, where immediate event triggering and analysis were essential.” This prompted a clear need for evolution and the start of their search for a more efficient solution.


Ongage's prior analytics setup relied heavily on a large MySQL cluster, managed and operated by AWS RDS. As their data volumes increased, the limitations of MySQL started to surface. The performance sharply declined and the analytics page load times became too long.


ClickHouse entered the picture, offering a significant leap in data processing real\-time analytics capabilities. MySQL is still retained for handling transaction data that doesn’t grow significantly, and is used to enrich data in ClickHouse with details such as account and campaign names.


One of the key elements that eased this transition was ClickHouse's built\-in MySQL engine. This feature enabled the Ongage team to extract data from MySQL and convert it into ClickHouse's native table format effortlessly. The MySQL engine was used not just to query data, but also to facilitate a smooth migration into ClickHouse.


## Why ClickHouse Overcame SingleStore in Ongage's Assessment [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#why-clickhouse-overcame-singlestore-in-ongages-assessment)


When selecting a data management solution, the team at Ongage didn't just go with the first option. They explored various solutions, SingleStore being a prime contender. During an in\-depth evaluation, they stacked SingleStore against ClickHouse, considering storage costs and specific feature availability.


From a cost perspective, ClickHouse presented a far more economical choice. SingleStore storage costs were six times more than those of ClickHouse Cloud for identical data volumes. Considering Ongage's data\-intensive operations, this meant a considerable expense.


In terms of feature offerings, ClickHouse offers a clear advantage that SingleStore lacks \- the implementation of Materialized Views. This feature is a major timesaver as it facilitates aggregating a substantial number of events into a smaller, more manageable table. This, in turn, speeds up query execution considerably.


Nevertheless, it's worth noting that SingleStore might be a more suitable fit for organizations prioritizing transactional capabilities. As Ongage specifically sought real\-time analytics, this wasn't one of the factors for them. ClickHouse clearly emerged as the champion, considering the specific needs and plans Ongage had.


## The Decision: Why ClickHouse Cloud? [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#the-decision-why-clickhouse-cloud)


Ongage's decision to use ClickHouse Cloud over the open\-source self\-managed option was influenced by several key factors.


Firstly, the operational efficiency of the cloud solution stood out. Raslin explained, "We spent so much work and money into managing the Mongo clusters and the Redshift clusters. We don't want to waste this time anymore." Despite their DevOps team being comfortable with self\-hosting, they recognized the substantial time and resources they could conserve by opting for ClickHouse Cloud. The operational burden of managing MongoDB and Redshift clusters was already heavy, and bypassing such hassles was too appealing to pass up.


Secondly, the value of the ClickHouse support team cannot be understated. They played a crucial role in Ongage's accelerated transformation, providing vital tips and clarifications that made the whole process smoother. This collaboration proved to be a winning formula \- working directly with the developers of the product ensured that Ongage was using ClickHouse to its full potential. As Raslin put it, "For sure, the people who build the technology are best equipped to operate it."


Lastly, the financial aspect also weighed in favor of ClickHouse Cloud. During the transformation phase, the service offered substantial cost savings by scaling automatically based on use, ensuring that resources were used efficiently. It was the ideal balance of performance and cost\-effectiveness for Ongage's needs.


## ClickHouse In Action: Seamless Transition and Enhancing Ongage's Use Cases [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#clickhouse-in-action-seamless-transition-and-enhancing-ongages-use-cases)


Ongage's transition to ClickHouse was smoother than expected due to its compatibility with MySQL, meaning most of their existing queries functioned without modifications. As Raslin highlighted “The query didn't change much from what we had before, given the similarities in table structures between MySQL \& Redshift.” This compatibility greatly facilitated the integration, reducing potential disruptions.


Once Ongage had ClickHouse integrated into their system, two main use cases were identified.


The first use case revolved around campaign analytics. Ongage implemented ClickHouse with the current UI that their customers were already familiar with. This ensured a seamless transition where users noticed a marked increase in speed, without having to adjust to a new interface. Behind the scenes, a newly built microservice in front of ClickHouse was deployed, utilizing Node.js.


![Analytics.jpg](/uploads/Analytics_ec486eef36.jpg)
The second use case focused on their automation system. Ongage designed a user\-friendly drag and drop system that triggers specific actions based on user interactions. For example, if a user clicked on a specific campaign, the system will respond with actions such as sending an email or SMS after a set waiting period. It can also make checks for user segmentation before proceeding with an action. Crucially, each block of this drag and drop system has analytics attached, allowing for an overview of how it performed over a chosen time range.


Interestingly, despite the significant backend changes, there was no alteration to the UI for both use cases.
![Marketing-automation-ongage.png](/uploads/Marketing_automation_ongage_5309175415.png)


The implementation of ClickHouse also brought real\-time decision\-making capabilities to Ongage. Previously, generating essential business reports was a time\-consuming and sometimes troublesome task. "We used MySQL before, and sometimes the warehouse took two to three hours to generate a report, sometimes causing alerts in the system. It was a pain," said Raslin.


With ClickHouse, however, the situation changed dramatically. "When we tested how much time the same reports would take with ClickHouse, people were amazed. We ran the same data, and in a blink of an eye, we had the results," said Raslin. The rapid data access offered by ClickHouse not only impressed the team but also won over the company's directors. The newfound efficiency and speed has enabled them to make informed decisions faster than ever before.


## Ongage's Scalable Architecture: Leveraging ClickHouse for Real\-Time Analytics [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#ongages-scalable-architecture-leveraging-clickhouse-for-real-time-analytics)


Ongage's architecture has evolved over time to cater to real\-time data analytics and automation infrastructure needs. At the core of Ongage's architecture is ClickHouse.


1. Insert Raw Data and Enrichment: The first step in their architecture involves the transfer of raw data to S3\. Using the S3 cluster function it is then immediately inserted into ClickHouse. Concurrently, around eight tables from MySQL are copied into ClickHouse using the MySQL engine to ensure that their data remains updated and enriched. This data is then transferred to a MergeTree table and becomes available with the exchange command. This process is streamlined thanks to ClickHouse's MySQL syntax compatibility.
2. Materialized Views and SummingMergeTree: The final step in their architecture involves the use of a materialized view triggered on the insertion of raw data. This materialized view runs multiple joins to enrich the data, which is then written to a SummingMergeTree table \- the final destination from where consumers query. This step aggregates all the data together on different 'group by' parameters, enabling rapid analytical results. Depending on the use case, MySQL data is either append\-only or refreshed completely.


Materialized Views and SummingMergeTree: The final step in their architecture involves the use of a materialized view triggered on the insertion of raw data. This materialized view runs multiple joins to enrich the data, which is then written to a SummingMergeTree table \- the final destination from where consumers query. This step aggregates all the data together on different 'group by' parameters, enabling rapid analytical results. Depending on the use case, MySQL data is either append\-only or refreshed completely.


![Events collector.png](/uploads/Events_collector_182f981f80.png)
## What's Next for Ongage and ClickHouse: The Road Ahead [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#whats-next-for-ongage-and-clickhouse-the-road-ahead)


Ongage began their journey with ClickHouse focused primarily on analytics and has since extended the usage to their automation project. The journey doesn't end here though; they are actively looking to migrate more of their processes to ClickHouse.


The first step in this continued transformation involves fully migrating some of their legacy pipelines. They plan to use Kafka to stream data, taking advantage of the [recent ClickPipes offering](https://clickhouse.com/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service).


Ongage plans to transfer more data from their existing Redshift clusters to ClickHouse. Their experiences with the real\-time capabilities and cost\-effectiveness of ClickHouse have shown them that the platform can manage many of the tasks that they currently use Redshift for.


## Conclusion [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#conclusion)


Ongage's transition to ClickHouse has provided impressive results in a remarkably short time. Not only has their system performance significantly improved, but their reporting and real\-time analytics capabilities have also seen a substantial boost. The simplicity of query transition and the support from ClickHouse during the transformation process further eased their migration.


With the scalability of ClickHouse, handling data of their magnitude has become more streamlined. The use of materialized views and the strategic use of the MySQL engine improved the speed of data analysis, allowing better decision\-making across the board.


Moreover, the cost\-effectiveness of ClickHouse versus their previous systems ensured that Ongage not only gained a powerful data handling solution but also a sustainable one as data volumes invariably grow. As Ongage continues to leverage ClickHouse, the opportunities for further performance enhancements and cost savings are promising.


Learn more: <https://www.ongage.com/>

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

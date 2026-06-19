# Measuring brand impact: How LoopMe uses ClickHouse to deliver better brand advertising outcomes


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Measuring brand impact: How LoopMe uses ClickHouse to deliver better brand advertising outcomes

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 19, 2024 · 8 minutes read![loopMe.png](/uploads/loop_Me_ac182ffc41.png)
[LoopMe](https://loopme.com/) is on a mission to bring brand advertising into the digital age. Founded in 2012, the company’s AI\-powered ad tech solutions allow brands and agencies to effectively gauge consumer insights and improve the performance of brand advertising campaigns.


Building great ad tech products requires vast amounts of data. For LoopMe, this data is essential to analyzing user behavior, finely tuning their algorithms, and creating products that allow advertisers to send highly targeted, impactful brand campaigns. However, managing and processing such large datasets can be prohibitively expensive.


Adopting ClickHouse as their database management solution — and, more recently, switching to ClickHouse Cloud on Google Cloud Platform (GCP) — has allowed LoopMe to manage their data with far greater efficiency, scalability, and cost\-effectiveness. Perhaps most importantly, it has allowed Marco and the team to focus their efforts on what matters most: building innovative ad tech solutions.


## Transforming brand advertising [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#transforming-brand-advertising)


Marco and his co\-founder Stephen Upstone have worked in ad tech since 2005\. After the launch of the iPhone in 2009 sparked widespread adoption of touchscreen phones, they saw an opportunity to combine instant consumer feedback with machine learning to solve an age\-old problem in brand advertising: how to measure performance and outcomes.



> “It’s about making brand awareness, intent, and consideration measurable,” says co\-founder and CTO Marco van de Bergh. “Because when it’s measurable, you can optimize for it.


As Marco explains, “traditional” digital media buying relies on metrics like click\-through and video completion rates — but these metrics don’t reflect true brand impact. “It doesn’t really say anything about whether the user remembers your brand, or whether the campaign has changed their mind or made them consider buying a product,” he says.


LoopMe addresses this gap by collecting direct user feedback via surveys after campaigns. Questions are geared around brand recognition (“Which of these brands do you recognize most?”, “What is your perception of them?”) as well as intent and consideration (“Are you planning to travel in the next six months?”, “Would you consider booking a flight with this airline?”). This data helps media buyers move beyond simple metrics, gaining deeper insights into consumer behavior and whether brand campaigns influenced purchasing decisions.


With their extensive background in behavioral targeting and machine learning, Marco and his team have been at the forefront of using AI in ad tech, progressing from linear regression algorithms to sophisticated machine learning models. Their current approach involves a dynamic “model ecosystem,” where multiple algorithms run concurrently for each campaign, competing to deliver the best outcomes. For two minutes at a time, whichever model has the best results buys the media, before the model resets and the process begins again.


For LoopMe’s customers — PepsiCo Mountain Dew, Sony Pictures, Warner Bros Discovery., to name a few — its value lies in the ability to enhance upper\-funnel measurement, focusing on building brand equity rather than just driving clicks. By providing precise insights into the impact of brand campaigns, LoopMe helps brands tailor their advertising strategies to resonate with different audiences, leading to greater brand awareness and measurable results.


![loopme_mindshare.png](/uploads/loopme_mindshaqre_b408b9165a.png)
## A better data solution [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#a-better-data-solution)


To build and train its ad tech products, LoopMe requires enormous volumes of data that must be processed and analyzed in real time. This data, which comes from a diverse array of sources and formats, including user behavior data, device information, and interaction metrics, is what allows LoopMe’s AI models to optimize brand advertising campaigns.


Along with the operational and financial challenges of managing such huge and complex quantities of data, LoopMe must ensure that its data is accurate to effectively optimize campaigns, it must keep its data secure to comply with privacy regulations, and it must be able to increase data loads seasonally without sacrificing on performance or cost.


These are complex challenges for any company, and they’re what led Marco’s team to investigate a better solution for their data needs. After evaluating several options, they found that most traditional databases struggled with the high query rates and data ingestion speeds necessary for their requirements. ClickHouse, on the other hand, showed it could process large volumes of data quickly and efficiently, making it an ideal choice.


Marco also says that while initially there were hesitations about partnering with a third\-party service, especially given the sensitive nature of the data involved in ad tech, they were drawn to ClickHouse’s well\-documented security policies and practices. This documentation ensured that LoopMe could maintain security integrity while using ClickHouse, and provided the necessary assurances to auditors that their data security was intact.


## The benefits of ClickHouse [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#the-benefits-of-clickhouse)


Marco’s team began integrating ClickHouse into their infrastructure in 2019\. Right away they saw its ability to handle large datasets and complex queries with lightning\-fast speed and efficiency. Soon, all of LoopMe’s ad tech products, as well as its business intelligence tools, were running on ClickHouse.


In 2024, LoopMe moved its data operations to ClickHouse Cloud. The managed service not only ensured fast, efficient, and scalable data handling, it has also dramatically simplified their infrastructure management.



> “We like to build ad tech products, not build our own infrastructure,” Marco says. “We’re very happy when we find a provider who can do things better than us.”


## Performance and efficiency [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#performance-and-efficiency)


ClickHouse’s core strength lies in its ability to process large datasets quickly. Its columnar storage format allows for faster retrieval and processing of data, speeding up analytical queries and reporting. For LoopMe, the move to ClickHouse Cloud has further optimized these processes thanks to cloud\-native technologies that enhance data processing capabilities without the overhead of managing physical servers.


The efficiency provided by ClickHouse not only speeds up operations but also reduces the load on resources, lowering operational costs. By switching to ClickHouse Cloud, LoopMe is running the same system on three nodes, as compared to the 20 it was using with its pre\-cloud ClickHouse infrastructure. With fewer resources needed to handle the same amount of data, LoopMe is able to run a leaner, more cost\-effective operation.



> “We’re a company that tries to ingest as much data as possible to make optimization decisions, which can be a recipe for rising costs,” Marco says. “ClickHouse Cloud makes that process so efficient, and the price point is so much lower, we can actually look forward to ingesting more data into our systems while keeping costs relatively at bay.”


## Seasonal scalability [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#seasonal-scalability)


Given the cyclic nature of the advertising industry, LoopMe’s revenue and data volume can vary dramatically between seasons. Data processing demands rise and fall from Q4 to Q1, for example, underscoring the value of a scalable infrastructure that can not only handle increased workloads but that also scales down efficiently during quieter periods.


While other databases and cloud services are built to accommodate growth, they’re not designed to automatically scale down during slower periods. This mismatch leads to over\-provisioning, where companies continue to incur high costs for resources that are no longer necessary.


ClickHouse, according to Marco, offers more fluid scalability. This means that LoopMe can adjust their resource use up or down, matching their infrastructure costs more closely with their actual needs throughout the year. This ability to dynamically adjust resources is crucial for maintaining cost efficiency in the fluctuating ad tech market.


## Simplified data management [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#simplified-data-management)


Transitioning to ClickHouse Cloud has greatly simplified how LoopMe manages its data infrastructure. The managed service model offered by ClickHouse Cloud means that many of the tasks associated with database maintenance, such as software upgrades, scaling, and performance tuning, are handled for them. The reduction in administrative burden allows LoopMe’s technical team to focus on innovation and improving their products rather than on maintaining their data infrastructure.



> “With ClickHouse, you have a very impressive infrastructure capable of handling big loads at a very low\-cost point,” Marco says. “The managed service opens up new opportunities for us to think differently, and it allows us to focus our resources on other challenges.”


## Continued innovation [\#](/blog/measuring-brand-impact-how-loopme-uses-clickhouse-to-deliver-better-brand-advertising-outcomes#continued-innovation)


As Marco and the LoopMe team continue to enhance their ad tech products, they plan to expand their use of ClickHouse for even greater cost optimization and resource efficiency. The ability to ingest more data while keeping costs in check means they can continuously refine their AI models and deliver more impactful solutions. And with ClickHouse Cloud handling the complexities of database management, they have more time for innovation and product development.


ClickHouse has already helped LoopMe solve one of the biggest challenges faced by ad tech providers: efficiently managing vast amounts of data. Now, it’s helping LoopMe solve another problem for businesses: measuring and optimizing brand campaigns.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

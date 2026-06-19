# Boosting Game Performance: ExitLag's Quest for a Better Data Management System


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Boosting Game Performance: ExitLag's Quest for a Better Data Management System

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Jun 26, 2023 · 4 minutes readImagine playing your favorite online game with almost no lag, enjoying smooth gameplay, and experiencing improved routing that reduces ping and ends packet loss. This is the kind of elevated gaming experience that [ExitLag](http://www.exitlag.com) is bringing to gamers worldwide.


ExitLag is a tool that optimizes the gaming experience for over 1,700 games on over 900 servers worldwide and provides a faster, less crowded connection, thus minimizing lag, enhancing game routes, and ending packet loss. In their continuous effort to resolve common connection problems for gamers, ExitLag faced performance issues with MySQL. They encountered bottlenecks and slowdowns with specific analytical queries about user behavior analysis and network route mapping, especially as their data volume increased.


In order to provide a better gaming experience, ExitLag has developed a sophisticated method for sending connection packets from users. These packets are sent simultaneously through different routes, thus increasing the guarantee that the packet will be delivered. Information such as region, IP, date, and connection type is used to decide the best route.


[Datacosmos Consultoria](https://www.datacosmos.com.br/), a leading IT consultancy based in Brazil, specializing in database and cloud services, has been instrumental in helping ExitLag take their customer experience to the next level with ClickHouse.


![Exitlag_dashboard.png](/uploads/Exitlag_dashboard_a2f4db9e3e.png)
## From MySQL to ClickHouse [\#](/blog/boosting-game-performance-exitlag-quest-for-a-better-data-management-system#from-mysql-to-clickhouse)


Datacosmos helped ExitLag transition from MySQL to ClickHouse, which they chose for its exceptional performance, scalability, and efficient data compression capabilities. ClickHouse offers a significant advantage over MySQL when it comes to the performance of analytical queries. In the past, even if a server had resources comparable to or better than those used in ClickHouse, it was still impossible to analyze certain data with the same level of efficiency. With ClickHouse, ExitLag could quickly process billions of lines of data in a short time, catering to their need for speed and scale.


ExitLag processes approximately 6 million daily events, using ClickHouse to analyze user behavior on their service and map possible network routes. These valuable insights into user behavior, game preferences, session durations, and network performance have not only provided gamers with optimized routes and an enhanced gaming experience but also improved ExitLag's ability to handle data at scale.


![Exitlag_architecture.png](/uploads/Exitlag_architecture_f36c38c856.png)
## ClickHouse Advantages [\#](/blog/boosting-game-performance-exitlag-quest-for-a-better-data-management-system#clickhouse-advantages)


ClickHouse's materialized views have been another game\-changer for ExitLag. By precomputing and storing results of complex queries, materialized views provide faster access to aggregated data, reducing the need for repetitive computations. This feature, coupled with ClickHouse's scalability, has allowed ExitLag to efficiently handle an increasing data volume and provide swift responses to analytical queries. Visualization tools such as Grafana and Power BI, as well as ad\-hoc queries, are used to analyze and present this aggregate data.


The transition to ClickHouse has resulted in significant cost savings. ClickHouse's efficient data compression allows for managing vast volumes of data with lower disk consumption, resulting in reduced infrastructure costs. Additionally, faster data analysis with ClickHouse has optimized resource utilization, further driving down operational costs.


As Leandro Sandmann, Co\-Founder and Executive Board Member at Exitlag, states, “My experience with ClickHouse adoption has been revolutionary. By implementing this innovative technology, I have witnessed a significant jump in the productivity of my business. The benefits were immediate, with faster data processing and accurate analytics that allowed me to make strategic decisions with confidence. ClickHouse opened new horizons for the growth and success of my company, raising our executive vision to levels never reached before.”


## Future Plans with ClickHouse [\#](/blog/boosting-game-performance-exitlag-quest-for-a-better-data-management-system#future-plans-with-clickhouse)


Moving forward, ExitLag plans to leverage ClickHouse's analytical and machine learning capabilities. They aim to deepen their understanding of user behavior, network performance, and game preferences to continually improve their services. They also plan to explore ClickHouse's advanced features such as data replication and real\-time analytics and predictions.


ExitLag's journey in embracing ClickHouse, with the help of Datacosmos Consultoria, has not only solved their data management challenges but also redefined their ability to provide a superior gaming experience. The transition from MySQL to ClickHouse has showcased the importance of finding a solution that aligns with a company's specific needs, while also being scalable and cost\-effective.


As Rodrigo Salviatto, Director of Datacosmos explains, "If the goal is to analyze a large amount of data, in the order of billions of lines, in a time reduced to a minimum, the most appropriate choice is ClickHouse."


## Learn More [\#](/blog/boosting-game-performance-exitlag-quest-for-a-better-data-management-system#learn-more)


Visit: <www.exitlag.com>


Visit: [www.datacosmos.com.br](https://www.datacosmos.com.br/)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

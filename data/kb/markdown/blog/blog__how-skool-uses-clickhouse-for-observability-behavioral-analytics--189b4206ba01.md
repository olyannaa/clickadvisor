# From minutes to seconds: How Skool’s migration from Postgres to ClickHouse transformed their analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# From minutes to seconds: How Skool’s migration from Postgres to ClickHouse transformed their analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 20, 2024 · 6 minutes read[Skool](https://www.skool.com/) is an all\-in\-one community platform where users can discover communities or create and monetize their own. Founded in 2019 with the goal of making learning and collaboration fun, Skool empowers users — including hobbyists and high\-profile artists—with easy\-to\-use tools for communication and content sharing.


Two years ago, Skool co\-founder and CTO Daniel Kang recognized the need for a more scalable, long\-term analytic database solution to support the company’s growing user base. His search culminated in the adoption of ClickHouse, a move that transformed how Skool’s platform ingests, processes, and analyzes millions of records daily.


At an [August 2024 meetup in Los Angeles](https://clickhouse.com/videos/skools-journey-with-clickhouse), Skool’s head of data, Jason Anderson, shared more about their decision to adopt ClickHouse, plus some of the ways the company is using it to power real\-time observability, experimentation, and behavioral analytics.


## The search for speed [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#the-search-for-speed)


In their initial database setup, Skool used Postgres to handle both transactional and analytics workloads. While this setup was sufficient early on, by 2022, as Skool's user base expanded, the system began to show strain. Running both workloads on the same database technology led to bottlenecks, with analytics queries often taking minutes to complete. Jason noted, "You could make it work, but it was slow and needed a lot of optimization".


As Jason explains, the company needed a new database solution that could 1\) ingest more than 100 million rows of telemetry data daily and 2\) deliver "lightning\-fast analytics queries." After evaluating different options, they chose ClickHouse, a columnar OLAP database management system, and moved their analytics operations to ClickHouse Cloud. The migration brought immediate improvements, particularly in query performance.



> "We went from minutes for analytic queries down to seconds without really any optimization effort at all. That's been a huge win for our entire business."
> 
> Jason Anderson, Head of Data


## Unlocking data potential [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#unlocking-data-potential)


Over the past two years, Skool has expanded its use of ClickHouse to cover an increasing number of use cases, including real\-time observability, experimentation, and behavioral analytics. At the meetup in Los Angeles, Jason shared more about these use cases:


### Observability dashboards [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#observability-dashboards)


Skool uses Grafana, integrated with ClickHouse, to visualize real\-time observability across their systems. These dashboards provide a unified, global view of Skool’s platform, allowing the team to monitor both front\-end and back\-end systems effectively.


Telemetry data from all Skool servers flows into ClickHouse, where it’s stored in an efficient columnar format. Data includes everything from server health metrics to user activity logs, which are then queried in real\-time by Grafana. ClickHouse’s ability to handle large volumes of data and run fast queries ensures that the dashboards remain up to date, allowing the team to identify and address any performance issues or anomalies quickly.


While Skool is still exploring advanced features like materialized views, Jason says ClickHouse’s performance has been more than sufficient, enabling real\-time insights without adding complexity. As the platform grows, he says Skool plans to adopt more ClickHouse features to handle the increasing data load, improving their monitoring capabilities.


### Experimentation platform [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#experimentation-platform)


To iterate and improve the user experience, Skool runs A/B tests with GrowthBook, an open\-source experimentation platform. ClickHouse powers the backend, storing telemetry and event data from user interactions. The platform records each experiment variant and tracks user behavior in real time, allowing the Skool team to compare control groups and variants based on metrics like signups and comments.


Jason notes that ClickHouse's performance has made this process seamless, delivering fast experiment results and letting the team make quick decisions without heavy optimization.



> "We haven't had to optimize anything, ClickHouse is fast enough."
> 
> Jason Anderson, Head of Data


### Behavioral analytics [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#behavioral-analytics)


Skool also uses ClickHouse to monitor user behavior, analyzing data from key stages of the user journey, such as account creation and group joining. As Jason explains, "We're always trying to understand what users are doing on our site so we can reduce friction and make their time more enjoyable."


For instance, telemetry events are recorded for each step in the signup funnel, giving the team granular insights into where users drop off. With ClickHouse powering their analytics, Skool can segment these funnels by device type, location, and other factors, optimizing the user experience accordingly. Funnel data is visualized in Grafana, giving Skool actionable insights that help eliminate roadblocks and drive higher engagement across mobile and desktop.


### Learning on the fly [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#learning-on-the-fly)


The adoption of ClickHouse has brought a number of benefits, from faster query times to a newfound ability to monitor real\-time analytics, experiment with new features, and gain deeper insights into user behavior. Still, Jason acknowledges Skool has more to unlock in terms of the database's full potential. For anyone considering making the switch, he shared some key learnings from their experience using ClickHouse so far.


First, he emphasizes the importance of carefully planning table structures and partition keys at the outset, as these can't be easily modified later. The team also learned that reducing the cardinality of indexes by using functions like [`toStartOfHour`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#tostartofhour) can significantly improve performance when working with time\-based data.


Finally, Jason encourages anyone with questions about ClickHouse, especially those who are considering implementing it, to reach out to ClickHouse's support team, who he says have been responsive and helpful throughout Skool's journey with ClickHouse Cloud.


"Talk to your ClickHouse reps," he says. "They're great at what they do. They're a wealth of knowledge. And they want to make sure you're successful."


## A strong foundation [\#](/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics#a-strong-foundation)


With ClickHouse powering its analytics operations, Skool is primed for continued growth and success. The reduction in query times means the team can focus on innovation and improving the user experience, while ClickHouse Cloud ensures the platform can scale to handle any increase in data volumes. As Jason notes, Skool is already exploring advanced features like materialized views to expand its capabilities even further.


Looking ahead, Skool is set up to keep scaling its community platform without sacrificing performance. The combination of ClickHouse’s real\-time analytics, scalability, and the support of a responsive team means Skool can continue developing new tools for creators, educators, entrepreneurs, and other community builders.


Want to learn more about how ClickHouse can supercharge your analytics with real\-time insights? [Try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

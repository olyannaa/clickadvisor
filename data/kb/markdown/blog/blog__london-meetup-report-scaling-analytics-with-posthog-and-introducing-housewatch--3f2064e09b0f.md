# London Meetup Report: Scaling Analytics with PostHog and Introducing HouseWatch


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# London Meetup Report: Scaling Analytics with PostHog and Introducing HouseWatch

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Jul 5, 2023 · 6 minutes read
  

On May 25th, 2023, at the ClickHouse meetup in London, Tim Glaser, co\-founder and CTO of [PostHog](https://posthog.com/), introduced their new project [HouseWatch](https://posthog.com/blog/introducing-housewatch) \- an open\-source suite of tools for monitoring and managing ClickHouse. During the presentation he also shared insights into PostHog's handling of huge amounts of analytics queries and their strategies for scaling, optimization, and administration.


PostHog is an open\-source solution that combines multiple analytics tools into one platform. It enables users to perform complex funnel queries, visualize trends, and filter product analytics data, providing valuable insights into user behavior.


PostHog boasts a vibrant developer community with more than 10,000 GitHub stars. It has tracked over 50 billion events, primarily on their US cloud, and manages an impressive volume of data. Their events table alone handles around 62 terabytes of uncompressed data for just one column. The total volume of uncompressed data being queried is in the range of a couple of hundred terabytes.


## Features of PostHog: Session Replay, Feature Flags, and Seamless Data Integration [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#features-of-posthog-session-replay-feature-flags-and-seamless-data-integration)


PostHog offers several distinct features that simplify operations and provide key insights. With session replay, users can watch real\-time interactions on their websites for deep analysis. Feature flags allow specific user groups to experience new features, aiding data\-driven product decisions. Additionally, PostHog's advanced event pipeline supports seamless data transfer to different systems, integrating generated insights effectively.


![posthog_1.png](/uploads/posthog_1_bce1040450.png)
## Enhanced Scalability with ClickHouse [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#enhanced-scalability-with-clickhouse)


PostHog successfully scaled their platform by [transitioning from Postgres to ClickHouse](https://posthog.com/blog/how-we-turned-clickhouse-into-our-eventmansion) and leveraging AWS servers, effectively catering to their growing usage needs. PostHog tackled slow queries and user data aggregation issues by introducing strategic optimizations.


### Challenge 1: Optimizing JSON Field Reading [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#challenge-1-optimizing-json-field-reading)


One significant challenge encountered by PostHog was the performance impact of reading from JSON fields. Although ClickHouse handles this efficiently, queries involving billions of events for their largest customers became slow. To address this, PostHog introduced a [materialized column to the events table](https://posthog.com/blog/clickhouse-materialized-columns), identifying the most frequently used columns and materializing them. This optimization dramatically improved query performance and reduced processing time.


![posthog_2.png](/uploads/posthog_2_b0575d359b.png)
### Challenge 2: Aggregating by Unique Users [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#challenge-2-aggregating-by-unique-users)


PostHog faced a complex problem when it came to aggregating data by unique users. Due to mutable user IDs and the need to merge user data from different sources, traditional approaches proved inefficient. To overcome this challenge, PostHog implemented a pattern based on a person override table. Instead of modifying the event data directly, they store old and new person IDs along with versions in a separate table. This approach allows for efficient querying and aggregation by incorporating the correct person IDs when needed. More specifically,


1. A "person overrides" table was created: This table is separate from the main event table. It stores the old person ID, the new person ID, and a version identifier (to know what the latest is).
2. The person ID ingested with events is the one that is believed to be correct: This is correct in about 96% of cases. But if a merge happens (for instance, when someone logs in or when an anonymous user becomes a logged\-in user), a row is added to the person overrides table.
3. The person overrides table is used in queries: When running a query, they join in the person overrides table and use either the overridden person ID or the original person ID that was on the event.
4. They periodically update the person IDs based on the override table: To prevent the person override table from becoming too large, they run a job that updates the person IDs based on the override table, rolling up all changes and maintaining fast query performance.


![posthog_3.png](/uploads/posthog_3_d20847a2c5.png)
The optimizations made by PostHog had a dramatic effect on performance. As Tim Glaser highlighted, "Y Combinator's queries went from 18 seconds down to one second on average, and P95 queries went from 60 seconds to four seconds." This improvement in performance allows for more efficient data analysis, leading to faster insights and better decision\-making.


### Additional Optimization: Sampling for Improved Performance [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#additional-optimization-sampling-for-improved-performance)


PostHog recognized the value of providing users with control over query performance. To address this, they introduced a sampling feature, allowing users to trade off accuracy for speed. By offering a button to adjust the sampling rate, users can expedite query execution and obtain quick results, especially during high\-demand or overwhelming situations.


## Introducing HouseWatch \- Streamlining ClickHouse Administration [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#introducing-housewatch---streamlining-clickhouse-administration)


PostHog launched [HouseWatch](https://posthog.com/blog/introducing-housewatch), a react app deployable via Docker, to provide enhanced visibility and control over ClickHouse infrastructures. This tool simplifies ClickHouse administration by offering extensive query monitoring and operations management features.


HouseWatch enables real\-time query monitoring, providing essential performance metrics. Users can quickly assess query performance and identify potential bottlenecks, improving their decision\-making process.


### Monitoring Long\-Running Queries [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#monitoring-long-running-queries)


HouseWatch enables users to identify and monitor long\-running queries with ease. The tool offers a clear view of the top 10 queries with extended execution times. Users can quickly pinpoint the specific teams or parameters associated with these queries, allowing for focused optimization efforts and improved overall query performance.


### Schema Stats and Disk Usage Analysis [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#schema-stats-and-disk-usage-analysis)


With HouseWatch, users gain access to valuable schema statistics. The tool provides an overview of the largest tables within ClickHouse, facilitating efficient disk usage analysis. By drilling down into individual tables, users can identify the largest columns and take proactive measures to optimize storage and enhance performance.


### Simplified Operations and Query Control [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#simplified-operations-and-query-control)


HouseWatch streamlines ClickHouse operations by providing essential management features. Users can terminate running queries seamlessly, eliminating the need for manual intervention. Additionally, HouseWatch includes a migration management system that allows users to create forwards and backward migrations, simplifying database schema updates and ensuring a seamless operational workflow.


![posthog_4.png](/uploads/posthog_4_6be1ed1bad.png)
PostHog's open\-source product provides users with powerful tools for product analytics, session replay, feature flags, and experimentation. With optimizations and innovations like materialized columns and the person overrides table, PostHog has significantly improved query performance. The introduction of HouseWatch helps streamline ClickHouse administration, offering valuable insights, query control, and simplified operations. As Tim states, "We're committed to revolutionizing data management and delivering exceptional value to ClickHouse users."


### More Details [\#](/blog/london-meetup-report-scaling-analytics-with-posthog-and-introducing-housewatch#more-details)


- This talk was given at the [ClickHouse Meetup in London](https://www.meetup.com/clickhouse-london-user-group/events/292892824/) on May 25, 2023
- The presentation materials are available [on GitHub](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup75/Serving%205m%20analytics%20queries%20a%20month%20with%20ClickHouse%20-%20PostHog.pdf)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

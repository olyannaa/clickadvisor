# Querying ClickHouse on your Phone with Zing Data \& ChatGPT


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Querying ClickHouse on your Phone with Zing Data \& ChatGPT

![](/_next/image?url=%2Fuploads%2Fzing_36ffbb512c.png&w=96&q=75)Zach Hendlin, Co\-founder \& CEO of Zing DataMay 2, 2023 · 5 minutes read
ClickHouse is used by companies to power fast queries. But for many companies, the challenge of having an analyst write a query, create a dashboard, and share that throughout the organization adds substantial lag to getting questions answered – even if the database is fast.


Zing Data is a modern data analysis and business intelligence platform, built to work on any device you have \- iOS, Android, and the web. Even from mobile, Zing’s new ClickHouse support means you can:


- Query with natural language querying (powered by OpenAI’s ChatGPT)
- Visually query in just a few taps – even from raw tables and views
- Set up real\-time alerts (push or email) to get notified when data changes
- Query based on your phone’s current location


Zing’s AI\-powered query optimization helps suggest date handling (like casting timestamps to dates), graph types, and even handles long running queries – simply sending you a notification when results are ready and showing sampled previews for large result sets.


## Mobile Querying and Visualization [\#](/blog/querying-clickhouse-on-your-phone-with-zing-data#mobile-querying-and-visualization)


Zing Data's [mobile app provides a powerful yet simple interface for querying and visualizing ClickHouse data on the go](https://docs.getzingdata.com/docs/asking-questions/). Unlike other BI tools which require somebody at a computer to pre\-create dashboards or limit you to certain filters, Zing lets you ask *any question of your raw data from iOS, Android, and the Web.*


The app supports a wide range of visualizations, including line charts, bar charts, data tables, maps, and more. Calculated fields, a SQL typeahead, and joins empower you to do more complex data operations.


For long running queries, Zing’s server persists a connection to ClickHouse to complete the query in the background, and sends you a push notification when the results are ready.


## Enabling OpenAI Queries on ClickHouse Data [\#](/blog/querying-clickhouse-on-your-phone-with-zing-data#enabling-openai-queries-on-clickhouse-data)


Zing Data's ClickHouse integration allows you to leverage the power of OpenAI to ask complex questions and receive meaningful answers fast. Ask questions in a conversational style without worrying about syntax or debugging SQL – and Zing supports asking natural language questions in an array of languages including English, Spanish, French, German, and Japanese (among others).


Zing’s query intelligence layer takes the SQL for your natural language query and applies visualization logic \- ensuring aggregations are on the y\-axis, dates/times are on x\-axis, and multiple group bys show up as stacked series.



![zing_with_open_ai.jpg](/uploads/zing_with_open_ai_c30c3e592b.jpg)

## Real\-Time Alerts [\#](/blog/querying-clickhouse-on-your-phone-with-zing-data#real-time-alerts)


Zing Data's [real\-time alerts functionality](https://docs.getzingdata.com/docs/alerts/) allows users to set up push notifications or emails that trigger when certain conditions are met in a query on ClickHouse data. This enables users to monitor their data in real\-time and take action when important trends or anomalies are detected without having to constantly check dashboards.


Users can create alerts based on a wide range of conditions, such as when sales exceed a certain threshold, when inventory levels drop below a certain level, or when customer churn rates increase beyond a certain level. Alert conditions can be checked as frequently as every minute, or as infrequently as every month.


Zing Data's real\-time alerts are highly customizable \- for example you can set up multiple alerts for different conditions or datasets and each user can have their own individual alert settings.



![zing_alerts.jpg](/uploads/zing_alerts_5f600e693d.jpg)

## Location\-Based Questions [\#](/blog/querying-clickhouse-on-your-phone-with-zing-data#location-based-questions)


For any tables with latitude and longitude fields, [Zing can query and display results based on your phone’s current location](https://docs.getzingdata.com/docs/location-based-querying/). For instance, a maintenance worker could see all the high priority jobs that are beyond their SLA within 10 miles of their current location to go take action. Or a store manager could see which nearby warehouses are stock of a critical product.


This location can be dynamic to each user’s device, so somebody in Tampa will see results within 10 miles of their location, while another user accessing the same question will see results within 10 miles of, say, San Francisco.



![zing_locations.gif](/uploads/zing_locations_621093cd2e.gif)

## Getting Started [\#](/blog/querying-clickhouse-on-your-phone-with-zing-data#getting-started)


Zing Data's ClickHouse integration is a powerful tool that enables users to query and visualize ClickHouse data on mobile devices web, run advanced OpenAI queries on ClickHouse data, and set up real\-time alerts on top of ClickHouse data.


Whether you're a data analyst, a business user, or a developer, Zing Data's ClickHouse integration can help you unlock valuable insights from your data and make better decisions in real\-time.


Both Zing Data and ClickHouse have generous free tiers and are affordable at scale. A [step\-by\-step setup guide to getting started is here](https://docs.getzingdata.com/docs/setting-up-a-data-source/clickhouse_setup/).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

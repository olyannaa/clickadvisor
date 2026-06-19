# A ClickHouse\-powered Observability Solution: Overview of Highlight.io


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# A ClickHouse\-powered Observability Solution: Overview of Highlight.io

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Apr 21, 2023 · 5 minutes readObservability has become a critical aspect of understanding system performance, identifying issues, and ensuring seamless user experiences. [Highlight.io](https://www.highlight.io/) is an open\-source observability platform that utilizes ClickHouse for data storage and retrieval. Initially focused on session replay and frontend web development features, Highlight.io has now expanded into the full\-stack observability space. This enables developers to track user experiences within web apps, identify backend errors, and analyze associated logs across their infrastructure, ultimately helping engineers diagnose the root cause of an issue.


With just a few lines of code, developers can integrate Highlight.io into their frontend and backend systems, gaining access to insights ranging from user button clicks in the frontend to the downstream effects on their infrastructure and services. All of this information is available in a single\-pane view, streamlining the troubleshooting process.


## Enhancing Highlight.io with Backend Log Monitoring [\#](/blog/overview-of-highlightio#enhancing-highlightio-with-backend-log-monitoring)


As Highlight.io continues to evolve and expand its offerings to provide a more comprehensive observability solution, the platform has [recently added logging capabilities](https://www.highlight.io/blog/how-we-built-logging-with-clickhouse) to its stack, powered by ClickHouse. This addition is aimed at enabling developers to gain deeper insights into their applications by capturing and analyzing server\-side logs. With plans to further explore traces in the near future, Highlight.io is on its way to offering an even more robust and holistic solution for developers to monitor and optimize their applications.


![Highlightio_image1.png](/uploads/Highlightio_image1_488ce7093f.png)
Vadim Korolik, CTO of Highlight.io, explained the company's shift towards backend monitoring: "Now that we are committed to this transition, we're interested in recording traces, logs, and even more context from server\-side information. As a first step, we explored building our new logging product. Now, our customers can search through months of browser and server\-side log data in under a second thanks to the tech behind ClickHouse.”


![Highlightio_image2.png](/uploads/Highlightio_image2_1dd59a7b92.png)
Highlight.io’s use of ClickHouse began with the log visualization product due to the natural fit of an OLAP DB for the time\-series data. Now, they’re looking to adopt it for other parts of their query engine across frontend user sessions, application errors, and metrics due to the benefits they’ve seen in terms of superior performance and lower data storage costs.


## High Data Ingestion Rates with ClickHouse [\#](/blog/overview-of-highlightio#high-data-ingestion-rates-with-clickhouse)


Highlight.io's integration with ClickHouse enables the platform to handle high data ingestion rates, ensuring that developers can access up\-to\-date information in real\-time. The platform's architecture, which includes a front\-end built with React and TypeScript, and a back\-end built using Go, leverages ClickHouse for storing log data and combining it with information from other data stores. This integration allows developers to quickly access and analyze user sessions, logs, and error information, helping them identify and resolve issues more effectively in a cohesive way.


![Highlightio_image3.png](/uploads/Highlightio_image3_3d76db2cbb.png)
To install Highlight.io, customers simply add a few lines of code by installing their respective Highlight.io SDK. Behind the scenes, Highlight.io uses a cloud\-hosted OpenTelemetry agent, publicly exposed for customers’ SDKs to connect to, which, for simplicity, wrap OpenTelemetry SDKs to keep installation simple. Upon ingestion, data is stored in a single table with a project ID as part of the primary key for handling multi\-tenancy and scaling. This allows for a manageable but performant data schema by leveraging ClickHouse features such as conditional TTLs and map indexes for efficient search over both structured and unstructured data.


ClickHouse offers an extended version of SQL, with features for writing optimal analytical queries. This is incredibly performant as well as being familiar to engineers, meaning time is spent building their product rather than learning new tools.


## Journey Towards Backend Monitoring [\#](/blog/overview-of-highlightio#journey-towards-backend-monitoring)


Highlight.io selected ClickHouse over other alternatives, including Elasticsearch, thanks to its exceptional performance, real\-time analytics features, and versatile deployment options. With open\-source ClickHouse for self\-managed implementations and the highly scalable ClickHouse Cloud for their production cloud offering, they found the perfect solution. In their cloud offering, Highlight leverages ClickHouse Cloud seamlessly connected through AWS PrivateLink.


Highlight.io has a strong commitment to open\-source development and they are continually exploring ways to enhance their product offerings and improve their integration with ClickHouse. In fact, Highlight.io's team is working on improving their query syntax, making it easier for developers to search and filter logs based on specific criteria.


As developers increasingly demand more effective ways to monitor their applications, platforms like Highlight.io are stepping up to provide the necessary insights to ensure optimal performance. By leveraging ClickHouse's high\-performance capabilities, Highlight.io delivers a robust and scalable observability solution that can help developers keep their applications running smoothly and efficiently. With the launch of their logging product, Highlight.io and ClickHouse are set to provide developers with a cohesive solution for diagnosing and uncovering issues in their applications.


Visit: [highlight.io](https://www.highlight.io/) and read their [recent blog on OpenTelemetry](https://www.highlight.io/blog/opentelemetry).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

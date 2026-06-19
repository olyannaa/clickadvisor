# Prefect \- Event\-driven workflow orchestration powered by ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Prefect \- Event\-driven workflow orchestration powered by ClickHouse

![](/_next/image?url=%2Fuploads%2Fprefect_avatar_ed11470250.png&w=96&q=75)Sarah Bedell \& Chris Guidry, PrefectMay 30, 2024 · 10 minutes readPrefect’s orchestration and observability platform helps developers build and understand their data pipelines and, crucially, react to them. Providing a resilient and versatile product guides their mission to continuously evolve, adapt, and stay relevant to developer needs. It’s no surprise they are enabling the move to an event\-based architecture, as Sarah Krasnik Bedell, Director of Growth Marketing at Prefect explains: *“We want to be able to handle a wide variety of different data pipelines and code tasks. Ultimately, the goal is to enable whatever deployment and trigger patterns developers, data engineers, platform engineers, and software engineers need,”* and this is why ClickHouse has become integral to Prefect.


![Screenshot 2024-05-29 at 8.27.30 AM.png](/uploads/Screenshot_2024_05_29_at_8_27_30_AM_ff0dd81ad9.png)
## Prefect \- event\-driven workflow automation at scale [\#](/blog/prefect-event-driven-workflow-orchestration-powered-by-clickhouse#prefect---event-driven-workflow-automation-at-scale)


The funny thing is, Prefect is not focused on pipeline success, but rather on dealing with failures. *“We want to expose errors in a way that is most productive to help our users react to failures,”* says Bedell. The times when tracking is most important is when things fail, she continues: *“No one logs into an orchestration dashboard and says ‘Wow, my pipelines are great today’, and then continues looking at the dashboard and stays there, right?”* Failure creates the urgency to observe and react — and that is Prefect’s focus.


When users capture and process large amounts of data, workflow observability, flexible automation, and notifications become increasingly important. Enter Prefect Cloud, which builds on the strong foundation of Prefect’s open\-source product to address these needs in a turnkey, enterprise\-grade and secure way: *“With Prefect Cloud, we’re taking observability up a notch to enable people to observe and react to the health of any code that drives their business,”* says Bedell.


Rather than observing why one particular run (an instance of workflow execution) failed or had a problem, Prefect Cloud is moving towards a much higher\-level abstraction meant for team leaders. Bedell wants to deliver observability that can answer more complex questions with additional scope encompassing business impact: *“For example, we want to enable our customers to answer, ‘where are the biggest cost centers in terms of moving data?’, or maybe ‘are these expensive machine learning pipelines optimized?’ It’s a much broader code base than just batch data pipelines and that's where the conversation around ClickHouse started.”*


On a consistent basis, Prefect Cloud runs over a million “flow runs” per day – a “flow” is the most fundamental concept in Prefect representing a container for workflow logic as\-code. Bedell explains: *“Each of those flow runs could range from a few to hundreds of tasks. Then within each of those, breaking it up from the largest object to smallest object, each creates events, and those events could be state events, they could be artifacts created – it’s not one task, one object.”* Having a multi\-tenant architecture means that events from different customers are within the same database, all sliced out into partitions. Events are also customers’ log messages. So, when customers log data during the course of their flows those log messages are also events, as Staff Software Engineer, at Prefect, Chris Guidry explains: *“Our logs feature on Prefect Cloud is also backed by the same event stream, so volume is tied to a fundamental metric we watch – how many flow runs per day are people running. Any given flow might spawn 200\+ events. In February, Prefect had between 150 to 200 million events per day and the ambition is much greater.”*


## Original data stack \- Google BigQuery and PostgreSQL [\#](/blog/prefect-event-driven-workflow-orchestration-powered-by-clickhouse#original-data-stack---google-bigquery-and-postgresql)


The Prefect team started with the observability platform on Google BigQuery, a traditional cloud data warehouse, as a main datastore and a medium\-sized PostgreSQL database instance in front as a hot data cache. Success and growth soon meant an event stream of billions, and they were pushing at the edge of PostgreSQL capabilities, since this transactional database was not built to handle analytical workloads, *“All those events go to long\-term storage in a BigQuery table. We had to scale it up several notches vertically and we were definitely pushing at the edge of what PostgreSQL and Cloud SQL could handle,”* he continues.


As Prefect started to explore the possibility of doing a higher level analysis over customers’ workflows, Guidry says there were already challenges around reliably pulling event streams and showing all the events that happen to an object or that happened during the course of a workflow running: *“As we started to talk about analyzing all the events over the many workflows that happened in a week, we quickly realized that it wasn’t going to work on our PostgreSQL because we just couldn’t query and aggregate over many things.”* They needed to rethink the technology stack to match the new value they wanted to deliver to customers.


Plus, as Guidry describes, building interactive, data\-driven applications where answers are expected by users real\-time meant costs were rising: *“Where your application or users might be querying that information hundreds of times a day or thousands of times a day. That's pretty expensive to query.”* Rising costs were a direct result of technology / use case mismatch. Postgres database is great for handling transactional workloads, but does not use hardware resources efficiently, when answering analytical questions, because as a row\-oriented database scans too much data when running aggregations on just a few columns. On the other hand, Google BigQuery was originally designed to handle data warehousing workloads – infrequent ad\-hoc queries, and as a result, its pricing model based on the amount of data scanned is exorbitantly expensive for real\-time analytical workloads, where queries are generated by the application and concurrency is high.


## ClickHouse Cloud \- Real\-time analytics platform powering next\-gen workflow observability [\#](/blog/prefect-event-driven-workflow-orchestration-powered-by-clickhouse#clickhouse-cloud---real-time-analytics-platform-powering-next-gen-workflow-observability)


![Screenshot 2024-05-29 at 8.27.37 AM.png](/uploads/Screenshot_2024_05_29_at_8_27_37_AM_5215288b9a.png)
To build the next\-gen workflow orchestration observability solution for their customers, Guidry says simply : *“We needed a new database.”* They wanted to provide Prefect users with more comprehensive metrics and triggers and a more powerful way to ask new questions of this data: *“For us, ClickHouse’s strength is looking at massive volumes of time\-oriented data, it’s very much made for event streams and we’re very happy with how ClickHouse approaches the challenge.” ClickHouse is now part of a portfolio of databases for Prefect, but added Guidry: “It’s a very important one because it's going to enable the observability features we’re already thinking about to evolve and deliver more value from Prefect Cloud.”*


Prefect Cloud launched Metrics as one of the first ways to leverage ClickHouse for more advanced aggregations, a real step towards their observability vision: *“Failure is likely a symptom of a bigger problem that needs fixing. Does it happen every single day, at a specific time? We want our users to be able to fix errors at a larger scale,”* explains Bedell. While the team started small, with just a few cards that deliver metrics derived from looking over the past week of flow runs, Guidry points out: *“What we’ve done would not have been possible without ClickHouse, that’s quite an impact!”*


Following Metrics, came Automations, Guidry explains it’s one of the earliest features put in place, where the big goal isn’t capturing information, but crucially enabling users to act on it and offering Prefect Cloud users a powerful feature set designed to create responsive systems within their workspace. The system can now respond to specific events by triggering subsequent actions, so users can better mitigate risks and maintain operational efficiency. For instance, should an uptick in late flow occurrences exceed a certain threshold, an automated alert to Slack can signal potential issues requiring attention. Explaining other scenarios Guidry says: *“Users can execute automated actions, such as database reboots, to promptly address potential database issues. If the failure rate surpasses a predetermined threshold, within a specific timeframe, the system can automatically generate new incidents with detailed information for swift resolution.”*


## Additional benefits \- Simpler, more resilient data stack and cost savings [\#](/blog/prefect-event-driven-workflow-orchestration-powered-by-clickhouse#additional-benefits---simpler-more-resilient-data-stack-and-cost-savings)


In addition to enabling Prefect to realize their vision of building a real\-time data\-driven application on top of ClickHouse, migrating from a BigQuery and PostgreSQL based analytical stack helped simplify operations and save costs.


ClickHouse allowed Prefect to consolidate multiple architectural components into one, simplifying their architecture and making it more reliable: *“ClickHouse has created resiliency in a completely new way with fewer systems to maintain, I think that's another reason why this work is so important.”* Says Bedell. Prefect also has the tools to autonomously handle large\-scale disruptions and unforeseen events, they’re reaping benefits from the platform's potential in creating resilience and adaptability



> ClickHouse was critical functionality not cost\-saving, yet ClickHouse has reduced the costs to less than $8,000 a month


Prefect was spending around $12,000 a month on CloudSQL and BigQuery overrun, because they have customers whose queries are very complex or require accessing large datasets or historical data, which would then trigger the use of BigQuery. Prefect was exceeding their budget and usage limits, resulting in additional costs. The primary motivation for implementing ClickHouse was critical functionality not cost\-saving, yet ClickHouse has reduced the costs to less than $8,000 a month. As Guidry concludes: *“We have saved costs, savings not to be sniffed at, but that was not the driving factor. This was a qualitative step. We just could not do the things we wanted until we had ClickHouse and that is why we’re so excited about it.”*


## About Prefect [\#](/blog/prefect-event-driven-workflow-orchestration-powered-by-clickhouse#about-prefect)


Prefect is a versatile event\-driven orchestration and workflow observability platform. Used for orchestrating data pipelines it simplifies the process of building, scheduling, and monitoring workflows. A Python\-based framework means users can define complex workflows as code, making it easier to manage dependencies, handle errors, and scale workflows. Prefect is widely used in industries such as finance, healthcare, e\-commerce, and more, where managing and processing large volumes of data efficiently is crucial. Prefect is continuously evolving and offers both a free, open\-source Community Edition, a paid Enterprise Edition and Prefect Cloud offering with additional features and support.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

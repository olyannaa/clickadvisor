# EMQ and ClickHouse: Real\-time, AI\-assisted analytics at the industrial edge


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# EMQ and ClickHouse: Real\-time, AI\-assisted analytics at the industrial edge

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 15, 2025 · 11 minutes read## Summary


div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

EMQ uses ClickHouse Cloud to power real\-time analytics across its MQTT\-based industrial IoT platform, serving over 1,000 enterprise customers. A ClickHouse\-based data pipeline connects edge devices to cloud dashboards, supporting high\-throughput ingestion and sub\-second queries. With ClickHouse MCP, EMQ is building AI\-powered observability tools that help operators troubleshoot issues and query live data using natural language.

When you hear “industrial IoT,” what comes to mind? Probably sensors ticking away in factories, telemetry from smart vehicles, automated alerts from machines on the line. But what often goes unnoticed are the systems that make it all work—the message brokers, data pipelines, and analytics engines powering real\-time intelligence behind the scenes.


For over a decade, [EMQ](https://www.emqx.com/en) has been at the forefront of that infrastructure. Its journey began in 2013 with the launch of [EMQX](https://www.emqx.com/en/platform), an open\-source MQTT broker designed to connect devices in low\-bandwidth, high\-concurrency environments. It quickly became the world’s most scalable MQTT platform, trusted across IoT, IIoT, and connected vehicle applications alike.


Since then, EMQ has grown into a global leader, serving more than 1,000 enterprise customers and connecting over 250 million devices. Its technology powers everything from factory equipment and energy grids to autonomous vehicles and robotic systems, with customers including Geely, HPE, VMware, Verifone, SAIC Volkswagen, Lucid, and Ericsson.


As EMQ’s scale and reach have grown, so have the demands on its platform. Customers aren’t just routing messages between devices; they need to understand what those messages mean. They want real\-time insights, flexible analysis, and the ability to act on data the moment it arrives. That shift, from connectivity to intelligence, called for something new.


Earlier this year, solution architect Cheng Sun joined us at a pair of ClickHouse meetups in Tokyo—in [April](https://clickhouse.com/videos/tokyo-meetup-EMQ-15apr25) and again in [June](https://clickhouse.com/videos/tokyo-meetup-emq-29jul25)—to share [how EMQ integrates with ClickHouse](https://clickhouse.com/docs/integrations/emqx) to deliver fast, flexible, end\-to\-end visibility from the edge to the cloud. From the messaging backbone to the AI\-powered observability layer, he showed what it looks like when messaging and analytics are no longer separate systems, but part of the same real\-time platform.


## Making MQTT work at scale [\#](/blog/emq-ai-assisted-analytics#making-mqtt-work-at-scale)


EMQ’s flagship product is an MQTT broker called [EMQX](https://www.emqx.com/en). “Whereas Kafka focuses more on data transaction capabilities, our focus is on parallelism and latency,” Cheng explains. “Our challenge is to deliver data from the edge to cloud services with minimal latency.”


[MQTT](https://en.wikipedia.org/wiki/MQTT) is a lightweight protocol originally created at IBM in 1999 and made publicly available in 2010\. Unlike HTTP, which uses point\-to\-point communication, MQTT introduces a broker between publishers and subscribers. “The broker’s role is to route messages correctly, as well as manage the state of each message and connection,” Cheng says.


Developers can also fine\-tune message delivery through MQTT’s Quality of Service settings. “You can use level 0 for lightweight, less important data—sending it just once and that’s it,” Cheng explains. “For critical data, you can use level 1 to ensure delivery at least once. And depending on the requirements, you can use level 2 to make sure data is sent exactly once.”


That flexibility, combined with its ability to support high\-concurrency environments, is a big reason MQTT has become the protocol of choice for IoT and industrial workloads.


But running a large\-scale MQTT cluster comes with challenges, particularly around state management. Every connection carries metadata: message headers, footers, connection status between publishers and subscribers. “There’s a lot of data that needs to be monitored,” Cheng says. “That’s why synchronizing data between servers in a cluster is a complex challenge.”


EMQX solves this with a cloud architecture that includes two node types: core nodes that manage session state, and replica nodes that scale out processing. “This allows you to build a cloud environment that can scale infinitely,” Cheng says.


In 2024, the team deployed a cluster capable of handling 100 million concurrent connections. “We achieved extremely high throughput on this cloud, reaching 2 million messages per second,” Cheng says. “At that time, we were running up to 23 nodes. More recently, we’ve been able to build a large\-scale IoT cloud with up to 75 nodes.”


## Real\-time analytics with ClickHouse [\#](/blog/emq-ai-assisted-analytics#real-time-analytics-with-clickhouse)


To turn raw device data into real\-time insights, EMQ needed a setup that could support high ingestion rates, low\-latency queries, and broad compatibility with both industrial protocols and modern analytics tools. For that, they turned to [ClickHouse Cloud](https://clickhouse.com/cloud).


![User Story EMQ Issue 1209 (2).png](/uploads/User_Story_EMQ_Issue_1209_2_8bbcc13f2d.png)
EMQ’s ClickHouse\-based analytics setup connects edge devices to cloud dashboards.


ClickHouse sits at the heart of EMQ’s analytics stack, powering everything from ingestion to visualization. It pulls in data from a variety of sources, including relational databases like Postgres and MySQL, streaming systems like Kafka, and industrial brokers like EMQX.


In a typical data flow, industrial devices send telemetry through southbound protocols to [NeuronEX](https://www.emqx.com/en/products/neuronex), EMQ’s edge gateway for data normalization. From there, the data travels via MQTT to EMQX, then through Kafka and finally into ClickHouse Cloud. “With this kind of architecture, you can connect data from the edge all the way to the database,” Cheng says, noting that the setup delivers sub\-second analytics, even across public networks.


![User Story EMQ Issue 1209 (1).png](/uploads/User_Story_EMQ_Issue_1209_1_d6d2b3001b.png)
End\-to\-end data pipeline from edge devices to ClickHouse\-powered analytics.


Once inside ClickHouse, the data is immediately available for fast querying. Features like [dictionaries](https://clickhouse.com/docs/sql-reference/dictionaries), [projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection), and [materialized views](https://clickhouse.com/docs/materialized-views) accelerate access and reduce resource usage. Engineers can explore the data using tools like Grafana, Power BI, or Tableau, or work with it directly in Python, Java, Rust, or Go. ClickHouse also integrates with external data lakes like [S3](https://clickhouse.com/docs/integrations/s3) and [Delta Lake](https://clickhouse.com/docs/integrations/deltalake), making it easy to combine real\-time streams with historical data.


At the April meetup, Cheng shared a live demo using simulated factory data generated in Python. OPC\-UA devices produced sensor readings like temperature and humidity, while Modbus devices sent things like production counts and error codes. The data was normalized using NeuronEX, then streamed via MQTT to EMQX. From there, EMQX’s sink feature routed it into ClickHouse using SQL\-configured pipelines.


Once ingested, the data was immediately ready for querying and visualization. Cheng highlighted ClickHouse’s [AI\-assisted query builder](https://clickhouse.com/docs/use-cases/AI/ai-powered-sql-generation), which translates natural\-language prompts into SQL. “I find the AI features offered by ClickHouse to be very user\-friendly,” he says. “The AI can analyze in a single sentence and instantly generate a SQL statement, allowing you to check the data in real time.”


He also showed off ClickHouse Cloud’s built\-in [dashboards](https://clickhouse.com/docs/cloud/manage/dashboards), setting the refresh interval to 10 seconds to display the latest data. “You can instantly see production numbers, defect counts, and more—all in real time,” he says.


## AI at the edge with ClickHouse MCP [\#](/blog/emq-ai-assisted-analytics#ai-at-the-edge-with-clickhouse-mcp)



At the July meetup, Cheng shared how EMQ has continued to expand its use of ClickHouse’s AI features to build real\-time, AI\-powered analytics tools for industrial IoT environments. To do that, they first needed to tackle three core challenges facing manufacturing clients.


The first is the complexity of managing diverse edge devices. “With so many different types of equipment and production sites,” Cheng says, “management becomes complicated.”


The second is tracking message latency. “We can’t track the delay of each individual message,” he explains. “We can only monitor average delays or delays for some messages.”


And the third is juggling multiple databases on the northbound (AKA cloud\-facing) side of the architecture). “We need a time\-series database for each message, a relational database to store detailed equipment information, and a vector database to record internal knowledge.”


The team’s goal, as Cheng puts it, was to “use ClickHouse as a unified data platform and combine the functions of all three databases into one.”


That’s where they turned to the [ClickHouse MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp). MCP (Model Context Protocol) is a new open protocol designed to let AI agents interact with third\-party systems (e.g. databases, APIs, tools) via natural language. Each system is wrapped in an MCP server, enabling developers to trace, debug, query, and analyze events with AI\-enhanced workflows. In EMQ’s case, that means giving operators the ability to ask questions like, “Why did the machine fail?” or “Where is the delay happening?” and get answers based on live data from ClickHouse.


During the demo, Cheng showed how MCP enables real\-time observability, advanced analytics, and AI\-powered troubleshooting. Using trace IDs and vector search, operators can instantly pinpoint the source of a machine error, retrieve the associated error code, and look up relevant solutions, all within the same system. “By using MCP, you can perform highly complex analytics, monitor data, and exercise fine\-grained control,” Cheng says. “With this, you can detect changes in latency and errors in real time.”


He also demonstrated new developer tools that simulate sensor data, generate schema recommendations, and automatically configure EMQX rule engines using LLMs. “I’m not very good at SQL,” Cheng admits, “so having features like this is really helpful.”


The system can stream and process data at scale, with even lightweight edge hardware feeding into cloud dashboards for cross\-cluster visibility. And to support more constrained environments, the team is looking at ways to integrate MCP with MQTT. “Since it’s difficult to install MCP on various lightweight devices, we’re exploring new approaches,” Cheng says. “By installing the MCP server proxy on the broker, you can add AI capabilities to even traditional, standard devices. All devices can be enhanced with AI features.”


## Powering the factories of the future [\#](/blog/emq-ai-assisted-analytics#powering-the-factories-of-the-future)


EMQ’s integration of ClickHouse—from real\-time pipelines to AI\-powered observability with ClickHouse MCP—shows just how far industrial IoT infrastructure has come. Instead of stitching together separate systems for messaging, storage, and analytics, companies can now build a unified stack that’s fast, flexible, and AI\-ready from day one.


By making it easier to query, monitor, and act on data, EMQ is helping customers run smarter, more responsive operations. And with seamless integration between EMQX and ClickHouse, plus AI features like MCP, ClickHouse is quickly becoming the platform of choice for the intelligent, data\-driven factories of the future.


Learn more about [how EMQX integrates with ClickHouse](https://clickhouse.com/docs/integrations/emqx), and try both [EMQX Cloud](https://www.emqx.com/en/try) and [ClickHouse Cloud](https://clickhouse.com/cloud) for free.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-26-get-started-today-sign-up&utm_blogctaid=26)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

# Introducing AgentHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing AgentHouse

![](/_next/image?url=%2Fuploads%2Fdmitry_03503caafa.jpg&w=96&q=75)[Dmitry Pavlov](/authors/dmitry-pavlov)Apr 24, 2025 · 6 minutes read![Blog_IntroducingAgentHouse_202504_FNL.png](/uploads/Blog_Introducing_Agent_House_202504_FNL_0639a4c186.png)
## Introducing AgentHouse [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#introducing-agenthouse)


A few weeks after Anthropic released its [MCP protocol](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) in 2024, the ClickHouse integrations team showed a small internal demo of Anthropic’s Sonnet model accessing a ClickHouse database. It was a very basic integration involving running a simple query against random data and getting a result to the LLM.


As an internal DWH team lead at ClickHouse, once I saw the demo, I immediately wanted to have this in [my Data Warehouse](https://clickhouse.com/blog/building-a-data-warehouse-with-clickhouse). I want my lovely internal users (sales, ops, product, finance, and engineering teams at ClickHouse) to be able to talk to the data instead of using the traditional BI tool or running queries.


Two months later, we launched Dwaine (Data Warehouse AI Natural Expert) \- an internal LLM that helps internal users answer their questions based on data. What is our revenue? What is this customer doing? What problems do our customers face right now? How many visitors do we have on our website, and what is our conversion rate? Dwaine dramatically helped our internal users to get those and other insights. You may have seen my [small personal article in LinkedIn](https://www.linkedin.com/pulse/bi-dead-change-my-mind-dmitry-pavlov-2otae).


After I described this experience, many people reached out to me and asked for a demo. I demonstrated Dwaine to a few friends and partners, but though they were super excited, I felt they could not experience its full potential as they could not talk to Dwaine by themselves because it worked with confidential information.


This is how AgentHouse, available at [llm.clickhouse.com](https://llm.clickhouse.com), was built. But let him introduce himself :) All further text is written by the AgentHouse LLM.


## Hi, I’m AgentHouse! [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#hi-im-agenthouse)


I'm [AgentHouse](https://llm.clickhouse.com) \- a fully interactive demo environment that showcases the powerful combination of ClickHouse's real\-time analytics capabilities with large language models. My name combines "Agent" (representing the LLM agent) and "House" (from ClickHouse), highlighting how these technologies work together seamlessly. Together with other demo environments ([ClickHouse SQL Playground](http://sql.clickhouse.com) and [ADSB visualizer](https://adsb.exposed/)), I allow you to try the ClickHouse Cloud database in different real\-world scenarios without creating an account or uploading any data.


![agenthouse.gif](/uploads/agent_house_v3_7e163b96ca.gif)
### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## What am I made of? [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#what-am-i-made-of)


These are my main body parts:


1. **[Anthropic’s large language model Claude Sonnet](https://www.anthropic.com/claude/sonnet)** \- this LLM is especially good at understanding complex contexts and reasoning about structured data – making it an ideal partner for ClickHouse's analytical prowess. The model's ability to understand database schemas, generate accurate SQL, and interpret query results demonstrates why ClickHouse and advanced LLMs are natural companions.
2. **[LibreChat UI project](https://www.librechat.ai)** \- an open\-source LLM UI that helps you work with popular LLMs out of the box. We selected LibreChat as the user interface because of its open\-source nature, clean design, and growing community support. We would also like to thank the LibreСhat team for their assistance when building this demo.
3. My secret sauce is the **[ClickHouse MCP](https://github.com/ClickHouse/mcp-clickhouse)** (Model Context Protocol) server that the ClickHouse team developed. This specialized server acts as the bridge between ClickHouse databases and large language models, enabling:


- Efficient data transfer between ClickHouse and LLMs
- Intelligent query optimization for LLM\-generated SQL
- Context management for stateful conversations about data
- Secure and controlled access to database resources
- Streamlined handling of various public datasets


4. **[ClickHouse Cloud database](https://clickhouse.com)** \- a fully\-managed cloud service that provides the ClickHouse database as a Software\-as\-a\-Service (SaaS) offering.


![Images_PoweringAIAgentsAnalytics_202504_FNL(1).png](/uploads/Images_Powering_AI_Agents_Analytics_202504_FNL_1_54be5a6747.png)
## Why Sonnet and LibreChat? [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#why-sonnet-and-librechat)


Anthropic's Sonnet model represents a significant advancement in LLM capabilities, particularly in understanding complex contexts and reasoning about structured data – making it an ideal partner for ClickHouse's analytical prowess. The model's ability to understand database schemas, generate accurate SQL and interpret query results demonstrates why ClickHouse and advanced LLMs are natural companions.


I use LibreChat as the user interface because of its open\-source nature, clean design, and growing community support. The interface allows users to have natural conversations about their data and to build visual artifacts (charts, tables, etc), making complex analytical tasks accessible even to those without SQL knowledge.


## My purpose [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#my-purpose)



I was created specifically as a testing ground for users to delve 😉 into how ClickHouse, through our MCP server, can serve as an ideal backend for LLM applications. I have access to multiple public datasets that showcase various use cases, allowing you to explore the possibilities through a simple conversational interface. This includes 37 different datasets, including:



- **github** \- Contains GitHub activity data, repositories, and user interactions. Updated hourly.
- **pypi** \- a row for every Python package downloaded with `pip`, updated daily \- over 1\.3 trillion rows
- **rubygems** \- a row for every gem installed \- updated hourly \- over 180 billion rows
- **hackernews** \- Contains posts and comments from Hacker News
- **imdb**\- Contains movie database information from IMDB
- **nyc\_taxi** \- Contains NYC taxi trip data
- **opensky** \- Contains aviation data from the OpenSky Network
- **reddit** \- Contains posts and comments from Reddit
- **stackoverflow** \- Contains questions and answers from Stack Overflow
- **uk** \- contains a comprehensive collection of UK property transaction data and related geographical information


And others.


## My key features [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#my-key-features)


- Test Natural Language Queries: See how plain English questions transform into optimized SQL queries for ClickHouse via the MCP server
- Experience Real\-Time Analytics: Witness how our MCP server enables ClickHouse's renowned speed to be combined with AI\-powered insights with minimal latency
- Try Interactive Data Exploration: Explore demo datasets through a conversational interface powered by the MCP\-LLM connection
- View Automated Visualizations: See how data flowing through our MCP server can be automatically visualized


## Exploring the Demo [\#](/blog/agenthouse-demo-clickhouse-llm-mcp#exploring-the-demo)


To start with AgentHouse, go to [llm.clickhouse.com](https://llm.clickhouse.com), and log into the demo environment with your Google account and start asking questions. A great way to start is to ask "Which datasets do you have?" \- this will give you a list of databases and you can start exploring them.


I look forward to answering all your questions!

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

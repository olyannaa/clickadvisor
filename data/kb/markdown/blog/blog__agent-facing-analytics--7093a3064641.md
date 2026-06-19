# Agent\-Facing Analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Agent\-Facing Analytics

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Feb 13, 2025 · 19 minutes readYou operate an analytics database, and suddenly you notice a cohort of users that seem to never sleep, never take breaks, and generate SQL queries like there's no tomorrow. You might ask: Are we getting DDoS’d again? The answer is no. It turns out that the company just deployed a fleet of autonomous AI agents that are tasked with monitoring and optimizing some business metrics.


If you’re in charge of a database or someone who designs database systems, that probably sounds both exciting and terrifying at the same time.


AI agents are rapidly evolving, gaining reasoning abilities combined with connectivity to 3rd party systems like real\-time databases. With 2025 already labeled as the “agentic revolution” year, this post explores AI agents at the intersection of real\-time analytics: how agents interact with data, their usage patterns, and what it means for real\-time database design. We’ll take a look at AI agents as a “new user persona” for real\-time databases and explore initial themes about how systems can adapt to their workloads. Finally, we’ll explore an example of a real\-time analytics agentic workflow by demonstrating the ClickHouse MCP Server.



![image (8).png](/uploads/image_8_5d12fd1281.png)
*Google Trends Interest over time for “AI agents” in 2024*



The next section will introduce definitions and background about the recent developments of AI. It will be useful in the rest of the post, but if you are already familiar with AI concepts (and have managed to keep up with the hype!), then I recommend skipping straight to the section [Real\-time analytics for AI agents](/blog/agent-facing-analytics#real-time-analytics-for-ai-agents).


## AI concepts catch\-up [\#](/blog/agent-facing-analytics#ai-concepts-catch-up)


### ELI5: AI Agents and how LLMs enabled the agentic\-era [\#](/blog/agent-facing-analytics#eli5-ai-agents-and-how-llms-enabled-the-agentic-era)


*ELI5 stands for “Explain Like I'm Five”, inspired by the subreddit [r/explainlikeimfive](https://www.reddit.com/r/explainlikeimfive/)*


One can think of AI agents as digital assistants that have evolved beyond simple task execution (or function calling): they can understand context, make decisions, and take meaningful actions toward specific goals. They operate in a "sense\-think\-act" loop (see [ReAct agents](https://www.leewayhertz.com/react-agents-vs-function-calling-agents/)), processing various inputs (text, media, data), analyzing situations, and then doing something useful with that information. Most importantly, depending on the application domain, they can theoretically operate at various levels of autonomy, requiring or not human supervision.


The game changer here has been the advent of Large Language Models (LLMs). While we had the notion of AI agents [for quite a while](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95.pdf), LLMs like the [GPT series](https://www.youtube.com/watch?v=wjZofJX0v4M) have given them a massive upgrade in their ability to “understand” and communicate. It's as if they've suddenly become more fluent in “human” aka. able to grasp requests and respond with relevant contextual information drawn from the model’s training.


### AI agents superpowers: “Tools” [\#](/blog/agent-facing-analytics#ai-agents-superpowers-tools)


These agents can have superpowers through their access to “tools”. Tools enhance AI agents by giving them abilities to perform tasks. Rather than just being conversational interfaces, they can now get things done whether it’s crunching numbers, searching for information, or managing customer communications. Think of it as the difference between having someone who can describe how to solve a problem and someone who can actually solve it.


For example, ChatGPT is now shipped by default with a search tool. This integration with search providers allows the model to pull current information from the web during conversations. This means it can fact\-check responses, access recent events and data, and provide up\-to\-date information rather than relying solely on its training data.



![image (8).png](/uploads/2_agent_analytics_e99802b546.png)
*ChatGPT’s search tool UI*



Tools can also be used to simplify the implementation of Retrieval\-Augmented Generation (RAG) pipelines. Instead of relying only on what an AI model learned during training, RAG lets the model pull in relevant information before formulating a response. Here's an example: Using an AI assistant to help with customer support (e.g. Salesforce [AgentForce](https://www.salesforce.com/agentforce/), [ServiceNow AI Agents](https://www.servicenow.com/products/ai-agents.html)). Without RAG, it would only use its general training to answer questions. But with RAG, when a customer asks about the latest product feature, the system retrieves the most recent documentation, release notes, and historical support tickets before crafting its response. This means that answers are now grounded in the latest information available to the AI model.


### Think before you speak: Reasoning models [\#](/blog/agent-facing-analytics#think-before-you-speak-reasoning-models)


Thinking before speaking sounds like a smart thing to do, doesn't it?


Another development in the AI space, and perhaps one of the most interesting, is the emergence of reasoning models. Systems like [OpenAI o1](https://openai.com/index/learning-to-reason-with-llms/), [Anthropic Claude](https://www.anthropic.com/news/claude-3-family), or [DeepSeek\-R1](https://github.com/deepseek-ai/DeepSeek-R1) take a more methodical approach by introducing a “thinking” step before responding to a prompt. Instead of generating the answer straightaway, reasoning models use prompting techniques like [Chain\-of\-Thought (CoT)](https://openreview.net/pdf?id=_VjQlMeSB_J) to analyze problems from multiple angles, break them down into steps, and use the tools available to them to gather contextual information when needed.


This represents a shift toward more capable systems that can handle more complex tasks through a combination of reasoning and practical tools. One of the latest examples in this area is the introduction of OpenAI’s [deep research](https://openai.com/index/introducing-deep-research/), an agent that can autonomously conduct complex multi\-step research tasks online. lt processes and synthesizes information from various sources, including text, images, and PDFs, to generate comprehensive reports within 5 to 30 minutes, a task that would traditionally take a human several hours.



![image (7).png](/uploads/image_7_da5378760d.png)
*A simplified AI timeline*




> If you need to spend more time on AI definitions, I recommend this great [video](https://www.youtube.com/watch?v=F8NKVhkZZWI) about AI agents from IBM.


## Real\-time analytics for AI agents [\#](/blog/agent-facing-analytics#real-time-analytics-for-ai-agents)


Alright, so it’s 2025 and we have LLM\-powered AI agents that can perform tasks at various degrees of autonomy, and can access external tools to run queries, gather information, or execute actions.


Now let’s take the case of an agentic AI assistant with access to a real\-time analytics database containing the company’s CRM data. When a user asks about the latest (up\-to\-the\-minute) sales trends, the AI assistant queries the connected data source, iteratively analyzes the data to identify meaningful patterns and trends, such as month\-over\-month growth, seasonal variations, or emerging product categories, and generates a natural language response explaining key findings, often with supporting visualizations. When the main interface is chat\-based like in this case, performance matters since these iterative explorations trigger a series of queries that can scan large amounts of data to extract relevant insights.


Some properties make real\-time databases especially suitable for such workloads. For example, real\-time analytics databases are designed to work with near real\-time data, allowing them to process and deliver insights almost immediately as new data arrives. This is crucial for AI agents, as they can require up\-to\-date information to make (or help make) timely and relevant decisions.


The core analytical capabilities are also important. Real\-time analytics databases shine in performing complex aggregations and pattern detection across large datasets. Unlike operational databases focusing primarily on raw data storage or retrieval, these systems are optimized for analyzing vast amounts of information. This makes them particularly well\-suited for AI agents that need to uncover trends, detect anomalies, and derive actionable insights.


Real\-time analytics databases are also expected to deliver fast performance for interactive querying, essential for chat\-based interaction and high\-frequency explorative workloads. They ensure consistent performance even with large data volumes and high query concurrency, enabling responsive dialogues and a smoother user experience.


Finally, real\-time analytics databases often serve as the ultimate “data sinks” effectively consolidating valuable domain\-specific data in a single location. By co\-locating essential data across different sources and formats under the same tent, these databases ensure that AI agents have access to a unified view of the domain information, decoupled from operational systems.


![Agent Facing Analytics Artboard 2.png](/uploads/Agent_Facing_Analytics_Artboard_2_7cfbc8f1df.png)
![Agent Facing Analytics Artboard 1.png](/uploads/Agent_Facing_Analytics_Artboard_1_0a19dfc171.png)
These properties already empower real\-time databases to play a vital role in serving AI data retrieval use cases at scale (e.g. [OpenAI’s acquisition of Rockset](https://openai.com/index/openai-acquires-rockset)). They can also enable AI agents to provide fast data\-driven responses while offloading the heavy computational work.


It positions the real\-time analytics database as a preferred “context provider” for AI agents when it comes to insights, but one question remains: are the real\-time analytics databases ready to deliver this value in their current form?


## AI agents as an emerging user persona [\#](/blog/agent-facing-analytics#ai-agents-as-an-emerging-user-persona)


The best way I have found to think about AI agents leveraging real\-time analytics databases is to perceive them as a new category of users, or in product manager speak: a user persona.



![image (7).png](/uploads/Agent_Facing_Analytics_Feb_2025_Chat_6faacd34f5.png)
*A fictional agentic AI assistant user persona card*



Think about it a moment from the database perspective, we can expect a potentially uncapped number of AI agents, concurrently running a large number of queries on behalf of users, or in autonomy, to perform investigations, refine iterative research and insights, and execute tasks.


Over the years, real\-time databases have had the time to adapt to human interactive users, directly connected to the system or via a middleware application layer. Classic personas examples include database administrators, business analysts, data scientists, or software developers building applications on top of the database. The industry has progressively learned their usage patterns and requirements and organically, provided the interfaces, the operators, the UIs, the formats, the clients, and the performance to satisfy their various use cases.


The question now becomes, *are we ready to accommodate the AI agent's workloads? What specific features do we need to re\-think or create from scratch for these usage patterns?*


It feels early to answer these questions but we already can hint towards some directions (note that this exercise will probably raise more questions than provide answers at this stage):


#### Optimizing SQL for agent interactions [\#](/blog/agent-facing-analytics#optimizing-sql-for-agent-interactions)


SQL is a widely used language that most LLMs can generate easily, thanks to the availability of training data. Modern reasoning models are increasingly good at crafting SQL queries, often working iteratively through trial and error. But here is the question: can we improve the quality of the SQL generation by providing specific features? More importantly, how do we ensure the correctness of key metrics definitions, especially in critical queries (e.g. computing financial results)? One approach could be combining the free\-form SQL access with templated [query API endpoints](https://clickhouse.com/blog/automatic-query-endpoints), offering clear definitions to better control workflows. Another option could be the introduction of specific SQL language extensions: new operators and formats specifically designed for LLM’s use.


#### Improved discoverability [\#](/blog/agent-facing-analytics#improved-discoverability)


An example of a useful SQL extension can be for data discoverability. AI agent tasks tend to begin by describing the available datasets through `DESCRIBE` and `SHOW` queries, often followed by selecting data samples and descriptive aggregates. These queries usually help humans understand the structure and properties of the data. However, there’s room to improve this process by creating similar operators tailored for LLMs, allowing them to annotate dataset descriptions with data properties. Think of it like a server\-side version of [`pandas.describe()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html) designed specifically for agents.


#### LLM\-friendly documentation [\#](/blog/agent-facing-analytics#llm-friendly-documentation)


Documentation for real\-time analytics databases is typically structured for human users. To improve how AI agents interact with this documentation, we could enhance its accessibility for LLMs. One promising and [growing](https://directory.llmstxt.cloud/) approach is the use of a standardized format like [LLMs.txt](https://llmstxt.org/), which would present the documentation in a machine\-readable form. This makes it easier for AI agents to understand and use documentation, ensuring more effective interactions with the data.


#### Scaling real\-time analytics for AI workloads [\#](/blog/agent-facing-analytics#scaling-real-time-analytics-for-ai-workloads)


Just like traditional interactive users, AI agents require fast response times for concurrent tasks. The difference here is that each AI prompt can trigger multiple exploratory and aggregation queries in short time spans. With organizations deploying AI agents at a rapid pace, real\-time analytics systems could face specific scalability challenges. The solution isn’t very specific in this case: [efficient](https://benchmark.clickhouse.com/) real\-time databases capable of supporting high\-throughput and exploratory workloads without compromising performance.


#### A server\-side state for AI Memory [\#](/blog/agent-facing-analytics#a-server-side-state-for-ai-memory)


AI systems can retain and recall information over time which can help them make better decisions, personalize responses, or improve performance based on past interactions. This is often referred to as “AI memory”.


In the database, we can envision server\-side features to support maintaining a state for the agents, the same way interactive users can maintain sessions with their settings and preferences preserved. This can be extended to various cache levels if recurring queries are submitted (especially relevant for data discovery queries) and will require reliable ways to identify agent users and the scope of their tasks.


#### Customized access control models and mechanisms [\#](/blog/agent-facing-analytics#customized-access-control-models-and-mechanisms)


Databases use Role\-Based Access Control (RBAC) models to manage user permissions according to roles assigned to users, ensuring secure access to data. Similarly, the API landscape has evolved to support short\-lived API tokens, which offer temporary access to specific resources, minimizing the risk of unauthorized access. There may be lessons to be learned from the API world to enhance secure access for AI agents, such as using short\-lived tokens that align with the duration of an AI agent’s task.



> "Our vision is bold: to help customers scale their workforces and augment their employees with one billion Agentforce agents by the end of 2025"  
> 
> Marc Benioff, CEO of Salesforce, about [AgentForce, Salesforce’s Agentic Offering](https://www.salesforce.com/news/stories/agentforce-launch-zone-announcement/)


Please note that the list above is not a roadmap and is not intended to be exhaustive. It only serves as a brainstorming exercise. With growing usage and new use cases, the industry is only beginning to explore the many ways to better serve the AI agent user persona.


So the answer to the initial question: are the real\-time analytics databases ready to deliver AI agents value in their current form? **The answer is yes** (and we’ll demo it in the next section), but as with any emerging use case, there are many opportunities for iterative improvements.


## A real\-world application: The ClickHouse MCP server [\#](/blog/agent-facing-analytics#a-real-world-application-the-clickhouse-mcp-server)


In November 2024, Anthropic [announced](https://www.anthropic.com/news/model-context-protocol) the Model Context Protocol (MCP), an [open standard](https://github.com/modelcontextprotocol) designed to facilitate connections between AI\-powered applications and data sources. With a simple architecture, developers can expose their data through MCP servers or build AI applications (MCP clients) that connect to these servers. [Example MCP servers](https://modelcontextprotocol.io/examples) include databases, file systems, development tools, web automation APIs, and productivity tools.


We recently released an official [ClickHouse MCP server](https://github.com/ClickHouse/mcp-clickhouse/) that can bridge between AI models and a ClickHouse instance. It exposes 3 simple tools that enable the LLMs to list databases on the ClickHouse instance connected, list tables, and most importantly run select queries.


![6_agent-analytics.png](/uploads/6_agent_analytics_3b1e88363c.png)
With MCP, we now have a standardized way to connect LLMs with the context they need during a specific task. The short video below shows a live demo of its capabilities against the ClickHouse Cloud [public playground](https://sql.clickhouse.com/) service, using Anthropic’s model Claude Sonnet 3\.5\.



  

Our first question triggers the model to get familiar with the datasets. Claude runs the `list_tables` tool on two databases: Forex and Stock then requests data samples by running select queries (note that the previous prompt asked about all available datasets).


![7_agent-analytics.png](/uploads/7_agent_analytics_329cb2753c.png)
Later, we asked about the tech stocks that were hit the worst by the dot com bubble. Note that the question was purposefully vague with no specific dates or field names mentioned, however, the model still managed to understand the scope of the query, propose a relevant methodology, a metric, and a time range, and run the analysis requested. It is interesting to compare the duration of this task to the time needed for an analyst to produce a similar result.



![image (7).png](/uploads/8_agent_analytics_6f4227459e.png)
*Iterative exploration of the data by Claude*



The prompts we submitted for this investigation resulted in a total of 10 SQL queries to the database. The result is a set of insights extracted from raw data, in a few seconds, with supporting visualization and descriptive analysis.


![9_agent-analytics.png](/uploads/9_agent_analytics_1d451ffde6.png)
![10_agent-analytics.png](/uploads/10_agent_analytics_fa7a7e685d.png)
Even if exciting, this approach has known limitations and isn’t a silver bullet. While grounding responses in real\-time data helps, AI agents are not immune to hallucinations: situations where the model generates incorrect information with high confidence. Ensuring data integrity (e.g. with templated queries), setting sensible default settings (e.g. [temperature](https://www.ibm.com/think/topics/llm-temperature)), and implementing safeguards to verify AI\-generated outputs are crucial steps required for minimizing this risk.


### Run it on your laptop! [\#](/blog/agent-facing-analytics#run-it-on-your-laptop)


The best way to grasp this use case is to try it yourself. You’ll find details about how to connect to the ClickHouse public playground service in our [documentation](https://clickhouse.com/docs/en/getting-started/playground). The setup of the ClickHouse MCP Server with Claude desktop is also described in its [README](https://github.com/ClickHouse/mcp-clickhouse/blob/main/README.md) file. Finally, you can also set up a local offline version with an alternative, tools\-compatible model. We experimented with a local setup using the following components:


- Model: [llama3\.2 3B](https://ollama.com/library/llama3.2) running on Ollama
- Client: [mcp\-cli](https://github.com/chrishayuk/mcp-cli)


While the local version prioritizes privacy through local data processing (and is not rate\-limited!), the smaller model size combined with limited reasoning capabilities makes it less suitable for exploratory analysis. It works better with direct questions that hint at the tables and fields needed to answer and will hit dead\-ends faster. But there’s hope, the availability of open\-source reasoning models like DeepSeek R1 is expected to unlock more of these capabilities (at the time of writing, [DeepSeek R1](https://github.com/deepseek-ai/DeepSeek-R1/issues/9) doesn't support tools invocation).



![image (7).png](/uploads/11_agent_analytics_5e3734a62c.png)
*Local deployment of llama3\.2 with the ClickHouse MCP server*



## Conclusion [\#](/blog/agent-facing-analytics#conclusion)


The emergence of AI agents as active users of real\-time analytics databases marks an interesting shift in how we think about data systems. While we're still in the early stages, the foundations are already taking shape through developments like the Model Context Protocol and a growing ecosystem of AI\-powered analytics tools.


The journey from simple query executors and “function callers” to agents that can reason about data, maintain context, and drive insights represents both an opportunity and a challenge for the real\-time database. As these agents become more autonomous and their deployment more widespread, we'll likely see new patterns in how they interact with data systems, leading to new optimizations and features.


While we've explored some potential directions for how real\-time analytics databases might evolve to better the use case, we're still at the beginning of understanding the full impact and as organizations continue to deploy AI agents at scale and new use cases emerge, the relationship between agents and real\-time databases will probably continue to evolve in ways we haven't yet anticipated.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

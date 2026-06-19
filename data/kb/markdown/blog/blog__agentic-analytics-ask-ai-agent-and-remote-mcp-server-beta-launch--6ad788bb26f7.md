# One step closer to Agentic Analytics: Ask AI agent \& Remote MCP server beta launch


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# One step closer to Agentic Analytics: Ask AI agent \& Remote MCP server beta launch

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Sep 25, 2025 · 5 minutes readWe've been talking about [agent\-facing analytics](https://clickhouse.com/blog/agent-facing-analytics) for a while now. The idea is that AI agents would become primary consumers of analytics databases, running queries at machine speed and generating insights semi\-autonomously. Well, today we're making that future more accessible by announcing the public beta release of two flagship features: the ClickHouse Ask AI agent and the remote MCP server for ClickHouse Cloud.


## The “Ask AI” agent in ClickHouse Cloud [\#](/blog/agentic-analytics-ask-ai-agent-and-remote-mcp-server-beta-launch#the-ask-ai-agent-in-clickhouse-cloud)


The “Ask AI” agent is a turn\-key experience that allows users to trigger complex analysis tasks on top of the data hosted in their ClickHouse Cloud service. Instead of writing SQL or navigating dashboards, users can describe what they are looking for in natural language. The assistant responds with generated queries, visualizations, or summaries, and can incorporate context like active tabs, saved queries, schema details, and dashboards to improve accuracy. It’s designed to work as an embedded assistant, helping users move quickly from questions to insights, and from prompts to working dashboards or APIs.


![ask_ai.gif](/uploads/ask_ai_d57107b308.gif)
The experience also embeds a "Docs AI" sub\-agent that can be used to ask specific questions about the ClickHouse documentation straight from the console. Instead of searching through hundreds of pages, users can ask direct questions like "How do I configure materialized views?" or "What's the difference between ReplacingMergeTree and AggregatingMergeTree?" and receive precise answers with relevant code examples and links to source documentation.


![image 2 unnamed.png](/uploads/image_2_unnamed_c7b0c3ac51.png)
## Remote MCP Server Integration [\#](/blog/agentic-analytics-ask-ai-agent-and-remote-mcp-server-beta-launch#remote-mcp-server-integration)


Not all users interact with ClickHouse through the Cloud console, however. For example, many developers work directly from their preferred code editors, CLI agents, or connect to the database via custom setups, while others rely on general\-purpose AI assistants such as Anthropic Claude for most of their explorations. These users, and the agentic workloads acting on their behalf, need a way to securely access and query ClickHouse Cloud without complex setups or custom infrastructure.


![image 3.png](/uploads/image_3_936c8d05a0.png)
### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
The new remote MCP server capability in ClickHouse Cloud addresses this by exposing a standard interface that external agents can use to retrieve analytical context. MCP, or [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro), is a standard for structured data access by AI applications powered by LLMs. With this integration, external agents can list databases and tables, inspect schemas, and run scoped, read\-only SELECT queries. Authentication is handled via OAuth, and the server is fully managed on ClickHouse Cloud, so no setup or maintenance is required.


This makes it easier for agentic tools to plug into ClickHouse and retrieve the data they need, whether for analysis, summarization, code generation, or exploration.


![mcp_cursor.gif](/uploads/mcp_cursor_125691e256.gif)
Note that we also provide a “traditional” MCP Server for ClickHouse, which can be used in self\-managed setups and installed via PyPI. At the time of writing, it has been downloaded more [than 220k times](https://clickpy.clickhouse.com/dashboard/mcp-clickhouse).


[https://github.com/ClickHouse/mcp\-clickhouse](https://github.com/ClickHouse/mcp-clickhouse)


## Reducing Time to Insight [\#](/blog/agentic-analytics-ask-ai-agent-and-remote-mcp-server-beta-launch#reducing-time-to-insight)


Features like Ask AI and a remote MCP server directly influence the velocity at which insights can be extracted from data. Traditional analytics workflows often involve multiple handoffs between data engineers writing queries, analysts building dashboards, and business users interpreting results. Each step introduces latency measured in hours or days.   

  

With these agentic capabilities, that timeline collapses to seconds or minutes. A product manager can ask "What's driving the spike in churn last week?" and immediately receive not just the answer, but the underlying query, a visualization, and potential next questions to explore.


This is closely aligned with our own experience at Clickhouse. Six months ago, we introduced Dwaine (Data Warehouse AI Natural Expert): an internal agent that enables our team to query business data through natural language. Since then, questions like "What's our current revenue?", "How is this customer using our product?", "What issues are customers experiencing?" or "What's our website traffic and conversion rate?" are getting instant answers. Dwaine has transformed how our internal teams access insights, eliminating the bottleneck of SQL queries and data requests. The adoption quickly followed, for instance, ClickHouse internal users generated more than 15 million LLM tokens in a single day on Dwaine, roughly 1 month after its rollout.


![image 5 .png](/uploads/image_5_9cbcd1cc6f.png)
*The first 3 months of DWAINE \- Token Counts per Day*


If you want to experience what it looks like, we recommend visiting [llm.clickhouse.com](http://llm.clickhouse.com), our public demonstration agent code\-named [AgentHouse](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp), which exposes publicly available datasets via an agentic interface.


Finally, while grounding responses in real\-time data helps, AI agents are not immune to hallucinations: situations where the model generates incorrect information with high confidence. Our own experience running internal agents within ClickHouse taught us that the best remediation comes from providing the LLMs with the maximum and most accurate context possible. This can be achieved by commenting the tables using the SQL [COMMENT](https://clickhouse.com/docs/sql-reference/statements/alter/column#comment-column) syntax for example, or by providing more context in\-line, in the chat, or part of the system prompt of an LLM session.


## Conclusion [\#](/blog/agentic-analytics-ask-ai-agent-and-remote-mcp-server-beta-launch#conclusion)


The beta release of Ask AI and remote MCP server represents a step toward our vision of the agentic analytics experience. By making ClickHouse natively accessible to both interactive users through natural language and third\-party agents through MCP, we're aiming at reducing the friction that has traditionally separated questions from answers. You can read more about these features in our documentation: [Ask AI](https://clickhouse.com/docs/use-cases/AI_ML/AIChat), [Remote MCP server](https://clickhouse.com/docs/use-cases/AI/MCP/remote_mcp).   

  

As always, when we release Beta features, we’d love to receive your feedback and remarks, as it’s the only way to improve! You can contact us using this [form](https://clickhouse.com/company/contact) or via our [community Slack](https://clickhouse.com/slack).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

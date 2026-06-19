# ClickHouse Cloud joins the new AWS Marketplace “AI Agents and Tools” category with a remote MCP server for a turn\-key AI\-to\-data connectivity


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud joins the new AWS Marketplace “AI Agents and Tools” category with a remote MCP server for a turn\-key AI\-to\-data connectivity

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 16, 2025 · 5 minutes readBuilding AI agents and applications that can process and analyze data in real\-time requires access to high\-performance analytics.


Today, we're excited to announce that ClickHouse Cloud is now available in the new [“AI Agents and Tools”](https://aws.amazon.com/marketplace/pp/prodview-jettukeanwrfc) category in the AWS Marketplace, making it easier than ever for developers to integrate lightning\-fast analytics into their AI\-powered applications and workflows. This milestone is made possible thanks to the availability (in private preview at the time of writing) of our new remote Model Context Protocol server feature that simplifies how AI agents and applications connect to data in ClickHouse Cloud.


## Introducing the remote MCP Server in ClickHouse Cloud [\#](/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp#introducing-the-remote-mcp-server-in-clickhouse-cloud)


The Model Context Protocol (MCP) simplifies how AI agents and applications interact with data. ClickHouse Cloud’s Remote MCP Server provides a secure, managed bridge between analytical data and any MCP\-compatible client. No infrastructure to deploy, no servers to maintain, just instant connectivity between your data and the AI tools your team already uses.


![mcpwas1.png](/uploads/mcpwas1_e9e56e43f5.png)
### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Key Benefits [\#](/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp#key-benefits)


**Turn\-key MCP Integration**  

Built directly into ClickHouse Cloud, this managed service eliminates the complexity of exposing data to AI agents. Teams no longer need to create custom integrations, manage authentication systems, or worry about infrastructure scaling.


**OAuth authentication**  

Ensures secure access to your data from external AI applications. The remote MCP Server capability is built on top of the existing ClickHouse Cloud Query API Endpoints and fine\-grained access control model.


**Compatible with Your Favorite MCP\-compatible AI Tools**  

Whether you use a chat\-based interface like Claude, ChatGPT, an AI IDE like Cursor or Windsurf, or custom AI agents deployed within your infrastructure.


## How to Get Started [\#](/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp#how-to-get-started)



> The ClickHouse Cloud Remote MCP server is in private preview. Join the waitlist by filling out the form at [clickhouse.ai](http://clickhouse.ai)


- **Enable the remote MCP Server** → Built into your ClickHouse Cloud service (only for service admins)
- **Connect Your MCP Client** → Add the MCP server URL to your client configuration
- **Authenticate** → Secure OAuth flow for client authorization
- **Query** → Use natural language to analyze your data


You’ll find a complete tutorial using Claude Code as an MCP client in [our documentation](https://clickhouse.com/docs/use-cases/AI/MCP/remote_mcp).


![mcp_cursor.gif](/uploads/mcp_cursor_be77949483.gif)
## Our journey with agentic analytics [\#](/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp#our-journey-with-agentic-analytics)


Back in February, we wrote about how [agentic access to real\-time data](https://clickhouse.com/blog/agent-facing-analytics) can unlock many use\-cases, including:


- Intelligent dashboards where users can ask questions in natural language
- Enhanced monitoring of metrics and alerts on anomalies
- AI\-powered IDEs that can query production data to inform development decisions
- Customer service agents with real\-time access to user data


At ClickHouse, we have been running our internal agentic product analytics use\-cases for months, powered by Amazon Bedrock and the [ClickHouse MCP server](https://github.com/ClickHouse/mcp-clickhouse). Its rapid adoption revealed the power of conversational data interfaces, allowing us to experience first\-hand the game\-changing paradigm it introduces when associated with real\-time data. To make sure everyone has a chance to experience it, we also released a [public demonstration](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) on top of the ClickHouse playground service at: [llm.clickhouse.com](http://llm.clickhouse.com)


Now with the remote MCP server for ClickHouse Cloud, it is easier than ever to experience conversational data exploration against real\-time data with minimal setup.


## Security and MCP [\#](/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp#security-and-mcp)


Ensuring the security of the remote MCP server was paramount in its design and implementation. Like all other ClickHouse Cloud services, the remote MCP server has undergone a stringent internal security process to guarantee its security.


**OAuth\-based authorization**  

The remote MCP server uses the OAuth protocol to ensure that the permissions are properly checked on a user level; after registration and authentication, the identity used by the MCP server is only able to act on behalf of the user. This decision limits the MCP server to what the user can interact with directly in Clickhouse Cloud and ensures that no accidental privilege escalation can take place. Existing permissions in a ClickHouse Cloud service will therefore apply to the MCP server.


**Disabled by default, and read\-only by design**  

The remote MCP Server feature is disabled by default for ClickHouse Cloud services; it can be enabled via the Connect menu. We also took the conscious decision to limit the MCP server capabilities to read\-only operations. With an expanding attack surface through [prompt injections](https://www.ibm.com/think/topics/prompt-injection) and the LLM behavior landscape ever evolving, the risk of a prompt injection triggering destructive actions exists.


![mcpaws2.png](/uploads/mcpaws2_0bf21e253b.png)
## Get started today [\#](/blog/clickhouse-cloud-joins-aws-ai-agents-and-tools-mcp#get-started-today)


Ready to give your AI agents and applications direct access to lightning\-fast analytics? Here's how to begin:


1. Join the waitlist by filling out the form at [clickhouse.ai](http://clickhouse.ai)
2. Connect to your ClickHouse service or find ClickHouse Cloud in the [AWS Marketplace AI Agents category](http://aws.amazon.com/marketplace/solutions/ai-agents-and-tools/)
3. Check out our [Remote MCP Server documentation](https://clickhouse.com/docs/use-cases/AI/MCP/remote_mcp) for setup guides


The combination of a lightning\-fast database and a Remote MCP Server creates new possibilities for AI\-powered analytics. We can't wait to see what you build!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

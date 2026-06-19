# Agentic analytics in Slack with ClickHouse, MCP, and PydanticAI


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Agentic analytics in Slack with ClickHouse, MCP, and PydanticAI

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)Jul 23, 2025 · 10 minutes readWe're often asked, "Can I use ClickHouse for BI?", and the answer is "Yes!", but perhaps we should be looking a bit differently at BI in 2025?


In the past, we’ve relied on BI tools to let analysts build charts and place them on a dashboard. This typically means a multi\-step process:


1. personA thinks of a question
2. personA asks analystA to answer the question
3. analystA spends a while figuring out what personA **actually** means
4. analystA spends time figuring out the right tables and columns
5. analystA shows personA the chart
6. personA realises it's not what they want, go back to step 3
7. personB thinks of a question…


And that’s assuming we're not bottle\-necked behind a ticket queue longer than you'd find outside "The world's largest concrete garden gnome" (it's real, thanks Iowa.)


So, let’s try something different; let's build a self\-service analytics agent that we can talk to directly in Slack, that transparently queries our ClickHouse data warehouse.


## What we’re building [\#](/blog/agentic-analytics-slack-clickhouse-mcp#what-were-building)


We’re going to build a Slack bot that can be added to a channel, or messaged privately. The Slack bot will be connected to a ClickHouse data warehouse via the [ClickHouse MCP server](https://github.com/ClickHouse/mcp-clickhouse).


We’ll use [PydanticAI](https://ai.pydantic.dev/) to integrate the Slack bot with the Anthropic API to process natural language, invoke MCP tools and generate SQL queries.


Via MCP, the bot will send the SQL queries to ClickHouse, and the LLM will interpret the result. We’ll return a natural language response to the original question in Slack.


The diagram below shows a high level view of the flow, but note that there could be multiple back\-and\-forth interactions between the bot, LLM and ClickHouse.


You can find the [full code for this example on GitHub](https://dub.sh/EsZMXl7).


![466107429-3fbca03a-7659-4e81-933b-5b709e79357a.png](/uploads/466107429_3fbca03a_7659_4e81_933b_5b709e79357a_d9c40c688f.png)
### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## 1\. Setting Up Your Slack Bot [\#](/blog/agentic-analytics-slack-clickhouse-mcp#1-setting-up-your-slack-bot)


We’re running the bot locally and using Slack’s “Socket Mode” to receive events as this is much easier to get started \- if you were to deploy this for real usage, you’d probably want to switch to “HTTP mode”.


**a. Create a Slack App**


Go to <https://api.slack.com/apps> and click "**Create New App**". Then, choose "**From scratch**" and give your app a name. You'll be prompted to select your Slack workspace.


**b. Install the app to your workspace**


**c. Configure Slack App Settings**


Go to **App Home** , then under "Show Tabs" → "Messages Tab" enable **Allow users to send Slash commands and messages from the messages tab** .


Then, go to **Socket Mode** and enable **Socket Mode**. Note down the **Socket Mode Handler** for the environment variable `SLACK_APP_TOKEN`


Go to **OAuth \& Permissions** and add the following **Bot Token Scopes**:  

\* `app_mentions:read`  

\* `assistant:write`  

\* `chat:write`  

\* `im:history`  

\* `im:read`  

\* `im:write`  

\* `channels:history`


Now install the app to your workspace and note down the **Bot User OAuth Token** for the environment variable `SLACK_BOT_TOKEN`.


Finally, go to **Event Subscriptions** and enable **Events**. Then, under **Subscribe to bot events**, add:  

\* `app_mention`  

\* `assistant_thread_started`  

\* `message:im`


**d. Add the bot to a channel in your workspace.**


## 2\. Configuring and loading EnvVars [\#](/blog/agentic-analytics-slack-clickhouse-mcp#2-configuring-and-loading-envvars)


We need to configure some variables that we’ll use in our code. In a `.env` file, add the following template.


Update the `SLACK_BOT_TOKEN` and `​​SLACK_APP_TOKEN` with the values noted when creating the Slack bot. Update the `ANTHROPIC_API_KEY` with your own Anthropic API key.


You can customise the ClickHouse settings to use your own instance, or leave them as\-is to connect to the public [sql.clickhouse.com](http://sql.clickhouse.com) playground which has 35\+ datasets ready to go. You’re welcome to use it for testing!



```
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
ANTHROPIC_API_KEY=
CLICKHOUSE_HOST="sql-clickhouse.clickhouse.com"
CLICKHOUSE_PORT="8443"
CLICKHOUSE_USER="demo"
CLICKHOUSE_PASSWORD=""
CLICKHOUSE_SECURE="true"

```

In our Python script, we need to load the configured variables:



```
load_dotenv()

# --- CONFIGURATION ---
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "xoxb-your-token")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "xapp-your-app-token")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-ant-xxx")

# ClickHouse MCP env
CLICKHOUSE_ENV = {
    "CLICKHOUSE_HOST": os.environ.get("CLICKHOUSE_HOST", "sql-clickhouse.clickhouse.com"),
    "CLICKHOUSE_PORT": os.environ.get("CLICKHOUSE_PORT", "8443"),
    "CLICKHOUSE_USER": os.environ.get("CLICKHOUSE_USER", "demo"),
    "CLICKHOUSE_PASSWORD": os.environ.get("CLICKHOUSE_PASSWORD", ""),
    "CLICKHOUSE_SECURE": os.environ.get("CLICKHOUSE_SECURE", "true"),
}

```

## 2\. Configuring PydanticAI to use mcp\-clickhouse [\#](/blog/agentic-analytics-slack-clickhouse-mcp#2-configuring-pydanticai-to-use-mcp-clickhouse)


We use the `MCPServerStdio` class from PydanticAI to configure our ClickHouse MCP server. This lets us run the MCP server as needed in response to a request, rather than leaving a process running. That can introduce a bit of latency, but makes it easier to manage. In the future, [ClickHouse Cloud will provide a remote MCP server](https://clickhouse.com/ai) than can be connected to without this step.


We then configure the `Agent`, which controls which model to use, adds the MCP server and allows us to inject a system prompt. You can customize the system prompt to tailor the agent’s behaviour to your needs, but the prompt below is a good place to start.



```
mcp_server = MCPServerStdio(
    'uv',
    args=[
        'run',
        '--with', 'mcp-clickhouse',
        '--python', '3.13',
        'mcp-clickhouse'
    ],
    env=CLICKHOUSE_ENV
)

agent = Agent(
    "anthropic:claude-sonnet-4-0",
    mcp_servers=[mcp_server],
    system_prompt="You are a data assistant. You have access to a ClickHouse database from which you can answer the user's questions. You have tools available to you that let you explore the database, e.g. to list available databases, tables, etc., and to execute SQL queries against them. Use these tools to answer the user's questions. You must always answer the user's questions by using the available tools. If the database cannot help you, say so. You must include a summary of how you came to your answer: e.g. which data you used and how you queried it."
)

```

## 3\. Configuring message handling [\#](/blog/agentic-analytics-slack-clickhouse-mcp#3-configuring-message-handling)


Next we need to initialize the Slack bot and create handlers that deal with messages arriving.


We’re listening for `message` (direct messages) and `app_mention` (when you @ the bot in a channel) events. In both cases, we’re pushing the message to the same function with the main logic for our agentic flow.



```
app = AsyncApp(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
async def handle_app_mention(event, say):
    await handle_slack_query(event, say)

@app.event("message")
async def handle_dm(event, say):
    if event.get("channel_type") == "im":
        await handle_slack_query(event, say)

async def main():
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

## 4\. Working on the message [\#](/blog/agentic-analytics-slack-clickhouse-mcp#4-working-on-the-message)


Finally, we need to let our agent fly. We send an immediate response to the user saying so they know something is happening. Then, if needed, we collect messages from the current chat thread as context (so the LLM knows about previous messages).


The new question (and any context) is sent as a prompt, and the PydanticAI `Agent` we configured does all the magic to handle the back\-and\-forth communication with the LLM. If the LLM wants to interact with ClickHouse, it uses the MCP tools from the mcp\-clickhouse server we configured.



```
async def handle_slack_query(event, say):
    user = event["user"]
    text = event.get("text", "")
    thread_ts = event.get("thread_ts") or event["ts"]
    channel = event["channel"]

    await say(text=f"<@{user}>: Let me think...", thread_ts=thread_ts)

    async def do_agent():
        # Build context from thread if present
        context = ""
        if thread_ts and thread_ts != event["ts"]:
            client = AsyncWebClient(token=SLACK_BOT_TOKEN)
            replies = await client.conversations_replies(channel=channel, ts=thread_ts)
            # Exclude the current message, and bot messages
            messages = [m for m in replies["messages"] if m["ts"] != event["ts"]]
            # Format as "user: message"
            context_lines = []
            for m in messages:
                uname = m.get("user", "bot")
                msg = m.get("text", "")
                context_lines.append(f"{uname}: {msg}")
            context = "n".join(context_lines)

        # Compose prompt for the agent
        if context:
            prompt = f"Thread context so far:n{context}nnNew question: {text}"
        else:
            prompt = text

        async with agent.run_mcp_servers():
            result = await agent.run(prompt)
            await say(text=f"{result.output}", thread_ts=thread_ts)

    asyncio.create_task(do_agent())

```

## 5\. Running \& testing [\#](/blog/agentic-analytics-slack-clickhouse-mcp#5-running--testing)


We can run the example locally using `uv`:



```
uv run [main.py](http://main.py)

INFO:slack_bolt.AsyncApp:A new session (s_xxxx) has been established  
INFO:slack_bolt.AsyncApp:⚡️ Bolt app is running!  

```

In Slack, we can now ask our bot questions:  

![mcp_slack_bot.gif](/uploads/mcp_slack_bot_81aa68071a.gif)


In your terminal, you should see output like the following. If you read through the output, you can understand how the LLM is interacting with MCP and ClickHouse. We can see that the LLM first lists the available tools, then uses those tools to interact with ClickHouse \- listing databases, tables and finally sending a SQL query.



```
[07/09/25 13:24:46] INFO     Starting MCP server 'mcp-clickhouse' with transport 'stdio'                                                                                                    server.py:1352  
2025-07-09 13:24:46,428 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest  
INFO:httpx:HTTP Request: POST https://api.anthropic.com/v1/messages?beta=true "HTTP/1.1 200 OK"  
2025-07-09 13:24:48,683 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest  
2025-07-09 13:24:48,684 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest  
2025-07-09 13:24:48,686 - mcp-clickhouse - INFO - Listing all databases  
2025-07-09 13:24:48,686 - mcp-clickhouse - INFO - Creating ClickHouse client connection to sql-clickhouse.clickhouse.com:8443 as demo (secure=True, verify=True, connect_timeout=30s, send_receive_timeout=300s)  
2025-07-09 13:24:49,282 - mcp-clickhouse - INFO - Successfully connected to ClickHouse server version 25.6.2.5432  
2025-07-09 13:24:49,434 - mcp-clickhouse - INFO - Found 37 databases  
2025-07-09 13:24:49,435 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest  
INFO:httpx:HTTP Request: POST https://api.anthropic.com/v1/messages?beta=true "HTTP/1.1 200 OK"  
2025-07-09 13:24:51,587 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest  
2025-07-09 13:24:51,588 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest  
2025-07-09 13:24:51,589 - mcp-clickhouse - INFO - Listing tables in database 'github'  
2025-07-09 13:24:51,589 - mcp-clickhouse - INFO - Creating ClickHouse client connection to sql-clickhouse.clickhouse.com:8443 as demo (secure=True, verify=True, connect_timeout=30s, send_receive_timeout=300s)  
2025-07-09 13:24:51,965 - mcp-clickhouse - INFO - Successfully connected to ClickHouse server version 25.6.2.5432  
2025-07-09 13:24:54,143 - mcp-clickhouse - INFO - Found 19 tables  
2025-07-09 13:24:54,145 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest  
INFO:httpx:HTTP Request: POST https://api.anthropic.com/v1/messages?beta=true "HTTP/1.1 200 OK"  
2025-07-09 13:25:00,234 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest  
2025-07-09 13:25:00,235 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest  
2025-07-09 13:25:00,236 - mcp-clickhouse - INFO - Executing SELECT query: SELECT repo_name, COUNT(*) as contributor_count   
FROM github.actors_per_repo   
WHERE repo_name LIKE '%ClickHouse%' OR repo_name LIKE '%clickhouse%'  
GROUP BY repo_name   
ORDER BY contributor_count DESC  
LIMIT 10  

```

## Conclusion [\#](/blog/agentic-analytics-slack-clickhouse-mcp#conclusion)


Creating a Slack bot that can process natural language questions and execute them as queries over a ClickHouse data warehouse is surprisingly simple! This post covers a basic example that has enormous room for improvement and expansion; the bot could be extended to produce images from query results, save or share analytics work in external systems, and Slack is adding new ways to support agents in their interface which improve the experience.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

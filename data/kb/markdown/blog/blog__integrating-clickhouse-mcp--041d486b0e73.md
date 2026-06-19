# Integrating with ClickHouse MCP


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Integrating with ClickHouse MCP

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Al Brown](/authors/al-brown) and [Mark Needham](/authors/mark-needham)Jun 5, 2025 · 9 minutes read[MCP](https://www.anthropic.com/news/model-context-protocol) is a protocol for connecting third\-party services \- databases, APIs, tools, etc. \- to LLMs. Creating an MCP server defines how a client can interact with your service. An MCP client (like Claude Desktop, ChatGPT, Cursor, Windsurf, and more) connects to the server, and allows an LLM to interact with your service. MCP is quickly becoming the de\-facto protocol, and we published the ClickHouse MCP server earlier in the year: [mcp\-clickhouse](https://github.com/ClickHouse/mcp-clickhouse).



  

Natural language interfaces are becoming popular across pretty much all domains, including the spaces where we find ClickHouse users. Software engineers, data engineers, analytics engineers, you name it. We're all starting to adopt natural language and agentic interfaces for parts of the job. It's making it easier than ever to work with data, whether you're comfortable with SQL or not. What we're seeing is that LLMs are helping to round out and expand people's skills \- software engineers can do more with data, data engineers can do more with software, etc. There's never been a time when a wider audience could work with data.


Universally across these users, domains, and interfaces is the expectation of speed and interactivity in the user experience. Users aren't firing off a query on Friday afternoon, grabbing a delicious Bánh mì on the way home, and picking up a report on Monday morning. They're having a collaborative, interactive conversation with an LLM, where responses are delivered in seconds, and there is a real back\-and\-forth. If we add third\-party services into the mix, we can't disrupt the user experience. If a user wants to query their database this way, it needs to handle this kind of responsiveness.


That's what makes ClickHouse the ideal database for agentic AI data workflows. ClickHouse is built to be the world's fastest analytical database, where no bits, bytes, or milliseconds are wasted. Even before the LLM and agentic era, ClickHouse aimed to support interactive analytics at scale. We didn't set out to be the best database for agentic AI \- sometimes, happy accidents just happen.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Future use cases [\#](/blog/integrating-clickhouse-mcp#future-use-cases)


Popularity aside, it's still early days, and the tools, workflows, and use cases are evolving rapidly. We see a lot of people forgoing the traditional SQL interface and BI tooling, instead using chat interfaces like Claude Desktop or ChatGPT to talk to their data, skipping SQL entirely, and generating insights and visualizations. We also see developers without a traditional data background building user\-facing applications that expose data to end users, relying on LLMs not just to generate front\-ends, but to structure data and optimise queries for very high concurrency.


With ClickHouse also becoming [the best choice for observability 2\.0](https://clickhouse.com/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse), we're seeing SREs and DevOps teams using LLMs to query their traces, metrics, and logs, blending full\-text search and analytics without obscure query syntax.


And we're imagining what might come next: perhaps we'll see LLMs able to use existing observability data to inform their thinking, perhaps making recommendations for architecture, performance enhancements, or bug fixes based on the data they can access without requiring users to prompt with specific errors or traces.



> Soon, ClickHouse Cloud will offer a remote MCP server as a default interface. That means any MCP client could connect directly to your cloud instance without additional local setup.
> 
> 
> Want early access? [Sign up for the AI features waitlist at clickhouse.ai](http://clickhouse.ai).


## ClickHouse MCP Agent Examples [\#](/blog/integrating-clickhouse-mcp#clickhouse-mcp-agent-examples)


To make it dead simple to get started, we’ve put together some practical examples showing how to integrate various libraries with the ClickHouse MCP server.


You can do this today with the open\-source [mcp\-clickhouse server](https://github.com/ClickHouse/mcp-clickhouse). For more on how this fits into the bigger picture, check out [this AgentHouse demo](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) and our thoughts on [agent\-facing analytics](https://clickhouse.com/blog/agent-facing-analytics).


You can find all five in the [ClickHouse/examples repo](https://github.com/ClickHouse/examples/tree/main/ai/mcp). They are all configured to run against the [ClickHouse SQL Playground](https://sql.clickhouse.com/), which is configured via the following config:



```

```
1env = {
2    "CLICKHOUSE_HOST": "sql-clickhouse.clickhouse.com",
3    "CLICKHOUSE_PORT": "8443",
4    "CLICKHOUSE_USER": "demo",
5    "CLICKHOUSE_PASSWORD": "",
6    "CLICKHOUSE_SECURE": "true"
7}
```

```

We also use Anthropic models and have provided our API key via the `ANTHROPIC_API_KEY` environment variable.


### 1\. Agno [\#](/blog/integrating-clickhouse-mcp#1-agno)


Let’s start with [Agno](https://docs.agno.com/tools/mcp/mcp#multiple-mcp-servers) (previously PhiData), a lightweight, high\-performance library for building Agents.



```

```
1async with MCPTools(command="uv run --with mcp-clickhouse --python 3.13 mcp-clickhouse", env=env, timeout_seconds=60) as mcp_tools:
2    agent = Agent(
3        model=Claude(id="claude-3-5-sonnet-20240620"),
4        markdown=True, 
5        tools = [mcp_tools]
6    )
7    await agent.aprint_response("What's the most starred project in 2025?", stream=True)
```

```

This one has a straightforward API. We initialize `MCPTools` with the command to launch our local MCP Server, and all the tools become available via the `mcp_tools` variable. We can then pass the tools into our agent before calling it on the last line.


 
📄 [View the full Agno example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/agno)   

🧪 [Try the Agno notebook](https://github.com/ClickHouse/examples/tree/main/ai/mcp/agno)



### 2\. DSPy [\#](/blog/integrating-clickhouse-mcp#2-dspy)


[DSPy](https://dspy.ai/) is a framework from Stanford for programming language models.



```

```
1server_parameters = StdioServerParameters(
2    command="uv",
3    args=[
4        'run',
5        '--with', 'mcp-clickhouse',
6        '--python', '3.13',
7        'mcp-clickhouse'
8    ],
9    env=env
10)
11
12dspy.configure(lm=dspy.LM("anthropic/claude-sonnet-4-20250514"))
13
14class DataAnalyst(dspy.Signature):
15    """You are a data analyst. You'll be asked questions and you need to try to answer them using the tools you have access to. """
16
17    user_request: str = dspy.InputField()
18    process_result: str = dspy.OutputField(
19        desc=(
20            "Answer to the query"
21        )
22    )
23
24async with stdio_client(server_params) as (read, write):
25    async with ClientSession(read, write) as session:
26        await session.initialize()
27        tools = await session.list_tools()
28
29        dspy_tools = []
30        for tool in tools.tools:
31            dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))
32
33        print("Tools", dspy_tools)
34
35        react = dspy.ReAct(DataAnalyst, tools=dspy_tools)
36        result = await react.acall(user_request="What's the most popular Amazon product category")
37        print(result)
```

```

This one is more complicated. We similarly initialize our MCP server, but rather than having a single command as a string, we need to split up the command and the arguments.


DSPy also requires us to specify a `Signature` class for each interaction, where we define input and output fields. We then provide that class when initializing our agent, which is done using the `React` class.


`ReAct` stands for "reasoning and acting," which asks the LLM to decide whether to call a tool or wrap up the process. If a tool is required, the LLM takes responsibility for deciding which tool to call and providing the appropriate arguments.


You’ll notice that we must iterate over our MCP tools and convert them to DSPy ones.


 
📄 [View the full DSPy example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/DSPy)   

🧪 [Try the DSPy notebook](https://github.com/ClickHouse/examples/tree/main/ai/mcp/dspy)



### 3\. LangChain [\#](/blog/integrating-clickhouse-mcp#3-langchain)


[LangChain](https://github.com/langchain-ai/langchain-mcp-adapters) is a framework for building LLM\-powered applications.



```

```
1server_params = StdioServerParameters(
2    command="uv", 
3    args=[
4        "run", 
5        "--with", "mcp-clickhouse",
6        "--python", "3.13", 
7        "mcp-clickhouse"
8    ],
9    env=env
10)
11         
12async with stdio_client(server_params) as (read, write):
13    async with ClientSession(read, write) as session:
14        await session.initialize()
15        tools = await load_mcp_tools(session)
16        agent = create_react_agent("anthropic:claude-sonnet-4-0", tools)
17        
18        handler = UltraCleanStreamHandler()        
19        async for chunk in agent.astream_events(
20            {"messages": [{"role": "user", "content": "Who's committed the most code to ClickHouse?"}]}, 
21            version="v1"
22        ):
23            handler.handle_chunk(chunk)
24            
25        print("\n")
```

```

LangChain follows a similar approach to DSPy when initializing the MCP Server. Like DSPy, we need to invoke a ReAct function to create the agent, passing in our MCP tools. We (well, Claude!) wrote a custom bit of code (`UltaCleanStreamHandler`) to render the output in a more user\-friendly way.


 
📄 [View the full LangChain example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/langchain)   

🧪 [Try the LangChain notebook](https://github.com/ClickHouse/examples/tree/main/ai/mcp/langchain)



### 4\. LlamaIndex [\#](/blog/integrating-clickhouse-mcp#4-llamaindex)


[LlamaIndex](https://docs.llamaindex.ai/en/stable/api_reference/tools/mcp/) is a data framework for your LLM applications.



```

```
1mcp_client = BasicMCPClient(
2    "uv", 
3    args=[
4        "run", 
5        "--with", "mcp-clickhouse",
6        "--python", "3.13", 
7        "mcp-clickhouse"
8    ],
9    env=env
10)
11
12mcp_tool_spec = McpToolSpec(
13    client=mcp_client,
14)
15
16tools = await mcp_tool_spec.to_tool_list_async()
17
18agent_worker = FunctionCallingAgentWorker.from_tools(
19    tools=tools, 
20    llm=llm, verbose=True, max_function_calls=10
21)
22agent = AgentRunner(agent_worker)
23
24response = agent.query("What's the most popular repository?")
```

```

LlamaIndex follows the familiar approach of initializing the MCP server. We then initialize an agent with our tools and LLM. We found the default `max_function_calls` value of 5 was too low and wasn’t enough to answer any questions, so we increased it to 10\.


 
📄 [View the full LlamaIndex example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/llamaindex)   

🧪 [Try the LlamaIndex notebook](https://github.com/ClickHouse/examples/tree/main/ai/mcp/llamaindex)



### 5\. PydanticAI [\#](/blog/integrating-clickhouse-mcp#5-pydanticai)


[PydanticAI](https://ai.pydantic.dev/mcp/run-python/#installation) is a Python agent framework designed to make it less painful to build production\-grade applications with Generative AI.



```

```
1server = MCPServerStdio(  
2    'uv',
3    args=[
4        'run',
5        '--with', 'mcp-clickhouse',
6        '--python', '3.13',
7        'mcp-clickhouse'
8    ],
9    env=env
10)
11agent = Agent('anthropic:claude-sonnet-4-0', mcp_servers=[server])
12
13async with agent.run_mcp_servers():
14    result = await agent.run("Who's done the most PRs for ClickHouse?")
15    print(result.output)
```

```

Pydantic has the simplest API. Again, we initialize our MCP server and pass it into the agent. It then runs the server as an asynchronous context manager and we can ask the agent questions inside that block.


 
📄 [View the full PydanticAI example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/pydantic-ai)   

🧪 [Try the PydanticAI notebook](https://github.com/ClickHouse/examples/tree/main/ai/mcp/pydanticai)



## Try It Out [\#](/blog/integrating-clickhouse-mcp#try-it-out)


We’re just getting started with MCP and ClickHouse, and we’d love to hear about what you’re building and your experience using mcp\-clickhouse.


Try out the examples, build something cool, and let us know what you think. If you run into issues or have ideas, open a GitHub issue or [chat with us in Slack](https://clickhouse.com/slack).

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

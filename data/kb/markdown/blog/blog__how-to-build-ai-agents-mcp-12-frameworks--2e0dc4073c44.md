# How to build AI agents with MCP: 12 framework comparison (2025\)


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How to build AI agents with MCP: 12 framework comparison (2025\)

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Al Brown](/authors/al-brown) and [Mark Needham](/authors/mark-needham)Oct 13, 2025 · 36 minutes read
> **TL;DR**  
>   
> Building AI agents with MCP? There are now (at least) **12 major agent SDKs** with MCP support.  
>   
> Each framework has different strengths: **Claude Agent SDK** for security\-first production, **OpenAI Agents SDK** for delegation patterns, **CrewAI** for multi\-agent workflows, **LangChain** for ecosystem breadth, **Agno** for minimal code, **DSPy** for prompt optimization, and more.  
>   
> **We have a look at each of the frameworks and include code for interacting with a Model Context Protocol (MCP) Server for each of them.**


[Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) is an open protocol that standardizes how applications interact with large language models (LLMs). Launched in late 2024, MCP has become the de facto standard for integrating systems and applications with LLMs, with support now available across major AI platforms, including [OpenAI](https://platform.openai.com/docs/guides/tools-connectors-mcp), [Gemini](https://developers.googleblog.com/en/gemini-cli-fastmcp-simplifying-mcp-server-development/), and [Google's Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/build-and-manage-multi-system-agents-with-vertex-ai).


Platforms like [GitHub](https://github.com/github/github-mcp-server), [AWS](https://github.com/awslabs/mcp) and [ClickHouse](https://github.com/ClickHouse/mcp-clickhouse) build MCP servers, which define sets of tools and resources that LLMs can interact with. The LLM lists the tools available, and picks the most appropriate tool for the action it is trying to take.


For example, the ClickHouse MCP server provides a tool called `run_select_query` that can be used to run a SQL SELECT statement against a ClickHouse database. The MCP server implements all of the logic needed to perform that action when the tool is used (creating a connection, authentication, etc.).


MCP servers are conceptually very similar to REST APIs; in fact, before MCP was released, people were just using REST APIs to integrate with LLMs. REST APIs worked pretty well, but MCP provides clearer standardisation for developers and LLMs. MCP servers don’t replace REST APIs, they often live side\-by\-side providing functionality for different purposes.


MCP servers originally ran locally as subprocesses, communicating through stdio or SSE (Server\-Sent Events). However, there's been a recent shift toward platforms hosting remote MCP servers \- similar to how REST APIs are deployed.


With remote MCPs, users don't run the server themselves; their MCP client simply connects to an already\-running service endpoint, often at a URL like `https://api.example.com/mcp`. This shift means MCP servers now need to handle concerns that were previously managed by the client environment: authentication, rate limiting, multi\-tenancy, and authorization. Essentially, remote MCP servers are converging with REST APIs in terms of operational requirements, while maintaining MCP's standardized protocol for LLM tool usage.


## Agent SDKs [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#agent-sdks)


Agent SDKs are a building block used by developers to build agentic experiences in their applications, often providing much of the boilerplate needed to integrate with MCP servers (and much more). The full feature set offered by agent SDKs varies greatly, with Microsoft Agent Framework making it easy to integrate with [Azure AI Foundry](https://ai.azure.com/), and [Vercel AI SDK](https://ai-sdk.dev/docs/introduction) coming out of the box with chat UI components.


Which agent SDK you choose depends on what matters to the application you’re building, how much abstraction you prefer, and which languages you intend to use. If you’re a TypeScript developer building a React app with a chat interface, you’re likely going to be at home with the Vercel AI SDK, while a Java developer building headless agents will prefer [Google’s Agent Development Kit Java SDK](https://github.com/google/adk-java).




| Library | Languages supported | Best suited for |
| --- | --- | --- |
| [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#claude-agent-sdk)) | PythonTypeScript | Production deployments with Claude models, security\-conscious applications requiring explicit tool allowlists |
| [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#openai-agents-sdk)) | PythonTypeScript | Agent handoffs and delegation patterns, responsive UIs with streaming tool calls, lightweight composable agents |
| [Microsoft Agent Framework](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#microsoft-agent-framework)) | Python.NET | Azure ecosystem integration, enterprise features, .NET developers |
| [Google Agent Development Kit](https://google.github.io/adk-docs/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#google-agent-development-kit)) | PythonJava | Gemini and Google ecosystem, Java developers, production deployments with web UI/CLI/API |
| [CrewAI](https://www.crewai.com/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#crewai)) | Python | Multi\-agent workflows, orchestrating fleets of autonomous agents |
| [Upsonic](https://upsonic.ai/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#upsonic)) | Python | Financial sector applications, security and scale, handling LLM exploits |
| [mcp\-agent](https://github.com/lastmile-ai/mcp-agent) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#mcp-agent)) | Python | MCP\-specific workflows, Anthropic's agent patterns (augmented LLM, parallel, router, etc.), lightweight MCP\-optimized development |
| [Agno](https://github.com/agno-agi/agno) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#agno)) | Python | Speed and minimal boilerplate (\~10 lines for MCP), spawning thousands of agents, runtime performance optimization |
| [DSPy](https://dspy.ai/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#dspy)) | Python | Automatic prompt optimization, treating prompting as a programming problem, systematically optimizing agent behavior |
| [LangChain](https://www.langchain.com/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#langchain)) | PythonJavaScript | Extensive ecosystem of integrations, complex workflows beyond MCP, composability and flexibility |
| [LlamaIndex](https://www.llamaindex.ai/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#llama-index)) | PythonTypeScript | Data\-aware AI applications, RAG (retrieval\-augmented generation), combining structured and unstructured data |
| [PydanticAI](https://ai.pydantic.dev/) ([↓](/blog/how-to-build-ai-agents-mcp-12-frameworks#pydanticai)) | Python | Type safety and data validation, runtime type checking, Python applications using Pydantic, testing utilities |


In June 2025, we showed [how to integrate the ClickHouse MCP Server with the most popular AI agent libraries](https://clickhouse.com/blog/integrating-clickhouse-mcp). Only four months later, there’s a whole raft of new agent SDKs, frameworks and libraries, and remote MCP servers are becoming increasingly common.


![star-history-20251010.png](/uploads/star_history_20251010_1ffeaad5fd.png)
*[The GitHub star history for the frameworks discussed in this post](https://www.star-history.com/#pydantic/pydantic-ai&run-llama/llama_index&langchain-ai/langchain&stanfordnlp/dspy&agno-agi/agno&Upsonic/Upsonic&lastmile-ai/mcp-agent&crewAIInc/crewAI&google/adk-python&microsoft/agent-framework&anthropics/claude-agent-sdk-python&openai/openai-agents-python). Source: [https://www.star\-history.com](https://www.star-history.com)*
We'll cover 12 leading agent SDKs with MCP support:


1. [Claude Agent SDK](/blog/how-to-build-ai-agents-mcp-12-frameworks#claude-agent-sdk)
2. [OpenAI Agents SDK](/blog/how-to-build-ai-agents-mcp-12-frameworks#openai-agents-sdk)
3. [Microsoft Agent Framework](/blog/how-to-build-ai-agents-mcp-12-frameworks#microsoft-agent-framework)
4. [Google Agent Development Kit](/blog/how-to-build-ai-agents-mcp-12-frameworks#google-agent-development-kit)
5. [CrewAI](/blog/how-to-build-ai-agents-mcp-12-frameworks#crewai)
6. [Upsonic](/blog/how-to-build-ai-agents-mcp-12-frameworks#upsonic)
7. [mcp\-agent](/blog/how-to-build-ai-agents-mcp-12-frameworks#mcp-agent)
8. [Agno](/blog/how-to-build-ai-agents-mcp-12-frameworks#agno)
9. [DSPy](/blog/how-to-build-ai-agents-mcp-12-frameworks#dspy)
10. [LangChain](/blog/how-to-build-ai-agents-mcp-12-frameworks#langchain)
11. [LlamaIndex](/blog/how-to-build-ai-agents-mcp-12-frameworks#llama-index)
12. [PydanticAI](/blog/how-to-build-ai-agents-mcp-12-frameworks#pydanticai)


## Example MCP server [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#example-mcp-server)


These libraries can connect to any MCP server, like [GitHub MCP](https://github.com/github/github-mcp-server), [Google Analytics MCP](https://developers.google.com/analytics/devguides/MCP), or [Azure MCP](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server).


To demonstrate these agent libraries in action, we'll use the [ClickHouse MCP Server](https://github.com/ClickHouse/mcp-clickhouse). The ClickHouse MCP Server connects ClickHouse to AI assistants, providing tools to execute SQL queries, list databases and tables, and work with both ClickHouse clusters and chDB's embedded OLAP engine.



ClickHouse is particularly well\-suited for AI agent workloads due to its ability to handle large volumes of data with low latency and high concurrency. Since AI agents tend to send numerous queries and overall user latency is already high, you don't want the database making responses even slower.


We'll learn how to use these agent libraries with the ClickHouse MCP Server using the [ClickHouse SQL playground](https://clickhouse.com/blog/announcing-the-new-sql-playground). This hosted ClickHouse service contains a variety of datasets, ranging from New York taxi rides to UK property prices.



```

```
1env = {
2    "CLICKHOUSE_HOST": "sql-clickhouse.clickhouse.com",
3    "CLICKHOUSE_PORT": "8443", 
4    "CLICKHOUSE_USER": "demo",
5    "CLICKHOUSE_PASSWORD": "",
6    "CLICKHOUSE_SECURE": "true",
7    "CLICKHOUSE_VERIFY": "true",
8    "CLICKHOUSE_CONNECT_TIMEOUT": "30",
9    "CLICKHOUSE_SEND_RECEIVE_TIMEOUT": "30"
10}
```


```

## Claude Agent SDK [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#claude-agent-sdk)


The [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) by Anthropic is a framework for building autonomous agents. This was initially released as the Claude Code SDK in July 2025 and then [renamed in September 2025](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk).


Given that Anthropic developed the Model Context Protocol (MCP), it's perhaps not surprising that this library offers first\-class support for MCP.


[Anthropic’s Claude models are often regarded as some of the highest performing models for MCP tool usage](https://gorilla.cs.berkeley.edu/leaderboard.html), being good at determining when to request a tool, using the tool correctly, and hallucinating less often.


The Claude Agent SDK is available for both TypeScript and Python. We’re going to use the Python library, which can be installed using pip:



```

```
1pip install claude-agent-sdk
```


```

Integrating our ClickHouse MCP server with the Claude Agent SDK is quite simple. Let’s have a look at the code:



```

```
1import asyncio
2from claude_agent_sdk import query, ClaudeAgentOptions
3
4options = ClaudeAgentOptions(
5    allowed_tools=[
6        "mcp__mcp-clickhouse__list_databases",
7        "mcp__mcp-clickhouse__list_tables", 
8        "mcp__mcp-clickhouse__run_select_query",
9        "mcp__mcp-clickhouse__run_chdb_select_query"
10    ],
11    mcp_servers={
12        "mcp-clickhouse": {
13            "command": "uv",
14            "args": [
15                "run",
16                "--with", "mcp-clickhouse",
17                "--python", "3.10",
18                "mcp-clickhouse"
19            ],
20            "env": env
21        }
22    }
23)
24
25
26async def main():
27    query = """
28    Tell me something interesting about UK property sales
29    """
30    async for message in query(prompt=query, options=options):
31        print(message)
32
33
34asyncio.run(main())
```


```

The setup is straightforward, but there's an interesting difference worth mentioning. Most libraries will discover all available tools from the MCP server by default, while the Claude Agent SDK requires the `allowed_tools` property to explicitly define which tools it can use. If you find yourself asking “Why wont the Claude Agent SDK find any MCP tools?” it might be because you’ve forgotten to set the `allowed_tools` property.


This is actually a useful security feature \- MCP servers can provide a lot of tools, and some tools may give access to features that you do not want to expose in your agent. These could be destructive operations, like dropping a database table or deleting a git repo. The Claude Agent SDK takes a “zero trust” approach, blocking all tools unless explicitly allowed.


 
📄 
[View the full Claude Agent SDK example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/claude-agent-sdk)
  
 
🧪 
[Try the Claude Agent SDK notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/claude-agent/claude-agent.ipynb)



## OpenAI Agents SDK [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#openai-agents-sdk)


The [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) is OpenAI's official framework for building AI agents, released in December 2024\. This SDK represents OpenAI's opinionated approach to agent development, incorporating lessons learned from their experimental [Swarm framework](https://github.com/openai/swarm) and focusing on **lightweight, composable agent patterns** rather than heavyweight abstractions.


The OpenAI Agents SDK takes a minimalist approach \- it provides just enough structure to build reliable agents without imposing complex architectural decisions. This philosophy extends to its MCP support, which treats MCP servers as native tools that agents can discover and use without additional configuration layers. The SDK is particularly optimized for OpenAI's models, with built\-in handling for model\-specific features like parallel tool calling and structured outputs.


The SDK is available in both Python and TypeScript. For Python, install it via pip:



```

```
1pip install openai-agents
```

```

Here's how to integrate the ClickHouse MCP server:



```

```
1from agents.mcp import MCPServer, MCPServerStdio
2from agents import Agent, Runner, trace
3import json
4
5async with MCPServerStdio(
6        name="ClickHouse SQL Playground",
7        params={
8            "command": "uv",
9            "args": [
10                'run',
11                '--with', 'mcp-clickhouse',
12                '--python', '3.13',
13                'mcp-clickhouse'
14            ],
15            "env": env
16        }, client_session_timeout_seconds = 60
17) as server:
18    agent = Agent(
19        name="Assistant",
20        instructions="Use the tools to query ClickHouse and answer questions based on those files.",
21        mcp_servers=[server],
22    )
23
24    message = "What's the biggest GitHub project so far in 2025?"
25    print(f"nnRunning: {message}")
26    with trace("Biggest project workflow"):
27        result = Runner.run_streamed(starting_agent=agent, input=message, max_turns=20)
28        async for chunk in result.stream_events():
29            simple_render_chunk(chunk)
```

```

We’ve omitted, the `simple_render_chunk` function but brevity, but you can find that code in our [OpenAI agent docs](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/openai-agents). You’ll notice that the function ends up being quite complicated as the library returns us a fine grained response object containing information about tool calls, tool output, as well as a running commentary of what the model is thinking along the way.


What distinguishes the OpenAI Agents SDK is its **focus on agent handoffs and delegation patterns**. Rather than building monolithic agents that try to do everything, the SDK encourages creating specialized agents that can seamlessly hand off tasks to each other. This works particularly well with MCP servers \- you might have one agent that specializes in data analysis using the ClickHouse MCP server, another that handles visualization, and they coordinate through the SDK's handoff mechanisms.


The SDK also includes first\-class support for **streaming responses with tool calls**, making it excellent for building responsive user interfaces where you want to show both the agent's thinking process and the MCP tools being called in real\-time.


 
📄 
[View the full OpenAI Agents SDK example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/openai-agents)
  
 
🧪 
[Try the OpenAI Agents SDK notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/openai-agents/openai-agents.ipynb)



## Microsoft Agent Framework [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#microsoft-agent-framework)


The [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) is currently in public preview as of October 2025\. It combines AutoGen, a Microsoft Research project, with Semantic Kernel's enterprise features into a single framework for developers.


The Microsoft Agent Framework is available in both .NET and Python. We’re partial to Python, so we’ll use that. It can be installed using pip, but you need to provide the `--pre` flag as it has not been officially published as of October 2025\.



```

```
1pip install agent-framework --pre
```


```

Time for some code:



```

```
1import asyncio
2from agent_framework import ChatAgent, MCPStdioTool
3from agent_framework.openai import OpenAIResponsesClient
4
5
6async def run_with_mcp() -> None:
7    clickhouse_mcp_server = MCPStdioTool(
8        name="clickhouse",
9        command="uv",
10        args=[
11            "run",
12            "--with", "mcp-clickhouse",
13            "--python", "3.10",
14            "mcp-clickhouse"
15        ],
16        env=env
17    )
18
19    async with ChatAgent(
20        chat_client=OpenAIResponsesClient(model_id="gpt-5-mini-2025-08-07"),
21        name="AnalystAgent",
22        instructions="You are a helpful assistant that can help query a ClickHouse database",
23        tools=clickhouse_mcp_server,
24    ) as agent:
25        query = "Tell me about UK property prices over the last five years"
26        print(f"User: {query}")
27        async for chunk in agent.run_stream(query):
28            print(chunk.text, end="", flush=True)
29        print("nn")
30
31asyncio.run(run_with_mcp())
```


```

Although the Microsoft Agent Framework is clearly designed for building AI agents on Azure, you can use OpenAI and Anthropic models directly without using Azure . To use Anthropic models with the Microsoft Agent Framework, you can provide the parameter `base_url="https://api.anthropic.com/v1/"` when initializing the client.


The Microsoft Agent Framework defaults to having all tools available, but you can provide an allowlist via the [`allowed_tools`](https://github.com/microsoft/agent-framework/blob/8967269d3eba4bb84544a710e9d675fe216d220c/python/packages/core/agent_framework/_mcp.py#L727) parameter.


 
📄 [View the full Microsoft Agent Framework example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/microsoft-agent-framework)
  
 
🧪 [Try the Microsoft Agent Framework notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/microsoft-agent-framework/microsoft-agent-framework.ipynb)



## Google Agent Development Kit [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#google-agent-development-kit)


[Google Agent Development Kit](https://google.github.io/adk-docs/) (ADK) is a framework for developing and deploying AI agents. While it includes optimizations for Gemini and the Google ecosystem, it’s designed to be model\-agnostic and deployment\-agnostic, with compatibility for other frameworks.


According to their docs, it “attempts to make agent development feel more like traditional software development, providing developers with tools to create, deploy, and orchestrate agentic architectures for both simple tasks and complex workflows”.


The Google Agent Development Kit supports both Python and Java \- it’s one of the only major SDKs we’ve come across that offers support for Java. We’ll continue to use Python, and install the SDK via pip:



```

```
1pip install google-adk
```

```

And now for the code:



```

```
1from google.adk.agents import LlmAgent
2from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
3from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
4from mcp import StdioServerParameters
5
6
7root_agent = LlmAgent(
8  model='gemini-2.5-flash',
9  name='database_agent',
10  instruction='Help the user query a ClickHouse database.',
11  tools=[
12    MCPToolset(
13      connection_params=StdioConnectionParams(
14        server_params = StdioServerParameters(
15          command='uv',
16          args=[
17              "run",
18              "--with", "mcp-clickhouse",
19              "--python", "3.10",
20              "mcp-clickhouse"
21          ],
22          env=env
23        ),
24        timeout=60,
25      ),
26    )
27  ],
28)
```


```

This one is a bit different, as you only define the agent \- there isn’t an easy way (at least that we could find) to call the agent in code. Instead, there are various commands that you can execute from the terminal to run the agent. For example, we can launch a web UI by running the following:



```

```
1uv run --with google-adk adk web
```


```

If you take this approach, you get a ChatGPT\-esque UI where you can ask questions and have them answered by the model. It will show you the tools that it calls along the way.


Alternatively, there’s an experimental CLI that you can launch like this:



```

```
1uv run --with google-adk adk run mcp_agent
```


```

This time, you will get a prompt like this:



```
[user]: Tell me about UK property prices in the early 2020s

```

You ask your question, press enter, and off it goes:



```
2025-10-09 16:40:15,882 - mcp-clickhouse - INFO - Listing all databases
2025-10-09 16:40:15,882 - mcp-clickhouse - INFO - Creating ClickHouse client connection to sql-clickhouse.clickhouse.com:8443 as demo (secure=True, verify=True, connect_timeout=30s, send_receive_timeout=30s)
2025-10-09 16:40:16,578 - mcp-clickhouse - INFO - Successfully connected to ClickHouse server version 25.8.1.8344
2025-10-09 16:40:16,756 - mcp-clickhouse - INFO - Found 38 databases
2025-10-09 16:40:16,765 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-10-09 16:40:18,612 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-10-09 16:40:18,620 - mcp-clickhouse - INFO - Listing tables in database 'uk'
2025-10-09 16:40:18,621 - mcp-clickhouse - INFO - Creating ClickHouse client connection to sql-clickhouse.clickhouse.com:8443 as demo (secure=True, verify=True, connect_timeout=30s, send_receive_timeout=30s)
2025-10-09 16:40:19,298 - mcp-clickhouse - INFO - Successfully connected to ClickHouse server version 25.8.1.8344
2025-10-09 16:40:20,764 - mcp-clickhouse - INFO - Found 9 tables
2025-10-09 16:40:20,772 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-10-09 16:40:26,109 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-10-09 16:40:26,112 - mcp-clickhouse - INFO - Executing SELECT query: SELECT toYear(date) AS year, avg(price) AS average_price FROM uk.uk_price_paid_with_projections_v2 WHERE date >= '2020-01-01' AND date <= '2022-12-31' GROUP BY year ORDER BY year
2025-10-09 16:40:26,113 - mcp-clickhouse - INFO - Creating ClickHouse client connection to sql-clickhouse.clickhouse.com:8443 as demo (secure=True, verify=True, connect_timeout=30s, send_receive_timeout=30s)
2025-10-09 16:40:26,703 - mcp-clickhouse - INFO - Successfully connected to ClickHouse server version 25.8.1.8344
2025-10-09 16:40:27,436 - mcp-clickhouse - INFO - Query returned 3 rows
2025-10-09 16:40:27,443 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
[database_agent]: The average UK property prices in the early 2020s were:

*   **2020:** £377,777.77
*   **2021:** £388,990.83
*   **2022:** £413,481.61

```

Or, you can run the agent via an API endpoint, which we expect is the preferred mode of usage:



```

```
1uv run --with google-adk adk api_server
```


```

 
📄 [View the full Google Agent Development Kit example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/google-agent-development-kit)
  
 
🧪 [Try the Google Agent Development Kit example](https://github.com/ClickHouse/examples/blob/main/ai/mcp/google-agent-development-kit)



## CrewAI [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#crewai)


[CrewAI](https://github.com/crewAIInc/crewAI) is an agent framework with a particular **emphasis on building multi\-agent workflows**. While the framework itself is open source, the company behind it offers a commercial platform designed for orchestrating and managing fleets of autonomous agents.


CrewAI is available only in Python and installed with pip:



```

```
1pip install "crewai-tools[mcp]"
```

```

The code to build a CrewAI agent with ClickHouse MCP support is shown below:



```

```
1from crewai import Agent
2from crewai_tools import MCPServerAdapter
3from mcp import StdioServerParameters
4
5server_params=StdioServerParameters(
6    command='uv',
7    args=[
8        "run",
9        "--with", "mcp-clickhouse",
10        "--python", "3.10",
11        "mcp-clickhouse"
12    ],
13    env=env
14)
15
16with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
17    print(f"Available tools: {[tool.name for tool in mcp_tools]}")
18
19    my_agent = Agent(
20        role="MCP Tool User",
21        goal="Utilize tools from an MCP server.",
22        backstory="I can connect to MCP servers and use their tools.",
23        tools=mcp_tools,
24        reasoning=True,
25        verbose=True
26    )
27    my_agent.kickoff(messages=[
28        {"role": "user", "content": "Tell me about property prices in London between 2024 and 2025"}
29    ])
```


```

 
📄 
[View the full CrewAI example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/crewai)
  
 
🧪 
[Try the CrewAI notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/crewai/crewai.ipynb)



## mcp\-agent [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#mcp-agent)


[mcp\-agent](https://github.com/lastmile-ai/mcp-agent) is a framework by [lastmileAI](https://lastmileai.dev/) that takes deep inspiration from [Anthropic’s Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) paper. The paper covers various patterns and workflows that Anthropic has seen perform well in real\-world agentic applications, and mcp\-agent offers a composable framework for developing agents that follow Anthropic’s guidance.


mcp\-agent’s integration with MCP feels largely similar to the other frameworks and SDKs in this post, and the framework is not offering the extensive bells\-and\-whistles that you might get from the likes of Google’s ADK. Instead, mcp\-agent is (as you might guess from the name) **designed specifically for MCP**, offering developers a simple, lightweight library that is highly optimized for the patterns suggested by Anthropic:


- [Augmented LLM](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#augmentedllm)
- [Parallel](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#parallel)
- [Router](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#router)
- [Intent\-Classifier](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#intentclassifier)
- [Orchestrator\-Workers](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#orchestrator-workers)
- [Evaluator\-Optimizer](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#evaluator-optimizer)


mcp\-agent also provides support for the experimental [OpenAI Swarm](https://github.com/lastmile-ai/mcp-agent?tab=readme-ov-file#swarm-1), which has now been replaced by the new [OpenAI Agents SDK](https://github.com/openai/openai-agents-python).


mcp\-agent is a Python library that can be installed via pip:



```

```
1pip install mcp-agent openai
```


```

And the code is shown below:



```

```
1from mcp_agent.app import MCPApp
2from mcp_agent.agents.agent import Agent
3from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
4from mcp_agent.config import Settings, MCPSettings, MCPServerSettings, OpenAISettings
5
6settings = Settings(
7    execution_engine="asyncio",
8    openai=OpenAISettings(
9        default_model="gpt-5-mini-2025-08-07",
10    ),
11    mcp=MCPSettings(
12        servers={
13            "clickhouse": MCPServerSettings(
14                command='uv',
15                args=[
16                    "run",
17                    "--with", "mcp-clickhouse",
18                    "--python", "3.10",
19                    "mcp-clickhouse"
20                ],
21                env=env
22            ),
23        }
24    ),
25)
26
27app = MCPApp(name="mcp_basic_agent", settings=settings)
28
29async with app.run() as mcp_agent_app:
30    logger = mcp_agent_app.logger
31    data_agent = Agent(
32        name="database-anayst",
33        instruction="""You can answer questions with help from a ClickHouse database.""",
34        server_names=["clickhouse"],
35    )
36
37    async with data_agent:
38        llm = await data_agent.attach_llm(OpenAIAugmentedLLM)
39        result = await llm.generate_str(
40            message="Tell me about UK property prices in 2025. Use ClickHouse to work it out."
41        )
42        
43        logger.info(result)
```


```

 
📄 
[View the full mcp\-agent example](javascript:void(0))
  
 
🧪 [Try the mcp\-agent notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/mcp-agent/mcp-agent.ipynb)



## Upsonic [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#upsonic)


[Upsonic](https://github.com/Upsonic/Upsonic) is an AI agent framework targeted toward the financial sector. Being used in finance, it emphasises its ability to handle scale, and deflect common attacks that attempt to exploit LLMs.


Upsonic is available in Python, and installed using pip:



```

```
1pip install "upsonic[loaders,tools]" openai
```


```

The code to create an agent enabled with MCP is familiar:



```

```
1from upsonic import Agent, Task
2from upsonic.models.openai import OpenAIResponsesModel
3
4class DatabaseMCP:
5    """
6    MCP server for ClickHouse database operations.
7    Provides tools for querying tables and databases
8    """
9    command="uv"
10    args=[
11        "run",
12        "--with", "mcp-clickhouse",
13        "--python", "3.10",
14        "mcp-clickhouse"
15    ]
16    env=env
17
18
19database_agent = Agent(
20    name="Data Analyst",
21    role="ClickHouse specialist.",
22    goal="Query ClickHouse database and tables and answer questions",
23    model=OpenAIResponsesModel(model_name="gpt-5-mini-2025-08-07")
24)
25
26
27task = Task(
28    description="Tell me what happened in the UK property market in the 2020s. Use ClickHouse.",
29    tools=[DatabaseMCP]
30)
31
32workflow_result = database_agent.do(task)
33print("nMulti-MCP Workflow Result:")
34print(workflow_result)
```


```

This time the MCP Server needs to be wrapped inside a class that you provide as a tool rather than passing in the tool logic directly to the task. It’s not a big difference compared to other libraries, but seems worth pointing out.


Interestingly, given that Upsonic has a “security first” approach, it appears to discover and enable all MCP tools by default, as opposed to the “zero trust” approach of the Claude Agent SDK which requires an explicit allowlist of tools.


 
📄 [View the full Upsonic example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/upsonic)
  
 
🧪 
[Try the Upsonic notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/upsonic/upsonic.ipynb)



## Agno [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#agno)


[Agno](https://github.com/agno-agi/agno) is a framework that prioritizes **speed \- both development velocity and runtime performance**. The framework aims for minimal boilerplate, with MCP integration achievable in about 10 lines of code, which is the shortest of all the libraries that we explored. This focus on simplicity extends throughout the framework, with Pythonic APIs that avoid unnecessary abstractions.


Performance is a key differentiator for Agno. They've optimized for scenarios where workflows spawn thousands of agents, recognizing that even modest user bases can hit performance bottlenecks with agent systems. Their benchmarks show agent instantiation at \~3μs on average with a memory footprint of \~6\.5KB per agent \- numbers that matter when you're running agent fleets at scale.


Agno is Python\-only and can be installed via pip:



```

```
1pip install agno
```

```

And the code to build a ClickHouse\-backed agent is as follows:



```

```
1from agno.agent import Agent
2from agno.tools.mcp import MCPTools
3from agno.models.anthropic import Claude
4
5async with MCPTools(command="uv run --with mcp-clickhouse --python 3.13 mcp-clickhouse", env=env, timeout_seconds=60) as mcp_tools:
6   agent = Agent(
7       model=Claude(id="claude-3-5-sonnet-20240620"),
8       markdown=True,
9       tools = [mcp_tools]
10   )
11await agent.aprint_response("What's the most starred project in 2025?", stream=True)
```

```

Beyond the open\-source framework, Agno is building AgentOS, a development platform designed to bridge the gap from development to production. AgentOS adds deployment capabilities, observability, and monitoring to agents built with the Agno framework. The platform handles the operational complexity of running agents in production while maintaining the simplicity that defines the core framework.


 
📄 
[View the full Agno example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/agno)
  
 
🧪 
[Try the Agno notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/agno/agno.ipynb)



## DSPy [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#dspy)


[DSPy](https://github.com/stanfordnlp/dspy) takes a fundamentally different approach to building AI agents. Rather than writing explicit prompts and chaining tools together, DSPy treats **prompting as a programming problem** that can be optimized automatically. It's essentially a compiler for AI pipelines \- you define what you want to accomplish, and DSPy figures out the best prompts and configurations to achieve it.


DSPy's MCP integration is particularly interesting because it can automatically learn how to use MCP tools effectively. Instead of manually crafting prompts that explain how to use your ClickHouse MCP server, DSPy can generate and optimize these prompts based on examples of successful interactions. This makes it excellent for scenarios where you need to integrate multiple MCP servers and want the system to learn the most effective ways to coordinate between them.


DSPy is Python\-only and installed via pip:



```

```
1pip install dspy
```

```

And, let’s have a look at the code:



```

```
1from mcp import ClientSession, StdioServerParameters
2from mcp.client.stdio import stdio_client
3import dspy
4
5server_params = StdioServerParameters(
6    command="uv",
7    args=[
8        'run',
9        '--with', 'mcp-clickhouse',
10        '--python', '3.13',
11        'mcp-clickhouse'
12    ],
13    env=env
14)
15
16class DataAnalyst(dspy.Signature):
17    """You are a data analyst. You'll be asked questions and you need to try to answer them using the tools you have access to. """
18
19    user_request: str = dspy.InputField()
20    process_result: str = dspy.OutputField(
21        desc=(
22            "Answer to the query"
23        )
24    )
25
26from utils import print_dspy_result
27
28async with stdio_client(server_params) as (read, write):
29    async with ClientSession(read, write) as session:
30        await session.initialize()
31        tools = await session.list_tools()
32
33        dspy_tools = []
34        for tool in tools.tools:
35            dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))
36
37        react = dspy.ReAct(DataAnalyst, tools=dspy_tools)
38        result = await react.acall(user_request="What's the most popular Amazon product category")
39        print_dspy_result(result)
```

```

A unique feature of DsPy is that you need to provide a signature class to your requests. Our signature is reasonably simple \- it takes in a string and returns a string. We’ve excluded the [`print_dspy_result`](https://github.com/ClickHouse/examples/blob/main/ai/mcp/dspy/utils.py) function for brevity, but if you take a look at [the code on GitHub](https://github.com/ClickHouse/examples/blob/main/ai/mcp/dspy/utils.py), you can see that DsPy gives us back a very fine grained response.


The key advantage of DSPy is its ability to **systematically optimize agent behavior**. If you find yourself constantly tweaking prompts to get better results from your MCP tools, DSPy can automate this process. It's particularly powerful when combined with evaluation datasets \- you can define what "good" looks like for your agent's outputs, and DSPy will optimize the entire pipeline to maximize that metric.


 
📄 
[View the full DSPy example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/dspy)
  
 
🧪 
[Try the DSPy notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/dspy/dspy.ipynb)



## LangChain [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#langchain)


[LangChain](https://github.com/langchain-ai/langchain) is one of the most established frameworks in the AI agent ecosystem, predating MCP by several years. It's known for its **extensive ecosystem of integrations** \- if there's a tool, database, or LLM you want to use, LangChain probably has an integration for it. With MCP support added in early 2025, LangChain now bridges its massive ecosystem with the standardized MCP protocol.


What makes LangChain's MCP implementation unique is how it treats MCP servers as just another type of tool in its vast toolkit. This means you can seamlessly combine MCP servers with LangChain's hundreds of other integrations \- use an MCP server to query ClickHouse, then feed those results into a LangChain document loader, vector store, or any other component.


LangChain supports both Python and JavaScript/TypeScript:



```

```
1pip install langchain langchain-mcp
```

```

The code is shown below:



```

```
1from mcp import ClientSession, StdioServerParameters
2from mcp.client.stdio import stdio_client
3
4server_params = StdioServerParameters(
5    command="uv",
6    args=[
7        "run",
8        "--with", "mcp-clickhouse",
9        "--python", "3.13",
10        "mcp-clickhouse"
11    ],
12    env=env
13)
14
15async with stdio_client(server_params) as (read, write):
16    async with ClientSession(read, write) as session:
17        await session.initialize()
18        tools = await load_mcp_tools(session)
19        agent = create_react_agent("anthropic:claude-sonnet-4-0", tools)
20        
21        handler = UltraCleanStreamHandler()        
22        async for chunk in agent.astream_events(
23            {"messages": [{"role": "user", "content": "Who's committed the most code to ClickHouse?"}]}, 
24            version="v1"
25        ):
26            handler.handle_chunk(chunk)
27            
28        print("n")
```

```

We’ve excluded the `UltraCleanStreamHandler` for brevity. We need this custom stream handler as LangChain also returns fine grained output describing tool calls, tool outputs, as well as a commentary on what the agent is thinking.


LangChain's strength lies in its **composability and flexibility**. While newer frameworks might offer cleaner APIs for MCP specifically, LangChain excels when you need to build complex workflows that go beyond just MCP tools. Its extensive documentation and large community also mean you'll find examples and solutions for almost any integration challenge.


 
📄 
[View the full LangChain example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/langchain)
  
 
🧪 
[Try the LangChain notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/langchain/langchain.ipynb)



## LlamaIndex [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#llama-index)


[LlamaIndex](https://github.com/run-llama/llama_index/) (formerly GPT Index) specializes in **data\-aware AI applications**, particularly those involving retrieval\-augmented generation (RAG). While other frameworks focus on general agent capabilities, LlamaIndex is optimized for scenarios where agents need to work with large amounts of structured and unstructured data.


LlamaIndex's MCP integration is designed to work seamlessly with its data indexing and retrieval capabilities. This makes it particularly powerful when combined with analytical databases like ClickHouse \- you can use MCP tools to query structured data, then combine those results with LlamaIndex's document retrieval and synthesis capabilities to provide comprehensive answers.


Available in both Python and TypeScript:



```

```
1pip install llama-index llama-index-mcp
```

```

And the code:



```

```
1from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
2
3mcp_client = BasicMCPClient(
4    "uv",
5    args=[
6        "run",
7        "--with", "mcp-clickhouse",
8        "--python", "3.13",
9        "mcp-clickhouse"
10    ],
11    env=env
12)
13
14mcp_tool_spec = McpToolSpec(
15    client=mcp_client,
16)
17
18tools = await mcp_tool_spec.to_tool_list_async()
19
20from llama_index.core.agent import AgentRunner, FunctionCallingAgentWorker
21
22agent_worker = FunctionCallingAgentWorker.from_tools(
23    tools=tools,
24    llm=llm, verbose=True, max_function_calls=10
25)
26agent = AgentRunner(agent_worker)
27
28from llama_index.llms.anthropic import Anthropic
29llm = Anthropic(model="claude-sonnet-4-0")
30
31response = agent.query("What's the most popular repository?")
```


```

The framework's **query engine abstraction** is what sets it apart. Rather than thinking about individual tool calls, LlamaIndex lets you define complex query patterns that can automatically orchestrate multiple MCP servers, retrieve relevant documents, and synthesize responses. This is particularly useful for building agents that need to answer complex analytical questions by combining data from multiple sources.


 
📄 
[View the full LlamaIndex example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/llamaindex)
  
 
🧪 
[Try the LlamaIndex notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/llamaindex/llamaindex.ipynb)



## PydanticAI [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#pydanticai)


[PydanticAI](https://github.com/pydantic/pydantic-ai) launched in December 2024 by the team behind the popular Pydantic validation library. It brings Pydantic's philosophy of **type safety and data validation** to the world of AI agents. If you've ever struggled with agents returning inconsistently formatted data or making type errors when calling tools, PydanticAI aims to solve these problems.


PydanticAI's MCP integration leverages Pydantic's powerful validation system to ensure that all inputs and outputs from MCP servers conform to expected schemas. This means runtime type checking for all MCP tool calls, automatic validation of responses, and clear error messages when something goes wrong. It's particularly valuable when building agents that need to integrate with existing Python applications that already use Pydantic for data validation.


Python\-only, installed via pip:



```

```
1pip install pydantic-ai
```

```

Let’s have a look at the code:



```

```
1from pydantic_ai import Agent
2from pydantic_ai.mcp import MCPServerStdio
3
4server = MCPServerStdio(
5    'uv',
6    args=[
7        'run',
8        '--with', 'mcp-clickhouse',
9        '--python', '3.13',
10        'mcp-clickhouse'
11    ],
12    env=env
13)
14agent = Agent('anthropic:claude-sonnet-4-0', mcp_servers=[server])
15
16async with agent.run_mcp_servers():
17    result = await agent.run("Who's done the most PRs for ClickHouse?")
18    print(result.output)
```

```

What makes PydanticAI compelling is its **focus on correctness and developer experience**. By treating agent responses as structured data that can be validated and typed, it brings many of the benefits of static typing to the inherently dynamic world of LLMs. The framework also includes excellent testing utilities, making it easier to write unit tests for agents that use MCP servers \- something that's traditionally been challenging.


 
📄 
[View the full PydanticAI example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/pydanticai)
  
 
🧪 
[Try the PydanticAI notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/pydanticai/pydantic.ipynb)



## Frequently Asked Questions [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#faq)


### What is the best AI agent framework for MCP? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#what-is-the-best-ai-agent-framework-for-mcp)


There's no single "best" framework \- it depends on your use case. For production deployments with Claude models, the Claude Agent SDK offers the tightest integration. If you're already in the Azure ecosystem, Microsoft Agent Framework is the obvious choice.


For complex multi\-agent workflows, CrewAI excels. LangChain wins on ecosystem breadth, while PydanticAI is best if you need type safety and validation. Anf if you want to write the smallest amount of code, don’t forget to look at Agno.


### Can I use multiple MCP servers with one agent? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#can-i-use-multiple-mcp-servers-with-one-agent)


Yes, most frameworks support connecting to multiple MCP servers simultaneously. Your agent can use tools from a ClickHouse MCP server for data analysis, a GitHub MCP server for code operations, and a Slack MCP server for notifications \- all in the same workflow. The agent will automatically select the appropriate server based on the tools it needs.


### Is MCP better than OpenAI function calling? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#is-mcp-better-than-openai-function-calling)


They're complementary, not competing. OpenAI function calling is model\-specific, while MCP is model\-agnostic. MCP provides standardization across different LLM providers and includes features like resource management and progress reporting that go beyond simple function calling. Many frameworks use function calling under the hood to implement MCP.


### How much latency does MCP add? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#how-much-latency-does-mcp-add)


MCP itself adds minimal overhead \- typically 10\-50ms for the protocol layer. The real latency comes from tool execution. For a ClickHouse query, you're looking at the database query time plus MCP overhead. In practice, expect 50\-200ms additional latency compared to direct API calls, though this is usually negligible compared to LLM inference time (2\-5 seconds).


### Do MCP servers work with local LLMs? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#do-mcp-servers-work-with-local-llms)


Yes, MCP is model\-agnostic. You can use MCP servers with local models through frameworks like LangChain or LlamaIndex. The quality of tool usage will depend on the model's capabilities \- models like Llama 3\.3 70B or Qwen 2\.5 72B handle MCP tools well, while smaller models may struggle with complex tool selection.


### Can I use MCP servers without an agent framework? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#can-i-use-mcp-servers-without-an-agent-framework)


Technically yes, but it's not recommended. You'd need to implement the MCP client protocol yourself, handle tool discovery, manage message passing, and deal with error handling. The frameworks in this guide handle all of this complexity for you. Even lightweight options like the OpenAI Agents SDK are easier than rolling your own.


### How do I debug MCP connection issues? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#how-do-i-debug-mcp-connection-issues)


Start by checking the MCP server logs \- most servers provide detailed logging. Common issues include authentication failures (check your environment variables), network connectivity (ensure the host is reachable), and timeout errors (increase connection timeout). Use the `--verbose` flag when running MCP servers locally to see detailed debug output.


### What's the difference between local and remote MCP servers? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#whats-the-difference-between-local-and-remote-mcp-servers)


Local MCP servers run as subprocess on your machine using stdio communication \- they're started and stopped by your agent. Remote MCP servers run as standalone services accessed over HTTP/WebSocket, supporting multiple concurrent clients. Local servers are simpler to set up but don't scale. Remote servers require more infrastructure but support production workloads.


### Can MCP servers modify data or only read it? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#can-mcp-servers-modify-data-or-only-read-it)


MCP servers can provide any tools they want, including destructive operations. The ClickHouse MCP server intentionally only provides `run_select_query` to prevent accidental data modification, but other servers might offer write operations. Always review which tools an MCP server exposes, especially in production. The Claude Agent SDK's allowlist approach is good practice here.


### How do I handle MCP server authentication? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#how-do-i-handle-mcp-server-authentication)


Authentication is handled through environment variables passed to the MCP server on startup. Each server defines its own auth requirements \- ClickHouse uses standard database credentials, GitHub uses personal access tokens, etc. Store credentials securely (use environment variables, not hardcoded values) and ensure they have minimal required permissions.


### What happens if an MCP tool call fails? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#what-happens-if-an-mcp-tool-call-fails)


Error handling varies by framework. Most will return the error to the LLM, which can then decide whether to retry, try a different approach, or report the failure. Some frameworks like Agno include automatic retry logic. You should implement timeout handling and consider circuit breakers for production deployments.


### Can I create custom MCP servers? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#can-i-create-custom-mcp-servers)


Yes, MCP is an open protocol. [You can build MCP servers in Python](https://modelcontextprotocol.io/docs/develop/build-server), TypeScript, or any language that can handle JSON\-RPC over stdio or HTTP. The [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) provides templates and utilities. Custom servers are useful for exposing internal APIs or building domain\-specific tools.


### How do MCP servers handle concurrent requests? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#how-do-mcp-servers-handle-concurrent-requests)


This depends on the server implementation. Stdio\-based local servers typically handle one request at a time. Remote MCP servers can handle concurrent requests, but may have rate limits. The ClickHouse MCP server creates separate database connections per request, allowing concurrent queries up to the database's connection limit.


### Which LLMs work best with MCP tools? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#which-llms-work-best-with-mcp-tools)


Claude 3\.5 Sonnet and Opus consistently top the tool usage benchmarks. GPT\-4 and GPT\-4 Turbo perform well but may hallucinate tool parameters more often. In our experience, the GPT\-5 series of models interact with MCP servers more effectively.


Gemini 2\.0 Flash is fast and capable, but we’ve found that the 2\.5 series of models work better with MCP. Open\-source models like Llama 3\.3 70B and Qwen 2\.5 72B can handle MCP tools but require more explicit instructions.


### Do I need to pay for MCP? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#do-i-need-to-pay-for-mcp)


MCP itself is free and open source. You pay for the LLM API calls and any resources the MCP servers connect to (databases, APIs, etc.). The agent frameworks are mostly open source, though some offer paid cloud platforms for deployment and monitoring.


### How do I deploy MCP agents to production? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#how-do-i-deploy-mcp-agents-to-production)


For simple deployments, containerize your agent and MCP servers together. For scale, run remote MCP servers as separate services behind a load balancer, and deploy agents as stateless workers. Consider using platforms like Modal, Railway, or the commercial offerings from CrewAI or LangChain for managed deployments. Monitor tool usage, implement rate limiting, and ensure proper error handling.


### Can MCP servers access local files? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#can-mcp-servers-access-local-files)


MCP servers can technically access anything the process can reach, but this is controlled by the server implementation. The filesystem MCP server explicitly provides file access tools. Always run MCP servers with minimal permissions and consider sandboxing them in production environments.


### What's the difference between MCP and LangChain tools? [\#](/blog/how-to-build-ai-agents-mcp-12-frameworks#whats-the-difference-between-mcp-and-langchain-tools)


LangChain tools are framework\-specific, while MCP is a universal protocol. LangChain now supports MCP servers as a type of tool, giving you access to both ecosystems. MCP provides better standardization and portability, while LangChain tools may offer deeper framework integration.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

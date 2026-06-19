# LLM chat UIs that support MCP


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# LLM chat UIs that support MCP

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Aug 12, 2025 · 15 minutes readAs open\-source LLM chat applications continue to evolve, support for emerging standards like Model Context Protocol (MCP) is becoming increasingly important \- especially for developers building data\-rich, tool\-augmented AI experiences.


This post will explore four popular open\-source ChatGPT\-style apps \- LibreChat, AnythingLLM, Open WebUI, and Chainlit \- through MCP compatibility.


Whether you're integrating with external tools, orchestrating server\-side inference, or just curious about making chat apps more context\-aware, this guide walks you through each platform's pros, cons, and setup steps.


Let’s get started!


## LibreChat [\#](/blog/llm-chat-mcp-support#librechat)


LibreChat is a leading enterprise\-focused open\-source ChatGPT alternative. It delivers a pixel\-perfect interface that rivals the original while adding powerful enhancements like multi\-provider support, conversation forking, and advanced search capabilities.


LibreChat is among the first platforms to fully implement Model Context Protocol (MCP) server support, positioning it at the forefront of universal AI tool integration. It supports stdio/streamable HTTPSSE transport, multi\-user isolation, and flexible deployment options through YAML configuration \-making it one of the most enterprise\-ready MCP implementations.


We've chosen LibreChat as the foundation for [AgentHouse](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp), our interactive demo environment. This environment seamlessly bridges ClickHouse's lightning\-fast real\-time analytics with large language models through MCP integration. This showcases LibreChat's extensible architecture and cutting\-edge protocol support, making it ideal for sophisticated, data\-driven AI applications beyond simple chat interfaces.


You can run LibreChat directly with npm, Docker, or Kubernetes with a Helm Chart. I’ve opted for Docker as that’s the option they guide you towards on the Quick Start!


### Setting up LibreChat [\#](/blog/llm-chat-mcp-support#setting-up-librechat)


To install LibreChat, you’ll first need to clone the repository:



```

```
1git clone https://github.com/danny-avila/LibreChat.git
2cd LibreChat
```

```

The top\-level directory has a Docker compose file containing a service for LibreChat itself and ones for MongoDB, MeiliSearch, PGVector, and a LibreChat RAG image.


Before doing anything else, copy the example dummy file and add an API key for your preferred LLM.



```

```
1cp .env.example .env
```

```

Next, we’ll need to do the same thing with the example LibreChat YAML file:



```

```
1cp librechat.example.yaml librechat.yaml
```

```

You’ll then need to add a `docker-compose.override.yaml` file that mounts that file with the `api` service:



```

```
1services:
2  api:
3    volumes:
4      - ./librechat.yaml:/app/librechat.yaml
5    depends_on:
6      mcp-fetch:
7        condition: service_healthy
8      mcp-time:
9        condition: service_healthy
```

```

### Setting up MCP Servers with LibreChat [\#](/blog/llm-chat-mcp-support#setting-up-mcp-servers-with-librechat)


There are two ways to configure MCP Servers with LibreChat. You can install using the normal approach of providing your command and args in a config file, in this case, `librechat.yaml`:


For example, to add the [fetch MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch):



```

```
1mcpServers: fetch:
2    command: uvx
3    args: ["mcp-server-fetch"]
```

```

When the LibreChat container starts, these servers will start, and their lifespan will match the container's.


Alternatively, you can run your MCP Server in its own container. If you do this, you must ensure it can communicate over a non\-local transport mechanism (i.e., not stdio). Most MCP Servers only support stdio, but you can use `mcp-proxy` to make an MCP Server available over SSE. To do this, you can add the following to `docker-compose.override.yml`:



```

```
1mcp-fetch:
2    image: python:3.11-slim
3    container_name: mcp-fetch
4    ports:
5      - 8002:8080
6    extra_hosts:
7      - "host.docker.internal:host-gateway"
8    healthcheck:
9      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8080/sse')"]
10      interval: 10s
11      timeout: 5s
12      retries: 5
13      start_period: 30s
14    command: >
15      sh -c "
16        pip install uv mcp-proxy &&
17        mcp-proxy --port=8080 --host=0.0.0.0 --pass-environment uvx mcp-server-fetch
18      "
```

```

When launching an MCP Server like this, LibreChat will try to connect to it before its ready. We therefore need to have the LibreChat container wait until the health check passes, by adding the following to `docker-compose.override.yaml`:



```

```
1services:
2  api:
3    depends_on:
4      mcp-fetch:
5        condition: service_healthy
```

```

And then we’d add the following entry in `librechat.yaml`:



```

```
1mcpServers:
2  fetch:
3    type: sse
4    url: http://host.docker.internal:8002/sse
```

```

Once we’ve done all that, we’re ready to launch the stack:



```

```
1docker compose up
```

```

We should see the following lines in the logs indicating that the MCP Server has been successfully loaded:



```
LibreChat         | 2025-07-25 15:40:25 info: [MCP][fetch] Available tools: fetch
LibreChat         | 2025-07-25 15:40:28 info: [MCP] Initialized 1/1 app-level server(s)
LibreChat         | 2025-07-25 15:40:28 info: [MCP][fetch] ✓ Initialized
LibreChat         | 2025-07-25 15:40:28 info: MCP servers initialized successfully

```

We can then navigate to [http://localhost](http://localhost:3080) to try out LibreChat. Under the chat box, we should see a drop\-down titled ‘MCP Servers’ and the `fetch` tool should be listed:


![0_mcpapps.png](/uploads/0_mcpapps_deeab35222.png)
We can enable an MCP Server for the next conversation by selecting it. Only the selected MCP Servers will be used \- if an MCP Server is on the list but isn’t selected, it won’t be used.


Once we’ve selected fetch, we can ask a question requiring an HTML page to fetch. For example, we could ask for the main takeaways of the [Postgres/ClickHouse modelling tips blog post](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2):


![1_mcpapps.png](/uploads/1_mcpapps_b44a49d3c4.png)
It will first make several calls to the MCP Server to retrieve the page’s content:


![2_mcpapps.png](/uploads/2_mcpapps_a73b6d1e18.png)
And then it’ll compose an answer:


![3_mcpapps.png](/uploads/3_mcpapps_a86703fee3.png)
LibreChat stands out for its enterprise authentication features, comprehensive MCP implementation, and extensive customization options. The trade\-off is increased setup complexity, which best suits organizations with technical resources and multi\-user requirements.


➡️ [Learn how to use LibreChat with the ClickHouse MCP Server](https://clickhouse.com/docs/use-cases/AI/MCP/librechat)


## AnythingLLM [\#](/blog/llm-chat-mcp-support#anythingllm)


AnythingLLM is a document\-focused open\-source AI application that excels at RAG (Retrieval\-Augmented Generation) workflows. It offers a desktop app and web deployment options with comprehensive multi\-provider LLM support.


Its "workspaces" system organizes documents into isolated contexts, while features like vector caching and multi\-format document processing (PDFs, codebases, YouTube channels) make it ideal for knowledge\-intensive applications.


AnythingLLM provides solid MCP support through its AI Agents framework. stdio, SSE, and Streamable HTTP transports are managed via a user\-friendly configuration interface.


### Setting up AnythingLLM [\#](/blog/llm-chat-mcp-support#setting-up-anythingllm)


As mentioned above, AnythingLLM has a desktop application, but we will use the Docker image because that’s way more fun!


We need to set up a directory to store its metadata:



```
export STORAGE_LOCATION=$PWD/anythingllm && 
mkdir -p $STORAGE_LOCATION && 
touch "$STORAGE_LOCATION/.env"

```

### Setting up MCP Servers with AnythingLLM [\#](/blog/llm-chat-mcp-support#setting-up-mcp-servers-with-anythingllm)


Next, we’ll create a `plugins` directory:



```
mkdir -p "$STORAGE_LOCATION/plugins"

```

And create a file called `anythingllm_mcp_servers.json`. This time we’ll use the [`time`](https://playbooks.com/mcp/time) MCP Server, which can look up the current time for any place:



```

```
1{
2  "mcpServers": {
3    "time": {
4      "command": "uvx",
5      "args": ["mcp-server-time"]
6    }
7  }
8}
```

```

Now, we’re ready to start the AnythingLLM container:



```

```
1docker run -p 3001:3001 
2--cap-add SYS_ADMIN 
3-v ${STORAGE_LOCATION}:/app/server/storage 
4-v ${STORAGE_LOCATION}/.env:/app/server/.env 
5-e STORAGE_DIR="/app/server/storage" 
6mintplexlabs/anythingllm
```

```

Once that’s started, we can navigate to <http://localhost:3001/>.


To start MCP Servers in AnythingLLM, we need to navigate to the settings menu and then select `Agent Skills`:


![4_mcpapps.png](/uploads/4_mcpapps_f6ac99a6ae.png)
We can go to our workspace once our MCP Server has started. You can also control which MCP Servers are running from this page:


![5_mcpapps.png](/uploads/5_mcpapps_a8b830413a.png)
MCP Servers are only available in Agent mode, which we can enter by prefixing our message with `@agent`. You can select which MCP Servers are enabled at the app level, but there isn’t a way to control the available ones at a conversation level.


Let’s ask it to help us schedule a meeting across time zones:


![6_mcpapps.png](/uploads/6_mcpapps_ac0623690b.png)
It’ll work out the current time in each of those places:


![7_mcpapps.png](/uploads/7_mcpapps_769404a099.png)
Before coming up with a suggested meeting time:


![8_mcpapps.png](/uploads/8_mcpapps_8cf4b7fc2a.png)
AnythingLLM offers a simpler MCP setup process with its straightforward JSON configuration and built\-in management interface. However, I didn't immediately realize the `@agent` mode requirement for MCP functionality!


➡️ [Learn how to use AnythingLLM with the ClickHouse MCP Server](https://clickhouse.com/docs/use-cases/AI/MCP/anythingllm)


## Open WebUI [\#](/blog/llm-chat-mcp-support#open-webui)


Open WebUI is the most popular open\-source ChatGPT alternative, with over 100,000 GitHub stars. Built with strong Ollama integration and broad OpenAI\-compatible API support, it excels at local model deployment with advanced features like multi\-model conversations, built\-in RAG, voice/video calls, and a comprehensive pipelines framework for customization.


However, Open WebUI does not have native MCP support. Instead, it requires using their [`mcpo`](https://github.com/open-webui/mcpo) (MCP\-to\-OpenAPI proxy) to convert MCP servers into REST API endpoints that the platform can consume.


The `mcpo` approach transforms MCP's stdio\-based communication into HTTP REST endpoints, making MCP tools accessible through Open WebUI's existing tool integration system. While this adds an extra layer compared to native MCP implementations, it allows converting any MCP server into a standardized OpenAPI service that can be used across different platforms, not just Open WebUI.


### Setting up Open WebUI [\#](/blog/llm-chat-mcp-support#setting-up-open-webui)


To launch Open WebUI, we can run the following command:



```

```
1uv run --with open-webui open-webui serve
```

```

We can then navigate to [http://localhost/](http://localhost:8080/).


Open WebUI works with Ollama models by default, but we can also add OpenAI\-compatible endpoints. These are configured via the settings menu, and then we need to click on the **Connections** tab:


![9_mcpapps.png](/uploads/9_mcpapps_b14ce9bc0f.png)
And then let’s add the OpenAI endpoint and our OpenAI API key:


![10_mcpapps.png](/uploads/10_mcpapps_6ca0c66849.png)
### Setting up MCP Servers with Open WebUI [\#](/blog/llm-chat-mcp-support#setting-up-mcp-servers-with-open-webui)


As mentioned above, we must convert our MCP Servers into Open API endpoints. We’ll use the [ferdousbhai/investor\-agent](https://github.com/ferdousbhai/investor-agent) MCP Server for this example:



```

```
1uvx mcpo --port 8000 -- 
2uv run --with investor-agent --python 3.13 investor-agent
```

```

If we then go back to Open WebUI and go to the settings menu again, but this time click on `Tools`. We can click the `+` button and then add localhost as our URL:


![11_mcpapps.png](/uploads/11_mcpapps_29fac60b73.png)
Once we’ve done that, we’ll see a **1** next to the tool icon on the chat bar:


![20_mcpapps.png](/uploads/20_mcpapps_949e1b9933.png)
If we click on the spanner icon, we can see a list of available tools:


![12_mcpapps.png](/uploads/12_mcpapps_e67d431fb9.png)
Now, let’s ask it to compare Tesla and Apple’s valuations:


![13_mcpapps.png](/uploads/13_mcpapps_1dac7fd27e.png)
This time, we see the answer to the query first and some suggested follow\-up questions as well, which is a neat feature. The tool call is available as a citation underneath.


We can click on the tool call to see the query made and the response returned:


![14_mcpapps.png](/uploads/14_mcpapps_f02048b794.png)
Open WebUI offers the smoothest initial setup experience and most polished interface, but its MCP implementation requires running a separate proxy server (mcpo) as an intermediary step. While this adds complexity compared to native MCP support, the proxy approach does make MCP tools accessible through familiar REST endpoints.


The platform's focus on OpenAI\-compatible APIs means some LLM integrations aren't as seamless as Ollama\-native alternatives. However, this limitation is becoming less relevant as the industry standardizes around OpenAI's API format. Features like automatic follow\-up question suggestions showcase the platform's attention to user experience details.


➡️ [Learn how to use Open WebUI with the ClickHouse MCP Server](https://clickhouse.com/docs/use-cases/AI/MCP/open-webui)


## Chainlit [\#](/blog/llm-chat-mcp-support#chainlit)


Chainlit is a developer\-focused open\-source Python framework designed to build conversational AI applications and LLM\-powered chat interfaces with minimal code. Unlike ready\-to\-use applications like AnythingLLM, Open WebUI, or LibreChat, Chainlit requires Python programming to create custom chat applications.


It is ideal for developers who need complete control over their AI application logic and user experience. Chainlit handles the complexities of real\-time streaming, session management, and WebSocket communication, allowing developers to focus on AI logic rather than UI implementation.


Chainlit offers native MCP support through SSE and stdio transport. It features built\-in UI controls for server management and dedicated handlers (`@cl.on_mcp_connect` and `@cl.on_mcp_disconnect`) that enable seamless tool integration.


### Setting up Chainlit [\#](/blog/llm-chat-mcp-support#setting-up-chainlit)


This one requires a bit more setup, so you’ll have to clone the ClickHouse/examples repository:



```

```
1git clone https://github.com/ClickHouse/examples.git
2cd examples/ai/mcp/chainlit
```

```

You can run a basic Chainlit app without MCP Server support by running the following:



```

```
1uv run --with anthropic --with chainlit chainlit run chat_basic.py -w -h
```

```

### Setting up MCP Servers with Chainlit [\#](/blog/llm-chat-mcp-support#setting-up-mcp-servers-with-chainlit)


Depending on which MCP Server you’re running, you might need to update your `.chainlit/config.toml` file to allow the `uv` command to be used:



```

```
1[features.mcp.stdio]
2    enabled = true
3    # Only the executables in the allow list can be used for MCP stdio server.
4    # Only need the base name of the executable, e.g. "npx", not "/usr/bin/npx".
5    # Please don't comment this line for now, we need it to parse the executable name.
6    allowed_executables = [ "npx", "uvx", "uv" ]
```

```

There's some [glue code to get MCP Servers working with Chainlit](https://github.com/ClickHouse/examples/blob/main/ai/mcp/chainlit/chat_mcp.py#L20), so we'll need to run this command to launch Chainlit instead:



```

```
1uv run --with anthropic --with chainlit chainlit run chat_mcp.py -w -h
```

```

Then we can navigate to localhost. MCP Servers in Chainlit are configured via the UI by clicking the plug icon.


![15_mcpapps.png](/uploads/15_mcpapps_dd2592e6ca.png)
We then enter the command for our MCP Server, providing any environment variables as part of that command. Chainlit stores the details of our MCP servers in the browser’s local storage.


For example, to install [/erithwik/mcp\-hn](https://github.com/erithwik/mcp-hn) we would type `uvx mcp-hn` in the `Command` field. We can then ask a question about Hacker News:


![16_mcpapps.png](/uploads/16_mcpapps_46b92de9ee.png)
Chainlit has identified that it needs to call `get_stories,` and that’s what it does next:


![17_mcpapps.png](/uploads/17_mcpapps_2ad0604f4e.png)
We can see the output of the tool call:


![18_mcpaps.png](/uploads/18_mcpaps_b5a94b14d7.png)
And then finally, the response:


![19_mcpapps.png](/uploads/19_mcpapps_ffa0c8e6b4.png)
Chainlit's code\-first approach provides the most flexibility for developers building custom AI applications. Unlike the other platforms, it requires Python programming knowledge and custom code to handle MCP integration.


The framework only supports single conversations rather than persistent chat history. However, its ability to launch MCP servers directly from the UI is particularly convenient, and the local storage approach simplifies deployment without needing external databases or complex configurations.


➡️ [Learn how to use Chainlit with the ClickHouse MCP Server](https://clickhouse.com/docs/use-cases/AI/MCP/open-webui)


## The ClickHouse MCP Server [\#](/blog/llm-chat-mcp-support#the-clickhouse-mcp-server)


When evaluating chat UIs that support MCP, ClickHouse offers a practical example of connecting to external data systems. Many chat interfaces work well for general tasks, but ClickHouse's MCP server shows how these tools can integrate with actual databases and analytical workflows.


If you're comparing MCP\-enabled chat applications, the ClickHouse integration provides a straightforward way to test how well each interface handles data queries, maintains context across multiple questions, and presents query results.


It's a useful benchmark because it represents a common real\-world scenario: connecting your chat interface to existing data infrastructure. Whether you're working with event logs, user analytics, or business metrics, the ClickHouse MCP server demonstrates the practical value of having your chat UI connect to live data sources rather than just relying on its training data.


The ClickHouse MCP Server integrates with all the chat apps we’ve discussed, and detailed walkthroughs are included in our [MCP guides documentation](https://clickhouse.com/docs/use-cases/AI/MCP).


## In conclusion [\#](/blog/llm-chat-mcp-support#in-conclusion)


Each platform covered offers a different balance of usability, flexibility, and MCP support.


LibreChat stands out for its enterprise\-grade features and full native MCP integration, making it an excellent choice for complex, multi\-user environments. AnythingLLM provides a more guided setup and excels in document\-based RAG use cases. Open WebUI trades native support for OpenAPI adaptability via `mcpo`, while Chainlit offers the most developer control for building custom, code\-first experiences.


If you're working with ClickHouse or integrating real\-time data workflows, any of these apps can serve as a front end for the ClickHouse MCP Server \- it's just a matter of choosing the right tool for your project’s scale and complexity.


Whether you're deploying locally or orchestrating microservices in production, the growing MCP ecosystem makes bringing external tools into the chat loop easier than ever.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

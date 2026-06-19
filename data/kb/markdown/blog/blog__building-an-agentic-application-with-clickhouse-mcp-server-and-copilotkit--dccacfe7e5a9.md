# Building an agentic app with ClickHouse MCP and CopilotKit


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building an agentic app with ClickHouse MCP and CopilotKit

![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin)Jun 12, 2025 · 13 minutes readSearching for your new house, you’re trying to understand the price trends in the neighborhood. Imagine that instead of browsing through pre\-defined charts, clicking through filters and dropdowns to get the information you’re interested in, you could just ask:


**“Show me the price evolution in Manchester for the last 10 years.”**


And it just responds with a chart, an explanation, and maybe even follow\-up questions.


![agentic-application-animation-2.gif](/uploads/agentic_application_animation_2_6098bb8a92.gif)
That is the promise of Agentic applications. Powered by Large Language Models (LLMs), they can reason through complex tasks, call APIs, and build entire workflows from a single user prompt, making them intelligent, interactive user experiences.


Watch our customer panel discuss the potential of MCP in real\-time analytics applications in this video.



  

In this blog, we will show how to build one. We will create a build\-your\-own analytics dashboard experience for the UK real estate market using [ClickHouse MCP Server](https://github.com/ClickHouse/mcp-clickhouse) and [CopilotKit](https://www.copilotkit.ai/). This example is built using React with Next.js, but the same approach can be used with any modern application framework.


## Components of the Agentic application [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#components-of-the-agentic-application)


Let’s start by going through the components of an agentic application.


### Large language model [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#large-language-model)


At the core of any agentic application is a [Large Language Model](https://en.wikipedia.org/wiki/Large_language_model) (LLM). The LLM interprets user prompts, understands context, generates responses, and decides what actions to take.


For a smooth and responsive experience, it is essential to use a capable model with fast performance and a reasonably large context window. Agentic applications often deal with complex prompts, interact with external tools, and use data from third\-party systems. As more information is added to the context, the model must process it efficiently and respond quickly. This is what enables an interactive and natural experience for the end user.


In our example, we use the model Claude Sonnet 3\.7 from [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models/overview). When writing this blog, it was one of the best\-performing on [TAU\-bench](https://arxiv.org/abs/2406.12045) for the [airline](https://hal.cs.princeton.edu/taubench_airline) and [retail](https://hal.cs.princeton.edu/taubench_retail) use case, a benchmark that aims to rank LLMs on their interaction with human users and ability to follow domain\-specific rules.


### ClickHouse MCP Server [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#clickhouse-mcp-server)


Our agentic application is going to help users analyze the UK real estate market data by building their custom dashboard. While the market data is [public](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads) and the model may have seen it in pre\-training, that information is stored in the model’s weights, not as exact records. This means that even if the model has seen some of the data, there’s a chance it’ll make up some numbers if we asked questions about property in the UK. In many cases, the model will need access to live or proprietary data sources to provide accurate and useful insights.


This is the purpose of a [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (MCP) server, an open standard that enables developers to build secure, two\-way connections between their data sources and AI\-powered tools.


[ClickHouse MCP server](https://github.com/ClickHouse/mcp-clickhouse) enables developers to integrate ClickHouse inside their agentic application, allowing the application to query data directly from the application.


### CopilotKit [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#copilotkit)


The third core component in this setup is [CopilotKit](https://www.copilotkit.ai/) which is a UI framework designed to simplify the development of agentic applications.


I chose to use CopilotKit for this project because it abstract away several complex aspects of the architecture. It provides built\-in support for the chat interface, connects easily with different LLMs, and manages tool calls or UI actions that the model can decide to perform.


Next, we will see how each of these components works together.


## High level architecture [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#high-level-architecture)


Let’s walk through the flow triggered by a user request. This example illustrates how the components interact to turn a natural language prompt into a fully rendered chart.


![agentic-application-diagram-1.png](/uploads/agentic_application_diagram_1_8a6a2d7d2a.png)
1. The user sends the following prompt: “Show me the price evolution in Manchester for the last 10 years.”
2. The prompt, along with the list of available actions and state variables, is sent to the CopilotKit runtime.
3. CopilotKit enriches the prompt with the list of MCP resources, then forwards it to the LLM. The LLM analyzes the prompt and available resources, determines that it needs to retrieve data, and generates a SQL query targeting ClickHouse.
4. The CopilotKit runtime uses the MCP client to send the query request.
5. MCP Client calls the ClickHouse MCP Server with the SQL query to retrieve the price data in the Manchester area for the last 10 years.
6. The data is returned to the LLM along with the current context. The model identifies the generateChart action and prepares the response by formatting the data according to the expected chart parameters.


This flow highlights how the different parts of the agentic application work together. The model interprets the user’s prompt, fetches data using ClickHouse through the MCP Server, and updates the UI by calling predefined actions.


## How to build the Agentic application [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#how-to-build-the-agentic-application)


Now that we’ve covered how the application works at a high level, let’s go through a step\-by\-step guide to building it from scratch.


This section focuses only on the important part of the implementation. For a fully working example, look at the example in [this Github repository](https://github.com/ClickHouse/examples/tree/main/ai/mcp/copilotkit).


### Initialize the application [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#initialize-the-application)


We start by creating a new React application and initializing it with the CopilotKit framework. To do this, we use the [npx helper](https://docs.npmjs.com/cli/v8/commands/npx) to bootstrap the project. When prompted about how the application will interact with the model, be sure to select the MCP option.



```

```
1npx create-next-app@latest
2cd agentic-app
3npx copilotkit@latest init
```

```

### Bring your own LLM [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#bring-your-own-llm)


By default, OpenAI is configured by CopilotKit. We can swap with another model if we wish to, [here](https://docs.copilotkit.ai/direct-to-llm/guides/bring-your-own-llm) is the list of models supported by Copilotkit.


The connection to the LLM happens on the server side, by default CopilotKit exposes an API route that the client integrates with to interact with the LLM.


Edit the file `./app/api/copilotkit/routes.ts` to swap the model.



```

```
1import { AnthropicAdapter } from "@copilotkit/runtime";
2
3// const serviceAdapter = new OpenAIAdapter()
4const serviceAdapter = new AnthropicAdapter({model: "claude-3-7-sonnet-latest"});
```

```

Don’t forget to provide the API key (`ANTHROPIC_API_KEY`) as an environment variable.


### Deploy the ClickHouse MCP Server [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#deploy-the-clickhouse-mcp-server)


In this example, we deploy the ClickHouse MCP Server locally, but it is also possible to deploy it remotely and have multiple MCP clients connect to it.



> Soon, ClickHouse Cloud will offer a remote MCP server as a default interface. That means any MCP client could connect directly to your cloud instance without additional local setup.
> 
> 
> Want early access? [Sign up for the AI features waitlist at clickhouse.ai](http://clickhouse.ai).



```

```
1# Clone the ClickHouse MCP Server repository
2git clone https://github.com/ClickHouse/mcp-clickhouse
3# Install dependencies
4python3 -m venv .venv && source .venv/bin/activate && uv sync && uv add fastmcp
5# Configure connection to ClickHouse database 
6export CLICKHOUSE_HOST="sql-clickhouse.clickhouse.com"
7export CLICKHOUSE_USER="demo"
8export CLICKHOUSE_SECURE="true"
9export CLICKHOUSE_PORT="8443"
10# Run the MCP server and expose SSE transport protocol
11fastmcp run mcp_clickhouse/mcp_server.py:mcp --transport sse
```

```

For this demo, we’re using the ClickHouse [SQL Playground](https://sql.clickhouse.com), which includes the [UK market dataset](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid).


Finally, we use the [fastmcp](https://gofastmcp.com/deployment/running-server#the-fastmcp-cli) command to start the MCP server and expose it using SSE transport, by default, on port 8000\.


### Configure the MCP Client [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#configure-the-mcp-client)


CopilotKit comes with built\-in [support](https://docs.copilotkit.ai/direct-to-llm/guides/model-context-protocol?cli=do-it-manually) for MCP client, we just need to configure the connection so it can access it.


Edit the file `./app/copilotkit/page.tsx` to add the ClickHouse MCP Server connection.



```

```
1useEffect(() => {
2    setMcpServers([
3      { endpoint: "http://localhost:8000/sse" },
4    ]);
5 }, []);
```

```

### Create the agent actions [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#create-the-agent-actions)


The main promise of an agentic application is that it can take actions on behalf of the user, guided by their conversation.


In our case, the goal is for the application to generate custom charts based on the user's description. This is the action we need to describe so the LLM can perform it.


For this, we're going to use the CopilotKit hook [useCopilotAction](https://docs.copilotkit.ai/reference/hooks/useCopilotAction). This hook lets developers define custom actions that the model can invoke. In our example, the action is to add a new chart configuration.


We are also going to leverage another hook: [useCopilotReadable](https://docs.copilotkit.ai/reference/hooks/useCopilotReadable), which allows us to share a state variable from the application with the model. Here, we make the chart configuration array available to the model.


To set this up, edit the file `./app/copilotkit/page.tsx` to define the new action and make the charts state variable available to the model.



```

```
1// Chart configuration array 
2const [charts, setCharts] = useState<Chart[]>([]);
3
4// Share the charts state variable with LLM
5useCopilotReadable({
6  description: "These are all the charts props",
7  value: charts,
8});
9
10// Create a new action generateChart that will be used by the LLM to create the correct chart configuration and add it to the state variable. 
11useCopilotAction({
12    name: "generateChart",
13    description: "Generate a chart based on the provided data. Make sure to provide the data in the correct format and specify what field should be used a x-axis.",
14    parameters: [
15        {
16            name: "data",
17            type: "object[]",
18            description: "Data to be used for the chart. The data should be an array of objects, where each object represents a data point.",
19        },
20        {
21            name: "chartType",
22            type: "string",
23            description: "Type of chart to be generated. Lets use bar, line, area, or pie.",
24        },
25        {
26            name: "title",
27            type: "string",
28            description: "Title of the chart. Cant be more than 30 characters.",
29        },
30        { name: "xAxis", type: "string", description: "x-axis label" }
31    ],
32
33    handler: async ({ data, chartType, title, xAxis }) => {
34        const newChart = {
35            data,
36            chartType,
37            title,
38            xAxis
39        };
40        setCharts((charts) => [...charts, newChart] );
41    },
42    render: "Adding chart...",
43});
```

```

Then we need to add a DynamicGrid component to iterate through the chart configuration array and build the charts for each of them.



```

```
1function DynamicGrid({ charts }: { charts: Chart[] }) {
2return (
3      charts.map((chart, index) => (
4      <div className="flex flex-col gap-4" key={index}>
5              <p className="text-white whitespace-nowrap overflow-hidden text-overflow-ellipsis text-xl leading-[150%] font-bold font-inter">{chart.title}</p>
6              <GenericChart {...chart} />
7          </div>
8      ))
9  )
10}
```

```

The GenericChart component uses the [echart](https://echarts.apache.org/examples/en/index.html) for react chart library, but you can easily swap for your preferred ones. You can see the code for the GenericChart component [here](https://github.com/ClickHouse/examples/blob/copilotkit/ai/mcp/copilotkit/components/GenericChart.tsx).


### Final result [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#final-result)


We’ve covered the key parts of the implementation. From here, it’s mostly a matter of adding some styling to make the application look polished. The full source code can be found on [Github](https://github.com/ClickHouse/examples/tree/main/ai/mcp/copilotkit).


## Benefits of using ClickHouse in an Agentic application [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#benefits-of-using-clickhouse-in-an-agentic-application)


### Real\-time analytics database [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#real-time-analytics-database)


Using a real\-time analytics database like ClickHouse is essential for this type of agentic application.


![benefit-db-ai-agents.png](/uploads/benefit_db_ai_agents_c7a5f47245.png)
Real\-time analytics databases have properties that make them well\-suited for Agentic application workload. They work with near real\-time data, allowing systems to incorporate the latest information as it arrives. This supports agents that need to make or support timely decisions.


These databases are also built for complex analytical tasks such as aggregations, trend analysis, and anomaly detection across large datasets. Unlike operational databases, they are optimized for extracting insights rather than simply storing or retrieving raw records.


Finally, they support interactive querying at high frequency and under high concurrency. This ensures stable performance during chat\-based interactions and exploratory data work, contributing to a smoother and more responsive user experience.


### Fine grained permissions and quotas [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#fine-grained-permissions-and-quotas)


One of the main challenges when building agentic applications is maintaining control over what the LLM is allowed to do on your behalf. This becomes especially important when the model has access to query a production database through a MCP server.


Fortunately, ClickHouse offers a wide range of [permissions](https://clickhouse.com/docs/operations/access-rights) and [quotas](https://clickhouse.com/docs/operations/quotas) making it straightforward to control exactly what the MCP server can expose to the model.


In this example, we're using the SQL Playground to host the UK Market dataset. We have configured the MCP Server to authenticate to the Playground using the demo user. You can see the configuration of this user [here](https://github.com/ClickHouse/sql.clickhouse.com/blob/main/setup.sql).


The demo user has read\-only access and is restricted to a specific set of databases. This allows us to limit the data the LLM can reach. On top of that, we apply quota settings and assign a limited profile to the user to prevent the model from overloading the server with too many or overly expensive queries. This setup gives us fine\-grained control over both the scope and cost of what the model can do.


## Conclusion [\#](/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit#conclusion)


In this blog post, we explored how to build an agentic application using ClickHouse MCP Server and CopilotKit.


By leveraging the capabilities of LLMs, we created an application that allows users to build their own analytics dashboard on UK market data.


The use of a fast, scalable and secure analytics database like ClickHouse is crucial for the efficiency and effectiveness of such applications. This approach opens up new possibilities for creating AI\-powered tools that provide deeper insights and better user experiences.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

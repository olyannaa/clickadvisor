# Define once, use everywhere: a metrics layer for ClickHouse with MooseStack


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Define once, use everywhere: a metrics layer for ClickHouse with MooseStack

![](/_next/image?url=%2Fuploads%2Ffiveonefour_avatar_8b25b9739c.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fnakulbio_3533dbd36d.jpg&w=96&q=75)[Fiveonefour](/authors/fiveonefour) and [Nakul Mishra (AWS)](/authors/nakul-mishra)Mar 13, 2026 · 11 minutes readLet’s say you’re tracking data on revenue in your ClickHouse database. Metrics about revenue might be served up to interested parties in a variety of places: BI tools, custom dashboards, API endpoints, agentic tools, MCP servers, AI chat, etc. Are the numbers the same in every place? Maybe, maybe not. When the same metric is re\-defined in multiple locations (or generated on the fly by an LLM), it's easy for that definition to skew. It happens more often than you might think.


The below example is based on something we saw at one of our customers: their custom chat client vibe\-SQLed a definition of revenue that made sense (sum of `amount`), but didn’t exclude transactions that were incomplete (Figure A: chat overstates revenue). That kind of mistake becomes impossible with a well\-defined metrics layer (Figure B: chat matches actual revenue).

Previous slide\<\-Next slide\-\>![](/_next/image?url=%2Fuploads%2F1_cdd0a13188.png&w=3840&q=75)![](/_next/image?url=%2Fuploads%2F2_0e4864ac05.png&w=3840&q=75)![](/_next/image?url=%2Fuploads%2F1_cdd0a13188.png&w=384&q=75)![](/_next/image?url=%2Fuploads%2F2_0e4864ac05.png&w=384&q=75)*Image 1 shows chat going rogue on the definition of revenue. Image 2 shows how the metrics layer keeps everything consistent.*


When I was at Nike, we had to work hard to make sure this didn’t happen just across our APIs. Now, there’s APIs, dashboard, chats and AI, MCP… The surface area for inconsistency has multiplied.


And what happens when we need to change that definition? We end up with two problems:


1. Metrics need to be consistent everywhere. Same definition, same answer, across chat, APIs, dashboards, and MCP. One mistake kills credibility.
2. Metrics need to be easy to define and change safely. Add a metric once, update it once, and have every surface stay in sync when the schema changes. The developer experience needs to be better than manually crafting all this.


In this post, we’ll introduce an approach for a lightweight metrics layer (or “query layer” or “semantic layer”) on top of ClickHouse. We’ll use MooseStack, an open source developer agent harness for ClickHouse, to implement our metrics layer in code, where our coding agents can help accelerate the process.


If you want to jump straight into some sample code, check out [the repo for the demo app](https://github.com/514-labs/financial-query-layer-demo) that you can see in the screenshots above. If you want to go straight to implementing this yourself, check out [the docs](https://docs.fiveonefour.com/moosestack/reference/query-layer) or the [tutorial guide](https://docs.fiveonefour.com/guides/chat-in-your-app/tutorial).


## Define once, project everywhere [\#](/blog/metrics-layer-with-fiveonefour#define-once-project-everywhere)


There are a bunch of semantic / metric layer approaches out there that all have their own advantages and disadvantages (take cube.dev, dbt metrics, MetricFlow, Looker; and frontend first approaches like TanStack Table and AG Grid).


The approach we’ll cover today doesn’t rely on external systems or human processes for correctness: it's an as\-code metrics layer. Define your metrics once in code. Project them to every surface.


A metric has three components:


1. The aggregation: the SQL expression (what to calculate). `SUM(amount)`, `COUNT(DISTINCT user_id)`, `AVG(duration)`.
2. Dimensions: what to group by (how to slice it). Region, month, status. Column keys or SQL expressions.
3. Filters: what constraints are valid (how to scope it). Which columns can be filtered, which operators are allowed.


These three components assemble into any query your surfaces need. "Revenue by region this quarter" becomes: aggregation \= `sumIf(amount, status = 'completed') AS revenue`, dimension \= `region`, filter \= `timestamp >= Q1 start`.


Another benefit is that multiple metrics can share the same dimensions and filters. That helps keep not just business logic consistent, but also grain: how data is sliced, grouped, and compared.


The query model is the source of truth. Each surface consumes it differently:


- First party chat: the model constrains which metrics the LLM can query. No freestyle SQL. The model is the guardrail. (When you build your own chat, you have much more control over the user experience, including how tools are called).
- MCP: the model becomes a tool definition. Same metrics in Claude Desktop, Cursor, any agent client.
- API: the model generates parameterized SQL. Deterministic. No LLM in the loop.
- Dashboard: the model's metadata drives the UI. Dimension pickers, metric selectors, filter controls.


[The demo application covers all of these with some toy data, so you can see how metrics are defined, and how they interact with these different surfaces.](https://github.com/514-labs/financial-query-layer-demo)


## A type\-safe query model [\#](/blog/metrics-layer-with-fiveonefour#a-type-safe-query-model)


Let’s assume you are doing your data modeling in ClickHouse, and want *everything* as easy, type\-safe code, that comes with a developer harness (dev MCP, skills etc.) to make it easy to work with. If you want to implement metrics with the approach above, you can use [MooseStack's](https://github.com/514-labs/moosestack) open source `QueryModel`.


![3.png](/uploads/3_d129fddf9a.png)QueryModels take Data Model objects as inputs, that represent ClickHouse tables (`OlapTable`), Views (`View`) or Materialized Views (`MaterializedView`), and let you define metrics, dimensions, and filters on top.


```
1// The data model — defines the table schema 
2interface EventModel {
3  /** When the event occurred */
4  // MooseStack propagates JSDocs describing the tables and columns 
5  // to ClickHouse as comments 
6  event_time: Date;
7  /** Unique identifier for the user who triggered the event */
8  user_id: string;
9  /** Lifecycle state: active, completed, or refunded */
10  status: "active" | "completed" | "refunded";
11  /** Geographic region where the event originated */
12  region: string;
13  /** Transaction value in USD */
14  amount: number;
15}
16
17// The OlapTable — typed reference to the ClickHouse table
18export const Events = new OlapTable<EventModel>("events", {
19  orderBy: "event_time",
20});
21
22// Your query model — references the data model directly
23export const eventsModel = defineQueryModel({
24  name: "events",
25  description: "Event analytics: user activity and engagement metrics",
26  table: Events,  // <-- typed reference to the OlapTable
27
28  dimensions: {
29    region: { column: "region", description: "Geographic region" }, 
30    day: {
31      expression: sql.fragment`toDate(${Events.columns.event_time})`,  // <-- Column object, not a string 
32      as: "time", 
33      description: "Daily time bucket",
34    },
35    month: {
36      expression: sql.fragment`toStartOfMonth(${Events.columns.event_time})`,
37      as: "time",
38      description: "Monthly time bucket",
39    },
40  },
41
42  metrics: {
43    totalEvents: { agg: sql.fragment`count(*)`, description: "Total number of events" },
44    totalAmount: { agg: sql.fragment`sum(${Events.columns.amount})`, description: "Sum of all event amounts" },  // <-- Column object
45    uniqueUsers: { agg: sql.fragment`uniq(${Events.columns.user_id})`, description: "Distinct users" },  // <-- Column object
46  },
47
48  filters: {
49    timestamp: { column: "event_time", operators: ["gte", "lte"] as const },  // <-- typed against EventModel keys
50    region: { column: "region", operators: ["eq", "in"] as const },
51  },
52
53  sortable: ["totalAmount", "totalEvents", "uniqueUsers"] as const,
54});
```
### Type safety back to the table [\#](/blog/metrics-layer-with-fiveonefour#type-safety-back-to-the-table)


Since metrics are built on Data Models, you get type\-safety end\-to\-end. In the example below, dimensions and filters are generic over `keyof Transaction`. Metrics reference `TransactionTable.columns.totalAmount` (a `Column` object, not a string). Rename or remove a field in your data model and the query model gets a compile error, not a silent wrong answer in production.


![4.png](/uploads/4_e21e0fc3f9.png)Here, I changed `totalAmount` to `total_Amount` (ugh) and you can see all the dependent query models show the type\-error. That keeps the metrics layer and the ClickHouse tables defined in code necessarily in sync.


### One definition, every surface [\#](/blog/metrics-layer-with-fiveonefour#one-definition-every-surface)


The same `eventsModel` object then becomes a chat tool, an MCP tool, and an API:



```

```
1// Chat — Vercel AI SDK tool
2const tool = createModelTool(transactionMetrics);
3// tool.schema has the zod params, tool.buildRequest parses them, transactionMetrics.toSql generates the query
```

```


```

```
1// MCP — register as tool for Claude Desktop, Cursor, etc.
2registerModelTools(server, [transactionMetrics], mooseUtils.client.query);
```

```


```

```
1// REST API — deterministic SQL, no LLM
2const data = await buildQuery(transactionMetrics)
3  .metrics(["revenue"])
4  .dimensions(["region"])
5  .orderBy(["revenue", "DESC"])
6  .execute(client.query);
```

```

Add a metric to the model, it shows up on every surface.


### Metrics are still code [\#](/blog/metrics-layer-with-fiveonefour#metrics-are-still-code)


Importantly, it's not a config of a dashboard, or a fingers crossed attempt at prompt engineering.


Your metric definitions go through the same PR review, CI, and deployment pipeline as everything else.


## The dev harness in action [\#](/blog/metrics-layer-with-fiveonefour#the-dev-harness-in-action)


MooseStack isn’t just a developer framework. The framework and the tooling surrounding it (the dev MCP, the skills, the CLI) make up the dev agent harness ([the guide will walk you through setting it up](https://docs.fiveonefour.com/guides/chat-in-your-app/tutorial?lang=typescript)). This agent harness turns your regular coding agent (Claude Code, Cursor, etc) into a ClickHouse specialist, which can drastically accelerate your implementation of a metrics layer.


Once the harness is ready, one prompt can add a metric:



```
"Add a revenue metric. Revenue is the sum of amount for completed events only."

```

The dev harness knows your data models and your query models. It adds the metric using TypeScript and moose\-lib to extend the query model object.


### The diff [\#](/blog/metrics-layer-with-fiveonefour#the-diff)



```
metrics: {
  totalTransactions: {
    agg: count(),
    as: "totalTransactions",
    description: "Total transaction count across all statuses",
  },

  completedTransactions: {
    agg: sql`countIf(${TransactionTable.columns.status} = 'completed')`,
    as: "completedTransactions",
    description: "Count of completed (settled) transactions",
  },

+ revenue: {
+   agg: sql`
+     sumIf(
+       ${TransactionTable.columns.totalAmount},
+       ${TransactionTable.columns.status} = 'completed'
+     )
+   `,
+   as: "revenue",
+   description: "Total revenue from completed transactions only",
+ },
},

```

One edit only: add the metric to the model, and it propagates across all existing query surfaces.


### Check the blast radius [\#](/blog/metrics-layer-with-fiveonefour#check-the-blast-radius)


The infra map shows every surface that consumes `transactionMetrics`, which the agent can retrieve with the MooseDev MCP infra map tool call:



```

```
1$ get_infra_map search="transactionMetrics"
2
3Components:
4  WEB_APP  /tools               → pulls_data_from: [transactions]   # MCP tools (registerModelTools)
5  WEB_APP  /revenue/by-region   → pulls_data_from: [transactions]   # Dashboard API (buildQuery)
6  WEB_APP  /transaction/metrics → pulls_data_from: [transactions]   # Report builder API (buildQuery)
7  CHAT     /api/chat            → pulls_data_from: [/tools]         # Chat UI (AI SDK → MCP client)
```

```

Four surfaces. The new `revenue` metric is now available on all of them. Chat users can ask for it. MCP clients can query it. The API endpoint can serve it. The dashboard can display it.


### Validate the SQL [\#](/blog/metrics-layer-with-fiveonefour#validate-the-sql)


Call the MCP tool with "revenue by region this quarter" and inspect the generated SQL:



```

```
1SELECT
2    region,
3    sumIf(totalAmount, status = 'completed') AS revenue  -- constraint from the metric definition
4FROM transactions
5WHERE timestamp >= toStartOfQuarter(now())
6     AND timestamp <= now()
7GROUP BY region
8ORDER BY revenue DESC
```

```

The `sumIf` came from the metric definition. The `WHERE` came from the filter. The `GROUP BY` came from the dimension. Nothing was improvised. The model produced the SQL, and you can read it to verify.

Loading video...## Putting Metrics into practice [\#](/blog/metrics-layer-with-fiveonefour#putting-metrics-into-practice)


A query model only helps if your team treats it as the contract for production analytics. What we recommend is a practice like:


**Ad\-hoc SQL for discovery. Query model for production.**


Chat in your product, dashboard cards, report APIs, MCP tools exposed to users or internal teams: all of those should consume the same model. That is how "revenue" stops being three implementations and becomes one definition.


Freeform chat/chat\-to\-SQL still has a place. We keep it for development, exploration, debugging, and analyst/admin workflows. But that is a discovery path, not a production path. Once a number matters enough to appear in a product surface, it gets promoted into the query model.


In practice, adoption looks like this:


- **Exploration first.** A developer, analyst, or PM asks a question in chat or writes an ad hoc query.
- **Codify the metric.** Once the definition is useful and stable, it gets added to `defineQueryModel()`.
- **Project it everywhere.** Chat tools, MCP tools, APIs, and dashboards all consume that definition.
- **Review it like code.** Changes to metric definitions go through PR review, tests, and normal deployment.
- **Limit bypass paths.** Production surfaces do not ship hand\-written SQL for metrics that already exist in the model.


This is where the "as code" part matters. The model is not just a convenience for generating SQL. It gives the team a shared artifact to review, version, and own. Product’s definition is in that code, not in a document. Engineering refers to the same code for analytical feature development. Agents can consume it.


The goal is not to eliminate ad hoc analysis, but to make sure ad hoc analysis is not the thing your product depends on.


That is the adoption pattern we think works best: **explore freely, standardize deliberately, serve consistently.**


## Try it out [\#](/blog/metrics-layer-with-fiveonefour#try-it-out)


One `defineQueryModel()`. Type\-safe back to your tables and views. Chat, MCP, and API from the same definition. The dev harness builds it. The type system keeps it in sync. Code review and SDLC keeps it safe. Try it out yourself:


- [**The guide**](https://docs.fiveonefour.com/guides/chat-in-your-app/tutorial?lang=typescript)**.** Step\-by\-step from zero to production: data models, query models, query builder, chat, MCP, brownfield setup (`moose init --from-remote`), auth, and deployment.
- [**The demo app**](https://github.com/514-labs/financial-query-layer-demo)**.** Check out the example implementation, including frontend with dashboard, AI chat, and report builder.
- [**Start from 514 Hosting**](https://fiveonefour.boreal.cloud/sign-up)**.** Sign up for Fiveonefour, get a hosted ClickHouse backend, and deploy with preview branches and schema migration support. 514 Hosting proudly uses ClickHouse Cloud.


### Acknowledgements [\#](/blog/metrics-layer-with-fiveonefour#acknowledgements)


Thanks to Nakul Mishra from AWS for feedback on the post, and for validating the Fiveonefour agent harness with AWS’s agentic coding IDE, Kiro \- including the newly developed [Kiro Power for ClickHouse](https://github.com/nklmish/clickhouse-kiro-power). Nakul’s views and opinions are Nakul’s own.


Thanks to MooseStack / ClickHouse community members Lukáš Kozelnický and Michael Klein for the hands\-on feedback, and the F45 team, Loyalsnap team and Oliver Naaris for feedback on the demo.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

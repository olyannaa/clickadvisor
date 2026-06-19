# AI\-powered migrations from Postgres to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# AI\-powered migrations from Postgres to ClickHouse

![](/_next/image?url=%2Fuploads%2Ffiveonefour_avatar_8b25b9739c.png&w=96&q=75)[Fiveonefour](/authors/fiveonefour)Feb 17, 2026 · 18 minutes read
> **TL;DR:**
> AI can drastically accelerate migrating analytical workloads from Postgres to ClickHouse. To set your agents up for success, give them the right environment:
> 
> 
> 1. Code: keep everything in code, it’s your agent’s comfort zone
> 2. Cadence: enable fast, safe feedback loops
> 3. Context: inject ClickHouse best practices via agent skills and references
> 
> 
> Wrap it all up in an agent harness like [MooseStack](https://github.com/514-labs/moosestack) to avoid AI slop.
> 
> 
> Want to jump right to implementation? Here's a practical, step\-by\-step [guide](https://docs.fiveonefour.com/guides/performant-dashboards/tutorial).

Your dashboards are starting to crawl. Postgres is choking on your analytical queries. You know that Postgres with ClickHouse is the answer. You want to keep Postgres for your transactional workloads, but offload your analytical workloads onto ClickHouse. You want that vision of the unified data stack: Postgres \+ ClickHouse, working seamlessly in tandem, with the right tool used for the right job.


So how do you go about actually migrating your analytical workloads from Postgres to ClickHouse? You want AI to do the heavy lifting. We agree. But most AI\-assisted migrations produce garbage. We’ve learned this the hard way migrating thousands of customer tables and queries.


This post explores how to make your AI agents *actually effective* at offloading analytics from Postgres to ClickHouse.


![Opening-top.png](/uploads/Opening_top_7b2eeacfcb.png)
*An AI agent effectively implementing ClickHouse best practices*### Try the unified data stack

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-68-try-the-unified-data-stack-get-access&utm_blogctaid=68)## ClickHouse Migrations: Simple vs Reality [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#clickhouse-migrations-simple-vs-reality)


If you’re just building a toy or a POC, your standard AI agent can probably do a decent job. The challenge comes when you’re building something real. Real is complex and full of edge cases and baggage. And you don’t just want “functional”: you need integrated, scalable, reliable, and blazing fast. That means carefully considering the nuances and specializations of the system.


If you want the best out of ClickHouse in your production application, then you’re looking at (1\) rearchitecting data models for OLAP performance, (2\) rebuilding read\-time joins and aggregations into write\-time Materialized Views, (3\) optimizing queries in your APIs, and (4\) propagating and testing changes through to your frontend components.


So, the question isn’t just “can my agent write ClickHouse SQL?”. It’s “can I give my agent everything it needs to work effectively within the complex environment of my integrated application stack?” To pull this off, you need to expose all the interfaces, tools, skills, code and context to your agent that are needed to rapidly and safely iterate to success. In other words: you need an “agent harness” for Postgres \+ ClickHouse.


![Agentic-Harness-dark.png](/uploads/Agentic_Harness_dark_1b04481cd8.png)
Of course you can architect this harness yourself, but throughout this post, we’ll demonstrate how to leverage [MooseStack](https://github.com/514-labs/moosestack) (the ClickHouse\-native open source developer framework) out of the box, as your harness to make your agents successful working with Postgres \+ ClickHouse.


From startups to large enterprises, we’ve seen this method successfully migrate production analytical workloads from Postgres to ClickHouse in days, instead of months.


Let's dig in.



> Want to get right to implementation? Here's a practical step\-by\-step [guide](https://docs.fiveonefour.com/guides/performant-dashboards/tutorial) for migrating your dashboards to ClickHouse with the help of AI.


## **Code:** Everything as code \- make your analytics stack legible to AI [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#code-everything-as-code---make-your-analytics-stack-legible-to-ai)


Coding agents are great at reading, writing, and reviewing code. They’re much less effective when it comes to coordinating infrastructure, tracking database status, managing schema evolutions, and other work that goes into implementing an actual production ClickHouse architecture.


The way to solve this is by treating your unified application and data stack as a single system expressed as code. Not as scattered DDL scripts, raw SQL strings, and tribal knowledge. But, rather, as shared, typed objects with explicit dependencies (see example below). All managed with git, and readily available in your IDE and local filesystem, ie your coding agent’s home turf.



```
import { MaterializedView, OlapTable, sql } from "@514labs/moose-lib";
import { sourceTable } from "path/to/SourceTable"; // could also be a view

// Define the rows we want to serve to dashboards.
// This is the schema of the destination ClickHouse table.
// JSDoc comments embed as column descriptions in CH,
// readable by agents querying the data.
interface TargetSchema {
id: string;

/** Mean rating value computed across all submitted reviews with ratings. */
average_rating: number;

/** Total number of valid reviews contributing to the average rating. */
num_reviews: number;
}

// Declare the destination serving table in code.
export const targetTable = new OlapTable<TargetSchema>("target_table", {
  orderByFields: ["id"],
});

// Declare the OLTP -> OLAP rewrite as a first-class object:
// source table(s) -> transformation -> serving table.
export const mvToTargetTable = new MaterializedView<TargetSchema>({
  // Turn query-time aggregation into a precomputed rollup.
  selectStatement: sql`
    SELECT
      ${sourceTable.columns.id},
      avg(${sourceTable.columns.rating}) AS average_rating,
      count(*) AS num_reviews
    FROM ${sourceTable}
    GROUP BY ${sourceTable.columns.id}
  `,

  // Explicit upstream dependencies (the “reads from” side of the graph).
  selectTables: [sourceTable],

  // Explicit downstream dependency (the “writes to” side of the graph).
  targetTable,

  // The name of the ClickHouse Materialized View.
  materializedViewName: "mv_to_target_table",
});

```

With MooseStack, code becomes your agents’ default interface to your ClickHouse data stack. For example, your source tables and your materialized views are declared as typed objects in your code base. This means:


1. Your agent is working with common Typescript patterns that it’s already familiar with and more likely to succeed with
2. When it doesn’t succeed, your agent’s work is just lines of code, which means easy rollbacks, evolutions, and iterations, in the form factor coding agents are built for (plus the added security of version control with git)


Not to mention, your agent can leverage and propagate these typed data models, eg. downstream to your APIs (e.g. Express, Fastify, Nextjs), your MCPs, your frontend, or wherever else the data that you have in ClickHouse is (now safely) referenced. Under the hood, this creates a dependency graph that is explicit and reproducible: MooseStack captures it as an “InfraMap” that can be surfaced to the agent via the [MooseStack dev MCP](https://docs.fiveonefour.com/moosestack/moosedev-mcp). When an agent edits a source schema or rollup, it no longer has to guess what breaks downstream: the dependencies are explicit, and the blast radius is discoverable from the code instantly accessible by your agent through the MCP.


“Everything is code” turns a ClickHouse migration from a brittle database rewrite into a normal refactor of a modular codebase. This is exactly the kind of problem AI agents are good at.


## **Cadence:** Fast feedback loops for AI\-safe OLAP iteration [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#cadence-fast-feedback-loops-for-ai-safe-olap-iteration)


Even better, once the system is all code, you can build feedback loops around it!


[Boyd’s law](https://blog.codinghorror.com/boyds-law-of-iteration/) states that the speed of iteration beats quality of iteration. If you rely on an LLM to one\-shot your migration, it’s unlikely to succeed.


So, ideally, you’re validating the migration end\-to\-end with each incremental change: schema, rollups, API queries, and dashboard outputs. That’s only practical if the feedback loop is fast. Really fast. If every tweak requires a cloud deployment and a backfill just to discover a mistake, AI iteration becomes too slow to be useful.


MooseStack gives developers and agents three layers of fast feedback during Postgres → ClickHouse migration work:


1. **In the IDE**: catch schema, type and ClickHouse SQL issues while the agent is still writing code.
2. **In local dev** (`moose dev`): run the full OLAP stack end\-to\-end with hot\-swapping infra, realistic data, and runtime errors and logs.
3. **In “preview branch” deployments**: validate behavior and performance on production\-like infrastructure in the cloud before merging.


### IDE feedback: schema, type, and SQL errors before you run anything [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#ide-feedback-schema-type-and-sql-errors-before-you-run-anything)


As we discussed above, MooseStack treats tables and views as first\-class, typed objects in your codebase, so your IDE can flag broken field references immediately. An agent can use this for almost instantaneous feedback.


For example, a React component might render fields from a shared `EventModel`:



```
// app/analytics/page.tsx
import { getEvents } from "moose";

export default async function AnalyticsPage() {
  const events = await getEvents();

  return (
    <ul>
      {events.map((e) => (
        <li key={e.id}>
          {e.id}: {e.amount} at {e.event_time.toISOString()}
        </li>
      ))}
    </ul>
  );
}

```

The MooseStack `OlapTable` object declares the ClickHouse object. The LLM might need to change that data model as part of a data modeling optimization in an OLTP → OLAP migration:



```
// moose/models/events.ts
import { OlapTable } from "@514labs/moose-lib";

export interface EventModel {
  id: string;
  amount: number;

  // agent change: renamed `event_time` -> `occurred_at`
  occurred_at: Date;
}

// This declares the ClickHouse table in code.
export const Events = new OlapTable<EventModel>("events", {
  orderByFields: ["occurred_at"],
});

```

Because of the strict typing, this will cause an error in the frontend, which is presented to the agent almost immediately:



```
// app/analytics/page.tsx
// ❌ IDE error: Property 'event_time' does not exist on type 'EventModel'
<li key={e.id}>
  {e.id}: {e.amount} at {e.event_time.toISOString()}
</li>


```

Going further than type\-safety (and, depending on the CLI) the agent can also directly access the [MooseStack LSP](https://docs.fiveonefour.com/moosestack/language-server) for validating syntax, autocomplete and error diagnostics.


### Local dev feedback for AI: run the full OLAP stack end\-to\-end with `moose dev` [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#local-dev-feedback-for-ai-run-the-full-olap-stack-end-to-end-with-moose-dev)


Many problems with real applications only show up once the entire system is actually running: mutations fail asynchronously, schemas apply in unexpected order, data arrives with unexpected shapes, or rollups silently produce the wrong numbers in the frontend.


That’s why your agent needs a fast, cheap runtime loop that mirrors your production stack. Agents should be able to apply schemas, push data through materialized views, execute real API queries, and validate the actual outputs your dashboards depend on.


The best version of this is local, hot\-reloading infrastructure with realistic data. Run your entire ClickHouse \+ Postgres \+ frontend stack locally, end\-to\-end, and make validation cheap enough that the agent can iterate on real mistakes instead of guessing.


With MooseStack, that starts with:



```
moose dev

```

This command spins up your whole OLAP stack locally (including ClickHouse), and then automatically infers and applies schema change DDLs in real time as your agent writes code.


This gives the agent two kinds of additional fast feedback:


1. **Runtime errors**. If, for example, your application can’t connect to ClickHouse or a transformation throws an exception when it encounters unexpected data shapes (JSON is a common culprit), these failures can’t be silent. With `moose dev` they surface immediately in the console logs, which makes them visible to both developers and agents while they’re iterating.
2. **MCP validation**. The [MooseDev MCP](https://docs.fiveonefour.com/moosestack/moosedev-mcp?lang=typescript) gives the agent tools to interrogate the local dev server. This allows the agent to validate: “did the system end up in the state the agent thought it created”? Are the right tables and views present? Does the transformed output look correct when queried? Are the logs telling the LLM anything interesting? The agent can even use `moose query` and `moose seed` to insert data to test data flows, sampling data from any step in the process.


Realistic data is what makes these checks meaningful. Without it, you can “pass” validation on toy datasets and still ship incorrect rollups.


This is what makes OLTP → OLAP migration AI\-safe: agents get fast, reality\-based feedback from a running system, not just confidence from code that compiles.


## **Context:** Opinions, expertise, and patterns \- give your agent the most relevant migration and OLAP context [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#context-opinions-expertise-and-patterns---give-your-agent-the-most-relevant-migration-and-olap-context)


Of course, your agent’s work is only as good as the context you pass in. In addition to the real time context for feedback loops discussed above, there’s also:


1. Static context: data and documentation about your existing implementation in your OLTP stack that needs to be migrated over to OLAP
2. Skills and guides: reusable implementation patterns peculiar to OLAP / Migrations
3. Reference implementations: show what “good” or “solved” has looked like in your organization


### Static context: ground your agent in your real data and patterns [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#static-context-ground-your-agent-in-your-real-data-and-patterns)


In migration cases, where your core business logic already exists (and just needs to be translated), you of course want to pass all of that context in on your existing implementation. In addition, you’ll want to provide context and data that enables the agent to complete end\-to\-end testing of the migration as it iterates. That means:


- Schemas, data dictionaries and data documentation
- Source data
- Any existing stored procedures or intermediate views
- Sample query inputs and outputs from the current system


Our [Improving Dashboard Performance Guide](https://docs.fiveonefour.com/guides/performant-dashboards/tutorial) comes with [a starter kit](https://github.com/514-labs/moosestack/tree/main/examples/dashboard-migration), which you can clone into your project to compile context across all four categories listed above. This includes prebuilt prompts and templates for you to easily dispatch your agents and have them gather example requests and responses for representative test cases for later validation, e.g.:



```
## Test case: <short-name>
 
### Request (curl)
 
```bash
# Method: GET|POST
# Path: /api/<endpoint>
# Expected: HTTP 200
# Auth: Bearer token via $API_TOKEN (do not paste secrets)
# Notes: <timezone/order/pagination assumptions if relevant>
 
# Set once in your shell:
# export API_BASE_URL="http://localhost:4000"
# export API_TOKEN="..."
 
# GET (query params)
curl -sS -G "$API_BASE_URL/api/<endpoint>" 
  -H "Authorization: Bearer $API_TOKEN" 
  -H "Content-Type: application/json" 
  --data-urlencode "param1=value1" 
  --data-urlencode "param2=value2" 
  | jq .
 
# POST (JSON body)
curl -sS -X POST "$API_BASE_URL/api/<endpoint>" 
  -H "Authorization: Bearer $API_TOKEN" 
  -H "Content-Type: application/json" 
  -d '{"param1": "value1", "param2": "value2"}' 
  | jq .
 
```
 
### Expected response
 
```json
{
  "REPLACE_ME": "paste the full JSON response body here (verbatim from the running endpoint)"
}
 
```

```

Front\-loading the right context dramatically reduces migration debugging. Across the Postgres → ClickHouse migrations we’ve worked on, we’ve found that real query outputs give agents something concrete to reason against, helping them converge on correct ClickHouse models with fewer blind rewrites and fewer “looks right, but is wrong” failures.


### Skills teach your agent *how* to implement OLAP migrations [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#skills-teach-your-agent-how-to-implement-olap-migrations)


Static context helps an agent understand what you’re trying to do. Skills help it understand how to do it (with ClickHouse).


MooseStack’s agent harness offers battle\-tested [agent skills](https://github.com/514-labs/agent-skills), which codify ClickHouse best practices into agent\-friendly rules for implementing ClickHouse in your application stack in Typescript or Python.



```
// skills/clickhouse-best-practices/SKILL.mdname: clickhouse-best-practices
description: MUST USE when reviewing ClickHouse schemas, queries, or configurations.
Contains 28 rules that MUST be checked before providing recommendations.
Always read relevant rule files and cite specific rules in responses.

```


```
// skills/clickhouse-best-practices/rules/schema-types-avoid-nullable.md

title: Avoid Nullable Unless Semantically Required
impact: HIGH
impactDescription: "Nullable adds storage overhead; use DEFAULT values instead"

```

These rules extend [ClickHouse’s agent skills](https://clickhouse.com/blog/introducing-clickhouse-agent-skills) (which focus on SQL implementation of ClickHouse best practices), and cover thorny, specialized topics in OLAP data modeling, like choosing efficient ORDER BY fields, managing cardinality, proper use of Nullability and other typing issues.


Give them a spin:



```
// data modeling best practices skills

npx skills add clickhouse/agent-skills // for ClickHouse SQL
npx skills add 514-labs/agent-skills   // for Typescript or Python

//Prompt: review and update my data models to implement more efficient OLAP best practices

```

### Reference implementations: your agent shouldn’t have to re\-solve solved problems [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#reference-implementations-your-agent-shouldnt-have-to-re-solve-solved-problems)


Even with good context and skills, agents will still try to invent solutions if they don’t see a concrete precedent. Point your agent at code that already reflects how you want your ClickHouse implementation built, for instance:


- **An example semantic / query layer** ([`query-layer`](https://github.com/514-labs/query-layer)) which shows how to structure reusable, ClickHouse\-aware queries in typescript abstractions
- **End\-to\-end example apps**, like the MooseStack examples ([`moosestack/examples`](https://github.com/514-labs/moosestack/tree/main/examples)), which demonstrate how schemas, materialized views, APIs, and dashboards fit together in a real project


These examples anchor the agent in the *target* architecture, not the Postgres source. When it encounters a familiar problem shape, it works forward from established OLAP designs rather than backward from OLTP habits. That dramatically reduces variance and makes AI\-assisted migrations feel deliberate instead of improvisational.


For example, the query layer example above defines a serving\-oriented query model once, and then reuses it everywhere dashboards need data:



```
export const eventsModel = defineQueryModel({
  table: Events,

  dimensions: {
    status: { column: "status" },
    day: { expression: sql`toDate(${Events.columns.event_time})`, as: "day" },
  },

  metrics: {
    totalEvents: { agg: sql`count(*)` },
    totalAmount: { agg: sql`sum(${Events.columns.amount})` },
  },

  filters: {
    timestamp: { column: "event_time", operators: ["gte", "lte"] as const },
    status: { column: "status", operators: ["eq", "in"] as const },
  },
});

```

This does two important things for migrations. First, it encodes OLAP\-native patterns: pre\-aggregated metrics, explicit dimensions, and constrained filters, rather than ad\-hoc SQL scattered across handlers. Second, it gives the agent a concrete shape to imitate. Instead of inventing a new query abstraction mid\-migration, it can adapt a proven one.


By the way, we’re working on adding a lightweight semantic / metrics layer to MooseStack as a first class citizen, inspired by this query\-layer example. If you have any feedback or requests, we’d love to hear from you on [our community slack](http://slack.moosestack.com).

### Try the unified data stack

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-66-try-the-unified-data-stack-get-access&utm_blogctaid=66)## A Quick Teaser: From Local to Production [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#a-quick-teaser-from-local-to-production)


A local, code‑first workflow doesn’t replace production deployment. It just makes it safe to iterate quickly before you ship. Your production ClickHouse cluster has different configuration, more data, and different failure modes. A materialized view that looks fine on 10,000 rows can fall apart at 10 million.


In practice, deploying safely means creating staging and preview environments in the cloud. [Moose Migrate](https://docs.fiveonefour.com/moosestack/migrate) provides a code\-based, optional human\-in\-the\-loop path for deploying your new ClickHouse configurations to your cloud environment.



> Want to go from local, agentic iteration to cloud deployment with a `git push`? [Fiveonefour’s hosting](https://fiveonefour.boreal.cloud/sign-up) works with ClickHouse Cloud to provide automated preview branches, managed schema migrations, deep integration with Github and CI/CD, and an agentic harness for your unified data stack in the cloud. [Sign up for free](https://fiveonefour.boreal.cloud/sign-up).


We’re also excited about the next step: letting agents inspect your cloud deployments directly. The 514 CLI (currently in alpha) is designed to expose the same surface area a human would use to debug ClickHouse workloads: streaming logs, querying ClickHouse system tables, and verifying that migrations and materialized views completed successfully. These inspection capabilities are rolling out incrementally over the coming days and weeks, so deployments become observable and machine\-verifiable within your AI harness, end\-to\-end. If you are interested in participating in this alpha release, [join our slack and let us know](http://slack.moosestack.com).


## Conclusion [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#conclusion)


Postgres \+ ClickHouse is the unified data stack for modern applications: transactional speed where you need it, analytical power where you don’t want compromise. With the right agent harness, like [MooseStack](https://github.com/514-labs/moosestack), AI can help you get there. When your unified data stack is expressed as code, reinforced with tight feedback loops, and grounded in ClickHouse best practices, agents can iterate safely and converge on real production outcomes. Ready to try it out in your own environment? Check out the [detailed step by step guide](https://docs.fiveonefour.com/guides/performant-dashboards/tutorial) to migrating your analytical workloads onto ClickHouse with the help of AI agents.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

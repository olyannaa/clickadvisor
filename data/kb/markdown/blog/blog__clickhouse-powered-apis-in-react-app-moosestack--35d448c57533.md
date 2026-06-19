# Build ClickHouse\-powered APIs with React and MooseStack


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Build ClickHouse\-powered APIs with React and MooseStack

![](/_next/image?url=%2Fuploads%2Ffiveonefour_avatar_8b25b9739c.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[Fiveonefour](/authors/fiveonefour) and [ClickHouse](/authors/clickhouse)Sep 16, 2025 · 16 minutes read
> This post is a **practical guide of how to build a ClickHouse\-powered API in your web app that will be familiar to anyone who’s worked with Postgres**.  
>   
> You’ll learn how to create a production ClickHouse Cloud service with real\-time data sync from Postgres to ClickHouse.  
>   
> You’ll use [Moose OLAP](https://docs.fiveonefour.com/moose/getting-started/from-clickhouse) to create TypeScript native interfaces for ClickHouse tables, build fully type\-safe APIs for analytical queries, integrate it into your app and deploy to production infrastructure.


If you’ve launched analytics in your user\-facing app, chances are you built it over your existing transactional (OLTP) database, like Postgres or MongoDB. We’ve all been there, it's the fastest way to get started and ship a valuable feature to your users. But, you’re probably starting to see queries slow down as you scale; more users, more data, more queries, slower dashboard. It’s affecting the user experience, and time spent trying to optimize performance is taking time away from shipping other features.


![514_b3_1.gif](/uploads/514_b3_1_14dd848d3b.gif)
*Caption: Example dashboard from our open source [reference application](https://area-code-lite-web-frontend-foobar.preview.boreal.cloud/) ft. a Vite \+ React web frontend and side\-by\-side transactional \& analytical database backends*
[If you’ve seen the benchmarks, you already know that ClickHouse is the fastest analytical (OLAP) database in the world](https://benchmark.clickhouse.com/). Purpose built for analytical queries, ClickHouse can query billions of rows in milliseconds. But the idea of retrofitting a new service into your web stack can seem daunting; you might be familiar with integrating Postgres into your app, but unsure what that looks like for ClickHouse.


This post is a **practical guide of how to build a ClickHouse\-powered API in your web app that will be familiar to anyone who’s worked with Postgres**. Plus you’ll set yourself up for future iteration with a great DX that scales across your team.


We’ll be using ClickHouse as our fast analytics database, plus [Moose OLAP](https://docs.fiveonefour.com/moose/olap) to provide a delightful and familiar developer experience:


- ClickHouse speed with ORM\-inspired schemas as code
- End\-to\-end type safety and contracts, from DB to React hooks
- Web app\-native, local\-first development for rapid iteration
- Safe deploys with preview environments and managed migrations


![514_b3_2.png](/uploads/514_b3_2_da51d64b1b.png)
Throughout the post, we’ll provide example code snippets from an open source reference application that implements this architecture. You can [play with the frontend here](https://area-code-lite-web-frontend-foobar.preview.boreal.cloud/), and find the [full code base on github](https://github.com/514-labs/area-code/tree/main/ufa-lite).


## Sync Postgres with ClickHouse [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#sync-postgres-with-clickhouse)


ClickHouse (and the entire stack we’re using in this post) is open source, can run locally and can be self\-hosted on your own infrastructure. But the fastest way to get started is to spin up a free trial cluster on [ClickHouse Cloud](https://clickhouse.com/cloud), giving you a production\-ready cluster in minutes—no servers or clusters to manage. Later in the post, you’ll see how to seed partial data from ClickHouse Cloud to a local container running your development ClickHouse instance.


With a ClickHouse cluster ready, first things first \- you’ll need some data.


In your application, your transactional database (e.g., Postgres) is the source of truth for data. ClickHouse is kept in\-sync with your transactional database via Change Data Capture (CDC). ClickHouse Cloud provides [ClickPipes](https://clickhouse.com/cloud/clickpipes), a simple, yet high\-performance, CDC engine that you can configure in under a minute. This will bring all existing data across into ClickHouse, and keep all future changes in\-sync in real\-time.


![514_b3_3.jpg](/uploads/514_b3_3_f2696bba29.jpg)
Within a couple minutes you’ll have your Postgres data mirroring into a production ready ClickHouse cluster. Now, the next step is making that data usable from your application code.


## Pulling your table schemas into code [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#pulling-your-table-schemas-into-code)


If you’re used to transactional ORMs like Drizzle or Prisma, you know the `db pull` workflow: generate TypeScript types directly from your schema. [Moose OLAP](http://docs.fiveonefour.com/moose/olap) offers similar ORM\-esque functionality, but built natively for ClickHouse. ([Popular transactional ORMs tend not to map well to OLAP](https://clickhouse.com/blog/moosestack-does-olap-need-an-orm)—ClickHouse has engines, unique defaults, and other modeling primitives that don’t exist in Postgres/MySQL.)


[You’ll need to install `moose`, the MooseStack CLI,](https://docs.fiveonefour.com/moose/getting-started/quickstart) and then run this from your project root to get started:



```

```
# initialize a new MooseStack project called "analytics service"
moose init analytics-service --from-remote
```

```

Follow the prompts to connect to your remote ClickHouse database, and MooseStack will introspect the ClickHouse database to discover its structure, then scaffold a new `analytics-service` folder with:


- Data models as TypeScript types, that you can reuse across APIs and queries
- Typescript “[OlapTable](http://docs.fiveonefour.com/moose/olap/model-table)” objects for each table in your ClickHouse database


MooseStack OLAP lets you interact with your database tables and schemas via native typescript interfaces, like this:



```

```
/* Link to full source code:
https://github.com/514-labs/area-code/blob/main/ufa-lite/services/analytical-moose-foobar/app/externalModels.ts
*/
export interface foo {
    id: Key>;
    name: string;
    description: string | undefined;
    status: string;
    priority: number & ClickHouseInt<"int32">;
    is_active: boolean;
    metadata: string | undefined;
    tags: string[];
    score: string & ClickHouseDecimal<10, 2> | undefined;
    large_text: string | undefined;
    created_at: string & typia.tags.Format<"date-time"> & ClickHousePrecision<6>;
    updated_at: string & typia.tags.Format<"date-time"> & ClickHousePrecision<6>;
    _peerdb_synced_at: string & typia.tags.Format<"date-time"> & ClickHousePrecision<9> & ClickHouseDefault<"now64()">;
    _peerdb_is_deleted: number & ClickHouseInt<"int8">;
    _peerdb_version: number & ClickHouseInt<"int64">;
}

export const FooTable = new OlapTable("foo", {
    orderByFields: ["id"],
    engine: ClickHouseEngines.ReplacingMergeTree,
    ver: "_peerdb_version",
    settings: { index_granularity: "8192" },
    lifeCycle: LifeCycle.EXTERNALLY_MANAGED,
});
```

```

At this point, you’ve done the heavy lifting: your ClickHouse schema is now in code. It’s typed, versioned, and sitting right alongside the rest of your application logic. But code on its own isn’t enough — you need a way to actually *use* it: run queries, break things, fix them, and evolve APIs without risking production.


That’s exactly what the next step gives you: running MooseStack as part of your local dev environment.


## Local\-first dev with seeded ClickHouse [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#local-first-dev-with-seeded-clickhouse)


Think about how you work on your frontend: you’d never ship a UI change without firing it up locally first.


With the Moose CLI, you get that same feedback loop: your analytics backend runs locally as a first\-class service next to your app, so you can spin it up, seed it with production data, and safely experiment before anything touches staging or prod.


In our example [reference app](https://github.com/514-labs/area-code/tree/main/ufa-lite), this plays out in a monorepo (although the monorepo approach certainly isn’t required):


- `/apps/web` → Vite React frontend web app
- `/services/transactional` → Fastify API server with CRUD endpoints backed by Supabase \+ Drizzle ORM
- `/services/analytical` → MooseStack backend powered by ClickHouse added specifically for analytics


So when developing locally, you just start each piece of the stack side by side:



```

```
cd apps/web && pnpm dev
cd services/transactional && pnpm dev
cd services/analytical && pnpm dev

# or from the root of the monorepo
pnpm dev
```

```

If you’re following along, your local dev stack now looks like:


- **React frontend** → localhost
- **App server** → localhost (with API access to Postgres)
- **MooseStack analytics service** → localhost (with API access to ClickHouse)


### Seeding Your Local ClickHouse [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#seeding-your-local-clickhouse)


When you run `moose dev`, the CLI spins up a local ClickHouse container. By default, your tables are created, but they contain no data. To test queries and APIs, you can seed them with real data from your ClickHouse Cloud cluster that is in\-sync with your Postgres.



```

```
moose seed clickhouse --connection-string $MOOSE_REMOTE_CLICKHOUSE_URL --limit 100000
```

```

This example copies over up to 100,000 rows per table into your local instance. This allows you to develop fully locally, without any calls to remote infrastructure, over a representative sample of data.


## Status check: what we’ve covered so far [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#status-check-what-weve-covered-so-far)


So far, you’ve accomplished a few very important things:


1. Created a production\-grade ClickHouse service.
2. Solved Postgres\-ClickHouse syncronisation.
3. Brought your schemas into code as TypeScript types and contracts.
4. Brought those schemas to life in a local ClickHouse dev instance, seeded with representative production data.


Analytics is no longer “some remote database you poke at.” It’s part of your development workflow. You can try queries on your laptop, evolve schemas under version control, and see changes hot\-reload—just like in your frontend or API server.


## Building type\-safe analytics APIs [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#building-type-safe-analytics-apis)


From here, your existing web app doesn’t need to talk directly to ClickHouse. Your new `analytics-service` can translate API calls into typed queries and enforce contracts for you. Let’s put that to work now, by exposing typed endpoints for your frontend to call.


If you’ve worked with ORMs in OLTP systems, this pattern will feel familiar. In the Postgres/MySQL world, tools like Drizzle or Prisma let you define a schema in TypeScript, derive validators, and reuse them across your routes and UI forms. When the schema changes, the validators update automatically and errors are caught at build time.


When you build an analytical API in Moose, the API contract is just TypeScript. The request/response types you declare are automatically compiled into runtime validators. That means you get **both dev\-time and runtime type safety** without introducing additional parsing or validation layers.



```

```
/* Link to full source code: https://github.com/514-labs/area-code/blob/main/ufa-lite/services/analytical-moose-foobar/app/apis/foo/consumption/foo-score-over-time-api.ts */

import { Api } from "@514labs/moose-lib";
import { FooTable } from "../../externalModels";

export type FoosScoreOverTimeDataPoint = {
  date: string;
  averageScore: number;
  totalCount: number;
};

export type GetFoosScoreOverTimeParams = { days?: number };

export type GetFoosScoreOverTimeResponse = {
  data: FoosScoreOverTimeDataPoint[];
  queryTime: number;
};

export const scoreOverTimeApi = new Api<
  GetFoosScoreOverTimeParams,
  GetFoosScoreOverTimeResponse
>("foo-score-over-time", async ({ days = 90 }, { client, sql }) => {
  /* scoreOverTimeApi function code, see below */
});
```

```

On the query side, Moose OLAP makes SQL schema\-aware. Your `OlapTable` objects expose typed columns, so you can use them inline when writing queries. This turns SQL from a brittle string into something your editor understands: **if you reference a column that doesn’t exist, you’ll see the error immediately in your IDE instead of at runtime**.



```

```
/* Link to source code: https://github.com/514-labs/area-code/blob/main/ufa-lite/services/analytical-moose-foobar/app/apis/foo/consumption/foo-score-over-time-api.ts */

/* scoreOverTimeApi function code */
const start = new Date();
start.setDate(start.getDate() - days);
const end = new Date();

const startStr = start.toISOString().split("T")[0];
const endStr = end.toISOString().split("T")[0];

const query = sql`
  SELECT
    toDate(${FooTable.columns.created_at}) AS date,
    AVG(${FooTable.columns.score})         AS averageScore,
    COUNT(*)                               AS totalCount
  FROM ${FooTable}
  WHERE toDate(${FooTable.columns.created_at}) BETWEEN toDate(${startStr}) AND toDate(${endStr})
    AND ${FooTable.columns.score} IS NOT NULL
  GROUP BY toDate(${FooTable.columns.created_at})
  ORDER BY date ASC
`;
```

```

### Testing your API endpoints [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#testing-your-api-endpoints)


When you run `moose dev`, the **MooseStack CLI hot\-reloads your APIs** and updates a generated OpenAPI 3\.0 spec (`.moose/openapi.json`). That means you can **test endpoints immediately**—whether with curl, Swagger UI, or a VSCode extension:



```

```
curl -X 'GET'
  'http://localhost:4410/api/foo-score-over-time?days=10'
  -H 'accept: application/json'

{
  "data": [
    {
      "date": "2025-06-15",
      "averageScore": 41.81,
      "totalCount": "6"
    },
    {
      "date": "2025-06-16",
      "averageScore": 22.3,
      "totalCount": "5"
    },
    {
      "date": "2025-06-17",
      "averageScore": 52.29,
      "totalCount": "6"
    },
...
  ]
}
```

```

Every query you execute is also logged in the terminal that is running `moose dev`. If there’s an error, you’ll see it in the API response as well as in the dev logs. This instant feedback loop makes it easy to fix mistakes on the spot instead of chasing them in staging.



```

```
API Executing API: foo-score-over-time
API Query: SELECT toDate(`created_at`) as date, AVG(`score`) as averageScore, COUNT(*) as totalCount FROM `foo` WHERE toDate(`created_at`) >= toDate('2025-06-15') AND toDate(`created_at`) <= toDate('2025-09-13') AND `score` IS NOT NULL GROUP BY toDate(`created_at`) ORDER BY date ASC
API Query completed: 14ms
```

```

As you’re migrating your under\-performing legacy APIs to your new, blazing\-fast ClickHouse\-powered APIs, don’t forget to use your AI co\-pilot of choice. The real time feedback loop here is particularly effective for enabling agentic coders that—as we all know—don’t always one\-shot everything.


## Bridging to the frontend [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#bridging-to-the-frontend)


The generated OpenAPI spec is more than just documentation—it’s your bridge to the frontend. Instead of manually keeping contracts in sync, you can plug the spec into an SDK generator like [Orval](https://orval.dev) or [Kubb](https://kubb.dev).


In our reference app, we use [Kubb](https://github.com/kubb-project/kubb) to generate a fully typed React fetch client directly from the auto generated OpenAPI spec. The integration is simple: configure the Moose dev server to [trigger SDK codegen on reload](https://docs.fiveonefour.com/moose/apis/openapi-sdk), and point Kubb at the `.moose/openapi.yaml` file that Moose dev outputs.



```

```
[http_server_config]
on_reload_complete_script="pnpm generate-sdk"

# Link to full source code: https://github.com/514-labs/area-code/blob/main/ufa-lite/services/analytical-moose-foobar/moose.config.toml
```

```

Now every schema or API change automatically regenerates your frontend data fetchers. In React, all you need to do is import the generated client and call your backend from a component:



```

```
/* Link to full source code: https://github.com/514-labs/area-code/blob/main/ufa-lite/apps/web-frontend-foobar/src/features/foo/foo.score-over-time.graph.tsx */

import {
  getApiFooScoreOverTime,
  GetApiFooScoreOverTimeQueryParams,
  GetFoosScoreOverTimeResponse as ApiGetFoosScoreOverTimeResponse,
} from "@/analytical-api-client";

const fetchChartData = async (
  baseUrl?: string,
  fetchApiEndpoint?: string,
  days: number = 90
): [object Object], => {
    // Use new API client for analytical API
    const params: GetApiFooScoreOverTimeQueryParams = {
      days,
    };

    const response: ApiGetFoosScoreOverTimeResponse =
      await getApiFooScoreOverTime(params, {
        baseURL: baseUrl,
      });

    return response;
}
```

```

This closes the loop: your schema definitions drive your APIs, MooseAPIs enforce contracts automatically, and your frontend consumes generated clients that are always up to date. And it’s all running locally and updating in real time as you code. The result is end\-to\-end type safety without manual type sharing, and analytics APIs that are just as easy to integrate as your old API routes that read from your Postgres/MySQL/Mongo database.


## Ship to production with Boreal [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#ship-to-production-with-boreal)


Once your schemas are verified and APIs tested locally, you’re ready to go live. [Boreal](https://www.fiveonefour.com/boreal) by 514 (creators of MooseStack) gives your analytical data the same developer experience you expect from platforms like Vercel or Heroku. Connect your GitHub repo, create a branch, and Boreal provisions a matching preview environment with its own staging database in your ClickHouse cluster. Merge to main, and your MooseStack service and schema changes go live in production automatically.


When you deploy, Boreal doesn’t just ship code—it also ships schema migrations derived from your latest changes. To keep things safe, it validates your code against the live database state. If an upstream process like ClickPipes dropped a column, Boreal blocks the rollout until you’ve updated your code, so your APIs never point at missing data. Just [pull the latest schemas](https://framework-docs-git-db-pull-docs.preview.boreal.cloud/moose/olap/db-pull) into your project, so you can update your APIs, re\-test locally, and merge again—this time with confidence everything lines up.



```

```
moose db pull --connection-string $MOOSE_REMOTE_CLICKHOUSE_URL
```

```


> [Open source MooseStack is fully self\-hostable](https://framework-docs-git-db-pull-docs.preview.boreal.cloud/moose/deploying). But just as ClickHouse Cloud is the fastest way to get a production\-grade database, [Boreal](https://www.fiveonefour.com/boreal) is the fastest way to get a production\-grade analytical service—with CI/CD, preview branches, and GitHub integration built in.


### Getting set up [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#getting-set-up)


1. Sign in at [boreal.cloud](https://boreal.cloud/sign-up) with your GitHub login
2. Link the repo where your MooseStack project lives
3. Connect to your ClickHouse Cloud cluster with your admin credentials


From there, the workflow is the same one you’ve been using: open a PR and merge to main. Boreal takes care of the rest—building your MooseStack service, validating the schema in ClickHouse Cloud, and rolling out your APIs.


## In conclusion [\#](/blog/clickhouse-powered-apis-in-react-app-moosestack#in-conclusion)


Delivering snappy analytics for your users demands a dedicated real time analytical database, and ClickHouse is the best on the market for this. Integrating ClickHouse into your app doesn’t have to be daunting. Pairing ClickHouse for millisecond OLAP with [MooseStack](https://docs.fiveonefour.com/moose) for a local\-first dev loop gives you the speed users expect and the DX your team needs.


Get up and running today with [ClickHouse Cloud](https://clickhouse.com/cloud) and [ClickPipes](https://clickhouse.com/cloud/clickpipes), for mirroring data from your transactional database. Pull your schemas into code with [Moose OLAP](https://docs.fiveonefour.com/moose/olap), create runtime\-validated endpoints with [Moose APIs](https://docs.fiveonefour.com/moose/apis), and bridge straight into React with automatically generated hooks. And when it’s time to go live, [Boreal](https://www.fiveonefour.com/boreal) gives you a familiar path to production with preview environments, schema migrations, and CI/CD integrated deployments. Start with ClickHouse next to your existing transactional database today, migrate at your pace, and keep shipping features—without spinners.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

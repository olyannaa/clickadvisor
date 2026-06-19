# Data engineering and software engineering are converging


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Data engineering and software engineering are converging

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Ffiveonefour_avatar_8b25b9739c.png&w=96&q=75)Fiveonefour \& ClickHouse TeamAug 26, 2025 · 18 minutes read
> TL;DR:   
>   
> · If you’re an engineer building realtime analytics or AI\-powered features, you need the right data infrastructure coupled with the right developer experience (DX).   
>   
> · A great DX for data infrastructure should empower both software devs and data engineers, while taking inspiration from the best of modern web development (git\-native, local\-first, everything as code, CI/CD friendly, etc).   
>   
> · [MooseStack](https://github.com/514-labs/moosestack) by 514 offers a fully open source implementation of a DX layer for ClickHouse.


Data engineering and software engineering are converging.


For years, data infrastructure was built for analysts. Warehouses, lakes, BI dashboards—all SQL\-first, point\-and\-click workflows. But today, analytics isn’t just about reporting or data science. Real\-time data is at the center of modern user experiences and AI\-readiness. SaaS apps are surfacing analytics and AI directly in their UX to drive adoption, engagement, and retention. Enterprises are accelerating their business with AI\-powered automations for faster insights, predictions, and operations.


Engineering teams are on the hook to ship data\-backed functionality with the same discipline as any other application code. If you’re coming from the software engineering world, you probably start with a transactional database like Postgres, MySQL or Mongo. The tooling is great, and the developer experience is mature—but those systems are built for transactions, not analytics. As cardinality and scan sizes grow, queries bog down. Dashboards spin. AI chat slows to a crawl.


Alternatively, if you’re coming from the data engineering world, you’re probably on managed analytics platforms like Snowflake, BigQuery, or Databricks. These work well for batch ETL and reporting, but fall short when you need freshness, concurrency, or sub\-second response times. They’re also full of rough edges for developers. You don’t get a real local environment. Iteration cycles are slow. They’re just not built for the modern software development lifecycle.


So we’re left with a gap—and it’s two\-fold: user experience (UX) and developer experience (DX).


### 1\. The user experience (UX) gap [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#1-the-user-experience-ux-gap)


End users want sub\-second analytics at application scale. Enter ClickHouse. ClickHouse offers [best in class performance on analytical queries](https://benchmark.clickhouse.com/)—orders of magnitude faster than transactional databases like Postgres, and [many times faster and more cost efficient than cloud data warehouses like Snowflake or Databricks](https://clickhouse.com/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance). That means snappy dashboards and conversation\-speed AI chat for your UX.


### 2\. The developer experience (DX) gap [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#2-the-developer-experience-dx-gap)


Engineers need the same kind of safe, tight iteration loop that’s been taken for granted in web development for twenty years. Interestingly, ClickHouse can run efficiently at any scale, from megabytes to petabytes of data, and can adapt to any type of deployment—from serverless functions, to a container on your laptop, to a cluster of thousands of servers working together. This makes ClickHouse uniquely suited for both a local\-first development workflow and massive production scale. But how to build on ClickHouse’s power and flexibility with a full\-blown, modern, open source developer experience? Enter [MooseStack](https://github.com/514-labs/moosestack).


## Adding a modern software DX to ClickHouse [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#adding-a-modern-software-dx-to-clickhouse)


A great data \& analytics DX should serve both (1\) data engineers leaning into software development best practices, and (2\) software engineers leaning into data, analytics and AI. And it should take inspiration from the most innovative tools driving the modern web development experience—like [Ruby on Rails](https://rubyonrails.org/), [Next.js](https://nextjs.org/), [TanStack](https://tanstack.com/), and [Supabase](https://supabase.com/).


In short, a great data \& analytics DX should embrace the following core principles:


1. Git\-based version control \& governance
2. Local\-first development
3. Native programming languages (not YAML)
4. Infrastructure boilerplate abstractions
5. Horizontal integration, with modularization
6. Open source native
7. AI copilot native
8. Transparent migrations \& integrated CI/CD


The remainder of this post explores each of these principles in more detail, while also referencing how they are implemented with [MooseStack](https://github.com/514-labs/moose) by 514—an open source developer toolkit for building TypeScript or Python apps on ClickHouse and other open source data infrastructure.


## 1\. Git\-based version control and governance [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#1-git-based-version-control-and-governance)


Version control systems like git are at the heart of the modern software development lifecycle. Make changes, track changes, collaborate on code, etc. This is the norm for any software developer, but not so much with many data \& analytics platforms, with cloud\-based GUIs and point and click interfaces. And if there is code, it’s not always easy to integrate with git—expecially with browser\-based code editors, and heavy\-handed cloud\-to\-local\-to\-cloud workflows.


**A great developer experience should be grounded in a code base that is easily tracked and managed with git.**


With MooseStack libraries and tools, you can build your entire user\-facing analytics app, or even your data warehouse, in native Typescript or Python, with git integration natively supported \- it’s just code.


![514_1.png](/uploads/514_1_4513d7aee6.png)
*git\-based version control means audit trails for your data contracts*
## 2\. Local dev experience [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#2-local-dev-experience)



> “Data engineering shouldn’t have to trail software development by a decade or more when it comes to developer experience. MooseStack brings the tools and abstractions that you expect from a modern developer framework.”  
> 
> – Pardhu Gunnam, CEO/Creator of Metaphor Data


The best developer experience for you is in your IDE of choice, not in a browser tab. Web development figured this out a long time ago. You don’t “yolo” changes directly into a live server. You spin up a dev environment on your laptop that mirrors production. You create a branch, make changes, and immediately see what broke in a live preview of your application. Your build logs tell you if you’ve stranded an import or introduced a syntax error. You have a safe environment to freely experiment and break things, knowing that the worst thing that can happen is your code gets into an error state and you just kill the branch and start a fresh one. By the time you merge, you’ve had multiple layers of validation and review. That workflow gives you confidence. You can see exactly how your changes impact the entire system before they ever hit production.


**A great developer experience should provide an isolated, production\-like environment to freely experiment and immediately see what breaks in a live preview of your application.**


With MooseStack, local development is first\-class. “Modern” data platforms tend to be large, distributed, and cloud native—Snowflake and BigQuery won’t run on your laptop. But ClickHouse and other next\-gen data infrastructure (like [Redpanda](https://www.redpanda.com/), for example) can run locally in a container. MooseStack’s [local dev server](https://docs.fiveonefour.com/moose/local-dev) runs your entire analytics stack in one CLI command: `moose dev`. Combine that with git\-native development, and you’ve got a DX where you can create a branch off main, pull it down, run Moose dev, and all your models running in production are instantly materialized in a local ClickHouse instance for development. Seed it with sample data, and your dev server gives you the full loop—ingest, transform, aggregate, serve—hot\-reloaded as you edit code. The same APIs your app calls in production are live in development, so your feature work is always exercising the real data paths and pipelines.


![514_2.png](/uploads/514_2_a8b1cc8196.png)
*MooseStack’s dev server gives you a local mirror of your production data infrastructure with hot\-swapped code changes for your application*
## 3\. Native programming languages (not YAML) [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#3-native-programming-languages-not-yaml)


In our previous post, we dug into the question, “[*Does OLAP need an ORM?*](https://clickhouse.com/blog/moosestack-does-olap-need-an-orm)”. Traditional ORMs can sometimes cause more harm than good, e.g., with leaky abstractions, or by hiding SQL performance implications. But the core idea is worth keeping: modeling tables as objects in application code. That pattern gives you type\-safety, IDE auto\-completion, and immediate visibility when a change in your schema layer breaks an API in your app layer (or the other way around). In web development, if you change a prop in a React component, your IDE and dev server immediately show you which pages are broken. Analytics deserves the same feedback loop.


For many teams, YAML\-based DSLs are the first step toward treating data as code. That’s progress: your schema definitions are at least version\-controlled and reviewable, instead of being declared directly into a live database. But YAML is a configuration file format, not a programming language. It can’t express complex business logic—no IF statements, no loops, no variables—so non\-trivial transformations end up pushed into shell scripts, SQL fragments, or proprietary templating. The result is fragmentation: schemas live in one place, pipelines in another, and there’s no way to reason about them together at compile time.


**A great developer experience should leverage the full capabilities of application programming languages, with schemas represented as native types in the same language where you write your application and pipeline logic.**



```
interface DataModel {
columnName: Key<string>;
	secondColumnName: Date;
}

export const my_table = new OlapTable<DataModel>("table_name")

```

With MooseStack, everything lives in Typescript or Python: [schemas](https://docs.fiveonefour.com/moose/data-modeling), pipelines, transforms, APIs—all versioned in your repo alongside application logic. Yes, [some transformations are still expressed in SQL](http://docs.fiveonefour.com/moose/olap/modeling-materialized-view), but the SQL isn’t floating around as raw strings. It’s written inside language\-native templates that reference typed schema objects. Rename a column in your TypeScript interface or Python class, and Moose updates the underlying ClickHouse schema ([Moose OLAP](https://docs.fiveonefour.com/moose/olap)) and immediately flags every SQL fragment, stream ([Moose Streaming](http://docs.fiveonefour.com/moose/streaming)), pipeline ([Moose Workflows](https://docs.fiveonefour.com/moose/workflows)), or API ([Moose APIs](https://docs.fiveonefour.com/moose/apis)) that depends on it. You’re still writing real SQL—but with the safety net and ergonomics of a programming language.



```
const result = await client.query.execute(sql`
      SELECT 
        ${my_table.columnName} as my_column,
        COUNT(*) as total_records,
      FROM ${my_table} 
      GROUP BY ${my_table.columnName} 
`);

```

The payoff is that schemas and pipelines evolve together. Changes are surfaced instantly in your IDE and in your dev loop, not hours later in production. You keep SQL where it belongs—as the lingua franca of analytics—but ground it in the same typed codebase as the rest of your application.


## 4\. Infrastructure boilerplate abstractions [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#4-infrastructure-boilerplate-abstractions)



> “MooseStack abstracts away all the annoying boilerplate, and gives me simple, intuitive primitives to build with, and a local dev server to iterate on.”  
> 
> – David Der, Chief AI officer, SingleStone


Boilerplate infrastructure code is the worst. You have to get it right, or everything breaks, but it’s hard to get right. And more often than not, there is a best practice way to do it that covers 90%\+ of use cases. This is the perfect scenario for abstraction. In modern web development, you don’t configure your router from scratch—you use [next.js](http://next.js)’s router or [TanStack Router](https://tanstack.com/router), and you use their elegant abstractions. No need to reinvent the wheel every time.


**A great developer experience should abstract away commonly used boilerplate code for infrastructure best practices.**


Data infrastructure is full of examples like this. Buffering streaming events for batch writes to the database. Runtime data validation and dead letter queueing on data ingestion. Structuring tables for advanced materialized views. MooseStack provides simple abstractions in TypeScript/Python for each of these. So you can focus on the unique business logic of your application, instead of the data infrastructure glue and duct tape.



```
export const FooPipeline =
 new IngestPipeline<FooDataModel>("myFooPipeline", {
   table: true,
   stream: true,
   api: true,
 });

```

For example, MooseStack’s IngestPipeline object automatically wires up a complete ingest pipeline, typed to a particular data model. This includes:


- An ingest API with runtime data validation, automatic OpenAPI documentation, and optional dead letter queuing
- A [Redpanda](https://www.redpanda.com/)/[Kafka](https://kafka.apache.org/) streaming buffer with at least once delivery and optional streaming transformations
- A ClickHouse table with writes automatically batched to maximize performance


## 5\. Horizontal integration, with modularization [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#5-horizontal-integration-with-modularization)



> “MooseStack brings together all the modules needed for building end\-to\-end data services into a simple unified dev framework.”  
> 
> – Scott Haines, Distinguished Software Engineer, Fortune 100 Brand


Modern web frameworks like [Next.js](https://nextjs.org/) show the power of horizontal integration by bundling routing, rendering, APIs, and deployment into a seamless developer experience. At the same time, tools like [TanStack](https://tanstack.com/) highlight why modularization matters—providing composable, swappable pieces that work across frameworks without lock\-in. Data infrastructure tends to be particularly piecemeal, with a sprawling landscape of services surrounding the core database, including streaming, orchestration, connectors, transformations, catalogues, etc.


**A great developer experience should leverage integrated workflows for speed, and modular building blocks for long\-term flexibility.**


MooseStack offers a variety of modules with developer abstractions for all the core parts of a standard analytical backend. These modules can be used independently and swapped out for alternative solutions. For example, you could use the Moose OLAP module to manage your ClickHouse deployment, paired with [ClickHouse Cloud’s ClickPipes](https://clickhouse.com/cloud/clickpipes) to bring data in, and [FastAPI](https://fastapi.tiangolo.com/) to layer Python APIs on top. Or if you’ve got an existing ClickHouse cluster, and need to add data from a bespoke source, you could just use the Moose Workflows module to create a custom data connector and pipeline in Typescript. But as you adopt MooseStack across more of your analytical backend, you get the benefits of a unified end\-to\-end abstraction layer, shared data models and a consistent local development experience.


![514_3.png](/uploads/514_3_e0b1fec6e3.png)
*MooseStack modules and tooling can be used individually, or combined for an end\-to\-end experience*
## 6\. Open source native [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#6-open-source-native)


The modern web development experience is built on open source frameworks and technologies. Open source tooling reduces vendor lock\-in, increases trust and security, encourages innovation, and keeps control in the hands of the developer. ClickHouse is, of course, open source. So why would you want to wrap it in a closed\-source developer experience that locks you in to a particular vendor?


**A great developer experience should be grounded in open source tooling, offering flexibility and transparency.**


MooseStack is [open source and MIT\-licensed](https://github.com/514-labs/moosestack), and integrates with the rest of your open source software stack, including:


- Data infrastructure: ClickHouse, [Kafka](https://kafka.apache.org/), [RedPanda](https://www.redpanda.com/), [Temporal](https://temporal.io/), [Iceberg](https://iceberg.apache.org/), [Delta Lake](https://delta.io/), etc
- Full stack frameworks: [Next.js](https://nextjs.org/), [Remix](https://remix.run/), [TanStack](https://tanstack.com/), etc
- Micro frameworks: [Flask](https://github.com/pallets/flask), [fastAPI](https://github.com/fastapi), [Fastify](https://fastify.io/), etc
- API standards: [OpenAPI](https://www.openapis.org/), etc
- Language Runtimes: [Node](https://nodejs.org/) and [Python](https://www.python.org/)
- Frontend Clients: [React](https://react.dev/), [TanStack Query](https://tanstack.com/query), [Streamlit](https://streamlit.io/), etc
- Transactional ORMs: [Prisma](https://www.prisma.io/), [Drizzle](https://orm.drizzle.team/), etc
- Typing and data validation: [Typia](https://typia.io/), [Pydantic](https://docs.pydantic.dev/latest/), etc
- Libraries: all your favorite TS and Python libraries can be imported


## 7\. AI copilot native [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#7-ai-copilot-native)



> “Arming our full stack engineers with MooseStack and Sloan AI agents puts data engineering in the ‘full stack’.”  
> 
> – C. Rodes Boyd, Bracket Real Estate


Whatever your client of choice, you probably have some kind of copilot helping write code, or even an agent creating entire applications. LLM\-powered copilots and agents tend to be pretty good at creating web apps (not perfect of course, but moving quickly in the right direction). The performance here is powered by:


- Tons of examples to learn from
- Tons of frameworks and abstractions to reduce the complexity and the surface area of interaction
- Great local dev experience to iterate quickly to functional output


**It turns out, the same things that make a great developer experience for human developers, also make a great developer experience for LLMs and agentic developers.**


MooseStack is designed from the ground up to be agentic coder friendly, including:


- Following familiar patterns from the transactional world that LLMs are comfortable with
- Offering abstractions and reduced surface area to constrain LLMs to viable solutions
- Offering great local dev experience to quickly iterate in


And if you want to supercharge your coding co\-pilot, Fiveonefour’s [Sloan AI](https://www.fiveonefour.com/sloan) (from the creators of MooseStack) offers agents and tools trained specifically on MooseStack to boost your developer experience further.


![514_4v2.jpg](/uploads/514_4v2_fb6fc6c658.jpg)
*Using Sloan’s MCP integration with Cursor to create (and immediately test locally!) a new API endpoint on ClickHouse*
## 8\. Transparent migrations \& integrated CI/CD [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#8-transparent-migrations--integrated-cicd)


Of course, development doesn’t stop when you push a commit—you need to get to production. In web development, deployment has matured: innovations like automated governance and CI/CD pipelines in GitHub, and preview branches in Vercel and Supabase, give developers confidence that their production deployments won’t break. That confidence comes from transparency: you can see exactly what will happen before code hits prod, and you know you can safely roll it back if something goes wrong.


**A great developer experience should bring confidence and transparency to production deployment for data systems.**


With data backends, the stakes are even higher. Shipping a half\-applied migration isn’t like breaking a web page—it can corrupt or orphan critical datasets. Analytical/OLAP systems are especially fragile here: schema changes are often non\-transactional, meaning there’s no easy rollback. A failed `ALTER` can leave a table in limbo, requiring you to write and apply your own reverse mutations by hand. Plus, in systems where analysts or external pipelines can also mutate schemas, drift between your code and the live database is common.


MooseStack addresses this head\-on with [Moose Migrate](https://docs.fiveonefour.com/moose/migrate). Before deploying to production, MooseStack diffs your code against the live schema and generates a migration plan to apply to your production database to update schemas and business logic. You can also generate the plan [in advance](https://docs.fiveonefour.com/moose/olap/planned-migrations), to review, edit, and version control your migration. Either way, when you go to deploy, if drift has crept in between your code and the live database state, the migration fails fast, rather than shipping a broken deployment. The result is your application code and schema changes always ship together, in sync.


If you want to go further, Fiveonefour’s [Boreal](https://www.fiveonefour.com/boreal) (from the creators of MooseStack) can host and manage your ClickHouse cluster on top of [ClickHouse Cloud](https://clickhouse.com/cloud), along with your data streaming, API endpoints, and pipeline orchestration. Boreal integrates natively with GitHub, so you get one\-click deploys, deep integration with your CI/CD workflows, and automatic previews of your dev branches deployed to the cloud. You also get enterprise\-grade security, compliance, and observability. Boreal is SOC 2 Type 2 certified and offers logs and metrics endpoints to collect your observability data into your monitoring/alerting tool of choice.


### Wrapping up [\#](/blog/eight-principles-of-great-developer-experience-for-data-infrastructure#wrapping-up)


The performance and flexibility of ClickHouse unlocks new ways of approaching data engineering, and new ways of integrating analytics and AI into software applications. But taking full advantage requires a modern developer experience layer, not just a powerful engine. That’s our mission at [Fiveonefour](https://www.fiveonefour.com/) with open\-source [MooseStack](https://github.com/514-labs/moosestack): to build upon ClickHouse's powerful core, offering a developer experience that feels as productive and familiar as modern web development.


[Give the repo a star if you think it's interesting.](https://github.com/514-labs/moosestack)



> “The developer experience is what really stands out with MooseStack. It’s my go\-to now for every new project that needs an analytics backend.”  
> 
> – David Der, Chief AI officer, SingleStone

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

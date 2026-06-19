# Does OLAP need an ORM?


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Does OLAP need an ORM?

![](/_next/image?url=%2Fuploads%2Ffiveonefour_avatar_8b25b9739c.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)Fiveonefour \& ClickHouse TeamAug 15, 2025 · 20 minutes read
> **TL;DR**  
>   
> · ORMs have proven to be useful for many developers in the OLTP/transactional stack (Postgres, MySQL, etc).  
>   
> · OLAP/analytical databases like ClickHouse could potentially benefit from ORM abstractions.  
>   
> · Existing transactional ORMs probably shouldn’t be extended to OLAP due to fundamental differences in semantic meaning between OLTP and OLAP.  
>   
> · [Moose OLAP](https://docs.fiveonefour.com/moose/getting-started/from-clickhouse) (part of [MooseStack](https://github.com/514-labs/moose)) is an open source, MIT\-licensed implementation of an ORM\-like interface for ClickHouse, inspired by transactional ORMs, but adjusted for the OLAP world.  
>   
> The intention of this article is to open a debate with [the community](https://join.slack.com/t/moose-community/shared_invite/zt-2fjh5n3wz-cnOmM9Xe9DYAgQrNu8xKxg), and explore the question: what might an effective ORM for OLAP actually look like?


Modern applications are leaning into user\-facing analytics and AI functionality—i.e. features that are powered by aggregations across large data sets. That’s pushing dev teams beyond their standard transactional/OLTP database ([Postgres](https://www.postgresql.org/), [MySQL](https://www.mysql.com/), etc), and into the world of analytical/OLAP databases like ClickHouse—in other words, beyond the typical scope and capabilities of your go\-to Object\-Relational Mapper (ORM).


While sometimes polarizing, ORMs like [Prisma](https://www.prisma.io/), [Drizzle](https://orm.drizzle.team/), and [SQLAlchemy](https://www.sqlalchemy.org/) are popular because they let language specific objects in your application code govern your database schema. You get IDE\-native ergonomics (like autocomplete, inline type checks, jump\-to\-definition, safe refactors) that keep database code clean and close to your business logic. But there are downsides to creating an abstraction layer above SQL, from reduced visibility and control, to potentially leaky abstractions.


Interestingly, analytical workloads tend to amplify these ORM weaknesses. OLAP queries tend to be more complex and harder to optimize than simple CRUD operations. And analytical databases often provide specialized functionality—window functions, incremental aggregations, table engines, etc—that existing OLTP ORMs don’t expose.


But what if we could bring some of the benefits of ORMs to the world of OLAP? Or maybe to start: why don’t we just use the ORMs we already have for our new analytical needs?


## **OLTP ORMs Probably Shouldn’t Extend to OLAP** [\#](/blog/moosestack-does-olap-need-an-orm#oltp-orms-probably-shouldnt-extend-to-olap)


At first glance, extending an existing OLTP ORM seems like the most efficient path. They already have the core building blocks: schema APIs, query builders, migration tooling, and established communities. However, we’ve tried this approach (foreshadowing!) and found it ill\-advised. The foundational assumptions of an OLTP database are divergent from those of OLAP databases in ways that can create significant confusion and anti\-patterns for ORM users.


OLTP schema modeling APIs are built around the assumptions of row‑oriented, write‑time enforcement. OLAP databases like ClickHouse are column‑oriented, append‑only, and rely on background processing for deduplication. Those differences leak into the meaning of the ORM’s core modeling concepts.


If you take an ORM like Drizzle—built for OLTP—and just point it at an OLAP database like ClickHouse, you can create a false sense of sameness. The APIs might look the same, but the defaults, guarantees, and even the meaning of the same method names change drastically.


Let’s take two examples to illustrate the point: `nullable()` and `unique()`.


### Example \#1: Nullability is Inverted [\#](/blog/moosestack-does-olap-need-an-orm#example-1-nullability-is-inverted)


In OLTP, you assume by default that a column can accept a null value. To overwrite this constraint, you can add a modifier to the column to say that a value for a column is **required:**



```
import { integer, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
  integer: integer('integer').notNull(), // in OLTP, you override nullable assumption
});

```

In contrast, because OLAP stores data as columns rather than rows, it is expensive to have NULL values in a column. As a result, the default behavior in OLAP tables is that all columns are required. To overwrite this, [you mark a column as `NULLABLE`](https://clickhouse.com/docs/sql-reference/data-types/nullable).



```
CREATE TABLE t_null(
x Int8, 
y Nullable(Int8) -- in OLAP, you override required assumption
) ENGINE TinyLog 

```

If you were to reuse the same `.nullable()` / `.notNull()` API for both, you would flip the default meaning and hide the performance implications. A developer could easily create a schema that looks fine but performs poorly.


### Example \#2: “Uniqueness” is fundamentally different [\#](/blog/moosestack-does-olap-need-an-orm#example-2-uniqueness-is-fundamentally-different)


In OLTP databases (Postgres, MySQL, etc.), uniqueness is enforced at write time.



```
CREATE TABLE users (
  id UUID PRIMARY KEY, 
  email TEXT UNIQUE -- in OLTP, you enforce uniqueness positively
);

```

With this example, the moment you try to insert a duplicate `id` or `email`, the database rejects it. This works because OLTP inserts are usually small, row\-by\-row, and the database is optimized to check every write against existing data.


In OLAP, that guarantee is prohibitively expensive. Data is ingested in batches, and the database can’t check every row against existing data during ingestion without destroying performance. Instead:


- All rows are appended as‑is.
- Deduplication happens later during background merges.
- The merge process only knows what to keep if you explicitly define the rules.


That’s why `.unique()` alone is meaningless in OLAP. You must specify:


1. How to identify duplicates (sorting key)
2. Which record wins when there is a duplicate (version column, timestamp, or sequence number)
3. When to enforce uniqueness (during background merges or at query time)


Here’s how you might define a table for unique events in ClickHouse:



```
CREATE TABLE events
(
    event_id UUID,
    user_id UInt64,
    event_time DateTime,
    payload String,
    version UInt64 -- The "version" used to decide which duplicate wins
)
ENGINE = ReplacingMergeTree(version) -- The engine that handles deduplication
ORDER BY (event_id); -- The "key" that defines what a duplicate is


```

This creates a table that:


- Groups rows by event\_id
- Keeps the row with the highest version
- Discards the others, but only after merges


If you change the sort key or omit the version column, then the deduplication behavior changes entirely.


If you take `.unique()` from an OLTP ORM and silently remap it to this behavior, you muddy the contract. In OLTP, `.unique()` means “duplicates can’t exist.” In OLAP, it means “duplicates may exist until merges run, and the winner is determined by extra logic you must model yourself.”


That’s all to say, if you reuse the same modeling API across OLTP and OLAP, developers will assume they’re getting the same behavior—but they won’t be, or at least they shouldn’t be. The safer approach might be to design an OLAP‑specific modeling API that reflects OLAP’s defaults and semantics, instead of trying to “bolt on” OLAP support to an OLTP‑first ORM.


## So what might an ORM for OLAP look like? [\#](/blog/moosestack-does-olap-need-an-orm#so-what-might-an-orm-for-olap-look-like)


In short, we’d propose that a great developer experience (DX) layer for OLAP should selectively borrow from the transactional ORM playbook, while discarding what doesn't fit the analytical world:


**Borrow the best core concepts**:


- Schemas as application code means you get version control, PR review and type‑safe changes.
- A query builder that feels like SQL and lets you write “real” ClickHouse queries with IDE autocompletion and compile‑time checking.
- Local development and CI should mirror production so you can preview schema changes before they apply to prod.


**Promote OLAP\-friendly behavior**:


- Create OLAP\-native semantics and defaults (nullable, uniqueness/dedup, etc)
- Assume some schema changes will happen outside of the control of the application (eg. from CDC pipelines or downstream analysts)
- Offer OLAP\-native migration paths (favor versioned rollouts over in\-place `ALTER`)
- Expose types that can travel across all the infra that might surround your OLAP database (eg. [Kafka](https://kafka.apache.org/) ↔ ClickHouse)


**Don’t lose the power of OLAP**:


- OLAP databases like ClickHouse have powerful engines under the hood and rich OLAP\-specific functionality. A great DX should balance simplicity and power: exposing the right amount of complexity for optimizing common use cases, while providing escape hatches into full configurability.
- OLAP workloads revolve around aggregations, window functions and statistical functions—and have rich function libraries to show for it. The DX should make them easier to use, not hide them away.


## Applying ORM Principles in OLAP with MooseStack [\#](/blog/moosestack-does-olap-need-an-orm#applying-orm-principles-in-olap-with-moosestack)


For us, these principles have become more practical than theoretical as we’ve been building out [MooseStack](https://docs.fiveonefour.com/moose): an open source toolkit for developers building on analytical infrastructure. One of the core modules of MooseStack, [Moose OLAP](https://docs.fiveonefour.com/moose/olap), provides abstractions over ClickHouse in Typescript and Python. While Moose OLAP isn’t exactly an ORM itself, we knew there was a lot we could learn from the world of transactional ORMs.


### Schemas as Composable, Cross\-System Code [\#](/blog/moosestack-does-olap-need-an-orm#schemas-as-composable-cross-system-code)


It all starts with schemas as code—one of the most valuable aspects of ORMs. Our first Moose OLAP prototype tried repurposing [Prisma schemas](https://www.prisma.io/) to model ClickHouse tables.



```
model ClickHouseTable {
  id        Int      
  createdAt DateTime  
  name      String?
}

```

It accomplished a familiar developer experience, but quickly exposed a few practical problems:


- **We couldn’t refer to models directly in code,** and ended up generating TypeScript types from Prisma models just to use them in business logic.
- **Composition/inheritance was too limited.** OLAP favors denormalized, derived tables, so we wanted type\-level reuse that composes columns into a single wide table—no joins. Prisma lacks true schema inheritance and pushes reuse via relations (normalized tables \+ join\-time composition). That’s misaligned: OLAP doesn’t enforce Foreign Keys, joins are costly, and precomputed denormalized shapes win. We needed native extends/mixins within one table.
- **OLAP\-native semantics.** Prisma’s types didn’t map cleanly to ClickHouse features we care about (e.g., Nullable, LowCardinality, engine\-specific tags).


Since we were already generating TS types to get work done, the simpler path was to go all\-in on native language types (akin to Drizzle / [SQLModel](https://sqlmodel.tiangolo.com/)) and annotate for ClickHouse where needed. This is what data modelling in Moose OLAP looks like now:



```
interface DataModel {
	columnName: Key<string>;
	secondColumnName: Date;
}

export const table = new OlapTable<DataModel>("table_name")

```

A few key ideas here, that are critical for making schema\-as\-code data modelling successful for OLAP:


**1\) OLAP\-native configuration.** Key configuration options like selecting “order by” fields, selecting ClickHouse engines, setting field nullability, etc are all exposed through the interface, with sane defaults specifically for OLAP workloads.



```
export const table = new OlapTable<DataModel>("table_name", {
	orderByFields: ["columnName"]
	engine: ClickHouseEngines.MergeTree
})

```

**2\) Schema–table decoupling and composability.** Because a schema is just a TypeScript interface (or a [Pydantic](https://docs.pydantic.dev/latest/) Model), you can extend and reuse it naturally:



```
interface DataModel {
columnName: Key<string>;
	secondColumnName: Date;
}

interface ExtendedModel extends DataModel {
payload: Record<string, Any>; // JSON column
version: number;
}

const extendedTable = new OlapTable<ExtendedModel>("another_table_name")

```

This makes sense in OLAP pipelines: you often create derived tables that share most fields with an upstream table but add a few computed columns. Being able to reuse and extend schemas creates lineage trails and reduces repetition.


This also means that as long as your existing transactional ORM uses (or can generate) native types, you can share / reuse those as base models to be extended for your analytical stack.


**3\) Union types enable cross‑system compatibility.** A column’s base type (e.g., `string`) can be extended with tags (e.g., `LowCardinality` or `ClickHouseInt<”int8”>`) to model specific ClickHouse data types.



```
interface DataModel {
columnName: string & LowCardinality; //ClickHouse specific typing
	secondColumnName: number & ClickHouseInt<'int8'>; //ClickHouse specific typing 
}

```

The base type can then be serialized to a Kafka schema registry, while the tags tell Moose how to map it in ClickHouse. This lets you leverage the same type definition across your Kafka topics *and* your ClickHouse tables, preventing schema drift when data flows from your streams to your OLAP tables.


This capability also leverages the [Typia](https://typia.io/) (TS) and [Pydantic](https://docs.pydantic.dev/latest/) (Python) schema validation libraries. This means, not only do you get custom types passed to your ClickHouse schema, but you also get type constraints that can power runtime data validation in [Moose APIs](https://docs.fiveonefour.com/moose/apis) on data ingestion or retrieval.


### Embracing ORM\-like Typing in SQL for Complex Queries [\#](/blog/moosestack-does-olap-need-an-orm#embracing-orm-like-typing-in-sql-for-complex-queries)


If you’ve got your OLAP schemas as objects in your application code, the logical next step is building queries that utilize these objects for type safety, auto\-complete, etc.


Traditional ORMs provide high‑level “relational APIs” (`User.findMany()`) to abstract away SQL. That’s great for simple row‑oriented reads and writes, but it leaks for analytics operations. OLAP queries rarely operate on individual rows; they aggregate millions of rows and apply sophisticated functions. Generic CRUD helpers can’t express “approximate top‑k per user within the last hour” or “ANOVA across multiple groups.”


Instead, Moose OLAP borrows from the “[if you know SQL, you know Drizzle](https://orm.drizzle.team/docs/data-querying)” philosophy. Currently, you write your database queries as a tagged `sql` template literal. By using the `sql` template, you can interpolate your table and column names from the objects you’ve modeled in your code, so you get better type safety compared to regular raw SQL strings in your code, while preserving the full expressiveness of the underlying SQL.



```
sql`SELECT 
${events.columns.user_id}, 
approxTopK(5, ${events.columns.event_name} 
FROM ${events} 
GROUP BY ${events.columns.user_id}`

```

ClickHouse’s SQL dialect has a lot of functions and nuances. When you’re new to the engine, this can be overwhelming. Autocomplete \+ type\-checked identifiers help avoid silly mistakes as you write your queries.


This is the current state. But we’re considering going further with query\-builder type functionality. Drizzle’s chained query builder API stays very close to SQL, and will still flag syntax errors in your IDE if you group by a column you didn’t select. Adopting a similar approach with Moose OLAP could look something like this:



```
db.select({
  user_id: events.user_id,
  top_events: approxTopK(5, events.event_name)
})
.from(events)
.groupBy(events.user_id);

```

The hard part isn’t “a nicer API”. The challenge here is preserving 1 access to ClickHouse’s full surface area (functions, modifiers, hints, etc) so you can still reason about plans and costs, without building something that’s impossible to maintain as the dialect evolves.


**Open question for readers:** Where’s the right line between a type\-safe builder and “just write SQL”? What would you want typed (functions? combinators? window frames?) vs. left as raw SQL to keep intent and performance crystal clear?


### OLAP\-first Schema Management and Migrations [\#](/blog/moosestack-does-olap-need-an-orm#olap-first-schema-management-and-migrations)


If you’ve built migrations with OLTP ORMs, the muscle memory is simple: edit your models in your codebase, generate a migration, apply it, and your database ends up matching your code. This is the [“code\-first” approach](https://orm.drizzle.team/docs/drizzle-kit-generate) that most ORMs follow, where your code is the source of truth, and all database changes must go through the ORM. That works well in a closed loop where one service owns both the schema and the writes. However, this assumption rarely holds up for OLAP. Instead, most OLAP databases sit between many producers upstream (CDC, ETL, third\-party APIs) and many consumers downstream (dashboards, ML jobs, internal APIs, human or agentic analysts). Schemas can change under your feet, and cutovers ripple through systems you don’t control.


Some ORMs do support a [“database\-first” approach](https://orm.drizzle.team/docs/drizzle-kit-pull), where the code is derived from the actual state of the database, but this typically doesn’t come with migration support, since it’s intended to be used when a separate migration tool is managing the database schemas.


With Moose OLAP, we’re trying to find a happy medium that:


1. Maintains the code as the source of truth by default
2. Offers robust migration support and automation
3. Expects and gracefully handles cases where the code and the database diverge


#### Migration Planning in MooseStack [\#](/blog/moosestack-does-olap-need-an-orm#migration-planning-in-moosestack)


We’ve seen above how you can define OLAP tables as code with Moose OLAP. In your [Moose local dev](https://docs.fiveonefour.com/moose/getting-started/local-dev) environment (`moose dev`)—where you can iterate safely—schema changes are hot\-reloaded into your local ClickHouse. For example, if you have table named `events` defined in your code, and you add a new `status` field to the schema:



```
interface EventSchema {
	id: Key<string>
	number: number & ClickHouseInt<"int64">	status: string   // <--- new field
}

const events = new OlapTable<EventSchema>("events")

```

The second you save your changes, you’ll see the infrastructure updates logged to your terminal.



```
$ moose dev
⠋ Processing Infrastructure changes from file watcher
     ~  Table: events
          Column changes:
               + status: String

```

But what about going to production, where you want a migration path that inspires trust and confidence? [Moose Migrate](https://docs.fiveonefour.com/moose/migrate#how-it-works) generates the actual SQL that will be applied to your database during deployment to execute the migration. You can review this migration plan showing all the proposed changes implied by your code, before going to production. This planning capability can be integrated into your local development flow, your CI/CD automation, and your PR review process. So when you’re ready to deploy changes to production, you can be confident in what exactly you’re deploying.


#### Expecting and Handling Schema Drift [\#](/blog/moosestack-does-olap-need-an-orm#expecting-and-handling-schema-drift)


Most ORMs and their related migration tools generate migration plans by diff’ing code↔code (ie. comparing the new models vs. the last migration snapshot). This is usually reliable in the OLTP world, where the database shouldn’t change out of band, and code snapshots should reflect current reality.


But in OLAP, where unexpected schema changes are the expectation, static, code\-first migrations that presume authority can generate the wrong SQL. This is exacerbated by the fact that, as OLAP databases lack transactions, a failed migration can be more challenging to rollback than in OLTP.


To help mitigate this risk, Moose Plan flips the default diff mechanism to a code↔live database method. We aren’t reinventing the wheel here, but we are borrowing from a less common paradigm found in some OLTP migration tools ([Alembic](https://alembic.sqlalchemy.org/en/latest/autogenerate.html), for example). Instead of comparing code↔code, `moose plan` compares your desired schema to the actual state of the production database. This way, if the schema has drifted, Moose Migrate will know about it, you’ll know about it, and your migration plan will account for it.


Additionally, within your Moose OLAP Table objects, you can declare ownership explicitly. If a table is managed by CDC (e.g. via ClickHouse’s [ClickPipes](https://clickhouse.com/cloud/clickpipes)) or another external ETL service, [mark it](https://www.fiveonefour.com/blog/Introducing-Lifecycle-Management) `EXTERNALLY_MANAGED` and Moose will observe it without trying to mutate it:



```
import { OlapTable, LifeCycle } from "@514labs/moose-lib";
 
interface ClickPipesUserEvent {
  user_id: string;
  event_type: string;
  event_data: Record<string, any>;
  captured_at: Date;
  source_table: string;
}
 
const clickPipesEvents = new OlapTable<ClickPipesUserEvent>("clickpipes_events", {
  lifeCycle: LifeCycle.EXTERNALLY_MANAGED
});

```

Moose Migrate is another area of MooseStack that we’re really interested in expanding. Coming soon is the ability to express intent when the migration tool can’t safely guess it (e.g., “rename this column” vs “drop and recreate”). We’re also exploring another common migration pattern in OLAP: staged, versioned rollouts. Since OLAP databases tend to have many upstream and downstream dependencies, a best practice is often to follow API\-style versioning, where you run multiple versions of the same table/view/etc at once, and deprecate older versions over time. This allows producers and consumers that depend on that table—but that are outside of your control—to migrate on their own time to the latest version.


![ch-fiveonefour-diag.png](/uploads/ch_fiveonefour_diag_92c24678d5.png)
Versioned tables are already supported in Moose OLAP, and ClickHouse’s [materialized views](https://clickhouse.com/docs/materialized-views) (also [supported](https://docs.fiveonefour.com/moose/olap/model-materialized-view)) offer an elegant path for migrating data between versioned tables (we could do a whole blog post in this \- let us know if you’re interested!). We suspect there are opportunities for Moose Migrate to automatically generate migration helpers to simplify the architecting and deployment of this kind of versioned release model.


## Conclusion: Beyond an ORM for OLAP [\#](/blog/moosestack-does-olap-need-an-orm#conclusion-beyond-an-orm-for-olap)


We’ve hinted at it throughout this post, but the various modules of [MooseStack](https://docs.fiveonefour.com/moose) extend far beyond the ORM\-inspired capabilities of [Moose OLAP](https://docs.fiveonefour.com/moose/olap) covered in this post. Our mission at [Fiveonefour](https://www.fiveonefour.com/) is to bring great developer experiences to the analytics stack \- and this covers everything from streaming topics and orchestrated workflows, to the local dev server, to github integrations and preview branches, to AI copilots. More to come on this in the future!


In the meantime, we’d absolutely love it if you wanted to get your hands on Moose OLAP to try it out. [In less than 5 minutes](https://docs.fiveonefour.com/moose/getting-started/from-clickhouse) you can be up and running with Moose \+ your existing ClickHouse deployment, or point at the [ClickHouse playground](https://clickhouse.com/docs/getting-started/playground) environment to kick the tires.


[We’re building this in the open](https://github.com/514-labs/moose), and we’re likely wrong about some of it. If you’re running ClickHouse at scale, if you’ve solved schema annotations better, if you have a typed\-SQL approach that keeps the engine’s edge without turning into a maintenance burden, or if you’ve run smooth topic/table version cutovers, we want to learn from you: find us on [Slack here](https://join.slack.com/t/moose-community/shared_invite/zt-2fjh5n3wz-cnOmM9Xe9DYAgQrNu8xKxg), and give us a shout. The goal isn’t to force an ORM on OLAP; it’s to make analytics feel as developer\-friendly as the best web stacks—without losing the power that makes OLAP worth using in the first place.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

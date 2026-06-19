# Manage your ClickHouse Schema\-as\-Code using Atlas


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Manage your ClickHouse Schema\-as\-Code using Atlas

![](/_next/image?url=%2Fuploads%2Frotem_90bcd87c4f.png&w=96&q=75)Rotem TamirMar 12, 2024 · 7 minutes read
> Today, we welcome Rotem Tamir from [ariga](https://ariga.io/), who maintains the open\-core tool [atlas](https://atlasgo.io/) for managing database schemas as code. Rotem dives into the details and shows the value of the recent support for ClickHouse.


## The Rise and Fall of Schema\-less Technologies [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#the-rise-and-fall-of-schema-less-technologies)


In the early 2010s, dynamically typed languages like Python and Javascript, and NoSQL databases like MongoDB and Elasticsearch marked the trend of departing from rigid, upfront schema planning. All of these technologies, with less verbose syntax and greater flexibility, promised quicker development cycles and easier prototyping, making them the languages of choice for startups and new projects aiming for rapid market entry.


However, as projects and organizations grew larger in size and complexity, the initial advantages of these technologies began to reveal significant trade\-offs. The lack of schema enforcement led to inconsistencies in data, making it harder to ensure data quality and integrity as applications evolved. The absence of strict type systems and the flexible nature of schema\-less databases made debugging and maintaining large codebases increasingly difficult.


The increasing interest in relational storage technology such as ClickHouse signifies a nuanced shift in our industry’s approach to data management. While modern data systems need to process diverse datasets that sometimes require an unstructured approach, there is a growing appreciation for the efficiency and organization that comes with strongly typed, structured data processing methods.


## Managing Schemas is still a Pain [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#managing-schemas-is-still-a-pain)


One of the drivers of the NoSQL movement was that many developers wanted to avoid the pains of managing database schemas at all costs. Schema changes, also called migrations, require technical expertise to be done safely and efficiently. Modern databases provide a limited, *imperative*, way of changing schemas called DDL statements.


What if instead of giving up on schemas and their benefits entirely, we could make managing them a seamless process that does not require any special effort? Administering database schemas undoubtedly requires technical expertise, but it's not an infinitely complex problem. Thus, automated tools can be created to simplify the task for non\-experts.


## Database Schema\-as\-Code [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#database-schema-as-code)


![atlas_declarative_vs_imperative.png](/uploads/atlas_declarative_vs_imperative_ffff9cd809.png)
In recent years, in the wake of huge advancements made in cloud resource management with an approach called [Infrastructure\-as\-Code](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code), a new approach for managing database schemas is emerging. This approach, coined ["Database Schema\-as\-Code"](https://atlasgo.io/blog/2024/01/24/why-schema-as-code) and embodied by projects such as [Atlas](https://atlasgo.io) and [Skeema](https://www.skeema.io/), aims to greatly simplify schema management by arming engineers with a tool that offers a \_declarative \_API for interacting with databases.


A declarative API works by providing the tool with the *desired state* of the system and letting the tool figure out the operations needed to reconcile it with the *current state*. In the context of database schema management, users provide the tool with the schema they would like their database to have, let the tool inspect the current database information schema, and generate a migration plan for them automatically.


Automatic migration planning isn’t a new concept, of course. Application development frameworks and ORMs such as Django, have offered similar capabilities for many years. The issue with automating migration planning at the ORM level is that they are only usable in their specific context and cannot be applied generically for every stack. In addition, ORMs tend to focus on a small subset of database features such as tables, columns, foreign keys, and indexes and do not provide a way to manage more advanced objects such as views, materialized views, stored procedures, etc.


## How it works [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#how-it-works)


Let’s see how Database Schema\-as\-Code and declarative migrations work in practice. To demonstrate it we will use [Atlas](https://atlasgo.io), an open\-core database schema\-as\-code tool (F.D: I am one of the creators). For getting started and installation instructions, visit the [Atlas docs](https://atlasgo.io/getting-started).


As a prerequisite to this demo, let’s run a local, empty ClickHouse instance using Docker:



```
docker run --rm -d --name atlas-demo -e CLICKHOUSE_DB=demo -p 9000:9000 clickhouse/clickhouse-server:latest

```

Contrary to more traditional approaches, with declarative migrations, we always start with the desired state of the database. Let’s create a file named `schema.sql` with the following contents:



```
CREATE TABLE `users` (
   `id` UInt64,
   `name` String)
ENGINE = MergeTree
PRIMARY KEY (`id`)
ORDER BY `id`;

```

Now, we can apply this schema to the target database using the `atlas schema apply` command:



```
atlas schema apply \
-u "clickhouse://localhost:9000/demo" \
--to file://schema.sql \
--dev-url "docker://clickhouse/23.11/demo"

```

This will tell Atlas that we want to apply the schema defined in the file named `schema.sql` to the ClickHouse database at `localhost:9000/demo` (which we just used Docker to spin up locally).


Atlas connects to the target database, inspects its information schema, calculates the diff between the current and desired state, and prompts us to approve the migration plan:



```
-- Planned Changes:
-- Create "users" table
CREATE TABLE `users` (
  `id` UInt64,
  `name` String
) ENGINE = MergeTree
 PRIMARY KEY (`id`) SETTINGS index_granularity = 8192;
? Are you sure?:
  ▸ Apply
    Lint and edit
    Abort

```

The plan looks good, and so we hit "Apply" to apply the changes to the database.


After successfully running the migration Atlas planned for us, we can re\-run the `schema apply` command to ensure that the database is at its desired state:



```
atlas schema apply \
-u "clickhouse://localhost:9000/demo" \
--to file://schema.sql \
--dev-url "docker://clickhouse/23.11/demo"

```

Once again, Atlas connects to our ClickHouse instance, inspects it, and calculates the diff, this time telling us:



```
Schema is synced, no changes to be made

```

Next, let’s make a small change to our desired state to show that declarative migrations work on a live database with an existing schema. Let’s add a new column to our `users` table, `email_address`. Edit `schema.sql` adding the following column:



```
CREATE TABLE `users` (
    `id` UInt64,
    `name` String,
+    `email_address` String
)
 ENGINE = MergeTree
 PRIMARY KEY (`id`)
ORDER BY `id`;

```

Next, let’s re\-run the `schema apply`command and see how Atlas plans the migration for us:



```
-- Planned Changes:
ALTER TABLE `users` ADD COLUMN `email_address` String;
? Are you sure?:
  ▸ Apply
    Lint and edit
    Abort

```

Great! Atlas detected the existing table and planned migration to add the missing column to the target database. Let’s hit `Apply` to bring our database to the desired state.


## Wrapping Up [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#wrapping-up)


The 2010s trended towards schema\-less databases as developers sought to avoid the complexities of schema management, but this shift led to challenges in data consistency and maintenance as systems scaled. Learning from the challenges of the past, the tech industry is now showing a renewed interest in relational technologies.


However, developers still face the same challenges with schema management as they did in the past. Database Schema\-as\-Code tools such as [Atlas](https://atlasgo.io) emerge as a solution, offering to simplify and streamline schema operations, bridging the gap between the desire for development efficiency and the need for structured data integrity.


In this article, we have shown a glimpse of the capabilities of Atlas which in what is by no means a comprehensive guide. A more complete "Getting Started with Atlas" for ClickHouse users is available on the [Atlas documentation website](https://atlasgo.io/guides/clickhouse).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

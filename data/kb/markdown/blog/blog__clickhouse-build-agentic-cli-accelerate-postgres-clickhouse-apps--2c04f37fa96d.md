# clickhouse.build: An agentic CLI to accelerate Postgres apps with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# clickhouse.build: An agentic CLI to accelerate Postgres apps with ClickHouse

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fpete_h_avatar_b5e79cbc11.jpg&w=96&q=75)![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene), [Pete Hampton](/authors/pete-hampton) and [Al Brown](/authors/al-brown)Dec 2, 2025 · 13 minutes read[clickhouse.build](https://github.com/ClickHouse/clickhouse.build) is an open source, agentic CLI that accelerates the adoption of ClickHouse within your existing Postgres\-backed TypeScript application. The goal is not to replace Postgres, but to seamlessly combine it with ClickHouse for analytical workloads, using the strengths of each database together, within the same application.


It uses a multi\-agent workflow that:


- Scans your Postgres\-backed codebase to identify analytical queries (whether SQL in\-line or ORM\-based)
- Determines which tables are required to support those analytical queries and creates a plan.
- Helps to automatically sync the relevant tables to ClickHouse Cloud using ClickPipes API.
- Rewrites the relevant portions of the code so that it uses ClickHouse for analytics and Postgres for transactions, while keeping the application backwards\-compatible by introducing a feature flag.


clickhouse.build is intended as an accelerator, and can help you to have a working proof of concept (PoC) in under an hour. You can use the PoC to evaluate how your application performs with a combined Postgres\+ClickHouse backend.


Already evaluating Postgres \+ ClickHouse? [Skip to how it works](#how-clickhousebuild-works), or read on to understand why these two databases are so good together.


![chbuild.png](/uploads/chbuild_8f68f3f55e.png)### Try clickhouse.build today

Try clickhouse.build today with a free trial of ClickHouse Cloud. Get a working PoC in under an hour.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-400-try-clickhouse-build-today-sign-up&utm_blogctaid=400)Work on clickhouse.build was initiated in partnership with the AWS Prototyping and Cloud Engineering ([PACE](https://www.linkedin.com/groups/12710205/)) team and uses Amazon Bedrock and the [Strands Agents SDK](https://github.com/strands-agents/sdk-python). We would like to thank our partners for this collaboration.


## Postgres \+ ClickHouse: the default data stack [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#postgres--clickhouse-the-default-data-stack)


Postgres \& ClickHouse have seen huge community adoption; they are the most popular open source databases in their respective categories, each with flourishing ecosystems around them. That adoption has seen [the two become an unbeatable duo](https://about.gitlab.com/blog/two-sizes-fit-most-postgresql-and-clickhouse/), with [agentic AI only accelerating the trend](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain).


### Adding ClickHouse to a Postgres application [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#adding-clickhouse-to-a-postgres-application)


ClickHouse doesn’t replace Postgres, instead, the two work in tandem to handle workloads that are best suited to them; transactional workloads go to Postgres, and analytical workloads go to ClickHouse.


Many application backends are sending all queries to Postgres, whether it's a `SELECT *` of a single row by ID, or performing a `SUM() … GROUP BY` over 100,00 rows. The former is where Postgres shines, while the latter can be 100\-1000x faster in ClickHouse.


![chb_pgonly_diag.jpg](/uploads/chb_pgonly_diag_8a9fd8e7ea.jpg)
With Postgres \+ ClickHouse, your application backend can send queries to the right database for the job. You avoid needing to oversize Postgres or fight with replication, and improve the user\-facing performance and experience. Prototyping the new architecture can take a few weeks, particularly if it's your first time with ClickHouse, while you identify the right queries to migrate, setup data synchronization, and update backend integration. Building this prototype is where clickhouse.build can help.


![chb_pg_and_ch_diag.jpg](/uploads/chb_pg_and_ch_diag_b7774d3bf6.jpg)## How clickhouse.build works [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#how-clickhousebuild-works)


The clickhouse.build CLI uses multiple, task\-specific agents to migrate Postgres\-backed TypeScript apps to a Postgres\+ClickHouse architecture. These agents can be used independently, or called via an all\-in\-one workflow. A Quality Assurance (QA) sub\-agent checks every proposed code change, which has been augmented with high\-quality reference examples.


There are 3 primary agents:


### Scanner [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#scanner)


The scanner agent scans your TypeScript code base and looks for Postgres queries. It currently works whether you use a direct Postgres driver with queries in code, or using the query builders of Prisma and Drizzle ORMs.


When it finds queries, it will inspect them to determine whether the query is better suited for Postgres or ClickHouse: single\-row lookups and insert/update/delete operations are typically best fit for Postgres, while COUNTs, SUMs and GROUP BYs are more optimal in ClickHouse. The scanner agent produces a structured output report with the identified queries that should be migrated to ClickHouse.

Loading video...*A demo of the scanner agent, called on its own outside of the all\-in\-one workflow*


### Data migrator [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#data-migrator)


The data migrator agent assists in syncing the necessary Postgres tables to ClickHouse. Based on the queries identified by the scanner agent, it determines which tables ClickHouse needs to serve the queries. It then generates the relevant ClickPipes API payloads to configure the [ClickPipes Postgres CDC connector](https://clickhouse.com/docs/integrations/clickpipes/postgres). This connector keeps ClickHouse in sync with Postgres, first backfilling all historical data, and then maintaining a continuous, real\-time flow of changes from Postgres to ClickHouse.

Loading video...*A demo of the data migrator agent, called on its own outside of the all\-in\-one workflow*


### Code migrator [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#code-migrator)


The code migrator agent handles the job of updating queries and code. It can adjust SQL syntax to be correct for ClickHouse (queries between Postgres and ClickHouse are often compatible without change, but not always, especially if ORM query builders are used), and update TypeScript code to call ClickHouse via the [official ClickHouse JS client](https://clickhouse.com/docs/integrations/javascript). This agent will pause the migrations after each significant step, requesting input for the human to accept or reject the changes proposed. It’s also possible to accept all changes in one command.


Rather than remove your existing, working Postgres queries, the code migrator uses a backwards compatible indirection pattern. The queries for each database are moved to separate utility files, and a feature flag lets you pick which backend to use at run time. This means you can easily toggle between the two modes to compare performance and correctness while you evaluate your resulting application.


#### QA agent [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#qa-agent)


The QA agent is a sub\-agent of the code migrator, which validates any changes made. The code migrator will suggest what it wants to do, and then ask the QA agent if the change is appropriate. The QA agent scans the change and runs checks and validations comparing patterns against patterns from a series of reference code bases that already use Postgres\+ClickHouse successfully.

Loading video...*A demo of the code migrator agent, called on its own outside of the all\-in\-one workflow*


### All\-in\-one workflow [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#all-in-one-workflow)


While each agent can be used on its own, the CLI has an all\-in\-one workflow that invokes each agent in the correct order (scanner \-\> data migrator \-\> code migrator). This is generally the recommended way to use the CLI for your PoC, but we won’t hold it against you if you want to call the agents yourself.


## Using clickhouse.build [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#using-clickhousebuild)


You can get the CLI from the [clickhouse.build GitHub repo](https://github.com/ClickHouse/clickhouse.build). The README contains detailed instructions on setting up and configuring the CLI.


With the CLI configured, **we recommend creating a new branch in your application repository to work in**. You can then run the all\-in\-one migration workflow:



```
uv run main.py migrate /path/to/your/repo --replication-mode cdc

```

This will walk through all agents in order: scanner \-\> data migrator \-\> code migrator. **The agents are not fully autonomous** by default. The CLI will prompt you to review and accept/deny changes as you go, though you can choose to “accept all” if you wish.


The scanner agent will go through your code, discover your Postgres queries, and output a structured JSON file of the queries, a description, and their file location. The data migrator agent will read this scan file and extract the names of tables that need to be replicated into ClickHouse. With the `--replication-mode cdc` option set, the **data migrator agent will produce the `curl` commands needed to configure ClickPipes Postgres CDC** via the [ClickHouse Cloud API](https://clickhouse.com/docs/cloud/manage/api/api-overview).


Currently, **the ClickPipes configuration commands require some manual input**. Along with the command, the output contains some environment variables you’ll need to complete some details about your ClickHouse Cloud account and Postgres instance. With these details completed, you’ll need to run the `curl` commands yourself.

Loading video...*A demo of running the ClickPipes configuration commands and validating the running ClickPipes service in ClickHouse Cloud*


The code migrator agent is the final piece of the workflow. It begins by loading the scan file and installing the [clickhouse.js driver](https://clickhouse.com/docs/integrations/javascript) using your project’s package manager. After loading some reference examples of Postgres\+ClickHouse implementations in its context, the agent begins analysing your code base to build a plan of what to change.


The agent aims to implement the ‘strategy pattern’, where the specific backend implementation is abstracted. This pattern means you can toggle between using the original Postgres backend or the new ClickHouse\+Postgres backend with a simple feature flag. A file for each of Postgres and ClickHouse is created under `lib/strategies` which contains the logic for serving your queries via each of the respective databases. The agent will attempt to find the correct way to integrate this into your project, which means the next step can vary a bit. A common pattern is to create a database configuration at `lib/db.ts` which implements the logic to toggle between these strategies, and then update your existing routes to use the backend as configured in `db.ts`.


With each step, you’ll be asked to review the changes (unless you have chosen to accept all), and the QA sub\-agent will automatically review changes for baseline quality against the reference examples.


The workflow will wrap up by ensuring your project builds, producing a summary of the changes it made, and instructions on how to use the feature flag to toggle between strategies. You can now evaluate the impact of using ClickHouse in your application.


### Evaluating the result [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#evaluating-the-result)


You can run your application as normal, and it should continue to use your existing Postgres implementation by default. To use the new ClickHouse implementation, **add the new feature flag to your environment variables: `USE_CLICKHOUSE=true`**. You can flip this flag to `false` to switch back.

Loading video...*A demo of an application being switched between Postgres and ClickHouse backends, showing a 3x gain in performance.*


We recommend testing the normal flows of your application, having new rows inserted into Postgres to test replication, and comparing the performance of features with and without the ClickHouse feature flag enabled.


In many cases, the difference is immediately obvious; you should see that stats, charts, and tables that display analytics load several times faster without perceptible latency. Though it can be more fun to put some logging in and see the real numbers!


The change in performance you’ll see can be variable, but generally, the larger your data, the bigger the performance gain.


## The clickhouse.build design principles [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#the-clickhousebuild-design-principles)


clickhouse.build is a highly opinionated implementation. Its design is informed by lessons we have learned building agents for [data warehousing](https://clickhouse.com/blog/ai-first-data-warehouse), [for SREs](https://www.youtube.com/watch?v=og8ieNxixp4), and [agentic analytics](https://clickhouse.com/blog/agent-facing-analytics).


We believe that the best agentic flows **keep the human in the loop**, not only keeping you informed, but also involved in the actions that are taken. **Backwards compatibility** ensures we can validate correctness and assess the real impact of changes.


Agentic workflows are new, our understanding is still evolving, and we should approach changes to production with caution, but **agents are an obvious accelerator in development and proof of concepts**.


Agents can be tuned for different tasks by supplying specific context and instructions, which means **we can have one agent optimised to make changes, and another optimised to validate those changes**. We’ve seen that this can be effective in reducing errors, but it isn’t always perfect \- that’s why we keep the human around, too.


**Evaluations might just be the highest impact and under\-explored area** that we see in agentic workflows today. Getting to an 80% level of quality can be achieved relatively easily, but going beyond this barrier takes significant effort. We think this is where evaluations become critical, allowing us to constantly review, assess, and improve. But they can also be hard to do, and easy to forget. To mitigate this, we aim to bake evaluations into the workflow itself, adopting new techniques and tooling as the space develops.


**Open\-source is the way forward.** There’s no secret sauce behind clickhouse.build. While most companies are building proprietary agents that are served from some black\-box API, we decided to build an open, client\-side application that’s free to use and free to adapt. Want a new LLM API? To support a new database? [We’d love for you to contribute!](https://github.com/ClickHouse/clickhouse.build)


## What’s next? [\#](/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps#whats-next)


[Accelerating Postgres with ClickHouse](https://clickhouse.com/resources/engineering/managed-postgres-for-ai-and-real-time-apps) is just the beginning for clickhouse.build. We started with Postgres because this combination has become the default data stack for high\-performance applications. But other transactional databases, like MySQL or MongoDB, benefit just as much and are a natural next step.


Similarly, we expect to expand support beyond TypeScript apps, with likely next candidates being Python, Go, Rust, or Ruby.


We also see this model benefiting not just application builders, but data and analytics engineers as well, where ClickHouse can reduce the cost and accelerate the workloads of cloud data warehouses.


clickhouse.build is open source and open for contributions. Feedback, suggestions, and comments are welcome; we’d love to see you in our [Community Slack](https://clickhouse.com/slack).

### Try clickhouse.build today

Try clickhouse.build today with a free trial of ClickHouse Cloud. Get a working PoC in under an hour.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-401-try-clickhouse-build-today-sign-up&utm_blogctaid=401)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

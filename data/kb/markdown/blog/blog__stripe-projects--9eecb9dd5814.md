# Agents can now provision ClickHouse and Postgres on ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Agents can now provision ClickHouse and Postgres on ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FImage_512x512_16_b2d9fc2d13.jpeg&w=96&q=75)[Chloé Carasso dit Carson](/authors/chloe-carson)Jun 10, 2026 · 3 minutes readClickHouse is now available in [Stripe Projects](https://projects.dev/), the new Stripe CLI workflow that lets developers and AI agents provision real infrastructure without leaving the command line.


Starting today, one command provisions a ClickHouse or Postgres service on ClickHouse Cloud, returns working credentials to your environment, and hands off to [`clickhousectl`](https://clickhouse.com/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud), a new ClickHouse CLI built for agents, so the agent can keep building.


## Why we built this [\#](/blog/stripe-projects#why-we-built-this)


Agents cannot create accounts, click through setup flows, or paste credentials into a config file. We built this integration so that spinning up a ClickHouse or Postgres service on ClickHouse Cloud is something an agent can do completely, with real credentials landing in the environment without any UI interaction.


Stripe Projects is the CLI workflow that puts it all together. Run `stripe projects init my-app`, select the services you need, and Stripe Projects provisions real resources in your own provider accounts, syncs credentials to your `.env`, and keeps everything auditable from the terminal. Credentials land in your environment without any manual steps, and the workflow is the same whether a human or an agent is running it.


This is a developer preview. We want feedback from teams building agent\-assisted workflows or just trying to cut the time from new repo to running app.


## What can you provision? [\#](/blog/stripe-projects#what-can-you-provision)


ClickHouse Cloud offers two services through Stripe Projects:


**ClickHouse** is the real\-time analytics database. ClickHouse is known for: high\-ingest, high\-concurrency, billions of rows in milliseconds. If your app needs to query event streams, power user\-facing analytics, or run aggregations at scale, this is the right service.


**Postgres (public beta)** is a fully managed Postgres service on ClickHouse Cloud, built on local NVMe storage for microsecond latency and up to 10x faster performance on I/O\-heavy workloads. For teams that need a transactional store alongside their analytics layer, both services are provisioned through the same CLI workflow, land in the same account, and share credentials.


## How credentials flow to the agent [\#](/blog/stripe-projects#how-credentials-flow-to-the-agent)


Once provisioning completes, credentials are written directly to your `.env` file in an agent\-readable format. From there, the agent picks them up and continues all operations through `clickhousectl`, the ClickHouse CLI, without any manual credential handling or context switching.



> Note: clickhousectl \>v0\.3\.0 is required.


## Try it [\#](/blog/stripe-projects#try-it)


ClickHouse is in the Stripe Projects developer preview today.



```

```
1# Create a project
2stripe projects init my-app
3
4# Add a ClickHouse service
5stripe projects add clickhouse/clickhouse
6
7# Or add a managed Postgres service (public beta)
8stripe projects add clickhouse/postgres
```

```
Install the Stripe CLI, run `stripe projects init my-app`, and add whichever service fits your stack. Credentials sync to `.env` automatically. From there, `clickhousectl` takes over: set up data ingestion with ClickPipes, query your service, and keep building without leaving the terminal.


To learn more, visit [clickhouse.com/cloud](https://clickhouse.com/cloud) or the [Stripe Projects documentation](https://docs.stripe.com/projects).

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-850-get-started-today-sign-up&utm_blogctaid=850)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_appoints_apac_leader_f2c3722e9c.jpg&w=828&q=75)Company and culture### [ClickHouse appoints new leader for Asia Pacific and expands global go\-to\-market leadership team](/blog/clickhouse-appoints-apac-leader-and-expands-global-gtm-leadership)

ClickHouse · Jun 8, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

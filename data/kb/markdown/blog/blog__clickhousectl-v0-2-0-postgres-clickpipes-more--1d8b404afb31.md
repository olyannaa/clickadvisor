# clickhousectl v0\.2\.0: Postgres, ClickPipes and more


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# clickhousectl v0\.2\.0: Postgres, ClickPipes and more

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)May 20, 2026 · 7 minutes readWe're releasing `clickhousectl` v0\.2\.0\. This release adds Postgres (local and ClickHouse Cloud managed), ClickPipes management for the full set of supported sources, SQL over HTTP against Cloud services, a few agent\-friendly output tweaks, and a standalone Rust client library for the ClickHouse Cloud API.


If you already have `clickhousectl` installed, update with:



```
clickhousectl update

```

If you don't, install it with:



```
curl https://clickhouse.com/cli | sh

```

## Postgres [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#postgres)


`clickhousectl` now manages Postgres, too. Just like ClickHouse, you can use it locally (Docker\-backed) and in ClickHouse Cloud (managed Postgres). Develop locally, and go to Cloud when you're ready for prod. Postgres managed by ClickHouse gives you the [fastest, enterprise\-grade cloud Postgres](https://postgresbench.clickhouse.com), backed by NVMes, with HA, read replicas, and point\-in\-time restore.


Local Postgres runs as a Docker container, keyed on `(name, major version)`. Data lives under `.clickhouse/servers/<name>-pg<major>/data/`, so a single name can host multiple Postgres majors with isolated state. Supported versions are 16, 17, and 18\.



```
# Pre-pull an image (optional; start pulls on demand)
clickhousectl local install postgres@16

# Start a Postgres instance
clickhousectl local postgres start --name dev --version 16 --port 5433

# Connect with psql (host psql if installed, otherwise docker exec)
clickhousectl local postgres client --name dev --query "SELECT 1"

# Write connection vars to .env
clickhousectl local postgres dotenv --name dev

# Stop / remove
clickhousectl local postgres stop dev
clickhousectl local postgres remove dev

```

ClickHouse and Postgres servers share `server list`, so you can see both engines side by side in a single command.


Cloud\-managed Postgres requires a [ClickHouse Cloud](https://console.clickhouse.cloud/signUp) account, and the CLI must be authenticated with API Keys.



```
# Create a managed Postgres service
clickhousectl cloud postgres create \
  --name my-pg \
  --region us-east-1 \
  --size c6gd.large \
  --storage-gb 100 \
  --pg-version 17 \
  --ha-type sync

```

## ClickPipes [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#clickpipes)


`clickhousectl` now creates and manages [ClickPipes](https://clickhouse.com/docs/integrations/clickpipes), ClickHouse Cloud's managed connectors for streaming and batch ingest.


Supported sources:




| Source | Mode | Subcommand |
| --- | --- | --- |
| S3 / GCP / Azure Blob | Batch | `clickpipe create object-storage` |
| Kafka / Redpanda / Confluent / MSK | Streaming | `clickpipe create kafka` |
| Amazon Kinesis | Streaming | `clickpipe create kinesis` |
| Postgres | CDC | `clickpipe create postgres` |
| MySQL | CDC | `clickpipe create mysql` |
| MongoDB | CDC | `clickpipe create mongodb` |
| BigQuery | Snapshot | `clickpipe create bigquery` |


Creating a Kafka pipe:



```
clickhousectl cloud clickpipe create kafka <service-id> \
  --name my-kafka-pipe \
  --brokers 'broker:9092' --topics events \
  --format JSONEachRow \
  --kafka-type redpanda \
  --auth SCRAM-SHA-256 --username user --password pass \
  --ca-certificate ./ca.crt \
  --database default --table events \
  --column "event_id:Int64" --column "name:String"

```

Creating a Postgres CDC pipe:



```
clickhousectl cloud clickpipe create postgres <service-id> \
  --name my-pg-pipe \
  --host db.example.com --pg-database mydb \
  --username pguser --password pgpass \
  --table-mapping "public.users:public_users" \
  --table-mapping "public.orders:public_orders"

```

Once a pipe is running, you can list, start, stop, scale, resync (for CDC pipes), and delete it:



```
clickhousectl cloud clickpipe list <service-id>
clickhousectl cloud clickpipe scale <service-id> <clickpipe-id> \
  --replicas 2 --cpu-millicores 250 --memory-gb 1
clickhousectl cloud clickpipe resync <service-id> <clickpipe-id>

```
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-650-get-started-today-sign-up&utm_blogctaid=650)## Improvements [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#improvements)


### Querying ClickHouse services in ClickHouse Cloud [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#querying-clickhouse-services-in-clickhouse-cloud)


Querying ClickHouse services in ClickHouse Cloud no longer requires a local ClickHouse binary to use as the client. The CLI now uses ClickHouse Cloud's Query Endpoints to send SQL over HTTP.


`cloud service create` provisions a Query Endpoint on new services by default. A new API Key is created that is scoped only to the new service (so it can't be used to go rogue), and the Query Endpoint itself is locked down to the new API Key. The CLI stores the new key alongside your existing API Key. `cloud service query` then runs SQL over HTTP using that key:



```
clickhousectl cloud service query --name my-service --query "SELECT 1"
clickhousectl cloud service query --id <service-id> \
  --query "SELECT count() FROM system.tables" \
  --format JSONEachRow
echo "SELECT 1+1" | clickhousectl cloud service query --name my-service

```

For existing services without a Query Endpoint or stored key, `cloud service query` provisions one lazily on first use. Pass `--no-auto-enable` to fail instead, or `--no-enable-query` on `service create` to skip the create\-time hook.


The query endpoint binding is created with role `sql_console_admin`, which grants read and write inside the bound service only. The API key itself has no org\-level roles, so the binding is the only thing granting access: a stolen key can only hit the service it was minted for. `cloud service delete` removes the stored key from `credentials.json`.


### Experience [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#experience)


Two small changes that make a difference when an agent (or a human) is reading output.


**Lighter tables.** Tabular output now uses Markdown\-style tables with ASCII separators instead of rounded Unicode box\-drawing characters. The result is friendlier to copy into a markdown file, a PR description, or a chat with an LLM, and uses fewer tokens when an agent is reading it.


**`--debug` for credential resolution.** Pass `--debug` to any `cloud` command to print the resolved credential source and the API URL to stderr before the command runs.



```
clickhousectl cloud --debug service list
# [debug] auth source: credentials file (.clickhouse/credentials.json)
# [debug] api url: https://api.clickhouse.cloud/v1
# ... normal output ...

```

## Rust clickhouse\-cloud\-api client library [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#rust-clickhouse-cloud-api-client-library)


`clickhousectl` manages ClickHouse Cloud using the [ClickHouse Cloud API](https://clickhouse.com/docs/cloud/manage/api/api-overview). The Cloud API code is now its own crate, [`clickhouse-cloud-api`](https://github.com/ClickHouse/clickhousectl/tree/main/crates/clickhouse-cloud-api), a typed async Rust client.


The CLI is now a consumer of this crate like any other downstream user.


## New contributors [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#new-contributors)


Thanks to the new contributors who shipped code in this release:


- Kaushik Iska ([@iskakaushik](https://github.com/iskakaushik))
- Mark Dawson ([@markdawson](https://github.com/markdawson))


## What's next [\#](/blog/clickhousectl-v0-2-0-postgres-clickpipes-more#whats-next)


`clickhousectl` is only 5 weeks old at the time of releasing v0\.2\.0, but already over 5000 ClickHouse developers are using it to build with ClickHouse locally and in Cloud.


There's still lots of features to support: work is already underway for [ClickStack](https://clickhouse.com/cloud/clickstack) (the ClickHouse observability stack), and we're looking into local PeerDB support to mirror the Postgres\<\>ClickHouse CDC capabilities that are already possible in Cloud.


Outside of features, we're doing some exciting research into agentic experience (AX) and how we can better optimise the CLI, our APIs, MCP and other surface areas for agents. We're thinking about how we can improve an agent's ability to complete tasks, as well as their consistency, speed, tool calls, and cost. Expect some rapid iteration on the experience side.


`clickhousectl` is in beta, and we'd love to hear from you: please [raise issues in the `clickhousectl` repo](https://github.com/ClickHouse/clickhousectl) and join us in the [community Slack](https://clickhouse.com/slack).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

# Introducing clickhousectl: the CLI for ClickHouse local and cloud (beta)


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing clickhousectl: the CLI for ClickHouse local and cloud (beta)

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)Apr 9, 2026 · 5 minutes read`clickhousectl` is the official CLI for ClickHouse. It manages local installations, runs local servers, and operates ClickHouse Cloud. It's designed to work for humans and AI agents alike. It's in beta starting today.



```
curl https://clickhouse.com/cli | sh

```


> **Beta:** clickhousectl is currently in beta. Features and behavior may change.


## Why a CLI, and why now [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#why-a-cli-and-why-now)


Agentic development is the biggest shift in how software gets built in decades, and is fundamentally changing how platforms like ClickHouse will be used. High quality, powerful infrastructure matters more than ever, but it needs to adapt to a new way of working: agents interacting on behalf of the user.


Agentic Experience is now an integral part of Developer Experience.


ClickHouse is open source, it's a single binary, and it runs great on a laptop. The local developer experience has long been one of ClickHouse's many strengths. But the experience was designed for humans. There’s more we can do to help LLMs develop with ClickHouse.


Whether an agent is building a local prototype or deploying to production on ClickHouse Cloud, `clickhousectl` gives it a streamlined, predictable interface that supports agentic development.


## Local development [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#local-development)


### Version management [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#version-management)


`clickhousectl` works as a version manager for ClickHouse, inspired by tools like `uv` and `pnpm`. The CLI helps to discover and download available ClickHouse versions. Installed binaries are stored in a global repository at `~/.clickhouse/versions/`, so they can be reused across projects without duplicating storage.



```
# See what's available
clickhousectl local list --remote

# Install the latest stable release
clickhousectl local install stable

# Set the active version (installs it if needed)
clickhousectl local use stable

```

### Project scaffolding [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#project-scaffolding)


`clickhousectl` can scaffold a standard project structure for your ClickHouse SQL files. This is optional (use your own structure if you prefer), but for agents, having a consistent convention means less ambiguity when writing and organizing SQL.



```
clickhousectl local init

```

This creates:



```
clickhouse/
├── tables/                 # CREATE TABLE statements
├── materialized_views/     # Materialized view definitions
├── queries/                # Saved queries
└── seed/                   # Seed data and INSERT statements

```

### Running local servers [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#running-local-servers)


`clickhousectl` can create, manage and query local ClickHouse server instances. Each server gets its own isolated, persistent data directory, so you can run multiple servers side by side for different projects. If default ports are already in use, free ports are detected and assigned automatically.



```
# Start a server with the system default version (configured by `clickhousectl local use`)
clickhousectl local server start --name dev

# Connect and run a query
clickhousectl local client --name dev --query "CREATE DATABASE product"

# Run SQL from a file
clickhousectl local client --name dev --queries-file clickhouse/tables/events.sql

# Start a second server with a specific version
clickhousectl local server start --name dev-new --version 26.3

```

## ClickHouse Cloud [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#clickhouse-cloud)


When it's time to go to production, the same CLI that managed your local development now manages your cloud infrastructure. The cloud commands cover organizations, services, backups, API keys, team members, invitations, and activity logs. Every command supports `--json` output for easy parsing by agents and scripts.



```
# Create with specific infrastructure
clickhousectl cloud service create --name my-service \
  --provider aws \
  --region us-east-1 \
  --min-replica-memory-gb 8 \
  --max-replica-memory-gb 32 \
  --num-replicas 2

# List services
clickhousectl cloud service list

# Scale a running service
clickhousectl cloud service scale <service-id> \
  --min-replica-memory-gb 24 \
  --max-replica-memory-gb 48 \
  --num-replicas 3

```

## Destructive operations and permissions [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#destructive-operations-and-permissions)


clickhousectl supports destructive operations — removing servers, dropping data, deleting Cloud services — as you'd expect from a CLI.


Using the CLI with AI agents means those agents inherit the ability to perform destructive operations. We're still investigating what good looks like for agent guardrails here, so we'd encourage you to be cautious when pairing agents with clickhousectl around production resources.


For ClickHouse Cloud, clickhousectl supports two authentication methods: OAuth and API keys. OAuth uses a device flow that opens your browser. Credentials obtained through OAuth are read\-only, meaning you can list services, run queries, and inspect resources, but you cannot perform destructive operations. To create, scale, delete, or otherwise modify Cloud resources, you must authenticate with an API key.


API keys are created at the organization level, so an agent authenticated with a key is scoped to that organization and can't escape to another. You're responsible for creating the key and selecting its permissions — read\-write across all services, read\-only on some and read\-write on others, or whatever granularity fits your setup.


## Agent skills [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#agent-skills)


`clickhousectl` can also install the official [ClickHouse Agent Skills](https://github.com/ClickHouse/agent-skills) directly into your coding agents. In addition to the existing best practices skill, we’ve added 2 new skills that help your agent work with ClickHouse locally and in the cloud using the CLI.



```
# Interactive: choose your agents
clickhousectl skills

# Non-interactive: install into all detected agents automatically
clickhousectl skills --detected-only

```

## Get started [\#](/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud#get-started)


`clickhousectl` is in beta for macOS and Linux.



```
curl https://clickhouse.com/cli | sh

```

Tip: A `chctl` alias is created automatically for convenience.


We'd love feedback. If you hit issues or have ideas for what the CLI should do next, [let us know on GitHub](https://github.com/ClickHouse/clickhousectl).

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

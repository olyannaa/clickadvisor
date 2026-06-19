---
source: blog
url: https://clickhouse.com/cli
topic: introducing-clickhousectl-the-cli-for-clickhouse-local-and-cloud-beta
ch_version_introduced: '26.3'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

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

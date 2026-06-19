---
source: blog
url: https://grupomasmovil.com/
topic: how-grupo-masmovil-monitors-radio-access-networks-with-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 7
---

# How Grupo MasMovil Monitors Radio Access Networks with ClickHouse

\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Grupo MasMovil Monitors Radio Access Networks with ClickHouse

![](/_next/image?url=%2Fuploads%2FRodrigo_Aguirregabiria_Herrero_34bc55d4a9.jpeg&w=96&q=75)Rodrigo Aguirregabiria Herrero, Grupo MasMovilFeb 16, 2024 · 10 minutes read*We're excited to share this guest post from [Grupo Masmovil](https://grupomasmovil.com/), one of Spain's largest telecommunications operators. Rodrigo Aguirregabiria Herrero, a Senior Monitoring Engineer from Masmovil's OSS \& Tools Monitoring department, details the challenges of monitoring Radio Access Networks (RAN) and how ClickHouse has transformed their approach.*

For those who are not familiar with Radio Access Networks (RAN), they are the first point of access to mobile networks. These nodes allow your smartphone to access 2G, 3G, 4G and 5G networks.

These networks are large and require thousands of nodes (or antennas) to be deployed. This way, when you move away from one node, you can connect to another one and maintain your internet connection.

In MasMovil we decided to migrate from Telecom\-specific tools to open source technologies for BigData, one of these is ClickHouse which has allowed us to:

- Improve our monitoring solutions:
	- Having more reliable solutions
	- Speeding our processing times
	- Keeping more data
- Save costs in:
	- Software Licenses
	- 3rd level supports
	- Hardware

Let’s see how we’ve done it.

## The Actual Size of the Data [\#](/blog/how-grupo-masmovil-monitors-radio-access-networks-with-clickhouse#the-actual-size-of-the-data)

So, how can we monitor the thousands of nodes that provide internet services to millions of people?

There are several ways to do this, but in this case, we will focus on the information that comes directly from those nodes.

These nodes have many metrics to monitor almost every aspect of their performance, such as connection to other nodes, number of calls, traffic, and literally thousands of counters per node.

We don’t need all that information, so we filter it. However, we still have hundreds of counters and thousands of nodes, all publishing data every 15 minutes.

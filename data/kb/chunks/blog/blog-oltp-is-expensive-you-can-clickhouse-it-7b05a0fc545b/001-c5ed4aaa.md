---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"OLTP
topic: oltp-is-expensive-you-can-clickhouse-it-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 1
total_chunks_in_doc: 6
---

# OLTP is expensive, you can ClickHouse it. \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"OLTP is expensive, you can ClickHouse it.","description":"Offload settled Postgres data to ClickHouse to reduce storage and query costs while keeping active transactions in Postgres.","image":"/uploads/OLTP\_is\_expensive\_Click\_House\_is\_better\_for\_most\_of\_your\_data\_d1bc1900f3\.png","publisher":{"@type":"Organization","@id":"https://clickhouse.com/\#organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-10\-15T14:59:39\.900Z","dateModified":"2026\-10\-15T14:59:39\.766Z","author":{"@context":"https://schema.org","@type":"Person","name":"Andrey Chudnovskiy","url":"https://clickhouse.com/authors/andrey\-chudnovskiy","@id":"https://clickhouse.com/authors/andrey\-chudnovskiy\#person","image":"/uploads/andrey\_f81fcad742\.jpg","jobTitle":"Platform Tech Lead"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# OLTP is expensive, you can ClickHouse it.

![andrey](/_next/image?url=%2Fuploads%2Fandrey_f81fcad742.jpg&w=96&q=75)[Andrey Chudnovskiy](/authors/andrey-chudnovskiy)Oct 15, 2026 · 9 minutes read
div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

## Summary \#

In this article we explore a new application pattern \- offloading more of your Postgres data to ClickHouse. Leading to an order of magnitude better unit economics for your applications, as the data size increases.

We start with what an Online Transactional Processing (OLTP) database like Postgres does on every write and read, and the costs it takes on to keep transactions ACID\-compliant. We then show how to stop paying those costs for the data and queries that don’t need them.

![](/_next/image?url=%2Fuploads%2Foltp_oct2026_postgres_clickhouse_matrix_863a16d405.png&w=2048&q=75)

## The last time the datasets exploded \#

Back in the 2000s Web and Mobile booms exponentially increased the dataset sizes the systems needed to process. At the time, many fast growing companies turned to NoSQL databases for scalability and efficiency, which SQL databases couldn’t provide at the time.

Over the following few years the question of operational databases' scalability was resolved. With the cloud advancements, the latest systems offer tens of terabytes on single\-writer OSS PostgreSQL deployments. With some closed source forks scaling beyond 100 TB of storage without compromising OLTP guarantees. While systems like Spanner and sharded MySQL/Postgres allow web\-scale companies to achieve transactional consistency at global scale.

The increased scalability comes with a big cloud infrastructure bill. The systems based on OLTP engines scale linearly at best. You pay N times more for Postgres, you get up to N times more storage and processing power. With ClickHouse Managed Postgres NVMe based architecture you can get better multipliers on transactional throughput.  

Still though as your dataset sizes explode, the compute and storage costs grow linearly.

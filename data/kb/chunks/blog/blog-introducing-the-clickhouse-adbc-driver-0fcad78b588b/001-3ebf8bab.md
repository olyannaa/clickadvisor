---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"One
topic: one-driver-one-format-every-language-adbc-clickhouse
ch_version_introduced: '0.1'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 10
---

# One Driver, One Format, Every Language: ADBC \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"One Driver, One Format, Every Language: ADBC","description":"ClickHouse now has an official ADBC driver, giving Ruby, R, C, and every other ADBC\-aware tool zero\-conversion, Arrow\-native access to ClickHouse without a dedicated client for each language.","image":"/uploads/ADBC\_Logos\_aff1f6d333\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-07\-10T15:00:55\.868Z","dateModified":"2026\-07\-10T15:00:55\.771Z","author":{"@context":"https://schema.org","@type":"Person","name":"Luke Gannon","url":"https://clickhouse.com/authors/luke\-gannon","@id":"https://clickhouse.com/authors/luke\-gannon\#person","image":"/uploads/Luke\_Gannon\_NE\_4\_J\_5562a05272\.jpeg"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# One Driver, One Format, Every Language: ADBC

![luke gannon ne4j](/_next/image?url=%2Fuploads%2FLuke_Gannon_NE_4_J_5562a05272.jpeg&w=96&q=75)[Luke Gannon](/authors/luke-gannon)Jul 10, 2026 · 15 minutes read## Summary

- **ClickHouse now has an official ADBC driver**, the modern, Arrow\-native alternative to ODBC and JDBC for analytics and AI applications.
- **Zero\-conversion, end\-to\-end columnar data movement**: results leave ClickHouse as Apache Arrow and arrive in your application as Apache Arrow, with no row\-oriented round trip in between.
- **Brings ClickHouse to languages without an official client**, including Ruby, R, and C, through a single Rust\-built driver rather than a separate implementation per language.
- **Install with one command** via `dbc`, the ADBC driver package manager, distributed through the ADBC Driver Foundry in partnership with Columnar.
ADBC is a modern database access standard from the Apache Arrow project, and today we are announcing the official ClickHouse driver for it. Whether you are building a data science pipeline in R, a Ruby web application that queries analytics, or a C application collecting IoT sensor data, you now have a single, standards\-compliant driver that works across all of them.

## What is ADBC? \#

ADBC (Arrow Database Connectivity) is the modern alternative to ODBC and JDBC for analytics and AI applications. It's a multi\-language API spec and driver standard that delivers data in Apache Arrow columnar format. Older standards like ODBC and JDBC gave the software industry a common way to talk to databases in a row\-oriented world; ADBC brings that standardization to the columnar world that modern analytics now runs on.

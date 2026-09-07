---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Announcing
topic: announcing-the-new-clickhouse-sql-playground-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 7
---

# Announcing the new ClickHouse SQL Playground \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Announcing the new ClickHouse SQL Playground","description":"Announcing the ClickHouse SQL Playground—now live at sql.clickhouse.com! With 35\+ datasets, 220\+ example queries, and easy sharing features, it’s never been easier to explore ClickHouse.","image":"/uploads/Announcing\_SQL\_playground\_4\_304f579ee6\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2024\-10\-29T15:59:12\.331Z","dateModified":"2026\-03\-03T12:38:15\.069Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Announcing the new ClickHouse SQL Playground

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 31, 2024 · 11 minutes read### TLDR \#

As part of our efforts to make querying large datasets easier than ever, we’re pleased to announce the availability of [sql.clickhouse.com](https://sql.clickhouse.com/?query=U0VMRUNUCiAgICBtb250aCx0eXBlLAogICAgYXZnKHByaWNlKSBBUyBwcmljZQpGUk9NIHVrLnVrX3ByaWNlX3BhaWQKR1JPVVAgQlkgdG9TdGFydE9mTW9udGgoZGF0ZSkgQVMgbW9udGgsIGlmKGR1cmF0aW9uID0gJ2xlYXNlaG9sZCcsICdsZWFzZWhvbGQnLCAnZnJlZWhvbGQnKSBBUyB0eXBlCk9SREVSIEJZIG1vbnRoIEFTQw&chart=eyJ0eXBlIjoibGluZSIsImNvbmZpZyI6eyJ4YXhpcyI6Im1vbnRoIiwieWF4aXMiOiJwcmljZSIsInNlcmllcyI6InR5cGUifX0&run_query=true&tab=charts)! This new SQL playground has over 35 datasets and 220 example queries to get started. We’ve included some simple charting capabilities, which we plan to improve, and the ability to save and share queries! Take it for a spin and share your favorite queries either on social or via the [GitHub repo](https://github.com/ClickHouse/sql.clickhouse.com), where we’ll add them for others to enjoy!

![sql.clickhouse.com.png](/_next/image?url=%2Fuploads%2Fsql_clickhouse_com_1db08a674b.png&w=2048&q=75)

## Background \#

As ClickHouse users, we are passionate about datasets. We even have an internal slack channel, aptly named "data lovers" for sharing interesting datasets for experimentation and testing of features! Historically, we've documented these datasets and tried to provide example queries to get users started. While we also made many of these datasets available in a public ClickHouse instance, also referenced from our documentation, this used the classic Play interface packaged with ClickHouse.

![old_play.png](/_next/image?url=%2Fuploads%2Fold_play_36776bd4f7.png&w=2048&q=75)

This Play interface is deliberately simple and ideal for getting started: it has no dependencies and is a single HTML file.

However, this didn’t provide the rich user experience we wanted for our playground. Ideally, we wanted something where users could navigate and save example queries while supporting syntax highlighting, autocomplete, query parameters, results export, basic charting, and rich sharing features. These features would allow users to explore datasets and hopefully help users get started with ClickHouse and share their problems.

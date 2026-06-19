---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-24-4
ch_version_introduced: '0.656'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 11
---

# ClickHouse Release 24\.4

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.4

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 5, 2024 · 18 minutes readAnother month goes by, which means it’s time for another release!

ClickHouse version 24\.3 contains **13 new features** 🎁 **16 performance optimisations** 🛷 **65 bug fixes** 🐛

## New Contributors [\#](/blog/clickhouse-release-24-04#new-contributors)

As always, we send a special welcome to all the new contributors in 24\.4! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.

Below are the names of the new contributors:

*Alexey Katsman, Anita Hammer, Arnaud Rocher, Chandre Van Der Westhuizen, Eduard Karacharov, Eliot Hautefeuille, Igor Markelov, Ilya Andreev, Jhonso7393, Joseph Redfern, Josh Rodriguez, Kirill, KrJin, Maciej Bak, Murat Khairulin, Paweł Kudzia, Tristan, dilet6298, loselarry*

Hint: if you’re curious how we generate this list… [click here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).

You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.4/).

## Recursive CTEs [\#](/blog/clickhouse-release-24-04#recursive-ctes)

### Contributed by Maksim Kita [\#](/blog/clickhouse-release-24-04#contributed-by-maksim-kita)

[SQL](https://en.wikipedia.org/wiki/SQL:1999) introduced recursive common table expressions (CTEs) for [hierarchical queries](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL), making SQL a [Turing\-complete](https://en.wikipedia.org/wiki/Turing_completeness) programming language.

So far, ClickHouse has supported hierarchical queries by utilizing [hierarchical dictionaries](https://clickhouse.com/docs/en/sql-reference/dictionaries#hierarchical-dictionaries). With our new query analysis and optimization infrastructure, now [enabled](https://clickhouse.com/blog/clickhouse-release-24-03#analyzer-enabled-by-default) by default, we finally have everything in place to introduce long\-awaited and powerful features like recursive CTEs.

ClickHouse recursive CTEs [have](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL) the standard SQL syntax and [pass](https://www.youtube.com/live/dtUqgcfOGmE?si=Dzg93iQE3a5XCutn&t=2813) all PostgreSQL tests for recursive CTEs. Furthermore, ClickHouse now has better support for recursive CTEs than PostgreSQL. Inside the CTE’s UNION ALL clause’s bottom part, multiple (arbitrarily complex) queries can be specified, the CTE base table can be referenced multiple times, etc.

Recursive CTEs can solve hierarchical problems elegantly and simply. For example, they can easily answer reachability questions for [hierarchical data models](https://en.wikipedia.org/wiki/Hierarchical_database_model) (e.g. trees and graphs) .

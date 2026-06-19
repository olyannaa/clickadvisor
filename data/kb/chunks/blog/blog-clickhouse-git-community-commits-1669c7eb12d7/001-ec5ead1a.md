---
source: blog
url: https://ghe.clickhouse.tech/
topic: git-commits-and-our-community
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

# Git commits and our community

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Git commits and our community

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 15, 2022 · 7 minutes read![community-is-strength.jpg](/uploads/community_is_strength_65569fbe5b.jpg)
This is the first in a series where we’ll highlight some cool queries and share interesting tips and tricks related to ClickHouse. For the first few posts, we will focus on an analysis of the ClickHouse repository using the `git-import` tool distributed with ClickHouse.

## Introduction [\#](/blog/clickhouse-git-community-commits#introduction)

In this post, we’d like to give some insights back to our community. The [Github archive](https://ghe.clickhouse.tech/) dataset has been the foundation for examples and demos for some time. While a great resource, it doesn’t track the details of repositories at a code level, e.g., commits and changes to lines of code, but instead focuses on issues, stars, PRs, and events. Meanwhile, Git insights (via pulse) are interesting but incomplete…and exploring ClickHouse is substantially more fun.

Fortunately, a tool is distributed with ClickHouse that solves this very issue: the `git-import` tool.

```

ClickHouse % clickhouse-git-import -h

A tool to extract information from Git repository for analytics.

It dumps the data for the following tables:
- commits - commits with statistics;
- file_changes - files changed in every commit with the info about the change and statistics;
- line_changes - every changed line in every changed file in every commit with full info about the line and the information about previous change of this line.

The largest and the most important table is "line_changes".

Run this tool inside your git repository. It will create .tsv files that can be loaded into ClickHouse (or into other DBMS if you dare).


```

For the ClickHouse repository, this generates files of the following sizes in a few minutes as of November 8th, 2022:

- `commits.tsv` \- 7\.8M \- 266,051 rows
- `file_changes.tsv` \- 53M \- 266,051 rows
- `line_changes.tsv` \- 2\.7G \- 7,535,157 rows

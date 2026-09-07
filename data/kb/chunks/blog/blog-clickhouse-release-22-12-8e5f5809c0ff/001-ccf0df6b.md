---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-22-12-clickhouse
ch_version_introduced: '0.236'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 6
---

# ClickHouse Release 22\.12 \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"ClickHouse Release 22\.12","description":"17 new features. 8 performance optimisations. 39 bug fixes. If that’s not enough to get you interested in trying it out. Check out some of the headline items: \* \`grace\_hash\` JOINs \* password complexity rules \* BSON support \* \`GROUP BY ALL\` support \* Add","image":"/uploads/22\_12\_Release\_Post\_36da60fb27\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2022\-12\-19T15:08:17\.293Z","dateModified":"2026\-03\-03T12:37:30\.759Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 22\.12

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 19, 2022 · 11 minutes readIt’s a holiday bonanza.

The delivery of 11 months of regular releases wasn’t enough for the team. Neither was the Early Access, Beta, and GA of ClickHouse Cloud. Speaking of which, if you want the easiest way to run ClickHouse in production (or for development) start a free trial of [ClickHouse Cloud](https://clickhouse.cloud/signUp&loc=blog) today.

As a holiday gift, we are pleased to introduce 22\.12\.

## Release Summary \#

17 new features. 8 performance optimisations. 39 bug fixes.

If that’s not enough to get you interested in trying it out. Check out some of the headline items:

- `grace_hash` JOINs
- password complexity rules
- BSON support
- `GROUP BY ALL` support
- Addition of a Prometheus endpoint for ClickHouse Keeper

And, of course, a host of performance improvements.

## Helpful Links \#

- [22\.12 Release Changelog](https://clickhouse.com/docs/en/whats-new/changelog/)
- [22\.12 Release Presentation](https://presentations.clickhouse.com/release_22.12)
- [ClickHouse 22\.12 Release Webinar](https://www.youtube.com/watch?v=sREupr6uc2k)

## Grace Hopper Hash Join (Sergei Skvortsov \+ Vladimir Cherkasov) \#

Historically, in ClickHouse, users had a few choices with respect to joins: either use the `hash` method, which is fast but memory\-bound or revert to using the `partial_merge` algorithm. The latter relies on sorting data and dumping it to disk, often overcoming memory at the expense of performance. While this at least allowed users to execute large joins, it often suffered from slow performance. With this release, we introduce an exciting non\-memory bound addition to the join algorithms, which overcomes some of the performance challenges of partial merge: The Grace Hash.

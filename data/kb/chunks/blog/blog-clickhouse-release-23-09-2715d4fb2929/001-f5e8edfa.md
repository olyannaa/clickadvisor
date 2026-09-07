---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-23-9-clickhouse
ch_version_introduced: '2.31'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 10
---

# ClickHouse Release 23\.9 \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"ClickHouse Release 23\.9","description":"ClickHouse 23\.9 is available with 20 new features, 19 performance optimizations \& 55 bug fixes! Learn how we added better JSON support, improved compression through the GCD codec, and secure authentication with just your SSH keys.","image":"/uploads/Release\_23\_9\_JSON\_and\_More\_5866ed38fc.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2023\-10\-24T17:27:17\.120Z","dateModified":"2026\-03\-03T12:30:14\.437Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 23\.9

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 24, 2023 · 15 minutes readWe are super excited to share a trove of amazing features in 23\.9

And, we already have a date for the 23\.10 release, please [register now](https://clickhouse.com/company/events/v23-10-community-release-call) to join the community call on November 2nd at 9:00 AM (PDT) / 6:00 PM (CET).

## Release Summary \#

20 new features.

19 performance optimisations.

55 bug fixes.

A small subset of highlighted features are below…But the release covers dropping tables only if empty, auto\-detection of JSON formats, support for long column names, improvements for converting numerics to datetimes, non\-constant time zones, improved logging for backups, more MYSQL compatibility, the ability to generate temporary credentials, parallel reading of files for the INFILE clause, support for Tableau online and so…much…more.

## New Contributors \#

As ever, we send a special welcome to all the new contributors in 23\.9! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.

If you see your name here, please reach out to us...but we will be finding you on twitter, etc as well.

*Alexander van Olst, Christian Clauss, CuiShuoGuo, Fern, George Gamezardashvili, Julia Kartseva, LaurieLY, Leonardo Maciel, Max Kainov, Petr Vasilev, Roman G, Tiakon, Tim Windelschmidt, Tomas Barton, Yinzheng\-Sun, bakam412, priera, seshWCS, slvrtrn, wangtao.2077, xuzifu666, yur3k, Александр Нам.*

## Type Inference for JSON \#

#### Contributed by Pavel Kruglov \#

When will JSON be production\-ready in ClickHouse?

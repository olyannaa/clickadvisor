---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Introducing
topic: introducing-loom-agent-memory-that-keeps-up-with-your-code-clickhouse
ch_version_introduced: auto
last_updated: '2026-11-16'
chunk_index: 1
total_chunks_in_doc: 10
---

# Introducing Loom: agent memory that keeps up with your code \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Introducing Loom: agent memory that keeps up with your code","description":"Loom gives coding agents shared memory and a code index grounded in the repository, so each session can build on what the last one learned.","image":"/uploads/Introducing\_Loom\_agent\_memory\_that\_keeps\_up\_with\_your\_code\_d2c2c52e54\.jpg","publisher":{"@type":"Organization","@id":"https://clickhouse.com/\#organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-11\-13T17:46:52\.524Z","dateModified":"2026\-11\-13T17:46:52\.441Z","author":\[{"@context":"https://schema.org","@type":"Person","name":"James Cunningham","url":"https://clickhouse.com/authors/jtcunning","@id":"https://clickhouse.com/authors/jtcunning\#person","image":"/uploads/IMG\_1444\_a6d52d269d.png","jobTitle":"Senior Product Manager"},{"@context":"https://schema.org","@type":"Person","name":"Lareb Zafar","url":"https://clickhouse.com/authors/lareb\-zafar","@id":"https://clickhouse.com/authors/lareb\-zafar\#person","image":"/uploads/Image\_512x512\_10\_99b8d7ab91\.png"}]}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Introducing Loom: agent memory that keeps up with your code

![img 1444](/_next/image?url=%2Fuploads%2FIMG_1444_a6d52d269d.png&w=96&q=75)![image 512x512 10](/_next/image?url=%2Fuploads%2FImage_512x512_10_99b8d7ab91.png&w=96&q=75)[James Cunningham](/authors/jtcunning) and [Lareb Zafar](/authors/lareb-zafar)Nov 13, 2026 · 16 minutes readShared agent memory, checked against your code as it changes.

[Loom](https://github.com/ClickHouse/loom) is an open\-source tool built on ClickHouse. It gives coding agents a shared code index and a place to keep what they learn, so the next session doesn't start from zero.

On our own benchmarks, introducing Loom pushed the mean answer\-quality score on ClickHouse code questions from 0\.78 up to 0\.84\.

## Why did we build Loom? \#

[GroeneAI, our autonomous contributor](https://clickhouse.com/blog/meet-groeneai-our-autonomous-contributor-to-clickhouse), has been working on ClickHouse pull requests since March: reproducing CI failures, hunting for bugs and missing tests, and babysitting its own PRs through review; and by October it had more than 3,000 merged pull requests. Those numbers hide an early weakness, though: every GroeneAI session started from almost nothing.

Starting from nothing was really becoming a burden. Each branch had a relatively normal lifecycle: a build, an overnight CI run, a reviewer who came back later in the week, a detour turning up a test turned flaky since last Tuesday. Standard practices and quirks that built up into a sore lack of being able to start at the current state of history with no memory of linear history whatsoever. Without memory, the agent rebuilds all of linear history to get to the decision it has to make at\-hand, or worse, guesses. With memory, it just simply… remembers. In one session GroeneAI remembered that a particular logical error had two throw sites and the open fix only covered one, checked the code, and pointed a maintainer at the right one.

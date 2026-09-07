---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"CPU
topic: cpu-dispatch-in-clickhouse-clickhouse
ch_version_introduced: '10.1002'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 14
---

# CPU Dispatch in ClickHouse \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"CPU Dispatch in ClickHouse","description":"Dive into the internals of how we optimize ClickHouse for specific architectures and instruction sets with our CPU\-dispatch framework ","image":"/uploads/cpu\_dispatch\_8149df289c.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2023\-10\-02T08:01:37\.023Z","dateModified":"2026\-03\-03T12:30:11\.983Z","author":{"@context":"https://schema.org","@type":"Person","name":"Maksim Kita","url":"https://clickhouse.com/authors/maksim\-kita","@id":"https://clickhouse.com/authors/maksim\-kita\#person","image":"/uploads/maksim\_642330ee4f.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# CPU Dispatch in ClickHouse

![maksim.png](/_next/image?url=%2Fuploads%2Fmaksim_642330ee4f.png&w=96&q=75)[Maksim Kita](/authors/maksim-kita)Oct 3, 2023 · 15 minutes read## Overview \#

In this post, I will describe how vectorization works, what CPU dispatch is, how to find places for CPU dispatch optimizations and how we use CPU dispatch in ClickHouse.

First, let’s describe our problem. Hardware vendors constantly add new instructions to the instruction set of modern CPUs. And we often want to use the latest instructions for optimizations, and the most important are [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) instructions. But the main issue with this is the compatibility. For example, if your program is compiled with [AVX2](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#Advanced_Vector_Extensions_2) instruction set, and your CPU supports only [SSE4\.2](https://en.wikipedia.org/wiki/SSE4#SSE4.2), then if it runs such a program, you will get an illegal instruction signal ([SIGILL](https://en.wikipedia.org/wiki/Signal_(IPC)#SIGILL)).

Also, an important thing to note is that data structures and algorithms can be specifically designed around SIMD instructions, for example, modern [integer compression codecs](https://onlinelibrary.wiley.com/doi/10.1002/spe.2203), or ported to such instructions later on, for example, [JSON parsing](https://arxiv.org/pdf/1902.08318.pdf).

To improve performance while retaining compatibility with older hardware, parts of your code can be compiled for different instruction sets, and then at runtime the program can dispatch execution to the most performant variant.

For any examples in this post I will use the clang\-15 compiler.

## Vectorization basics \#

Vectorization is an optimization where your data is processed using vector operations instead of scalar operations. Modern CPUs have specific instructions that allow you to process your data in vectors using [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) instructions. Such optimizations can be performed manually, or compilers can perform [automatic vectorization](https://en.wikipedia.org/wiki/Automatic_vectorization).

Let’s consider such code example:

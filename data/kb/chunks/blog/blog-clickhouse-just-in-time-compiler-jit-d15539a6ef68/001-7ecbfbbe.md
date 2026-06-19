---
source: blog
url: https://maksimkita.com/
topic: jit-in-clickhouse
ch_version_introduced: '10.3'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 20
---

# JIT in ClickHouse

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# JIT in ClickHouse

![maksim.png](/_next/image?url=%2Fuploads%2Fmaksim_642330ee4f.png&w=96&q=75)[Maksim Kita](/authors/maksim-kita)Nov 23, 2022 · 30 minutes read![just_in_time.jpg](/uploads/large_just_in_time_d9c935fa41.jpg)
*This blog post was originally posted on [Maksim's personal blog](https://maksimkita.com/), which we recommend for those interested in the low\-level details of Performance Engineering, Query Analysis and Planning, JIT Compilation, System Programming and Distributed Systems.*

## Overview [\#](/blog/clickhouse-just-in-time-compiler-jit#overview)

In this post, I will describe what JIT compilation is, how LLVM infrastructure can be used for JIT compilation, and how JIT compilation works in ClickHouse.

Most of this post is a summary of talks that I give on C\+\+ Russia 2021 “JIT in ClickHouse”, HighLoad 2022 “JIT compilation of queries in ClickHouse”, C\+\+ Russia 2022 “ClickHouse performance optimization practices”, and there are also additional examples and things that I have not covered in these talks.

## JIT basics [\#](/blog/clickhouse-just-in-time-compiler-jit#jit-basics)

First, let’s start with what JIT compilation is. [JIT](https://en.wikipedia.org/wiki/Just-in-time_compilation) \- Just\-in\-time compilation. The main idea is to generate machine code and execute it in runtime. Examples of such systems are JVM Hotspot and V8\. Most database systems support JIT compilation.

To better understand how JIT compilation works, we can start from the bottom up \- make JIT compilation with our bare hands.

Consider such code example:

```
int64_t sum(int64_t value_1, int64_t value_2)
{
    return value_1 + value_2;
}

int main(int argc, char ** argv)
{
    printf("Sum %ld\n", sum(1, 2));
    return 0;
}

```

We have a `sum` function that takes two integer values, computes their sum, and returns it. In the `main` function, we print the result of the `sum` function execution with constants 1 and 2\.

If we compile this example with gcc and explore binary using [objdump](https://en.wikipedia.org/wiki/Objdump), we can extract `sum` function assembly.

```
g++ --version
g++ (Ubuntu 10.3.0-1ubuntu1~20.04) 10.3.0

```

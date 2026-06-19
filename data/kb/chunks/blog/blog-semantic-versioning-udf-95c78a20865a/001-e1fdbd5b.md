---
source: blog
url: https://embrace.io/
topic: semantic-versioning-udf-in-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 5
---

# Semantic Versioning UDF in ClickHouse

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Semantic Versioning UDF in ClickHouse

![](/_next/image?url=%2Fuploads%2FJuan_Carrillo_profile_1f4aa99e38.jpeg&w=96&q=75)Juan S. CarrilloOct 9, 2024 · 7 minutes readI work at [Embrace](https://embrace.io/), where we build the only user\-focused mobile app observability solution based on OpenTelemetry (OTel). We use ClickHouse to power our time series analytics products.

One of the most important sorting categories for Embrace users is app version. App versions often use [semantic versioning](https://semver.org/), where the version will be described in the format `<MAJOR>.<MINOR>.<PATCH>`. You increment them according to the following rules:

1. MAJOR version when you make incompatible API changes
2. MINOR version when you add functionality in a backward compatible manner
3. PATCH version when you make backward compatible bug fixes

We want to be able to sort app versions such that 2\.1\.0, 2\.1\.2, and 2\.1\.10 would appear in that order, rather than 2\.1\.0, 2\.1\.10, and 2\.1\.2, which happens when you sort in lexicographic order.

ClickHouse doesn’t provide a way to sort for semantic versioning right out of the box. However, you can use User\-Defined Functions (UDFs), which were introduced in ClickHouse [v21\.10](https://clickhouse.com/blog/click-house-v2110-released), to solve this.

The final UDF we use can be found below. Please read on if you want to see how we built it, and the improvements we made in our querying and in our reasoning.

```
CREATE FUNCTION sortableSemVer AS version -> 
  arrayMap(
    x -> toUInt32OrZero(x), 
    splitByChar('.', extract(version, '(\\d+(\\.\\d+)+)'))
  )

```

## Versions as ints in strings [\#](/blog/semantic-versioning-udf#versions-as-ints-in-strings)

Versions are most commonly stored as strings in databases. As many of you may know, sorting version strings using lexicographical order will not work as expected.

```
SELECT *
FROM
(
    SELECT ['1.0', '2.0', '3.0.0', '10.0'] AS versions
)
ARRAY JOIN versions
ORDER BY versions DESC

┌─versions─┐
│ 3.0.0    │
│ 2.0      │
│ 10.0     │ << ???
│ 1.0      │
└──────────┘

```

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"chDB
topic: chdb-kernel-upgrade-journey-upgrading-clickhouse-to-v25-8-2-29-clickhouse
ch_version_introduced: '2.0'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 13
---

# chDB Kernel Upgrade Journey: Upgrading ClickHouse to v25\.8\.2\.29 \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"chDB Kernel Upgrade Journey: Upgrading ClickHouse to v25\.8\.2\.29 ","description":"chDB recently upgraded the ClickHouse kernel from v25\.5 to v25\.8\.2\.29\. This blog post goes through that journey.","image":"/uploads/Image\_from\_Git\_Hub\_2\_8a0578365a.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2025\-11\-14T11:51:54\.007Z","dateModified":"2026\-03\-03T12:38:53\.266Z","author":{"@context":"https://schema.org","@type":"Person","name":"Victor Gao"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# chDB Kernel Upgrade Journey: Upgrading ClickHouse to v25\.8\.2\.29

![image 512x512 5](/_next/image?url=%2Fuploads%2FImage_512x512_5_11da9e142c.jpeg&w=96&q=75)Victor GaoNov 19, 2025 · 19 minutes read[chDB](https://github.com/chdb-io/chdb) is an embedded OLAP SQL engine that packages ClickHouse's powerful analytical capabilities as a Python module, allowing developers to enjoy high\-performance data analysis in Python without installing or running a ClickHouse server. Recently, we completed a major kernel upgrade ([PR \#383](https://github.com/chdb-io/chdb/pull/383)), upgrading the ClickHouse kernel from v25\.5 to v25\.8\.2\.29\. This upgrade not only brought new features and performance improvements but also exposed a series of technical challenges. This article will detail the technical aspects and solutions from this upgrade process.

## 1\. chDB architecture and code structure \#

### 1\.1 Overall architecture \#

The core design philosophy of chDB is to embed ClickHouse into the Python process, achieving a true in\-process query engine. Its architecture can be summarized in the following layers:

![Image 511556138 2776x2790.jpg](/_next/image?url=%2Fuploads%2FImage_511556138_2776x2790_1bbb194323.jpg&w=2048&q=75)

Unlike the traditional client/server architecture, chDB has no independent server process:

- **Zero\-copy data passing**: Uses Python `memoryview` and C\+\+ `WriteBufferFromVector` for zero\-copy data transfer
- **Embedded design**: ClickHouse engine runs directly in the Python process, avoiding inter\-process communication overhead
- **Multi\-format support**: Native support for 60\+ formats including Parquet, CSV, JSON, Arrow, ORC

### 1\.2 Code structure \#

chDB's code structure is inherited from ClickHouse but with extensive customizations:

```
1chdb/
2├── chdb/                    # Python package
3│   ├── __init__.py          # Main query interface
4│   ├── session/             # Session management
5│   ├── dbapi/               # DB-API 2.0 implementation
6│   └── udf/                 # User-defined functions
7├── programs/local/          # Local query engine
8│   ├── LocalChdb.cpp        # chDB main entry
9│   ├── PythonSource.cpp     # Python Table Engine
10│   └── PandasDataFrame.cpp  # Pandas integration
11├── src/                     # ClickHouse core source
12└── contrib/                 # Third-party dependencies
```
Copy command
Core query flow:

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Loading
topic: loading-parquet-data-into-mysql-with-clickhouse-clickhouse
ch_version_introduced: '127.0'
last_updated: '2026-10-12'
chunk_index: 1
total_chunks_in_doc: 5
---

# Loading Parquet data into MySQL with ClickHouse \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Loading Parquet data into MySQL with ClickHouse","description":"Use ClickHouse to load Parquet files into MySQL, explore remote data, and run MySQL queries with table functions and named collections.","image":"/uploads/Loading\_Parquet\_Data\_into\_My\_SQL\_9371e998c0\.jpg","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-09\-11T13:17:45\.862Z","dateModified":"2026\-09\-11T13:17:45\.785Z","author":{"@context":"https://schema.org","@type":"Person","name":"Mark Needham","url":"https://clickhouse.com/authors/mark\-needham","@id":"https://clickhouse.com/authors/mark\-needham\#person","image":"/uploads/mark\_needham\_a17c08008e.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Loading Parquet data into MySQL with ClickHouse

![mark needham](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Sep 10, 2026 · 7 minutes readA couple of weeks ago, I was working on a video for the [MySQL CDC connector for ClickPipes](https://clickhouse.com/blog/mysql-cdc-connector-for-clickpipes-is-now-generally-available) and I needed to get some data from Parquet files into MySQL. There isn't a native way to do this, so I decided to use [clickhouse\-local](https://clickhouse.com/docs/concepts/features/tools-and-utilities/clickhouse-local), my favorite tool for doing this type of adhoc data work.

## Setting up MySQL \#

I used AWS RDS for MySQL in the video, but to make it easier to reproduce, we'll use MySQL running on my machine for this blog post. We can launch MySQL by running the following:

```
1docker run --name parquet-mysql \
2    -p 127.0.0.1:3306:3306 \
3    -e MYSQL_ROOT_PASSWORD=local-root-password \
4    -e MYSQL_DATABASE=stackoverflow \
5    -e MYSQL_USER=admin \
6    -e MYSQL_PASSWORD=local-demo-password \
7    -v parquet-mysql-data:/var/lib/mysql \
8    mysql:8.4
```
Copy command
## Setting up ClickHouse \#

We'll run ClickHouse via its binary, which we can download like this:

```
1curl https://clickhouse.com | sh
```
Copy command
We'll then launch it:

```
1./clickhouse -mn \
2--config-file ch-config.yaml \
3--param_mysql_password "local-demo-password" \
4--param_mysql_host "127.0.0.1:3306" \
5--output-format Pretty
```
Copy command
Tip

We're passing in the MySQL host and password in plain text because it's running on our machine. For a production system, we'd have those values stored in environment variables.

The contents of `ch-config.yaml` are shown below:

```
1echo: 0
2users_config: ch-users.yaml
3named_collections:
4  mysql_demo:
5    host: '127.0.0.01'
6    port: 3306
7    user: 'admin'
8    password: 'local-demo-password'
9    database: 'stackoverflow'
```
Copy command
`ch-users.yaml` contains config for the default user. The named collection `mysql_demo` contains our MySQL credentials that we'll use later in the post.

## Exploring StackOverflow dataset \#

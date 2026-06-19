---
source: blog
url: https://clickhouse.com/blog/getting-data-into-clickhouse-part-2-json
topic: getting-data-into-clickhouse-part-1
ch_version_introduced: '203.682'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 9
---

https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.csv.gz ``` At 4\.6GB, and 28m rows, this compressed file should take 5\-10 minutes to download. ### Sampling [\#](/blog/getting-data-into-clickhouse-part-1#sampling) [clickhouse\-local](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local/) allows users to perform fast processing on local files without having to deploy and configure the ClickHouse server.

Before storing any data in ClickHouse, let's sample the file using clickhouse\-local. From the clickhouse\-local console:

```
clickhouse-local

```

```
SELECT *
FROM file('hacknernews.csv.gz', CSVWithNames)
LIMIT 2
SETTINGS input_format_try_infer_datetimes = 0
FORMAT Vertical


Row 1:
──────
id:          344065
deleted:     0
type:        comment
by:          callmeed
time:        2008-10-26 05:06:58
text:        What kind of reports do you need?<p>ActiveMerchant just connects your app to a gateway for cc approval and processing.<p>Braintree has very nice reports on transactions and it's very easy to refund a payment.<p>Beyond that, you are dealing with Rails after all–it's pretty easy to scaffold out some reports from your subscriber base.
dead:        0
parent:      344038
poll:        0
kids:        []
url:
score:       0
title:
parts:       []
descendants: 0

Row 2:
──────
id:          344066
deleted:     0
type:        story
by:          acangiano
time:        2008-10-26 05:07:59
text:
dead:        0
parent:      0
poll:        0
kids:        [344111,344202,344329,344606]
url:         http://antoniocangiano.com/2008/10/26/what-arc-should-learn-from-ruby/
score:       33
title:       What Arc should learn from Ruby
parts:       []
descendants: 10

```

There are a lot of subtle capabilities in this command. The [file](https://clickhouse.com/docs/en/sql-reference/functions/files/#file) operator allows us to read the file from a local disk, specifying only the format “CSVWithNames”. Most importantly, the schema is automatically inferred for us from the file contents. Note also how clickhouse\-local is able to read the compressed file, inferring the gzip format from the extension. We format Verticially for the purposes of rendering.

As well as inferring the structure, schema inference determines a type for each column.

An astute reader may have noticed that we used the setting `input_format_try_infer_datetimes=0`. This setting disables date parsing during schema inference as, at the time of writing (22\.8\), the datetimes in this specific CSV file cannot be parsed automatically. This has been addressed in later versions.

### Loading the Data [\#](/blog/getting-data-into-clickhouse-part-1#loading-the-data)

Our simplest and most powerful tool for data loading is the [clickhouse\-client](https://clickhouse.com/docs/en/interfaces/cli/#clickhouse-client): a feature\-rich native command\-line client. To load data, we can again exploit schema inference, relying on ClickHouse to determine the types of the columns.

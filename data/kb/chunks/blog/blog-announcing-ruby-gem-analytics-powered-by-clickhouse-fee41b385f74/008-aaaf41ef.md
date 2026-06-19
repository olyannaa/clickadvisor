---
source: blog
url: https://clickgems.clickhouse.com/
topic: announcing-ruby-gem-analytics-powered-by-clickhouse-and-ruby-central
ch_version_introduced: '252.989'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 15
---

impractical: they receive one file per Fastly region per hour, and each arrival triggers a Lambda function that processes the file independently. These Lambda invocations happen concurrently, and there's no reliable or desirable way to serialize their delivery.

Given the possible out\-of\-order delivery, we thus use unordered mode with S3Queue.
- We create a new S3Queue and materialized view each day, also dropping the queue and view from the 2 days ago. This ensures each queue doesn't need to track an excessive number of files (less than a 1000\). Each day's queue also thus has a 48 hour gratuitous period, in case files are delivered late.
- We adjust the queue defaults, increasing the minimum and maximum polling time as well as increasing the number of tracked files to 2000\.
- Note the pattern `**/*.json.gz` provides recursive processing of files.
- Our [sql.clickhouse.com](http://sql.clickhouse.com) environment into which we are loading this data has three nodes, each with 60 vCPUs. The setting `s3queue_processing_threads_num` assigns the number of threads for file processing per server. In addition, the ordered mode also introduces the setting `s3queue_buckets`. [As recommended](https://clickhouse.com/docs/en/engines/table-engines/integrations/s3queue#ordered-mode), we set this to equal a multiplication of the number of replicas (3\) by the number of processing threads (10\).

With this in place, the data started to flow in. An example query exploring downloads per hour for the [bundler gem](https://rubygems.org/gems/bundler):

```

```
SELECT
	toStartOfHour(timestamp) AS hour,
	count()
FROM rubygems.downloads
WHERE gem = 'bundler' AND timestamp > today() - INTERVAL 1 WEEK
GROUP BY hour
ORDER BY hour ASC
```

```

With all data loaded from 2017, this dataset totals around 180 billion rows, compressing from around 9\.5 TB of Gzipped JSON (160 TB uncompressed) to less than 5 TB in ClickHouse:

```

```
SELECT
   `table`,
   formatReadableSize(sum(data_compressed_bytes)) AS total_size
FROM system.columns
WHERE (database = 'rubygems') AND (`table` = 'downloads')
GROUP BY `table`
ORDER BY sum(data_compressed_bytes) DESC
```

```

### Daily aggregate downloads [\#](/blog/announcing-ruby-gem-analytics-powered-by-clickhouse#daily-aggregate-downloads-1)

Our second dataset is hosted in github and updated periodically (approximately weekly). 

To backfill this data, we simply cloned the repo and ran the following command, using clickhouse\-local to parse the files and insert them into our Cloud instance:

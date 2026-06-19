---
source: kb.altinity.com
url: https://clickhouse.com/blog/a\-new\-powerful\-json\-data\-type\-for\-clickhouse](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse
topic: best-schema-for-storing-many-metrics-registered-from-the-single-source-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 3
---

of value’ somehow (NULLs or default values) - to read full row \- you need to read a lot of column files. ### 2b Using arrays / Nested / Map i.e.: timestamp, sourceid, array\_of\_metric\_names, array\_of\_metric\_values Pros and cons:

- Pros
	- easy to extend, you can have very dynamic / huge number of metrics.
	- you can use Array(LowCardinality(String)) for storing metric names efficiently
	- good for sparse recording (each time point can have only 1% of all the possible metrics)
- Cons
	- you need to extract all metrics for row to reach a single metric
	- not very handy / complicated non\-standard syntax
	- different metrics values stored in single array (bad compression)
	- to use values of different datatype you need to cast everything to string or introduce few arrays for values of different types.

### 2c Using JSON

i.e.: timestamp, sourceid, metrics\_data\_json

Pros and cons:

- Pros
	- easy to extend, you can have very dynamic / huge number of metrics.
	- the only option to store hierarchical / complicated data structures, also with arrays etc. inside.
	- good for sparse recording (each time point can have only 1% of all the possible metrics)
	- ClickHouse® has efficient API to work with JSON
	- nice if your data originally came in JSON (don’t need to reformat)
- Cons
	- uses storage non efficiently
	- different metrics values stored in single array (bad compression)
	- you need to extract whole JSON field to reach single metric
	- slower than arrays

### 2d Using querystring\-format URLs

i.e.: timestamp, sourceid, metrics\_querystring
Same pros/cons as raw JSON, but usually bit more compact than JSON

Pros and cons:

- Pros
	- ClickHouse has efficient API to work with URLs (extractURLParameter etc)
	- can have sense if you data came in such format (i.e. you can store GET / POST request data directly w/o reprocessing)
- Cons
	- slower than arrays

### 2e Several ‘baskets’ of arrays

i.e.: timestamp, sourceid, metric\_names\_basket1, metric\_values\_basket1, …, metric\_names\_basketN, metric\_values\_basketN
The same as 2b, but there are several key\-value arrays (‘basket’), and metric go to one particular basket depending on metric name (and optionally by metric type)

Pros and cons:

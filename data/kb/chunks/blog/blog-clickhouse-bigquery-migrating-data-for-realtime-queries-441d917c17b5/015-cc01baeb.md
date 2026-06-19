---
source: blog
url: https://clickhouse.com/blog/hifis-migration-from-bigquery-to-clickhouse
topic: clickhouse-vs-bigquery-using-clickhouse-to-serve-real-time-queries-on-top-of-bigquery-data
ch_version_introduced: '22.712'
last_updated: '2026-06-12'
chunk_index: 15
total_chunks_in_doc: 20
---

example [here](https://github.com/ClickHouse/examples/blob/main/ethereum/batch/beam_dataflow/sync_clickhouse.py). ![clickhouse_data_flow.png](/uploads/clickhouse_data_flow_6052a93ed8.png) Executing this pipeline to migrate the blocks table would require the python code to be run as shown below. This assumes you have configured your machine to [use Google Dataflow and have the required permissions](https://cloud.google.com/dataflow/docs/quickstarts/create-pipeline-python):

```
python -m sync_clickhouse --target_table ethereum.blocks --clickhouse_host <clickhouse_host> --clickhouse_password <password> --region us-central1 --runner DataflowRunner --project <GCE project> --temp_location gs://<bucket> --requirements_file requirements.txt

```

Note the need to also provide the dependencies via a [requirements.txt](https://github.com/ClickHouse/examples/blob/main/ethereum/batch/beam_dataflow/requirements.txt) and a GCS bucket in which data can be cached, as the BigQuery connector works by exporting data to a bucket and using this as an intermediary store \- a bit like our earlier approach. The GCE console provides a nice visualization of the process.

![dataflow_execution.png](/uploads/dataflow_execution_abb63d43da.png)
The above approach has the following limitations, and we leave these improvements as an exercise for the reader:

- Ideal solution would utilize a streaming pipeline that runs forever as more data is added to the source. However, a streaming pipeline requires an [unbounded source](https://beam.apache.org/documentation/basics/#pcollection), and since the BigQuery source is bounded, it cannot be used in streaming pipelines. Instead, we use a batch pipeline runs until completion based on a snapshot and then stops. The easiest solution here is to have the pipeline identify the current max timestamp in ClickHouse on start, and use this as filter criteria to BigQuery. The pipeline can then easily be scheduled to run using [Cloud Scheduler](https://cloud.google.com/community/tutorials/schedule-dataflow-jobs-with-cloud-scheduler).
- Our ClickHouse connector has to structure the rows into a 2\-dimensional array for use with the ClickHouse python client. This work could also be done as a parallelized ParDo.
- We batch using the [BatchElements transform](https://beam.apache.org/releases/pydoc/2.22.0/apache_beam.transforms.util.html#apache_beam.transforms.util.BatchElements) with a fixed size of 10000k. Other datasets may need to adapt this. Note that this transformation can also do adaptive batching.
- We provide dependencies through a requirements.txt file. This is the simplest means to get started, but isn’t recommended in [production settings](https://medium.com/google-cloud/installing-python-dependencies-in-dataflow-fe1c6cf57784).

## Note on Continuous Data Loading [\#](/blog/clickhouse-bigquery-migrating-data-for-realtime-queries#note-on-continuous-data-loading)

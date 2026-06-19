---
source: blog
url: https://clickhouse.com/blog/clickhouse-open-ai-user-defined-functions-udfs
topic: executable-udfs-are-now-in-public-beta-on-clickhouse-cloud
ch_version_introduced: '2.4'
last_updated: '2026-06-12'
chunk_index: 11
total_chunks_in_doc: 12
---

somewhere. The data lives somewhere else. The glue between them is its own system. The setup in this repo flattens that. There's a ClickHouse Cloud cluster, a 2MB Python file, and one DDL statement that binds them together.

Every piece of UI logic in the webapp is a SQL query. Anomaly detection
is the only ML in the system, and even that's not "ML in the webapp",
it's a column in a table. The "how anomalous is this symbol's last
hour" calculation, the "find me similar trades by cosine distance"
query, the per\-symbol p95 baseline, the materialized views that keep it
all fresh: standard SQL features, running against standard ClickHouse
tables.

Executable UDFs in Cloud don't add new abstractions on top of
ClickHouse. They give you a way to make Python part of your SQL.

## Reproduce it [\#](/blog/executable-udfs-clickhouse-cloud-beta#reproduce-it)

The full project is at [https://github.com/clickhouse/stock\-anomaly\-udf](https://github.com/clickhouse/stock-anomaly-udf).

```
stock-anomaly-udf/
├── notebook/   # Train the autoencoder, export weights, package the UDF zip
├── udf/        # The deployable bundle: main.py, model weights, deployment notes
├── sql/        # Source schema, the auto-embed MV, two refreshable baseline MVs
└── web/        # Next.js demo app

```

### Quickstart [\#](/blog/executable-udfs-clickhouse-cloud-beta#quickstart)

1. **Get the UDF onto your cluster.**

	- Zip the contents of `udf/embed_trade/`:
	

	```
	cd udf/embed_trade && zip embed_trade.zip main.py requirements.txt *.pt
	
	```
	- Upload via the Cloud UDF deployment UI. Configure per
	[`udf/cloud-deployment.md`](https://github.com/ClickHouse/stock-anomaly-udf/blob/main/udf/cloud-deployment.md).
2. **Run the SQL files in order:**

```
:run sql/01_source_schema.sql
:run sql/02_embeddings_mv.sql
:run sql/03_score_baselines.sql
:run sql/04_dim_baselines.sql

```
3. **Backfill historical data** (optional). Bulk INSERT into
`trades_embeddings` using the same SELECT pattern as the MV, scoped to
any time range. The MV in step 2 will catch every subsequent INSERT
into `default.trades` automatically.
4. **Start the webapp:**

```
cd web
cp .env.example .env.local   # fill in CH_HOST/PORT/USER/PASS/DB
npm install
npm run dev

```

Open <http://localhost:3000>.

The notebook in `notebook/` walks through training your own autoencoder
end to end. It streams training data from `default.trades` into Parquet
chunks, fits a `StandardScaler` incrementally, trains with early
stopping, and zips the artifacts into a deployable bundle.

## Try executable UDFs [\#](/blog/executable-udfs-clickhouse-cloud-beta#try-executable-udfs)

Public beta is live in ClickHouse Cloud today. Drop us a note if you put
something interesting together with it!

### Get started today

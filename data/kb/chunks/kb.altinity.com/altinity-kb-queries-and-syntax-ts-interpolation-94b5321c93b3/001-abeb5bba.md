---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/a51da1141f03e9f209a61ea1f41e1f0acf43f122
topic: time-series-alignment-with-interpolation-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 2
---

# Time\-series alignment with interpolation \| Altinity® Knowledge Base for ClickHouse®

1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. Time\-series alignment with interpolation
# Time\-series alignment with interpolation

This article demonstrates how to perform time\-series data alignment with interpolation using window functions in ClickHouse. The goal is to align two different time\-series (A and B) on the same timestamp axis and fill the missing values using linear interpolation.

Step\-by\-Step Implementation
We begin by creating a table with test data that simulates two time\-series (A and B) with randomly distributed timestamps and values. Then, we apply interpolation to fill missing values for each time\-series based on the surrounding data points.

#### 1\. Drop Existing Table (if it exists)

```
DROP TABLE test_ts_interpolation;

```
This ensures that any previous versions of the table are removed.

#### 2\. Generate Test Data

In this step, we generate random time\-series data with timestamps and values for series A and B. The values are calculated differently for each series:

```
CREATE TABLE test_ts_interpolation
ENGINE = Log AS
SELECT
    ((number * 100) + 50) - (rand() % 100) AS timestamp, -- random timestamp generation
    transform(rand() % 2, [0, 1], ['A', 'B'], '') AS ts, -- randomly assign series 'A' or 'B'
    if(ts = 'A', timestamp * 10, timestamp * 100) AS value -- different value generation for each series
FROM numbers(1000000);

```
Here, the timestamp is generated randomly and assigned to either series A or B using the transform() function. The value is calculated based on the series type (A or B), with different multipliers for each.

#### 3\. Preview the Generated Data

After generating the data, you can inspect it by running a simple SELECT query:

```
SELECT * FROM test_ts_interpolation;

```
This will show the randomly generated timestamps, series (A or B), and their corresponding values.

#### 4\. Perform Interpolation with Window Functions

To align the time\-series and interpolate missing values, we use window functions in the following query:

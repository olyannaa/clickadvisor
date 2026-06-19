---
source: kb.altinity.com
url: http://s3.us-east-1.amazonaws.com/BUCKET_NAME/test_s3_disk/</endpoint>
topic: setup-maintenance-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '98.091'
last_updated: '2026-06-12'
chunk_index: 43
total_chunks_in_doc: 186
---

and buffers are allocated for each column and each part. > - *Vertical merge* processes columns in batches — first merging only columns from `ORDER BY`, then the rest one by one. This approach **significantly reduces memory usage**.

The most memory\-intensive scenario is a **horizontal merge of wide parts** in a table with a large number of columns.

---

## Demonstrating the Problem

The issue can be reproduced easily by adjusting a few settings:

```
ALTER TABLE system.metric_log MODIFY SETTING min_bytes_for_wide_part = 100;
OPTIMIZE TABLE system.metric_log FINAL;

```
Example log output:

```
[c9d66aa9f9d1] 2025.11.10 10:04:59.091067 [97] <Debug> MemoryTracker: Background process (mutate/merge) peak memory usage: 6.00 GiB.

```
**The merge consumed 6 GB of memory** — far too much for this table.

---

## Vertical Merges Are Not Affected

If you explicitly force vertical merges, memory consumption normalizes, although the process becomes slightly slower:

```
ALTER TABLE system.metric_log MODIFY SETTING 
    min_bytes_for_wide_part = 100,
    vertical_merge_algorithm_min_rows_to_activate = 1;

OPTIMIZE TABLE system.metric_log FINAL;

```
Example log output:

```
[c9d66aa9f9d1] 2025.11.10 10:06:14.575832 [97] <Debug> MemoryTracker: Background process (mutate/merge) peak memory usage: 13.98 MiB.

```
Now memory usage **drops from 6 GB to only 14 MB**.

---

## Root Cause

The problem stems from the fact that:

- the threshold for enabling *wide* parts is configured in **bytes** (`min_bytes_for_wide_part`);
- while the threshold for enabling *vertical merges* is configured in **rows** (`vertical_merge_algorithm_min_rows_to_activate`).

When a table contains very **wide rows** (many lightweight columns), this mismatch causes wide parts to appear too early, while vertical merges are triggered much later.

---

## Default Settings

| Parameter | Value |
| --- | --- |
| `vertical_merge_algorithm_min_rows_to_activate` | 131072 |
| `vertical_merge_algorithm_min_bytes_to_activate` | 0 |
| `min_bytes_for_wide_part` | 10485760 (10 MB) |
| `min_rows_for_wide_part` | 0 |

The average row size in `metric_log` is approximately **2\.8 KB**, meaning wide parts are created after roughly:

```
10485760 / 2800 ≈ 3744 rows

```
Meanwhile, the vertical merge algorithm activates only after **131 072 rows** — much later.

---

## Possible Solutions

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-26-8-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-10-26'
chunk_index: 10
total_chunks_in_doc: 19
---

an index using the `fine_grained` parameter. Four strings are inserted into both tables, either containing the word `大学` ("university") standalone (row 1\), embedded inside a longer compound word (rows 2 and 3\), or not at all (row 4\).

```
1CREATE TABLE table_coarse
2(
3    key UInt64,
4    str String,
5    INDEX text_idx str TYPE text(tokenizer = chinese) -- default: coarse_grained
6)
7ENGINE = MergeTree ORDER BY key;
8
9CREATE TABLE table_fine
10(
11    key UInt64,
12    str String,
13    INDEX text_idx str TYPE text(tokenizer = chinese('fine_grained'))
14)
15ENGINE = MergeTree ORDER BY key;
16
17INSERT INTO table_coarse VALUES
18    (1, '他考上了大学，很开心'), -- standalone 大学
19    (2, '北京邮电大学的通信工程专业很强'), -- compound 北京邮电大学
20    (3, '我毕业于北京大学计算机系'), -- compound 北京大学
21    (4, '今天天气不错，适合散步'); -- no mention
22
23INSERT INTO table_fine SELECT * FROM table_coarse;
```
Copy command
The queries below use the `hasAllTokens` function to search for `大学` ("university"), first on the table using the default `coarse_grained` parameter in its `chinese` index, then for the second table using the `fine_grained` parameter.

For the first table, only `他考上了大学，很开心` ("He got into university and was very happy."), the sentence with a standalone mention of `大学`, is returned. For the second table, both the sentence with the standalone mention of `大学` and the sentences with the compound mentions are returned:

```
1SELECT
2    key,
3    str
4FROM table_coarse
5WHERE hasAllTokens(str, '大学')
6ORDER BY key ASC;
```
Copy command
Query ID: `7e348059-9cd1-4f72-8026-8d76266050e4`

| key | str |
| --- | --- |
| 1 | 他考上了大学，很开心 |


1 row in set. Elapsed: 0\.002 sec.

```
1SELECT
2    key,
3    str
4FROM table_fine
5WHERE hasAllTokens(str, '大学')
6ORDER BY key ASC;
```
Copy command
Query ID: `4da23c89-8a10-4099-9637-bd2a14f6aa1b`

| key | str |
| --- | --- |
| 1 | 他考上了大学，很开心 |
| 2 | 北京邮电大学的通信工程专业很强 |
| 3 | 我毕业于北京大学计算机系 |


3 rows in set. Elapsed: 0\.002 sec.

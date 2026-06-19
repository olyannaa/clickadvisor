---
source: kb.altinity.com
url: http://altinity.com/
topic: altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 430
total_chunks_in_doc: 478
---

TABLE statements is not always useful, as they expand to create table DDL, and changing them is inconvenient. **Using a Null Table, Materialized View, and** rowNumberInAllBlocks A more efficient approach involves using a Null table and materialized views.

```
create table XX 
(
  id Int64,
  data String
) engine=MergeTree order by id;

create table Null (data String) engine=Null;
create materialized view _XX to XX as
select toSnowflake(now(),rowNumberInAllBlocks()) is id, data
from Null;

```
### Converting from UUID to SnowFlakeID for subsequent events

Consider that your event stream only has a UUID column identifying a particular user. Registration time that can be used as a base for SnowFlakeID is presented only in the first ‘register’ event, but not in subsequent events. It’s easy to generate SnowFlakeID for the register event, but next, we need to get it from some other table without disturbing the ingestion process too much. Using Hash JOINs in Materialized Views is not recommended, so we need some “nested loop join” to get data fast. In Clickhouse, the “nested loop join” is still not supported, but Direct Dictionary can work around it.

```
CREATE TABLE UUID2ID_store (user_id UUID, id UInt64) 
ENGINE = MergeTree() -- EmbeddedRocksDB can be used instead
ORDER BY user_id
settings index_granularity=256;

CREATE DICTIONARY UUID2ID_dict (user_id UUID, id UInt64) 
PRIMARY KEY user_id
LAYOUT ( DIRECT ())
SOURCE(CLICKHOUSE(TABLE 'UUID2ID_store'));

CREATE OR REPLACE FUNCTION UUID2ID AS (uuid) -> dictGet('UUID2ID_dict',id,uuid);

CREATE MATERIALIZED VIEW _toUUID_store TO UUID2ID_store AS
select user_id, toSnowflake64(event_time, cityHash64(user_id)) as id
from Actions;

```
**Conclusion**

Snowflake IDs provide an efficient mechanism for generating unique, monotonic primary keys, which are essential for optimizing query performance in data warehousing environments. By combining timestamps and unique identifiers, snowflake IDs facilitate faster row filtering and ensure stable, surrogate key generation. Implementing these IDs using SQL functions and materialized views ensures that your data warehouse remains performant and scalable.

# 7\.11 \- Two columns indexing

How to create ORDER BY suitable for filtering over two different columns in two different queriesSuppose we have telecom CDR data in which A party calls B party. Each data row consists of A party details: event\_timestamp, A MSISDN , A IMEI, A IMSI , A start location, A end location , B MSISDN, B IMEI, B IMSI , B start location, B end location, and some other metadata.

---
source: blog
url: 'https://schema.org","@type":"BlogPosting","headline":"Streamkap:'
topic: streamkap-an-out-of-the-box-cdc-solution-for-clickhouse-clickhouse
ch_version_introduced: '37.368'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 12
---

ClickHouse, with the query performance benefiting from moving data transformation to insert time. Below, we present some common transformations performed by Streamkap. #### Fix inconsistencies in semi\-structured data \# Consider the fixing of an inconsistent semi\-structured date field:

```
1"someDateField": {"$date": "2023-08-04T09:12:20.29Z"}
2"someDateField": "2023-08-07T08:14:57.817325+00:00"
3"someDateField": {"$date": {"$numberLong": 1702853448000}}
```
Copy command
Using Streamkap transforms, all records can be converted to a common format for ingestion into Clickhouse [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) column:

```
1"someDateField": "yyyy-MM-dd HH:mm:ss.SSS"
```
Copy command
#### Split large semi\-structured JSON documents \#

With document databases, child entities can be modelled as sub\-arrays nested inside the parent entity document:

```
1{
2    "key": "abc1234",
3    "array": [
4        {
5            "id": "11111",
6            "someField": "aa-11"
7        },
8        {
9            "id": "22222",
10            "someField": "bb-22"
11        }
12    ]
13}
```
Copy command
In ClickHouse it can make sense to represent these child entities as separate rows. Using Streamkap transforms, the child entity records can be split into individual records:

```
1{
2    "id": "11111",
3    "parentKey": "abc1234",
4    "someField": "aa-11"
5}
6
7{
8    "id": "22222",
9    "parentKey": "abc1234",
10    "someField": "bb-22"
11}
```
Copy command
### Schema evolution \#

Schema evolution or drift handling is the process of making changes to the destination tables to reflect upstream changes.

The Streamkap connector automatically handles schema drift in the following scenarios.

- **Additional Columns:** An additional field will be detected, and a new column in the table will be created to receive the new data.
- **Removal of Columns:** This column will now be ignored, and no further action will be taken.
- **Changing Column Type**: An additional column is created in the table using a suffix to represent the new type. e.g. `ColumnName_type`

Additional tables can be added to the pipeline at any stage. We show some examples of this schema evolution below.

#### Add Column \#

Consider the following input record before schema evolution:

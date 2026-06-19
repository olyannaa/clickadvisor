# Two columns indexing \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. Two columns indexing
# Two columns indexing

How to create ORDER BY suitable for filtering over two different columns in two different queriesSuppose we have telecom CDR data in which A party calls B party. Each data row consists of A party details: event\_timestamp, A MSISDN , A IMEI, A IMSI , A start location, A end location , B MSISDN, B IMEI, B IMSI , B start location, B end location, and some other metadata.

Searches will use one of the A or B fields, for example, A IMSI, within the start and end time window.

A msisdn, A imsi, A imei values are tightly coupled as users rarely change their phones.

The queries will be:


```
select * from X where A = '0123456789' and ts between ...;
select * from X where B = '0123456789' and ts between ...;

```
and both A \& B are high\-cardinality values

ClickHouse® primary skip index (ORDER BY/PRIMARY KEY) works great when you always include leading ORDER BY columns in the WHERE filter. There are exceptions for low\-cardinality columns and high\-correlated values, but here is another case. A \& B both have high cardinality, and it seems that their correlation is at a medium level.

Various solutions exist, and their effectiveness largely depends on the correlation of different column data. Testing all solutions on actual data is necessary to select the best one.

### ORDER BY \+ additional Skip Index


```
create table X (
    A UInt32,
    B UInt32,
    ts DateTime,
    ....
    INDEX ix_B (B) type minmax GRANULARITY 3
) engine = MergeTree
partition by toYYYYMM(ts)
order by (toStartOfDay(ts),A,B);

```
bloom\_filter index type instead of min\_max could work fine in some situations.

### Inverted index as a projection


```
create table X (
    A UInt32,
    B UInt32,
    ts DateTime,
    ....
    PROJECTION ix_B  (
        select A, B,ts ORDER BY B, ts
    )
) engine = MergeTree
partition by toYYYYMM(ts)
order by (toStartOfDay(ts),A,B);

select * from X 
where A in (select A from X where B='....' and ts between ...)
  and B='...' and ts between ... ;

```
- The number of rows the subquery returns should not be very high. 1M rows seems to be a suitable limit.
- A separate table with a Materialized View can also be used similarly.
- accessing pattern for the main table will “point”, so better to lower index\_granularity to 256\. That will increase RAM usage by Primary Key

### mortonEncode

(available from 23\.10\)

Do not prioritize either A or B, but distribute indexing efficiency between them.

- <https://github.com/ClickHouse/ClickHouse/issues/41195>
- [https://www.youtube.com/watch?v\=5GR1J4T4\_d8](https://www.youtube.com/watch?v=5GR1J4T4_d8)
- [https://clickhouse.com/docs/en/operations/settings/settings\#analyze\_index\_with\_space\_filling\_curves](https://clickhouse.com/docs/en/operations/settings/settings#analyze_index_with_space_filling_curves)


```
create table X (
    A UInt32,
    B UInt32,
    ts DateTime,
    ....
) engine = MergeTree
partition by toYYYYMM(ts)
order by (toStartOfDay(ts),mortonEncode(A,B));
select * from X where A = '0123456789' and ts between ...;
select * from X where B = '0123456789' and ts between ...;

```
### mortonEncode with non\-UInt columns

[mortonEncode](https://clickhouse.com/docs/en/sql-reference/functions/encoding-functions#mortonencode)
function requires UInt columns, but sometimes different column types are needed (like String or ipv6\). In such a case, the cityHash64() function can be used both for inserting and querying:


```
create table X (
    A IPv6,
    B IPv6,
    AA alias cityHash64(A),
    BB alias cityHash64(B),
    ts DateTime materialized now()
) engine = MergeTree
partition by toYYYYMM(ts)
order by 
(toStartOfDay(ts),mortonEncode(cityHash64(A),cityHash64(B)))
;

insert into X values ('fd7a:115c:a1e0:ab12:4843:cd96:624c:9a17','fd7a:115c:a1e0:ab12:4843:cd96:624c:9a17')

select * from X where cityHash64(toIPv6('fd7a:115c:a1e0:ab12:4843:cd96:624c:9a17')) =  AA;

```
### hilbertEncode as alternative

(available from 24\.6\)

[hilbertEncode](https://clickhouse.com/docs/en/sql-reference/functions/encoding-functions#hilbertencode)
can be used instead of mortonEncode. On some data it allows better results than mortonEncode.

Last modified 2024\.09\.30: [Update two\-columns\-indexing.md (69d3de7\)](https://github.com/Altinity/altinityknowledgebase/commit/69d3de7ae116bfc02c3a808027aa8e2c74039739)

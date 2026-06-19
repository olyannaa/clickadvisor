# ClickHouse Over the Years with Benchmarks


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Over the Years with Benchmarks

![photo-ilya-yatsishin.jpeg](/_next/image?url=%2Fuploads%2Fphoto_ilya_yatsishin_f7befc8421.jpeg&w=96&q=75)[Ilya Yatsishin](/authors/ilya-yatsishin)Jun 14, 2022 · 13 minutes readClickHouse is developing very quickly: you can see semi\-structured data support, asynchronous inserts, replicated database engine, RBAC and other large features developed just recently. We are constantly improving performance, user experience and adding new features. Every time when somebody performs a benchmark of ClickHouse it is very handy. If we see that something is not so fast as expected we can improve it. If ClickHouse is faster or more efficient it is just nice to see. But results can be outdated really fast. Unfortunately we do not have some automated infrastructure (yet?) to run and publish benchmarks on every release and see how performance changes over time. Nevertheless our CI process checks every commit for performance changes and helps us to make ClickHouse faster. You can read more about performance testing in [this blog post](https://clickhouse.com/blog/testing-the-performance-of-click-house/). It also can be misleading if you just look at some old report and not try to make a decision without actual tests with your scenario.


Today I tried to run all available versions of ClickHouse and compare how performance changed over time using results of Star Schema Benchmark. It is even more interesting as I can’t improve performance of old ClickHouse versions and we can see even performance degradations if we had any. For this exercise I take x86\_64 AWS m5\.8xlarge server with Ubuntu 20\.04\.


*NOTE: The Star Schema Benchmark, while providing the value of comparison, has the immediate challenge of unrealistic random values distribution. As a result, we have found that it does not resemble real datasets. With that said, there is some utility in understanding the applicability to our current software.*


![ClickHouseBenchmarks-s.webp](/uploads/Click_House_Benchmarks_s_2e69fc665a.webp)
## **Finding the oldest available version** [\#](/blog/clickhouse-over-the-years-with-benchmarks#finding-the-oldest-available-version)


To start out archeological study we need to define a site to dig into. We changed our repository recently and there are no ancient versions available in the new one. Thus we can open an old branch on GitHub and look at how we proposed to install ClickHouse at that time. My random pick chose 18\.16 one here you can see [installation instructions](https://github.com/ClickHouse/ClickHouse/blob/v18.16/docs/en/getting_started/index.md).


First, do not forget to add a separate repository. You can try to run apt\-get install clickhouse\-server, but Ubuntu’s default repository only provides the 18\.16\.1\+ds\-7 version. It is pretty old and you can then question why it lacks something recent like s3 support. There are several reasons why we have not updated this version. We believe in static linkage and it is not allowed in official debian repositories. And ClickHouse release cycle with monthly stable releases has much higher velocity than Ubuntu provides.


So we add repositories for apt. Note that for recent releases we need to add new packages.clickhouse.com repo:



```
echo "deb http://repo.yandex.ru/clickhouse/deb/stable/ main/" | sudo tee /etc/apt/sources.list.d/clickhouse_old.list
echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee     /etc/apt/sources.list.d/clickhouse.list

```

Provide key to check signature of packages later and update cache:



```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4    # optional
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754
sudo apt-get update

```

We are not yet ready to install ClickHouse as it will install the most recent stable version. To get all versions list let’s run



```
apt list -a clickhouse-server

```

We can see that the repo has 328 versions of ClickHouse which is huge concerning that the oldest release in this repository is from 2018\-04\-16\. That means we released more than 80 releases a year including patch releases for supported versions.



```
apt show clickhouse-server=1.1.54378
Package: clickhouse-server
Version: 1.1.54378
Priority: optional
Section: database
Source: clickhouse
Maintainer: Alexey Milovidov <milovidov@yandex-team.ru>
Installed-Size: 71.7 kB
Provides: clickhouse-server-common
Depends: clickhouse-common-static (= 1.1.54378), adduser, tzdata
Replaces: clickhouse-server-base, clickhouse-server-common
Download-Size: 14.2 kB
APT-Sources: http://repo.yandex.ru/clickhouse/deb/stable main/ Packages
Description: Server binary for clickhouse
 Yandex ClickHouse is a column-oriented database management system
 that allows generating analytical data reports in real time.
 .
 This package provides clickhouse common configuration files

```

How I found it is from 2018? We actually have all releases in a separate list which is updated automatically [https://github.com/ClickHouse/ClickHouse/blob/master/utils/list\-versions/version\_date.tsv](https://github.com/ClickHouse/ClickHouse/blob/master/utils/list-versions/version_date.tsv)


This list helps to notify users with a new client binary that it is time to update ClickHouse server.


We found a pretty old version of ClickHouse, but this one is still 1\.5 years older than the first OpenSourced ClickHouse version. You can try to build the initial release, but there are no deb packages in the repository for earlier versions. Next, install this release.



```
sudo apt-get install clickhouse-client=1.1.54378 clickhouse-server=1.1.54378 clickhouse-common-static=1.1.54378
sudo service clickhouse-server start
clickhouse-client

ClickHouse client version 1.1.54378.
Connecting to localhost:9000.
Connected to ClickHouse server version 1.1.54378.

ip-172-31-19-143.us-east-2.compute.internal :) SELECT version()

SELECT version()

┌─version()─┐
│ 1.1.54378 │
└───────────┘

1 rows in set. Elapsed: 0.020 sec.

```

And we have our smiling client running in our hands!


## **The Results** [\#](/blog/clickhouse-over-the-years-with-benchmarks#the-results)


To perform some benchmarks I need data and queries. To start I will get [Star Schema Benchmark](https://clickhouse.com/docs/en/getting-started/example-datasets/star-schema/), [Brown University Benchmark](https://clickhouse.com/docs/en/getting-started/example-datasets/brown-benchmark/) and [ClickHouse performance benchmark](https://clickhouse.com/docs/en/operations/performance-test/).


For Star Schema Benchmark we clone the original benchmark generation tool, build it and generate a dataset with 100 scale. It is close to 100Gb of raw data.



```
git clone git@github.com:lemire/StarSchemaBenchmark.git
sudo apt-get install make clang-12
cd StarSchemaBenchmark
make CC=clang-12
./dbgen -s 100 -T a

```

Brown University Benchmark data is easier to get



```
wget https://datasets.clickhouse.com/mgbench{1..3}.csv.xz
xz -v -d mgbench{1..3}.csv.xz

```

ClickHouse performance benchmark data is available as binary parts that can be copied to ClickHouse data directory. It was intentionally updated recently to a newer format that supports adaptive granularity, so we will have to convert it to data that can be consumed by old ClickHouse version.



```
wget https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/benchmark/clickhouse/benchmark-new.sh
wget https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/benchmark/clickhouse/queries.sql
chmod a+x benchmark-new.sh
wget https://datasets.clickhouse.com/hits/partitions/hits_100m_obfuscated_v1.tar.xz
tar xvf hits_100m_obfuscated_v1.tar.xz -C .

```

We have this hits\_100m\_obfuscated\_v1 directory in internal format, but we don’t need to install a newer version of ClickHouse to read it. We will use clickhouse\-local mode that can perform ad\-hoc queries with any data without storing it to a disk. So I downloaded the newest build from master in the easiest way possible.



```
curl https://clickhouse.com/ | sh

```

Now I can just give the clickhouse\-local path to the data directory to start in interactive mode.



```
./clickhouse local --path hits_100m_obfuscated_v1
ip-172-31-16-30.us-east-2.compute.internal :) SHOW TABLES FROM default

SHOW TABLES FROM default

Query id: 7f43c001-22eb-4f33-9e67-f8ee0772a943

┌─name─────────────────┐
│ hits_100m_obfuscated │
└──────────────────────┘

1 rows in set. Elapsed: 0.001 sec.

```

To export and import data I need to choose a format. I will ask ClickHouse what formats it supports and to make this list a bit shorter will remove all “WithNames” and “WithNamesAndTypes” formats. I’ll try something trivial that the old version should definitely support: CSV.



```
ip-172-31-16-30.us-east-2.compute.internal :) select * from system.formats where is_output and is_input and name not like '%With%'
SELECT *
FROM system.formats
WHERE is_output AND is_input AND (name NOT LIKE '%With%')

Query id: bf3979fd-2ec6-44e1-b136-fa2b153f0165

┌─name──────────────────────┬─is_input─┬─is_output─┐
│ CapnProto                 │        1 │         1 │
│ ArrowStream               │        1 │         1 │
│ Avro                      │        1 │         1 │
│ ORC                       │        1 │         1 │
│ JSONCompactEachRow        │        1 │         1 │
│ CustomSeparated           │        1 │         1 │
│ RawBLOB                   │        1 │         1 │
│ Template                  │        1 │         1 │
│ MsgPack                   │        1 │         1 │
│ ProtobufList              │        1 │         1 │
│ ProtobufSingle            │        1 │         1 │
│ Native                    │        1 │         1 │
│ LineAsString              │        1 │         1 │
│ Protobuf                  │        1 │         1 │
│ RowBinary                 │        1 │         1 │
│ Arrow                     │        1 │         1 │
│ Parquet                   │        1 │         1 │
│ JSONCompactStringsEachRow │        1 │         1 │
│ TabSeparated              │        1 │         1 │
│ TSKV                      │        1 │         1 │
│ TSV                       │        1 │         1 │
│ CSV                       │        1 │         1 │
│ TSVRaw                    │        1 │         1 │
│ Values                    │        1 │         1 │
│ JSONStringsEachRow        │        1 │         1 │
│ TabSeparatedRaw           │        1 │         1 │
│ JSONEachRow               │        1 │         1 │
└───────────────────────────┴──────────┴───────────┘

27 rows in set. Elapsed: 0.001 sec.

```

It is sufficient just to give ClickHouse a hint about format and compression in a file name and that is it. Amazing.



```
ip-172-31-16-30.us-east-2.compute.internal :) SELECT * FROM default.hits_100m_obfuscated INTO OUTFILE 'hits_100m_obfuscated.csv.gz'

SELECT *
FROM default.hits_100m_obfuscated
INTO OUTFILE 'hits_100m_obfuscated.csv.gz'

Query id: 19a15f08-2e9e-4237-9a54-b1c27de0a9e2

100000000 rows in set. Elapsed: 537.464 sec. Processed 100.00 million rows, 74.69 GB (186.06 thousand rows/s., 138.96 MB/s.)

```

And retrieve the table schema to recreate it later.



```
ip-172-31-16-30.us-east-2.compute.internal :) SHOW CREATE TABLE default.hits_100m_obfuscated FORMAT LineAsString

SHOW CREATE TABLE default.hits_100m_obfuscated
FORMAT LineAsString

Query id: b515671e-01b0-4ca7-9e79-03ec9bc5aa86

CREATE TABLE default.hits_100m_obfuscated
(
    `WatchID` UInt64,
    `JavaEnable` UInt8,
    `Title` String,
    `GoodEvent` Int16,
    `EventTime` DateTime,
    `EventDate` Date,
    `CounterID` UInt32,
    `ClientIP` UInt32,
    `RegionID` UInt32,
    `UserID` UInt64,
    `CounterClass` Int8,
    `OS` UInt8,
    `UserAgent` UInt8,
    `URL` String,
    `Referer` String,
    `Refresh` UInt8,
    `RefererCategoryID` UInt16,
    `RefererRegionID` UInt32,
    `URLCategoryID` UInt16,
    `URLRegionID` UInt32,
    `ResolutionWidth` UInt16,
    `ResolutionHeight` UInt16,
    `ResolutionDepth` UInt8,
    `FlashMajor` UInt8,
    `FlashMinor` UInt8,
    `FlashMinor2` String,
    `NetMajor` UInt8,
    `NetMinor` UInt8,
    `UserAgentMajor` UInt16,
    `UserAgentMinor` FixedString(2),
    `CookieEnable` UInt8,
    `JavascriptEnable` UInt8,
    `IsMobile` UInt8,
    `MobilePhone` UInt8,
    `MobilePhoneModel` String,
    `Params` String,
    `IPNetworkID` UInt32,
    `TraficSourceID` Int8,
    `SearchEngineID` UInt16,
    `SearchPhrase` String,
    `AdvEngineID` UInt8,
    `IsArtifical` UInt8,
    `WindowClientWidth` UInt16,
    `WindowClientHeight` UInt16,
    `ClientTimeZone` Int16,
    `ClientEventTime` DateTime,
    `SilverlightVersion1` UInt8,
    `SilverlightVersion2` UInt8,
    `SilverlightVersion3` UInt32,
    `SilverlightVersion4` UInt16,
    `PageCharset` String,
    `CodeVersion` UInt32,
    `IsLink` UInt8,
    `IsDownload` UInt8,
    `IsNotBounce` UInt8,
    `FUniqID` UInt64,
    `OriginalURL` String,
    `HID` UInt32,
    `IsOldCounter` UInt8,
    `IsEvent` UInt8,
    `IsParameter` UInt8,
    `DontCountHits` UInt8,
    `WithHash` UInt8,
    `HitColor` FixedString(1),
    `LocalEventTime` DateTime,
    `Age` UInt8,
    `Sex` UInt8,
    `Income` UInt8,
    `Interests` UInt16,
    `Robotness` UInt8,
    `RemoteIP` UInt32,
    `WindowName` Int32,
    `OpenerName` Int32,
    `HistoryLength` Int16,
    `BrowserLanguage` FixedString(2),
    `BrowserCountry` FixedString(2),
    `SocialNetwork` String,
    `SocialAction` String,
    `HTTPError` UInt16,
    `SendTiming` UInt32,
    `DNSTiming` UInt32,
    `ConnectTiming` UInt32,
    `ResponseStartTiming` UInt32,
    `ResponseEndTiming` UInt32,
    `FetchTiming` UInt32,
    `SocialSourceNetworkID` UInt8,
    `SocialSourcePage` String,
    `ParamPrice` Int64,
    `ParamOrderID` String,
    `ParamCurrency` FixedString(3),
    `ParamCurrencyID` UInt16,
    `OpenstatServiceName` String,
    `OpenstatCampaignID` String,
    `OpenstatAdID` String,
    `OpenstatSourceID` String,
    `UTMSource` String,
    `UTMMedium` String,
    `UTMCampaign` String,
    `UTMContent` String,
    `UTMTerm` String,
    `FromTag` String,
    `HasGCLID` UInt8,
    `RefererHash` UInt64,
    `URLHash` UInt64,
    `CLID` UInt32
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate, intHash32(UserID), EventTime)
SAMPLE BY intHash32(UserID)
SETTINGS index_granularity_bytes = 1048576, index_granularity = 8192

1 rows in set. Elapsed: 0.001 sec.

```

## **Import datasets to the oldest version** [\#](/blog/clickhouse-over-the-years-with-benchmarks#import-datasets-to-the-oldest-version)


We can still use the most recent client to import data to ClickHouse from the year 2018\. So just switch from local to client mode. Note that there is no dash(\-) in the command as we have only one downloaded binary and symlinks with pretty names were not created.



```
./clickhouse client

```

To start with ClickHouse dataset can try the statement from above, but it complains that index\_granularity\_bytes is something unknown yet. So I trivially remove this setting and run this query successfully.


Then to import data we can’t use FROM INFILE or file() table function as the server is not ready for this feature. But we can import it just piping CSV data to client



```
zcat hits_100m_obfuscated.csv.gz | ./clickhouse client -q 'INSERT INTO default.hits_100m_obfuscated FORMAT CSV'

```

And check that number of rows is correct or just see progress. It should return 100m in the end.



```
watch -n 10 -x ./clickhouse client -q 'SELECT COUNT(*) from default.hits_100m_obfuscated'
Every 10.0s: ./clickhouse client -q SELECT COUNT(*) from default.hits_100m_obfuscated
ip-172-31-16-30: Thu Apr  7 13:33:17 2022
100000000

```

Next benchmark tables. We can see that instructions already mention LowCardinality data type, but it was still unsupported. So I convert LowCardinality(String) to simple String. The same reasons to use String for client\_ip instead of IPv4\.To store log\_time in DateTime format instead of DateTime64 we need to add milliseconds column and split data on insert to not lose any data. It is easier to create materialized columns and insert as before.



```
CREATE DATABASE mgbench;

CREATE TABLE mgbench.logs1 (
  log_time      DateTime,
  machine_name  String,
  machine_group String,
  cpu_idle      Nullable(Float32),
  cpu_nice      Nullable(Float32),
  cpu_system    Nullable(Float32),
  cpu_user      Nullable(Float32),
  cpu_wio       Nullable(Float32),
  disk_free     Nullable(Float32),
  disk_total    Nullable(Float32),
  part_max_used Nullable(Float32),
  load_fifteen  Nullable(Float32),
  load_five     Nullable(Float32),
  load_one      Nullable(Float32),
  mem_buffers   Nullable(Float32),
  mem_cached    Nullable(Float32),
  mem_free      Nullable(Float32),
  mem_shared    Nullable(Float32),
  swap_free     Nullable(Float32),
  bytes_in      Nullable(Float32),
  bytes_out     Nullable(Float32)
)
ENGINE = MergeTree()
ORDER BY (machine_group, machine_name, log_time);

CREATE TABLE mgbench.logs2 (
  log_time    DateTime,
  client_ip   String,
  request     String,
  status_code UInt16,
  object_size UInt64
)
ENGINE = MergeTree()
ORDER BY log_time;

CREATE TABLE mgbench.logs3 (
  log_time_raw String,
  device_id    FixedString(15),
  device_name  String,
  device_type  String,
  device_floor UInt8,
  event_type   String,
  event_unit   FixedString(1),
  event_value  Nullable(Float32),
  log_time     DateTime MATERIALIZED splitByChar('.', log_time_raw)[1],
  log_time_millis UInt16 MATERIALIZED splitByChar('.', log_time_raw)[2]
)
ENGINE = MergeTree()
ORDER BY (event_type, log_time, log_time_millis);

```

Then we just insert data. Note that you need to specify materialized columns if you want to read those. Asterisk is not showing them.



```
clickhouse-client --query "INSERT INTO mgbench.logs1 FORMAT CSVWithNames" < mgbench1.csv
clickhouse-client --query "INSERT INTO mgbench.logs2 FORMAT CSVWithNames" < mgbench2.csv
clickhouse-client --query "INSERT INTO mgbench.logs3 FORMAT CSVWithNames" < mgbench3.csv

ubuntu@ip-172-31-16-30:~/Brown$ clickhouse-client -q 'SELECT *, log_time, log_time_millis FROM mgbench.logs3 limit 1 FORMAT Vertical'
Row 1:
──────
log_time_raw:    2017-09-07 00:00:27.156
device_id:       157EAB3E2B0C9B4
device_name:     front_center_1
device_type:     door
device_floor:    1
event_type:      door_close
event_unit:      \0
event_value:     0
log_time:        2017-09-07 00:00:27
log_time_millis: 156

```

To import data for Star Schema Benchmark we need a bit more changes. We will create a schema without LowCardinality columns. And we have to add materialized columns with dates as we already supported best effort date time parsing, but there is no setting –date\_time\_input\_format\=best\_effort



```
CREATE TABLE customer
(
        C_CUSTKEY       UInt32,
        C_NAME          String,
        C_ADDRESS       String,
        C_CITY          String,
        C_NATION        String,
        C_REGION        String,
        C_PHONE         String,
        C_MKTSEGMENT    String
)
ENGINE = MergeTree ORDER BY (C_CUSTKEY);

CREATE TABLE lineorder
(
    LO_ORDERKEY             UInt32,
    LO_LINENUMBER           UInt8,
    LO_CUSTKEY              UInt32,
    LO_PARTKEY              UInt32,
    LO_SUPPKEY              UInt32,
    LO_ORDERDATE_RAW        String,
    LO_ORDERPRIORITY        String,
    LO_SHIPPRIORITY         UInt8,
    LO_QUANTITY             UInt8,
    LO_EXTENDEDPRICE        UInt32,
    LO_ORDTOTALPRICE        UInt32,
    LO_DISCOUNT             UInt8,
    LO_REVENUE              UInt32,
    LO_SUPPLYCOST           UInt32,
    LO_TAX                  UInt8,
    LO_COMMITDATE_RAW       String,
    LO_SHIPMODE             String,
    LO_ORDERDATE            Date MATERIALIZED parseDateTimeBestEffort(LO_ORDERDATE_RAW),
    LO_COMMITDATE           Date MATERIALIZED parseDateTimeBestEffort(LO_COMMITDATE_RAW)
)
ENGINE = MergeTree PARTITION BY toYear(LO_ORDERDATE) ORDER BY (LO_ORDERDATE, LO_ORDERKEY);

CREATE TABLE part
(
        P_PARTKEY       UInt32,
        P_NAME          String,
        P_MFGR          String,
        P_CATEGORY      String,
        P_BRAND         String,
        P_COLOR         String,
        P_TYPE          String,
        P_SIZE          UInt8,
        P_CONTAINER     String
)
ENGINE = MergeTree ORDER BY P_PARTKEY;

CREATE TABLE supplier
(
        S_SUPPKEY       UInt32,
        S_NAME          String,
        S_ADDRESS       String,
        S_CITY          String,
        S_NATION        String,
        S_REGION        String,
        S_PHONE         String
)
ENGINE = MergeTree ORDER BY S_SUPPKEY;

```

Format of tbl files is similar to CSV, but delimiter is \| and there is a delimiter in the end of the row that we need to remove. There are commas in the values, but no tabs, so we can update the data files and import them as TSV format. It is trivial just to use CSV or Template format in recent ClickHouse to import this data without converting, but in 2018 we had to improvise.



```
# check
grep -P '\t' *.tbl
# import
cat customer.tbl | sed 's/|$//; s/|/\t/g' | clickhouse-client --query "INSERT INTO customer FORMAT TSV"
cat part.tbl | sed 's/|$//; s/|/\t/g' | clickhouse-client --query "INSERT INTO part FORMAT TSV"
cat supplier.tbl | sed 's/|$//; s/|/\t/g' | clickhouse-client --query "INSERT INTO supplier FORMAT TSV"
cat lineorder.tbl | sed 's/|$//; s/|/\t/g' | clickhouse-client --query "INSERT INTO lineorder FORMAT TSV"
# check import
wc -l StarSchemaBenchmark/*.tbl
    3000000 StarSchemaBenchmark/customer.tbl
       2556 StarSchemaBenchmark/date.tbl
  600038145 StarSchemaBenchmark/lineorder.tbl
ubuntu@ip-172-31-16-30:~/StarSchemaBenchmark$ clickhouse-client -q 'select count(*) from lineorder'
600038145

```

Next step is to generate a flattened table. This version doesn’t have support for several joins in a query, so we need to adapt and overcome. We could try to join one by one, but probably it is not our goal. We can join using the recent version.



```
# original tables are owned by user clickhouse
sudo -u clickhouse ./clickhouse local --path /var/lib/clickhouse --no-system-tables --history_file /tmp/client-history
# switch from _local for easier queries
USE default

```

We are a bit lazy and don’t want to have mistakes in flattened table schema. Unfortunately at the moment you can’t use SHOW CREATE TABLE AS SELECT … statement, but you can create a view with the same AS SELECT and get it’s schema through SHOW CREATE TABLE view.



```
CREATE VIEW _local.lineorder_flat_view 
AS SELECT
    toYear(LO_ORDERDATE) AS F_YEAR,
    toMonth(LO_ORDERDATE) AS F_MONTHNUM,
    l.LO_ORDERKEY AS LO_ORDERKEY,
    l.LO_LINENUMBER AS LO_LINENUMBER,
    l.LO_CUSTKEY AS LO_CUSTKEY,
    l.LO_PARTKEY AS LO_PARTKEY,
    l.LO_SUPPKEY AS LO_SUPPKEY,
    l.LO_ORDERDATE AS LO_ORDERDATE,
    l.LO_ORDERPRIORITY AS LO_ORDERPRIORITY,
    l.LO_SHIPPRIORITY AS LO_SHIPPRIORITY,
    l.LO_QUANTITY AS LO_QUANTITY,
    l.LO_EXTENDEDPRICE AS LO_EXTENDEDPRICE,
    l.LO_ORDTOTALPRICE AS LO_ORDTOTALPRICE,
    l.LO_DISCOUNT AS LO_DISCOUNT,
    l.LO_REVENUE AS LO_REVENUE,
    l.LO_SUPPLYCOST AS LO_SUPPLYCOST,
    l.LO_TAX AS LO_TAX,
    l.LO_COMMITDATE AS LO_COMMITDATE,
    l.LO_SHIPMODE AS LO_SHIPMODE,
    c.C_NAME AS C_NAME,
    c.C_ADDRESS AS C_ADDRESS,
    c.C_CITY AS C_CITY,
    c.C_NATION AS C_NATION,
    c.C_REGION AS C_REGION,
    c.C_PHONE AS C_PHONE,
    c.C_MKTSEGMENT AS C_MKTSEGMENT,
    s.S_NAME AS S_NAME,
    s.S_ADDRESS AS S_ADDRESS,
    s.S_CITY AS S_CITY,
    s.S_NATION AS S_NATION,
    s.S_REGION AS S_REGION,
    s.S_PHONE AS S_PHONE,
    p.P_NAME AS P_NAME,
    p.P_MFGR AS P_MFGR,
    p.P_CATEGORY AS P_CATEGORY,
    p.P_BRAND AS P_BRAND,
    p.P_COLOR AS P_COLOR,
    p.P_TYPE AS P_TYPE,
    p.P_SIZE AS P_SIZE,
    p.P_CONTAINER AS P_CONTAINER
FROM lineorder AS l
INNER JOIN customer AS c ON c.C_CUSTKEY = l.LO_CUSTKEY
INNER JOIN supplier AS s ON s.S_SUPPKEY = l.LO_SUPPKEY
INNER JOIN part AS p ON p.P_PARTKEY = l.LO_PARTKEY;

SHOW CREATE VIEW _local.lineorder_flat_view
FORMAT Vertical

Query id: f41acb3b-7a10-4729-afaa-349b04f8aeb6

Row 1:
──────
statement: CREATE VIEW _local.lineorder_flat_view
(
    `F_YEAR` UInt16,
    `F_MONTHNUM` UInt8,
    `LO_ORDERKEY` UInt32,
    `LO_LINENUMBER` UInt8,
    `LO_CUSTKEY` UInt32,
    `LO_PARTKEY` UInt32,
    `LO_SUPPKEY` UInt32,
    `LO_ORDERDATE` Date,
    `LO_ORDERPRIORITY` String,
    `LO_SHIPPRIORITY` UInt8,
    `LO_QUANTITY` UInt8,
    `LO_EXTENDEDPRICE` UInt32,
    `LO_ORDTOTALPRICE` UInt32,
    `LO_DISCOUNT` UInt8,
    `LO_REVENUE` UInt32,
    `LO_SUPPLYCOST` UInt32,
    `LO_TAX` UInt8,
    `LO_COMMITDATE` Date,
    `LO_SHIPMODE` String,
    `C_NAME` String,
    `C_ADDRESS` String,
    `C_CITY` String,
    `C_NATION` String,
    `C_REGION` String,
    `C_PHONE` String,
    `C_MKTSEGMENT` String,
    `S_NAME` String,
    `S_ADDRESS` String,
    `S_CITY` String,
    `S_NATION` String,
    `S_REGION` String,
    `S_PHONE` String,
    `P_NAME` String,
    `P_MFGR` String,
    `P_CATEGORY` String,
    `P_BRAND` String,
    `P_COLOR` String,
    `P_TYPE` String,
    `P_SIZE` UInt8,
    `P_CONTAINER` String
) AS
SELECT
    toYear(LO_ORDERDATE) AS F_YEAR,
    toMonth(LO_ORDERDATE) AS F_MONTHNUM,
    l.LO_ORDERKEY AS LO_ORDERKEY,
    l.LO_LINENUMBER AS LO_LINENUMBER,
    l.LO_CUSTKEY AS LO_CUSTKEY,
    l.LO_PARTKEY AS LO_PARTKEY,
    l.LO_SUPPKEY AS LO_SUPPKEY,
    l.LO_ORDERDATE AS LO_ORDERDATE,
    l.LO_ORDERPRIORITY AS LO_ORDERPRIORITY,
    l.LO_SHIPPRIORITY AS LO_SHIPPRIORITY,
    l.LO_QUANTITY AS LO_QUANTITY,
    l.LO_EXTENDEDPRICE AS LO_EXTENDEDPRICE,
    l.LO_ORDTOTALPRICE AS LO_ORDTOTALPRICE,
    l.LO_DISCOUNT AS LO_DISCOUNT,
    l.LO_REVENUE AS LO_REVENUE,
    l.LO_SUPPLYCOST AS LO_SUPPLYCOST,
    l.LO_TAX AS LO_TAX,
    l.LO_COMMITDATE AS LO_COMMITDATE,
    l.LO_SHIPMODE AS LO_SHIPMODE,
    c.C_NAME AS C_NAME,
    c.C_ADDRESS AS C_ADDRESS,
    c.C_CITY AS C_CITY,
    c.C_NATION AS C_NATION,
    c.C_REGION AS C_REGION,
    c.C_PHONE AS C_PHONE,
    c.C_MKTSEGMENT AS C_MKTSEGMENT,
    s.S_NAME AS S_NAME,
    s.S_ADDRESS AS S_ADDRESS,
    s.S_CITY AS S_CITY,
    s.S_NATION AS S_NATION,
    s.S_REGION AS S_REGION,
    s.S_PHONE AS S_PHONE,
    p.P_NAME AS P_NAME,
    p.P_MFGR AS P_MFGR,
    p.P_CATEGORY AS P_CATEGORY,
    p.P_BRAND AS P_BRAND,
    p.P_COLOR AS P_COLOR,
    p.P_TYPE AS P_TYPE,
    p.P_SIZE AS P_SIZE,
    p.P_CONTAINER AS P_CONTAINER
FROM default.lineorder AS l
INNER JOIN default.customer AS c ON c.C_CUSTKEY = l.LO_CUSTKEY
INNER JOIN default.supplier AS s ON s.S_SUPPKEY = l.LO_SUPPKEY
INNER JOIN default.part AS p ON p.P_PARTKEY = l.LO_PARTKEY

1 rows in set. Elapsed: 0.000 sec.

```

And export data to gzipped csv file. Note that I had to output it to the tmp directory as I haven’t granted clickhouse user permissions to write to my home directory.



```
SELECT * FROM _local.lineorder_flat_view INTO OUTFILE '/tmp/lineorder_flat.csv.gz'

sudo chown ubuntu:ubuntu lineorder_flat.csv.gz
mv /tmp/lineorder_flat.csv.gz .

```

Now we create a table with a schema copied from a view and insert data.



```
CREATE TABLE lineorder_flat
(
    `F_YEAR` UInt16,
    `F_MONTHNUM` UInt8,
    `LO_ORDERKEY` UInt32,
    `LO_LINENUMBER` UInt8,
    `LO_CUSTKEY` UInt32,
    `LO_PARTKEY` UInt32,
    `LO_SUPPKEY` UInt32,
    `LO_ORDERDATE` Date,
    `LO_ORDERPRIORITY` String,
    `LO_SHIPPRIORITY` UInt8,
    `LO_QUANTITY` UInt8,
    `LO_EXTENDEDPRICE` UInt32,
    `LO_ORDTOTALPRICE` UInt32,
    `LO_DISCOUNT` UInt8,
    `LO_REVENUE` UInt32,
    `LO_SUPPLYCOST` UInt32,
    `LO_TAX` UInt8,
    `LO_COMMITDATE` Date,
    `LO_SHIPMODE` String,
    `C_NAME` String,
    `C_ADDRESS` String,
    `C_CITY` String,
    `C_NATION` String,
    `C_REGION` String,
    `C_PHONE` String,
    `C_MKTSEGMENT` String,
    `S_NAME` String,
    `S_ADDRESS` String,
    `S_CITY` String,
    `S_NATION` String,
    `S_REGION` String,
    `S_PHONE` String,
    `P_NAME` String,
    `P_MFGR` String,
    `P_CATEGORY` String,
    `P_BRAND` String,
    `P_COLOR` String,
    `P_TYPE` String,
    `P_SIZE` UInt8,
    `P_CONTAINER` String
)
ENGINE = MergeTree
PARTITION BY F_YEAR
ORDER BY (S_REGION, C_REGION, P_CATEGORY, F_MONTHNUM, LO_ORDERDATE, LO_ORDERKEY)

zcat lineorder_flat.csv.gz | clickhouse-client -q 'INSERT INTO lineorder_flat FORMAT CSV'

```

## **Adaptive granularity** [\#](/blog/clickhouse-over-the-years-with-benchmarks#adaptive-granularity)


It has been a while since we added the adaptive granularity feature, but there are versions in our versions set that had no support (\<19\.6\). We will create a new table with this feature enabled (Similar CREATE statement but with `index_granularity_bytes = 1048576` set) and populate it with data from `hits_100m_obfuscated` table. And the same with `lineorder_flat`.



```
INSERT INTO default.hits_100m_obfuscated_adaptive SELECT * FROM default.hits_100m_obfuscated
INSERT INTO default.lineorder_flat_adaptive SELECT * FROM default.lineorder_flat

```

## **Running benchmarks** [\#](/blog/clickhouse-over-the-years-with-benchmarks#running-benchmarks)


We have a ready script to run common ClickHouse benchmarks on different hardware. It runs a set of queries three times and stores results in JSON. It is trivial to add more queries in the list, so we added Star Schema Benchmark and Brown University Benchmark queries.


Just adding some bash code that makes it possible to run different versions and collect results in the most straightforward manner possible we can start collecting data. Here is a variant that supports tables with adaptive granularity – it just adds adds one more field and queries corresponding tables.



```
#!/bin/bash
VERSION_ARR=(${1//[-v]/ })
VERSION=${VERSION_ARR[0]}
FILE_NAME=${VERSION}_adaptive.json
DATE=$2

echo "$VERSION $DATE"
sudo DEBIAN_FRONTEND=noninteractive apt-get install --allow-downgrades --yes clickhouse-client=$VERSION clickhouse-server=$VERSION clickhouse-common-static=$VERSION
sudo service clickhouse-server restart
echo '
[
    {
        "system":       "'$DATE' '$VERSION'",
        "system_full":  "ClickHouse '$VERSION $DATE'(adaptive)",
        "version":      "'$VERSION",
        "type":         "adaptive",
        "comments":     "",
        "result":
        [
' | tee $FILE_NAME

./benchmark-new-adaptive.sh >> $FILE_NAME

sed -i '$ s/,$//' $FILE_NAME

echo '          ]
    }
]' >> $FILE_NAME

```

## **Results** [\#](/blog/clickhouse-over-the-years-with-benchmarks#results)


We already have our common report web page that allows us to compare results of different hardware or versions. I had to place all results in [one more directory](https://github.com/ClickHouse/ClickHouse/pull/36628) and publish the report. Overall we can see that ClickHouse is 28% faster than the version from 2018\. The 18\.16 version is quite special as this version is available in Ubuntu repositories, but it is obsolete and we don’t recommend using it now.


Complete results are available at <https://clickhouse.com/benchmark/versions/>. You can choose what version you want to compare. Query speed is better when smaller. Color makes it easier to see how results are compared in one row – green is better. It is possible to see that some versions show faster results than newer ones. We are investigating what are the reasons: some older versions could return incorrect results or we have points of improvement.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

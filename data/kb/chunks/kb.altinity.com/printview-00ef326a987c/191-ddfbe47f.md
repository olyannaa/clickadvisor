---
source: kb.altinity.com
url: http://altinity.com/
topic: altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 191
total_chunks_in_doc: 478
---

unixODBC # Debian/Ubuntu sudo apt install openssl unixodbc ``` - MacOS (assuming you have [Homebrew](https://brew.sh/) installed): ``` brew install poco openssl libiodbc ``` 2. register the driver so that the corresponding ODBC provider is able to locate it.

All this involves modifying a dedicated registry keys in case of MDAC, or editing `odbcinst.ini` (for driver registration) and `odbc.ini` (for DSN definition) files for UnixODBC or iODBC, directly or indirectly.

This will be done automatically using some default values if you are installing the driver using native installers.

Otherwise, if you are configuring manually, or need to modify the default configuration created by the installer, please see the exact locations of files (or registry keys) that need to be modified.

# 4\.5 \- ClickHouse® \+ Spark

### jdbc

The trivial \& natural way to talk to ClickHouse from Spark is using jdbc. There are 2 jdbc drivers:

- [https://github.com/ClickHouse/clickhouse\-jdbc/](https://github.com/ClickHouse/clickhouse-jdbc/)
- [https://github.com/housepower/ClickHouse\-Native\-JDBC\#integration\-with\-spark](https://github.com/housepower/ClickHouse-Native-JDBC#integration-with-spark)

ClickHouse\-Native\-JDBC has some hints about integration with Spark even in the main README file.

‘Official’ driver does support some conversion of complex data types (Roaring bitmaps) for Spark\-ClickHouse integration: [https://github.com/ClickHouse/clickhouse\-jdbc/pull/596](https://github.com/ClickHouse/clickhouse-jdbc/pull/596)

But proper partitioning of the data (to spark partitions) may be tricky with jdbc.

Some example snippets:

- [https://markelic.de/how\-to\-access\-your\-clickhouse\-database\-with\-spark\-in\-python/](https://markelic.de/how-to-access-your-clickhouse-database-with-spark-in-python/)
- [https://stackoverflow.com/questions/60448877/how\-can\-i\-write\-spark\-dataframe\-to\-clickhouse](https://stackoverflow.com/questions/60448877/how-can-i-write-spark-dataframe-to-clickhouse)

### Connectors

- [https://github.com/DmitryBe/spark\-clickhouse](https://github.com/DmitryBe/spark-clickhouse)
(looks dead)
- [https://github.com/VaBezruchko/spark\-clickhouse\-connector](https://github.com/VaBezruchko/spark-clickhouse-connector)
(is not actively maintained).
- [https://github.com/housepower/spark\-clickhouse\-connector](https://github.com/housepower/spark-clickhouse-connector)
(actively developing connector from housepower \- same guys as authors of ClickHouse\-Native\-JDBC)

### via Kafka

ClickHouse can produce / consume data from/to Kafka to exchange data with Spark.

### via hdfs

You can load data into hadoop/hdfs using sequence of statements like `INSERT INTO FUNCTION hdfs(...) SELECT ... FROM clickhouse_table`
later process the data from hdfs by spark and do the same in reverse direction.

### via s3

Similar to above but using s3\.

### via shell calls

You can call other commands from Spark. Those commands can be `clickhouse-client` and/or `clickhouse-local`.

### do you really need Spark? :)

In many cases you can do everything inside ClickHouse without Spark help :)
Arrays, Higher\-order functions, machine learning, integration with lot of different things including the possibility to run some external code using executable dictionaries or UDF.

## More info \+ some unordered links (mostly in Chinese / Russian)

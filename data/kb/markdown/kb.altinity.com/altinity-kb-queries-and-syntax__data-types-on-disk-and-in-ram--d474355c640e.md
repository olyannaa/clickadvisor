# Data types on disk and in RAM \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. Data types on disk and in RAM
# Data types on disk and in RAM



| DataType | RAM size (\=byteSize) | Disk Size |
| --- | --- | --- |
| String | string byte length \+ 9string length: 64 bit integerzero\-byte terminator: 1 byte. | string length prefix (varint) \+ string itself:string shorter than 128 \- string byte length \+ 1string shorter than 16384 \- string byte length \+ 2string shorter than 2097152 \- string byte length \+ 2string shorter than 268435456 \- string byte length \+ 4 |
| AggregateFunction(count, ...) |  | varint |

See also the presentation [Data processing into ClickHouse®](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup41/data_processing.pdf)
, especially slides 17\-22\.

Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)

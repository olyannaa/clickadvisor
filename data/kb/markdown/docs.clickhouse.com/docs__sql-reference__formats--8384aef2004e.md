# Formats for Input and Output Data \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- Input and Output Formats
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/formats.mdx)# Formats for input and output data


ClickHouse supports most of the known text and binary data formats. This allows easy integration into almost any working
data pipeline to leverage the benefits of ClickHouse.


## Input formats[​](#input-formats "Direct link to Input formats")


Input formats are used for:


- Parsing data provided to `INSERT` statements
- Performing `SELECT` queries from file\-backed tables such as `File`, `URL`, or `HDFS`
- Reading dictionaries


Choosing the right input format is crucial for efficient data ingestion in ClickHouse. With over 70 supported formats,
selecting the most performant option can significantly impact insert speed, CPU and memory usage, and overall system
efficiency. To help navigate these choices, we benchmarked ingestion performance across formats, revealing key takeaways:


- **The [Native](/docs/interfaces/formats/Native) format is the most efficient input format**, offering the best compression, lowest
resource usage, and minimal server\-side processing overhead.
- **Compression is essential** \- LZ4 reduces data size with minimal CPU cost, while ZSTD offers higher compression at the
expense of additional CPU usage.
- **Pre\-sorting has a moderate impact**, as ClickHouse already sorts efficiently.
- **Batching significantly improves efficiency** \- larger batches reduce insert overhead and improve throughput.


For a deep dive into the results and best practices,
read the full [benchmark analysis](https://www.clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient).
For the full test results, explore the [FastFormats](https://fastformats.clickhouse.com/) online dashboard.


## Output formats[​](#output-formats "Direct link to Output formats")


Formats supported for output are used for:


- Arranging the results of a `SELECT` query
- Performing `INSERT` operations into file\-backed tables


## Formats overview[​](#formats-overview "Direct link to Formats overview")


The supported formats are:




| Format Input Output| [TabSeparated](/docs/interfaces/formats/TabSeparated) ✔ ✔| [TabSeparatedRaw](/docs/interfaces/formats/TabSeparatedRaw) ✔ ✔| [TabSeparatedWithNames](/docs/interfaces/formats/TabSeparatedWithNames) ✔ ✔| [TabSeparatedWithNamesAndTypes](/docs/interfaces/formats/TabSeparatedWithNamesAndTypes) ✔ ✔| [TabSeparatedRawWithNames](/docs/interfaces/formats/TabSeparatedRawWithNames) ✔ ✔| [TabSeparatedRawWithNamesAndTypes](/docs/interfaces/formats/TabSeparatedRawWithNamesAndTypes) ✔ ✔| [Template](/docs/interfaces/formats/Template) ✔ ✔| [TemplateIgnoreSpaces](/docs/interfaces/formats/TemplateIgnoreSpaces) ✔ ✗| [CSV](/docs/interfaces/formats/CSV) ✔ ✔| [CSVWithNames](/docs/interfaces/formats/CSVWithNames) ✔ ✔| [CSVWithNamesAndTypes](/docs/interfaces/formats/CSVWithNamesAndTypes) ✔ ✔| [CustomSeparated](/docs/interfaces/formats/CustomSeparated) ✔ ✔| [CustomSeparatedWithNames](/docs/interfaces/formats/CustomSeparatedWithNames) ✔ ✔| [CustomSeparatedWithNamesAndTypes](/docs/interfaces/formats/CustomSeparatedWithNamesAndTypes) ✔ ✔| [SQLInsert](/docs/interfaces/formats/SQLInsert) ✗ ✔| [Values](/docs/interfaces/formats/Values) ✔ ✔| [Vertical](/docs/interfaces/formats/Vertical) ✗ ✔| [JSON](/docs/interfaces/formats/JSON) ✔ ✔| [JSONAsString](/docs/interfaces/formats/JSONAsString) ✔ ✗| [JSONAsObject](/docs/interfaces/formats/JSONAsObject) ✔ ✗| [JSONStrings](/docs/interfaces/formats/JSONStrings) ✔ ✔| [JSONColumns](/docs/interfaces/formats/JSONColumns) ✔ ✔| [JSONColumnsWithMetadata](/docs/interfaces/formats/JSONColumnsWithMetadata) ✔ ✔| [JSONCompact](/docs/interfaces/formats/JSONCompact) ✔ ✔| [JSONCompactStrings](/docs/interfaces/formats/JSONCompactStrings) ✗ ✔| [JSONCompactColumns](/docs/interfaces/formats/JSONCompactColumns) ✔ ✔| [JSONEachRow](/docs/interfaces/formats/JSONEachRow) ✔ ✔| [PrettyJSONEachRow](/docs/interfaces/formats/PrettyJSONEachRow) ✗ ✔| [JSONEachRowWithProgress](/docs/interfaces/formats/JSONEachRowWithProgress) ✗ ✔| [JSONStringsEachRow](/docs/interfaces/formats/JSONStringsEachRow) ✔ ✔| [JSONStringsEachRowWithProgress](/docs/interfaces/formats/JSONStringsEachRowWithProgress) ✗ ✔| [JSONCompactEachRow](/docs/interfaces/formats/JSONCompactEachRow) ✔ ✔| [JSONCompactEachRowWithNames](/docs/interfaces/formats/JSONCompactEachRowWithNames) ✔ ✔| [JSONCompactEachRowWithNamesAndTypes](/docs/interfaces/formats/JSONCompactEachRowWithNamesAndTypes) ✔ ✔| [JSONCompactEachRowWithProgress](/docs/interfaces/formats/JSONCompactEachRowWithProgress) ✗ ✔| [JSONCompactStringsEachRow](/docs/interfaces/formats/JSONCompactStringsEachRow) ✔ ✔| [JSONCompactStringsEachRowWithNames](/docs/interfaces/formats/JSONCompactStringsEachRowWithNames) ✔ ✔| [JSONCompactStringsEachRowWithNamesAndTypes](/docs/interfaces/formats/JSONCompactStringsEachRowWithNamesAndTypes) ✔ ✔| [JSONCompactStringsEachRowWithProgress](/docs/interfaces/formats/JSONCompactStringsEachRowWithProgress) ✗ ✔| [JSONObjectEachRow](/docs/interfaces/formats/JSONObjectEachRow) ✔ ✔| [BSONEachRow](/docs/interfaces/formats/BSONEachRow) ✔ ✔| [TSKV](/docs/interfaces/formats/TSKV) ✔ ✔| [Pretty](/docs/interfaces/formats/Pretty) ✗ ✔| [PrettyNoEscapes](/docs/interfaces/formats/PrettyNoEscapes) ✗ ✔| [PrettyMonoBlock](/docs/interfaces/formats/PrettyMonoBlock) ✗ ✔| [PrettyNoEscapesMonoBlock](/docs/interfaces/formats/PrettyNoEscapesMonoBlock) ✗ ✔| [PrettyCompact](/docs/interfaces/formats/PrettyCompact) ✗ ✔| [PrettyCompactNoEscapes](/docs/interfaces/formats/PrettyCompactNoEscapes) ✗ ✔| [PrettyCompactMonoBlock](/docs/interfaces/formats/PrettyCompactMonoBlock) ✗ ✔| [PrettyCompactNoEscapesMonoBlock](/docs/interfaces/formats/PrettyCompactNoEscapesMonoBlock) ✗ ✔| [PrettySpace](/docs/interfaces/formats/PrettySpace) ✗ ✔| [PrettySpaceNoEscapes](/docs/interfaces/formats/PrettySpaceNoEscapes) ✗ ✔| [PrettySpaceMonoBlock](/docs/interfaces/formats/PrettySpaceMonoBlock) ✗ ✔| [PrettySpaceNoEscapesMonoBlock](/docs/interfaces/formats/PrettySpaceNoEscapesMonoBlock) ✗ ✔| [Prometheus](/docs/interfaces/formats/Prometheus) ✗ ✔| [Protobuf](/docs/interfaces/formats/Protobuf) ✔ ✔| [ProtobufSingle](/docs/interfaces/formats/ProtobufSingle) ✔ ✔| [ProtobufList](/docs/interfaces/formats/ProtobufList) ✔ ✔| [Avro](/docs/interfaces/formats/Avro) ✔ ✔| [AvroConfluent](/docs/interfaces/formats/AvroConfluent) ✔ ✔| [Parquet](/docs/interfaces/formats/Parquet) ✔ ✔| [ParquetMetadata](/docs/interfaces/formats/ParquetMetadata) ✔ ✗| [Arrow](/docs/interfaces/formats/Arrow) ✔ ✔| [ArrowStream](/docs/interfaces/formats/ArrowStream) ✔ ✔| [ORC](/docs/interfaces/formats/ORC) ✔ ✔| [One](/docs/interfaces/formats/One) ✔ ✗| [Npy](/docs/interfaces/formats/Npy) ✔ ✔| [RowBinary](/docs/interfaces/formats/RowBinary) ✔ ✔| [RowBinaryWithNames](/docs/interfaces/formats/RowBinaryWithNames) ✔ ✔| [RowBinaryWithNamesAndTypes](/docs/interfaces/formats/RowBinaryWithNamesAndTypes) ✔ ✔| [RowBinaryWithDefaults](/docs/interfaces/formats/RowBinaryWithDefaults) ✔ ✗| [Native](/docs/interfaces/formats/Native) ✔ ✔| [Buffers](/docs/interfaces/formats/Buffers) ✔ ✔| [Null](/docs/interfaces/formats/Null) ✗ ✔| [Hash](/docs/interfaces/formats/Hash) ✗ ✔| [XML](/docs/interfaces/formats/XML) ✗ ✔| [CapnProto](/docs/interfaces/formats/CapnProto) ✔ ✔| [LineAsString](/docs/interfaces/formats/LineAsString) ✔ ✔| [LineAsStringWithNames](/docs/interfaces/formats/LineAsStringWithNames) ✔ ✔| [LineAsStringWithNamesAndTypes](/docs/interfaces/formats/LineAsStringWithNamesAndTypes) ✔ ✔| [Regexp](/docs/interfaces/formats/Regexp) ✔ ✗| [RawBLOB](/docs/interfaces/formats/RawBLOB) ✔ ✔| [MsgPack](/docs/interfaces/formats/MsgPack) ✔ ✔| [MySQLDump](/docs/interfaces/formats/MySQLDump) ✔ ✗| [DWARF](/docs/interfaces/formats/DWARF) ✔ ✗| [Markdown](/docs/interfaces/formats/Markdown) ✗ ✔| [Form](/docs/interfaces/formats/Form) ✔ ✗ | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


You can control some format processing parameters with the ClickHouse settings. For more information read the [Settings](/docs/operations/settings/formats) section.


## Format schema[​](#formatschema "Direct link to Format schema")


The file name containing the format schema is set by the setting `format_schema`.
It's required to set this setting when it is used one of the formats `Cap'n Proto` and `Protobuf`.
The format schema is a combination of a file name and the name of a message type in this file, delimited by a colon,
e.g. `schemafile.proto:MessageType`.
If the file has the standard extension for the format (for example, `.proto` for `Protobuf`),
it can be omitted and in this case, the format schema looks like `schemafile:MessageType`.


If you input or output data via the [client](/docs/interfaces/client) in interactive mode, the file name specified in the format schema
can contain an absolute path or a path relative to the current directory on the client.
If you use the client in the [batch mode](/docs/interfaces/client#batch-mode), the path to the schema must be relative due to security reasons.


If you input or output data via the [HTTP interface](/docs/interfaces/http) the file name specified in the format schema
should be located in the directory specified in [format\_schema\_path](/docs/operations/server-configuration-parameters/settings#format_schema_path)
in the server configuration.


## Skipping errors[​](#skippingerrors "Direct link to Skipping errors")


Some formats such as `CSV`, `TabSeparated`, `TSKV`, `JSONEachRow`, `Template`, `CustomSeparated` and `Protobuf` can skip broken row if parsing error occurred and continue parsing from the beginning of next row. See [input\_format\_allow\_errors\_num](/docs/operations/settings/formats#input_format_allow_errors_num) and
[input\_format\_allow\_errors\_ratio](/docs/operations/settings/formats#input_format_allow_errors_ratio) settings.
Limitations:


- In case of parsing error `JSONEachRow` skips all data until the new line (or EOF), so rows must be delimited by `\n` to count errors correctly.
- `Template` and `CustomSeparated` use delimiter after the last column and delimiter between rows to find the beginning of next row, so skipping errors works only if at least one of them is not empty.
[PreviousSyntax](/docs/sql-reference/syntax)[NextList of data types](/docs/sql-reference/data-types)- [Input formats](#input-formats)- [Output formats](#output-formats)- [Formats overview](#formats-overview)- [Format schema](#formatschema)- [Skipping errors](#skippingerrors)
Was this page helpful?

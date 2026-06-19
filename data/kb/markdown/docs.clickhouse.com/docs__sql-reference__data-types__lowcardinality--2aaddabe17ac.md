# LowCardinality(T) \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- LowCardinality(T)
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/lowcardinality.md)# LowCardinality(T)

Changes the internal representation of other data types to be dictionary\-encoded.


## Syntax[​](#syntax "Direct link to Syntax")



```
LowCardinality(data_type)

```

**Parameters**


- `data_type` — [String](/docs/sql-reference/data-types/string), [FixedString](/docs/sql-reference/data-types/fixedstring), [Date](/docs/sql-reference/data-types/date), [DateTime](/docs/sql-reference/data-types/datetime), and numbers excepting [Decimal](/docs/sql-reference/data-types/decimal). `LowCardinality` is not efficient for some data types, see the [allow\_suspicious\_low\_cardinality\_types](/docs/operations/settings/settings#allow_suspicious_low_cardinality_types) setting description.


## Description[​](#description "Direct link to Description")


`LowCardinality` is a superstructure that changes a data storage method and rules of data processing. ClickHouse applies [dictionary coding](https://en.wikipedia.org/wiki/Dictionary_coder) to `LowCardinality`\-columns. Operating with dictionary encoded data significantly increases performance of [SELECT](/docs/sql-reference/statements/select) queries for many applications.


The efficiency of using `LowCardinality` data type depends on data diversity. If a dictionary contains less than 10,000 distinct values, then ClickHouse mostly shows higher efficiency of data reading and storing. If a dictionary contains more than 100,000 distinct values, then ClickHouse can perform worse in comparison with using ordinary data types.


Consider using `LowCardinality` instead of [Enum](/docs/sql-reference/data-types/enum) when working with strings. `LowCardinality` provides more flexibility in use and often reveals the same or higher efficiency.


## Example[​](#example "Direct link to Example")


Create a table with a `LowCardinality`\-column:



```
CREATE TABLE lc_t
(
    `id` UInt16,
    `strings` LowCardinality(String)
)
ENGINE = MergeTree()
ORDER BY id

```

## Related Settings and Functions[​](#related-settings-and-functions "Direct link to Related Settings and Functions")


Settings:


- [low\_cardinality\_max\_dictionary\_size](/docs/operations/settings/settings#low_cardinality_max_dictionary_size)
- [low\_cardinality\_use\_single\_dictionary\_for\_part](/docs/operations/settings/settings#low_cardinality_use_single_dictionary_for_part)
- [low\_cardinality\_allow\_in\_native\_format](/docs/operations/settings/settings#low_cardinality_allow_in_native_format)
- [allow\_suspicious\_low\_cardinality\_types](/docs/operations/settings/settings#allow_suspicious_low_cardinality_types)
- [output\_format\_arrow\_low\_cardinality\_as\_dictionary](/docs/operations/settings/formats#output_format_arrow_low_cardinality_as_dictionary)


Functions:


- [toLowCardinality](/docs/sql-reference/functions/type-conversion-functions#toLowCardinality)


## Related content[​](#related-content "Direct link to Related content")


- Blog: [Optimizing ClickHouse with Schemas and Codecs](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema)
- Blog: [Working with time series data in ClickHouse](https://clickhouse.com/blog/working-with-time-series-data-and-functions-ClickHouse)
- [String Optimization (video presentation in Russian)](https://youtu.be/rqf-ILRgBdY?list=PL0Z2YDlm0b3iwXCpEFiOOYmwXzVmjJfEt). [Slides in English](https://github.com/ClickHouse/clickhouse-presentations/raw/master/meetup19/string_optimization.pdf)
[PreviousVariant(T1, T2, ...)](/docs/sql-reference/data-types/variant)[NextNullable(T)](/docs/sql-reference/data-types/nullable)- [Syntax](#syntax)- [Description](#description)- [Example](#example)- [Related Settings and Functions](#related-settings-and-functions)- [Related content](#related-content)
Was this page helpful?

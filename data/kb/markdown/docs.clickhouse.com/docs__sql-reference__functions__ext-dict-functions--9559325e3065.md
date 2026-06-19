# Functions for Working with Dictionaries \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Dictionaries
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/ext-dict-functions.md)# Functions for Working with Dictionaries

NoteFor dictionaries created with [DDL queries](/docs/sql-reference/statements/create/dictionary), the `dict_name` parameter must be fully specified, like `<database>.<dict_name>`. Otherwise, the current database is used.


For information on connecting and configuring dictionaries, see [Dictionaries](/docs/sql-reference/statements/create/dictionary).


## Example dictionaries[​](#example-dictionary "Direct link to Example dictionaries")


The examples in this section make use of the following dictionaries. You can create them in ClickHouse
to run the examples for the functions described below.


Example dictionary for dictGet\<T\> and dictGet\<T\>OrDefault functions
```
-- Create table with all the required data types
CREATE TABLE all_types_test (
    `id` UInt32,
    
    -- String type
    `String_value` String,
    
    -- Unsigned integer types
    `UInt8_value` UInt8,
    `UInt16_value` UInt16,
    `UInt32_value` UInt32,
    `UInt64_value` UInt64,
    
    -- Signed integer types
    `Int8_value` Int8,
    `Int16_value` Int16,
    `Int32_value` Int32,
    `Int64_value` Int64,
    
    -- Floating point types
    `Float32_value` Float32,
    `Float64_value` Float64,
    
    -- Date/time types
    `Date_value` Date,
    `DateTime_value` DateTime,
    
    -- Network types
    `IPv4_value` IPv4,
    `IPv6_value` IPv6,
    
    -- UUID type
    `UUID_value` UUID
) ENGINE = MergeTree() 
ORDER BY id;

```

```
-- Insert test data
INSERT INTO all_types_test VALUES
(
    1,                              -- id
    'ClickHouse',                   -- String
    100,                            -- UInt8
    5000,                           -- UInt16
    1000000,                        -- UInt32
    9223372036854775807,            -- UInt64
    -100,                           -- Int8
    -5000,                          -- Int16
    -1000000,                       -- Int32
    -9223372036854775808,           -- Int64
    123.45,                         -- Float32
    987654.123456,                  -- Float64
    '2024-01-15',                   -- Date
    '2024-01-15 10:30:00',          -- DateTime
    '192.168.1.1',                  -- IPv4
    '2001:db8::1',                  -- IPv6
    '550e8400-e29b-41d4-a716-446655440000' -- UUID
)

```

```
-- Create dictionary
CREATE DICTIONARY all_types_dict
(
    id UInt32,
    String_value String,
    UInt8_value UInt8,
    UInt16_value UInt16,
    UInt32_value UInt32,
    UInt64_value UInt64,
    Int8_value Int8,
    Int16_value Int16,
    Int32_value Int32,
    Int64_value Int64,
    Float32_value Float32,
    Float64_value Float64,
    Date_value Date,
    DateTime_value DateTime,
    IPv4_value IPv4,
    IPv6_value IPv6,
    UUID_value UUID
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' TABLE 'all_types_test' DB 'default'))
LAYOUT(HASHED())
LIFETIME(MIN 300 MAX 600);

```

Example dictionary for dictGetAllCreate a table to store the data for the regexp tree dictionary:
```
CREATE TABLE regexp_os(
    id UInt64,
    parent_id UInt64,
    regexp String,
    keys Array(String),
    values Array(String)
)
ENGINE = Memory;

```
Insert data into the table:
```
INSERT INTO regexp_os 
SELECT *
FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/' ||
    'user_agent_regex/regexp_os.csv'
);

```
Create the regexp tree dictionary:
```
CREATE DICTIONARY regexp_tree
(
    regexp String,
    os_replacement String DEFAULT 'Other',
    os_v1_replacement String DEFAULT '0',
    os_v2_replacement String DEFAULT '0',
    os_v3_replacement String DEFAULT '0',
    os_v4_replacement String DEFAULT '0'
)
PRIMARY KEY regexp
SOURCE(CLICKHOUSE(TABLE 'regexp_os'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(REGEXP_TREE);

```







Example range key dictionaryCreate the input table:
```
CREATE TABLE range_key_dictionary_source_table
(
    key UInt64,
    start_date Date,
    end_date Date,
    value String,
    value_nullable Nullable(String)
)
ENGINE = TinyLog();

```
Insert the data into the input table:
```
INSERT INTO range_key_dictionary_source_table VALUES(1, toDate('2019-05-20'), toDate('2019-05-20'), 'First', 'First');
INSERT INTO range_key_dictionary_source_table VALUES(2, toDate('2019-05-20'), toDate('2019-05-20'), 'Second', NULL);
INSERT INTO range_key_dictionary_source_table VALUES(3, toDate('2019-05-20'), toDate('2019-05-20'), 'Third', 'Third');

```
Create the dictionary:
```
CREATE DICTIONARY range_key_dictionary
(
    key UInt64,
    start_date Date,
    end_date Date,
    value String,
    value_nullable Nullable(String)
)
PRIMARY KEY key
SOURCE(CLICKHOUSE(HOST 'localhost' PORT tcpPort() TABLE 'range_key_dictionary_source_table'))
LIFETIME(MIN 1 MAX 1000)
LAYOUT(RANGE_HASHED())
RANGE(MIN start_date MAX end_date);

```







Example complex key dictionaryCreate the source table:
```
CREATE TABLE dict_mult_source
(
id UInt32,
c1 UInt32,
c2 String
) ENGINE = Memory;

```
Insert the data into the source table:
```
INSERT INTO dict_mult_source VALUES
(1, 1, '1'),
(2, 2, '2'),
(3, 3, '3');

```
Create the dictionary:
```
CREATE DICTIONARY ext_dict_mult
(
    id UInt32,
    c1 UInt32,
    c2 String
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' TABLE 'dict_mult_source' DB 'default'))
LAYOUT(FLAT())
LIFETIME(MIN 0 MAX 0);

```







Example hierarchical dictionaryCreate the source table:
```
CREATE TABLE hierarchy_source
(
  id UInt64,
  parent_id UInt64,
  name String
) ENGINE = Memory;

```
Insert the data into the source table:
```
INSERT INTO hierarchy_source VALUES
(0, 0, 'Root'),
(1, 0, 'Level 1 - Node 1'),
(2, 1, 'Level 2 - Node 2'),
(3, 1, 'Level 2 - Node 3'),
(4, 2, 'Level 3 - Node 4'),
(5, 2, 'Level 3 - Node 5'),
(6, 3, 'Level 3 - Node 6');

-- 0 (Root)
-- └── 1 (Level 1 - Node 1)
--     ├── 2 (Level 2 - Node 2)
--     │   ├── 4 (Level 3 - Node 4)
--     │   └── 5 (Level 3 - Node 5)
--     └── 3 (Level 2 - Node 3)
--         └── 6 (Level 3 - Node 6)

```
Create the dictionary:
```
CREATE DICTIONARY hierarchical_dictionary
(
    id UInt64,
    parent_id UInt64 HIERARCHICAL,
    name String
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' TABLE 'hierarchy_source' DB 'default'))
LAYOUT(HASHED())
LIFETIME(MIN 300 MAX 600);

```







## dictGet[​](#dictGet "Direct link to dictGet")


Introduced in: v18\.16\.0


Retrieves values from a dictionary.


**Syntax**



```
dictGet('dict_name', attr_names, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_names` — Name of the column of the dictionary, or tuple of column names. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning UInt64/Tuple(T). [`UInt64`](/docs/sql-reference/data-types/int-uint) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to id\_expr if the key is found.
If the key is not found, returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


**Examples**


**Retrieve a single attribute**



```
SELECT dictGet('ext_dict_test', 'c1', toUInt64(1)) AS val

```


```
1

```

**Multiple attributes**



```
SELECT
    dictGet('ext_dict_mult', ('c1','c2'), number + 1) AS val,
    toTypeName(val) AS type
FROM system.numbers
LIMIT 3;

```


```
┌─val─────┬─type───────────┐
│ (1,'1') │ Tuple(        ↴│
│         │↳    c1 UInt32,↴│
│         │↳    c2 String) │
│ (2,'2') │ Tuple(        ↴│
│         │↳    c1 UInt32,↴│
│         │↳    c2 String) │
│ (3,'3') │ Tuple(        ↴│
│         │↳    c1 UInt32,↴│
│         │↳    c2 String) │
└─────────┴────────────────┘

```

## dictGetAll[​](#dictGetAll "Direct link to dictGetAll")


Introduced in: v23\.5\.0


Converts a dictionary attribute value to `All` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetAll(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT
    'Mozilla/5.0 (Linux; Android 12; SM-G998B) Mobile Safari/537.36' AS user_agent,

    -- This will match ALL applicable patterns
    dictGetAll('regexp_tree', 'os_replacement', 'Mozilla/5.0 (Linux; Android 12; SM-G998B) Mobile Safari/537.36') AS all_matches,

    -- This returns only the first match
    dictGet('regexp_tree', 'os_replacement', 'Mozilla/5.0 (Linux; Android 12; SM-G998B) Mobile Safari/537.36') AS first_match;

```


```
┌─user_agent─────────────────────────────────────────────────────┬─all_matches─────────────────────────────┬─first_match─┐
│ Mozilla/5.0 (Linux; Android 12; SM-G998B) Mobile Safari/537.36 │ ['Android','Android','Android','Linux'] │ Android     │
└────────────────────────────────────────────────────────────────┴─────────────────────────────────────────┴─────────────┘

```

## dictGetChildren[​](#dictGetChildren "Direct link to dictGetChildren")


Introduced in: v21\.4\.0


Returns first\-level children as an array of indexes. It is the inverse transformation for [dictGetHierarchy](#dictGetHierarchy).


**Syntax**



```
dictGetChildren(dict_name, key)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `key` — Key to be checked. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the first\-level descendants for the key. [`Array(UInt64)`](/docs/sql-reference/data-types/array)


**Examples**


**Get the first\-level children of a dictionary**



```
SELECT dictGetChildren('hierarchical_dictionary', 2);

```


```
┌─dictGetChild⋯ionary', 2)─┐
│ [4,5]                    │
└──────────────────────────┘

```

## dictGetDate[​](#dictGetDate "Direct link to dictGetDate")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Date` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetDate(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetDate('all_types_dict', 'Date_value', 1)

```


```
┌─dictGetDate(⋯_value', 1)─┐
│               2020-01-01 │
└──────────────────────────┘

```

## dictGetDateOrDefault[​](#dictGetDateOrDefault "Direct link to dictGetDateOrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Date` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetDateOrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetDate('all_types_dict', 'Date_value', 1);

-- for key which does not exist, returns the provided default value
SELECT dictGetDateOrDefault('all_types_dict', 'Date_value', 999, toDate('1970-01-01'));

```


```
┌─dictGetDate(⋯_value', 1)─┐
│               2024-01-15 │
└──────────────────────────┘
┌─dictGetDateO⋯70-01-01'))─┐
│               1970-01-01 │
└──────────────────────────┘

```

## dictGetDateTime[​](#dictGetDateTime "Direct link to dictGetDateTime")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `DateTime` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetDateTime(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetDateTime('all_types_dict', 'DateTime_value', 1)

```


```
┌─dictGetDateT⋯_value', 1)─┐
│      2024-01-15 10:30:00 │
└──────────────────────────┘

```

## dictGetDateTimeOrDefault[​](#dictGetDateTimeOrDefault "Direct link to dictGetDateTimeOrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `DateTime` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetDateTimeOrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetDateTime('all_types_dict', 'DateTime_value', 1);

-- for key which does not exist, returns the provided default value
SELECT dictGetDateTimeOrDefault('all_types_dict', 'DateTime_value', 999, toDateTime('1970-01-01 00:00:00'));

```


```
┌─dictGetDateT⋯_value', 1)─┐
│      2024-01-15 10:30:00 │
└──────────────────────────┘
┌─dictGetDateT⋯0:00:00'))──┐
│      1970-01-01 00:00:00 │
└──────────────────────────┘

```

## dictGetDescendants[​](#dictGetDescendants "Direct link to dictGetDescendants")


Introduced in: v21\.4\.0


Returns all descendants as if the [`dictGetChildren`](#dictGetChildren) function were applied `level` times recursively.


**Syntax**



```
dictGetDescendants(dict_name, key, level)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `key` — Key to be checked. [`const String`](/docs/sql-reference/data-types/string)
- `level` — Key to be checked. Hierarchy level. If `level = 0` returns all descendants to the end. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the descendants for the key. [`Array(UInt64)`](/docs/sql-reference/data-types/array)


**Examples**


**Get the first\-level children of a dictionary**



```
-- consider the following hierarchical dictionary:
-- 0 (Root)
-- └── 1 (Level 1 - Node 1)
--     ├── 2 (Level 2 - Node 2)
--     │   ├── 4 (Level 3 - Node 4)
--     │   └── 5 (Level 3 - Node 5)
--     └── 3 (Level 2 - Node 3)
--         └── 6 (Level 3 - Node 6)

SELECT dictGetDescendants('hierarchical_dictionary', 0, 2)

```


```
┌─dictGetDesce⋯ary', 0, 2)─┐
│ [3,2]                    │
└──────────────────────────┘

```

## dictGetFloat32[​](#dictGetFloat32 "Direct link to dictGetFloat32")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Float32` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetFloat32(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetFloat32('all_types_dict', 'Float32_value', 1)

```


```
┌─dictGetFloat⋯_value', 1)─┐
│               -123.123   │
└──────────────────────────┘

```

## dictGetFloat32OrDefault[​](#dictGetFloat32OrDefault "Direct link to dictGetFloat32OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Float32` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetFloat32OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetFloat32('all_types_dict', 'Float32_value', 1);

-- for key which does not exist, returns the provided default value (-1.0)
SELECT dictGetFloat32OrDefault('all_types_dict', 'Float32_value', 999, -1.0);

```


```
┌─dictGetFloat⋯_value', 1)─┐
│                   123.45 │
└──────────────────────────┘
┌─dictGetFloat⋯e', 999, -1)─┐
│                       -1  │
└───────────────────────────┘

```

## dictGetFloat64[​](#dictGetFloat64 "Direct link to dictGetFloat64")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Float64` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetFloat64(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetFloat64('all_types_dict', 'Float64_value', 1)

```


```
┌─dictGetFloat⋯_value', 1)─┐
│                 -123.123 │
└──────────────────────────┘

```

## dictGetFloat64OrDefault[​](#dictGetFloat64OrDefault "Direct link to dictGetFloat64OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Float64` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetFloat64OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetFloat64('all_types_dict', 'Float64_value', 1);

-- for key which does not exist, returns the provided default value (nan)
SELECT dictGetFloat64OrDefault('all_types_dict', 'Float64_value', 999, nan);

```


```
┌─dictGetFloat⋯_value', 1)─┐
│            987654.123456 │
└──────────────────────────┘
┌─dictGetFloat⋯, 999, nan)─┐
│                      nan │
└──────────────────────────┘

```

## dictGetHierarchy[​](#dictGetHierarchy "Direct link to dictGetHierarchy")


Introduced in: v1\.1\.0


Creates an array, containing all the parents of a key in the [hierarchical dictionary](/docs/sql-reference/statements/create/dictionary/layouts/hierarchical#hierarchical-dictionaries).


**Syntax**



```
dictGetHierarchy(dict_name, key)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `key` — Key value. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns parents for the key. [`Array(UInt64)`](/docs/sql-reference/data-types/array)


**Examples**


**Get hierarchy for a key**



```
SELECT dictGetHierarchy('hierarchical_dictionary', 5)

```


```
┌─dictGetHiera⋯ionary', 5)─┐
│ [5,2,1]                  │
└──────────────────────────┘

```

## dictGetIPv4[​](#dictGetIPv4 "Direct link to dictGetIPv4")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `IPv4` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetIPv4(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetIPv4('all_types_dict', 'IPv4_value', 1)

```


```
┌─dictGetIPv4('all_⋯ 'IPv4_value', 1)─┐
│ 192.168.0.1                         │
└─────────────────────────────────────┘

```

## dictGetIPv4OrDefault[​](#dictGetIPv4OrDefault "Direct link to dictGetIPv4OrDefault")


Introduced in: v23\.1\.0


Converts a dictionary attribute value to `IPv4` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetIPv4OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetIPv4('all_types_dict', 'IPv4_value', 1);

-- for key which does not exist, returns the provided default value
SELECT dictGetIPv4OrDefault('all_types_dict', 'IPv4_value', 999, toIPv4('0.0.0.0'));

```


```
┌─dictGetIPv4('all_⋯ 'IPv4_value', 1)─┐
│ 192.168.0.1                         │
└─────────────────────────────────────┘
┌─dictGetIPv4OrDefa⋯0.0.0.0'))─┐
│ 0.0.0.0                      │
└──────────────────────────────┘

```

## dictGetIPv6[​](#dictGetIPv6 "Direct link to dictGetIPv6")


Introduced in: v23\.1\.0


Converts a dictionary attribute value to `IPv6` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetIPv6(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetIPv6('all_types_dict', 'IPv6_value', 1)

```


```
┌─dictGetIPv6('all_⋯ 'IPv6_value', 1)─┐
│ 2001:db8:85a3::8a2e:370:7334        │
└─────────────────────────────────────┘

```

## dictGetIPv6OrDefault[​](#dictGetIPv6OrDefault "Direct link to dictGetIPv6OrDefault")


Introduced in: v23\.1\.0


Converts a dictionary attribute value to `IPv6` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetIPv6OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetIPv6('all_types_dict', 'IPv6_value', 1);

-- for key which does not exist, returns the provided default value
SELECT dictGetIPv6OrDefault('all_types_dict', 'IPv6_value', 999, '::1'::IPv6);

```


```
┌─dictGetIPv6('all_⋯ 'IPv6_value', 1)─┐
│ 2001:db8:85a3::8a2e:370:7334        │
└─────────────────────────────────────┘
┌─dictGetIPv6OrDefa⋯:1'::IPv6)─┐
│ ::1                          │
└──────────────────────────────┘

```

## dictGetInt16[​](#dictGetInt16 "Direct link to dictGetInt16")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int16` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetInt16(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetInt16('all_types_dict', 'Int16_value', 1)

```


```
┌─dictGetInt16⋯_value', 1)─┐
│                    -5000 │
└──────────────────────────┘

```

## dictGetInt16OrDefault[​](#dictGetInt16OrDefault "Direct link to dictGetInt16OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int16` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetInt16OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetInt16('all_types_dict', 'Int16_value', 1);

-- for key which does not exist, returns the provided default value (-1)
SELECT dictGetInt16OrDefault('all_types_dict', 'Int16_value', 999, -1);

```


```
┌─dictGetInt16⋯_value', 1)─┐
│                    -5000 │
└──────────────────────────┘
┌─dictGetInt16⋯', 999, -1)─┐
│                       -1 │
└──────────────────────────┘

```

## dictGetInt32[​](#dictGetInt32 "Direct link to dictGetInt32")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int32` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetInt32(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetInt32('all_types_dict', 'Int32_value', 1)

```


```
┌─dictGetInt32⋯_value', 1)─┐
│                -1000000  │
└──────────────────────────┘

```

## dictGetInt32OrDefault[​](#dictGetInt32OrDefault "Direct link to dictGetInt32OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int32` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetInt32OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetInt32('all_types_dict', 'Int32_value', 1);

-- for key which does not exist, returns the provided default value (-1)
SELECT dictGetInt32OrDefault('all_types_dict', 'Int32_value', 999, -1);

```


```
┌─dictGetInt32⋯_value', 1)─┐
│                -1000000  │
└──────────────────────────┘
┌─dictGetInt32⋯', 999, -1)─┐
│                       -1 │
└──────────────────────────┘

```

## dictGetInt64[​](#dictGetInt64 "Direct link to dictGetInt64")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int64` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetInt64(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetInt64('all_types_dict', 'Int64_value', 1)

```


```
┌─dictGetInt64⋯_value', 1)───┐
│       -9223372036854775807 │
└────────────────────────────┘

```

## dictGetInt64OrDefault[​](#dictGetInt64OrDefault "Direct link to dictGetInt64OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int64` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetInt64OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetInt64('all_types_dict', 'Int64_value', 1);

-- for key which does not exist, returns the provided default value (-1)
SELECT dictGetInt64OrDefault('all_types_dict', 'Int64_value', 999, -1);

```


```
┌─dictGetInt64⋯_value', 1)─┐
│     -9223372036854775808 │
└──────────────────────────┘
┌─dictGetInt64⋯', 999, -1)─┐
│                       -1 │
└──────────────────────────┘

```

## dictGetInt8[​](#dictGetInt8 "Direct link to dictGetInt8")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int8` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetInt8(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetInt8('all_types_dict', 'Int8_value', 1)

```


```
┌─dictGetInt8(⋯_value', 1)─┐
│                     -100 │
└──────────────────────────┘

```

## dictGetInt8OrDefault[​](#dictGetInt8OrDefault "Direct link to dictGetInt8OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `Int8` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetInt8OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetInt8('all_types_dict', 'Int8_value', 1);

-- for key which does not exist, returns the provided default value (-1)
SELECT dictGetInt8OrDefault('all_types_dict', 'Int8_value', 999, -1);

```


```
┌─dictGetInt8(⋯_value', 1)─┐
│                     -100 │
└──────────────────────────┘
┌─dictGetInt8O⋯', 999, -1)─┐
│                       -1 │
└──────────────────────────┘

```

## dictGetKeys[​](#dictGetKeys "Direct link to dictGetKeys")


Introduced in: v25\.12\.0


Returns the dictionary key(s) whose attribute equals the specified value. This is the inverse of the function `dictGet` on a single attribute.


Use setting `max_reverse_dictionary_lookup_cache_size_bytes` to cap the size of the per\-query reverse\-lookup cache used by `dictGetKeys`.
The cache stores serialized key tuples for each attribute value to avoid re\-scanning the dictionary within the same query.
The cache is not persistent across queries. When the limit is reached, entries are evicted with LRU.
This is most effective with large dictionaries when the input has low cardinality and the working set fits in the cache. Set to `0` to disable caching.


**Syntax**



```
dictGetKeys('dict_name', 'attr_name', value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Attribute to match. [`String`](/docs/sql-reference/data-types/string)
- `value_expr` — Value to match against the attribute. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


For single key dictionaries: an array of keys whose attribute equals `value_expr`. For multi key dictionaries: an array of tuples of keys whose attribute equals `value_expr`. If there is no attribute corresponding to `value_expr` in the dictionary, then an empty array is returned. ClickHouse throws an exception if it cannot parse the value of the attribute or the value cannot be converted to the attribute data type.


**Examples**


**Sample usage**



```
SELECT dictGetKeys('task_id_to_priority_dictionary', 'priority_level', 'high') AS ids;

```


```
┌─ids───┐
│ [4,2] │
└───────┘

```

## dictGetOrDefault[​](#dictGetOrDefault "Direct link to dictGetOrDefault")


Introduced in: v18\.16\.0


Retrieves values from a dictionary, with a default value if the key is not found.


**Syntax**



```
dictGetOrDefault('dict_name', attr_names, id_expr, default_value)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_names` — Name of the column of the dictionary, or tuple of column names. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning UInt64/Tuple(T). [`UInt64`](/docs/sql-reference/data-types/int-uint) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value` — Default value to return if the key is not found. Type must match the attribute's data type.


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr` if the key is found.
If the key is not found, returns the `default_value` provided.


**Examples**


**Get value with default**



```
SELECT dictGetOrDefault('ext_dict_mult', 'c1', toUInt64(999), 0) AS val

```


```
0

```

## dictGetOrNull[​](#dictGetOrNull "Direct link to dictGetOrNull")


Introduced in: v21\.4\.0


Retrieves values from a dictionary, returning NULL if the key is not found.


**Syntax**



```
dictGetOrNull('dict_name', 'attr_name', id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. String literal. \- `attr_name` — Name of the column to retrieve. String literal. \- `id_expr` — Key value. Expression returning dictionary key\-type value.


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr` if the key is found.
If the key is not found, returns `NULL`.


**Examples**


**Example using the range key dictionary**



```
SELECT
    (number, toDate('2019-05-20')),
    dictGetOrNull('range_key_dictionary', 'value', number, toDate('2019-05-20')),
FROM system.numbers LIMIT 5 FORMAT TabSeparated;

```


```
(0,'2019-05-20')  \N
(1,'2019-05-20')  First
(2,'2019-05-20')  Second
(3,'2019-05-20')  Third
(4,'2019-05-20')  \N

```

## dictGetString[​](#dictGetString "Direct link to dictGetString")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `String` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetString(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetString('all_types_dict', 'String_value', 1)

```


```
┌─dictGetString(⋯_value', 1)─┐
│ test string                │
└────────────────────────────┘

```

## dictGetStringOrDefault[​](#dictGetStringOrDefault "Direct link to dictGetStringOrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `String` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetStringOrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetString('all_types_dict', 'String_value', 1);

-- for key which does not exist, returns the provided default value
SELECT dictGetStringOrDefault('all_types_dict', 'String_value', 999, 'default');

```


```
┌─dictGetString(⋯_value', 1)─┐
│ test string                │
└────────────────────────────┘
┌─dictGetStringO⋯ 999, 'default')─┐
│ default                         │
└─────────────────────────────────┘

```

## dictGetUInt16[​](#dictGetUInt16 "Direct link to dictGetUInt16")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt16` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetUInt16(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetUInt16('all_types_dict', 'UInt16_value', 1)

```


```
┌─dictGetUInt1⋯_value', 1)─┐
│                     5000 │
└──────────────────────────┘

```

## dictGetUInt16OrDefault[​](#dictGetUInt16OrDefault "Direct link to dictGetUInt16OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt16` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetUInt16OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetUInt16('all_types_dict', 'UInt16_value', 1);

-- for key which does not exist, returns the provided default value (0)
SELECT dictGetUInt16OrDefault('all_types_dict', 'UInt16_value', 999, 0);

```


```
┌─dictGetUInt1⋯_value', 1)─┐
│                     5000 │
└──────────────────────────┘
┌─dictGetUInt1⋯e', 999, 0)─┐
│                        0 │
└──────────────────────────┘

```

## dictGetUInt32[​](#dictGetUInt32 "Direct link to dictGetUInt32")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt32` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetUInt32(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetUInt32('all_types_dict', 'UInt32_value', 1)

```


```
┌─dictGetUInt3⋯_value', 1)─┐
│                  1000000 │
└──────────────────────────┘

```

## dictGetUInt32OrDefault[​](#dictGetUInt32OrDefault "Direct link to dictGetUInt32OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt32` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetUInt32OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetUInt32('all_types_dict', 'UInt32_value', 1);

-- for key which does not exist, returns the provided default value (0)
SELECT dictGetUInt32OrDefault('all_types_dict', 'UInt32_value', 999, 0);

```


```
┌─dictGetUInt3⋯_value', 1)─┐
│                  1000000 │
└──────────────────────────┘
┌─dictGetUInt3⋯e', 999, 0)─┐
│                        0 │
└──────────────────────────┘

```

## dictGetUInt64[​](#dictGetUInt64 "Direct link to dictGetUInt64")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt64` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetUInt64(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetUInt64('all_types_dict', 'UInt64_value', 1)

```


```
┌─dictGetUInt6⋯_value', 1)─┐
│      9223372036854775807 │
└──────────────────────────┘

```

## dictGetUInt64OrDefault[​](#dictGetUInt64OrDefault "Direct link to dictGetUInt64OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt64` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetUInt64OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetUInt64('all_types_dict', 'UInt64_value', 1);

-- for key which does not exist, returns the provideddefault value (0)
SELECT dictGetUInt64OrDefault('all_types_dict', 'UInt64_value', 999, 0);

```


```
┌─dictGetUInt6⋯_value', 1)─┐
│      9223372036854775807 │
└──────────────────────────┘
┌─dictGetUInt6⋯e', 999, 0)─┐
│                        0 │
└──────────────────────────┘

```

## dictGetUInt8[​](#dictGetUInt8 "Direct link to dictGetUInt8")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt8` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetUInt8(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetUInt8('all_types_dict', 'UInt8_value', 1)

```


```
┌─dictGetUInt8⋯_value', 1)─┐
│                      100 │
└──────────────────────────┘

```

## dictGetUInt8OrDefault[​](#dictGetUInt8OrDefault "Direct link to dictGetUInt8OrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UInt8` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetUInt8OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetUInt8('all_types_dict', 'UInt8_value', 1);

-- for key which does not exist, returns the provided default value (0)
SELECT dictGetUInt8OrDefault('all_types_dict', 'UInt8_value', 999, 0);

```


```
┌─dictGetUInt8⋯_value', 1)─┐
│                      100 │
└──────────────────────────┘
┌─dictGetUInt8⋯e', 999, 0)─┐
│                        0 │
└──────────────────────────┘

```

## dictGetUUID[​](#dictGetUUID "Direct link to dictGetUUID")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UUID` data type regardless of the dictionary configuration.


**Syntax**



```
dictGetUUID(dict_name, attr_name, id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
SELECT dictGetUUID('all_types_dict', 'UUID_value', 1)

```


```
┌─dictGetUUID(⋯_value', 1)─────────────┐
│ 123e4567-e89b-12d3-a456-426614174000 │
└──────────────────────────────────────┘

```

## dictGetUUIDOrDefault[​](#dictGetUUIDOrDefault "Direct link to dictGetUUIDOrDefault")


Introduced in: v1\.1\.0


Converts a dictionary attribute value to `UUID` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.


**Syntax**



```
dictGetUUIDOrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.


NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.


**Examples**


**Usage example**



```
-- for key which exists
SELECT dictGetUUID('all_types_dict', 'UUID_value', 1);

-- for key which does not exist, returns the provided default value
SELECT dictGetUUIDOrDefault('all_types_dict', 'UUID_value', 999, '00000000-0000-0000-0000-000000000000'::UUID);

```


```
┌─dictGetUUID('all_t⋯ 'UUID_value', 1)─┐
│ 550e8400-e29b-41d4-a716-446655440000 │
└──────────────────────────────────────┘
┌─dictGetUUIDOrDefa⋯000000000000'::UUID)─┐
│ 00000000-0000-0000-0000-000000000000   │
└────────────────────────────────────────┘

```

## dictHas[​](#dictHas "Direct link to dictHas")


Introduced in: v1\.1\.0


Checks whether a key is present in a dictionary.


**Syntax**



```
dictHas('dict_name', id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `id_expr` — Key value [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the key exists, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Check for the existence of a key in a dictionary**



```
-- consider the following hierarchical dictionary:
-- 0 (Root)
-- └── 1 (Level 1 - Node 1)
--     ├── 2 (Level 2 - Node 2)
--     │   ├── 4 (Level 3 - Node 4)
--     │   └── 5 (Level 3 - Node 5)
--     └── 3 (Level 2 - Node 3)
--         └── 6 (Level 3 - Node 6)

SELECT dictHas('hierarchical_dictionary', 2);
SELECT dictHas('hierarchical_dictionary', 7);

```


```
┌─dictHas('hie⋯ionary', 2)─┐
│                        1 │
└──────────────────────────┘
┌─dictHas('hie⋯ionary', 7)─┐
│                        0 │
└──────────────────────────┘

```

## dictIsIn[​](#dictIsIn "Direct link to dictIsIn")


Introduced in: v1\.1\.0


Checks the ancestor of a key through the whole hierarchical chain in the dictionary.


**Syntax**



```
dictIsIn(dict_name, child_id_expr, ancestor_id_expr)

```

**Arguments**


- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `child_id_expr` — Key to be checked. [`String`](/docs/sql-reference/data-types/string)
- `ancestor_id_expr` — Alleged ancestor of the `child_id_expr` key. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `0` if `child_id_expr` is not a child of `ancestor_id_expr`, `1` if `child_id_expr` is a child of `ancestor_id_expr` or if `child_id_expr` is an `ancestor_id_expr`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Check hierarchical relationship**



```
-- valid hierarchy
SELECT dictIsIn('hierarchical_dictionary', 6, 3)

-- invalid hierarchy
SELECT dictIsIn('hierarchical_dictionary', 3, 5)

```


```
┌─dictIsIn('hi⋯ary', 6, 3)─┐
│                        1 │
└──────────────────────────┘
┌─dictIsIn('hi⋯ary', 3, 5)─┐
│                        0 │
└──────────────────────────┘

```
[PreviousEncryption](/docs/sql-reference/functions/encryption-functions)[NextFiles](/docs/sql-reference/functions/files)- [Example dictionaries](#example-dictionary)- [dictGet](#dictGet)- [dictGetAll](#dictGetAll)- [dictGetChildren](#dictGetChildren)- [dictGetDate](#dictGetDate)- [dictGetDateOrDefault](#dictGetDateOrDefault)- [dictGetDateTime](#dictGetDateTime)- [dictGetDateTimeOrDefault](#dictGetDateTimeOrDefault)- [dictGetDescendants](#dictGetDescendants)- [dictGetFloat32](#dictGetFloat32)- [dictGetFloat32OrDefault](#dictGetFloat32OrDefault)- [dictGetFloat64](#dictGetFloat64)- [dictGetFloat64OrDefault](#dictGetFloat64OrDefault)- [dictGetHierarchy](#dictGetHierarchy)- [dictGetIPv4](#dictGetIPv4)- [dictGetIPv4OrDefault](#dictGetIPv4OrDefault)- [dictGetIPv6](#dictGetIPv6)- [dictGetIPv6OrDefault](#dictGetIPv6OrDefault)- [dictGetInt16](#dictGetInt16)- [dictGetInt16OrDefault](#dictGetInt16OrDefault)- [dictGetInt32](#dictGetInt32)- [dictGetInt32OrDefault](#dictGetInt32OrDefault)- [dictGetInt64](#dictGetInt64)- [dictGetInt64OrDefault](#dictGetInt64OrDefault)- [dictGetInt8](#dictGetInt8)- [dictGetInt8OrDefault](#dictGetInt8OrDefault)- [dictGetKeys](#dictGetKeys)- [dictGetOrDefault](#dictGetOrDefault)- [dictGetOrNull](#dictGetOrNull)- [dictGetString](#dictGetString)- [dictGetStringOrDefault](#dictGetStringOrDefault)- [dictGetUInt16](#dictGetUInt16)- [dictGetUInt16OrDefault](#dictGetUInt16OrDefault)- [dictGetUInt32](#dictGetUInt32)- [dictGetUInt32OrDefault](#dictGetUInt32OrDefault)- [dictGetUInt64](#dictGetUInt64)- [dictGetUInt64OrDefault](#dictGetUInt64OrDefault)- [dictGetUInt8](#dictGetUInt8)- [dictGetUInt8OrDefault](#dictGetUInt8OrDefault)- [dictGetUUID](#dictGetUUID)- [dictGetUUIDOrDefault](#dictGetUUIDOrDefault)- [dictHas](#dictHas)- [dictIsIn](#dictIsIn)
Was this page helpful?

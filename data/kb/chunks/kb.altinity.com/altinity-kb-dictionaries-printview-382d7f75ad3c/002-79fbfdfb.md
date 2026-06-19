---
source: kb.altinity.com
url: https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup34/clickhouse\_integration.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup34/clickhouse_integration.pdf
topic: dictionaries-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '99.0000'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 10
---

│ ['str0','str66','str132','str198','str264'] │ │ 42 │ [0,42,84,126,168] │ ['str0','str42','str84','str126','str168'] │ └─────┴────────────────────┴─────────────────────────────────────────────┘ SELECT dictGet('pg_arr_dict', 'array_int', toUInt64(42)) AS res_int, dictGetOrDefault('pg_arr_dict', 'array_str', toUInt64(424242), ['none']) AS res_str ┌─res_int───────────┬─res_str──┐ │ [0,42,84,126,168] │ ['none'] │ └───────────────────┴──────────┘ ``` ## Dictionary with MySQL as a source

### Test data in MySQL

```
-- casted into CH Arrays

create table arr_src(
   _key bigint(20) NOT NULL, 
   _array_int text, 
   _array_str text, 
   PRIMARY KEY(_key)
);

INSERT INTO arr_src VALUES 
  (42, '[0,42,84,126,168]','[''str0'',''str42'',''str84'',''str126'',''str168'']'),
  (66, '[0,66,132,198,264]','[''str0'',''str66'',''str132'',''str198'',''str264'']');

```
### Dictionary in MySQL

```
-- supporting table to cast data
CREATE TABLE arr_src
(
    `_key` UInt8,
    `_array_int` String,
    `array_int` Array(Int32) ALIAS cast(_array_int, 'Array(Int32)'),
    `_array_str` String,
    `array_str` Array(String) ALIAS cast(_array_str, 'Array(String)')
)
ENGINE = MySQL('mysql_host', 'ch', 'arr_src', 'ch', 'pass');

-- dictionary fetches data from the supporting table
CREATE DICTIONARY mysql_arr_dict
(
    _key UInt64,
    array_int Array(Int64) DEFAULT [1,2,3],
    array_str Array(String) DEFAULT ['1','2','3']
)
PRIMARY KEY _key
SOURCE(CLICKHOUSE(DATABASE 'default' TABLE 'arr_src'))
LIFETIME(120)
LAYOUT(HASHED());


select * from mysql_arr_dict;
┌─_key─┬─array_int──────────┬─array_str───────────────────────────────────┐
│   66 │ [0,66,132,198,264] │ ['str0','str66','str132','str198','str264'] │
│   42 │ [0,42,84,126,168]  │ ['str0','str42','str84','str126','str168']  │
└──────┴────────────────────┴─────────────────────────────────────────────┘


SELECT
    dictGet('mysql_arr_dict', 'array_int', toUInt64(42)) AS res_int,
    dictGetOrDefault('mysql_arr_dict', 'array_str', toUInt64(424242), ['none']) AS res_str

┌─res_int───────────┬─res_str──┐
│ [0,42,84,126,168] │ ['none'] │
└───────────────────┴──────────┘

SELECT
    dictGet('mysql_arr_dict', 'array_int', toUInt64(66)) AS res_int,
    dictGetOrDefault('mysql_arr_dict', 'array_str', toUInt64(66), ['none']) AS res_str

┌─res_int────────────┬─res_str─────────────────────────────────────┐
│ [0,66,132,198,264] │ ['str0','str66','str132','str198','str264'] │
└────────────────────┴─────────────────────────────────────────────┘

```
# 2 \- Dictionary on the top of several tables using VIEW

Dictionary on the top of several tables using VIEW
```

DROP TABLE IF EXISTS dictionary_source_en;
DROP TABLE IF EXISTS dictionary_source_ru;
DROP TABLE IF EXISTS dictionary_source_view;
DROP DICTIONARY IF EXISTS flat_dictionary;

CREATE TABLE dictionary_source_en
(
    id UInt64,
    value String
) ENGINE = TinyLog;

INSERT INTO dictionary_source_en VALUES (1, 'One'), (2,'Two'), (3, 'Three');

CREATE TABLE dictionary_source_ru
(
    id UInt64,
    value String
) ENGINE = TinyLog;

INSERT INTO dictionary_source_ru VALUES (1, 'Один'), (2,'Два'), (3, 'Три');

CREATE VIEW dictionary_source_view AS  SELECT id, dictionary_source_en.value as value_en, dictionary_source_ru.value as value_ru  FROM  dictionary_source_en LEFT JOIN dictionary_source_ru USING (id);

select * from dictionary_source_view;

CREATE DICTIONARY flat_dictionary
(
    id UInt64,
    value_en String,
    value_ru String
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' PASSWORD '' TABLE 'dictionary_source_view'))
LIFETIME(MIN 1 MAX 1000)
LAYOUT(FLAT());

SELECT
    dictGet(concat(currentDatabase(), '.flat_dictionary'), 'value_en', number + 1),
    dictGet(concat(currentDatabase(), '.flat_dictionary'), 'value_ru', number + 1)
FROM numbers(3);

```
# 3 \- Dimension table design

Dimension table design## Dimension table design considerations

### Choosing storage Engine

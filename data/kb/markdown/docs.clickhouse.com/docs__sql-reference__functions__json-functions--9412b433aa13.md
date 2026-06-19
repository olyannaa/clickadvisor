# JSON Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- JSON
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/json-functions.md)# JSON Functions

## Types of JSON functions[​](#types-of-functions "Direct link to Types of JSON functions")


There are two sets of functions to parse JSON:


- [`simpleJSON*` (`visitParam*`)](#simplejson-visitparam-functions) which is made for parsing a limited subset of JSON extremely fast.
- [`JSONExtract*`](#jsonextract-functions) which is made for parsing ordinary JSON.


### simpleJSON (visitParam) functions[​](#simplejson-visitparam-functions "Direct link to simpleJSON (visitParam) functions")


ClickHouse has special functions for working with simplified JSON. All these JSON functions are based on strong assumptions about what the JSON can be. They try to do as little as possible to get the job done as quickly as possible.


The following assumptions are made:


1. The field name (function argument) must be a constant.
2. The field name is somehow canonically encoded in JSON. For example: `simpleJSONHas('{"abc":"def"}', 'abc') = 1`, but `simpleJSONHas('{"\\u0061\\u0062\\u0063":"def"}', 'abc') = 0`
3. Fields are searched for on any nesting level, indiscriminately. If there are multiple matching fields, the first occurrence is used.
4. The JSON does not have space characters outside of string literals.


### JSONExtract functions[​](#jsonextract-functions "Direct link to JSONExtract functions")


These functions are based on [simdjson](https://github.com/lemire/simdjson), and designed for more complex JSON parsing requirements.


### Case\-Insensitive JSONExtract Functions[​](#case-insensitive-jsonextract-functions "Direct link to Case-Insensitive JSONExtract Functions")


These functions perform ASCII case\-insensitive key matching when extracting values from JSON objects.
They work identically to their case\-sensitive counterparts, except that object keys are matched without regard to case.
When multiple keys match with different cases, the first match is returned.


NoteThese functions may be less performant than their case\-sensitive counterparts, so use the regular JSONExtract functions if possible.


## JSONAllPaths[​](#JSONAllPaths "Direct link to JSONAllPaths")


Introduced in: v24\.8\.0


Returns the list of all paths stored in each row in JSON column.


**Syntax**



```
JSONAllPaths(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns an array of all paths in the JSON column. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json" : {"a" : 42}}, {"json" : {"b" : "Hello"}}, {"json" : {"a" : [1, 2, 3], "c" : "2020-01-01"}}
SELECT json, JSONAllPaths(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONAllPaths(json)─┐
│ {"a":"42"}                           │ ['a']              │
│ {"b":"Hello"}                        │ ['b']              │
│ {"a":["1","2","3"],"c":"2020-01-01"} │ ['a','c']          │
└──────────────────────────────────────┴────────────────────┘

```

## JSONAllPathsWithTypes[​](#JSONAllPathsWithTypes "Direct link to JSONAllPathsWithTypes")


Introduced in: v24\.8\.0


Returns the list of all paths and their data types stored in each row in JSON column.


**Syntax**



```
JSONAllPathsWithTypes(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns a map of all paths and their data types in the JSON column. [`Map(String, String)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json" : {"a" : 42}}, {"json" : {"b" : "Hello"}}, {"json" : {"a" : [1, 2, 3], "c" : "2020-01-01"}}
SELECT json, JSONAllPathsWithTypes(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONAllPathsWithTypes(json)───────────────┐
│ {"a":"42"}                           │ {'a':'Int64'}                             │
│ {"b":"Hello"}                        │ {'b':'String'}                            │
│ {"a":["1","2","3"],"c":"2020-01-01"} │ {'a':'Array(Nullable(Int64))','c':'Date'} │
└──────────────────────────────────────┴───────────────────────────────────────────┘

```

## JSONAllValues[​](#JSONAllValues "Direct link to JSONAllValues")


Introduced in: v26\.4\.0


Returns all values from each row in a JSON column as an array of strings.
Values are serialized in their text representation and ordered by their path names.


**Syntax**



```
JSONAllValues(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns an array of all values as strings in the JSON column. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json": {"a": 42}}, {"json": {"b": "Hello"}}, {"json": {"a": [1, 2, 3], "c": "2020-01-01"}}
SELECT json, JSONAllValues(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONAllValues(json)──────┐
│ {"a":42}                             │ ['42']                   │
│ {"b":"Hello"}                        │ ['Hello']                │
│ {"a":[1,2,3],"c":"2020-01-01"}       │ ['[1,2,3]','2020-01-01'] │
└──────────────────────────────────────┴──────────────────────────┘

```

## JSONArrayLength[​](#JSONArrayLength "Direct link to JSONArrayLength")


Introduced in: v23\.2\.0


Returns the number of elements in the outermost JSON array.
The function returns `NULL` if input JSON string is invalid.


**Syntax**



```
JSONArrayLength(json)

```

**Aliases**: `JSON_ARRAY_LENGTH`


**Arguments**


- `json` — String with valid JSON. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number of array elements if `json` is a valid JSON array string, otherwise returns `NULL`. [`Nullable(UInt64)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT
    JSONArrayLength(''),
    JSONArrayLength('[1,2,3]');

```


```
┌─JSONArrayLength('')─┬─JSONArrayLength('[1,2,3]')─┐
│                ᴺᵁᴸᴸ │                          3 │
└─────────────────────┴────────────────────────────┘

```

## JSONDynamicPaths[​](#JSONDynamicPaths "Direct link to JSONDynamicPaths")


Introduced in: v24\.8\.0


Returns the list of dynamic paths that are stored as separate subcolumns in JSON column.


**Syntax**



```
JSONDynamicPaths(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns an array of dynamic paths in the JSON column. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json" : {"a" : 42}}, {"json" : {"b" : "Hello"}}, {"json" : {"a" : [1, 2, 3], "c" : "2020-01-01"}}
SELECT json, JSONDynamicPaths(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONDynamicPaths(json)─┐
│ {"a":"42"}                           │ ['a']                  │
│ {"b":"Hello"}                        │ []                     │
│ {"a":["1","2","3"],"c":"2020-01-01"} │ ['a']                  │
└──────────────────────────────────────┴────────────────────────┘

```

## JSONDynamicPathsWithTypes[​](#JSONDynamicPathsWithTypes "Direct link to JSONDynamicPathsWithTypes")


Introduced in: v24\.8\.0


Returns the list of dynamic paths that are stored as separate subcolumns and their types in each row in JSON column.


**Syntax**



```
JSONDynamicPathsWithTypes(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns a map of dynamic paths and their data types in the JSON column. [`Map(String, String)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json" : {"a" : 42}}, {"json" : {"b" : "Hello"}}, {"json" : {"a" : [1, 2, 3], "c" : "2020-01-01"}}
SELECT json, JSONDynamicPathsWithTypes(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONDynamicPathsWithTypes(json)─┐
│ {"a":"42"}                           │ {'a':'Int64'}                   │
│ {"b":"Hello"}                        │ {}                              │
│ {"a":["1","2","3"],"c":"2020-01-01"} │ {'a':'Array(Nullable(Int64))'}  │
└──────────────────────────────────────┴─────────────────────────────────┘

```

## JSONExtract[​](#JSONExtract "Direct link to JSONExtract")


Introduced in: v19\.14\.0


Parses JSON and extracts a value with given ClickHouse data type.


**Syntax**



```
JSONExtract(json[, indices_or_keys, ...], return_type)

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `return_type` — ClickHouse data type to return. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of specified ClickHouse data type if possible, otherwise returns the default value for that type.


**Examples**


**Usage example**



```
SELECT JSONExtract('{"a": "hello", "b": [-100, 200.0, 300]}', 'Tuple(String, Array(Float64))') AS res;

```


```
┌─res──────────────────────────────┐
│ ('hello',[-100,200,300])         │
└──────────────────────────────────┘

```

## JSONExtractArrayRaw[​](#JSONExtractArrayRaw "Direct link to JSONExtractArrayRaw")


Introduced in: v20\.1\.0


Returns an array with elements of JSON array, each represented as unparsed string.


**Syntax**



```
JSONExtractArrayRaw(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of strings with JSON array elements. If the part is not an array or does not exist, an empty array will be returned. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT JSONExtractArrayRaw('{"a": "hello", "b": [-100, 200.0, "hello"]}', 'b') AS res;

```


```
┌─res──────────────────────────┐
│ ['-100','200.0','"hello"']   │
└──────────────────────────────┘

```

## JSONExtractArrayRawCaseInsensitive[​](#JSONExtractArrayRawCaseInsensitive "Direct link to JSONExtractArrayRawCaseInsensitive")


Introduced in: v25\.8\.0


Returns an array with elements of JSON array, each represented as unparsed string, using case\-insensitive key matching. This function is similar to [`JSONExtractArrayRaw`](#JSONExtractArrayRaw).


**Syntax**



```
JSONExtractArrayRawCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the array. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of raw JSON strings. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**basic**



```
SELECT JSONExtractArrayRawCaseInsensitive('{"Items": [1, 2, 3]}', 'ITEMS')

```


```
['1','2','3']

```

## JSONExtractBool[​](#JSONExtractBool "Direct link to JSONExtractBool")


Introduced in: v20\.1\.0


Parses JSON and extracts a value of Bool type.


**Syntax**



```
JSONExtractBool(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Bool value if it exists, otherwise returns `0`. [`Bool`](/docs/sql-reference/data-types/boolean)


**Examples**


**Usage example**



```
SELECT JSONExtractBool('{"passed": true}', 'passed') AS res;

```


```
┌─res─┐
│   1 │
└─────┘

```

## JSONExtractBoolCaseInsensitive[​](#JSONExtractBoolCaseInsensitive "Direct link to JSONExtractBoolCaseInsensitive")


Introduced in: v25\.8\.0


Parses JSON and extracts a boolean value using case\-insensitive key matching. This function is similar to [`JSONExtractBool`](#JSONExtractBool).


**Syntax**



```
JSONExtractBoolCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the extracted boolean value (1 for true, 0 for false), 0 if not found. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**basic**



```
SELECT JSONExtractBoolCaseInsensitive('{"IsActive": true}', 'isactive')

```


```
1

```

## JSONExtractCaseInsensitive[​](#JSONExtractCaseInsensitive "Direct link to JSONExtractCaseInsensitive")


Introduced in: v25\.8\.0


Parses JSON and extracts a value of the given ClickHouse data type using case\-insensitive key matching. This function is similar to [`JSONExtract`](#JSONExtract).


**Syntax**



```
JSONExtractCaseInsensitive(json [, indices_or_keys...], return_type)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `return_type` — The ClickHouse data type to extract [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the extracted value in the specified data type. [`Any`](/docs/sql-reference/data-types)


**Examples**


**int\_type**



```
SELECT JSONExtractCaseInsensitive('{"Number": 123}', 'number', 'Int32')

```


```
123

```

**array\_type**



```
SELECT JSONExtractCaseInsensitive('{"List": [1, 2, 3]}', 'list', 'Array(Int32)')

```


```
[1,2,3]

```

## JSONExtractFloat[​](#JSONExtractFloat "Direct link to JSONExtractFloat")


Introduced in: v20\.1\.0


Parses JSON and extracts a value of Float type.


**Syntax**



```
JSONExtractFloat(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Float value if it exists, otherwise returns `0`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT JSONExtractFloat('{"a": "hello", "b": [-100, 200.0, 300]}', 'b', 2) AS res;

```


```
┌─res─┐
│ 200 │
└─────┘

```

## JSONExtractFloatCaseInsensitive[​](#JSONExtractFloatCaseInsensitive "Direct link to JSONExtractFloatCaseInsensitive")


Introduced in: v25\.8\.0


Parses JSON and extracts a value of Float type using case\-insensitive key matching. This function is similar to [`JSONExtractFloat`](#JSONExtractFloat).


**Syntax**



```
JSONExtractFloatCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the extracted Float value, 0 if not found or cannot be converted. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**basic**



```
SELECT JSONExtractFloatCaseInsensitive('{"Price": 12.34}', 'PRICE')

```


```
12.34

```

## JSONExtractInt[​](#JSONExtractInt "Direct link to JSONExtractInt")


Introduced in: v20\.1\.0


Parses JSON and extracts a value of Int type.


**Syntax**



```
JSONExtractInt(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an Int value if it exists, otherwise returns `0`. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT JSONExtractInt('{"a": "hello", "b": [-100, 200.0, 300]}', 'b', 1) AS res;

```


```
┌──res─┐
│ -100 │
└──────┘

```

## JSONExtractIntCaseInsensitive[​](#JSONExtractIntCaseInsensitive "Direct link to JSONExtractIntCaseInsensitive")


Introduced in: v25\.8\.0


Parses JSON and extracts a value of Int type using case\-insensitive key matching. This function is similar to [`JSONExtractInt`](#JSONExtractInt).


**Syntax**



```
JSONExtractIntCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the extracted Int value, 0 if not found or cannot be converted. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**basic**



```
SELECT JSONExtractIntCaseInsensitive('{"Value": 123}', 'value')

```


```
123

```

**nested**



```
SELECT JSONExtractIntCaseInsensitive('{"DATA": {"COUNT": 42}}', 'data', 'Count')

```


```
42

```

## JSONExtractKeys[​](#JSONExtractKeys "Direct link to JSONExtractKeys")


Introduced in: v21\.11\.0


Parses a JSON string and extracts the keys.


**Syntax**



```
JSONExtractKeys(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array with the keys of the JSON object. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT JSONExtractKeys('{"a": "hello", "b": [-100, 200.0, 300]}') AS res;

```


```
┌─res─────────┐
│ ['a','b']   │
└─────────────┘

```

## JSONExtractKeysAndValues[​](#JSONExtractKeysAndValues "Direct link to JSONExtractKeysAndValues")


Introduced in: v20\.1\.0


Parses key\-value pairs from a JSON where the values are of the given ClickHouse data type.


**Syntax**



```
JSONExtractKeysAndValues(json[, indices_or_keys, ...], value_type)

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `value_type` — ClickHouse data type of the values. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array of tuples with the parsed key\-value pairs. [`Array(Tuple(String, value_type))`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT JSONExtractKeysAndValues('{"x": {"a": 5, "b": 7, "c": 11}}', 'Int8', 'x') AS res;

```


```
┌─res────────────────────┐
│ [('a',5),('b',7),('c',11)] │
└────────────────────────┘

```

## JSONExtractKeysAndValuesCaseInsensitive[​](#JSONExtractKeysAndValuesCaseInsensitive "Direct link to JSONExtractKeysAndValuesCaseInsensitive")


Introduced in: v25\.8\.0


Parses key\-value pairs from JSON using case\-insensitive key matching. This function is similar to [`JSONExtractKeysAndValues`](#JSONExtractKeysAndValues).


**Syntax**



```
JSONExtractKeysAndValuesCaseInsensitive(json [, indices_or_keys...], value_type)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the object. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `value_type` — The ClickHouse data type of the values [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array of tuples containing key\-value pairs. [`Array(Tuple(String, T))`](/docs/sql-reference/data-types/array)


**Examples**


**basic**



```
SELECT JSONExtractKeysAndValuesCaseInsensitive('{"Name": "Alice", "AGE": 30}', 'String')

```


```
[('Name','Alice'),('AGE','30')]

```

## JSONExtractKeysAndValuesRaw[​](#JSONExtractKeysAndValuesRaw "Direct link to JSONExtractKeysAndValuesRaw")


Introduced in: v20\.4\.0


Returns an array of tuples with keys and values from a JSON object. All values are represented as unparsed strings.


**Syntax**



```
JSONExtractKeysAndValuesRaw(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of tuples with parsed key\-value pairs where values are unparsed strings. [`Array(Tuple(String, String))`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT JSONExtractKeysAndValuesRaw('{"a": [-100, 200.0], "b": "hello"}') AS res;

```


```
┌─res──────────────────────────────────┐
│ [('a','[-100,200.0]'),('b','"hello"')] │
└──────────────────────────────────────┘

```

## JSONExtractKeysAndValuesRawCaseInsensitive[​](#JSONExtractKeysAndValuesRawCaseInsensitive "Direct link to JSONExtractKeysAndValuesRawCaseInsensitive")


Introduced in: v25\.8\.0


Extracts raw key\-value pairs from JSON using case\-insensitive key matching. This function is similar to [`JSONExtractKeysAndValuesRaw`](#JSONExtractKeysAndValuesRaw).


**Syntax**



```
JSONExtractKeysAndValuesRawCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the object. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of tuples containing key\-value pairs as raw strings. [`Array(Tuple(String, String))`](/docs/sql-reference/data-types/array)


**Examples**


**basic**



```
SELECT JSONExtractKeysAndValuesRawCaseInsensitive('{"Name": "Alice", "AGE": 30}')

```


```
[('Name','"Alice"'),('AGE','30')]

```

## JSONExtractKeysCaseInsensitive[​](#JSONExtractKeysCaseInsensitive "Direct link to JSONExtractKeysCaseInsensitive")


Introduced in: v25\.8\.0


Parses a JSON string and extracts the keys using case\-insensitive key matching to navigate to nested objects. This function is similar to [`JSONExtractKeys`](#JSONExtractKeys).


**Syntax**



```
JSONExtractKeysCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the object. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of keys from the JSON object. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**basic**



```
SELECT JSONExtractKeysCaseInsensitive('{"Name": "Alice", "AGE": 30}')

```


```
['Name','AGE']

```

**nested**



```
SELECT JSONExtractKeysCaseInsensitive('{"User": {"name": "John", "AGE": 25}}', 'user')

```


```
['name','AGE']

```

## JSONExtractRaw[​](#JSONExtractRaw "Direct link to JSONExtractRaw")


Introduced in: v20\.1\.0


Returns a part of JSON as unparsed string.


**Syntax**



```
JSONExtractRaw(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the part of JSON as an unparsed string. If the part does not exist or has a wrong type, an empty string will be returned. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT JSONExtractRaw('{"a": "hello", "b": [-100, 200.0, 300]}', 'b') AS res;

```


```
┌─res──────────────┐
│ [-100,200.0,300] │
└──────────────────┘

```

## JSONExtractRawCaseInsensitive[​](#JSONExtractRawCaseInsensitive "Direct link to JSONExtractRawCaseInsensitive")


Introduced in: v25\.8\.0


Returns part of the JSON as an unparsed string using case\-insensitive key matching. This function is similar to [`JSONExtractRaw`](#JSONExtractRaw).


**Syntax**



```
JSONExtractRawCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the raw JSON string of the extracted element. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**object**



```
SELECT JSONExtractRawCaseInsensitive('{"Object": {"key": "value"}}', 'OBJECT')

```


```
{"key":"value"}

```

## JSONExtractString[​](#JSONExtractString "Direct link to JSONExtractString")


Introduced in: v20\.1\.0


Parses JSON and extracts a value of String type.


**Syntax**



```
JSONExtractString(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a String value if it exists, otherwise returns an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT JSONExtractString('{"a": "hello", "b": [-100, 200.0, 300]}', 'a') AS res;

```


```
┌─res───┐
│ hello │
└───────┘

```

## JSONExtractStringCaseInsensitive[​](#JSONExtractStringCaseInsensitive "Direct link to JSONExtractStringCaseInsensitive")


Introduced in: v25\.8\.0


Parses JSON and extracts a string using case\-insensitive key matching. This function is similar to [`JSONExtractString`](#JSONExtractString).


**Syntax**



```
JSONExtractStringCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the extracted string value, empty string if not found. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**basic**



```
SELECT JSONExtractStringCaseInsensitive('{"ABC": "def"}', 'abc')

```


```
def

```

**nested**



```
SELECT JSONExtractStringCaseInsensitive('{"User": {"Name": "John"}}', 'user', 'name')

```


```
John

```

## JSONExtractUInt[​](#JSONExtractUInt "Direct link to JSONExtractUInt")


Introduced in: v20\.1\.0


Parses JSON and extracts a value of UInt type.


**Syntax**



```
JSONExtractUInt(json [, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — A list of zero or more arguments each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a UInt value if it exists, otherwise returns `0`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT JSONExtractUInt('{"a": "hello", "b": [-100, 200.0, 300]}', 'b', -1) AS res;

```


```
┌─res─┐
│ 300 │
└─────┘

```

## JSONExtractUIntCaseInsensitive[​](#JSONExtractUIntCaseInsensitive "Direct link to JSONExtractUIntCaseInsensitive")


Introduced in: v25\.8\.0


Parses JSON and extracts a value of UInt type using case\-insensitive key matching. This function is similar to [`JSONExtractUInt`](#JSONExtractUInt).


**Syntax**



```
JSONExtractUIntCaseInsensitive(json [, indices_or_keys]...)

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional. Indices or keys to navigate to the field. Keys use case\-insensitive matching [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the extracted UInt value, 0 if not found or cannot be converted. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**basic**



```
SELECT JSONExtractUIntCaseInsensitive('{"COUNT": 789}', 'count')

```


```
789

```

## JSONHas[​](#JSONHas "Direct link to JSONHas")


Introduced in: v20\.1\.0


Checks for the existence of the provided value(s) in the JSON document.


**Syntax**



```
JSONHas(json[ ,indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `[ ,indices_or_keys, ...]` — A list of zero or more arguments. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns `1` if the value exists in `json`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 'b') = 1;
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 'b', 4) = 0;

```


```
1
0

```

## JSONKey[​](#JSONKey "Direct link to JSONKey")


Introduced in: v20\.1\.0


Returns the key of a JSON object field by its index (1\-based). If the JSON is passed as a string, it is parsed first. The second argument is a JSON path to navigate into nested objects. The function returns the key name at the specified position.


**Syntax**



```
JSONKey(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional list of indices or keys specifying a path to a nested element. Each argument can be either a string (access by key) or an integer (access by index starting from 1\). [`String`](/docs/sql-reference/data-types/string) or [`Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the key name at the specified position in the JSON object. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT JSONKey('{"a": "hello", "b": [-100, 200.0, 300]}', 1);

```


```
a

```

## JSONLength[​](#JSONLength "Direct link to JSONLength")


Introduced in: v20\.1\.0


Return the length of a JSON array or a JSON object.
If the value does not exist or has the wrong type, `0` will be returned.


**Syntax**



```
JSONLength(json [, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `[, indices_or_keys, ...]` — Optional. A list of zero or more arguments. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the length of the JSON array or JSON object, otherwise returns `0` if the value does not exist or has the wrong type. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT JSONLength('{"a": "hello", "b": [-100, 200.0, 300]}', 'b') = 3;
SELECT JSONLength('{"a": "hello", "b": [-100, 200.0, 300]}') = 2;

```


```
1
1

```

## JSONMergePatch[​](#JSONMergePatch "Direct link to JSONMergePatch")


Introduced in: v23\.10\.0


Returns the merged JSON object string which is formed by merging multiple JSON objects.


**Syntax**



```
JSONMergePatch(json1[, json2, ...])

```

**Aliases**: `jsonMergePatch`


**Arguments**


- `json1[, json2, ...]` — One or more strings with valid JSON. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the merged JSON object string, if the JSON object strings are valid. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT JSONMergePatch('{"a":1}', '{"name": "joey"}', '{"name": "tom"}', '{"name": "zoey"}') AS res;

```


```
┌─res───────────────────┐
│ {"a":1,"name":"zoey"} │
└───────────────────────┘

```

## JSONSharedDataPaths[​](#JSONSharedDataPaths "Direct link to JSONSharedDataPaths")


Introduced in: v24\.8\.0


Returns the list of paths that are stored in shared data structure in JSON column.


**Syntax**



```
JSONSharedDataPaths(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns an array of paths stored in shared data structure in the JSON column. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json" : {"a" : 42}}, {"json" : {"b" : "Hello"}}, {"json" : {"a" : [1, 2, 3], "c" : "2020-01-01"}}
SELECT json, JSONSharedDataPaths(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONSharedDataPaths(json)─┐
│ {"a":"42"}                           │ []                        │
│ {"b":"Hello"}                        │ ['b']                     │
│ {"a":["1","2","3"],"c":"2020-01-01"} │ ['c']                     │
└──────────────────────────────────────┴───────────────────────────┘

```

## JSONSharedDataPathsWithTypes[​](#JSONSharedDataPathsWithTypes "Direct link to JSONSharedDataPathsWithTypes")


Introduced in: v24\.8\.0


Returns the list of paths that are stored in shared data structure and their types in each row in JSON column.


**Syntax**



```
JSONSharedDataPathsWithTypes(json)

```

**Arguments**


- `json` — JSON column. [`JSON`](/docs/sql-reference/data-types/newjson)


**Returned value**


Returns a map of paths stored in shared data structure and their data types in the JSON column. [`Map(String, String)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
CREATE TABLE test (json JSON(max_dynamic_paths=1)) ENGINE = Memory;
INSERT INTO test FORMAT JSONEachRow {"json" : {"a" : 42}}, {"json" : {"b" : "Hello"}}, {"json" : {"a" : [1, 2, 3], "c" : "2020-01-01"}}
SELECT json, JSONSharedDataPathsWithTypes(json) FROM test;

```


```
┌─json─────────────────────────────────┬─JSONSharedDataPathsWithTypes(json)─┐
│ {"a":"42"}                           │ {}                                  │
│ {"b":"Hello"}                        │ {'b':'String'}                      │
│ {"a":["1","2","3"],"c":"2020-01-01"} │ {'c':'Date'}                        │
└──────────────────────────────────────┴─────────────────────────────────────┘

```

## JSONType[​](#JSONType "Direct link to JSONType")


Introduced in: v20\.1\.0


Return the type of a JSON value. If the value does not exist, `Null=0` will be returned.


**Syntax**



```
JSONType(json[, indices_or_keys, ...])

```

**Arguments**


- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `json[, indices_or_keys, ...]` — A list of zero or more arguments, each of which can be either string or integer. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the type of a JSON value as a string, otherwise if the value doesn't exist it returns `Null=0` [`Enum`](/docs/sql-reference/data-types/enum)


**Examples**


**Usage example**



```
SELECT JSONType('{"a": "hello", "b": [-100, 200.0, 300]}') = 'Object';
SELECT JSONType('{"a": "hello", "b": [-100, 200.0, 300]}', 'a') = 'String';
SELECT JSONType('{"a": "hello", "b": [-100, 200.0, 300]}', 'b') = 'Array';

```


```
1
1
1

```

## JSON\_EXISTS[​](#JSON_EXISTS "Direct link to JSON_EXISTS")


Introduced in: v21\.8\.0


If the value exists in the JSON document, `1` will be returned.
If the value does not exist, `0` will be returned.


**Syntax**



```
JSON_EXISTS(json, path)

```

**Arguments**


- `json` — A string with valid JSON. [`String`](/docs/sql-reference/data-types/string)
- `path` — A string representing the path. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the value exists in the JSON document, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT JSON_EXISTS('{"hello":1}', '$.hello');
SELECT JSON_EXISTS('{"hello":{"world":1}}', '$.hello.world');
SELECT JSON_EXISTS('{"hello":["world"]}', '$.hello[*]');
SELECT JSON_EXISTS('{"hello":["world"]}', '$.hello[0]');

```


```
┌─JSON_EXISTS(⋯ '$.hello')─┐
│                        1 │
└──────────────────────────┘
┌─JSON_EXISTS(⋯llo.world')─┐
│                        1 │
└──────────────────────────┘
┌─JSON_EXISTS(⋯.hello[*]')─┐
│                        1 │
└──────────────────────────┘
┌─JSON_EXISTS(⋯.hello[0]')─┐
│                        1 │
└──────────────────────────┘

```

## JSON\_QUERY[​](#JSON_QUERY "Direct link to JSON_QUERY")


Introduced in: v21\.8\.0


Parses a JSON and extract a value as a JSON array or JSON object.
If the value does not exist, an empty string will be returned.


**Syntax**



```
JSON_QUERY(json, path)

```

**Arguments**


- `json` — A string with valid JSON. [`String`](/docs/sql-reference/data-types/string)
- `path` — A string representing the path. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the extracted JSON array or JSON object as a string, or an empty string if the value does not exist. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT JSON_QUERY('{"hello":"world"}', '$.hello');
SELECT JSON_QUERY('{"array":[[0, 1, 2, 3, 4, 5], [0, -1, -2, -3, -4, -5]]}', '$.array[*][0 to 2, 4]');
SELECT JSON_QUERY('{"hello":2}', '$.hello');
SELECT toTypeName(JSON_QUERY('{"hello":2}', '$.hello'));

```


```
["world"]
[0, 1, 4, 0, -1, -4]
[2]
String

```

## JSON\_VALUE[​](#JSON_VALUE "Direct link to JSON_VALUE")


Introduced in: v21\.11\.0


Parses a JSON and extract a value as a JSON scalar. If the value does not exist, an empty string will be returned by default.


This function is controlled by the following settings:


- by SET `function_json_value_return_type_allow_nullable` \= `true`, `NULL` will be returned. If the value is complex type (such as: struct, array, map), an empty string will be returned by default.
- by SET `function_json_value_return_type_allow_complex` \= `true`, the complex value will be returned.


**Syntax**



```
JSON_VALUE(json, path)

```

**Arguments**


- `json` — A string with valid JSON. [`String`](/docs/sql-reference/data-types/string)
- `path` — A string representing the path. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the extracted JSON scalar as a string, or an empty string if the value does not exist. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT JSON_VALUE('{"hello":"world"}', '$.hello');
SELECT JSON_VALUE('{"array":[[0, 1, 2, 3, 4, 5], [0, -1, -2, -3, -4, -5]]}', '$.array[*][0 to 2, 4]');
SELECT JSON_VALUE('{"hello":2}', '$.hello');
SELECT JSON_VALUE('{"hello":"world"}', '$.b') settings function_json_value_return_type_allow_nullable=true;

```


```
world
0
2
ᴺᵁᴸᴸ

```

## dynamicElement[​](#dynamicElement "Direct link to dynamicElement")


Introduced in: v24\.1\.0


Extracts a column with specified type from a `Dynamic` column.


This function allows you to extract values of a specific type from a Dynamic column. If a row contains a value
of the requested type, it returns that value. If the row contains a different type or NULL, it returns NULL
for scalar types or an empty array for array types.


**Syntax**



```
dynamicElement(dynamic, type_name)

```

**Arguments**


- `dynamic` — Dynamic column to extract from. [`Dynamic`](/docs/sql-reference/data-types/dynamic)
- `type_name` — The name of the variant type to extract (e.g., 'String', 'Int64', 'Array(Int64\)').


**Returned value**


Returns values of the specified type from the Dynamic column. Returns NULL for non\-matching types (or empty array for array types). [`Any`](/docs/sql-reference/data-types)


**Examples**


**Extracting different types from Dynamic column**



```
CREATE TABLE test (d Dynamic) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('Hello, World!'), ([1, 2, 3]);
SELECT d, dynamicType(d), dynamicElement(d, 'String'), dynamicElement(d, 'Int64'), dynamicElement(d, 'Array(Int64)'), dynamicElement(d, 'Date'), dynamicElement(d, 'Array(String)') FROM test

```


```
┌─d─────────────┬─dynamicType(d)─┬─dynamicElement(d, 'String')─┬─dynamicElement(d, 'Int64')─┬─dynamicElement(d, 'Array(Int64)')─┬─dynamicElement(d, 'Date')─┬─dynamicElement(d, 'Array(String)')─┐
│ ᴺᵁᴸᴸ          │ None           │ ᴺᵁᴸᴸ                        │                       ᴺᵁᴸᴸ │ []                                │                      ᴺᵁᴸᴸ │ []                                 │
│ 42            │ Int64          │ ᴺᵁᴸᴸ                        │                         42 │ []                                │                      ᴺᵁᴸᴸ │ []                                 │
│ Hello, World! │ String         │ Hello, World!               │                       ᴺᵁᴸᴸ │ []                                │                      ᴺᵁᴸᴸ │ []                                 │
│ [1,2,3]       │ Array(Int64)   │ ᴺᵁᴸᴸ                        │                       ᴺᵁᴸᴸ │ [1,2,3]                           │                      ᴺᵁᴸᴸ │ []                                 │
└───────────────┴────────────────┴─────────────────────────────┴────────────────────────────┴───────────────────────────────────┴───────────────────────────┴────────────────────────────────────┘

```

## dynamicType[​](#dynamicType "Direct link to dynamicType")


Introduced in: v24\.1\.0


Returns the variant type name for each row of a `Dynamic` column.


For rows containing NULL, the function returns 'None'. For all other rows, it returns the actual data type
stored in that row of the Dynamic column (e.g., 'Int64', 'String', 'Array(Int64\)').


**Syntax**



```
dynamicType(dynamic)

```

**Arguments**


- `dynamic` — Dynamic column to inspect. [`Dynamic`](/docs/sql-reference/data-types/dynamic)


**Returned value**


Returns the type name of the value stored in each row, or 'None' for NULL values. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Inspecting types in Dynamic column**



```
CREATE TABLE test (d Dynamic) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('Hello, World!'), ([1, 2, 3]);
SELECT d, dynamicType(d) FROM test;

```


```
┌─d─────────────┬─dynamicType(d)─┐
│ ᴺᵁᴸᴸ          │ None           │
│ 42            │ Int64          │
│ Hello, World! │ String         │
│ [1,2,3]       │ Array(Int64)   │
└───────────────┴────────────────┘

```

## isDynamicElementInSharedData[​](#isDynamicElementInSharedData "Direct link to isDynamicElementInSharedData")


Introduced in: v24\.1\.0


Returns true for rows in a Dynamic column that are stored in shared variant format rather than as separate subcolumns.


When a Dynamic column has a `max_types` limit, values that exceed this limit are stored in a shared binary format
instead of being separated into individual typed subcolumns. This function identifies which rows are stored in this shared format.


**Syntax**



```
isDynamicElementInSharedData(dynamic)

```

**Arguments**


- `dynamic` — Dynamic column to inspect. [`Dynamic`](/docs/sql-reference/data-types/dynamic)


**Returned value**


Returns true if the value is stored in shared variant format, false if stored as a separate subcolumn or is NULL. [`Bool`](/docs/sql-reference/data-types/boolean)


**Examples**


**Checking storage format in Dynamic column with max\_types limit**



```
CREATE TABLE test (d Dynamic(max_types=2)) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('Hello, World!'), ([1, 2, 3]);
SELECT d, isDynamicElementInSharedData(d) FROM test;

```


```
┌─d─────────────┬─isDynamicElementInSharedData(d)─┐
│ ᴺᵁᴸᴸ          │ false                           │
│ 42            │ false                           │
│ Hello, World! │ true                            │
│ [1,2,3]       │ true                            │
└───────────────┴─────────────────────────────────┘

```

## isValidJSON[​](#isValidJSON "Direct link to isValidJSON")


Introduced in: v20\.1\.0


Checks that the string passed is valid JSON.


**Syntax**



```
isValidJSON(json)

```

**Arguments**


- `json` — JSON string to validate [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the string is valid JSON, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT isValidJSON('{"a": "hello", "b": [-100, 200.0, 300]}') = 1;
SELECT isValidJSON('not JSON') = 0;

```


```
1
0

```

**Using integers to access both JSON arrays and JSON objects**



```
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 0);
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 1);
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 2);
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', -1);
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', -2);
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 3);

```


```
0
1
1
1
1
1
0

```

## prettyPrintJSON[​](#prettyPrintJSON "Direct link to prettyPrintJSON")


Introduced in: v26\.4\.0


Returns a pretty\-printed version of a JSON string with newlines and indentation with spaces.


**Syntax**



```
prettyPrintJSON(json [, indent])

```

**Arguments**


- `json` — A valid JSON string to format. [`String`](/docs/sql-reference/data-types/string)
- `indent` — Number of spaces per indentation level. Default: 4\. Max: 32 [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


A pretty\-printed JSON string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Simple object**



```
SELECT prettyPrintJSON('{"a":1,"b":"hello"}');

```


```
{
    "a": 1,
    "b": "hello"
}

```

**Custom indent**



```
SELECT prettyPrintJSON('{"a":1}', 8);

```


```
{
        "a": 1
}

```

## simpleJSONExtractBool[​](#simpleJSONExtractBool "Direct link to simpleJSONExtractBool")


Introduced in: v21\.4\.0


Parses a true/false value from the value of the field named `field_name`.
The result is `UInt8`.


**Syntax**



```
simpleJSONExtractBool(json, field_name)

```

**Aliases**: `visitParamExtractBool`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the value of the field is `true`, `0` otherwise. This means this function will return `0` including (and not only) in the following cases:


- If the field doesn't exists.
- If the field contains `true` as a string, e.g.: `{"field":"true"}`.
- If the field contains `1` as a numerical value. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":false,"bar":true}');
INSERT INTO jsons VALUES ('{"foo":"true","qux":1}');

SELECT simpleJSONExtractBool(json, 'bar') FROM jsons ORDER BY json;
SELECT simpleJSONExtractBool(json, 'foo') FROM jsons ORDER BY json;

```


```
0
1
0
0

```

## simpleJSONExtractFloat[​](#simpleJSONExtractFloat "Direct link to simpleJSONExtractFloat")


Introduced in: v21\.4\.0


Parses `Float64` from the value of the field named `field_name`.
If `field_name` is a string field, it tries to parse a number from the beginning of the string.
If the field does not exist, or it exists but does not contain a number, it returns `0`.


**Syntax**



```
simpleJSONExtractFloat(json, field_name)

```

**Aliases**: `visitParamExtractFloat`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number parsed from the field if the field exists and contains a number, otherwise `0`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":"-4e3"}');
INSERT INTO jsons VALUES ('{"foo":-3.4}');
INSERT INTO jsons VALUES ('{"foo":5}');
INSERT INTO jsons VALUES ('{"foo":"not1number"}');
INSERT INTO jsons VALUES ('{"baz":2}');

SELECT simpleJSONExtractFloat(json, 'foo') FROM jsons ORDER BY json;

```


```
0
-4000
0
-3.4
5

```

## simpleJSONExtractInt[​](#simpleJSONExtractInt "Direct link to simpleJSONExtractInt")


Introduced in: v21\.4\.0


Parses `Int64` from the value of the field named `field_name`.
If `field_name` is a string field, it tries to parse a number from the beginning of the string.
If the field does not exist, or it exists but does not contain a number, it returns `0`.


**Syntax**



```
simpleJSONExtractInt(json, field_name)

```

**Aliases**: `visitParamExtractInt`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number parsed from the field if the field exists and contains a number, `0` otherwise [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":"-4e3"}');
INSERT INTO jsons VALUES ('{"foo":-3.4}');
INSERT INTO jsons VALUES ('{"foo":5}');
INSERT INTO jsons VALUES ('{"foo":"not1number"}');
INSERT INTO jsons VALUES ('{"baz":2}');

SELECT simpleJSONExtractInt(json, 'foo') FROM jsons ORDER BY json;

```


```
0
-4
0
-3
5

```

## simpleJSONExtractRaw[​](#simpleJSONExtractRaw "Direct link to simpleJSONExtractRaw")


Introduced in: v21\.4\.0


Returns the value of the field named `field_name` as a `String`, including separators.


**Syntax**



```
simpleJSONExtractRaw(json, field_name)

```

**Aliases**: `visitParamExtractRaw`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the value of the field as a string, including separators if the field exists, or an empty string otherwise [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":"-4e3"}');
INSERT INTO jsons VALUES ('{"foo":-3.4}');
INSERT INTO jsons VALUES ('{"foo":5}');
INSERT INTO jsons VALUES ('{"foo":{"def":[1,2,3]}}');
INSERT INTO jsons VALUES ('{"baz":2}');

SELECT simpleJSONExtractRaw(json, 'foo') FROM jsons ORDER BY json;

```


```
"-4e3"
-3.4
5
{"def":[1,2,3]}

```

## simpleJSONExtractString[​](#simpleJSONExtractString "Direct link to simpleJSONExtractString")


Introduced in: v21\.4\.0


Parses `String` in double quotes from the value of the field named `field_name`.


**Implementation details**


There is currently no support for code points in the format `\uXXXX\uYYYY` that are not from the basic multilingual plane (they are converted to CESU\-8 instead of UTF\-8\).


**Syntax**



```
simpleJSONExtractString(json, field_name)

```

**Aliases**: `visitParamExtractString`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the unescaped value of a field as a string, including separators. An empty string is returned if the field doesn't contain a double quoted string, if unescaping fails or if the field doesn't exist [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":"\\n\\u0000"}');
INSERT INTO jsons VALUES ('{"foo":"\\u263"}');
INSERT INTO jsons VALUES ('{"foo":"\\u263a"}');
INSERT INTO jsons VALUES ('{"foo":"hello}');

SELECT simpleJSONExtractString(json, 'foo') FROM jsons ORDER BY json;

```


```
\n\0

☺

```

## simpleJSONExtractUInt[​](#simpleJSONExtractUInt "Direct link to simpleJSONExtractUInt")


Introduced in: v21\.4\.0


Parses `UInt64` from the value of the field named `field_name`.
If `field_name` is a string field, it tries to parse a number from the beginning of the string.
If the field does not exist, or it exists but does not contain a number, it returns `0`.


**Syntax**



```
simpleJSONExtractUInt(json, field_name)

```

**Aliases**: `visitParamExtractUInt`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number parsed from the field if the field exists and contains a number, `0` otherwise [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":"4e3"}');
INSERT INTO jsons VALUES ('{"foo":3.4}');
INSERT INTO jsons VALUES ('{"foo":5}');
INSERT INTO jsons VALUES ('{"foo":"not1number"}');
INSERT INTO jsons VALUES ('{"baz":2}');

SELECT simpleJSONExtractUInt(json, 'foo') FROM jsons ORDER BY json;

```


```
0
4
0
3
5

```

## simpleJSONHas[​](#simpleJSONHas "Direct link to simpleJSONHas")


Introduced in: v21\.4\.0


Checks whether there is a field named `field_name`.


**Syntax**



```
simpleJSONHas(json, field_name)

```

**Aliases**: `visitParamHas`


**Arguments**


- `json` — The JSON in which the field is searched for. [`String`](/docs/sql-reference/data-types/string)
- `field_name` — The name of the field to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the field exists, `0` otherwise [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE jsons
(
    `json` String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO jsons VALUES ('{"foo":"true","qux":1}');

SELECT simpleJSONHas(json, 'foo') FROM jsons;
SELECT simpleJSONHas(json, 'bar') FROM jsons;

```


```
1
0

```

## toJSONString[​](#toJSONString "Direct link to toJSONString")


Introduced in: v21\.7\.0


Serializes a value to its JSON representation. Various data types and nested structures are supported.
64\-bit [integers](/docs/sql-reference/data-types/int-uint) or bigger (like `UInt64` or `Int128`) are enclosed in quotes by default. [output\_format\_json\_quote\_64bit\_integers](/docs/operations/settings/formats#output_format_json_quote_64bit_integers) controls this behavior.
Special values `NaN` and `inf` are replaced with `null`. Enable [output\_format\_json\_quote\_denormals](/docs/operations/settings/formats#output_format_json_quote_denormals) setting to show them.
When serializing an [Enum](/docs/sql-reference/data-types/enum) value, the function outputs its name.


See also:


- [output\_format\_json\_quote\_64bit\_integers](/docs/operations/settings/formats#output_format_json_quote_64bit_integers)
- [output\_format\_json\_quote\_denormals](/docs/operations/settings/formats#output_format_json_quote_denormals)


**Syntax**



```
toJSONString(value)

```

**Arguments**


- `value` — Value to serialize. Value may be of any data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the JSON representation of the value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Map serialization**



```
SELECT toJSONString(map('key1', 1, 'key2', 2));

```


```
┌─toJSONString(map('key1', 1, 'key2', 2))─┐
│ {"key1":1,"key2":2}                     │
└─────────────────────────────────────────┘

```

**Special values**



```
SELECT toJSONString(tuple(1.25, NULL, NaN, +inf, -inf, [])) SETTINGS output_format_json_quote_denormals = 1;

```


```
┌─toJSONString(tuple(1.25, NULL, NaN, plus(inf), minus(inf), []))─┐
│ [1.25,null,"nan","inf","-inf",[]]                               │
└─────────────────────────────────────────────────────────────────┘

```
[PreviousIP Addresses](/docs/sql-reference/functions/ip-address-functions)[NextLogical](/docs/sql-reference/functions/logical-functions)- [Types of JSON functions](#types-of-functions)
	- [simpleJSON (visitParam) functions](#simplejson-visitparam-functions)- [JSONExtract functions](#jsonextract-functions)- [Case\-Insensitive JSONExtract Functions](#case-insensitive-jsonextract-functions)- [JSONAllPaths](#JSONAllPaths)- [JSONAllPathsWithTypes](#JSONAllPathsWithTypes)- [JSONAllValues](#JSONAllValues)- [JSONArrayLength](#JSONArrayLength)- [JSONDynamicPaths](#JSONDynamicPaths)- [JSONDynamicPathsWithTypes](#JSONDynamicPathsWithTypes)- [JSONExtract](#JSONExtract)- [JSONExtractArrayRaw](#JSONExtractArrayRaw)- [JSONExtractArrayRawCaseInsensitive](#JSONExtractArrayRawCaseInsensitive)- [JSONExtractBool](#JSONExtractBool)- [JSONExtractBoolCaseInsensitive](#JSONExtractBoolCaseInsensitive)- [JSONExtractCaseInsensitive](#JSONExtractCaseInsensitive)- [JSONExtractFloat](#JSONExtractFloat)- [JSONExtractFloatCaseInsensitive](#JSONExtractFloatCaseInsensitive)- [JSONExtractInt](#JSONExtractInt)- [JSONExtractIntCaseInsensitive](#JSONExtractIntCaseInsensitive)- [JSONExtractKeys](#JSONExtractKeys)- [JSONExtractKeysAndValues](#JSONExtractKeysAndValues)- [JSONExtractKeysAndValuesCaseInsensitive](#JSONExtractKeysAndValuesCaseInsensitive)- [JSONExtractKeysAndValuesRaw](#JSONExtractKeysAndValuesRaw)- [JSONExtractKeysAndValuesRawCaseInsensitive](#JSONExtractKeysAndValuesRawCaseInsensitive)- [JSONExtractKeysCaseInsensitive](#JSONExtractKeysCaseInsensitive)- [JSONExtractRaw](#JSONExtractRaw)- [JSONExtractRawCaseInsensitive](#JSONExtractRawCaseInsensitive)- [JSONExtractString](#JSONExtractString)- [JSONExtractStringCaseInsensitive](#JSONExtractStringCaseInsensitive)- [JSONExtractUInt](#JSONExtractUInt)- [JSONExtractUIntCaseInsensitive](#JSONExtractUIntCaseInsensitive)- [JSONHas](#JSONHas)- [JSONKey](#JSONKey)- [JSONLength](#JSONLength)- [JSONMergePatch](#JSONMergePatch)- [JSONSharedDataPaths](#JSONSharedDataPaths)- [JSONSharedDataPathsWithTypes](#JSONSharedDataPathsWithTypes)- [JSONType](#JSONType)- [JSON\_EXISTS](#JSON_EXISTS)- [JSON\_QUERY](#JSON_QUERY)- [JSON\_VALUE](#JSON_VALUE)- [dynamicElement](#dynamicElement)- [dynamicType](#dynamicType)- [isDynamicElementInSharedData](#isDynamicElementInSharedData)- [isValidJSON](#isValidJSON)- [prettyPrintJSON](#prettyPrintJSON)- [simpleJSONExtractBool](#simpleJSONExtractBool)- [simpleJSONExtractFloat](#simpleJSONExtractFloat)- [simpleJSONExtractInt](#simpleJSONExtractInt)- [simpleJSONExtractRaw](#simpleJSONExtractRaw)- [simpleJSONExtractString](#simpleJSONExtractString)- [simpleJSONExtractUInt](#simpleJSONExtractUInt)- [simpleJSONHas](#simpleJSONHas)- [toJSONString](#toJSONString)
Was this page helpful?

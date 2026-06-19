# Map functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Maps
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/tuple-map-functions.md)# Map functions

## extractKeyValuePairs[​](#extractKeyValuePairs "Direct link to extractKeyValuePairs")


Introduced in: v23\.4\.0


Extracts key\-value pairs from any string. The string does not need to be 100% structured in a key value pair format;


It can contain noise (e.g. log files). The key\-value pair format to be interpreted should be specified via function arguments.


A key\-value pair consists of a key followed by a `key_value_delimiter` and a value. Quoted keys and values are also supported. Key value pairs must be separated by pair delimiters.


**Syntax**



```
extractKeyValuePairs(data, [key_value_delimiter], [pair_delimiter], [quoting_character])

```

**Arguments**


- `data` \- String to extract key\-value pairs from. [String](/docs/sql-reference/data-types/string) or [FixedString](/docs/sql-reference/data-types/fixedstring).
- `key_value_delimiter` \- Character to be used as delimiter between the key and the value. Defaults to `:`. [String](/docs/sql-reference/data-types/string) or [FixedString](/docs/sql-reference/data-types/fixedstring).
- `pair_delimiters` \- Set of character to be used as delimiters between pairs. Defaults to `\space`, `,` and `;`. [String](/docs/sql-reference/data-types/string) or [FixedString](/docs/sql-reference/data-types/fixedstring).
- `quoting_character` \- Character to be used as quoting character. Defaults to `"`. [String](/docs/sql-reference/data-types/string) or [FixedString](/docs/sql-reference/data-types/fixedstring).
- `unexpected_quoting_character_strategy` \- Strategy to handle quoting characters in unexpected places during `read_key` and `read_value` phase. Possible values: `invalid`, `accept` and `promote`. Invalid will discard key/value and transition back to `WAITING_KEY` state. Accept will treat it as a normal character. Promote will transition to `READ_QUOTED_{KEY/VALUE}` state and start from next character. The default value is `INVALID`


**Returned values**


- The extracted key\-value pairs in a Map(String, String).


**Examples**


Query:


**Simple case**



```
arthur :) select extractKeyValuePairs('name:neymar, age:31 team:psg,nationality:brazil') as kv

SELECT extractKeyValuePairs('name:neymar, age:31 team:psg,nationality:brazil') as kv

Query id: f9e0ca6f-3178-4ee2-aa2c-a5517abb9cee

┌─kv──────────────────────────────────────────────────────────────────────┐
│ {'name':'neymar','age':'31','team':'psg','nationality':'brazil'}        │
└─────────────────────────────────────────────────────────────────────────┘

```

**Single quote as quoting character**



```
arthur :) select extractKeyValuePairs('name:\'neymar\';\'age\':31;team:psg;nationality:brazil,last_key:last_value', ':', ';,', '\'') as kv

SELECT extractKeyValuePairs('name:\'neymar\';\'age\':31;team:psg;nationality:brazil,last_key:last_value', ':', ';,', '\'') as kv

Query id: 0e22bf6b-9844-414a-99dc-32bf647abd5e

┌─kv───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ {'name':'neymar','age':'31','team':'psg','nationality':'brazil','last_key':'last_value'}                                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

unexpected\_quoting\_character\_strategy examples:


unexpected\_quoting\_character\_strategy\=invalid



```
SELECT extractKeyValuePairs('name"abc:5', ':', ' ,;', '\"', 'INVALID') as kv;

```


```
┌─kv────────────────┐
│ {'abc':'5'}  │
└───────────────────┘

```


```
SELECT extractKeyValuePairs('name"abc":5', ':', ' ,;', '\"', 'INVALID') as kv;

```


```
┌─kv──┐
│ {}  │
└─────┘

```

unexpected\_quoting\_character\_strategy\=accept



```
SELECT extractKeyValuePairs('name"abc:5', ':', ' ,;', '\"', 'ACCEPT') as kv;

```


```
┌─kv────────────────┐
│ {'name"abc':'5'}  │
└───────────────────┘

```


```
SELECT extractKeyValuePairs('name"abc":5', ':', ' ,;', '\"', 'ACCEPT') as kv;

```


```
┌─kv─────────────────┐
│ {'name"abc"':'5'}  │
└────────────────────┘

```

unexpected\_quoting\_character\_strategy\=promote



```
SELECT extractKeyValuePairs('name"abc:5', ':', ' ,;', '\"', 'PROMOTE') as kv;

```


```
┌─kv──┐
│ {}  │
└─────┘

```


```
SELECT extractKeyValuePairs('name"abc":5', ':', ' ,;', '\"', 'PROMOTE') as kv;

```


```
┌─kv───────────┐
│ {'abc':'5'}  │
└──────────────┘

```

**Escape sequences without escape sequences support**



```
arthur :) select extractKeyValuePairs('age:a\\x0A\\n\\0') as kv

SELECT extractKeyValuePairs('age:a\\x0A\\n\\0') AS kv

Query id: e9fd26ee-b41f-4a11-b17f-25af6fd5d356

┌─kv────────────────────┐
│ {'age':'a\\x0A\\n\\0'} │
└───────────────────────┘

```

**Syntax**



```
extractKeyValuePairs(input)

```

**Aliases**: `str_to_map`, `mapFromString`


**Arguments**


- None.


**Returned value**


**Examples**


## extractKeyValuePairsWithEscaping[​](#extractKeyValuePairsWithEscaping "Direct link to extractKeyValuePairsWithEscaping")


Introduced in: v23\.4\.0


Same as `extractKeyValuePairs` but with escaping support.


Escape sequences supported: `\x`, `\N`, `\a`, `\b`, `\e`, `\f`, `\n`, `\r`, `\t`, `\v` and `\0`.
Non standard escape sequences are returned as it is (including the backslash) unless they are one of the following:
`\\`, `'`, `"`, `backtick`, `/`, `=` or ASCII control characters (`c <= 31`).


This function will satisfy the use case where pre\-escaping and post\-escaping are not suitable. For instance, consider the following
input string: `a: "aaaa\"bbb"`. The expected output is: `a: aaaa\"bbbb`.


- Pre\-escaping: Pre\-escaping it will output: `a: "aaaa"bbb"` and `extractKeyValuePairs` will then output: `a: aaaa`
- Post\-escaping: `extractKeyValuePairs` will output `a: aaaa\` and post\-escaping will keep it as it is.


Leading escape sequences will be skipped in keys and will be considered invalid for values.


**Escape sequences with escape sequence support turned on**



```
arthur :) select extractKeyValuePairsWithEscaping('age:a\\x0A\\n\\0') as kv

SELECT extractKeyValuePairsWithEscaping('age:a\\x0A\\n\\0') AS kv

Query id: 44c114f0-5658-4c75-ab87-4574de3a1645

┌─kv───────────────┐
│ {'age':'a\n\n\0'} │
└──────────────────┘

```

**Syntax**



```
extractKeyValuePairsWithEscaping(input)

```

**Arguments**


- None.


**Returned value**


**Examples**


## map[​](#map "Direct link to map")


Introduced in: v21\.1\.0


Creates a value of type `Map(key, value)` from key\-value pairs.


**Syntax**



```
map(key1, value1[, key2, value2, ...])

```

**Arguments**


- `key_n` — The keys of the map entries. [`Any`](/docs/sql-reference/data-types)
- `value_n` — The values of the map entries. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a map containing key:value pairs. [`Map(Any, Any)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT map('key1', number, 'key2', number * 2) FROM numbers(3)

```


```
{'key1':0,'key2':0}
{'key1':1,'key2':2}
{'key1':2,'key2':4}

```

## mapAdd[​](#mapAdd "Direct link to mapAdd")


Introduced in: v20\.7\.0


Collect all the keys and sum corresponding values.


**Syntax**



```
mapAdd(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — Maps or tuples of two arrays in which items in the first array represent keys, and the second array contains values for each key. [`Map(K, V)`](/docs/sql-reference/data-types/map) or [`Tuple(Array(T), Array(T))`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a map or returns a tuple, where the first array contains the sorted keys and the second array contains values. [`Map(K, V)`](/docs/sql-reference/data-types/map) or [`Tuple(Array(T), Array(T))`](/docs/sql-reference/data-types/tuple)


**Examples**


**With Map type**



```
SELECT mapAdd(map(1, 1), map(1, 1))

```


```
{1:2}

```

**With tuple**



```
SELECT mapAdd(([toUInt8(1), 2], [1, 1]), ([toUInt8(1), 2], [1, 1]))

```


```
([1, 2], [2, 2])

```

## mapAll[​](#mapAll "Direct link to mapAll")


Introduced in: v23\.4\.0


Tests whether a condition holds for all key\-value pairs in a map.
`mapAll` is a higher\-order function.
You can pass a lambda function to it as the first argument.


**Syntax**



```
mapAll([func,] map)

```

**Arguments**


- `func` — Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `map` — Map to check. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns `1` if all key\-value pairs satisfy the condition, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT mapAll((k, v) -> v = 1, map('k1', 1, 'k2', 2))

```


```
0

```

## mapApply[​](#mapApply "Direct link to mapApply")


Introduced in: v22\.3\.0


Applies a function to each element of a map.


**Syntax**



```
mapApply(func, map)

```

**Arguments**


- `func` — Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `map` — Map to apply function to. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a new map obtained from the original map by application of `func` for each element. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapApply((k, v) -> (k, v * 2), map('k1', 1, 'k2', 2))

```


```
{'k1':2,'k2':4}

```

## mapConcat[​](#mapConcat "Direct link to mapConcat")


Introduced in: v23\.4\.0


Concatenates multiple maps based on the equality of their keys.
If elements with the same key exist in more than one input map, all elements are added to the result map, but only the first one is accessible via operator \[].


**Syntax**



```
mapConcat(maps)

```

**Arguments**


- `maps` — Arbitrarily many maps. [`Map`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a map with concatenated maps passed as arguments. [`Map`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapConcat(map('k1', 'v1'), map('k2', 'v2'))

```


```
{'k1':'v1','k2':'v2'}

```

## mapContainsKey[​](#mapContainsKey "Direct link to mapContainsKey")


Introduced in: v21\.2\.0


Determines if a key is contained in a map.


**Syntax**



```
mapContainsKey(map, key)

```

**Aliases**: `mapContains`


**Arguments**


- `map` — Map to search in. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `key` — Key to search for. Type must match the key type of the map. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns 1 if map contains key, 0 if not. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT mapContainsKey(map('k1', 'v1', 'k2', 'v2'), 'k1')

```


```
1

```

## mapContainsKeyLike[​](#mapContainsKeyLike "Direct link to mapContainsKeyLike")


Introduced in: v23\.4\.0


Checks whether map contains key `LIKE` specified pattern.


**Syntax**



```
mapContainsKeyLike(map, pattern)

```

**Arguments**


- `map` — Map to search in. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `pattern` — Pattern to match keys against. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `map` contains a key matching `pattern`, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE tab (a Map(String, String))
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO tab VALUES ({'abc':'abc','def':'def'}), ({'hij':'hij','klm':'klm'});

SELECT mapContainsKeyLike(a, 'a%') FROM tab;

```


```
┌─mapContainsKeyLike(a, 'a%')─┐
│                           1 │
│                           0 │
└─────────────────────────────┘

```

## mapContainsValue[​](#mapContainsValue "Direct link to mapContainsValue")


Introduced in: v25\.6\.0


Determines if a value is contained in a map.


**Syntax**



```
mapContainsValue(map, value)

```

**Arguments**


- `map` — Map to search in. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `value` — Value to search for. Type must match the value type of map. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `1` if the map contains the value, `0` if not. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT mapContainsValue(map('k1', 'v1', 'k2', 'v2'), 'v1')

```


```
1

```

## mapContainsValueLike[​](#mapContainsValueLike "Direct link to mapContainsValueLike")


Introduced in: v25\.5\.0


Checks whether a map contains a value `LIKE` the specified pattern.


**Syntax**



```
mapContainsValueLike(map, pattern)

```

**Arguments**


- `map` — Map to search in. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `pattern` — Pattern to match values against. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `map` contains a value matching `pattern`, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE tab (a Map(String, String))
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO tab VALUES ({'abc':'abc','def':'def'}), ({'hij':'hij','klm':'klm'});

SELECT mapContainsValueLike(a, 'a%') FROM tab;

```


```
┌─mapContainsV⋯ke(a, 'a%')─┐
│                        1 │
│                        0 │
└──────────────────────────┘

```

## mapExists[​](#mapExists "Direct link to mapExists")


Introduced in: v23\.4\.0


Tests whether a condition holds for at least one key\-value pair in a map.
`mapExists` is a higher\-order function.
You can pass a lambda function to it as the first argument.


**Syntax**



```
mapExists([func,] map)

```

**Arguments**


- `func` — Optional. Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `map` — Map to check. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns `1` if at least one key\-value pair satisfies the condition, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT mapExists((k, v) -> v = 1, map('k1', 1, 'k2', 2))

```


```
1

```

## mapExtractKeyLike[​](#mapExtractKeyLike "Direct link to mapExtractKeyLike")


Introduced in: v23\.4\.0


Give a map with string keys and a `LIKE` pattern, this function returns a map with elements where the key matches the pattern.


**Syntax**



```
mapExtractKeyLike(map, pattern)

```

**Arguments**


- `map` — Map to extract from. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `pattern` — Pattern to match keys against. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a map containing elements the key matching the specified pattern. If no elements match the pattern, an empty map is returned. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
CREATE TABLE tab (a Map(String, String))
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO tab VALUES ({'abc':'abc','def':'def'}), ({'hij':'hij','klm':'klm'});

SELECT mapExtractKeyLike(a, 'a%') FROM tab;

```


```
┌─mapExtractKeyLike(a, 'a%')─┐
│ {'abc':'abc'}              │
│ {}                         │
└────────────────────────────┘

```

## mapExtractValueLike[​](#mapExtractValueLike "Direct link to mapExtractValueLike")


Introduced in: v25\.5\.0


Given a map with string values and a `LIKE` pattern, this function returns a map with elements where the value matches the pattern.


**Syntax**



```
mapExtractValueLike(map, pattern)

```

**Arguments**


- `map` — Map to extract from. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `pattern` — Pattern to match values against. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a map containing elements the value matching the specified pattern. If no elements match the pattern, an empty map is returned. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
CREATE TABLE tab (a Map(String, String))
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO tab VALUES ({'abc':'abc','def':'def'}), ({'hij':'hij','klm':'klm'});

SELECT mapExtractValueLike(a, 'a%') FROM tab;

```


```
┌─mapExtractValueLike(a, 'a%')─┐
│ {'abc':'abc'}                │
│ {}                           │
└──────────────────────────────┘

```

## mapFilter[​](#mapFilter "Direct link to mapFilter")


Introduced in: v22\.3\.0


Filters a map by applying a function to each map element.


**Syntax**



```
mapFilter(func, map)

```

**Arguments**


- `func` — Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `map` — Map to filter. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a map containing only the elements in the map for which `func` returns something other than `0`. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapFilter((k, v) -> v > 1, map('k1', 1, 'k2', 2))

```


```
{'k2':2}

```

## mapFromArrays[​](#mapFromArrays "Direct link to mapFromArrays")


Introduced in: v23\.3\.0


Creates a map from an array or map of keys and an array or map of values.
The function is a convenient alternative to syntax `CAST([...], 'Map(key_type, value_type)')`.


**Syntax**



```
mapFromArrays(keys, values)

```

**Aliases**: `MAP_FROM_ARRAYS`


**Arguments**


- `keys` — Array or map of keys to create the map from. [`Array`](/docs/sql-reference/data-types/array) or [`Map`](/docs/sql-reference/data-types/map)
- `values` — Array or map of values to create the map from. [`Array`](/docs/sql-reference/data-types/array) or [`Map`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a map with keys and values constructed from the key array and value array/map. [`Map`](/docs/sql-reference/data-types/map)


**Examples**


**Basic usage**



```
SELECT mapFromArrays(['a', 'b', 'c'], [1, 2, 3])

```


```
{'a':1,'b':2,'c':3}

```

**With map inputs**



```
SELECT mapFromArrays([1, 2, 3], map('a', 1, 'b', 2, 'c', 3))

```


```
{1:('a', 1), 2:('b', 2), 3:('c', 3)}

```

## mapKeys[​](#mapKeys "Direct link to mapKeys")


Introduced in: v21\.2\.0


Returns the keys of a given map.
This function can be optimized by enabling setting [`optimize_functions_to_subcolumns`](/docs/operations/settings/settings#optimize_functions_to_subcolumns).
With the setting enabled, the function only reads the `keys` subcolumn instead of the entire map.
The query `SELECT mapKeys(m) FROM table` is transformed to `SELECT m.keys FROM table`.


**Syntax**



```
mapKeys(map)

```

**Arguments**


- `map` — Map to extract keys from. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns array containing all keys from the map. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT mapKeys(map('k1', 'v1', 'k2', 'v2'))

```


```
['k1','k2']

```

## mapPartialReverseSort[​](#mapPartialReverseSort "Direct link to mapPartialReverseSort")


Introduced in: v23\.4\.0


Sorts the elements of a map in descending order with additional limit argument allowing partial sorting.
If the func function is specified, the sorting order is determined by the result of the func function applied to the keys and values of the map.


**Syntax**



```
mapPartialReverseSort([func,] limit, map)

```

**Arguments**


- `func` — Optional. Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `limit` — Elements in the range `[1..limit]` are sorted. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `map` — Map to sort. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a partially sorted map in descending order. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapPartialReverseSort((k, v) -> v, 2, map('k1', 3, 'k2', 1, 'k3', 2))

```


```
{'k1':3,'k3':2,'k2':1}

```

## mapPartialSort[​](#mapPartialSort "Direct link to mapPartialSort")


Introduced in: v23\.4\.0


Sorts the elements of a map in ascending order with additional limit argument allowing partial sorting.
If the func function is specified, the sorting order is determined by the result of the func function applied to the keys and values of the map.


**Syntax**



```
mapPartialSort([func,] limit, map)

```

**Arguments**


- `func` — Optional. Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `limit` — Elements in the range `[1..limit]` are sorted. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `map` — Map to sort. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a partially sorted map. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapPartialSort((k, v) -> v, 2, map('k1', 3, 'k2', 1, 'k3', 2))

```


```
{'k2':1,'k3':2,'k1':3}

```

## mapPopulateSeries[​](#mapPopulateSeries "Direct link to mapPopulateSeries")


Introduced in: v20\.10\.0


Fills missing key\-value pairs in a map with integer keys.
To support extending the keys beyond the largest value, a maximum key can be specified.
More specifically, the function returns a map in which the keys form a series from the smallest to the largest key (or max argument if specified) with step size of 1, and corresponding values.
If no value is specified for a key, a default value is used as value.
In case keys repeat, only the first value (in order of appearance) is associated with the key.


**Syntax**



```
mapPopulateSeries(map[, max]) | mapPopulateSeries(keys, values[, max])

```

**Arguments**


- `map` — Map with integer keys. [`Map((U)Int*, V)`](/docs/sql-reference/data-types/map)
- `keys` — Array of keys. [`Array(T)`](/docs/sql-reference/data-types/array)
- `values` — Array of values. [`Array(T)`](/docs/sql-reference/data-types/array)
- `max` — Optional. Maximum key value. [`Int8`](/docs/sql-reference/data-types/int-uint) or [`Int16`](/docs/sql-reference/data-types/int-uint) or [`Int32`](/docs/sql-reference/data-types/int-uint) or [`Int64`](/docs/sql-reference/data-types/int-uint) or [`Int128`](/docs/sql-reference/data-types/int-uint) or [`Int256`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a map or a tuple of two arrays where the first has keys in sorted order, and the second values for the corresponding keys. [`Map(K, V)`](/docs/sql-reference/data-types/map) or [`Tuple(Array(UInt*), Array(Any))`](/docs/sql-reference/data-types/tuple)


**Examples**


**With Map type**



```
SELECT mapPopulateSeries(map(1, 10, 5, 20), 6)

```


```
{1:10, 2:0, 3:0, 4:0, 5:20, 6:0}

```

**With mapped arrays**



```
SELECT mapPopulateSeries([1, 2, 4], [11, 22, 44], 5)

```


```
([1, 2, 3, 4, 5], [11, 22, 0, 44, 0])

```

## mapReverseSort[​](#mapReverseSort "Direct link to mapReverseSort")


Introduced in: v23\.4\.0


Sorts the elements of a map in descending order.
If the func function is specified, the sorting order is determined by the result of the func function applied to the keys and values of the map.


**Syntax**



```
mapReverseSort([func,] map)

```

**Arguments**


- `func` — Optional. Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `map` — Map to sort. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a map sorted in descending order. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapReverseSort((k, v) -> v, map('k1', 3, 'k2', 1, 'k3', 2))

```


```
{'k1':3,'k3':2,'k2':1}

```

## mapSort[​](#mapSort "Direct link to mapSort")


Introduced in: v23\.4\.0


Sorts the elements of a map in ascending order.
If the func function is specified, the sorting order is determined by the result of the func function applied to the keys and values of the map.


**Syntax**



```
mapSort([func,] map)

```

**Arguments**


- `func` — Optional. Lambda function. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `map` — Map to sort. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns a map sorted in ascending order. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Usage example**



```
SELECT mapSort((k, v) -> v, map('k1', 3, 'k2', 1, 'k3', 2))

```


```
{'k2':1,'k3':2,'k1':3}

```

## mapSubtract[​](#mapSubtract "Direct link to mapSubtract")


Introduced in: v20\.7\.0


Collect all the keys and subtract corresponding values.


**Syntax**



```
mapSubtract(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — Maps or tuples of two arrays in which items in the first array represent keys, and the second array contains values for each key. [`Map(K, V)`](/docs/sql-reference/data-types/map) or [`Tuple(Array(T), Array(T))`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns one map or tuple, where the first array contains the sorted keys and the second array contains values. [`Map(K, V)`](/docs/sql-reference/data-types/map) or [`Tuple(Array(T), Array(T))`](/docs/sql-reference/data-types/tuple)


**Examples**


**With Map type**



```
SELECT mapSubtract(map(1, 1), map(1, 1))

```


```
{1:0}

```

**With tuple map**



```
SELECT mapSubtract(([toUInt8(1), 2], [toInt32(1), 1]), ([toUInt8(1), 2], [toInt32(2), 1]))

```


```
([1, 2], [-1, 0])

```

## mapUpdate[​](#mapUpdate "Direct link to mapUpdate")


Introduced in: v22\.3\.0


For two maps, returns the first map with values updated on the values for the corresponding keys in the second map.


**Syntax**



```
mapUpdate(map1, map2)

```

**Arguments**


- `map1` — The map to update. [`Map(K, V)`](/docs/sql-reference/data-types/map)
- `map2` — The map to use for updating. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns `map1` with values updated from values for the corresponding keys in `map2`. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Examples**


**Basic usage**



```
SELECT mapUpdate(map('key1', 0, 'key3', 0), map('key1', 10, 'key2', 10))

```


```
{'key3':0,'key1':10,'key2':10}

```

## mapValues[​](#mapValues "Direct link to mapValues")


Introduced in: v21\.2\.0


Returns the values of a given map.
This function can be optimized by enabling setting [`optimize_functions_to_subcolumns`](/docs/operations/settings/settings#optimize_functions_to_subcolumns).
With the setting enabled, the function only reads the `values` subcolumn instead of the entire map.
The query `SELECT mapValues(m) FROM table` is transformed to `SELECT m.values FROM table`.


**Syntax**



```
mapValues(map)

```

**Arguments**


- `map` — Map to extract values from. [`Map(K, V)`](/docs/sql-reference/data-types/map)


**Returned value**


Returns an array containing all the values from the map. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT mapValues(map('k1', 'v1', 'k2', 'v2'))

```


```
['v1','v2']

```
[PreviousTuples](/docs/sql-reference/functions/tuple-functions)[NextType conversion](/docs/sql-reference/functions/type-conversion-functions)- [extractKeyValuePairs](#extractKeyValuePairs)- [extractKeyValuePairsWithEscaping](#extractKeyValuePairsWithEscaping)- [map](#map)- [mapAdd](#mapAdd)- [mapAll](#mapAll)- [mapApply](#mapApply)- [mapConcat](#mapConcat)- [mapContainsKey](#mapContainsKey)- [mapContainsKeyLike](#mapContainsKeyLike)- [mapContainsValue](#mapContainsValue)- [mapContainsValueLike](#mapContainsValueLike)- [mapExists](#mapExists)- [mapExtractKeyLike](#mapExtractKeyLike)- [mapExtractValueLike](#mapExtractValueLike)- [mapFilter](#mapFilter)- [mapFromArrays](#mapFromArrays)- [mapKeys](#mapKeys)- [mapPartialReverseSort](#mapPartialReverseSort)- [mapPartialSort](#mapPartialSort)- [mapPopulateSeries](#mapPopulateSeries)- [mapReverseSort](#mapReverseSort)- [mapSort](#mapSort)- [mapSubtract](#mapSubtract)- [mapUpdate](#mapUpdate)- [mapValues](#mapValues)
Was this page helpful?

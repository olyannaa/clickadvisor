# Hash Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Hash
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/hash-functions.md)# Hash Functions

Hash functions can be used for the deterministic pseudo\-random shuffling of elements.


Simhash is a hash function, which returns close hash values for close (similar) arguments.


Most hash functions accept any number of arguments of any types.


NoteHash of NULL is NULL. To get a non\-NULL hash of a Nullable column, wrap it in a tuple:
```
SELECT cityHash64(tuple(NULL))

```



NoteTo calculate hash of the whole contents of a table, use `sum(cityHash64(tuple(*)))` (or other hash function). `tuple` ensures that rows with NULL values are not skipped. `sum` ensures that the order of rows doesn't matter.


## BLAKE3[​](#BLAKE3 "Direct link to BLAKE3")


Introduced in: v22\.10\.0


Calculates BLAKE3 hash string and returns the resulting set of bytes as FixedString.
This cryptographic hash\-function is integrated into ClickHouse with BLAKE3 Rust library.
The function is rather fast and shows approximately two times faster performance compared to SHA\-2, while generating hashes of the same length as SHA\-256\.
It returns a BLAKE3 hash as a byte array with type FixedString(32\).


**Syntax**



```
BLAKE3(message)

```

**Arguments**


- `message` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the 32\-byte BLAKE3 hash of the input string as a fixed\-length string. [`FixedString(32)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**hash**



```
SELECT hex(BLAKE3('ABC'))

```


```
┌─hex(BLAKE3('ABC'))───────────────────────────────────────────────┐
│ D1717274597CF0289694F75D96D444B992A096F1AFD8E7BBFA6EBB1D360FEDFC │
└──────────────────────────────────────────────────────────────────┘

```

## MD4[​](#MD4 "Direct link to MD4")


Introduced in: v21\.11\.0


Calculates the MD4 hash of the given string.


**Syntax**



```
MD4(s)

```

**Arguments**


- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the MD4 hash of the given input string as a fixed\-length string. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(MD4('abc'));

```


```
┌─hex(MD4('abc'))──────────────────┐
│ A448017AAF21D8525FC10AE87AA6729D │
└──────────────────────────────────┘

```

## MD5[​](#MD5 "Direct link to MD5")


Introduced in: v1\.1\.0


Calculates the MD5 hash of the given string.


**Syntax**



```
MD5(s)

```

**Arguments**


- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the MD5 hash of the given input string as a fixed\-length string. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(MD5('abc'));

```


```
┌─hex(MD5('abc'))──────────────────┐
│ 900150983CD24FB0D6963F7D28E17F72 │
└──────────────────────────────────┘

```

## RIPEMD160[​](#RIPEMD160 "Direct link to RIPEMD160")


Introduced in: v24\.10\.0


Calculates the RIPEMD\-160 hash of the given string.


**Syntax**



```
RIPEMD160(s)

```

**Arguments**


- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the RIPEMD160 hash of the given input string as a fixed\-length string. [`FixedString(20)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(RIPEMD160('The quick brown fox jumps over the lazy dog'));

```


```
┌─HEX(RIPEMD160('The quick brown fox jumps over the lazy dog'))─┐
│ 37F332F68DB77BD9D7EDD4969571AD671CF9DD3B                      │
└───────────────────────────────────────────────────────────────┘

```

## SHA1[​](#SHA1 "Direct link to SHA1")


Introduced in: v1\.1\.0


Calculates the SHA1 hash of the given string.


**Syntax**



```
SHA1(s)

```

**Arguments**


- `s` — The input string to hash [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the SHA1 hash of the given input string as a fixed\-length string. [`FixedString(20)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(SHA1('abc'));

```


```
┌─hex(SHA1('abc'))─────────────────────────┐
│ A9993E364706816ABA3E25717850C26C9CD0D89D │
└──────────────────────────────────────────┘

```

## SHA224[​](#SHA224 "Direct link to SHA224")


Introduced in: v1\.1\.0


Calculates the SHA224 hash of the given string.


**Syntax**



```
SHA224(s)

```

**Arguments**


- `s` — The input value to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the SHA224 hash of the given input string as a fixed\-length string. [`FixedString(28)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(SHA224('abc'));

```


```
┌─hex(SHA224('abc'))───────────────────────────────────────┐
│ 23097D223405D8228642A477BDA255B32AADBCE4BDA0B3F7E36C9DA7 │
└──────────────────────────────────────────────────────────┘

```

## SHA256[​](#SHA256 "Direct link to SHA256")


Introduced in: v1\.1\.0


Calculates the SHA256 hash of the given string.


**Syntax**



```
SHA256(s)

```

**Arguments**


- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the SHA256 hash of the given input string as a fixed\-length string. [`FixedString(32)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(SHA256('abc'));

```


```
┌─hex(SHA256('abc'))───────────────────────────────────────────────┐
│ BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD │
└──────────────────────────────────────────────────────────────────┘

```

## SHA384[​](#SHA384 "Direct link to SHA384")


Introduced in: v1\.1\.0


Calculates the SHA384 hash of the given string.


**Syntax**



```
SHA384(s)

```

**Arguments**


- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the SHA384 hash of the given input string as a fixed\-length string. [`FixedString(48)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(SHA384('abc'));

```


```
┌─hex(SHA384('abc'))───────────────────────────────────────────────────────────────────────────────┐
│ CB00753F45A35E8BB5A03D699AC65007272C32AB0EDED1631A8B605A43FF5BED8086072BA1E7CC2358BAECA134C825A7 │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## SHA512[​](#SHA512 "Direct link to SHA512")


Introduced in: v1\.1\.0


Calculates the SHA512 hash of the given string.


**Syntax**



```
SHA512(s)

```

**Arguments**


- `s` — The input string to hash [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the SHA512 hash of the given input string as a fixed\-length string. [`FixedString(64)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(SHA512('abc'));

```


```
┌─hex(SHA512('abc'))───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DDAF35A193617ABACC417349AE20413112E6FA4E89A97EA20A9EEEE64B55D39A2192992A274FC1A836BA3C23A3FEEBBD454D4423643CE80E2A9AC94FA54CA49F │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## SHA512\_256[​](#SHA512_256 "Direct link to SHA512_256")


Introduced in: v1\.1\.0


Calculates the SHA512\_256 hash of the given string.


**Syntax**



```
SHA512_256(s)

```

**Arguments**


- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the SHA512\_256 hash of the given input string as a fixed\-length string. [`FixedString(32)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT HEX(SHA512_256('abc'));

```


```
┌─hex(SHA512_256('abc'))───────────────────────────────────────────┐
│ 53048E2681941EF99B2E29B76B4C7DABE4C2D0C634FC6D46E0E2F13107E7AF23 │
└──────────────────────────────────────────────────────────────────┘

```

## URLHash[​](#URLHash "Direct link to URLHash")


Introduced in: v1\.1\.0


A fast, decent\-quality non\-cryptographic hash function for a string obtained from a URL using some type of normalization.


This hash function has two modes:




| Mode Description| `URLHash(url)` Calculates a hash from a string without one of the trailing symbols `/`,`?` or `#` at the end, if present.| `URLHash(url, N)` Calculates a hash from a string up to the N level in the URL hierarchy, without one of the trailing symbols `/`,`?` or `#` at the end, if present. Levels are the same as in `URLHierarchy`. | | | | | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- |


**Syntax**



```
URLHash(url[, N])

```

**Arguments**


- `url` — URL string to hash. [`String`](/docs/sql-reference/data-types/string)
- `N` — Optional. Level in the URL hierarchy. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value of `url`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT URLHash('https://www.clickhouse.com')

```


```
┌─URLHash('htt⋯house.com')─┐
│     13614512636072854701 │
└──────────────────────────┘

```

**Hash of url with specified level**



```
SELECT URLHash('https://www.clickhouse.com/docs', 0);
SELECT URLHash('https://www.clickhouse.com/docs', 1);

```


```
-- hash of https://www.clickhouse.com
┌─URLHash('htt⋯m/docs', 0)─┐
│     13614512636072854701 │
└──────────────────────────┘
-- hash of https://www.clickhouse.com/docs
┌─URLHash('htt⋯m/docs', 1)─┐
│     13167253331440520598 │
└──────────────────────────┘

```

## cityHash64[​](#cityHash64 "Direct link to cityHash64")


Introduced in: v1\.1\.0


Produces a 64\-bit [CityHash](https://github.com/google/cityhash) hash value.


This is a fast non\-cryptographic hash function.
It uses the CityHash algorithm for string parameters and implementation\-specific fast non\-cryptographic hash function for parameters with other data types.
The function uses the CityHash combinator to get the final results.


ReferencesGoogle changed the algorithm of CityHash after it was added to ClickHouse.
In other words, ClickHouse's cityHash64 and Google's upstream CityHash now produce different results.
ClickHouse cityHash64 corresponds to CityHash v1\.0\.2\.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
cityHash64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Call example**



```
SELECT cityHash64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS CityHash, toTypeName(CityHash) AS type;

```


```
┌─────────────CityHash─┬─type───┐
│ 12072650598913549138 │ UInt64 │
└──────────────────────┴────────┘

```

**Computing the checksum of the entire table with accuracy up to the row order**



```
CREATE TABLE users (
    id UInt32,
    name String,
    age UInt8,
    city String
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO users VALUES
(1, 'Alice', 25, 'New York'),
(2, 'Bob', 30, 'London'),
(3, 'Charlie', 35, 'Tokyo');

SELECT groupBitXor(cityHash64(*)) FROM users;

```


```
┌─groupBitXor(⋯age, city))─┐
│     11639977218258521182 │
└──────────────────────────┘

```

## farmFingerprint64[​](#farmFingerprint64 "Direct link to farmFingerprint64")


Introduced in: v20\.12\.0


Produces a 64\-bit [FarmHash](https://github.com/google/farmhash) value using the `Fingerprint64` method.


Tip`farmFingerprint64` is preferred for a stable and portable value over [`farmHash64`](#farmHash64).


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
farmFingerprint64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash value of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT farmFingerprint64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS FarmFingerprint, toTypeName(FarmFingerprint) AS type;

```


```
┌─────FarmFingerprint─┬─type───┐
│ 5752020380710916328 │ UInt64 │
└─────────────────────┴────────┘

```

## farmHash64[​](#farmHash64 "Direct link to farmHash64")


Introduced in: v1\.1\.0


Produces a 64\-bit [FarmHash](https://github.com/google/farmhash) using the `Hash64` method.


Tip[`farmFingerprint64`](#farmFingerprint64) is preferred for a stable and portable value.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
farmHash64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash value of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT farmHash64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS FarmHash, toTypeName(FarmHash) AS type;

```


```
┌─────────────FarmHash─┬─type───┐
│ 18125596431186471178 │ UInt64 │
└──────────────────────┴────────┘

```

## gccMurmurHash[​](#gccMurmurHash "Direct link to gccMurmurHash")


Introduced in: v20\.1\.0


Computes the 64\-bit [MurmurHash2](https://github.com/aappleby/smhasher) hash of the input value using the same seed as used by [GCC](https://github.com/gcc-mirror/gcc/blob/41d6b10e96a1de98e90a7c0378437c3255814b16/libstdc%2B%2B-v3/include/bits/functional_hash.h#L191).


It is portable between Clang and GCC builds.


**Syntax**



```
gccMurmurHash(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the calculated hash value of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    gccMurmurHash(1, 2, 3) AS res1,
    gccMurmurHash(('a', [1, 2, 3], 4, (4, ['foo', 'bar'], 1, (1, 2)))) AS res2

```


```
┌─────────────────res1─┬────────────────res2─┐
│ 12384823029245979431 │ 1188926775431157506 │
└──────────────────────┴─────────────────────┘

```

## halfMD5[​](#halfMD5 "Direct link to halfMD5")


Introduced in: v1\.1\.0


[Interprets](/docs/sql-reference/functions/type-conversion-functions#reinterpretAsString) all the input
parameters as strings and calculates the MD5 hash value for each of them. Then combines hashes, takes the first 8 bytes of the hash of the
resulting string, and interprets them as [UInt64](/docs/sql-reference/data-types/int-uint) in big\-endian byte order. The function is
relatively slow (5 million short strings per second per processor core).


Consider using the [`sipHash64`](#sipHash64) function instead.


The function takes a variable number of input parameters.
Arguments can be any of the supported data types.
For some data types calculated value of hash function may be the same for the same values even if types of arguments differ (integers of different size, named and unnamed Tuple with the same data, Map and the corresponding Array(Tuple(key, value)) type with the same data).


**Syntax**



```
halfMD5(arg1[, arg2, ..., argN])

```

**Arguments**


- `arg1[, arg2, ..., argN]` — Variable number of arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed half MD5 hash of the given input params returned as a `UInt64` in big\-endian byte order. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT HEX(halfMD5('abc', 'cde', 'fgh'));

```


```
┌─hex(halfMD5('abc', 'cde', 'fgh'))─┐
│ 2C9506B7374CFAF4                  │
└───────────────────────────────────┘

```

## hiveHash[​](#hiveHash "Direct link to hiveHash")


Introduced in: v20\.1\.0


Calculates a "HiveHash" from a string.
This is just [`JavaHash`](#javaHash) with zeroed out sign bits.
This function is used in [Apache Hive](https://en.wikipedia.org/wiki/Apache_Hive) for versions before 3\.0\.


NoteThis hash function is unperformant.
Use it only when this algorithm is already used in another system and you need to calculate the same result.


**Syntax**



```
hiveHash(arg)

```

**Arguments**


- `arg` — Input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the computed "hive hash" of the input string. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT hiveHash('Hello, world!');

```


```
┌─hiveHash('Hello, world!')─┐
│                 267439093 │
└───────────────────────────┘

```

## icebergHash[​](#icebergHash "Direct link to icebergHash")


Introduced in: v25\.5\.0


Implements the logic of the iceberg [hashing transform](https://iceberg.apache.org/spec/#appendix-b-32-bit-hash-requirements)


**Syntax**



```
icebergHash(value)

```

**Arguments**


- `value` — Source value to take the hash of [`Integer`](/docs/sql-reference/data-types/int-uint) or [`Bool`](/docs/sql-reference/data-types/boolean) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`Date`](/docs/sql-reference/data-types/date) or [`Time`](/docs/sql-reference/data-types/time) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns a 32\-bit Murmur3 hash, x86 variant, seeded with 0 [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Example**



```
SELECT icebergHash(1.0 :: Float32)

```


```
-142385009

```

## intHash32[​](#intHash32 "Direct link to intHash32")


Introduced in: v1\.1\.0


Calculates a 32\-bit hash of an integer.


The hash function is relatively fast but not cryptographic hash function.


**Syntax**



```
intHash32(arg)

```

**Arguments**


- `arg` — Integer to hash. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed 32\-bit hash code of the input integer [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT intHash32(42);

```


```
┌─intHash32(42)─┐
│    1228623923 │
└───────────────┘

```

## intHash64[​](#intHash64 "Direct link to intHash64")


Introduced in: v1\.1\.0


Calculates a 64\-bit hash of an integer.


The hash function is relatively fast (even faster than [`intHash32`](#intHash32)) but not a cryptographic hash function.


**Syntax**



```
intHash64(int)

```

**Arguments**


- `int` — Integer to hash. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


64\-bit hash code. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT intHash64(42);

```


```
┌────────intHash64(42)─┐
│ 11490350930367293593 │
└──────────────────────┘

```

## javaHash[​](#javaHash "Direct link to javaHash")


Introduced in: v20\.1\.0


Calculates JavaHash from:


- [string](http://hg.openjdk.java.net/jdk8u/jdk8u/jdk/file/478a4add975b/src/share/classes/java/lang/String.java#l1452),
- [Byte](https://hg.openjdk.java.net/jdk8u/jdk8u/jdk/file/478a4add975b/src/share/classes/java/lang/Byte.java#l405),
- [Short](https://hg.openjdk.java.net/jdk8u/jdk8u/jdk/file/478a4add975b/src/share/classes/java/lang/Short.java#l410),
- [Integer](https://hg.openjdk.java.net/jdk8u/jdk8u/jdk/file/478a4add975b/src/share/classes/java/lang/Integer.java#l959),
- [Long](https://hg.openjdk.java.net/jdk8u/jdk8u/jdk/file/478a4add975b/src/share/classes/java/lang/Long.java#l1060).


NoteThis hash function is unperformant.
Use it only when this algorithm is already in use in another system and you need to calculate the same result.


NoteJava only supports calculating the hash of signed integers,
so if you want to calculate a hash of unsigned integers you must cast them to the proper signed ClickHouse types.


**Syntax**



```
javaHash(arg)

```

**Arguments**


- `arg` — Input value to hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash of `arg` [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example 1**



```
SELECT javaHash(toInt32(123));

```


```
┌─javaHash(toInt32(123))─┐
│               123      │
└────────────────────────┘

```

**Usage example 2**



```
SELECT javaHash('Hello, world!');

```


```
┌─javaHash('Hello, world!')─┐
│               -1880044555 │
└───────────────────────────┘

```

## javaHashUTF16LE[​](#javaHashUTF16LE "Direct link to javaHashUTF16LE")


Introduced in: v20\.1\.0


Calculates [JavaHash](http://hg.openjdk.java.net/jdk8u/jdk8u/jdk/file/478a4add975b/src/share/classes/java/lang/String.java#l1452) from a string, assuming it contains bytes representing a string in UTF\-16LE encoding.


**Syntax**



```
javaHashUTF16LE(arg)

```

**Arguments**


- `arg` — A string in UTF\-16LE encoding. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the computed hash of the UTF\-16LE encoded string. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT javaHashUTF16LE(convertCharset('test', 'utf-8', 'utf-16le'));

```


```
┌─javaHashUTF16LE(convertCharset('test', 'utf-8', 'utf-16le'))─┐
│                                                      3556498 │
└──────────────────────────────────────────────────────────────┘

```

## jumpConsistentHash[​](#jumpConsistentHash "Direct link to jumpConsistentHash")


Introduced in: v1\.1\.0


Calculates the [jump consistent hash](https://arxiv.org/pdf/1406.2294.pdf) for an integer.


**Syntax**



```
jumpConsistentHash(key, buckets)

```

**Arguments**


- `key` — The input key. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `buckets` — The number of buckets. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT jumpConsistentHash(256, 4)

```


```
┌─jumpConsistentHash(256, 4)─┐
│                          3 │
└────────────────────────────┘

```

## kafkaMurmurHash[​](#kafkaMurmurHash "Direct link to kafkaMurmurHash")


Introduced in: v23\.4\.0


Calculates the 32\-bit [MurmurHash2](https://github.com/aappleby/smhasher) hash of the input value using the same seed as used by [Kafka](https://github.com/apache/kafka/blob/461c5cfe056db0951d9b74f5adc45973670404d7/clients/src/main/java/org/apache/kafka/common/utils/Utils.java#L482) and without the highest bit to be compatible with [Default Partitioner](https://github.com/apache/kafka/blob/139f7709bd3f5926901a21e55043388728ccca78/clients/src/main/java/org/apache/kafka/clients/producer/internals/BuiltInPartitioner.java#L328).


**Syntax**



```
kafkaMurmurHash(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of parameters for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the calculated hash value of the input arguments. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    kafkaMurmurHash('foobar') AS res1,
    kafkaMurmurHash(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS res2

```


```
┌───────res1─┬─────res2─┐
│ 1357151166 │ 85479775 │
└────────────┴──────────┘

```

## keccak256[​](#keccak256 "Direct link to keccak256")


Introduced in: v25\.4\.0


Calculates the Keccak\-256 cryptographic hash of the given string.
This hash function is widely used in blockchain applications, particularly Ethereum.


**Syntax**



```
keccak256(message)

```

**Arguments**


- `message` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the 32\-byte Keccak\-256 hash of the input string as a fixed\-length string. [`FixedString(32)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT hex(keccak256('hello'))

```


```
┌─hex(keccak256('hello'))──────────────────────────────────────────┐
│ 1C8AFF950685C2ED4BC3174F3472287B56D9517B9C948127319A09A7A36DEAC8 │
└──────────────────────────────────────────────────────────────────┘

```

## kostikConsistentHash[​](#kostikConsistentHash "Direct link to kostikConsistentHash")


Introduced in: v22\.6\.0


An O(1\) time and space consistent hash algorithm by Konstantin 'Kostik' Oblakov.
Only efficient with `n <= 32768`.


**Syntax**



```
kostikConsistentHash(input, n)

```

**Aliases**: `yandexConsistentHash`


**Arguments**


- `input` — An integer key. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `n` — The number of buckets. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT kostikConsistentHash(16045690984833335023, 2);

```


```
┌─kostikConsistentHash(16045690984833335023, 2)─┐
│                                             1 │
└───────────────────────────────────────────────┘

```

## metroHash64[​](#metroHash64 "Direct link to metroHash64")


Introduced in: v1\.1\.0


Produces a 64\-bit [MetroHash](http://www.jandrewrogers.com/2015/05/27/metrohash/) hash value.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
metroHash64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT metroHash64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS MetroHash, toTypeName(MetroHash) AS type;

```


```
┌────────────MetroHash─┬─type───┐
│ 14235658766382344533 │ UInt64 │
└──────────────────────┴────────┘

```

## murmurHash2\_32[​](#murmurHash2_32 "Direct link to murmurHash2_32")


Introduced in: v18\.5\.0


Computes the [MurmurHash2](https://github.com/aappleby/smhasher) hash of the input value.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
murmurHash2_32(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash value of the input arguments. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT murmurHash2_32(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS MurmurHash2, toTypeName(MurmurHash2) AS type;

```


```
┌─MurmurHash2─┬─type───┐
│  3681770635 │ UInt32 │
└─────────────┴────────┘

```

## murmurHash2\_64[​](#murmurHash2_64 "Direct link to murmurHash2_64")


Introduced in: v18\.10\.0


Computes the [MurmurHash2](https://github.com/aappleby/smhasher) hash of the input value.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
murmurHash2_64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT murmurHash2_64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS MurmurHash2, toTypeName(MurmurHash2) AS type;

```


```
┌──────────MurmurHash2─┬─type───┐
│ 11832096901709403633 │ UInt64 │
└──────────────────────┴────────┘

```

## murmurHash3\_128[​](#murmurHash3_128 "Direct link to murmurHash3_128")


Introduced in: v18\.10\.0


Computes the 128\-bit [MurmurHash3](https://github.com/aappleby/smhasher) hash of the input value.


**Syntax**



```
murmurHash3_128(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed 128\-bit `MurmurHash3` hash value of the input arguments. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT hex(murmurHash3_128('foo', 'foo', 'foo'));

```


```
┌─hex(murmurHash3_128('foo', 'foo', 'foo'))─┐
│ F8F7AD9B6CD4CF117A71E277E2EC2931          │
└───────────────────────────────────────────┘

```

## murmurHash3\_32[​](#murmurHash3_32 "Direct link to murmurHash3_32")


Introduced in: v18\.10\.0


Produces a [MurmurHash3](https://github.com/aappleby/smhasher) hash value.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
murmurHash3_32(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash value of the input arguments. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT murmurHash3_32(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS MurmurHash3, toTypeName(MurmurHash3) AS type;

```


```
┌─MurmurHash3─┬─type───┐
│     2152717 │ UInt32 │
└─────────────┴────────┘

```

## murmurHash3\_64[​](#murmurHash3_64 "Direct link to murmurHash3_64")


Introduced in: v18\.10\.0


Computes the [MurmurHash3](https://github.com/aappleby/smhasher) hash of the input value.


NoteThe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
murmurHash3_64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash value of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT murmurHash3_64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS MurmurHash3, toTypeName(MurmurHash3) AS type;

```


```
┌──────────MurmurHash3─┬─type───┐
│ 11832096901709403633 │ UInt64 │
└──────────────────────┴────────┘

```

## ngramMinHash[​](#ngramMinHash "Direct link to ngramMinHash")


Introduced in: v21\.1\.0


Splits a ASCII string into n\-grams of `ngramsize` symbols and calculates hash values for each n\-gram and returns a tuple with these hashes.
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case sensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
ngramMinHash(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHash('ClickHouse') AS Tuple;

```


```
┌─Tuple──────────────────────────────────────┐
│ (18333312859352735453,9054248444481805918) │
└────────────────────────────────────────────┘

```

## ngramMinHashArg[​](#ngramMinHashArg "Direct link to ngramMinHashArg")


Introduced in: v21\.1\.0


Splits a ASCII string into n\-grams of `ngramsize` symbols and returns the n\-grams with minimum and maximum hashes, calculated by the [`ngramMinHash`](#ngramMinHash) function with the same input.
It is case sensitive.


**Syntax**



```
ngramMinHashArg(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` n\-grams each. [`Tuple(String)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashArg('ClickHouse') AS Tuple;

```


```
┌─Tuple─────────────────────────────────────────────────────────────────────────┐
│ (('ous','ick','lic','Hou','kHo','use'),('Hou','lic','ick','ous','ckH','Cli')) │
└───────────────────────────────────────────────────────────────────────────────┘

```

## ngramMinHashArgCaseInsensitive[​](#ngramMinHashArgCaseInsensitive "Direct link to ngramMinHashArgCaseInsensitive")


Introduced in: v21\.1\.0


Splits a ASCII string into n\-grams of `ngramsize` symbols and returns the n\-grams with minimum and maximum hashes, calculated by the [`ngramMinHashCaseInsensitive`](#ngramMinHashCaseInsensitive) function with the same input.
It is case insensitive.


**Syntax**



```
ngramMinHashArgCaseInsensitive(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` n\-grams each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashArgCaseInsensitive('ClickHouse') AS Tuple;

```


```
┌─Tuple─────────────────────────────────────────────────────────────────────────┐
│ (('ous','ick','lic','kHo','use','Cli'),('kHo','lic','ick','ous','ckH','Hou')) │
└───────────────────────────────────────────────────────────────────────────────┘

```

## ngramMinHashArgCaseInsensitiveUTF8[​](#ngramMinHashArgCaseInsensitiveUTF8 "Direct link to ngramMinHashArgCaseInsensitiveUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into n\-grams of `ngramsize` symbols and returns the n\-grams with minimum and maximum hashes, calculated by the ngramMinHashCaseInsensitiveUTF8 function with the same input.
It is case insensitive.


**Syntax**



```
ngramMinHashArgCaseInsensitiveUTF8(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` n\-grams each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashArgCaseInsensitiveUTF8('ClickHouse') AS Tuple;

```


```
┌─Tuple─────────────────────────────────────────────────────────────────────────┐
│ (('ckH','ous','ick','lic','kHo','use'),('kHo','lic','ick','ous','ckH','Hou')) │
└───────────────────────────────────────────────────────────────────────────────┘

```

## ngramMinHashArgUTF8[​](#ngramMinHashArgUTF8 "Direct link to ngramMinHashArgUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into n\-grams of `ngramsize` symbols and returns the n\-grams with minimum and maximum hashes, calculated by the `ngramMinHashUTF8` function with the same input.
It is case sensitive.


**Syntax**



```
ngramMinHashArgUTF8(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` n\-grams each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashArgUTF8('ClickHouse') AS Tuple;

```


```
┌─Tuple─────────────────────────────────────────────────────────────────────────┐
│ (('ous','ick','lic','Hou','kHo','use'),('kHo','Hou','lic','ick','ous','ckH')) │
└───────────────────────────────────────────────────────────────────────────────┘

```

## ngramMinHashCaseInsensitive[​](#ngramMinHashCaseInsensitive "Direct link to ngramMinHashCaseInsensitive")


Introduced in: v21\.1\.0


Splits a ASCII string into n\-grams of `ngramsize` symbols and calculates hash values for each n\-gram and returns a tuple with these hashes
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case insensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
ngramMinHashCaseInsensitive(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String. [String](/docs/sql-reference/data-types/string). \- `ngramsize` — The size of an n\-gram. Optional. Possible values: any number from `1` to `25`. Default value: `3`. [UInt8](/docs/sql-reference/data-types/int-uint). \- `hashnum` — The number of minimum and maximum hashes used to calculate the result. Optional. Possible values: any number from `1` to `25`. Default value: `6`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned value**


Tuple with two hashes — the minimum and the maximum. [Tuple](/docs/sql-reference/data-types/tuple)([UInt64](/docs/sql-reference/data-types/int-uint), [UInt64](/docs/sql-reference/data-types/int-uint)). [`Tuple`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashCaseInsensitive('ClickHouse') AS Tuple;

```


```
┌─Tuple──────────────────────────────────────┐
│ (2106263556442004574,13203602793651726206) │
└────────────────────────────────────────────┘

```

## ngramMinHashCaseInsensitiveUTF8[​](#ngramMinHashCaseInsensitiveUTF8 "Direct link to ngramMinHashCaseInsensitiveUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into n\-grams of `ngramsize` symbols and calculates hash values for each n\-gram and returns a tuple with these hashes..
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case insensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
ngramMinHashCaseInsensitiveUTF8(string [, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashCaseInsensitiveUTF8('ClickHouse') AS Tuple;

```


```
┌─Tuple───────────────────────────────────────┐
│ (12493625717655877135,13203602793651726206) │
└─────────────────────────────────────────────┘

```

## ngramMinHashUTF8[​](#ngramMinHashUTF8 "Direct link to ngramMinHashUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into n\-grams of `ngramsize` symbols and calculates hash values for each n\-gram and returns a tuple with these hashes.
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case sensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
ngramMinHashUTF8(string[, ngramsize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT ngramMinHashUTF8('ClickHouse') AS Tuple;

```


```
┌─Tuple──────────────────────────────────────┐
│ (18333312859352735453,6742163577938632877) │
└────────────────────────────────────────────┘

```

## ngramSimHash[​](#ngramSimHash "Direct link to ngramSimHash")


Introduced in: v21\.1\.0


Splits a ASCII string into n\-grams of `ngramsize` symbols and returns the n\-gram `simhash`.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
ngramSimHash(string[, ngramsize])

```

**Arguments**


- `string` — String for which to compute the case sensitive `simhash`. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is`3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash of the input string. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT ngramSimHash('ClickHouse') AS Hash;

```


```
┌───────Hash─┐
│ 1627567969 │
└────────────┘

```

## ngramSimHashCaseInsensitive[​](#ngramSimHashCaseInsensitive "Direct link to ngramSimHashCaseInsensitive")


Introduced in: v21\.1\.0


Splits a ASCII string into n\-grams of `ngramsize` symbols and returns the n\-gram `simhash`.
It is case insensitive.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
ngramSimHashCaseInsensitive(string[, ngramsize])

```

**Arguments**


- `string` — String for which to compute the case insensitive `simhash`. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Hash value. [UInt64](/docs/sql-reference/data-types/int-uint). [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT ngramSimHashCaseInsensitive('ClickHouse') AS Hash;

```


```
┌──────Hash─┐
│ 562180645 │
└───────────┘

```

## ngramSimHashCaseInsensitiveUTF8[​](#ngramSimHashCaseInsensitiveUTF8 "Direct link to ngramSimHashCaseInsensitiveUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into n\-grams of `ngramsize` symbols and returns the n\-gram `simhash`.
It is case insensitive.


Can be used for detection of semi\-duplicate strings with [bitHammingDistance](/docs/sql-reference/functions/bit-functions#bitHammingDistance). The smaller is the [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
ngramSimHashCaseInsensitiveUTF8(string[, ngramsize])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT ngramSimHashCaseInsensitiveUTF8('ClickHouse') AS Hash;

```


```
┌───────Hash─┐
│ 1636742693 │
└────────────┘

```

## ngramSimHashUTF8[​](#ngramSimHashUTF8 "Direct link to ngramSimHashUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 encoded string into n\-grams of `ngramsize` symbols and returns the n\-gram `simhash`.
It is case sensitive.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
ngramSimHashUTF8(string[, ngramsize])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `ngramsize` — Optional. The size of an n\-gram, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT ngramSimHashUTF8('ClickHouse') AS Hash;

```


```
┌───────Hash─┐
│ 1628157797 │
└────────────┘

```

## sipHash128[​](#sipHash128 "Direct link to sipHash128")


Introduced in: v1\.1\.0


Like [`sipHash64`](#sipHash64) but produces a 128\-bit hash value, i.e. the final xor\-folding state is done up to 128 bits.


use sipHash128Reference for new projectsThis 128\-bit variant differs from the reference implementation and is weaker.
This version exists because, when it was written, there was no official 128\-bit extension for SipHash.
New projects are advised to use [`sipHash128Reference`](#sipHash128Reference).


**Syntax**



```
sipHash128(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a 128\-bit `SipHash` hash value. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT hex(sipHash128('foo', '\x01', 3));

```


```
┌─hex(sipHash128('foo', '', 3))────┐
│ 9DE516A64A414D4B1B609415E4523F24 │
└──────────────────────────────────┘

```

## sipHash128Keyed[​](#sipHash128Keyed "Direct link to sipHash128Keyed")


Introduced in: v23\.2\.0


Same as [`sipHash128`](#sipHash128) but additionally takes an explicit key argument instead of using a fixed key.


use sipHash128ReferenceKeyed for new projectsThis 128\-bit variant differs from the reference implementation and it's weaker.
This version exists because, when it was written, there was no official 128\-bit extension for SipHash.
New projects should probably use [`sipHash128ReferenceKeyed`](#sipHash128ReferenceKeyed).


**Syntax**



```
sipHash128Keyed((k0, k1), [arg1, arg2, ...])

```

**Arguments**


- `(k0, k1)` — A tuple of two UInt64 values representing the key. [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)
- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


A 128\-bit `SipHash` hash value of type [FixedString(16\)](/docs/sql-reference/data-types/fixedstring). [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT hex(sipHash128Keyed((506097522914230528, 1084818905618843912),'foo', '\x01', 3));

```


```
┌─hex(sipHash128Keyed((506097522914230528, 1084818905618843912), 'foo', '', 3))─┐
│ B8467F65C8B4CFD9A5F8BD733917D9BF                                              │
└───────────────────────────────────────────────────────────────────────────────┘

```

## sipHash128Reference[​](#sipHash128Reference "Direct link to sipHash128Reference")


Introduced in: v23\.2\.0


Like [`sipHash128`](/docs/sql-reference/functions/hash-functions#sipHash128) but implements the 128\-bit algorithm from the original authors of SipHash.


**Syntax**



```
sipHash128Reference(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed 128\-bit `SipHash` hash value of the input arguments. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT hex(sipHash128Reference('foo', '', 3));

```


```
┌─hex(sipHash128Reference('foo', '', 3))─┐
│ 4D1BE1A22D7F5933C0873E1698426260       │
└────────────────────────────────────────┘

```

## sipHash128ReferenceKeyed[​](#sipHash128ReferenceKeyed "Direct link to sipHash128ReferenceKeyed")


Introduced in: v23\.2\.0


Same as [`sipHash128Reference`](#sipHash128Reference) but additionally takes an explicit key argument instead of using a fixed key.


**Syntax**



```
sipHash128ReferenceKeyed((k0, k1), arg1[, arg2, ...])

```

**Arguments**


- `(k0, k1)` — Tuple of two values representing the key [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)
- `arg1[, arg2, ...]` — A variable number of input arguments for which to compute the hash. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed 128\-bit `SipHash` hash value of the input arguments. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT hex(sipHash128Reference('foo', '', 3));

```


```
┌─hex(sipHash128Reference('foo', '', 3))─┐
│ 4D1BE1A22D7F5933C0873E1698426260       │
└────────────────────────────────────────┘

```

## sipHash64[​](#sipHash64 "Direct link to sipHash64")


Introduced in: v1\.1\.0


Produces a 64\-bit [SipHash](https://en.wikipedia.org/wiki/SipHash) hash value.


This is a cryptographic hash function. It works at least three times faster than the [`MD5`](#MD5) hash function.


The function [interprets](/docs/sql-reference/functions/type-conversion-functions#reinterpretAsString) all the input parameters as strings and calculates the hash value for each of them.
It then combines the hashes using the following algorithm:


1. The first and the second hash value are concatenated to an array which is hashed.
2. The previously calculated hash value and the hash of the third input parameter are hashed in a similar way.
3. This calculation is repeated for all remaining hash values of the original input.


Notethe calculated hash values may be equal for the same input values of different argument types.
This affects for example integer types of different size, named and unnamed `Tuple` with the same data, `Map` and the corresponding `Array(Tuple(key, value))` type with the same data.


**Syntax**



```
sipHash64(arg1[, arg2, ...])

```

**Arguments**


- `arg1[, arg2, ...]` — A variable number of input arguments. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a computed hash value of the input arguments. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT sipHash64(array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS SipHash, toTypeName(SipHash) AS type;

```


```
┌──────────────SipHash─┬─type───┐
│ 11400366955626497465 │ UInt64 │
└──────────────────────┴────────┘

```

## sipHash64Keyed[​](#sipHash64Keyed "Direct link to sipHash64Keyed")


Introduced in: v23\.2\.0


Like [`sipHash64`](#sipHash64) but additionally takes an explicit key argument instead of using a fixed key.


**Syntax**



```
sipHash64Keyed((k0, k1), arg1[,arg2, ...])

```

**Arguments**


- `(k0, k1)` — A tuple of two values representing the key. [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)
- `arg1[,arg2, ...]` — A variable number of input arguments. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed hash of the input values. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT sipHash64Keyed((506097522914230528, 1084818905618843912), array('e','x','a'), 'mple', 10, toDateTime('2019-06-15 23:00:00')) AS SipHash, toTypeName(SipHash) AS type;

```


```
┌─────────────SipHash─┬─type───┐
│ 8017656310194184311 │ UInt64 │
└─────────────────────┴────────┘

```

## wordShingleMinHash[​](#wordShingleMinHash "Direct link to wordShingleMinHash")


Introduced in: v21\.1\.0


Splits a ASCII string into parts (shingles) of `shinglesize` words, calculates hash values for each word shingle and returns a tuple with these hashes.
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case sensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
wordShingleMinHash(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHash('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Tuple;

```


```
┌─Tuple──────────────────────────────────────┐
│ (16452112859864147620,5844417301642981317) │
└────────────────────────────────────────────┘

```

## wordShingleMinHashArg[​](#wordShingleMinHashArg "Direct link to wordShingleMinHashArg")


Introduced in: v1\.1\.0


Splits a ASCII string into parts (shingles) of `shinglesize` words each and returns the shingles with minimum and maximum word hashes, calculated by the wordShingleMinHash function with the same input.
It is case sensitive.


**Syntax**



```
wordShingleMinHashArg(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` word shingles each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashArg('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).', 1, 3) AS Tuple;

```


```
┌─Tuple─────────────────────────────────────────────────────────────────┐
│ (('OLAP','database','analytical'),('online','oriented','processing')) │
└───────────────────────────────────────────────────────────────────────┘

```

## wordShingleMinHashArgCaseInsensitive[​](#wordShingleMinHashArgCaseInsensitive "Direct link to wordShingleMinHashArgCaseInsensitive")


Introduced in: v21\.1\.0


Splits a ASCII string into parts (shingles) of `shinglesize` words each and returns the shingles with minimum and maximum word hashes, calculated by the [`wordShingleMinHashCaseInsensitive`](#wordShingleMinHashCaseInsensitive) function with the same input.
It is case insensitive.


**Syntax**



```
wordShingleMinHashArgCaseInsensitive(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` word shingles each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashArgCaseInsensitive('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).', 1, 3) AS Tuple;

```


```
┌─Tuple──────────────────────────────────────────────────────────────────┐
│ (('queries','database','analytical'),('oriented','processing','DBMS')) │
└────────────────────────────────────────────────────────────────────────┘

```

## wordShingleMinHashArgCaseInsensitiveUTF8[​](#wordShingleMinHashArgCaseInsensitiveUTF8 "Direct link to wordShingleMinHashArgCaseInsensitiveUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into parts (shingles) of `shinglesize` words each and returns the shingles with minimum and maximum word hashes, calculated by the [`wordShingleMinHashCaseInsensitiveUTF8`](#wordShingleMinHashCaseInsensitiveUTF8) function with the same input.
It is case insensitive.


**Syntax**



```
wordShingleMinHashArgCaseInsensitiveUTF8(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` word shingles each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashArgCaseInsensitiveUTF8('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).', 1, 3) AS Tuple;

```


```
┌─Tuple──────────────────────────────────────────────────────────────────┐
│ (('queries','database','analytical'),('oriented','processing','DBMS')) │
└────────────────────────────────────────────────────────────────────────┘

```

## wordShingleMinHashArgUTF8[​](#wordShingleMinHashArgUTF8 "Direct link to wordShingleMinHashArgUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into parts (shingles) of `shinglesize` words each and returns the shingles with minimum and maximum word hashes, calculated by the [`wordShingleMinHashUTF8`](#wordShingleMinHashUTF8) function with the same input.
It is case sensitive.


**Syntax**



```
wordShingleMinHashArgUTF8(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two tuples with `hashnum` word shingles each. [`Tuple(Tuple(String))`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashArgUTF8('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).', 1, 3) AS Tuple;

```


```
┌─Tuple─────────────────────────────────────────────────────────────────┐
│ (('OLAP','database','analytical'),('online','oriented','processing')) │
└───────────────────────────────────────────────────────────────────────┘

```

## wordShingleMinHashCaseInsensitive[​](#wordShingleMinHashCaseInsensitive "Direct link to wordShingleMinHashCaseInsensitive")


Introduced in: v21\.1\.0


Splits a ASCII string into parts (shingles) of `shinglesize` words, calculates hash values for each word shingle and returns a tuple with these hashes.
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case insensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
wordShingleMinHashCaseInsensitive(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashCaseInsensitive('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Tuple;

```


```
┌─Tuple─────────────────────────────────────┐
│ (3065874883688416519,1634050779997673240) │
└───────────────────────────────────────────┘

```

## wordShingleMinHashCaseInsensitiveUTF8[​](#wordShingleMinHashCaseInsensitiveUTF8 "Direct link to wordShingleMinHashCaseInsensitiveUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into parts (shingles) of `shinglesize` words, calculates hash values for each word shingle and returns a tuple with these hashes.
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case insensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
wordShingleMinHashCaseInsensitiveUTF8(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashCaseInsensitiveUTF8('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Tuple;

```


```
┌─Tuple─────────────────────────────────────┐
│ (3065874883688416519,1634050779997673240) │
└───────────────────────────────────────────┘

```

## wordShingleMinHashUTF8[​](#wordShingleMinHashUTF8 "Direct link to wordShingleMinHashUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into parts (shingles) of `shinglesize` words, calculates hash values for each word shingle and returns a tuple with these hashes.
Uses `hashnum` minimum hashes to calculate the minimum hash and `hashnum` maximum hashes to calculate the maximum hash.
It is case sensitive.


Can be used to detect semi\-duplicate strings with [`tupleHammingDistance`](/docs/sql-reference/functions/tuple-functions#tupleHammingDistance).
For two strings, if the returned hashes are the same for both strings, then those strings are the same.


**Syntax**



```
wordShingleMinHashUTF8(string[, shinglesize, hashnum])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `hashnum` — Optional. The number of minimum and maximum hashes used to calculate the result, any number from `1` to `25`. The default value is `6`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two hashes — the minimum and the maximum. [`Tuple(UInt64, UInt64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT wordShingleMinHashUTF8('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Tuple;

```


```
┌─Tuple──────────────────────────────────────┐
│ (16452112859864147620,5844417301642981317) │
└────────────────────────────────────────────┘

```

## wordShingleSimHash[​](#wordShingleSimHash "Direct link to wordShingleSimHash")


Introduced in: v21\.1\.0


Splits a ASCII string into parts (shingles) of `shinglesize` words and returns the word shingle `simhash`.
Is is case sensitive.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
wordShingleSimHash(string[, shinglesize])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT wordShingleSimHash('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Hash;

```


```
┌───────Hash─┐
│ 2328277067 │
└────────────┘

```

## wordShingleSimHashCaseInsensitive[​](#wordShingleSimHashCaseInsensitive "Direct link to wordShingleSimHashCaseInsensitive")


Introduced in: v21\.1\.0


Splits a ASCII string into parts (shingles) of `shinglesize` words and returns the word shingle `simhash`.
It is case insensitive.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
wordShingleSimHashCaseInsensitive(string[, shinglesize])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT wordShingleSimHashCaseInsensitive('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Hash;

```


```
┌───────Hash─┐
│ 2194812424 │
└────────────┘

```

## wordShingleSimHashCaseInsensitiveUTF8[​](#wordShingleSimHashCaseInsensitiveUTF8 "Direct link to wordShingleSimHashCaseInsensitiveUTF8")


Introduced in: v1\.1\.0


Splits a UTF\-8 encoded string into parts (shingles) of `shinglesize` words and returns the word shingle `simhash`.
It is case insensitive.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
wordShingleSimHashCaseInsensitiveUTF8(string[, shinglesize])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT wordShingleSimHashCaseInsensitiveUTF8('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Hash;

```


```
┌───────Hash─┐
│ 2194812424 │
└────────────┘

```

## wordShingleSimHashUTF8[​](#wordShingleSimHashUTF8 "Direct link to wordShingleSimHashUTF8")


Introduced in: v21\.1\.0


Splits a UTF\-8 string into parts (shingles) of `shinglesize` words and returns the word shingle `simhash`.
It is case sensitive.


Can be used for detection of semi\-duplicate strings with [`bitHammingDistance`](/docs/sql-reference/functions/bit-functions#bitHammingDistance).
The smaller the [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) of the calculated `simhashes` of two strings, the more likely these strings are the same.


**Syntax**



```
wordShingleSimHashUTF8(string[, shinglesize])

```

**Arguments**


- `string` — String for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)
- `shinglesize` — Optional. The size of a word shingle, any number from `1` to `25`. The default value is `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the computed hash value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT wordShingleSimHashUTF8('ClickHouse® is a column-oriented database management system (DBMS) for online analytical processing of queries (OLAP).') AS Hash;

```


```
┌───────Hash─┐
│ 2328277067 │
└────────────┘

```

## wyHash64[​](#wyHash64 "Direct link to wyHash64")


Introduced in: v22\.7\.0


Computes a 64\-bit [wyHash64](https://github.com/wangyi-fudan/wyhash) hash value.


**Syntax**



```
wyHash64(arg)

```

**Arguments**


- `arg` — String argument for which to compute the hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the computed 64\-bit hash value [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT wyHash64('ClickHouse') AS Hash;

```


```
12336419557878201794

```

## xxHash32[​](#xxHash32 "Direct link to xxHash32")


Introduced in: v20\.1\.0


Calculates a [xxHash](http://cyan4973.github.io/xxHash/) from a string.


For the 64\-bit version see [`xxHash64`](#xxHash64)


**Syntax**



```
xxHash32(arg)

```

**Arguments**


- `arg` — Input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the computed 32\-bit hash of the input string. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT xxHash32('Hello, world!');

```


```
┌─xxHash32('Hello, world!')─┐
│                 834093149 │
└───────────────────────────┘

```

## xxHash64[​](#xxHash64 "Direct link to xxHash64")


Introduced in: v20\.1\.0


Calculates a [xxHash](http://cyan4973.github.io/xxHash/) from a string.


For the 32\-bit version see [`xxHash32`](#xxHash32)


**Syntax**



```
xxHash64(arg)

```

**Arguments**


- `arg` — Input string to hash. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the computed 64\-bit hash of the input string. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT xxHash64('Hello, world!');

```


```
┌─xxHash64('Hello, world!')─┐
│      17691043854468224118 │
└───────────────────────────┘

```

## xxh3[​](#xxh3 "Direct link to xxh3")


Introduced in: v22\.12\.0


Computes a [XXH3](https://github.com/Cyan4973/xxHash) 64\-bit hash value.


**Syntax**



```
xxh3(expr)

```

**Arguments**


- `expr` — A list of expressions of any data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed 64\-bit `xxh3` hash value [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT xxh3('ClickHouse')

```


```
18009318874338624809

```

## xxh3\_128[​](#xxh3_128 "Direct link to xxh3_128")


Introduced in: v26\.2\.0


Computes a [XXH3](https://github.com/Cyan4973/xxHash) 128\-bit hash value.


**Syntax**



```
xxh3_128(expr)

```

**Arguments**


- `expr` — A list of expressions of any data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the computed 128\-bit `xxh3` hash value [`UInt128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT hex(xxh3_128('ClickHouse'))

```


```
3A038784C52804B4DBA43A038784C528

```
[PreviousSVG](/docs/sql-reference/functions/geo/svg)[NextIN Operator](/docs/sql-reference/functions/in-functions)- [BLAKE3](#BLAKE3)- [MD4](#MD4)- [MD5](#MD5)- [RIPEMD160](#RIPEMD160)- [SHA1](#SHA1)- [SHA224](#SHA224)- [SHA256](#SHA256)- [SHA384](#SHA384)- [SHA512](#SHA512)- [SHA512\_256](#SHA512_256)- [URLHash](#URLHash)- [cityHash64](#cityHash64)- [farmFingerprint64](#farmFingerprint64)- [farmHash64](#farmHash64)- [gccMurmurHash](#gccMurmurHash)- [halfMD5](#halfMD5)- [hiveHash](#hiveHash)- [icebergHash](#icebergHash)- [intHash32](#intHash32)- [intHash64](#intHash64)- [javaHash](#javaHash)- [javaHashUTF16LE](#javaHashUTF16LE)- [jumpConsistentHash](#jumpConsistentHash)- [kafkaMurmurHash](#kafkaMurmurHash)- [keccak256](#keccak256)- [kostikConsistentHash](#kostikConsistentHash)- [metroHash64](#metroHash64)- [murmurHash2\_32](#murmurHash2_32)- [murmurHash2\_64](#murmurHash2_64)- [murmurHash3\_128](#murmurHash3_128)- [murmurHash3\_32](#murmurHash3_32)- [murmurHash3\_64](#murmurHash3_64)- [ngramMinHash](#ngramMinHash)- [ngramMinHashArg](#ngramMinHashArg)- [ngramMinHashArgCaseInsensitive](#ngramMinHashArgCaseInsensitive)- [ngramMinHashArgCaseInsensitiveUTF8](#ngramMinHashArgCaseInsensitiveUTF8)- [ngramMinHashArgUTF8](#ngramMinHashArgUTF8)- [ngramMinHashCaseInsensitive](#ngramMinHashCaseInsensitive)- [ngramMinHashCaseInsensitiveUTF8](#ngramMinHashCaseInsensitiveUTF8)- [ngramMinHashUTF8](#ngramMinHashUTF8)- [ngramSimHash](#ngramSimHash)- [ngramSimHashCaseInsensitive](#ngramSimHashCaseInsensitive)- [ngramSimHashCaseInsensitiveUTF8](#ngramSimHashCaseInsensitiveUTF8)- [ngramSimHashUTF8](#ngramSimHashUTF8)- [sipHash128](#sipHash128)- [sipHash128Keyed](#sipHash128Keyed)- [sipHash128Reference](#sipHash128Reference)- [sipHash128ReferenceKeyed](#sipHash128ReferenceKeyed)- [sipHash64](#sipHash64)- [sipHash64Keyed](#sipHash64Keyed)- [wordShingleMinHash](#wordShingleMinHash)- [wordShingleMinHashArg](#wordShingleMinHashArg)- [wordShingleMinHashArgCaseInsensitive](#wordShingleMinHashArgCaseInsensitive)- [wordShingleMinHashArgCaseInsensitiveUTF8](#wordShingleMinHashArgCaseInsensitiveUTF8)- [wordShingleMinHashArgUTF8](#wordShingleMinHashArgUTF8)- [wordShingleMinHashCaseInsensitive](#wordShingleMinHashCaseInsensitive)- [wordShingleMinHashCaseInsensitiveUTF8](#wordShingleMinHashCaseInsensitiveUTF8)- [wordShingleMinHashUTF8](#wordShingleMinHashUTF8)- [wordShingleSimHash](#wordShingleSimHash)- [wordShingleSimHashCaseInsensitive](#wordShingleSimHashCaseInsensitive)- [wordShingleSimHashCaseInsensitiveUTF8](#wordShingleSimHashCaseInsensitiveUTF8)- [wordShingleSimHashUTF8](#wordShingleSimHashUTF8)- [wyHash64](#wyHash64)- [xxHash32](#xxHash32)- [xxHash64](#xxHash64)- [xxh3](#xxh3)- [xxh3\_128](#xxh3_128)
Was this page helpful?

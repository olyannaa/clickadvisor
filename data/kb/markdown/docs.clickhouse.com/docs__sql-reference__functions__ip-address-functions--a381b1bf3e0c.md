# Functions for working with IPv4 and IPv6 addresses \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- IP Addresses
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/ip-address-functions.md)# Functions for working with IPv4 and IPv6 addresses

## IPv4CIDRToRange[​](#IPv4CIDRToRange "Direct link to IPv4CIDRToRange")


Introduced in: v20\.1\.0


Takes an IPv4 address with its Classless Inter\-Domain Routing (CIDR) prefix length and returns the subnet's address range as a tuple of two IPv4 values: the first and last addresses in that subnet.
For the IPv6 version see [`IPv6CIDRToRange`](#IPv4CIDRToRange).


**Syntax**



```
IPv4CIDRToRange(ipv4, cidr)

```

**Arguments**


- `ipv4` — IPv4 address. [`IPv4`](/docs/sql-reference/data-types/ipv4) or [`String`](/docs/sql-reference/data-types/string)
- `cidr` — CIDR value. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two IPv4 addresses representing the subnet range. [`Tuple(IPv4, IPv4)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT IPv4CIDRToRange(toIPv4('192.168.5.2'), 16);

```


```
┌─IPv4CIDRToRange(toIPv4('192.168.5.2'), 16)─┐
│ ('192.168.0.0','192.168.255.255')          │
└────────────────────────────────────────────┘

```

## IPv4NumToString[​](#IPv4NumToString "Direct link to IPv4NumToString")


Introduced in: v1\.1\.0


Converts a 32\-bit integer to its IPv4 address string representation in dotted decimal notation (A.B.C.D format).
Interprets the input using big\-endian byte ordering.


**Syntax**



```
IPv4NumToString(num)

```

**Aliases**: `INET_NTOA`


**Arguments**


- `num` — IPv4 address as UInt32 number. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a number representing the MAC address, or `0` if the format is invalid. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
IPv4NumToString(3232235521)

```


```
192.168.0.1

```

## IPv4NumToStringClassC[​](#IPv4NumToStringClassC "Direct link to IPv4NumToStringClassC")


Introduced in: v1\.1\.0


Converts a 32\-bit integer to its IPv4 address string representation in dotted decimal notation (A.B.C.D format),
similar to [`IPv4NumToString`](#IPv4NumToString) but using `xxx` instead of the last octet.


**Syntax**



```
IPv4NumToStringClassC(num)

```

**Arguments**


- `num` — IPv4 address as UInt32 number. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the IPv4 address string with xxx replacing the last octet. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic example with aggregation**



```
SELECT
    IPv4NumToStringClassC(ClientIP) AS k,
    count() AS c
FROM test.hits
GROUP BY k
ORDER BY c DESC
LIMIT 10

```


```
┌─k──────────────┬─────c─┐
│ 83.149.9.xxx   │ 26238 │
│ 217.118.81.xxx │ 26074 │
│ 213.87.129.xxx │ 25481 │
│ 83.149.8.xxx   │ 24984 │
│ 217.118.83.xxx │ 22797 │
│ 78.25.120.xxx  │ 22354 │
│ 213.87.131.xxx │ 21285 │
│ 78.25.121.xxx  │ 20887 │
│ 188.162.65.xxx │ 19694 │
│ 83.149.48.xxx  │ 17406 │
└────────────────┴───────┘

```

## IPv4StringToNum[​](#IPv4StringToNum "Direct link to IPv4StringToNum")


Introduced in: v1\.1\.0


Converts an IPv4 address string in dotted decimal notation (A.B.C.D format) to its corresponding 32\-bit integer representation. (The reverse of [`IPv4NumToString`](#IPv4NumToString)).
If the IPv4 address has an invalid format, an exception is thrown.


**Syntax**



```
IPv4StringToNum(string)

```

**Aliases**: `INET_ATON`


**Arguments**


- `string` — IPv4 address string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns theIPv4 address. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
IPv4StringToNum('192.168.0.1')

```


```
3232235521

```

## IPv4StringToNumOrDefault[​](#IPv4StringToNumOrDefault "Direct link to IPv4StringToNumOrDefault")


Introduced in: v22\.3\.0


Converts an IPv4 address string in dotted decimal notation (A.B.C.D format) to its corresponding 32\-bit integer representation but if the IPv4 address has an invalid format, it returns `0`.


**Syntax**



```
IPv4StringToNumOrDefault(string)

```

**Arguments**


- `string` — IPv4 address string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the IPv4 address, or `0` if invalid. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Example with an invalid address**



```
SELECT
    IPv4StringToNumOrDefault('127.0.0.1') AS valid,
    IPv4StringToNumOrDefault('invalid') AS invalid;

```


```
┌──────valid─┬─invalid─┐
│ 2130706433 │       0 │
└────────────┴─────────┘

```

## IPv4StringToNumOrNull[​](#IPv4StringToNumOrNull "Direct link to IPv4StringToNumOrNull")


Introduced in: v22\.3\.0


Converts a 32\-bit integer to its IPv4 address string representation in dotted decimal notation (A.B.C.D format) but if the IPv4 address has an invalid format, it returns `NULL`.


**Syntax**



```
IPv4StringToNumOrNull(string)

```

**Arguments**


- `string` — IPv4 address string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the IPv4 address, or `NULL` if invalid. [`Nullable(UInt32)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Example with an invalid address**



```
SELECT
IPv4StringToNumOrNull('127.0.0.1') AS valid,
IPv4StringToNumOrNull('invalid') AS invalid;

```


```
┌──────valid─┬─invalid─┐
│ 2130706433 │    ᴺᵁᴸᴸ │
└────────────┴─────────┘

```

## IPv4ToIPv6[​](#IPv4ToIPv6 "Direct link to IPv4ToIPv6")


Introduced in: v1\.1\.0


Interprets a (big endian) 32\-bit number as an IPv4 address, which is then interpreted as the corresponding IPv6 address in `FixedString(16)` format.


**Syntax**



```
IPv4ToIPv6(x)

```

**Arguments**


- `x` — IPv4 address. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an IPv6 address in binary format. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT IPv6NumToString(IPv4ToIPv6(IPv4StringToNum('192.168.0.1'))) AS addr;

```


```
┌─addr───────────────┐
│ ::ffff:192.168.0.1 │
└────────────────────┘

```

## IPv6CIDRToRange[​](#IPv6CIDRToRange "Direct link to IPv6CIDRToRange")


Introduced in: v20\.1\.0


Takes an IPv6 address with its Classless Inter\-Domain Routing (CIDR) prefix length and returns the subnet's address range as a tuple of two IPv6 values: the lowest and highest addresses in that subnet.
For the IPv4 version see [`IPv4CIDRToRange`](#IPv4CIDRToRange).


**Syntax**



```
IPv6CIDRToRange(ipv6, cidr)

```

**Arguments**


- `ipv6` — IPv6 address. [`IPv6`](/docs/sql-reference/data-types/ipv6) or [`String`](/docs/sql-reference/data-types/string)
- `cidr` — CIDR value. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two IPv6 addresses representing the subnet range. [`Tuple(IPv6, IPv6)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT IPv6CIDRToRange(toIPv6('2001:0db8:0000:85a3:0000:0000:ac1f:8001'), 32);

```


```
┌─IPv6CIDRToRange(toIPv6('2001:0db8:0000:85a3:0000:0000:ac1f:8001'), 32)─┐
│ ('2001:db8::','2001:db8:ffff:ffff:ffff:ffff:ffff:ffff')                │
└────────────────────────────────────────────────────────────────────────┘

```

## IPv6NumToString[​](#IPv6NumToString "Direct link to IPv6NumToString")


Introduced in: v1\.1\.0


Converts an IPv6 address from binary format (FixedString(16\)) to its standard text representation.
IPv4\-mapped IPv6 addresses are displayed in the format `::ffff:111.222.33.44`.


**Syntax**



```
IPv6NumToString(x)

```

**Aliases**: `INET6_NTOA`


**Arguments**


- `x` — IPv6 address in binary format. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring) or [`IPv6`](/docs/sql-reference/data-types/ipv6)


**Returned value**


Returns the IPv6 address string in text format. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT IPv6NumToString(toFixedString(unhex('2A0206B8000000000000000000000011'), 16)) AS addr;

```


```
┌─addr─────────┐
│ 2a02:6b8::11 │
└──────────────┘

```

**IPv6 with hits analysis**



```
SELECT
    IPv6NumToString(ClientIP6 AS k),
    count() AS c
FROM hits_all
WHERE EventDate = today() AND substring(ClientIP6, 1, 12) != unhex('00000000000000000000FFFF')
GROUP BY k
ORDER BY c DESC
LIMIT 10

```


```
┌─IPv6NumToString(ClientIP6)──────────────┬─────c─┐
│ 2a02:2168:aaa:bbbb::2                   │ 24695 │
│ 2a02:2698:abcd:abcd:abcd:abcd:8888:5555 │ 22408 │
│ 2a02:6b8:0:fff::ff                      │ 16389 │
│ 2a01:4f8:111:6666::2                    │ 16016 │
│ 2a02:2168:888:222::1                    │ 15896 │
│ 2a01:7e00::ffff:ffff:ffff:222           │ 14774 │
│ 2a02:8109:eee:ee:eeee:eeee:eeee:eeee    │ 14443 │
│ 2a02:810b:8888:888:8888:8888:8888:8888  │ 14345 │
│ 2a02:6b8:0:444:4444:4444:4444:4444      │ 14279 │
│ 2a01:7e00::ffff:ffff:ffff:ffff          │ 13880 │
└─────────────────────────────────────────┴───────┘

```

**IPv6 mapped IPv4 addresses**



```
SELECT
    IPv6NumToString(ClientIP6 AS k),
    count() AS c
FROM hits_all
WHERE EventDate = today()
GROUP BY k
ORDER BY c DESC
LIMIT 10

```


```
┌─IPv6NumToString(ClientIP6)─┬──────c─┐
│ ::ffff:94.26.111.111       │ 747440 │
│ ::ffff:37.143.222.4        │ 529483 │
│ ::ffff:5.166.111.99        │ 317707 │
│ ::ffff:46.38.11.77         │ 263086 │
│ ::ffff:79.105.111.111      │ 186611 │
│ ::ffff:93.92.111.88        │ 176773 │
│ ::ffff:84.53.111.33        │ 158709 │
│ ::ffff:217.118.11.22       │ 154004 │
│ ::ffff:217.118.11.33       │ 148449 │
│ ::ffff:217.118.11.44       │ 148243 │
└────────────────────────────┴────────┘

```

## IPv6StringToNum[​](#IPv6StringToNum "Direct link to IPv6StringToNum")


Introduced in: v1\.1\.0


Converts an IPv6 address from its standard text representation to binary format (`FixedString(16)`).
Accepts IPv4\-mapped IPv6 addresses in the format `::ffff:111.222.33.44.`.
If the IPv6 address has an invalid format, an exception is thrown.


If the input string contains a valid IPv4 address, returns its IPv6 equivalent.
HEX can be uppercase or lowercase.


**Syntax**



```
IPv6StringToNum(string)

```

**Aliases**: `INET6_ATON`


**Arguments**


- `string` — IPv6 address string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns theIPv6 address in binary format. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Basic example**



```
SELECT addr, cutIPv6(IPv6StringToNum(addr), 0, 0) FROM (SELECT ['notaddress', '127.0.0.1', '1111::ffff'] AS addr) ARRAY JOIN addr;

```


```
┌─addr───────┬─cutIPv6(IPv6StringToNum(addr), 0, 0)─┐
│ notaddress │ ::                                   │
│ 127.0.0.1  │ ::ffff:127.0.0.1                     │
│ 1111::ffff │ 1111::ffff                           │
└────────────┴──────────────────────────────────────┘

```

## IPv6StringToNumOrDefault[​](#IPv6StringToNumOrDefault "Direct link to IPv6StringToNumOrDefault")


Introduced in: v22\.3\.0


Converts an IPv6 address from its standard text representation to binary format (`FixedString(16)`).
Accepts IPv4\-mapped IPv6 addresses in the format `::ffff:111.222.33.44.`.
If the IPv6 address has an invalid format, it returns the default value `::`.


**Syntax**



```
IPv6StringToNumOrDefault(string)

```

**Arguments**


- `string` — IPv6 address string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


IPv6 address in binary format, or zero\-filled FixedString(16\) if invalid. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Basic example with invalid address**



```
SELECT
    IPv6NumToString(IPv6StringToNumOrDefault('2001:db8::1')) AS valid,
    IPv6NumToString(IPv6StringToNumOrDefault('invalid')) AS invalid;

```


```
┌─valid───────┬─invalid─┐
│ 2001:db8::1 │ ::      │
└─────────────┴─────────┘

```

## IPv6StringToNumOrNull[​](#IPv6StringToNumOrNull "Direct link to IPv6StringToNumOrNull")


Introduced in: v22\.3\.0


Converts an IPv6 address from its standard text representation to binary format (`FixedString(16)`).
Accepts IPv4\-mapped IPv6 addresses in the format `::ffff:111.222.33.44.`.
If the IPv6 address has an invalid format, it returns `NULL`.


**Syntax**



```
IPv6StringToNumOrNull(string)

```

**Arguments**


- `string` — IPv6 address string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns IPv6 address in binary format, or `NULL` if invalid. [`Nullable(FixedString(16))`](/docs/sql-reference/data-types/nullable)


**Examples**


**Basic example with invalid address**



```
SELECT
    IPv6NumToString(IPv6StringToNumOrNull('2001:db8::1')) AS valid,
    IPv6StringToNumOrNull('invalid') AS invalid;

```


```
┌─valid───────┬─invalid─┐
│ 2001:db8::1 │    ᴺᵁᴸᴸ │
└─────────────┴─────────┘

```

## cutIPv6[​](#cutIPv6 "Direct link to cutIPv6")


Introduced in: v1\.1\.0


Accepts a `FixedString(16)` value containing the IPv6 address in binary format.
Returns a string containing the address of the specified number of bytes removed in text format.


**Syntax**



```
cutIPv6(x, bytesToCutForIPv6, bytesToCutForIPv4)

```

**Arguments**


- `x` — IPv6 address in binary format. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring) or [`IPv6`](/docs/sql-reference/data-types/ipv6)
- `bytesToCutForIPv6` — Number of bytes to cut for IPv6\. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `bytesToCutForIPv4` — Number of bytes to cut for IPv4\. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a string containing the IPv6 address in text format with specified bytes removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
WITH
    IPv6StringToNum('2001:0DB8:AC10:FE01:FEED:BABE:CAFE:F00D') AS ipv6,
    IPv4ToIPv6(IPv4StringToNum('192.168.0.1')) AS ipv4
SELECT
    cutIPv6(ipv6, 2, 0),
    cutIPv6(ipv4, 0, 2)

```


```
┌─cutIPv6(ipv6, 2, 0)─────────────────┬─cutIPv6(ipv4, 0, 2)─┐
│ 2001:db8:ac10:fe01:feed:babe:cafe:0 │ ::ffff:192.168.0.0  │
└─────────────────────────────────────┴─────────────────────┘

```

## isIPAddressInRange[​](#isIPAddressInRange "Direct link to isIPAddressInRange")


Introduced in: v21\.4\.0


Determines if an IP address is contained in a network represented in the [Classless Inter\-Domain Routing (CIDR)](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation.


This function accepts both IPv4 and IPv6 addresses (and networks) represented as strings. It returns `0` if the IP version of the address and the CIDR don't match.


**Syntax**



```
isIPAddressInRange(address, prefix)

```

**Arguments**


- `address` — An IPv4 or IPv6 address. [`String`](/docs/sql-reference/data-types/string)
- `prefix` — An IPv4 or IPv6 network prefix in CIDR. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the IP version of the address and the CIDR match, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**IPv4 address in range**



```
SELECT isIPAddressInRange('127.0.0.1', '127.0.0.0/8')

```


```
1

```

**IPv4 address not in range**



```
SELECT isIPAddressInRange('127.0.0.1', 'ffff::/16')

```


```
0

```

**IPv6 address not in range**



```
SELECT isIPAddressInRange('::ffff:192.168.0.1', '::ffff:192.168.0.4/128')

```


```
0

```

## isIPv4String[​](#isIPv4String "Direct link to isIPv4String")


Introduced in: v21\.1\.0


Determines whether the input string is an IPv4 address or not.
For the IPv6 version see [`isIPv6String`](#isIPv6String).


**Syntax**



```
isIPv4String(string)

```

**Arguments**


- `string` — IP address string to check. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `string` is IPv4 address, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT addr, isIPv4String(addr)
FROM(
SELECT ['0.0.0.0', '127.0.0.1', '::ffff:127.0.0.1'] AS addr
)
ARRAY JOIN addr;

```


```
┌─addr─────────────┬─isIPv4String(addr)─┐
│ 0.0.0.0          │                  1 │
│ 127.0.0.1        │                  1 │
│ ::ffff:127.0.0.1 │                  0 │
└──────────────────┴────────────────────┘

```

## isIPv6String[​](#isIPv6String "Direct link to isIPv6String")


Introduced in: v21\.1\.0


Determines whether the input string is an IPv6 address or not.
For the IPv4 version see [`isIPv4String`](#isIPv4String).


**Syntax**



```
isIPv6String(string)

```

**Arguments**


- `string` — IP address string to check. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `string` is IPv6 address, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT addr, isIPv6String(addr)
FROM(SELECT ['::', '1111::ffff', '::ffff:127.0.0.1', '127.0.0.1'] AS addr)
ARRAY JOIN addr;

```


```
┌─addr─────────────┬─isIPv6String(addr)─┐
│ ::               │                  1 │
│ 1111::ffff       │                  1 │
│ ::ffff:127.0.0.1 │                  1 │
│ 127.0.0.1        │                  0 │
└──────────────────┴────────────────────┘

```

## toIPv4[​](#toIPv4 "Direct link to toIPv4")


Introduced in: v20\.1\.0


Converts a string or a UInt32 form of IPv4 address to type IPv4\.
It is similar to [`IPv4StringToNum`](/docs/sql-reference/functions/ip-address-functions#IPv4StringToNum) and [`IPv4NumToString`](/docs/sql-reference/functions/ip-address-functions#IPv4NumToString) functions but it supports both string and unsigned integer data types as input arguments.


**Syntax**



```
toIPv4(x)

```

**Arguments**


- `x` — An IPv4 address [`String`](/docs/sql-reference/data-types/string) or [`UInt8/16/32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an IPv4 address. [`IPv4`](/docs/sql-reference/data-types/ipv4)


**Examples**


**Usage example**



```
SELECT toIPv4('171.225.130.45');

```


```
┌─toIPv4('171.225.130.45')─┐
│ 171.225.130.45           │
└──────────────────────────┘

```

**Comparison with IPv4StringToNum and IPv4NumToString functions.**



```
WITH
    '171.225.130.45' AS IPv4_string
SELECT
    hex(IPv4StringToNum(IPv4_string)),
    hex(toIPv4(IPv4_string))

```


```
┌─hex(IPv4StringToNum(IPv4_string))─┬─hex(toIPv4(IPv4_string))─┐
│ ABE1822D                          │ ABE1822D                 │
└───────────────────────────────────┴──────────────────────────┘

```

**Conversion from an integer**



```
SELECT toIPv4(2130706433);

```


```
┌─toIPv4(2130706433)─┐
│ 127.0.0.1          │
└────────────────────┘

```

## toIPv4OrDefault[​](#toIPv4OrDefault "Direct link to toIPv4OrDefault")


Introduced in: v22\.3\.0


Converts a string or a UInt32 form of an IPv4 address to [`IPv4`](/docs/sql-reference/data-types/ipv4) type.
If the IPv4 address has an invalid format, it returns `0.0.0.0` (0 IPv4\), or the provided IPv4 default.


**Syntax**



```
toIPv4OrDefault(string[, default])

```

**Arguments**


- `string` — IP address string to convert. [`String`](/docs/sql-reference/data-types/string)
- `default` — Optional. The value to return if string is an invalid IPv4 address. [`IPv4`](/docs/sql-reference/data-types/ipv4)


**Returned value**


Returns a string converted to the current IPv4 address, or the default value if conversion fails. [`IPv4`](/docs/sql-reference/data-types/ipv4)


**Examples**


**Valid and invalid IPv4 strings**



```
WITH
    '192.168.1.1' AS valid_IPv4_string,
    '999.999.999.999' AS invalid_IPv4_string,
    'not_an_ip' AS malformed_string
SELECT
    toIPv4OrDefault(valid_IPv4_string) AS valid,
    toIPv4OrDefault(invalid_IPv4_string) AS default_value,
    toIPv4OrDefault(malformed_string, toIPv4('8.8.8.8')) AS provided_default;

```


```
┌─valid─────────┬─default_value─┬─provided_default─┐
│ 192.168.1.1   │ 0.0.0.0       │ 8.8.8.8          │
└───────────────┴───────────────┴──────────────────┘

```

## toIPv4OrNull[​](#toIPv4OrNull "Direct link to toIPv4OrNull")


Introduced in: v22\.3\.0


Converts an input value to a value of type `IPv4` but returns `NULL` in case of an error.
Like [`toIPv4`](#toIPv4) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- String representations of IPv4 addresses in dotted decimal notation.
- Integer representations of IPv4 addresses.


Unsupported arguments (return `NULL`):


- Invalid IP address formats.
- IPv6 addresses.
- Out\-of\-range values.
- Malformed addresses.


**Syntax**



```
toIPv4OrNull(x)

```

**Arguments**


- `x` — A string or integer representation of an IPv4 address. [`String`](/docs/sql-reference/data-types/string) or [`Integer`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an IPv4 address if successful, otherwise `NULL`. [`IPv4`](/docs/sql-reference/data-types/ipv4) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toIPv4OrNull('192.168.1.1') AS valid_ip,
    toIPv4OrNull('invalid.ip') AS invalid_ip

```


```
┌─valid_ip────┬─invalid_ip─┐
│ 192.168.1.1 │       ᴺᵁᴸᴸ │
└─────────────┴────────────┘

```

## toIPv4OrZero[​](#toIPv4OrZero "Direct link to toIPv4OrZero")


Introduced in: v23\.1\.0


Converts an input value to a value of type [IPv4](/docs/sql-reference/data-types/ipv4) but returns zero IPv4 address in case of an error.
Like [`toIPv4`](#toIPv4) but returns zero IPv4 address (`0.0.0.0`) instead of throwing an exception on conversion errors.


Supported arguments:


- String representations of IPv4 addresses in dotted decimal notation.
- Integer representations of IPv4 addresses.


Unsupported arguments (return zero IPv4\):


- Invalid IP address formats.
- IPv6 addresses.
- Out\-of\-range values.


**Syntax**



```
toIPv4OrZero(x)

```

**Arguments**


- `x` — A string or integer representation of an IPv4 address. [`String`](/docs/sql-reference/data-types/string) or [`Integer`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an IPv4 address if successful, otherwise zero IPv4 address (`0.0.0.0`). [`IPv4`](/docs/sql-reference/data-types/ipv4)


**Examples**


**Usage example**



```
SELECT
    toIPv4OrZero('192.168.1.1') AS valid_ip,
    toIPv4OrZero('invalid.ip') AS invalid_ip

```


```
┌─valid_ip────┬─invalid_ip─┐
│ 192.168.1.1 │ 0.0.0.0    │
└─────────────┴────────────┘

```

## toIPv6[​](#toIPv6 "Direct link to toIPv6")


Introduced in: v20\.1\.0


onverts a string or a `UInt128` form of IPv6 address to [`IPv6`](/docs/sql-reference/data-types/ipv6) type.
For strings, if the IPv6 address has an invalid format, returns an empty value.
Similar to [`IPv6StringToNum`](/docs/sql-reference/functions/ip-address-functions#IPv6StringToNum) and [`IPv6NumToString`](/docs/sql-reference/functions/ip-address-functions#IPv6NumToString) functions, which convert IPv6 address to and from binary format (i.e. `FixedString(16)`).


If the input string contains a valid IPv4 address, then the IPv6 equivalent of the IPv4 address is returned.


**Syntax**



```
toIPv6(x)

```

**Arguments**


- `x` — An IP address. [`String`](/docs/sql-reference/data-types/string) or [`UInt128`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an IPv6 address. [`IPv6`](/docs/sql-reference/data-types/ipv6)


**Examples**


**Usage example**



```
WITH '2001:438:ffff::407d:1bc1' AS IPv6_string
SELECT
    hex(IPv6StringToNum(IPv6_string)),
    hex(toIPv6(IPv6_string));

```


```
┌─hex(IPv6StringToNum(IPv6_string))─┬─hex(toIPv6(IPv6_string))─────────┐
│ 20010438FFFF000000000000407D1BC1  │ 20010438FFFF000000000000407D1BC1 │
└───────────────────────────────────┴──────────────────────────────────┘

```

**IPv4\-to\-IPv6 mapping**



```
SELECT toIPv6('127.0.0.1');

```


```
┌─toIPv6('127.0.0.1')─┐
│ ::ffff:127.0.0.1    │
└─────────────────────┘

```

## toIPv6OrDefault[​](#toIPv6OrDefault "Direct link to toIPv6OrDefault")


Introduced in: v22\.3\.0


Converts a string or a UInt128 form of IPv6 address to [`IPv6`](/docs/sql-reference/data-types/ipv6) type.
If the IPv6 address has an invalid format, it returns `::` (0 IPv6\) or the provided IPv6 default.


**Syntax**



```
toIPv6OrDefault(string[, default])

```

**Arguments**


- `string` — IP address string to convert. \- `default` — Optional. The value to return if string has an invalid format.


**Returned value**


Returns the IPv6 address, otherwise `::` or the provided optional default if argument `string` has an invalid format. [`IPv6`](/docs/sql-reference/data-types/ipv6)


**Examples**


**Valid and invalid IPv6 strings**



```
WITH
    '2001:0db8:85a3:0000:0000:8a2e:0370:7334' AS valid_IPv6_string,
    '2001:0db8:85a3::8a2e:370g:7334' AS invalid_IPv6_string,
    'not_an_ipv6' AS malformed_string
SELECT
    toIPv6OrDefault(valid_IPv6_string) AS valid,
    toIPv6OrDefault(invalid_IPv6_string) AS default_value,
    toIPv6OrDefault(malformed_string, toIPv6('::1')) AS provided_default;

```


```
┌─valid──────────────────────────────────┬─default_value─┬─provided_default─┐
│ 2001:db8:85a3::8a2e:370:7334           │ ::            │ ::1              │
└────────────────────────────────────────┴───────────────┴──────────────────┘

```

## toIPv6OrNull[​](#toIPv6OrNull "Direct link to toIPv6OrNull")


Introduced in: v22\.3\.0


Converts an input value to a value of type `IPv6` but returns `NULL` in case of an error.
Like [`toIPv6`](#toIPv6) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- String representations of IPv6 addresses in standard notation.
- String representations of IPv4 addresses (converted to IPv4\-mapped IPv6\).
- Binary representations of IPv6 addresses.


Unsupported arguments (return `NULL`):


- Invalid IP address formats.
- Malformed IPv6 addresses.
- Out\-of\-range values.
- Invalid notation.


**Syntax**



```
toIPv6OrNull(x)

```

**Arguments**


- `x` — A string representation of an IPv6 or IPv4 address. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an IPv6 address if successful, otherwise `NULL`. [`IPv6`](/docs/sql-reference/data-types/ipv6) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toIPv6OrNull('2001:0db8:85a3:0000:0000:8a2e:0370:7334') AS valid_ipv6,
    toIPv6OrNull('invalid::ip') AS invalid_ipv6

```


```
┌─valid_ipv6──────────────────────────┬─invalid_ipv6─┐
│ 2001:db8:85a3::8a2e:370:7334        │         ᴺᵁᴸᴸ │
└─────────────────────────────────────┴──────────────┘

```

## toIPv6OrZero[​](#toIPv6OrZero "Direct link to toIPv6OrZero")


Introduced in: v23\.1\.0


Converts an input value to a value of type [IPv6](/docs/sql-reference/data-types/ipv6) but returns zero IPv6 address in case of an error.
Like [`toIPv6`](#toIPv6) but returns zero IPv6 address (`::`) instead of throwing an exception on conversion errors.


Supported arguments:


- String representations of IPv6 addresses in standard notation.
- String representations of IPv4 addresses (converted to IPv4\-mapped IPv6\).
- Binary representations of IPv6 addresses.


Unsupported arguments (return zero IPv6\):


- Invalid IP address formats.
- Malformed IPv6 addresses.
- Out\-of\-range values.


**Syntax**



```
toIPv6OrZero(x)

```

**Arguments**


- `x` — A string representation of an IPv6 or IPv4 address. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an IPv6 address if successful, otherwise zero IPv6 address (`::`). [`IPv6`](/docs/sql-reference/data-types/ipv6)


**Examples**


**Usage example**



```
SELECT
    toIPv6OrZero('2001:0db8:85a3:0000:0000:8a2e:0370:7334') AS valid_ipv6,
    toIPv6OrZero('invalid::ip') AS invalid_ipv6

```


```
┌─valid_ipv6──────────────────────────┬─invalid_ipv6─┐
│ 2001:db8:85a3::8a2e:370:7334        │ ::           │
└─────────────────────────────────────┴──────────────┘

```
[PreviousIntrospection](/docs/sql-reference/functions/introspection)[NextJSON](/docs/sql-reference/functions/json-functions)- [IPv4CIDRToRange](#IPv4CIDRToRange)- [IPv4NumToString](#IPv4NumToString)- [IPv4NumToStringClassC](#IPv4NumToStringClassC)- [IPv4StringToNum](#IPv4StringToNum)- [IPv4StringToNumOrDefault](#IPv4StringToNumOrDefault)- [IPv4StringToNumOrNull](#IPv4StringToNumOrNull)- [IPv4ToIPv6](#IPv4ToIPv6)- [IPv6CIDRToRange](#IPv6CIDRToRange)- [IPv6NumToString](#IPv6NumToString)- [IPv6StringToNum](#IPv6StringToNum)- [IPv6StringToNumOrDefault](#IPv6StringToNumOrDefault)- [IPv6StringToNumOrNull](#IPv6StringToNumOrNull)- [cutIPv6](#cutIPv6)- [isIPAddressInRange](#isIPAddressInRange)- [isIPv4String](#isIPv4String)- [isIPv6String](#isIPv6String)- [toIPv4](#toIPv4)- [toIPv4OrDefault](#toIPv4OrDefault)- [toIPv4OrNull](#toIPv4OrNull)- [toIPv4OrZero](#toIPv4OrZero)- [toIPv6](#toIPv6)- [toIPv6OrDefault](#toIPv6OrDefault)- [toIPv6OrNull](#toIPv6OrNull)- [toIPv6OrZero](#toIPv6OrZero)
Was this page helpful?

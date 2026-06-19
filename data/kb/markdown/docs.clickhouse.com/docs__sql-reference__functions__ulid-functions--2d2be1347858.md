# Functions for working with ULIDs \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- ULIDs
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/ulid-functions.md)# Functions for working with ULIDs

NoteThe documentation below is generated from the `system.functions` system table.


## ULIDStringToDateTime[​](#ULIDStringToDateTime "Direct link to ULIDStringToDateTime")


Introduced in: v23\.3\.0


This function extracts the timestamp from a [ULID](https://github.com/ulid/spec).


**Syntax**



```
ULIDStringToDateTime(ulid[, timezone])

```

**Arguments**


- `ulid` — Input ULID. [`String`](/docs/sql-reference/data-types/string) or [`FixedString(26)`](/docs/sql-reference/data-types/fixedstring)
- `timezone` — Optional. Timezone name for the returned value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Timestamp with milliseconds precision. [`DateTime64(3)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT ULIDStringToDateTime('01GNB2S2FGN2P93QPXDNB4EN2R')

```


```
┌─ULIDStringToDateTime('01GNB2S2FGN2P93QPXDNB4EN2R')─┐
│                            2022-12-28 00:40:37.616 │
└────────────────────────────────────────────────────┘

```

## generateULID[​](#generateULID "Direct link to generateULID")


Introduced in: v23\.2\.0


Generates a [Universally Unique Lexicographically Sortable Identifier (ULID)](https://github.com/ulid/spec).


**Syntax**



```
generateULID([x])

```

**Arguments**


- `x` — Optional. An expression resulting in any of the supported data types. The resulting value is discarded, but the expression itself if used for bypassing [common subexpression elimination](/docs/sql-reference/functions/overview#common-subexpression-elimination) if the function is called multiple times in one query. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a ULID. [`FixedString(26)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT generateULID()

```


```
┌─generateULID()─────────────┐
│ 01GNB2S2FGN2P93QPXDNB4EN2R │
└────────────────────────────┘

```

**Usage example if it is needed to generate multiple values in one row**



```
SELECT generateULID(1), generateULID(2)

```


```
┌─generateULID(1)────────────┬─generateULID(2)────────────┐
│ 01GNB2SGG4RHKVNT9ZGA4FFMNP │ 01GNB2SGG4V0HMQVH4VBVPSSRB │
└────────────────────────────┴────────────────────────────┘

```

## See also[​](#see-also "Direct link to See also")


- [UUID](/docs/sql-reference/functions/uuid-functions)
[PreviousUDF](/docs/sql-reference/functions/udf)[NextuniqTheta](/docs/sql-reference/functions/uniqtheta-functions)- [ULIDStringToDateTime](#ULIDStringToDateTime)- [generateULID](#generateULID)- [See also](#see-also)
Was this page helpful?

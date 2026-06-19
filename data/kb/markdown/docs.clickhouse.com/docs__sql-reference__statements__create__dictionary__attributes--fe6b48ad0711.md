# Dictionary attributes \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- Attributes
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/attributes.md)# Dictionary attributes

TipIf you are using a dictionary with ClickHouse Cloud please use the DDL query option to create your dictionaries, and create your dictionary as user `default`.
Also, verify the list of supported dictionary sources in the [Cloud Compatibility guide](/docs/whats-new/cloud-compatibility).


The `structure` clause describes the dictionary key and fields available for queries.


XML description:



```
<dictionary>
    <structure>
        <id>
            <name>Id</name>
        </id>

        <attribute>
            <!-- Attribute parameters -->
        </attribute>

        ...

    </structure>
</dictionary>

```

Attributes are described in the elements:


- `<id>` — Key column
- `<attribute>` — Data column: there can be a multiple number of attributes.


DDL query:



```
CREATE DICTIONARY dict_name (
    Id UInt64,
    -- attributes
)
PRIMARY KEY Id
...

```

Attributes are described in the query body:


- `PRIMARY KEY` — Key column
- `AttrName AttrType` — Data column. There can be a multiple number of attributes.


## Key[​](#key "Direct link to Key")


ClickHouse supports the following types of keys:


- Numeric key. `UInt64`. Defined in the `<id>` tag or using `PRIMARY KEY` keyword.
- Composite key. Set of values of different types. Defined in the tag `<key>` or `PRIMARY KEY` keyword.


An xml structure can contain either `<id>` or `<key>`. DDL\-query must contain single `PRIMARY KEY`.


NoteYou must not describe key as an attribute.


### Numeric Key[​](#numeric-key "Direct link to Numeric Key")


Type: `UInt64`.


Configuration example:



```
<id>
    <name>Id</name>
</id>

```

Configuration fields:


- `name` – The name of the column with keys.


For DDL\-query:



```
CREATE DICTIONARY (
    Id UInt64,
    ...
)
PRIMARY KEY Id
...

```

- `PRIMARY KEY` – The name of the column with keys.


### Composite Key[​](#composite-key "Direct link to Composite Key")


The key can be a `tuple` from any types of fields. The [layout](/docs/sql-reference/statements/create/dictionary/layouts) in this case must be `complex_key_hashed` or `complex_key_cache`.


TipA composite key can consist of a single element. This makes it possible to use a string as the key, for instance.


The key structure is set in the element `<key>`. Key fields are specified in the same format as the dictionary [attributes](#attributes). Example:



```
<structure>
    <key>
        <attribute>
            <name>field1</name>
            <type>String</type>
        </attribute>
        <attribute>
            <name>field2</name>
            <type>UInt32</type>
        </attribute>
        ...
    </key>
...

```

or



```
CREATE DICTIONARY (
    field1 String,
    field2 UInt32
    ...
)
PRIMARY KEY field1, field2
...

```

For a query to the `dictGet*` function, a tuple is passed as the key. Example: `dictGetString('dict_name', 'attr_name', tuple('string for field1', num_for_field2))`.


## Attributes[​](#attributes "Direct link to Attributes")


Configuration example:



```
<structure>
    ...
    <attribute>
        <name>Name</name>
        <type>ClickHouseDataType</type>
        <null_value></null_value>
        <expression>rand64()</expression>
        <hierarchical>true</hierarchical>
        <injective>true</injective>
        <is_object_id>true</is_object_id>
    </attribute>
</structure>

```

or



```
CREATE DICTIONARY somename (
    Name ClickHouseDataType DEFAULT '' EXPRESSION rand64() HIERARCHICAL INJECTIVE IS_OBJECT_ID
)

```

Configuration fields:




| Tag Description Required| `name` Column name. Yes| `type` ClickHouse data type: [UInt8](/docs/sql-reference/data-types/int-uint), [UInt16](/docs/sql-reference/data-types/int-uint), [UInt32](/docs/sql-reference/data-types/int-uint), [UInt64](/docs/sql-reference/data-types/int-uint), [Int8](/docs/sql-reference/data-types/int-uint), [Int16](/docs/sql-reference/data-types/int-uint), [Int32](/docs/sql-reference/data-types/int-uint), [Int64](/docs/sql-reference/data-types/int-uint), [Float32](/docs/sql-reference/data-types/float), [Float64](/docs/sql-reference/data-types/float), [UUID](/docs/sql-reference/data-types/uuid), [Decimal32](/docs/sql-reference/data-types/decimal), [Decimal64](/docs/sql-reference/data-types/decimal), [Decimal128](/docs/sql-reference/data-types/decimal), [Decimal256](/docs/sql-reference/data-types/decimal),[Date](/docs/sql-reference/data-types/date), [Date32](/docs/sql-reference/data-types/date32), [DateTime](/docs/sql-reference/data-types/datetime), [DateTime64](/docs/sql-reference/data-types/datetime64), [String](/docs/sql-reference/data-types/string), [Array](/docs/sql-reference/data-types/array).ClickHouse tries to cast value from dictionary to the specified data type. For example, for MySQL, the field might be `TEXT`, `VARCHAR`, or `BLOB` in the MySQL source table, but it can be uploaded as `String` in ClickHouse.[Nullable](/docs/sql-reference/data-types/nullable) is currently supported for [Flat](/docs/sql-reference/statements/create/dictionary/layouts/flat), [Hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed), [ComplexKeyHashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed#complex_key_hashed), [Direct](/docs/sql-reference/statements/create/dictionary/layouts/direct), [ComplexKeyDirect](/docs/sql-reference/statements/create/dictionary/layouts/direct#complex_key_direct), [RangeHashed](/docs/sql-reference/statements/create/dictionary/layouts/range-hashed), Polygon, [Cache](/docs/sql-reference/statements/create/dictionary/layouts/cache), [ComplexKeyCache](/docs/sql-reference/statements/create/dictionary/layouts/cache), [SSDCache](/docs/sql-reference/statements/create/dictionary/layouts/ssd-cache), [SSDComplexKeyCache](/docs/sql-reference/statements/create/dictionary/layouts/ssd-cache#complex_key_ssd_cache) dictionaries. In [IPTrie](/docs/sql-reference/statements/create/dictionary/layouts/ip-trie) dictionaries `Nullable` types are not supported. Yes| `null_value` Default value for a non\-existing element.In the example, it is an empty string. [NULL](/docs/sql-reference/syntax#null) value can be used only for the `Nullable` types (see the previous line with types description). Yes| `expression` [Expression](/docs/sql-reference/syntax#expressions) that ClickHouse executes on the value.The expression can be a column name in the remote SQL database. Thus, you can use it to create an alias for the remote column.Default value: no expression. No| `hierarchical` If `true`, the attribute contains the value of a parent key for the current key. See [Hierarchical Dictionaries](/docs/sql-reference/statements/create/dictionary/layouts/hierarchical).Default value: `false`. No| `injective` Flag that shows whether the `id -> attribute` image is [injective](https://en.wikipedia.org/wiki/Injective_function).If `true`, ClickHouse can automatically place after the `GROUP BY` clause the requests to dictionaries with injection. Usually it significantly reduces the amount of such requests.Default value: `false`. No| `is_object_id` Flag that shows whether the query is executed for a MongoDB document by `ObjectID`.Default value: `false`.  | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

[PreviousOverview](/docs/sql-reference/statements/create/dictionary)[NextOverview](/docs/sql-reference/statements/create/dictionary/sources)- [Key](#key)
	- [Numeric Key](#numeric-key)- [Composite Key](#composite-key)- [Attributes](#attributes)
Was this page helpful?

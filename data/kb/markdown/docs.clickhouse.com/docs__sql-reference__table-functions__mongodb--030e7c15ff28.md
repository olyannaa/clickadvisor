# mongodb \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- mongodb
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/mongodb.md)# mongodb

Allows `SELECT` queries to be performed on data that is stored on a remote MongoDB server.


## Syntax[​](#syntax "Direct link to Syntax")



```
mongodb(host:port, database, collection, user, password, structure[, options[, oid_columns]]);
mongodb(uri, collection, structure[, oid_columns]);
mongodb(named_collection_name[, <arg>=<value>...]);

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `host:port` MongoDB server address.| `database` Remote database name.| `collection` Remote collection name.| `user` MongoDB user.| `password` User password.| `structure` The schema for the ClickHouse table returned from this function.| `options` MongoDB connection string options (optional parameter).| `oid_columns` Comma\-separated list of columns that should be treated as `oid` in the WHERE clause. `_id` by default. | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


TipIf you are using the MongoDB Atlas cloud offering please add these options:
```
'connectTimeoutMS=10000&ssl=true&authSource=admin'

```



You can also connect by URI:



```
mongodb(uri, collection, structure[, oid_columns])

```



| Argument Description| `uri` Connection string.| `collection` Remote collection name.| `structure` The schema for the ClickHouse table returned from this function.| `oid_columns` Comma\-separated list of columns that should be treated as `oid` in the WHERE clause. `_id` by default.| :::  | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


You can pass the arguments using a named collection:



```
mongodb(_named_collection_[, host][, port][, database][, collection][, user][, password][, structure][, options][, oid_columns])
-- or
mongodb(_named_collection_[, uri][, structure][, oid_columns])

```

## Returned value[​](#returned_value "Direct link to Returned value")


A table object with the same columns as the original MongoDB table.


## Examples[​](#examples "Direct link to Examples")


Suppose we have a collection named `my_collection` defined in a MongoDB database named `test`, and we insert a couple of documents:



```
db.createUser({user:"test_user",pwd:"password",roles:[{role:"readWrite",db:"test"}]})

db.createCollection("my_collection")

db.my_collection.insertOne(
    { log_type: "event", host: "120.5.33.9", command: "check-cpu-usage -w 75 -c 90" }
)

db.my_collection.insertOne(
    { log_type: "event", host: "120.5.33.4", command: "system-check"}
)

```

Let's query the collection using the `mongodb` table function:



```
SELECT * FROM mongodb(
    '127.0.0.1:27017',
    'test',
    'my_collection',
    'test_user',
    'password',
    'log_type String, host String, command String',
    'connectTimeoutMS=10000'
)

```

or:



```
SELECT * FROM mongodb(
    'mongodb://test_user:[[email protected]](/cdn-cgi/l/email-protection):27017/test?connectionTimeoutMS=10000',
    'my_collection',
    'log_type String, host String, command String'
)

```

or:



```
CREATE NAMED COLLECTION mongo_creds AS
       uri='mongodb://test_user:[[email protected]](/cdn-cgi/l/email-protection):27017/test?connectionTimeoutMS=10000',
       collection='default_collection';

SELECT * FROM mongodb(
        mongo_creds,
        collection = 'my_collection',
        structure = 'log_type String, host String, command String'
)

```

## Related[​](#related "Direct link to Related")


- [The `MongoDB` table engine](/docs/engines/table-engines/integrations/mongodb)
- [Using MongoDB as a dictionary source](/docs/sql-reference/statements/create/dictionary/sources/mongodb)
[Previousmerge](/docs/sql-reference/table-functions/merge)[Nextmysql](/docs/sql-reference/table-functions/mysql)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Examples](#examples)- [Related](#related)
Was this page helpful?

# MongoDB dictionary source \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- SOURCE- MongoDB
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/sources/mongodb.md)# MongoDB dictionary source

Example of settings:


- DDL- Configuration file


```
SOURCE(MONGODB(
    host 'localhost'
    port 27017
    user ''
    password ''
    db 'test'
    collection 'dictionary_source'
    options 'ssl=true'
))

```
Or using a URI:
```
SOURCE(MONGODB(
    uri 'mongodb://localhost:27017/clickhouse'
    collection 'dictionary_source'
))

```



```
<source>
    <mongodb>
        <host>localhost</host>
        <port>27017</port>
        <user></user>
        <password></password>
        <db>test</db>
        <collection>dictionary_source</collection>
        <options>ssl=true</options>
    </mongodb>
</source>

```
Or using a URI:
```
<source>
    <mongodb>
        <uri>mongodb://localhost:27017/test?ssl=true</uri>
        <collection>dictionary_source</collection>
    </mongodb>
</source>

```



  

Setting fields:




| Setting Description| `host` The MongoDB host.| `port` The port on the MongoDB server.| `user` Name of the MongoDB user.| `password` Password of the MongoDB user.| `db` Name of the database.| `collection` Name of the collection.| `options` MongoDB connection string options. Optional.| `uri` URI for establishing the connection (alternative to individual host/port/db fields). | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


[More information about the engine](/docs/engines/table-engines/integrations/mongodb)

[PreviousClickHouse](/docs/sql-reference/statements/create/dictionary/sources/clickhouse)[NextRedis](/docs/sql-reference/statements/create/dictionary/sources/redis)Was this page helpful?

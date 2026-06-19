---
source: blog
url: https://clickhouse.com/blog/getting-data-into-clickhouse-part-1
topic: getting-data-into-clickhouse-part-2-a-json-detour
ch_version_introduced: '3.456'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 8
---

``` ``` SELECT * FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONAsObject', 'post JSON') LIMIT 1 FORMAT JSONEachRow; {"post":{"by":"brakmic","dead":1,"deleted":0,"descendants":0,"id":11132929,"kids":[11133170],"parent":0,"poll":0,"score":3,"text":"","time":"2016-02-19 11:40:55","title":"SF ‘tech bro’ writes to mayor: ‘I shouldn’t have to see the despair of homeless’","type":"story", "url":"https:\/\/www.washingtonpost.com\/news\/morning-mix\/wp\/2016\/02\/18\/s-f-tech-bro-writes-open-letter-to-mayor-i-shouldnt-have-to-see-the-pain-struggle-and-despair-of-homeless-people\/"}} 1 row in set. Elapsed: 3.456 sec. ```

This requires us to specify a target field for the JSON: post in this case. Note how we can also request our output to be returned in JSON by reusing the format JSONEachRow. The key observation is that the post column is assigned the new type `Object('json')`.

## JSON As Objects [\#](/blog/getting-data-into-clickhouse-part-2-json#json-as-objects)

Above, we introduced the `Object(‘json’)` type to represent a JSON row. Assuming we map our Hacker News rows to this type, our schema definition becomes trivial. This is the true power of this type. Our data is now treated as semi\-structured, and any sub\-columns will automatically be created and their types inferred from the data!

```

DROP TABLE IF EXISTS hackernews;
 
SET allow_experimental_object_type = 1;
 
CREATE TABLE hackernews
(
   `post` JSON
)
ENGINE = MergeTree
ORDER BY tuple();



```

A few important observations here. We use the JSON type as an abbreviation for `Object('JSON')` \- in the future, we may add additional Object representations beyond JSON. Secondly, we are required to set `allow_experimental_object_type = 1` to use this type since it is experimental. Finally, note that we can’t utilize any sub\-columns of post as primary keys and thus have defined our `ORDER BY as tuple()`, i.e., no primary key. We address this limitation later.

With this table created, insertion becomes trivial.

```

INSERT INTO hackernews SELECT post
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.json.gz', 'JSONAsObject', 'post JSON')
 
0 rows in set. Elapsed: 214.846 sec. Processed 28.74 million rows, 13.42 GB (133.76 thousand rows/s., 62.46 MB/s.)



```

Selecting a single row gives us an insight into how JSON is represented in ClickHouse.

```

SELECT *
FROM hackernews
LIMIT 1
FORMAT Vertical
 
Row 1:
──────
post: ('brakmic',1,0,0,11132929,[11133170],0,[],0,3,'','2016-02-19 11:40:55','SF ‘tech bro’ writes to mayor: ‘I shouldn’t have to see the despair of homeless’','story','https://www.washingtonpost.com/news/morning-mix/wp/2016/02/18/s-f-tech-bro-writes-open-letter-to-mayor-i-shouldnt-have-to-see-the-pain-struggle-and-despair-of-homeless-people/')


```

Using the `DESCRIBE` command and setting `describe_extend_object_types=1` confirms the use of Tuples as an internal representation:

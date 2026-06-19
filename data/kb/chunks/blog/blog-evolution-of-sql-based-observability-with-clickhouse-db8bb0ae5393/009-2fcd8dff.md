---
source: blog
url: https://clickhouse.com/blog/the-state-of-sql-based-observability
topic: the-evolution-of-sql-based-observability
ch_version_introduced: '40.77'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 18
---

toDate(TimestampTime) 21PRIMARY KEY (ServiceName, TimestampTime) 22ORDER BY (ServiceName, TimestampTime, Timestamp) ``` ``` All of this means users will be able to send arbitrary data in these above OTel columns, knowing they will be efficiently stored and easily queried.

> Note we still recommend adhering to the broader OTel schema, where columns exist on the root vs just using a single JSON column! These more explicit columns benefit from wider ClickHouse features, such as supporting codecs and secondary indices. It thus may still make sense to extract commonly queried columns to the root.

### Example [\#](/blog/evolution-of-sql-based-observability-with-clickhouse#example)

Consider a structured logs dataset.

```

```
1{"remote_addr":"40.77.167.129","remote_user":"-","run_time":0,"time_local":"2019-01-22 00:26:17.000","request_type":"GET","request_path":"\/image\/14925\/productModel\/100x100","request_protocol":"HTTP\/1.1","status":"500","size":1696.22,"referer":"-","user_agent":"Mozilla\/5.0 (compatible; bingbot\/2.0; +http:\/\/www.bing.com\/bingbot.htm)","response_time":23.2}
2{"remote_addr":"91.99.72.15","remote_user":"-","run_time":"0","time_local":"2019-01-22 00:26:17.000","request_type":"GET","request_path":"\/product\/31893\/62100\/----PR257AT","request_protocol":"HTTP\/1.1","status":200,"size":"41483","referer":"-","user_agent":"Mozilla\/5.0 (Windows NT 6.2; Win64; x64; rv:16.0)Gecko\/16.0 Firefox\/16.0","response_time":""}
```


```

While largely well structured, there are differences in types used for columns here \- `status`, `response_time​​`, `size`, and `run_time` are both numeric and String. Ingesting this sample from file, using [a OTel collector configuration](https://www.otelbin.io/#config=receivers%3A*N_filelog%3A*N___include%3A*N_____-_%2Fopt%2Fdata%2Flogs%2Faccess-structured.log*N___start*_at%3A_beginning*N___operators%3A*N_____-_type%3A_json*_parser*N_______timestamp%3A*N_________parse*_from%3A_attributes.time*_local*N_________layout%3A_*%22*.Y-*.m-*.d_*.H%3A*.M%3A*.S*%22*N*N*Nprocessors%3A*N__batch%3A*N____timeout%3A_5s*N____send*_batch*_size%3A_1*N*N*Nexporters%3A*N_logging%3A*N___loglevel%3A_debug*N*N*Nservice%3A*N_pipelines%3A*N___logs%3A*N_____receivers%3A_%5Bfilelog%5D*N_____processors%3A_%5Bbatch%5D*N_____exporters%3A_%5Blogging%5D%7E), would result in the following:

```

```
1SELECT
2	Timestamp,
3	LogAttributes
4FROM otel_logs
5FORMAT Vertical
6
7Row 1:
8──────
9Timestamp: 	2019-01-22 00:26:17.000000000
10LogAttributes: {'response_time':'23.2','remote_addr':'40.77.167.129','remote_user':'-','request_path':'/image/14925/productModel/100x100','size':'1696.22','request_type':'GET','run_time':'0','referer':'-','user_agent':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)','time_local':'2019-01-22 00:26:17.000','request_protocol':'HTTP/1.1','status':'500','log.file.name':'simple.log'}
11
12Row 2:
13──────
14Timestamp: 	2019-01-22 00:26:17.000000000
15LogAttributes: {'request_protocol':'HTTP/1.1','status':'200','user_agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0)Gecko/16.0 Firefox/16.0','size':'41483','run_time':'0','remote_addr':'91.99.72.15','request_type':'GET','referer':'-','log.file.name':'simple.log','remote_user':'-','time_local':'2019-01-22 00:26:17.000','response_time':'','request_path':'/product/31893/62100/----PR257AT'}
16
172 rows in set. Elapsed: 0.003 sec.
```


```

The OTel collector has placed our columns inside our `LogAttributes`, resulting in all column values being mapped to a String. Even simple queries, as a result, become syntactically complex e.g.

```

```
1SELECT LogAttributes['status'] AS status,
2	max(if((LogAttributes['response_time']) != '', 
3	  LogAttributes['response_time']::Float32, 0)) AS max
4FROM otel_logs
5GROUP BY status
6
7┌─status─┬──max─┐
8│ 500	│ 23.2 │
9│ 200	│	0 │
10└────────┴──────┘
11
122 rows in set. Elapsed: 0.016 sec.
```


```

If this same [data is inserted with the OTel schema](https://pastila.nl/?01f88fd7/553c960d083e0afc2080bf337a3ca1d0#Qg05Ld/o86RiWUI8y2j/+w==) using the JSON type for our `LogAttributes` column, we can see the types are preserved.

```

```
1SELECT
2	Timestamp,
3	LogAttributes
4FROM otel_logs
5FORMAT Vertical
6SETTINGS output_format_json_quote_64bit_integers = 0
7
8Row 1:
9──────
10Timestamp: 	2019-01-22 00:26:17.000000000
11LogAttributes: {"referer":"-","remote_addr":"91.99.72.15","remote_user":"-","request_path":"\/product\/31893\/62100\/----PR257AT","request_protocol":"HTTP\/1.1","request_type":"GET","response_time":"","run_time":"0","size":"41483","status":200,"time_local":"2019-01-22 00:26:17.000000000","user_agent":"Mozilla\/5.0 (Windows NT 6.2; Win64; x64; rv:16.0)Gecko\/16.0 Firefox\/16.0"}
12
13Row 2:
14──────
15Timestamp: 	2019-01-22 00:26:17.000000000
16LogAttributes: {"referer":"-","remote_addr":"40.77.167.129","remote_user":"-","request_path":"\/image\/14925\/productModel\/100x100","request_protocol":"HTTP\/1.1","request_type":"GET","response_time":23.2,"run_time":0,"size":1696.22,"status":"500","time_local":"2019-01-22 00:26:17.000000000","user_agent":"Mozilla\/5.0 (compatible; bingbot\/2.0; +http:\/\/www.bing.com\/bingbot.htm)"}
17
182 rows in set. Elapsed: 0.012 sec.
```


```

> By default, 64\-bit integers are quoted in output (for Javascript). We disable this for example purposes here with the setting `output_format_json_quote_64bit_integers=0`.

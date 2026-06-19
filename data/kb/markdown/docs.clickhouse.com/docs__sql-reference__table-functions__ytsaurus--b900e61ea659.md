# ytsaurus \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- ytsaurus
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/ytsaurus.md)# ytsaurus Table Function


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)
The table function allows to read data from the YTsaurus cluster.


## Syntax[​](#syntax "Direct link to Syntax")



```
ytsaurus(http_proxy_url, cypress_path, oauth_token, format)

```

ReferencesThis is an experimental feature that may change in backwards\-incompatible ways in the future releases.
Enable usage of the YTsaurus table function
with [allow\_experimental\_ytsaurus\_table\_function](/docs/operations/settings/settings#allow_experimental_ytsaurus_table_engine) setting.
Input the command `set allow_experimental_ytsaurus_table_function = 1`.


## Arguments[​](#arguments "Direct link to Arguments")


- `http_proxy_url` — URL to the YTsaurus http proxy.
- `cypress_path` — Cypress path to the data source.
- `oauth_token` — OAuth token.
- `format` — The [format](/docs/interfaces/formats) of the data source.


**Returned value**


A table with the specified structure for reading data in the specified ytsaurus cypress path in YTsaurus cluster.


**See Also**


- [ytsaurus engine](/docs/engines/table-engines/integrations/ytsaurus)
[Previoushudi](/docs/sql-reference/table-functions/hudi)[NexthudiCluster](/docs/sql-reference/table-functions/hudiCluster)- [Syntax](#syntax)- [Arguments](#arguments)
Was this page helpful?

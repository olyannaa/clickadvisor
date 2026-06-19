# YTsaurus dictionary source \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- SOURCE- YTsaurus
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/sources/ytsaurus.md)# YTsaurus dictionary source

Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)
Not supported in ClickHouse Cloud
ReferencesThis is an experimental feature that may change in backwards\-incompatible ways in future releases.
Enable usage of the YTsaurus dictionary source
using setting [`allow_experimental_ytsaurus_dictionary_source`](/docs/operations/settings/settings#allow_experimental_ytsaurus_dictionary_source).


Example of settings:


- DDL- Configuration file


```
SOURCE(YTSAURUS(
    http_proxy_urls 'http://localhost:8000'
    cypress_path '//tmp/test'
    oauth_token 'password'
))

```

```
<source>
    <ytsaurus>
        <http_proxy_urls>http://localhost:8000</http_proxy_urls>
        <cypress_path>//tmp/test</cypress_path>
        <oauth_token>password</oauth_token>
        <check_table_schema>1</check_table_schema>
    </ytsaurus>
</source>

```

  

Setting fields:




| Setting Description| `http_proxy_urls` URL to the YTsaurus http proxy.| `cypress_path` Cypress path to the table source.| `oauth_token` OAuth token. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |

[PreviousPostgreSQL](/docs/sql-reference/statements/create/dictionary/sources/postgresql)[NextNull](/docs/sql-reference/statements/create/dictionary/sources/null)Was this page helpful?

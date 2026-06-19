# HTTP(S) dictionary source \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- SOURCE- HTTP(S)
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/sources/http.md)# HTTP(S) dictionary source

Working with an HTTP(S) server depends on [how the dictionary is stored in memory](/docs/sql-reference/statements/create/dictionary/layouts). If the dictionary is stored using `cache` and `complex_key_cache`, ClickHouse requests the necessary keys by sending a request via the `POST` method.


Example of settings:


- DDL- Configuration file


```
SOURCE(HTTP(
    url 'http://[::1]/os.tsv'
    format 'TabSeparated'
    credentials(user 'user' password 'password')
    headers(header(name 'API-KEY' value 'key'))
))

```

```
<source>
    <http>
        <url>http://[::1]/os.tsv</url>
        <format>TabSeparated</format>
        <credentials>
            <user>user</user>
            <password>password</password>
        </credentials>
        <headers>
            <header>
                <name>API-KEY</name>
                <value>key</value>
            </header>
        </headers>
    </http>
</source>

```

  

In order for ClickHouse to access an HTTPS resource, you must [configure openSSL](/docs/operations/server-configuration-parameters/settings#openssl) in the server configuration.


Setting fields:




| Setting Description| `url` The source URL.| `format` The file format. All the formats described in [Formats](/docs/sql-reference/formats) are supported.| `credentials` Basic HTTP authentication. Optional.| `user` Username required for the authentication.| `password` Password required for the authentication.| `headers` All custom HTTP headers entries used for the HTTP request. Optional.| `header` Single HTTP header entry.| `name` Identifier name used for the header send on the request.| `value` Value set for a specific identifier name. | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


When creating a dictionary using the DDL command (`CREATE DICTIONARY ...`) remote hosts for HTTP dictionaries are checked against the contents of `remote_url_allow_hosts` section from config to prevent database users to access arbitrary HTTP server.

[PreviousExecutable Pool](/docs/sql-reference/statements/create/dictionary/sources/executable-pool)[NextODBC](/docs/sql-reference/statements/create/dictionary/sources/odbc)Was this page helpful?

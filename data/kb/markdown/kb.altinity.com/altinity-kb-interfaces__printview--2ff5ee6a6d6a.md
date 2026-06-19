# Interfaces \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-interfaces/).

# Interfaces

Frequent questions users have about `clickhouse-client`- 1: [clickhouse\-client](#pg-4afca0f707dc9950b20fa62ea6da93dc)

# 1 \- clickhouse\-client

ClickHouse® clientQ. How can I input multi\-line SQL code? can you guys give me an example?

A. Just run clickhouse\-client with `-m` switch, and it starts executing only after you finish the line with a semicolon.

Q. How can i use pager with clickhouse\-client

A. Here is an example: `clickhouse-client --pager 'less -RS'`

Q. Data is returned in chunks / several tables.

A. Data get streamed from the server in blocks, every block is formatted individually when the default `PrettyCompact` format is used. You can use `PrettyCompactMonoBlock` format instead, using one of the options:

- start clickhouse\-client with an extra flag: `clickhouse-client --format=PrettyCompactMonoBlock`
- add `FORMAT PrettyCompactMonoBlock` at the end of your query.
- change clickhouse\-client default format in the config. See [https://github.com/ClickHouse/ClickHouse/blob/976dbe8077f9076387528e2f40b6174f6d8a8b90/programs/client/clickhouse\-client.xml\#L42](https://github.com/ClickHouse/ClickHouse/blob/976dbe8077f9076387528e2f40b6174f6d8a8b90/programs/client/clickhouse-client.xml#L42)

Q. Сustomize client config

A. you can change it globally (for all users of the workstation)


```
nano /etc/clickhouse-client/conf.d/user.xml

<config>
    <user>default1</user>
    <password>default1</password>
    <host></host>
    <multiline>true</multiline>
    <multiquery>true</multiquery>
</config>
See also https://github.com/ClickHouse/ClickHouse/blob/976dbe8077f9076387528e2f40b6174f6d8a8b90/programs/client/clickhouse-client.xml#L42

```
or for particular users \- by adjusting one of.


```
./clickhouse-client.xml
~/.clickhouse-client/config.xml

```
Also, it’s possible to have several client config files and pass one of them to clickhouse\-client command explicitly

References:

- <https://clickhouse.com/docs/en/interfaces/cli>

# Local File dictionary source \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- SOURCE- Local File
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/sources/local-file.md)# Local File dictionary source

The local file source loads dictionary data from a file on the local filesystem. This is useful for small, static lookup tables that can be stored as flat files in formats such as TSV, CSV, or any other [supported format](/docs/sql-reference/formats).


Example of settings:


- DDL- Configuration file


```
SOURCE(FILE(path './user_files/os.tsv' format 'TabSeparated'))

```

```
<source>
  <file>
    <path>/opt/dictionaries/os.tsv</path>
    <format>TabSeparated</format>
  </file>
</source>

```

  

Setting fields:




| Setting Description| `path` The absolute path to the file.| `format` The file format. All the formats described in [Formats](/docs/sql-reference/formats) are supported. | | | | | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- |


When a dictionary with source `FILE` is created via DDL command (`CREATE DICTIONARY ...`), the source file needs to be located in the `user_files` directory to prevent DB users from accessing arbitrary files on the ClickHouse node.


**See Also**


- [Dictionary function](/docs/sql-reference/table-functions/dictionary)
[PreviousOverview](/docs/sql-reference/statements/create/dictionary/sources)[NextExecutable File](/docs/sql-reference/statements/create/dictionary/sources/executable-file)Was this page helpful?

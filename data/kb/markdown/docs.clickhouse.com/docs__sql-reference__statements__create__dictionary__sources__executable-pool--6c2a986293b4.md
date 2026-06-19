# Executable Pool dictionary source \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- SOURCE- Executable Pool
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/sources/executable-pool.md)# Executable Pool dictionary source

Executable pool allows loading data from a pool of processes.
This source does not work with dictionary layouts that need to load all data from source.


Executable pool works if the dictionary [is stored](/docs/sql-reference/statements/create/dictionary/layouts#storing-dictionaries-in-memory) using one of the following layouts:


- `cache`
- `complex_key_cache`
- `ssd_cache`
- `complex_key_ssd_cache`
- `direct`
- `complex_key_direct`


Executable pool will spawn a pool of processes with the specified command and keep them running until they exit. The program should read data from STDIN while it is available and output the result to STDOUT. It can wait for the next block of data on STDIN. ClickHouse will not close STDIN after processing a block of data, but will pipe another chunk of data when needed. The executable script should be ready for this way of data processing — it should poll STDIN and flush data to STDOUT early.


Example of settings:


- DDL- Configuration file


```
SOURCE(EXECUTABLE_POOL(
    command 'while read key; do printf "$key\tData for key $key\n"; done'
    format 'TabSeparated'
    pool_size 10
    max_command_execution_time 10
    implicit_key false
))

```

```
<source>
    <executable_pool>
        <command><command>while read key; do printf "$key\tData for key $key\n"; done</command</command>
        <format>TabSeparated</format>
        <pool_size>10</pool_size>
        <max_command_execution_time>10<max_command_execution_time>
        <implicit_key>false</implicit_key>
    </executable_pool>
</source>

```

Setting fields:




| Setting Description| `command` The absolute path to the executable file, or the file name (if the program directory is written to `PATH`).| `format` The file format. All the formats described in [Formats](/docs/sql-reference/formats) are supported.| `pool_size` Size of pool. If 0 is specified as `pool_size` then there is no pool size restrictions. Default value is `16`.| `command_termination_timeout` Executable script should contain main read\-write loop. After dictionary is destroyed, pipe is closed, and executable file will have `command_termination_timeout` seconds to shutdown before ClickHouse will send SIGTERM signal to child process. Specified in seconds. Default value is `10`. Optional.| `max_command_execution_time` Maximum executable script command execution time for processing block of data. Specified in seconds. Default value is `10`. Optional.| `command_read_timeout` Timeout for reading data from command stdout in milliseconds. Default value `10000`. Optional.| `command_write_timeout` Timeout for writing data to command stdin in milliseconds. Default value `10000`. Optional.| `implicit_key` The executable source file can return only values, and the correspondence to the requested keys is determined implicitly by the order of rows in the result. Default value is `false`. Optional.| `execute_direct` If `execute_direct` \= `1`, then `command` will be searched inside user\_scripts folder specified by [user\_scripts\_path](/docs/operations/server-configuration-parameters/settings#user_scripts_path). Additional script arguments can be specified using whitespace separator. Example: `script_name arg1 arg2`. If `execute_direct` \= `0`, `command` is passed as argument for `bin/sh -c`. Default value is `1`. Optional.| `send_chunk_header` Controls whether to send row count before sending a chunk of data to process. Default value is `false`. Optional. | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


That dictionary source can be configured only via XML configuration. Creating dictionaries with executable source via DDL is disabled, otherwise, the DB user would be able to execute arbitrary binary on ClickHouse node.

[PreviousExecutable File](/docs/sql-reference/statements/create/dictionary/sources/executable-file)[NextHTTP(S)](/docs/sql-reference/statements/create/dictionary/sources/http)Was this page helpful?

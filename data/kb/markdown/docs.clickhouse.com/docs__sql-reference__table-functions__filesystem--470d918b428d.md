# filesystem \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- filesystem
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/filesystem.md)# filesystem Table Function


Not supported in ClickHouse Cloud
Recursively iterates a directory and returns a table with file metadata (paths, sizes, types, permissions, modification times) and, optionally, file contents.


In `clickhouse-server` mode, the path must be within the [user\_files\_path](/docs/operations/server-configuration-parameters/settings#user_files_path) directory. Symlinks inside `user_files_path` that point outside of it are followed, but only entries whose path (through the symlink) starts with `user_files_path` are returned.


In `clickhouse-local` mode, there are no path restrictions.


## Syntax[​](#syntax "Direct link to Syntax")



```
filesystem([path])

```

## Arguments[​](#arguments "Direct link to Arguments")




| Parameter Description| `path` The directory to list. Can be an absolute path (must be inside `user_files_path` in server mode) or a path relative to `user_files_path`. If empty or omitted, defaults to `user_files_path`. | | | --- | --- | | |
| --- | --- | --- | --- |


## Returned columns[​](#returned_columns "Direct link to Returned columns")




| Column Type Description| `path` `String` Directory containing the entry (does not include the file/directory name itself).| `name` `String` File or directory name (the last component of the path).| `file` `String` (ALIAS of `name`) Alias for the `name` column.| `type` `Enum8` File type: `'none'`, `'not_found'`, `'regular'`, `'directory'`, `'symlink'`, `'block'`, `'character'`, `'fifo'`, `'socket'`, `'unknown'`.| `size` `Nullable(UInt64)` File size in bytes (for regular files). `NULL` for non\-regular files (directories, symlinks, etc.) and on error.| `depth` `UInt16` Recursion depth. `0` for the queried directory itself and its immediate children, `1` for entries one level deeper, and so on.| `modification_time` `Nullable(DateTime64(6))` Last modification time with microsecond precision. `NULL` on error.| `is_symlink` `Bool` Whether the entry is a symbolic link.| `content` `Nullable(String)` File contents (for regular files). `NULL` for non\-regular files (directories, symlinks, etc.). Read errors raise an exception. Reading this column triggers actual file I/O, so omit it if not needed.| `owner_read` `Bool` Owner has read permission.| `owner_write` `Bool` Owner has write permission.| `owner_exec` `Bool` Owner has execute permission.| `group_read` `Bool` Group has read permission.| `group_write` `Bool` Group has write permission.| `group_exec` `Bool` Group has execute permission.| `others_read` `Bool` Others have read permission.| `others_write` `Bool` Others have write permission.| `others_exec` `Bool` Others have execute permission.| `set_gid` `Bool` Set\-GID bit.| `set_uid` `Bool` Set\-UID bit.| `sticky_bit` `Bool` Sticky bit. | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Only columns actually used in the query are computed, so selecting a subset of columns (especially omitting `content`) is efficient.


## Examples[​](#examples "Direct link to Examples")


### List files in user\_files[​](#list-files "Direct link to List files in user_files")



```
SELECT name, type, size, depth
FROM filesystem()
ORDER BY name;

```

### Find large files[​](#find-large-files "Direct link to Find large files")



```
SELECT path, name, size
FROM filesystem()
WHERE type = 'regular' AND size > 1000000
ORDER BY size DESC;

```

### Read file contents[​](#read-contents "Direct link to Read file contents")



```
SELECT name, content
FROM filesystem('my_directory')
WHERE name LIKE '%.csv';

```

### List only immediate children[​](#list-immediate "Direct link to List only immediate children")



```
SELECT name, type
FROM filesystem('my_directory')
WHERE depth = 0;

```
[PreviousfileCluster](/docs/sql-reference/table-functions/fileCluster)[Nextformat](/docs/sql-reference/table-functions/format)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned columns](#returned_columns)- [Examples](#examples)
	- [List files in user\_files](#list-files)- [Find large files](#find-large-files)- [Read file contents](#read-contents)- [List only immediate children](#list-immediate)
Was this page helpful?

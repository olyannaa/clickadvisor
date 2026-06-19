---
source: blog
url: https://clickhouse.cloud/signUp?loc=blog
topic: user-defined-functions-in-clickhouse-cloud
ch_version_introduced: '0.011'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 5
---

to show the general structure: ``` CREATE FUNCTION file_path_history AS n -> if(empty(n), [], arrayConcat([n], file_path_history_01(( SELECT if(empty(old_path), NULL, old_path) FROM git.file_changes WHERE (path = n) AND ((change_type = 'Rename') OR (change_type = 'Add')) LIMIT 1 )))) ```

Our function `file_path_history` accepts the file's name of interest as a parameter `n` \- likely the current known path on the first call. This path is then concatenated to the current result using the arrayConcat function, in addition to the result of a UDF call to the next level via `file_path_history_01` (we haven’t defined this yet). To this function, we pass the previous filename via the query:

```

SELECT if(empty(old_path), Null, old_path) FROM git.file_changes WHERE path = n AND (change_type = 'Rename' OR change_type = 'Add') LIMIT 1
))))


```

The following function, `file_path_history_01`, is very similar, except it will receive the old path of the original file specified by the user. It, in turn, finds the previous path for this file, invoking `file_path_history_02`. This artificial recursion continues until either we reach the maximum depth (i.e., the file has been renamed more than five times) or no result is returned from a SELECT (effectively a Null).

![recursive_udf.png](/uploads/recursive_udf_e4ea7d0146.png)
Our complete function definitions look like this. Note our final function is different and provides a base case:

```

CREATE FUNCTION file_path_history AS (n) -> if(empty(n),  [], arrayConcat([n], file_path_history_01((SELECT if(empty(old_path), Null, old_path) FROM git.file_changes WHERE path = n AND (change_type = 'Rename' OR change_type = 'Add') LIMIT 1))));

CREATE FUNCTION file_path_history_01 AS (n) -> if(isNull(n), [], arrayConcat([n], file_path_history_02((SELECT if(empty(old_path), Null, old_path) FROM git.file_changes WHERE path = n AND (change_type = 'Rename' OR change_type = 'Add') LIMIT 1))));

CREATE FUNCTION file_path_history_02 AS (n) -> if(isNull(n), [], arrayConcat([n], file_path_history_03((SELECT if(empty(old_path), Null, old_path) FROM git.file_changes WHERE path = n AND (change_type = 'Rename' OR change_type = 'Add') LIMIT 1))));

CREATE FUNCTION file_path_history_03 AS (n) -> if(isNull(n), [], arrayConcat([n], file_path_history_04((SELECT if(empty(old_path), Null, old_path) FROM git.file_changes WHERE path = n AND (change_type = 'Rename' OR change_type = 'Add') LIMIT 1))));

CREATE FUNCTION file_path_history_04 AS (n) -> if(isNull(n), [], arrayConcat([n], file_path_history_05((SELECT if(empty(old_path), Null, old_path) FROM git.file_changes WHERE path = n AND (change_type = 'Rename' OR change_type = 'Add') LIMIT 1))));

CREATE FUNCTION file_path_history_05 AS (n) -> if(isNull(n), [], [n]);


```

## Using our function [\#](/blog/user-defined-functions-clickhouse-udfs#using-our-function)

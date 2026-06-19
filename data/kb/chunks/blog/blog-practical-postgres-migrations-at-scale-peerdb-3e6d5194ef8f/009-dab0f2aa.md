---
source: blog
url: https://clickhouse.com/cloud/postgres
topic: making-large-postgres-migrations-practical-1tb-in-2-hours-with-peerdb
ch_version_introduced: '27.175'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 10
---

AS _peerdb_rank FROM peerdb_temp._peerdb_raw_my_mirror -- contains all change-data of the mirror WHERE _peerdb_batch_id = $ 1 AND _peerdb_destination_table_name = $ 2 ) ``` 2. Now, we issue a `MERGE` command to push each change\-data to the final table.

```
MERGE INTO "public"."my_table" dst USING (
    SELECT
        (_peerdb_data ->> 'id') AS "id",
        (_peerdb_data ->> 'blob') AS "blob",
        (_peerdb_data ->> 'status') AS "status",
        _peerdb_record_type,
        _peerdb_unchanged_toast_columns
    FROM
        src_rank
    WHERE
        _peerdb_rank = 1
) src ON src."id" = dst."id"

```

3. First, we must account for inserts, which is straightforward.

```
   WHEN NOT MATCHED THEN -- row is not on target, so it is an INSERT
        INSERT
            ("id", "blob", "status", "_peerdb_synced_at")
        VALUES
            (
                src."id",
                src."blob",
                src."status",
                CURRENT_TIMESTAMP
            )

```

4. Now, we get into the conflict handling strategy in the case of updates. In an update record, `_peerdb_unchanged_toast_columns` is a comma\-separated string list of column names whose values are unchanged. If there are no such values, it will be an empty string like so.

```
   WHEN MATCHED -- row exists on target
    AND src._peerdb_record_type != 2  -- this means it isn't a delete, so it's an update
    AND _peerdb_unchanged_toast_columns = '' -- no unchanged toast columns, update everything
    THEN
        UPDATE
        SET
            "id" = src."id",
            "blob" = src."blob",
            "status" = src."status",
            "_peerdb_synced_at" = CURRENT_TIMESTAMP

```

5. In the case above though, for instance, `blob` was unchanged in the update. That would then be handled like:

```
   WHEN MATCHED -- row exists on target
    AND src._peerdb_record_type != 2 -- this means it isn't a delete, so it's an update
    AND _peerdb_unchanged_toast_columns = 'blob' -- unchanged toast column ! we cannot update this guy, because it would wipe out its value to empty string sent by PG
 THEN 
        UPDATE
        SET -- blob not updated here
            "id" = src."id",
            "status" = src."status",
            "_peerdb_synced_at" = CURRENT_TIMESTAMP
            WHEN MATCHED
            AND src._peerdb_record_type = 2 THEN DELETE

```

## A look ahead and getting started [\#](/blog/practical-postgres-migrations-at-scale-peerdb#a-look-ahead-and-getting-started)

At ClickHouse, we’re actively working on making Postgres migrations a one\-click experience. This is a first step in that direction. Stay tuned for more updates in the near future!

[PeerDB](https://github.com/PeerDB-io/peerdb) can be set up with a single command. You can head over to our open\-source repository on GitHub to [get started](https://github.com/PeerDB-io/peerdb?tab=readme-ov-file#get-started). Once ready, create a Postgres to Postgres by ClickHouse mirror with a few clicks by following our [documented guides](https://docs.peerdb.io/mirror/cdc-pg-pg).

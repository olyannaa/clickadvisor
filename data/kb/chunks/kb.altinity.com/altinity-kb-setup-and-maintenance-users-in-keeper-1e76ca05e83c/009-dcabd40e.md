---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/9bcf6913cc4e44dcf11c3bbc8d194218c49a4bc1
topic: how-to-replicate-clickhouse-rbac-users-and-grants-with-zookeeper-keeper-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 9
---

children for create/delete detection; - per\-entity watch on `/uuid/<id>` for payload changes. - thread model: - dedicated watcher thread (`runWatchingThread`); - on errors: reset cached Keeper client, sleep, retry; - after refresh: send `AccessChangesNotifier` notifications. - cache layers:

	- primary cache: `MemoryAccessStorage` inside replicated access storage;
	- higher\-level caches in `AccessControl` (`RoleCache`, `RowPolicyCache`, `QuotaCache`, `SettingsProfilesCache`) are updated/invalidated via access change notifications.
- Read path is memory\-backed (`MemoryAccessStorage` mirror), not direct Keeper reads per query.
- Write path requires Keeper availability; if Keeper is down, RBAC writes fail while some reads can continue from loaded state.
- Insert target is selected by storage order and writeability in `MultipleAccessStorage`; this is why leftover `local_directory` can hijack SQL user creation.
- `ignore_on_cluster_for_replicated_access_entities_queries` is implemented as AST rewrite that removes `ON CLUSTER` for access queries when replicated access storage is enabled.

## 12\. Version and history highlights

| Date | Change | Why it matters |
| --- | --- | --- |
| 2021\-07\-21 | `ReplicatedAccessStorage` introduced (`e33a2bf7bc9`, PR \#27426\) | First Keeper\-backed RBAC replication |
| 2023\-08\-18 | Ignore `ON CLUSTER` for replicated access entities (`14590305ad0`, PR \#52975\) | Reduced duplicate/overlap behavior |
| 2023\-12\-12 | Extended ignore behavior to `GRANT/REVOKE` (`b33f1245559`, PR \#57538\) | Fixed common operational conflict with grants |
| 2025\-06\-03 | Keeper replication logic extracted to `ZooKeeperReplicator` (`39eb90b73ef`, PR \#81245\) | Cleaner architecture, shared replication core |
| 2026\-01\-24 | Optional strict mode on invalid replicated entities (`3d654b79853`) | Lets operators fail fast on corrupted Keeper payloads |

## 13\. Code references for deep dives

- `src/Access/AccessControl.cpp`
- `src/Access/MultipleAccessStorage.cpp`
- `src/Access/ReplicatedAccessStorage.cpp`
- `src/Access/ZooKeeperReplicator.cpp`
- `src/Interpreters/removeOnClusterClauseIfNeeded.cpp`
- `src/Access/IAccessStorage.cpp`
- `src/Backups/BackupCoordinationOnCluster.cpp`
- `src/Backups/RestoreCoordinationOnCluster.cpp`
- `tests/integration/test_replicated_users/test.py`
- `tests/integration/test_replicated_access/test_invalid_entity.py`

Last modified 2026\.03\.25: [Apply suggestions from code review (9bcf691\)](https://github.com/Altinity/altinityknowledgebase/commit/9bcf6913cc4e44dcf11c3bbc8d194218c49a4bc1)

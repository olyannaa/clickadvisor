# Upgrade \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/upgrade/).

# Upgrade

Upgrade notes.- 1: [Vulnerabilities](#pg-06ff440b95ba6f51135176bbbc9a61f4)
- 2: [ClickHouse® Function/Engines/Settings Report](#pg-1f8e1210601ea0fb1a2a4a7bd7a3b65b)
- 3: [Removing empty parts](#pg-51f5584a0c33dfad80ddd52f05b0ff7f)
- 4: [Removing lost parts](#pg-4f0b5e6619b8a3ab62f90a0ae7370c20)

# ClickHouse® Version Upgrade Procedure

## Step\-by\-Step Guide:

Normally the upgrade procedure looks like that:

1. **Pick the release to upgrade**
	- If you upgrade the existing installation with a lot of legacy queries, please pick mature versions with extended lifetime for upgrade (use [Altinity Stable Builds](https://docs.altinity.com/altinitystablebuilds/)
	or LTS releases from the upstream).
2. **Review Release Notes/Changelog**
	- Compare the release notes/changelog between your current release and the target release.
	- For Altinity Stable Builds: check the release notes of the release you do upgrade to (if you going from some older release \- you may need to read several of them for every release in between (for example to upgrade from 22\.3 to 23\.8 you will need to check [22\.8](https://docs.altinity.com/releasenotes/altinity-stable-release-notes/22.8/)
	,
	[23\.3](https://docs.altinity.com/releasenotes/altinity-stable-release-notes/23.3/)
	,
	[23\.8](https://docs.altinity.com/releasenotes/altinity-stable-release-notes/23.8/)
	etc.)
	- For upstream releases check the [changelog](https://github.com/ClickHouse/ClickHouse/blob/master/CHANGELOG.md)
	- Also ensure that no configuration changes are needed.
		- Sometimes, you may need to adjust configuration settings for better compatibility.
		- or to opt\-out some new features you don’t need (maybe needed to to make the downgrade path possible, or to make it possible for 2 versions to work together)
3. **Prepare Upgrade Checklist**
	- Upgrade the package (note that this does not trigger an automatic restart of the clickhouse\-server).
	- Restart the clickhouse\-server service.
	- Check health checks and logs.
	- Repeat the process on other nodes.
4. **Prepare “Canary” Update Checklist**
	- Mixing several versions in the same cluster can lead to different degradations. It is usually not recommended to have a significant delay between upgrading different nodes in the same cluster.
	- (If needed / depends on use case) stop ingestion into odd replicas / remove them for load\-balancer etc.
	- Perform the upgrade on the odd replicas first. Once they are back online, repeat same on the even replicas.
	- Test and verify that everything works properly. Check for any errors in the log files.
5. **Upgrade Dev/Staging Environment**
	- Follow 3rd and 4th checklist and perform Upgrade the Dev/Staging environment.
	- Ensure your schema/queries work properly in the Dev/staging environment.
	- Perform testing before plan for production upgrade.
	- Also worth to test the downgrade (to have plan B on upgrade failure)
6. **Upgrade Production**
	- Once the Dev/Staging environment is verified, proceed with the production upgrade.


> **Note:** Prepare and test downgrade procedures on staging so the server can be returned to the previous version if necessary.

In some upgrade scenarios (depending on which version you are upgrading from and to), when different replicas use different ClickHouse versions, you may encounter the following issues:

1. Replication doesn’t work at all, and delays grow.
2. Errors about ‘checksum mismatch’ occur, and traffic between replicas increases as they need to resync merge results.
Both problems will be resolved once all replicas are upgraded.

To know more you can Download our free upgrade guide here : [https://altinity.com/clickhouse\-upgrade\-overview/](https://altinity.com/clickhouse-upgrade-overview/)

# 1 \- Vulnerabilities

Vulnerabilities## 2022\-03\-15: 7 vulnerabilities in ClickHouse® were published.

See the details [https://jfrog.com/blog/7\-rce\-and\-dos\-vulnerabilities\-found\-in\-clickhouse\-dbms/](https://jfrog.com/blog/7-rce-and-dos-vulnerabilities-found-in-clickhouse-dbms/)

Those vulnerabilities were fixed by 2 PRs:

- <https://github.com/ClickHouse/ClickHouse/pull/27136>
- <https://github.com/ClickHouse/ClickHouse/pull/27743>

All releases starting from v21\.10\.2\.15 have that problem fixed.

Also, the fix was backported to 21\.3 and 21\.8 branches \- versions v21\.8\.11\.4\-lts and v21\.3\.19\.1\-lts
accordingly have the problem fixed (and all newer releases in those branches).

The latest Altinity stable releases also contain the bugfix.

- [21\.8\.13](https://docs.altinity.com/releasenotes/altinity-stable-release-notes/21.8/21813/)
- [21\.3\.20](https://docs.altinity.com/releasenotes/altinity-stable-release-notes/21.3/21320/)

If you use some older version we recommend upgrading.

Before the upgrade \- please ensure that ports 9000 and 8123 are not exposed to the internet, so external
clients who can try to exploit those vulnerabilities can not access your clickhouse node.

# 2 \- ClickHouse® Function/Engines/Settings Report

Report on ClickHouse® functions, table functions, table engines, system and MergeTree settings, with availability information.Follow this link for a complete report on ClickHouse® features with their availability: <https://github.com/anselmodadams/ChMisc/blob/main/report/report.md>
. It is frequently updated (at least once a month).

# 3 \- Removing empty parts

Removing empty partsRemoving of empty parts is a new feature introduced in ClickHouse® 20\.12\.
Earlier versions leave empty parts (with 0 rows) if TTL removes all rows from a part (<https://github.com/ClickHouse/ClickHouse/issues/5491>
).
If you set up TTL for your data it is likely that there are quite many empty parts in your system.

The new version notices empty parts and tries to remove all of them immediately.
This is a one\-time operation which runs right after an upgrade.
After that TTL will remove empty parts on its own.

There is a problem when different replicas of the same table start to remove empty parts at the same time. Because of the bug they can block each other (<https://github.com/ClickHouse/ClickHouse/issues/23292>
).

What we can do to avoid this problem during an upgrade:

1. Drop empty partitions before upgrading to decrease the number of empty parts in the system.


```
SELECT concat('alter table ',database, '.', table, ' drop partition id ''', partition_id, ''';')
FROM system.parts WHERE active
GROUP BY database, table, partition_id
HAVING count() = countIf(rows=0)

```
2. Upgrade/restart one replica (in a shard) at a time.
If only one replica is cleaning empty parts there will be no deadlock because of replicas waiting for one another.
Restart one replica, wait for replication queue to process, then restart the next one.

Removing of empty parts can be disabled by adding `remove_empty_parts=0` to the default profile.


```
$ cat /etc/clickhouse-server/users.d/remove_empty_parts.xml
<clickhouse>
    <profiles>
        <default>
            <remove_empty_parts>0</remove_empty_parts>
        </default>
    </profiles>
</clickhouse>

```
# 4 \- Removing lost parts

Removing lost parts## There might be parts left in ZooKeeper that don’t exist on disk

The explanation is here <https://github.com/ClickHouse/ClickHouse/pull/26716>

The problem is introduced in ClickHouse® 20\.1\.

The problem is fixed in 21\.8 and backported to 21\.3\.16, 21\.6\.9, 21\.7\.6\.

## Regarding the procedure to reproduce the issue:

The procedure was not confirmed, but I think it should work.

1. Wait for a merge on a particular partition (or run an OPTIMIZE to trigger one)
At this point you can collect the names of parts participating in the merge from the system.merges table, or the system.parts table.
2. When the merge finishes, stop one of the replicas before the inactive parts are dropped (or detach the table).
3. Bring the replica back up (or attach the table).
Check that there are no inactive parts in system.parts, but they stayed in ZooKeeper.
Also check that the inactive parts got removed from ZooKeeper for another replica.
Here is the query to check ZooKeeper:


```
select name, ctime from system.zookeeper
where path='<table_zpath>/replicas/<replica_name>/parts/'
  and name like '<put an expression for the parts that were merged>'

```
4. Drop the partition on the replica that DOES NOT have those extra parts in ZooKeeper.
Check the list of parts in ZooKeeper.
We hope that after this the parts on disk will be removed on all replicas, but one of the replicas will still have some parts left in ZooKeeper.
If this happens, then we think that after a restart of the replica with extra parts in ZooKeeper it will try to download them from another replica.

## A query to find ‘forgotten’ parts

[https://kb.altinity.com/altinity\-kb\-useful\-queries/parts\-consistency/\#compare\-the\-list\-of\-parts\-in\-zookeeper\-with\-the\-list\-of\-parts\-on\-disk](https://kb.altinity.com/altinity-kb-useful-queries/parts-consistency/#compare-the-list-of-parts-in-zookeeper-with-the-list-of-parts-on-disk)

## A query to drop empty partitions with failing replication tasks


```
select 'alter table '||database||'.'||table||' drop partition id '''||partition_id||''';' 
from (
select database, table, splitByChar('_',new_part_name)[1] partition_id
from system.replication_queue
where type='GET_PART' and not is_currently_executing and create_time < toStartOfDay(yesterday())
group by database, table, partition_id) q
left join 
(select database, table, partition_id, countIf(active) cnt_active, count() cnt_total
from system.parts group by  database, table, partition_id
) p using database, table, partition_id
where cnt_active=0

```

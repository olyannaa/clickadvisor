# S3 \& object storage \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/altinity-kb-s3-object-storage/).

# S3 \& object storage

S3 \& object storage- 1: [AWS S3 Recipes](#pg-828bae3b9b7642a9616204fb40e1e9ed)
- 2: [Clean up orphaned objects on s3](#pg-f237075cd12a3b0d6ced37b10cce00ac)
- 3: [How much data are written to S3 during mutations](#pg-db2b60c010ae5fb71a41ed626158cd0e)
- 4: [Example of the table at s3 with cache](#pg-801e0b0de3b47ed85a19172aec522cdc)
- 5: [S3Disk](#pg-56d30b1c77fb6e372359df908c32cf1a)

# 1 \- AWS S3 Recipes

AWS S3 Recipes## Using AWS IAM — Identity and Access Management roles

For EC2 instance, there is an option to configure an IAM role:

![](/assets/select-ec2-iam-role.png)

Role shall contain a policy with permissions like:


```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "allow-put-and-get",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::BUCKET_NAME/test_s3_disk/*"
        }
    ]
}

```
Corresponding configuration of ClickHouse®:


```
<clickhouse>
    <storage_configuration>
        <disks>
            <disk_s3>
                <type>s3</type>
                <endpoint>http://s3.us-east-1.amazonaws.com/BUCKET_NAME/test_s3_disk/</endpoint>
                <use_environment_credentials>true</use_environment_credentials>
            </disk_s3>
        </disks>
        <policies>
            <policy_s3_only>
                <volumes>
                    <volume_s3>
                        <disk>disk_s3</disk>
                    </volume_s3>
                </volumes>
            </policy_s3_only>
        </policies>
    </storage_configuration>
</clickhouse>

```
Small check:


```
CREATE TABLE table_s3 (number Int64) ENGINE=MergeTree() ORDER BY tuple() PARTITION BY tuple() SETTINGS storage_policy='policy_s3_only';
INSERT INTO table_s3 SELECT * FROM system.numbers LIMIT 100000000;
SELECT * FROM table_s3;
DROP TABLE table_s3;

```
## How to use AWS IRSA and IAM in the Altinity Kubernetes Operator for ClickHouse to allow S3 backup without Explicit credentials

Install `clickhouse-operator` [https://github.com/Altinity/clickhouse\-operator/tree/master/docs/operator\_installation\_details.md](https://github.com/Altinity/clickhouse-operator/tree/master/docs/operator_installation_details.md)

Create Role and IAM Policy, look details in [https://docs.aws.amazon.com/emr/latest/EMR\-on\-EKS\-DevelopmentGuide/setting\-up\-enable\-IAM.html](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up-enable-IAM.html)

Create service account with annotations


```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: <SERVICE ACOUNT NAME>
  namespace: <NAMESPACE>
  annotations:
     eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>

```
Link service account to podTemplate it will create `AWS_ROLE_ARN` and `AWS_WEB_IDENTITY_TOKEN_FILE` environment variables.


```
apiVersion: "clickhouse.altinity.com/v1"
kind: "ClickHouseInstallation"
metadata:
  name: <NAME>
  namespace: <NAMESPACE>
spec:
  defaults:
     templates:
       podTemplate: <POD_TEMPLATE_NAME>
  templates:
    podTemplates:
      - name: <POD_TEMPLATE_NAME>
        spec:
          serviceAccountName: <SERVICE ACCOUNT NAME>
          containers:
            - name: clickhouse-backup

```
For EC2 instances the same environment variables should be created:


```
AWS_ROLE_ARN=arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>
AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token

```
# 2 \- Clean up orphaned objects on s3

Clean up orphaned objects left in an S3\-backed ClickHouse tiered‐storage### Problems

- TRUNCATE and DROP TABLE remove **metadata only**.
- Long\-running queries, merges or other replicas may still reference parts, so ClickHouse delays removal.
- There are bugs in Clickhouse that leave orphaned files, especially after failures.

### Solutions

- use our utility for garbage collection \- <https://github.com/Altinity/s3gc>
- or create a separate path in the bucket for every table and every replica and remove the whole path in AWS console
- you can also use [clickhouse\-disk](https://clickhouse.com/docs/operations/utilities/clickhouse-disks)
utility to delete s3 data:


```
clickhouse-disks --disk s3 --query "remove /cluster/database/table/replica1"

```
# 3 \- How much data are written to S3 during mutations

Example of how much data ClickHouse® reads and writes to s3 during mutations.## Configuration

S3 disk with disabled merges


```
<clickhouse>
    <storage_configuration>
        <disks>
            <s3disk>
                <type>s3</type>
                <endpoint>https://s3.us-east-1.amazonaws.com/mybucket/test/test/</endpoint>
                <use_environment_credentials>1</use_environment_credentials>  <!-- use IAM AWS role -->
                    <!--access_key_id>xxxx</access_key_id>
                    <secret_access_key>xxx</secret_access_key-->
            </s3disk>
        </disks>
        <policies>
          <s3tiered>
              <volumes>
                  <default>
                      <disk>default</disk>
                  </default>
                  <s3disk>
                      <disk>s3disk</disk>  
                      <prefer_not_to_merge>true</prefer_not_to_merge>
                  </s3disk>
              </volumes>
          </s3tiered>
        </policies>
    </storage_configuration>
</clickhouse>

```
Let’s create a table and load some synthetic data.


```
CREATE TABLE test_s3
(
    `A` Int64,
    `S` String,
    `D` Date
)
ENGINE = MergeTree
PARTITION BY D
ORDER BY A
SETTINGS storage_policy = 's3tiered';

insert into test_s3 select number, number, today() - intDiv(number, 10000000) from numbers(7e8);
0 rows in set. Elapsed: 98.091 sec. Processed 700.36 million rows, 5.60 GB (7.14 million rows/s., 57.12 MB/s.)


select disk_name, partition, sum(rows), formatReadableSize(sum(bytes_on_disk)) size, count() part_count 
from system.parts where table= 'test_s3' and active 
group by disk_name, partition
order by partition;

┌─disk_name─┬─partition──┬─sum(rows)─┬─size──────┬─part_count─┐
│ default   │ 2023-05-06 │  10000000 │ 78.23 MiB │          5 │
│ default   │ 2023-05-07 │  10000000 │ 78.31 MiB │          6 │
│ default   │ 2023-05-08 │  10000000 │ 78.16 MiB │          5 │
....
│ default   │ 2023-07-12 │  10000000 │ 78.21 MiB │          5 │
│ default   │ 2023-07-13 │  10000000 │ 78.23 MiB │          6 │
│ default   │ 2023-07-14 │  10000000 │ 77.39 MiB │          5 │
└───────────┴────────────┴───────────┴───────────┴────────────┘
70 rows in set. Elapsed: 0.023 sec.

```
## Performance of mutations for a local EBS (throughput: 500 MB/s)


```
select * from test_s3 where A=490000000;
1 row in set. Elapsed: 0.020 sec. Processed 8.19 thousand rows, 92.67 KB (419.17 thousand rows/s., 4.74 MB/s.)

select * from test_s3 where S='490000000';
1 row in set. Elapsed: 14.117 sec. Processed 700.00 million rows, 12.49 GB (49.59 million rows/s., 884.68 MB/s.)

delete from test_s3 where S = '490000000';
0 rows in set. Elapsed: 22.192 sec.

delete from test_s3 where A = '490000001';
0 rows in set. Elapsed: 2.243 sec.

alter table test_s3 delete where S = 590000000 settings mutations_sync=2;
0 rows in set. Elapsed: 21.387 sec.

alter table test_s3 delete where A = '590000001' settings mutations_sync=2;
0 rows in set. Elapsed: 3.372 sec.

alter table test_s3 update S='' where S = '690000000' settings mutations_sync=2;
0 rows in set. Elapsed: 20.265 sec.

alter table test_s3 update S='' where A = '690000001' settings mutations_sync=2;
0 rows in set. Elapsed: 1.979 sec.

```
## Let’s move data to S3


```
alter table test_s3 modify TTL D + interval 10 day to disk 's3disk';

-- 10 minutes later
┌─disk_name─┬─partition──┬─sum(rows)─┬─size──────┬─part_count─┐
│ s3disk    │ 2023-05-06 │  10000000 │ 78.23 MiB │          5 │
│ s3disk    │ 2023-05-07 │  10000000 │ 78.31 MiB │          6 │
│ s3disk    │ 2023-05-08 │  10000000 │ 78.16 MiB │          5 │
│ s3disk    │ 2023-05-09 │  10000000 │ 78.21 MiB │          6 │
│ s3disk    │ 2023-05-10 │  10000000 │ 78.21 MiB │          6 │
...
│ s3disk    │ 2023-07-02 │  10000000 │ 78.22 MiB │          5 │
...
│ default   │ 2023-07-11 │  10000000 │ 78.20 MiB │          6 │
│ default   │ 2023-07-12 │  10000000 │ 78.21 MiB │          5 │
│ default   │ 2023-07-13 │  10000000 │ 78.23 MiB │          6 │
│ default   │ 2023-07-14 │  10000000 │ 77.40 MiB │          5 │
└───────────┴────────────┴───────────┴───────────┴────────────┘
70 rows in set. Elapsed: 0.007 sec.

```
### Sizes of a table on S3 and a size of each column


```
select sum(rows), formatReadableSize(sum(bytes_on_disk)) size 
from system.parts where table= 'test_s3' and active and disk_name = 's3disk';
┌─sum(rows)─┬─size─────┐
│ 600000000 │ 4.58 GiB │
└───────────┴──────────┘

SELECT
    database,
    table,
    column,
    formatReadableSize(sum(column_data_compressed_bytes) AS size) AS compressed
FROM system.parts_columns
WHERE (active = 1) AND (database LIKE '%') AND (table LIKE 'test_s3') AND (disk_name = 's3disk')
GROUP BY
    database,
    table,
    column
ORDER BY column ASC

┌─database─┬─table───┬─column─┬─compressed─┐
│ default  │ test_s3 │ A      │ 2.22 GiB   │
│ default  │ test_s3 │ D      │ 5.09 MiB   │
│ default  │ test_s3 │ S      │ 2.33 GiB   │
└──────────┴─────────┴────────┴────────────┘

```
## S3 Statistics of selects


```
select *, _part from test_s3 where A=100000000;
┌─────────A─┬─S─────────┬──────────D─┬─_part──────────────────┐
│ 100000000 │ 100000000 │ 2023-07-08 │ 20230708_106_111_1_738 │
└───────────┴───────────┴────────────┴────────────────────────┘
1 row in set. Elapsed: 0.104 sec. Processed 8.19 thousand rows, 65.56 KB (79.11 thousand rows/s., 633.07 KB/s.)

┌─S3GetObject─┬─S3PutObject─┬─ReadBufferFromS3─┬─WriteBufferFromS3─┐
│           6 │           0 │ 70.58 KiB        │ 0.00 B            │
└─────────────┴─────────────┴──────────────────┴───────────────────┘

```
Select by primary key read only 70\.58 KiB from S3

Size of this part


```
SELECT
    database, table, column,
    formatReadableSize(sum(column_data_compressed_bytes) AS size) AS compressed
FROM system.parts_columns
WHERE (active = 1) AND (database LIKE '%') AND (table LIKE 'test_s3') AND (disk_name = 's3disk')
    and name = '20230708_106_111_1_738'
GROUP BY database, table, column ORDER BY column ASC

┌─database─┬─table───┬─column─┬─compressed─┐
│ default  │ test_s3 │ A      │ 22.51 MiB  │
│ default  │ test_s3 │ D      │ 51.47 KiB  │
│ default  │ test_s3 │ S      │ 23.52 MiB  │
└──────────┴─────────┴────────┴────────────┘

```

```
select * from test_s3 where S='100000000';
┌─────────A─┬─S─────────┬──────────D─┐
│ 100000000 │ 100000000 │ 2023-07-08 │
└───────────┴───────────┴────────────┘
1 row in set. Elapsed: 86.745 sec. Processed 700.00 million rows, 12.49 GB (8.07 million rows/s., 144.04 MB/s.)

┌─S3GetObject─┬─S3PutObject─┬─ReadBufferFromS3─┬─WriteBufferFromS3─┐
│         947 │           0 │ 2.36 GiB         │ 0.00 B            │
└─────────────┴─────────────┴──────────────────┴───────────────────┘

```
Select using fullscan of S column read only 2\.36 GiB from S3, the whole S column (2\.33 GiB) plus parts of A and D.


```

delete from test_s3 where A=100000000;
0 rows in set. Elapsed: 17.429 sec.

┌─q──┬─S3GetObject─┬─S3PutObject─┬─ReadBufferFromS3─┬─WriteBufferFromS3─┐
│ Q3 │        2981 │           6 │ 23.06 MiB        │ 27.25 KiB         │
└────┴─────────────┴─────────────┴──────────────────┴───────────────────┘

insert into test select 'Q3' q, event,value  from system.events where event like '%S3%';


delete from test_s3 where S='100000001';
0 rows in set. Elapsed: 31.417 sec.
┌─q──┬─S3GetObject─┬─S3PutObject─┬─ReadBufferFromS3─┬─WriteBufferFromS3─┐
│ Q4 │        4209 │           6 │ 2.39 GiB         │ 27.25 KiB         │
└────┴─────────────┴─────────────┴──────────────────┴───────────────────┘
insert into test select 'Q4' q, event,value  from system.events where event like '%S3%';



alter table test_s3 delete where A=110000000 settings mutations_sync=2;
0 rows in set. Elapsed: 19.521 sec.

┌─q──┬─S3GetObject─┬─S3PutObject─┬─ReadBufferFromS3─┬─WriteBufferFromS3─┐
│ Q5 │        2986 │          15 │ 42.27 MiB        │ 41.72 MiB         │
└────┴─────────────┴─────────────┴──────────────────┴───────────────────┘
insert into test select 'Q5' q, event,value  from system.events where event like '%S3%';


alter table test_s3 delete where S='110000001' settings mutations_sync=2;
0 rows in set. Elapsed: 29.650 sec.

┌─q──┬─S3GetObject─┬─S3PutObject─┬─ReadBufferFromS3─┬─WriteBufferFromS3─┐
│ Q6 │        4212 │          15 │ 2.42 GiB         │ 41.72 MiB         │
└────┴─────────────┴─────────────┴──────────────────┴───────────────────┘
insert into test select 'Q6' q, event,value  from system.events where event like '%S3%';

```
# 4 \- Example of the table at s3 with cache

s3 disk and s3 cache.## Storage configuration


```
cat /etc/clickhouse-server/config.d/s3.xml
<clickhouse>
    <storage_configuration>
        <disks>
            <s3disk>
                <type>s3</type>
                <endpoint>https://s3.us-east-1.amazonaws.com/mybucket/test/s3cached/</endpoint>
                <use_environment_credentials>1</use_environment_credentials>  <!-- use IAM AWS role -->
                    <!--access_key_id>xxxx</access_key_id>
                    <secret_access_key>xxx</secret_access_key-->
            </s3disk>
            <cache>
                <type>cache</type>
                <disk>s3disk</disk>
                <path>/var/lib/clickhouse/disks/s3_cache/</path>
                <max_size>50Gi</max_size>  <!-- 50GB local cache to cache remote data -->
            </cache>
        </disks>
        <policies>
          <s3tiered>
              <volumes>
                  <default>
                      <disk>default</disk>
                      <max_data_part_size_bytes>50000000000</max_data_part_size_bytes>   <!-- only for parts less than 50GB after they moved to s3 during merges -->         
                  </default>
                  <s3cached>
                      <disk>cache</disk>  <!-- sandwich cache plus s3disk -->
                      <!-- prefer_not_to_merge>true</prefer_not_to_merge>
                      <perform_ttl_move_on_insert>false</perform_ttl_move_on_insert-->
                  </s3cached>
              </volumes>
          </s3tiered>
        </policies>
    </storage_configuration>
</clickhouse>

```

```
select * from system.disks
┌─name────┬─path──────────────────────────────┬───────────free_space─┬──────────total_space─┬
│ cache   │ /var/lib/clickhouse/disks/s3disk/ │ 18446744073709551615 │ 18446744073709551615 │
│ default │ /var/lib/clickhouse/              │         149113987072 │         207907635200 │
│ s3disk  │ /var/lib/clickhouse/disks/s3disk/ │ 18446744073709551615 │ 18446744073709551615 │
└─────────┴───────────────────────────────────┴──────────────────────┴──────────────────────┴

select * from system.storage_policies;
┌─policy_name─┬─volume_name─┬─volume_priority─┬─disks───────┬─volume_type─┬─max_data_part_size─┬─move_factor─┬─prefer_not_to_merge─┐
│ default     │ default     │               1 │ ['default'] │ JBOD        │                  0 │           0 │                   0 │
│ s3tiered    │ default     │               1 │ ['default'] │ JBOD        │        50000000000 │         0.1 │                   0 │
│ s3tiered    │ s3cached    │               2 │ ['s3disk']  │ JBOD        │                  0 │         0.1 │                   0 │
└─────────────┴─────────────┴─────────────────┴─────────────┴─────────────┴────────────────────┴─────────────┴─────────────────────┘

```
## example with a new table


```
CREATE TABLE test_s3
(
    `A` Int64,
    `S` String,
    `D` Date
)
ENGINE = MergeTree
PARTITION BY D
ORDER BY A
SETTINGS storage_policy = 's3tiered';

insert into test_s3 select number, number, '2023-01-01' from numbers(1e9);

0 rows in set. Elapsed: 270.285 sec. Processed 1.00 billion rows, 8.00 GB (3.70 million rows/s., 29.60 MB/s.)

```
Table size is 7\.65 GiB and it at the default disk (EBS):


```
select disk_name, partition, sum(rows), formatReadableSize(sum(bytes_on_disk)) size, count() part_count 
from system.parts where table= 'test_s3' and active 
group by disk_name, partition;
┌─disk_name─┬─partition──┬──sum(rows)─┬─size─────┬─part_count─┐
│ default   │ 2023-01-01 │ 1000000000 │ 7.65 GiB │          8 │
└───────────┴────────────┴────────────┴──────────┴────────────┘

```
It seems my EBS write speed is slower than S3 write speed:


```
alter table test_s3 move partition '2023-01-01' to volume 's3cached';
0 rows in set. Elapsed: 98.979 sec.

alter table test_s3 move partition '2023-01-01' to volume 'default';
0 rows in set. Elapsed: 127.741 sec.

```
Queries performance against EBS:


```
select * from test_s3 where A = 443;
1 row in set. Elapsed: 0.002 sec. Processed 8.19 thousand rows, 71.64 KB (3.36 million rows/s., 29.40 MB/s.)

select uniq(A) from test_s3;
1 row in set. Elapsed: 11.439 sec. Processed 1.00 billion rows, 8.00 GB (87.42 million rows/s., 699.33 MB/s.)

select count() from test_s3 where S like '%4422%'
1 row in set. Elapsed: 17.484 sec. Processed 1.00 billion rows, 17.89 GB (57.20 million rows/s., 1.02 GB/s.)

```
Let’s move data to S3


```
alter table test_s3 move partition '2023-01-01' to volume 's3cached';
0 rows in set. Elapsed: 81.068 sec.

select disk_name, partition, sum(rows), formatReadableSize(sum(bytes_on_disk)) size, count() part_count 
from system.parts where table= 'test_s3' and active 
group by disk_name, partition;
┌─disk_name─┬─partition──┬──sum(rows)─┬─size─────┬─part_count─┐
│ s3disk    │ 2023-01-01 │ 1000000000 │ 7.65 GiB │          8 │
└───────────┴────────────┴────────────┴──────────┴────────────┘

```
The first query execution against S3, the second against the cache (local EBS):


```
select * from test_s3 where A = 443;
1 row in set. Elapsed: 0.458 sec. Processed 8.19 thousand rows, 71.64 KB (17.88 thousand rows/s., 156.35 KB/s.)
1 row in set. Elapsed: 0.003 sec. Processed 8.19 thousand rows, 71.64 KB (3.24 million rows/s., 28.32 MB/s.)

select uniq(A) from test_s3;
1 row in set. Elapsed: 26.601 sec. Processed 1.00 billion rows, 8.00 GB (37.59 million rows/s., 300.74 MB/s.)
1 row in set. Elapsed: 8.675 sec. Processed 1.00 billion rows, 8.00 GB (115.27 million rows/s., 922.15 MB/s.)

select count() from test_s3 where S like '%4422%'
1 row in set. Elapsed: 33.586 sec. Processed 1.00 billion rows, 17.89 GB (29.77 million rows/s., 532.63 MB/s.)
1 row in set. Elapsed: 16.551 sec. Processed 1.00 billion rows, 17.89 GB (60.42 million rows/s., 1.08 GB/s.)

```
Cache introspection


```
select cache_base_path, formatReadableSize(sum(size)) from system.filesystem_cache group by 1;
┌─cache_base_path─────────────────────┬─formatReadableSize(sum(size))─┐
│ /var/lib/clickhouse/disks/s3_cache/ │ 7.64 GiB                      │
└─────────────────────────────────────┴───────────────────────────────┘

system drop FILESYSTEM cache;

select cache_base_path, formatReadableSize(sum(size)) from system.filesystem_cache group by 1;
0 rows in set. Elapsed: 0.005 sec.

select * from test_s3 where A = 443;
1 row in set. Elapsed: 0.221 sec. Processed 8.19 thousand rows, 71.64 KB (37.10 thousand rows/s., 324.47 KB/s.)

select cache_base_path, formatReadableSize(sum(size)) from system.filesystem_cache group by 1;
┌─cache_base_path─────────────────────┬─formatReadableSize(sum(size))─┐
│ /var/lib/clickhouse/disks/s3_cache/ │ 105.95 KiB                    │
└─────────────────────────────────────┴───────────────────────────────┘

```
No data is stored locally (except system log tables).


```
select name, formatReadableSize(free_space) free_space, formatReadableSize(total_space) total_space from system.disks;
┌─name────┬─free_space─┬─total_space─┐
│ cache   │ 16.00 EiB  │ 16.00 EiB   │
│ default │ 48.97 GiB  │ 49.09 GiB   │
│ s3disk  │ 16.00 EiB  │ 16.00 EiB   │
└─────────┴────────────┴─────────────┘

```
## example with an existing table

The `mydata` table is created without the explicitly defined `storage_policy`, it means that implicitly `storage_policy=default` / `volume=default` / `disk=default`.


```
select disk_name, partition, sum(rows), formatReadableSize(sum(bytes_on_disk)) size, count() part_count 
from system.parts where table='mydata' and active 
group by disk_name, partition
order by partition;
┌─disk_name─┬─partition─┬─sum(rows)─┬─size───────┬─part_count─┐
│ default   │ 202201    │ 516666677 │ 4.01 GiB   │         13 │
│ default   │ 202202    │ 466666657 │ 3.64 GiB   │         13 │
│ default   │ 202203    │  16666666 │ 138.36 MiB │         10 │
│ default   │ 202301    │ 516666677 │ 4.01 GiB   │         10 │
│ default   │ 202302    │ 466666657 │ 3.64 GiB   │         10 │
│ default   │ 202303    │  16666666 │ 138.36 MiB │         10 │
└───────────┴───────────┴───────────┴────────────┴────────────┘

-- Let's change the storage policy, this command instant and changes only metadata of the table, and possible because the new storage policy and the old has the volume `default`.

alter table mydata modify setting storage_policy = 's3tiered';

0 rows in set. Elapsed: 0.057 sec.

```
### straightforward (heavy) approach


```
-- Let's add TTL, it's a heavy command and takes a lot time and creates the performance impact, because it reads `D` column and moves parts to s3.
alter table mydata modify TTL D + interval 1 year to volume 's3cached';

0 rows in set. Elapsed: 140.661 sec.

┌─disk_name─┬─partition─┬─sum(rows)─┬─size───────┬─part_count─┐
│ s3disk    │ 202201    │ 516666677 │ 4.01 GiB   │         13 │
│ s3disk    │ 202202    │ 466666657 │ 3.64 GiB   │         13 │
│ s3disk    │ 202203    │  16666666 │ 138.36 MiB │         10 │
│ default   │ 202301    │ 516666677 │ 4.01 GiB   │         10 │
│ default   │ 202302    │ 466666657 │ 3.64 GiB   │         10 │
│ default   │ 202303    │  16666666 │ 138.36 MiB │         10 │
└───────────┴───────────┴───────────┴────────────┴────────────┘

```
### gentle (manual) approach


```
-- alter modify TTL changes only metadata of the table and applied to only newly insterted data.
set materialize_ttl_after_modify=0;
alter table mydata modify TTL D + interval 1 year to volume 's3cached';
0 rows in set. Elapsed: 0.049 sec.

-- move data slowly partition by partition

alter table mydata move partition id '202201' to volume 's3cached';
0 rows in set. Elapsed: 49.410 sec.

alter table mydata move partition id '202202' to volume 's3cached';
0 rows in set. Elapsed: 36.952 sec.

alter table mydata move partition id '202203' to volume 's3cached';
0 rows in set. Elapsed: 4.808 sec.

-- data can be optimized to reduce number of parts before moving it to s3
optimize table mydata partition id '202301' final;
0 rows in set. Elapsed: 66.551 sec.

alter table mydata move partition id '202301' to volume 's3cached';
0 rows in set. Elapsed: 33.332 sec.

┌─disk_name─┬─partition─┬─sum(rows)─┬─size───────┬─part_count─┐
│ s3disk    │ 202201    │ 516666677 │ 4.01 GiB   │         13 │
│ s3disk    │ 202202    │ 466666657 │ 3.64 GiB   │         13 │
│ s3disk    │ 202203    │  16666666 │ 138.36 MiB │         10 │
│ s3disk    │ 202301    │ 516666677 │ 4.01 GiB   │          1 │ -- optimized partition
│ default   │ 202302    │ 466666657 │ 3.64 GiB   │         13 │
│ default   │ 202303    │  16666666 │ 138.36 MiB │         10 │
└───────────┴───────────┴───────────┴────────────┴────────────┘

```
## S3 and ClickHouse® start time

Let’s create a table with 1000 parts and move them to s3\.


```
CREATE TABLE test_s3( A Int64, S String, D Date)
ENGINE = MergeTree PARTITION BY D ORDER BY A
SETTINGS storage_policy = 's3tiered';

insert into test_s3 select number, number, toDate('2000-01-01') + intDiv(number,1e6) from numbers(1e9);
optimize table test_s3 final settings optimize_skip_merged_partitions = 1;

select disk_name, sum(rows), formatReadableSize(sum(bytes_on_disk)) size, count() part_count 
from system.parts where table= 'test_s3' and active group by disk_name;
┌─disk_name─┬──sum(rows)─┬─size─────┬─part_count─┐
│ default   │ 1000000000 │ 7.64 GiB │       1000 │
└───────────┴────────────┴──────────┴────────────┘

alter table test_s3 modify ttl D + interval 1 year to disk 's3disk';

select disk_name, sum(rows), formatReadableSize(sum(bytes_on_disk)) size, count() part_count 
from system.parts where table= 'test_s3' and active 
group by disk_name;
┌─disk_name─┬─sum(rows)─┬─size─────┬─part_count─┐
│ default   │ 755000000 │ 5.77 GiB │        755 │
│ s3disk    │ 245000000 │ 1.87 GiB │        245 │
└───────────┴───────────┴──────────┴────────────┘

----  several minutes later ----

┌─disk_name─┬──sum(rows)─┬─size─────┬─part_count─┐
│ s3disk    │ 1000000000 │ 7.64 GiB │       1000 │
└───────────┴────────────┴──────────┴────────────┘

```
### start time


```
:) select name, value from system.merge_tree_settings where name = 'max_part_loading_threads';
┌─name─────────────────────┬─value─────┐
│ max_part_loading_threads │ 'auto(4)' │
└──────────────────────────┴───────────┘

# systemctl stop clickhouse-server
# time systemctl start clickhouse-server  / real	4m26.766s
# systemctl stop clickhouse-server
# time systemctl start clickhouse-server  / real	4m24.263s

# cat /etc/clickhouse-server/config.d/max_part_loading_threads.xml
<?xml version="1.0"?>
<clickhouse>
    <merge_tree>
       <max_part_loading_threads>128</max_part_loading_threads>
    </merge_tree>
</clickhouse>

# systemctl stop clickhouse-server
# time systemctl start clickhouse-server / real	0m11.225s
# systemctl stop clickhouse-server
# time systemctl start clickhouse-server / real	0m10.797s

       <max_part_loading_threads>256</max_part_loading_threads>

# systemctl stop clickhouse-server
# time systemctl start clickhouse-server / real	0m8.474s
# systemctl stop clickhouse-server
# time systemctl start clickhouse-server / real	0m8.130s

```
# 5 \- S3Disk

## Settings


```
<clickhouse>
  <storage_configuration>
    <disks>
      <s3>
        <type>s3</type>
        <endpoint>http://s3.us-east-1.amazonaws.com/BUCKET_NAME/test_s3_disk/</endpoint>
        <access_key_id>ACCESS_KEY_ID</access_key_id>
        <secret_access_key>SECRET_ACCESS_KEY</secret_access_key>
        <skip_access_check>true</skip_access_check>
        <send_metadata>true</send_metadata>
      </s3>
    </disks>
  </storage_configuration>
</clickhouse>

```
- skip\_access\_check — if true, it’s possible to use read only credentials with regular MergeTree table. But you would need to disable merges (`prefer_not_to_merge` setting) on s3 volume as well.
- send\_metadata — if true, ClickHouse® will populate s3 object with initial part \& file path, which allow you to recover metadata from s3 and make debug easier.

## Restore metadata from S3

### Default

Limitations:

1. ClickHouse need RW access to this bucket

In order to restore metadata, you would need to create restore file in `metadata_path/_s3_disk_name_` directory:


```
touch /var/lib/clickhouse/disks/_s3_disk_name_/restore

```
In that case ClickHouse would restore to the same bucket and path and update only metadata files in s3 bucket.

### Custom

Limitations:

1. ClickHouse needs RO access to the old bucket and RW to the new.
2. ClickHouse will copy objects in case of restoring to a different bucket or path.

If you would like to change bucket or path, you need to populate restore file with settings in key\=value format:


```
cat /var/lib/clickhouse/disks/_s3_disk_name_/restore

source_bucket=s3disk
source_path=vol1/

```
## Links

- [https://altinity.com/blog/integrating\-clickhouse\-with\-minio](https://altinity.com/blog/integrating-clickhouse-with-minio)
- [https://altinity.com/blog/clickhouse\-object\-storage\-performance\-minio\-vs\-aws\-s3](https://altinity.com/blog/clickhouse-object-storage-performance-minio-vs-aws-s3)
- [https://altinity.com/blog/tips\-for\-high\-performance\-clickhouse\-clusters\-with\-s3\-object\-storage](https://altinity.com/blog/tips-for-high-performance-clickhouse-clusters-with-s3-object-storage)

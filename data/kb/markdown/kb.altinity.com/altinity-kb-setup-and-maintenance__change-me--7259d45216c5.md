# Replication: Can not resolve host of another ClickHouse® server \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Replication: Can not resolve host of another ClickHouse® server
# Replication: Can not resolve host of another ClickHouse® server

### Symptom

When configuring Replication the ClickHouse® cluster nodes are experiencing communication issues, and an error message appears in the log that states that the ClickHouse host cannot be resolved.


```
<Error> DNSResolver: Cannot resolve host (xxxxx), error 0: DNS error.
 auto DB::StorageReplicatedMergeTree::processQueueEntry(ReplicatedMergeTreeQueue::SelectedEntryPtr)::(anonymous class)::operator()(DB::StorageReplicatedMergeTree::LogEntryPtr &) const: Code: 198. DB::Exception: Not found address of host: xxxx. (DNS_ERROR),

```
### Cause:

The error message indicates that the host name of the one of the nodes of the cluster cannot be resolved by other cluster members, causing communication issues between the nodes.

Each node in the replication setup pushes its Fully Qualified Domain Name (FQDN) to Zookeeper, and if other nodes cannot access it using its FQDN, this can cause issues.

### Action:

There are two possible solutions to this problem:

1. Change the FQDN to allow other nodes to access it. This solution can also help to keep the environment more organized. To do this, use the following command to edit the hostname file:


```
sudo vim /etc/hostname

```
Or use the following command to change the hostname:


```
sudo hostnamectl set-hostname ...

```
2. Use the configuration parameter `<interserver_http_host>` to specify the IP address or hostname that the nodes can use to communicate with each other. This solution can have some issues, such as the one described in this link: <https://github.com/ClickHouse/ClickHouse/issues/2154>
.
To configure this parameter, refer to the documentation for more information: [https://clickhouse.com/docs/en/operations/server\-configuration\-parameters/settings/\#interserver\-http\-host](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings/#interserver-http-host)
.

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)

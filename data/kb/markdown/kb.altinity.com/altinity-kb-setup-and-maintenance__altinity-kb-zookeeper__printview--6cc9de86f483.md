# ZooKeeper \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/).

# ZooKeeper

ZooKeeper- 1: [clickhouse\-keeper\-initd](#pg-fe6c92b41d659a61ae843a9c968db4e3)
- 2: [clickhouse\-keeper\-service](#pg-582314d0ec1bd636faae316fd661315c)
- 3: [Install standalone Zookeeper for ClickHouse® on Ubuntu / Debian](#pg-05425e768ddcc5be5d1203f59044e6d5)
- 4: [How to check the list of watches](#pg-564a3bbd39f9550e577334d912a883dc)
- 5: [JVM sizes and garbage collector settings](#pg-722cb96284be123698aa3e56ea92ecaf)
- 6: [Proper setup](#pg-1ef2081889fb4a086febf3b281e44778)
- 7: [Recovering from complete metadata loss in ZooKeeper](#pg-66b660806f12af38114754857823e52a)
- 8: [Using clickhouse\-keeper](#pg-4c33701373e85b893c3b3464fa4f6683)
- 9: [ZooKeeper backup](#pg-8892167f56e913cb6f2d429fc16315c8)
- 10: [ZooKeeper cluster migration](#pg-f9f14245cdbc89d13e77a5b1b24de46e)
- 11: [ZooKeeper cluster migration when using K8s node local storage](#pg-9eb0d707fbf1e834507aa5b61897fc15)
- 12: [ZooKeeper Monitoring](#pg-4b2037cae63d87dd18115b5fa7174451)
- 13: [ZooKeeper schema](#pg-caaac474228860d2cc9228c7ba1fb3f9)

### Requirements

TLDR version:

1. USE DEDICATED FAST DISKS for the transaction log! (crucial for performance due to write\-ahead\-log, NVMe is preferred for heavy load setup).
2. use 3 nodes (more nodes \= slower quorum, less \= no HA).
3. low network latency between zookeeper nodes is very important (latency, not bandwidth).
4. have at least 4Gb of RAM, disable swap, [tune JVM sizes, and garbage collector settings](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/jvm-sizes-and-garbage-collector-settings/)
5. ensure that zookeeper will not be CPU\-starved by some other processes
6. [monitor zookeeper](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/zookeeper-monitoring/)
.

Side note:
in many cases, the slowness of the zookeeper is actually a symptom of some issue with ClickHouse® schema/usage pattern (the most typical issues: an enormous number of partitions/tables/databases with real\-time inserts, tiny \& frequent inserts).

### How to install

- [https://docs.altinity.com/operationsguide/clickhouse\-zookeeper/zookeeper\-installation/](https://docs.altinity.com/operationsguide/clickhouse-zookeeper/zookeeper-installation/)
- [altinity\-kb\-setup\-and\-maintenance/altinity\-kb\-zookeeper/install\_ubuntu/](/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/install_ubuntu/)

### Random links on best practices

- <https://docs.confluent.io/platform/current/zookeeper/deployment.html>
- [https://zookeeper.apache.org/doc/r3\.4\.9/zookeeperAdmin.html\#sc\_commonProblems](https://zookeeper.apache.org/doc/r3.4.9/zookeeperAdmin.html#sc_commonProblems)
- [https://clickhouse.tech/docs/en/operations/tips/\#zookeeper](https://clickhouse.tech/docs/en/operations/tips/#zookeeper)
- [https://lucene.apache.org/solr/guide/7\_4/setting\-up\-an\-external\-zookeeper\-ensemble.html](https://lucene.apache.org/solr/guide/7_4/setting-up-an-external-zookeeper-ensemble.html)
- <https://cwiki.apache.org/confluence/display/ZOOKEEPER/Troubleshooting>

Cite from [https://zookeeper.apache.org/doc/r3\.5\.7/zookeeperAdmin.html\#sc\_commonProblems](https://zookeeper.apache.org/doc/r3.5.7/zookeeperAdmin.html#sc_commonProblems)
:


> ## Things to Avoid
> 
> Here are some common problems you can avoid by configuring ZooKeeper correctly:
> 
> - *inconsistent lists of servers* : The list of ZooKeeper servers used by the clients must match the list of ZooKeeper servers that each ZooKeeper server has. Things work okay if the client list is a subset of the real list, but things will really act strange if clients have a list of ZooKeeper servers that are in different ZooKeeper clusters. Also, the server lists in each Zookeeper server configuration file should be consistent with one another.
> - *incorrect placement of transaction log* : The most performance critical part of ZooKeeper is the transaction log. ZooKeeper syncs transactions to media before it returns a response. A dedicated transaction log device is key to consistent good performance. Putting the log on a busy device will adversely affect performance. If you only have one storage device, increase the snapCount so that snapshot files are generated less often; it does not eliminate the problem, but it makes more resources available for the transaction log.
> - *incorrect Java heap size* : You should take special care to set your Java max heap size correctly. In particular, you should not create a situation in which ZooKeeper swaps to disk. The disk is death to ZooKeeper. Everything is ordered, so if processing one request swaps the disk, all other queued requests will probably do the same. the disk. DON’T SWAP. Be conservative in your estimates: if you have 4G of RAM, do not set the Java max heap size to 6G or even 4G. For example, it is more likely you would use a 3G heap for a 4G machine, as the operating system and the cache also need memory. The best and only recommend practice for estimating the heap size your system needs is to run load tests, and then make sure you are well below the usage limit that would cause the system to swap.
> - *Publicly accessible deployment* : A ZooKeeper ensemble is expected to operate in a trusted computing environment. It is thus recommended to deploy ZooKeeper behind a firewall.

### How to check number of followers:


```
echo mntr | nc zookeeper 2187 | grep foll
zk_synced_followers    2
zk_synced_non_voting_followers    0
zk_avg_follower_sync_time    0.0
zk_min_follower_sync_time    0
zk_max_follower_sync_time    0
zk_cnt_follower_sync_time    0
zk_sum_follower_sync_time    0

```
## Tools

[https://github.com/apache/zookeeper/blob/master/zookeeper\-docs/src/main/resources/markdown/zookeeperTools.md](https://github.com/apache/zookeeper/blob/master/zookeeper-docs/src/main/resources/markdown/zookeeperTools.md)

## Alternative for zkCli

- [https://github.com/go\-zkcli/zkcli](https://github.com/go-zkcli/zkcli)

## Web UI

- [https://github.com/elkozmon/zoonavigator\-api](https://github.com/elkozmon/zoonavigator-api)
- [https://github.com/tobilg/docker\-zookeeper\-webui](https://github.com/tobilg/docker-zookeeper-webui)
- [https://github.com/vran\-dev/PrettyZoo](https://github.com/vran-dev/PrettyZoo)
# 1 \- clickhouse\-keeper\-initd

clickhouse\-keeper\-initd## clickhouse\-keeper\-initd

An init.d script for clickhouse\-keeper.
This example is based on zkServer.sh


```
#!/bin/bash
### BEGIN INIT INFO
# Provides:          clickhouse-keeper
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Required-Start:
# Required-Stop:
# Short-Description: Start keeper daemon
# Description: Start keeper daemon
### END INIT INFO

NAME=clickhouse-keeper
ZOOCFGDIR=/etc/$NAME
ZOOCFG="$ZOOCFGDIR/keeper.xml"
ZOO_LOG_DIR=/var/log/$NAME
USER=clickhouse
GROUP=clickhouse
ZOOPIDDIR=/var/run/$NAME
ZOOPIDFILE=$ZOOPIDDIR/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

#echo "Using config: $ZOOCFG" >&2
ZOOCMD="clickhouse-keeper -C ${ZOOCFG} start --daemon"

# ensure PIDDIR exists, otw stop will fail
mkdir -p "$(dirname "$ZOOPIDFILE")"

if [ ! -w "$ZOO_LOG_DIR" ] ; then
mkdir -p "$ZOO_LOG_DIR"
fi

case $1 in
start)
    echo -n "Starting keeper ... "
    if [ -f "$ZOOPIDFILE" ]; then
      if kill -0 `cat "$ZOOPIDFILE"` > /dev/null 2>&1; then
         echo already running as process `cat "$ZOOPIDFILE"`.
         exit 0
      fi
    fi
    sudo -u clickhouse `echo "$ZOOCMD"`
    if [ $? -eq 0 ]
    then
      pgrep -f "$ZOOCMD" > "$ZOOPIDFILE"
      echo "PID:" `cat $ZOOPIDFILE`
      if [ $? -eq 0 ];
      then
        sleep 1
        echo STARTED
      else
        echo FAILED TO WRITE PID
        exit 1
      fi
    else
      echo SERVER DID NOT START
      exit 1
    fi
    ;;
start-foreground)
    sudo -u clickhouse clickhouse-keeper -C "$ZOOCFG" start
    ;;
print-cmd)
    echo "sudo -u clickhouse ${ZOOCMD}"
    ;;
stop)
    echo -n "Stopping keeper ... "
    if [ ! -f "$ZOOPIDFILE" ]
    then
      echo "no keeper to stop (could not find file $ZOOPIDFILE)"
    else
      ZOOPID=$(cat "$ZOOPIDFILE")
      echo $ZOOPID
      kill $ZOOPID
      while true; do
         sleep 3
         if kill -0 $ZOOPID > /dev/null 2>&1; then
            echo $ZOOPID is still running
         else
            break
         fi
      done
      rm "$ZOOPIDFILE"
      echo STOPPED
    fi
    exit 0
    ;;
restart)
    shift
    "$0" stop ${@}
    sleep 3
    "$0" start ${@}
    ;;
status)
    clientPortAddress="localhost"
    clientPort=2181
    STAT=`echo srvr | nc $clientPortAddress $clientPort 2> /dev/null | grep Mode`
    if [ "x$STAT" = "x" ]
    then
        echo "Error contacting service. It is probably not running."
        exit 1
    else
        echo $STAT
        exit 0
    fi
    ;;
*)
    echo "Usage: $0 {start|start-foreground|stop|restart|status|print-cmd}" >&2

esac

```
# 2 \- clickhouse\-keeper\-service

clickhouse\-keeper\-service## clickhouse\-keeper\-service

### installation

Need to install `clickhouse-common-static` \+ `clickhouse-keeper` OR `clickhouse-common-static` \+ `clickhouse-server`.
Both OK, use the first if you don’t need ClickHouse® server locally.


```
dpkg -i clickhouse-common-static_{%version}.deb clickhouse-keeper_{%version}.deb

```

```
dpkg -i clickhouse-common-static_{%version}.deb clickhouse-server_{%version}.deb clickhouse-client_{%version}.deb

```
Create directories


```
mkdir -p /etc/clickhouse-keeper/config.d
mkdir -p /var/log/clickhouse-keeper
mkdir -p /var/lib/clickhouse-keeper/coordination/log
mkdir -p /var/lib/clickhouse-keeper/coordination/snapshots
mkdir -p /var/lib/clickhouse-keeper/cores

chown -R clickhouse.clickhouse /etc/clickhouse-keeper /var/log/clickhouse-keeper /var/lib/clickhouse-keeper

```
### config


```
cat /etc/clickhouse-keeper/config.xml

<?xml version="1.0"?>
<clickhouse>
    <logger>
        <!-- Possible levels [1]:

          - none (turns off logging)
          - fatal
          - critical
          - error
          - warning
          - notice
          - information
          - debug
          - trace
          - test (not for production usage)

            [1]: https://github.com/pocoproject/poco/blob/poco-1.9.4-release/Foundation/include/Poco/Logger.h#L105-L114
        -->
        <level>trace</level>
        <log>/var/log/clickhouse-keeper/clickhouse-keeper.log</log>
        <errorlog>/var/log/clickhouse-keeper/clickhouse-keeper.err.log</errorlog>
        <!-- Rotation policy
             See https://github.com/pocoproject/poco/blob/poco-1.9.4-release/Foundation/include/Poco/FileChannel.h#L54-L85
          -->
        <size>1000M</size>
        <count>10</count>
        <!-- <console>1</console> --> <!-- Default behavior is autodetection (log to console if not daemon mode and is tty) -->

        <!-- Per level overrides (legacy):

        For example to suppress logging of the ConfigReloader you can use:
        NOTE: levels.logger is reserved, see below.
        -->
        <!--
        <levels>
          <ConfigReloader>none</ConfigReloader>
        </levels>
        -->

        <!-- Per level overrides:

        For example to suppress logging of the RBAC for default user you can use:
        (But please note that the logger name maybe changed from version to version, even after minor upgrade)
        -->
        <!--
        <levels>
          <logger>
            <name>ContextAccess (default)</name>
            <level>none</level>
          </logger>
          <logger>
            <name>DatabaseOrdinary (test)</name>
            <level>none</level>
          </logger>
        </levels>
        -->
        <!-- Structured log formatting:
        You can specify log format(for now, JSON only). In that case, the console log will be printed
        in specified format like JSON.
        For example, as below:
        {"date_time":"1650918987.180175","thread_name":"#1","thread_id":"254545","level":"Trace","query_id":"","logger_name":"BaseDaemon","message":"Received signal 2","source_file":"../base/daemon/BaseDaemon.cpp; virtual void SignalListener::run()","source_line":"192"}
        To enable JSON logging support, just uncomment <formatting> tag below.
        -->
        <!-- <formatting>json</formatting> -->
    </logger>

    <!-- Listen specified address.
     Use :: (wildcard IPv6 address), if you want to accept connections both with IPv4 and IPv6 from everywhere.
     Notes:
     If you open connections from wildcard address, make sure that at least one of the following measures applied:
     - server is protected by firewall and not accessible from untrusted networks;
     - all users are restricted to subset of network addresses (see users.xml);
     - all users have strong passwords, only secure (TLS) interfaces are accessible, or connections are only made via TLS interfaces.
     - users without password have readonly access.
     See also: https://www.shodan.io/search?query=clickhouse
    -->
    <!-- <listen_host>::</listen_host> -->


    <!-- Same for hosts without support for IPv6: -->
    <!-- <listen_host>0.0.0.0</listen_host> -->

    <!-- Default values - try listen localhost on IPv4 and IPv6. -->
    <!--
    <listen_host>::1</listen_host>
    <listen_host>127.0.0.1</listen_host>
    -->

    <!-- <interserver_listen_host>::</interserver_listen_host> -->
    <!-- Listen host for communication between replicas. Used for data exchange -->
    <!-- Default values - equal to listen_host -->

    <!-- Don't exit if IPv6 or IPv4 networks are unavailable while trying to listen. -->
    <!-- <listen_try>0</listen_try> -->

    <!-- Allow multiple servers to listen on the same address:port. This is not recommended.
    -->
    <!-- <listen_reuse_port>0</listen_reuse_port> -->
    <!-- <listen_backlog>4096</listen_backlog> -->

    <path>/var/lib/clickhouse-keeper/</path>
    <core_path>/var/lib/clickhouse-keeper/cores</core_path>

    <keeper_server>
	    <tcp_port>2181</tcp_port>
	    <server_id>1</server_id>
	    <log_storage_path>/var/lib/clickhouse-keeper/coordination/log</log_storage_path>
	    <snapshot_storage_path>/var/lib/clickhouse-keeper/coordination/snapshots</snapshot_storage_path>

	    <coordination_settings>
        	<operation_timeout_ms>10000</operation_timeout_ms>
	        <session_timeout_ms>30000</session_timeout_ms>
	        <raft_logs_level>trace</raft_logs_level>
	        <rotate_log_storage_interval>10000</rotate_log_storage_interval>
	    </coordination_settings>

            <raft_configuration>
	              <server>
                   <id>1</id>
                   <hostname>localhost</hostname>
                   <port>9444</port>
                </server>
           </raft_configuration>
    </keeper_server>
</clickhouse>

```

```
cat /etc/clickhouse-keeper/config.d/keeper.xml
<?xml version="1.0"?>
<clickhouse>
    <listen_host>::</listen_host>
    <keeper_server>
            <tcp_port>2181</tcp_port>
            <server_id>1</server_id>
            <raft_configuration>
                <server>
                   <id>1</id>
       	           <hostname>keeper-host-1</hostname>
                   <port>9444</port>
                </server>
                <server>
                   <id>2</id>
                   <hostname>keeper-host-2</hostname>
                   <port>9444</port>
                </server>
                <server>
                   <id>3</id>
                   <hostname>keeper-host-3</hostname>
                   <port>9444</port>
                </server>                
           </raft_configuration>
    </keeper_server>
</clickhouse>

```
### systemd service


```
cat /lib/systemd/system/clickhouse-keeper.service
[Unit]
Description=ClickHouse Keeper (analytic DBMS for big data)
Requires=network-online.target
# NOTE: that After/Wants=time-sync.target is not enough, you need to ensure
# that the time was adjusted already, if you use systemd-timesyncd you are
# safe, but if you use ntp or some other daemon, you should configure it
# additionaly.
After=time-sync.target network-online.target
Wants=time-sync.target

[Service]
Type=simple
User=clickhouse
Group=clickhouse
Restart=always
RestartSec=30
RuntimeDirectory=clickhouse-keeper
ExecStart=/usr/bin/clickhouse-keeper --config=/etc/clickhouse-keeper/config.xml --pid-file=/run/clickhouse-keeper/clickhouse-keeper.pid
# Minus means that this file is optional.
EnvironmentFile=-/etc/default/clickhouse
LimitCORE=infinity
LimitNOFILE=500000
CapabilityBoundingSet=CAP_NET_ADMIN CAP_IPC_LOCK CAP_SYS_NICE CAP_NET_BIND_SERVICE

[Install]
# ClickHouse should not start from the rescue shell (rescue.target).
WantedBy=multi-user.target

```

```
systemctl daemon-reload

systemctl status clickhouse-keeper

systemctl start clickhouse-keeper

```
### debug start without service (as foreground application)


```
sudo -u clickhouse /usr/bin/clickhouse-keeper --config=/etc/clickhouse-keeper/config.xml

```
# 3 \- Install standalone Zookeeper for ClickHouse® on Ubuntu / Debian

Install standalone Zookeeper for ClickHouse® on Ubuntu / Debian.## Reference script to install standalone Zookeeper for Ubuntu / Debian

Tested on Ubuntu 20\.


```
# install java runtime environment
sudo apt-get update
sudo apt install default-jre

# prepare folders, logs folder should be on the low-latency disk.
sudo mkdir -p /var/lib/zookeeper/data /var/lib/zookeeper/logs /etc/zookeeper /var/log/zookeeper /opt 

# download and install files 
export ZOOKEEPER_VERSION=3.6.3
wget https://dlcdn.apache.org/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz -O /tmp/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz
sudo tar -xvf /tmp/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz -C /opt
rm -rf /tmp/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz

# create the user 
sudo groupadd -r zookeeper
sudo useradd -r -g zookeeper --home-dir=/var/lib/zookeeper --shell=/bin/false zookeeper

# symlink pointing to the used version of zookeeper distibution
sudo ln -s /opt/apache-zookeeper-${ZOOKEEPER_VERSION}-bin /opt/zookeeper 
sudo chown -R zookeeper:zookeeper /var/lib/zookeeper /var/log/zookeeper /etc/zookeeper /opt/apache-zookeeper-${ZOOKEEPER_VERSION}-bin
sudo chown -h zookeeper:zookeeper /opt/zookeeper

# shortcuts in /usr/local/bin/
echo -e '#!/usr/bin/env bash\n/opt/zookeeper/bin/zkCli.sh "$@"'             | sudo tee /usr/local/bin/zkCli
echo -e '#!/usr/bin/env bash\n/opt/zookeeper/bin/zkServer.sh "$@"'          | sudo tee /usr/local/bin/zkServer
echo -e '#!/usr/bin/env bash\n/opt/zookeeper/bin/zkCleanup.sh "$@"'         | sudo tee /usr/local/bin/zkCleanup
echo -e '#!/usr/bin/env bash\n/opt/zookeeper/bin/zkSnapShotToolkit.sh "$@"' | sudo tee /usr/local/bin/zkSnapShotToolkit
echo -e '#!/usr/bin/env bash\n/opt/zookeeper/bin/zkTxnLogToolkit.sh "$@"'   | sudo tee /usr/local/bin/zkTxnLogToolkit
sudo chmod +x /usr/local/bin/zkCli /usr/local/bin/zkServer /usr/local/bin/zkCleanup /usr/local/bin/zkSnapShotToolkit /usr/local/bin/zkTxnLogToolkit

# put in the config
sudo cp opt/zookeeper/conf/* /etc/zookeeper
cat <<EOF | sudo tee /etc/zookeeper/zoo.cfg
initLimit=20
syncLimit=10
maxSessionTimeout=60000000
maxClientCnxns=2000
preAllocSize=131072
snapCount=3000000
dataDir=/var/lib/zookeeper/data
dataLogDir=/var/lib/zookeeper/logs # use low-latency disk!
clientPort=2181
#clientPortAddress=nthk-zoo1.localdomain
autopurge.snapRetainCount=10
autopurge.purgeInterval=1
4lw.commands.whitelist=*
EOF
sudo chown -R zookeeper:zookeeper /etc/zookeeper

# create systemd service file
cat <<EOF | sudo tee /etc/systemd/system/zookeeper.service
[Unit]
Description=Zookeeper Daemon
Documentation=http://zookeeper.apache.org
Requires=network.target
After=network.target

[Service]
Type=forking
WorkingDirectory=/var/lib/zookeeper
User=zookeeper
Group=zookeeper
Environment=ZK_SERVER_HEAP=1536 # in megabytes, adjust to ~ 80-90% of avaliable RAM (more than 8Gb is rather overkill)
Environment=SERVER_JVMFLAGS="-Xms256m -XX:+AlwaysPreTouch -Djute.maxbuffer=8388608 -XX:MaxGCPauseMillis=50"
Environment=ZOO_LOG_DIR=/var/log/zookeeper
ExecStart=/opt/zookeeper/bin/zkServer.sh start /etc/zookeeper/zoo.cfg
ExecStop=/opt/zookeeper/bin/zkServer.sh stop /etc/zookeeper/zoo.cfg
ExecReload=/opt/zookeeper/bin/zkServer.sh restart /etc/zookeeper/zoo.cfg
TimeoutSec=30
Restart=on-failure

[Install]
WantedBy=default.target
EOF

# start zookeeper
sudo systemctl daemon-reload
sudo systemctl start zookeeper.service 

# check status etc.
echo stat | nc localhost 2181
echo ruok | nc localhost 2181
echo mntr | nc localhost 2181

```
# 4 \- How to check the list of watches

How to check the list of watchesZookeeper use watches to notify a client on znode changes. This article explains how to check watches set by ZooKeeper servers and how it is used.

**Solution:**

Zookeeper uses the `'wchc'` command to list all watches set on the Zookeeper server.

`# echo wchc | nc zookeeper 2181`

Reference

[https://zookeeper.apache.org/doc/r3\.4\.12/zookeeperAdmin.html](https://zookeeper.apache.org/doc/r3.4.12/zookeeperAdmin.html)

The `wchp` and `wchc` commands are not enabled by default because of their known DOS vulnerability. For more information, see [ZOOKEEPER\-2693](https://issues.apache.org/jira/browse/ZOOKEEPER-2693)
and [Zookeeper 3\.5\.2 \- Denial of Service](https://vulners.com/exploitdb/EDB-ID:41277)
.

By default those commands are disabled, they can be enabled via Java system property:

`-Dzookeeper.4lw.commands.whitelist=*`

on in zookeeper config: `4lw.commands.whitelist=*`\\

# 5 \- JVM sizes and garbage collector settings

JVM sizes and garbage collector settings## TLDR version

use fresh Java version (11 or newer), disable swap and set up (for 4 Gb node):


```
JAVA_OPTS="-Xms512m -Xmx3G -XX:+AlwaysPreTouch -Djute.maxbuffer=8388608 -XX:MaxGCPauseMillis=50"

```
If you have a node with more RAM \- change it accordingly, for example for 8Gb node:


```
JAVA_OPTS="-Xms512m -Xmx7G -XX:+AlwaysPreTouch -Djute.maxbuffer=8388608 -XX:MaxGCPauseMillis=50"

```
## Details

1. ZooKeeper runs as in JVM. Depending on version different garbage collectors are available.
2. Recent JVM versions (starting from 10\) use `G1` garbage collector by default (should work fine).
On JVM 13\-14 using `ZGC` or `Shenandoah` garbage collector may reduce pauses.
On older JVM version (before 10\) you may want to make some tuning to decrease pauses, ParNew \+ CMS garbage collectors (like in Yandex config) is one of the best options.
3. One of the most important setting for JVM application is heap size. A heap size of \>1 GB is recommended for most use cases and monitoring heap usage to ensure no delays are caused by garbage collection. We recommend to use at least 4Gb of RAM for zookeeper nodes (8Gb is better, that will make difference only when zookeeper is heavily loaded).

Set the Java heap size smaller than available RAM size on the node. This is very important to avoid swapping, which will seriously degrade ZooKeeper performance. Be conservative \- use a maximum heap size of 3GB for a 4GB machine.

1. Add `XX:+AlwaysPreTouch` flag as well to load the memory pages into memory at the start of the zookeeper.
2. Set min (`Xms`) heap size to the values like 512Mb, or even to the same value as max (`Xmx`) to avoid resizing and returning the RAM to OS. Add `XX:+AlwaysPreTouch` flag as well to load the memory pages into memory at the start of the zookeeper.
3. `MaxGCPauseMillis=50` (by default 200\) \- the ’target’ acceptable pause for garbage collection (milliseconds)
4. `jute.maxbuffer` limits the maximum size of znode content. By default it’s 1Mb. In some usecases (lot of partitions in table) ClickHouse® may need to create bigger znodes.
5. (optional) enable GC logs: `-Xloggc:/path_to/gc.log`

## Zookeeper configuration used by Yandex Metrika (from 2017\)

The configuration used by Yandex ( [https://clickhouse.com/docs/en/operations/tips\#zookeeper](https://clickhouse.com/docs/en/operations/tips#zookeeper)
) \- they use older JVM version (with `UseParNewGC` garbage collector), and tune GC logs heavily:


```
JAVA_OPTS="-Xms{{ cluster.get('xms','128M') }} \
    -Xmx{{ cluster.get('xmx','1G') }} \
    -Xloggc:/var/log/$NAME/zookeeper-gc.log \
    -XX:+UseGCLogFileRotation \
    -XX:NumberOfGCLogFiles=16 \
    -XX:GCLogFileSize=16M \
    -verbose:gc \
    -XX:+PrintGCTimeStamps \
    -XX:+PrintGCDateStamps \
    -XX:+PrintGCDetails
    -XX:+PrintTenuringDistribution \
    -XX:+PrintGCApplicationStoppedTime \
    -XX:+PrintGCApplicationConcurrentTime \
    -XX:+PrintSafepointStatistics \
    -XX:+UseParNewGC \
    -XX:+UseConcMarkSweepGC \
    -XX:+CMSParallelRemarkEnabled"

```
## See also

- [https://wikitech.wikimedia.org/wiki/JVM\_Tuning\#G1\_for\_full\_gcs](https://wikitech.wikimedia.org/wiki/JVM_Tuning#G1_for_full_gcs)
- [https://sematext.com/blog/java\-garbage\-collection\-tuning/](https://sematext.com/blog/java-garbage-collection-tuning/)
- [https://www.oracle.com/technical\-resources/articles/java/g1gc.html](https://www.oracle.com/technical-resources/articles/java/g1gc.html)
- [https://docs.oracle.com/cd/E40972\_01/doc.70/e40973/cnf\_jvmgc.htm\#autoId2](https://docs.oracle.com/cd/E40972_01/doc.70/e40973/cnf_jvmgc.htm#autoId2)
- [https://docs.cloudera.com/runtime/7\.2\.7/kafka\-performance\-tuning/topics/kafka\-tune\-broker\-tuning\-jvm.html](https://docs.cloudera.com/runtime/7.2.7/kafka-performance-tuning/topics/kafka-tune-broker-tuning-jvm.html)
- [https://docs.cloudera.com/documentation/enterprise/6/6\.3/topics/cm\-tune\-g1gc.html](https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/cm-tune-g1gc.html)
- [https://www.maknesium.de/21\-most\-important\-java\-8\-vm\-options\-for\-servers](https://www.maknesium.de/21-most-important-java-8-vm-options-for-servers)
- [https://docs.oracle.com/javase/10/gctuning/introduction\-garbage\-collection\-tuning.htm\#JSGCT\-GUID\-326EB4CF\-8C8C\-4267\-8355\-21AB04F0D304](https://docs.oracle.com/javase/10/gctuning/introduction-garbage-collection-tuning.htm#JSGCT-GUID-326EB4CF-8C8C-4267-8355-21AB04F0D304)
- <https://github.com/chewiebug/GCViewer>
# 6 \- Proper setup

Proper setup### Main docs article

[https://docs.altinity.com/operationsguide/clickhouse\-zookeeper/zookeeper\-installation/](https://docs.altinity.com/operationsguide/clickhouse-zookeeper/zookeeper-installation/)

### Hardware requirements

TLDR version:

1. USE DEDICATED FAST DISKS for the transaction log! (crucial for performance due to write\-ahead\-log, NVMe is preferred for heavy load setup).
2. use 3 nodes (more nodes \= slower quorum, less \= no HA).
3. low network latency between zookeeper nodes is very important (latency, not bandwidth).
4. have at least 4Gb of RAM, disable swap, tune JVM sizes, and garbage collector settings.
5. ensure that zookeeper will not be CPU\-starved by some other processes
6. monitor zookeeper.

Side note:
in many cases, the slowness of the zookeeper is actually a symptom of some issue with ClickHouse® schema/usage pattern (the most typical issues: an enormous number of partitions/tables/databases with real\-time inserts, tiny \& frequent inserts).

Some doc about that subject:

- <https://docs.confluent.io/platform/current/zookeeper/deployment.html>
- [https://zookeeper.apache.org/doc/r3\.4\.9/zookeeperAdmin.html\#sc\_commonProblems](https://zookeeper.apache.org/doc/r3.4.9/zookeeperAdmin.html#sc_commonProblems)
- [https://clickhouse.tech/docs/en/operations/tips/\#zookeeper](https://clickhouse.tech/docs/en/operations/tips/#zookeeper)
- [https://lucene.apache.org/solr/guide/7\_4/setting\-up\-an\-external\-zookeeper\-ensemble.html](https://lucene.apache.org/solr/guide/7_4/setting-up-an-external-zookeeper-ensemble.html)
- <https://cwiki.apache.org/confluence/display/ZOOKEEPER/Troubleshooting>

Cite from [https://zookeeper.apache.org/doc/r3\.5\.7/zookeeperAdmin.html\#sc\_commonProblems](https://zookeeper.apache.org/doc/r3.5.7/zookeeperAdmin.html#sc_commonProblems)
:


> ## Things to Avoid
> 
> Here are some common problems you can avoid by configuring ZooKeeper correctly:
> 
> - *inconsistent lists of servers* : The list of ZooKeeper servers used by the clients must match the list of ZooKeeper servers that each ZooKeeper server has. Things work okay if the client list is a subset of the real list, but things will really act strange if clients have a list of ZooKeeper servers that are in different ZooKeeper clusters. Also, the server lists in each Zookeeper server configuration file should be consistent with one another.
> - *incorrect placement of transaction log* : The most performance critical part of ZooKeeper is the transaction log. ZooKeeper syncs transactions to media before it returns a response. A dedicated transaction log device is key to consistent good performance. Putting the log on a busy device will adversely affect performance. If you only have one storage device, increase the snapCount so that snapshot files are generated less often; it does not eliminate the problem, but it makes more resources available for the transaction log.
> - *incorrect Java heap size* : You should take special care to set your Java max heap size correctly. In particular, you should not create a situation in which ZooKeeper swaps to disk. The disk is death to ZooKeeper. Everything is ordered, so if processing one request swaps the disk, all other queued requests will probably do the same. the disk. DON’T SWAP. Be conservative in your estimates: if you have 4G of RAM, do not set the Java max heap size to 6G or even 4G. For example, it is more likely you would use a 3G heap for a 4G machine, as the operating system and the cache also need memory. The best and only recommend practice for estimating the heap size your system needs is to run load tests, and then make sure you are well below the usage limit that would cause the system to swap.
> - *Publicly accessible deployment* : A ZooKeeper ensemble is expected to operate in a trusted computing environment. It is thus recommended to deploy ZooKeeper behind a firewall.

# 7 \- Recovering from complete metadata loss in ZooKeeper

Recovering from complete metadata loss in ZooKeeper## Problem

Every ClickHouse® user experienced a loss of ZooKeeper one day. While the data is available and replicas respond to queries, inserts are no longer possible. ClickHouse uses ZooKeeper in order to store the reference version of the table structure and part of data, and when it is not available can not guarantee data consistency anymore. Replicated tables turn to the read\-only mode. In this article we describe step\-by\-step instructions of how to restore ZooKeeper metadata and bring ClickHouse cluster back to normal operation.

In order to restore ZooKeeper we have to solve two tasks. First, we need to restore table metadata in ZooKeeper. Currently, the only way to do it is to recreate the table with the `CREATE TABLE DDL` statement.


```
CREATE TABLE table_name ... ENGINE=ReplicatedMergeTree('zookeeper_path','replica_name');

```
The second and more difficult task is to populate zookeeper with information of ClickHouse data parts. As mentioned above, ClickHouse stores the reference data about all parts of replicated tables in ZooKeeper, so we have to traverse all partitions and re\-attach them to the recovered replicated table in order to fix that.

#### Info

Starting from ClickHouse version 21\.7 there is SYSTEM RESTORE REPLICA command[https://altinity.com/blog/a\-new\-way\-to\-restore\-clickhouse\-after\-zookeeper\-metadata\-is\-lost](https://altinity.com/blog/a-new-way-to-restore-clickhouse-after-zookeeper-metadata-is-lost)

## Test case

Let’s say we have replicated table `table_repl`.


```
CREATE TABLE table_repl 
(
   `number` UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/table_repl','{replica}')
PARTITION BY intDiv(number, 1000)
ORDER BY number;

```
And populate it with some data


```
SELECT * FROM system.zookeeper WHERE path='/clickhouse/cluster_1/tables/01/';

INSERT INTO table_repl SELECT * FROM numbers(1000,2000);

SELECT partition, sum(rows) AS rows, count() FROM system.parts WHERE table='table_repl' AND active GROUP BY partition;

```
Now let’s remove metadata in zookeeper using `ZkCli.sh` at ZooKeeper host:


```
deleteall  /clickhouse/cluster_1/tables/01/table_repl

```
And try to resync ClickHouse replica state with zookeeper:


```
SYSTEM RESTART REPLICA table_repl;

```
If we try to insert some data in the table, error happens:


```
INSERT INTO table_repl SELECT number AS number FROM numbers(1000,2000) WHERE number % 2 = 0;

```
And now we have an exception that we lost all metadata in zookeeper. It is time to recover!

## Current Solution

1. Detach replicated table.


```
DETACH TABLE table_repl;

```
2. Save the table’s attach script and change engine of replicated table to non\-replicated \*mergetree analogue. Table definition is located in the ‘metadata’ folder, ‘`/var/lib/clickhouse/metadata/default/table_repl.sql`’ in our example. Please make a backup copy and modify the file as follows:


```
ATTACH TABLE table_repl
(
   `number` UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/table_repl', '{replica}')
PARTITION BY intDiv(number, 1000)
ORDER BY number
SETTINGS index_granularity = 8192

```
Needs to be replaced with this:


```
ATTACH TABLE table_repl
(
   `number` UInt32
)
ENGINE = MergeTree()
PARTITION BY intDiv(number, 1000)
ORDER BY number
SETTINGS index_granularity = 8192

```
3. Attach non\-replicated table.


```
ATTACH TABLE table_repl;

```
4. Rename non\-replicated table.


```
RENAME TABLE table_repl TO table_repl_old;

```
5. Create a new replicated table. Take the saved attach script and replace ATTACH with CREATE, and run it.


```
CREATE TABLE table_repl
(
   `number` UInt32
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/table_repl', '{replica}')
PARTITION BY intDiv(number, 1000)
ORDER BY number
SETTINGS index_granularity = 8192

```
6. Attach parts from old table to new.


```
ALTER TABLE table_repl ATTACH PARTITION 1 FROM table_repl_old;

ALTER TABLE table_repl ATTACH PARTITION 2 FROM table_repl_old;

```

If the table has many partitions, it may require some shell script to make it easier.

### Automated approach

For a large number of tables, you can use script [https://github.com/Altinity/clickhouse\-zookeeper\-recovery](https://github.com/Altinity/clickhouse-zookeeper-recovery)
which partially automates the above approach.

# 8 \- Using clickhouse\-keeper

Moving to the ClickHouse® alternative to ZookeeperSince 2021 the development of built\-in ClickHouse® alternative for Zookeeper is happening, whose goal is to address several design pitfalls, and get rid of extra dependency.

See slides: <https://presentations.clickhouse.com/meetup54/keeper.pdf>
and video [https://youtu.be/IfgtdU1Mrm0?t\=2682](https://youtu.be/IfgtdU1Mrm0?t=2682)

## Current status (last updated: March 2026\)

ClickHouse Keeper is the recommended choice for new installations. It yields better performance in many cases due to the new features, like async replication or multi read. Some ClickHouse server features cannot be used without Keeper, for example the S3Queue.

- Use the latest Keeper version available in your supported upgrade path whenever possible.
- The Keeper version doesn’t need to match the ClickHouse server version
- Modern Keeper usually performs better than older versions because the codebase has matured significantly, new protocol feature flags have been added, and internal replication has improved.

For existing systems that currently use Apache Zookeeper, you can consider upgrading to clickhouse\-keeper especially if you will [upgrade ClickHouse](https://altinity.com/clickhouse-upgrade-overview/)
also.

#### Warning

Before upgrading ClickHouse Keeper from version older than 23\.9 please check Upgrade caveat for async\_replication [Upgrade caveat for async\_replication](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/clickhouse-keeper#upgrade-caveat-for-async_replication)## How does clickhouse\-keeper differ from Zookeeper?

Keeper is optimized for ClickHouse workloads and written in C\+\+ (and can be used as single\-binary), so it don’t need any external dependencies. It uses the same **client** protocol but both are implementing different consensus protocol: Zookeeper is using ZAB, while ClickHouse Keeper implements eBay NuRAFT [GitHub \- eBay/NuRaft: C\+\+ implementation of Raft core logic as a replication library](https://github.com/eBay/NuRaft)
which improves stability and performance of base RAFT protocol.

ClickHouse Keeper can also run in embedded mode, operating as a separate thread within the ClickHouse server process, which may be suitable for testing purposes or smaller instances where some performance can be sacrificed for simplicity

## Migration and upgrade guide

- A mixed ZooKeeper / ClickHouse Keeper quorum is not supported. Those are different consensus protocols.
- ZooKeeper snapshots and transaction logs are not format\-compatible with Keeper. For data migration use `clickhouse-keeper-converter`.
- If the above is too complex you can switch to new, empty Keeper ensemble and recreate the Keeper metadata using `SYSTEM RESTORE REPLICA` calls. This method takes longer time but it is suitable for smaller clusters. Check [procedure to restore multiple tables in RO mode article](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-check-replication-ddl-queue/#procedure-to-restore-multiple-tables-in-read-only-mode-per-replica)
- Keep in mind that some metadata is available in ZooKeeper only and will be lost if you don’t migrate with clickhouse\-keeper\-converter using above guide. For example: Distributed DDL queue, RBAC data (if configured), etc. Check [Keeper depended features](https://kb.altinity.com/altinity-kb-setup-and-maintenance/keeper-dependent-features)
for more information.

### Upgrade caveat for `async_replication`

`async_replication` is an internal Keeper optimization for RAFT replication and it’s turned on by default starting from [25\.10](https://github.com/ClickHouse/ClickHouse/pull/88515)
. It does not change ClickHouse replicated table semantics, but it can improve Keeper performance.

If you upgrade directly from a version older than `23.9` to `25.10+`:

- either upgrade Keeper to `23.9+` first, and then continue to `25.10+`
- or temporarily set `keeper_server.coordination_settings.async_replication=0` during the upgrade and enable it after the upgrade is finished

### Keeper in kubernetes

If you run ClickHouse on Kubernetes with Altinity operator, Keeper can be managed as a dedicated `ClickHouseKeeperInstallation` resource (often abbreviated as CHK). That is usually the cleanest way to run and upgrade a separate Keeper ensemble on Kubernetes. Please check examples [here](https://github.com/Altinity/clickhouse-operator/blob/master/docs/chk-examples/01-chi-simple-with-keeper.yaml)
.

## systemd service file

See [https://kb.altinity.com/altinity\-kb\-setup\-and\-maintenance/altinity\-kb\-zookeeper/clickhouse\-keeper\-service/](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/clickhouse-keeper-service/)

## init.d script

See [https://kb.altinity.com/altinity\-kb\-setup\-and\-maintenance/altinity\-kb\-zookeeper/clickhouse\-keeper\-initd/](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/clickhouse-keeper-initd/)

## More than 3 Keeper nodes

The main issue with a larger Keeper ensemble is that it takes more time to re\-elect a leader, and commits take longer, which can slow down insertions and DDL queries.

It should be fine, but we don’t recommend running more than three Keeper nodes (excluding observers).

Increasing the number of nodes offers no significant advantages (unless you need to tolerate the simultaneous failure of two Keeper nodes). In terms of performance, it doesn’t perform better—and may even perform worse—and it consumes additional resources (ZooKeeper requires fast, dedicated disks to perform well, as well as some RAM and CPU).

## clickhouse\-keeper\-client

In clickhouse\-keeper\-client, paths are now parsed more strictly and must be passed as string literals. In practice, this means using single quotes around paths—for example, `ls '/'` instead of `ls /`, and `get '/clickhouse/path'` instead of `get /clickhouse/path`.

## Embedded Keeper

To use the embedded ClickHouse Keeper, add the `<keeper_server>` section to the ClickHouse server configuration. In this setup, a separate client\-side `<keeper>` section is not required. If your ClickHouse servers use an external ClickHouse Keeper or ZooKeeper ensemble instead, see the section below.

## Example of a simple cluster

The Keeper ensemble size must be odd because it requires a majority (50% \+ 1 nodes) to form a quorum. A 2\-node Keeper setup will lose quorum after a single node failure, so the recommended number of Keeper replicas is 3\.

### hostname1


```
$ cat /etc/clickhouse-server/config.d/keeper.xml

<?xml version="1.0" ?>
<clickhouse>
    <keeper_server>
        <tcp_port>2181</tcp_port>
        <server_id>1</server_id>
        <log_storage_path>/var/lib/clickhouse/coordination/log</log_storage_path>
        <snapshot_storage_path>/var/lib/clickhouse/coordination/snapshots</snapshot_storage_path>

        <coordination_settings>
            <operation_timeout_ms>10000</operation_timeout_ms>
            <session_timeout_ms>30000</session_timeout_ms>
            <raft_logs_level>trace</raft_logs_level>
            <rotate_log_storage_interval>10000</rotate_log_storage_interval>
        </coordination_settings>

        <raft_configuration>
            <server>
                <id>1</id>
                <hostname>hostname1</hostname>
                <port>9444</port>
            </server>
            <server>
                <id>2</id>
                <hostname>hostname2</hostname>
                <port>9444</port>
            </server>
            <server>
                <id>3</id>
                <hostname>hostname3</hostname>
                <port>9444</port>
            </server>
        </raft_configuration>
    </keeper_server>

    <distributed_ddl>
        <path>/clickhouse/testcluster/task_queue/ddl</path>
    </distributed_ddl>
</clickhouse>

$ cat /etc/clickhouse-server/config.d/macros.xml

<?xml version="1.0" ?>
<clickhouse>
    <macros>
        <cluster>testcluster</cluster>
        <replica>replica1</replica>
        <shard>1</shard>
    </macros>
</clickhouse>

```
### hostname2


```
$ cat /etc/clickhouse-server/config.d/keeper.xml

<?xml version="1.0" ?>
<clickhouse>
    <keeper_server>
        <tcp_port>2181</tcp_port>
        <server_id>2</server_id>
        <log_storage_path>/var/lib/clickhouse/coordination/log</log_storage_path>
        <snapshot_storage_path>/var/lib/clickhouse/coordination/snapshots</snapshot_storage_path>

        <coordination_settings>
            <operation_timeout_ms>10000</operation_timeout_ms>
            <session_timeout_ms>30000</session_timeout_ms>
            <raft_logs_level>trace</raft_logs_level>
            <rotate_log_storage_interval>10000</rotate_log_storage_interval>
        </coordination_settings>

        <raft_configuration>
            <server>
                <id>1</id>
                <hostname>hostname1</hostname>
                <port>9444</port>
            </server>
            <server>
                <id>2</id>
                <hostname>hostname2</hostname>
                <port>9444</port>
            </server>
            <server>
                <id>3</id>
                <hostname>hostname3</hostname>
                <port>9444</port>
            </server>
        </raft_configuration>
    </keeper_server>

    <distributed_ddl>
        <path>/clickhouse/testcluster/task_queue/ddl</path>
    </distributed_ddl>
</clickhouse>

$ cat /etc/clickhouse-server/config.d/macros.xml

<?xml version="1.0" ?>
<clickhouse>
    <macros>
        <cluster>testcluster</cluster>
        <replica>replica2</replica>
        <shard>1</shard>
    </macros>
</clickhouse>

```
### hostname3


```
$ cat /etc/clickhouse-keeper/keeper_config.xml

<?xml version="1.0" ?>
<clickhouse>
    <keeper_server>
        <tcp_port>2181</tcp_port>
        <server_id>3</server_id>
        <log_storage_path>/var/lib/clickhouse/coordination/log</log_storage_path>
        <snapshot_storage_path>/var/lib/clickhouse/coordination/snapshots</snapshot_storage_path>

        <coordination_settings>
            <operation_timeout_ms>10000</operation_timeout_ms>
            <session_timeout_ms>30000</session_timeout_ms>
            <raft_logs_level>trace</raft_logs_level>
            <rotate_log_storage_interval>10000</rotate_log_storage_interval>
        </coordination_settings>

        <raft_configuration>
            <server>
                <id>1</id>
                <hostname>hostname1</hostname>
                <port>9444</port>
            </server>
            <server>
                <id>2</id>
                <hostname>hostname2</hostname>
                <port>9444</port>
            </server>
            <server>
                <id>3</id>
                <hostname>hostname3</hostname>
                <port>9444</port>
            </server>
        </raft_configuration>
    </keeper_server>
</clickhouse>

$ clickhouse-keeper --config /etc/clickhouse-keeper/keeper_config.xml

```
### on both ClickHouse nodes


```
$ cat /etc/clickhouse-server/config.d/clusters.xml

<?xml version="1.0" ?>
<clickhouse>
    <remote_servers>
        <testcluster>
            <shard>
                <replica>
                    <host>hostname1</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>hostname2</host>
                    <port>9000</port>
                </replica>
            </shard>
        </testcluster>
    </remote_servers>
</clickhouse>

```
Then create a table


```
create table test on cluster '{cluster}'   ( A Int64, S String)
Engine = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{database}/{table}','{replica}')
Order by A;

insert into test select number, '' from numbers(100000000);

-- on both nodes:
select count() from test;

```
## Useful references

- Official Keeper guide:
[https://clickhouse.com/docs/en/guides/sre/keeper/clickhouse\-keeper/](https://clickhouse.com/docs/en/guides/sre/keeper/clickhouse-keeper/)
- `clickhouse-keeper-client`:
[https://clickhouse.com/docs/en/operations/utilities/clickhouse\-keeper\-client](https://clickhouse.com/docs/en/operations/utilities/clickhouse-keeper-client)
- Keeper HTTP API and dashboard (`26.1+`):
[https://clickhouse.com/docs/operations/utilities/clickhouse\-keeper\-http\-api](https://clickhouse.com/docs/operations/utilities/clickhouse-keeper-http-api)
- `system.zookeeper`:
[https://clickhouse.com/docs/operations/system\-tables/zookeeper](https://clickhouse.com/docs/operations/system-tables/zookeeper)
- `system.zookeeper_connection`:
[https://clickhouse.com/docs/operations/system\-tables/zookeeper\_connection](https://clickhouse.com/docs/operations/system-tables/zookeeper_connection)
- `system.zookeeper_connection_log`:
[https://clickhouse.com/docs/operations/system\-tables/zookeeper\_connection\_log](https://clickhouse.com/docs/operations/system-tables/zookeeper_connection_log)
- `system.zookeeper_info` (`26.1+`):
[https://clickhouse.com/docs/operations/system\-tables/zookeeper\_info](https://clickhouse.com/docs/operations/system-tables/zookeeper_info)
- `system.zookeeper_log`:
[https://clickhouse.com/docs/operations/system\-tables/zookeeper\_log](https://clickhouse.com/docs/operations/system-tables/zookeeper_log)
- `aggregated_zookeeper_log` upstream PR:
resubmit <https://github.com/ClickHouse/ClickHouse/pull/87208>
- Altinity operator CHK examples:
[https://github.com/Altinity/clickhouse\-operator/tree/master/docs/chk\-examples](https://github.com/Altinity/clickhouse-operator/tree/master/docs/chk-examples)
- Altinity operator Keeper dashboard JSON:
[https://github.com/Altinity/clickhouse\-operator/blob/master/grafana\-dashboard/ClickHouseKeeper\_dashboard.json](https://github.com/Altinity/clickhouse-operator/blob/master/grafana-dashboard/ClickHouseKeeper_dashboard.json)
- Altinity operator Keeper alert rules:
[https://github.com/Altinity/clickhouse\-operator/blob/master/deploy/prometheus/prometheus\-alert\-rules\-chkeeper.yaml](https://github.com/Altinity/clickhouse-operator/blob/master/deploy/prometheus/prometheus-alert-rules-chkeeper.yaml)
# 9 \- ZooKeeper backup

ZooKeeper backupQuestion: Do I need to backup Zookeeper Database, because it’s pretty important for ClickHouse®?

TLDR answer: **NO, just backup ClickHouse data itself, and do SYSTEM RESTORE REPLICA during recovery to recreate zookeeper data**

Details:

Zookeeper does not store any data, it stores the STATE of the distributed system (“that replica have those parts”, “still need 2 merges to do”, “alter is being applied” etc). That state always changes, and you can not capture / backup / and recover that state in a safe manner. So even backup from few seconds ago is representing some ‘old state from the past’ which is INCONSISTENT with actual state of the data.

In other words \- if ClickHouse is working \- then the state of distributed system always changes, and it’s almost impossible to collect the current state of zookeeper (while you collecting it it will change many times). The only exception is ‘stop\-the\-world’ scenario \- i.e. shutdown all ClickHouse nodes, with all other zookeeper clients, then shutdown all the zookeeper, and only then take the backups, in that scenario and backups of zookeeper \& ClickHouse will be consistent. In that case restoring the backup is as simple (and is equal to) as starting all the nodes which was stopped before. But usually that scenario is very non\-practical because it requires huge downtime.

So what to do instead? It’s enough if you will backup ClickHouse data itself, and to recover the state of zookeeper you can just run the command `SYSTEM RESTORE REPLICA` command **AFTER** restoring the ClickHouse data itself. That will recreate the state of the replica in the zookeeper as it exists on the filesystem after backup recovery.

Normally Zookeeper ensemble consists of 3 nodes, which is enough to survive hardware failures.

On older version (which don’t have `SYSTEM RESTORE REPLICA` command \- it can be done manually, using instruction [https://clickhouse.com/docs/en/engines/table\-engines/mergetree\-family/replication/\#converting\-from\-mergetree\-to\-replicatedmergetree)](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replication/#converting-from-mergetree-to-replicatedmergetree%29)
, on scale you can try [https://github.com/Altinity/clickhouse\-zookeeper\-recovery](https://github.com/Altinity/clickhouse-zookeeper-recovery)

# 10 \- ZooKeeper cluster migration

ZooKeeper cluster migrationHere is a plan for ZK 3\.4\.9 (no dynamic reconfiguration):

1. Add the 3 new ZK nodes to the old cluster. No changes needed for the 3 old ZK nodes at this time.
	1. Configure one of the new ZK nodes as a cluster of 4 nodes (3 old \+ 1 new), start it.
	2. Configure the other two new ZK nodes as a cluster of 6 nodes (3 old \+ 3 new), start them.
2. Make sure the 3 new ZK nodes connected to the old ZK cluster as followers (run `echo stat | nc localhost 2181` on the 3 new ZK nodes)
3. Confirm that the leader has 5 synced followers (run `echo mntr | nc localhost 2181` on the leader, look for `zk_synced_followers`)
4. Stop data ingestion in CH (this is to minimize errors when CH loses ZK).
5. Change the zookeeper section in the configs on the CH nodes (remove the 3 old ZK servers, add the 3 new ZK servers)
6. Make sure that there are no connections from CH to the 3 old ZK nodes (run `echo stat | nc localhost 2181` on the 3 old nodes, check their `Clients` section). Restart all CH nodes if necessary (In some cases CH can reconnect to different ZK servers without a restart).
7. Remove the 3 old ZK nodes from `zoo.cfg` on the 3 new ZK nodes.
8. Restart the 3 new ZK nodes. They should form a cluster of 3 nodes.
9. When CH reconnects to ZK, start data loading.
10. Turn off the 3 old ZK nodes.

This plan works, but it is not the only way to do this, it can be changed if needed.

# 11 \- ZooKeeper cluster migration when using K8s node local storage

ZooKeeper cluster migration when using K8s node local storageDescribes how to migrate a ZooKeeper cluster when using K8s node\-local storage such as static PV, `local-path`, `TopoLVM`.

Requires HA setup (3\+ pods).

This solution is more risky than [migration by adding followers](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/altinity-kb-zookeeper-cluster-migration/)
because it reduces
the number of active consensus members but is operationally simpler. When running with `clickhouse-keeper`, it can be
performed gracefully so that quorum is maintained during the whole operation.

1. Find the leader pod and note its name
	1. To detect leader run `echo stat | nc 127.0.0.1 2181 | grep leader` inside pods
2. Make sure the ZK cluster is healthy and all nodes are in sync
	1. (run on leader) `echo mntr | nc 127.0.0.1 2181 | grep zk_synced_followers` should be N\-1 for N member cluster
3. Pick the first **non\-leader** pod and delete its `PVC`,
	1. `kubectl delete --wait=false pvc clickhouse-keeper-data-0` \-\> status should be `Terminating`
	2. Also delete `PV` if your `StorageClass` reclaim policy is set to `Retain`
4. If you are using dynamic volume provisioning make adjustments based on your k8s infrastructure (such as moving labels and taints or cordoning node) so that after pod delete the new one will be scheduled on the planned node
	1. `kubectl label node planned-node dedicated=zookeeper`
	2. `kubectl label node this-pod-node dedicated-`
	3. `kubectl taint node planned-node dedicated=zookeeper:NoSchedule`
	4. `kubectl taint node this-pod-node dedicated=zookeeper:NoSchedule-`
5. For manual volume provisioning wait till a new `PVC` is created and then provision volume on the planned node
6. Delete the first non\-leader pod and wait for its PV to be deleted
	1. `kubectl delete pod clickhouse-keeper-0`
	2. `kubectl wait --for=delete pv/pvc-0a823311-616f-4b7e-9b96-0c059c62ab3b --timeout=120s`
7. Wait for the new pod to be scheduled and volume provisioned (or provision manual volume per instructions above)
8. Ensure new member joined and synced
	1. (run on leader) `echo mntr | nc 127.0.0.1 2181 | grep zk_synced_followers` should be N\-1 for N member cluster
9. Repeat for all other non\-leader pods
10. (ClickHouse® Keeper only), for Zookeeper you will need to force an election by stopping the leader
	1. Ask the current leader to yield leadership
	2. `echo ydld | nc 127.0.0.1 2181` \-\> should print something like `Sent yield leadership request to ...`
	3. - Make sure a different leader was elected by finding your new leader
11. Finally repeat for the leader pod
# 12 \- ZooKeeper Monitoring

ZooKeeper Monitoring## ZooKeeper

### scrape metrics

- embedded exporter since version 3\.6\.0
	- [https://zookeeper.apache.org/doc/r3\.6\.2/zookeeperMonitor.html](https://zookeeper.apache.org/doc/r3.6.2/zookeeperMonitor.html)
- standalone exporter
	- [https://github.com/dabealu/zookeeper\-exporter](https://github.com/dabealu/zookeeper-exporter)

### Install dashboards

- embedded exporter <https://grafana.com/grafana/dashboards/10465>
- dabealu exporter <https://grafana.com/grafana/dashboards/11442>

See also [https://grafana.com/grafana/dashboards?search\=ZooKeeper\&amp;dataSource\=prometheus](https://grafana.com/grafana/dashboards?search=ZooKeeper&dataSource=prometheus)

### setup alert rules

- embedded exporter [link](https://github.com/Altinity/clickhouse-operator/blob/master/deploy/prometheus/prometheus-alert-rules-zookeeper.yaml)

### See also

- [https://www.datadoghq.com/blog/monitoring\-kafka\-performance\-metrics/\#zookeeper\-metrics](https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/#zookeeper-metrics)
- [https://dzone.com/articles/monitoring\-apache\-zookeeper\-servers](https://dzone.com/articles/monitoring-apache-zookeeper-servers)
\- note exhibitor is no longer maintained
- [https://github.com/samber/awesome\-prometheus\-alerts/blob/c3ba0cf1997c7e952369a090aeb10343cdca4878/\_data/rules.yml\#L1146\-L1170](https://github.com/samber/awesome-prometheus-alerts/blob/c3ba0cf1997c7e952369a090aeb10343cdca4878/_data/rules.yml#L1146-L1170)
(or [https://awesome\-prometheus\-alerts.grep.to/rules.html\#zookeeper](https://awesome-prometheus-alerts.grep.to/rules.html#zookeeper)
)
- [https://alex.dzyoba.com/blog/prometheus\-alerts/](https://alex.dzyoba.com/blog/prometheus-alerts/)
- [https://docs.datadoghq.com/integrations/zk/?tab\=host](https://docs.datadoghq.com/integrations/zk/?tab=host)
- [https://statuslist.app/uptime\-monitoring/zookeeper/](https://statuslist.app/uptime-monitoring/zookeeper/)
# 13 \- ZooKeeper schema

ZooKeeper schema## /metadata

Table schema.


```
date column -> legacy MergeTree partition expression.
sampling expression -> SAMPLE BY
index granularity -> index_granularity
mode -> type of MergeTree table
sign column -> sign - CollapsingMergeTree / VersionedCollapsingMergeTree
primary key -> ORDER BY key if PRIMARY KEY not defined.
sorting key -> ORDER BY key if PRIMARY KEY defined.
data format version -> 1
partition key -> PARTITION BY
granularity bytes -> index_granularity_bytes

types of MergeTree tables:
Ordinary            = 0
Collapsing          = 1
Summing             = 2
Aggregating         = 3
Replacing           = 5
Graphite            = 6
VersionedCollapsing = 7

```
## /mutations

Log of latest mutations

## /columns

List of columns for latest (reference) table version. Replicas would try to reach this state.

## /log

Log of latest actions with table.

Related settings:


```
┌─name────────────────────────┬─value─┬─changed─┬─description────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬─type───┐
│ max_replicated_logs_to_keep │ 1000  │       0 │ How many records may be in log, if there is inactive replica. Inactive replica becomes lost when when this number exceed.                                                  │ UInt64 │
│ min_replicated_logs_to_keep │ 10    │       0 │ Keep about this number of last records in ZooKeeper log, even if they are obsolete. It doesn't affect work of tables: used only to diagnose ZooKeeper log before cleaning. │ UInt64 │
└─────────────────────────────┴───────┴─────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┘

```
## /replicas

List of table replicas.

## /replicas/replica\_name/

### /replicas/replica\_name/mutation\_pointer

Pointer to the latest mutation executed by replica

### /replicas/replica\_name/log\_pointer

Pointer to the latest task from replication\_queue executed by replica

### /replicas/replica\_name/max\_processed\_insert\_time

### /replica/replica\_name/metadata

Table schema of specific replica

### /replica/replica\_name/columns

Columns list of specific replica.

## /quorum

Used for quorum inserts.

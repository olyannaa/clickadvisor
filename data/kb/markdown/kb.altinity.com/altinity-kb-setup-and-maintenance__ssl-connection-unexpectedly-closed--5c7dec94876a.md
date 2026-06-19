# SSL connection unexpectedly closed \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. SSL connection unexpectedly closed
# SSL connection unexpectedly closed

ClickHouse doesn’t probe CA path which is default on CentOS and Amazon Linux.

## ClickHouse client


```
cat /etc/clickhouse-client/conf.d/openssl-ca.xml
<config>
    <openSSL>
        <client> <!-- Used for connection to server's secure tcp port -->
            <caConfig>/etc/ssl/certs</caConfig>
        </client>
    </openSSL>
</config>

```
## ClickHouse server


```
cat /etc/clickhouse-server/conf.d/openssl-ca.xml
<config>
    <openSSL>
        <server>  <!-- Used for https server AND secure tcp port -->
            <caConfig>/etc/ssl/certs</caConfig>
        </server>
        <client>  <!-- Used for connecting to https dictionary source and secured Zookeeper communication -->
            <caConfig>/etc/ssl/certs</caConfig>
        </client>
    </openSSL>
</config>

```
<https://github.com/ClickHouse/ClickHouse/issues/17803>

<https://github.com/ClickHouse/ClickHouse/issues/18869>

Last modified 2021\.08\.24: [Format corrections and spell checks. (c865e00\)](https://github.com/Altinity/altinityknowledgebase/commit/c865e00c9976c80fb48234e9f1d09992e654a557)

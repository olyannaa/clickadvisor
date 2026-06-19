---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/operations/settings/composable-protocols.md)#
topic: composable-protocols-clickhouse-docs
ch_version_introduced: '127.0'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 3
---

### Specifying additional layer parameters[​](#some-modules-can-contain-specific-for-its-layer-parameters "Direct link to Specifying additional layer parameters") Some modules can contain additional layer parameters. For example, the TLS layer allows a private key (`privateKeyFile`) and certificate files (`certificateFile`) to be specified as follows:

```
<protocols>

  <plain_http>
    <type>http</type>
    <host>127.0.0.1</host>
    <port>8123</port>
  </plain_http>

  <https>
    <type>tls</type>
    <impl>plain_http</impl>
    <host>127.0.0.1</host>
    <port>8443</port>
    <privateKeyFile>another_server.key</privateKeyFile>
    <certificateFile>another_server.crt</certificateFile>
  </https>

</protocols>

```
[PreviousFormat Settings](/docs/operations/settings/formats)[NextConstraints on settings](/docs/operations/settings/constraints-on-settings)- [Overview](#overview)- [Configuring composable protocols](#composable-protocols-section-is-denoted-as-protocols-in-configuration-xml)
	- [Configuring protocol layers](#basic-modules-define-protocol-layers)- [Configuring endpoints](#endpoint-ie-listening-port-is-denoted-by-port-and-optional-host-tags)- [Configuring layer sequences](#layers-sequence-is-defined-by-impl-tag-referencing-another-module)- [Attaching endpoints to layers](#endpoint-can-be-attached-to-any-layer)- [Defining additional endpoints](#additional-endpoints-can-be-defined-by-referencing-any-module-and-omitting-type-tag)- [Custom HTTP handlers per endpoint](#custom-http-handlers-per-endpoint)- [Specifying additional layer parameters](#some-modules-can-contain-specific-for-its-layer-parameters)
Was this page helpful?

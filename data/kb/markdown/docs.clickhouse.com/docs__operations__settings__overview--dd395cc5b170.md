# Settings Overview \| ClickHouse Docs


- - [Settings](/docs/operations/settings)- Settings Overview
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/operations/settings/overview.md)# Settings Overview

## Overview[​](#overview "Direct link to Overview")


NoteXML\-based Settings Profiles and [configuration files](/docs/operations/configuration-files) are currently not
supported for ClickHouse Cloud. To specify settings for your ClickHouse Cloud
service, you must use [SQL\-driven Settings Profiles](/docs/operations/access-rights#settings-profiles-management).


There are following main groups of ClickHouse settings:


- Global server settings
- Session settings
- Query settings
- Background operations settings


Global settings apply by default unless overridden at further levels. Session settings can be specified via profiles, user configuration and SET commands. Query settings can be provided via SETTINGS clause and are applied to individual queries. Background operations settings are applied to Mutations, Merges and potentially other operations, executed asynchronously in the background.


## Viewing non\-default settings[​](#see-non-default-settings "Direct link to Viewing non-default settings")


To view which settings have been changed from their default value you can query the
`system.settings` table:



```
SELECT name, value FROM system.settings WHERE changed

```

If no settings have been changed from their default value, then ClickHouse will
return nothing.


To check the value of a particular setting, you can specify the `name` of the
setting in your query:



```
SELECT name, value FROM system.settings WHERE name = 'max_threads'

```

Which will return something like this:



```
┌─name────────┬─value─────┐
│ max_threads │ 'auto(8)' │
└─────────────┴───────────┘

1 row in set. Elapsed: 0.002 sec.

```

## Further reading[​](#further-reading "Direct link to Further reading")


- See [global server settings](/docs/operations/server-configuration-parameters/settings) to learn more about configuring your
ClickHouse server at the global server level.
- See [session settings](/docs/operations/settings/query-level) to learn more about configuring your ClickHouse
server at the session level.
- See [context hierarchy](/docs/development/architecture#context) to learn more about configuration processing by Clickhouse.
[PreviousSettings](/docs/operations/settings)[NextServer Settings](/docs/operations/server-configuration-parameters/settings)- [Overview](#overview)- [Viewing non\-default settings](#see-non-default-settings)- [Further reading](#further-reading)
Was this page helpful?

# Query\-level Session Settings \| ClickHouse Docs


- - [Settings](/docs/operations/settings)- Query\-level Session Settings
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/operations/settings/settings-query-level.md)# Query\-level Session Settings

## Overview[​](#overview "Direct link to Overview")


There are multiple ways to run statements with specific settings.
Settings are configured in layers, and each subsequent layer redefines the previous values of a setting.


## Order of priority[​](#order-of-priority "Direct link to Order of priority")


The order of priority for defining a setting is:


1. Applying a setting to a user directly, or within a settings profile


	- SQL (recommended)
	- adding one or more XML or YAML files to `/etc/clickhouse-server/users.d`
2. Session settings


	- Send `SET setting=value` from the ClickHouse Cloud SQL console or
	`clickhouse client` in interactive mode. Similarly, you can use ClickHouse
	sessions in the HTTP protocol. To do this, you need to specify the
	`session_id` HTTP parameter.
3. Query settings


	- When starting `clickhouse client` in non\-interactive mode, set the startup
	parameter `--setting=value`.
	- When using the HTTP API, pass CGI parameters (`URL?setting_1=value&setting_2=value...`).
	- Define settings in the
	[SETTINGS](/docs/sql-reference/statements/select#settings-in-select-query)
	clause of the SELECT query. The setting value is applied only to that query
	and is reset to the default or previous value after the query is executed.


## Converting a setting to its default value[​](#converting-a-setting-to-its-default-value "Direct link to Converting a setting to its default value")


If you change a setting and would like to revert it back to its default value, set the value to `DEFAULT`. The syntax looks like:



```
SET setting_name = DEFAULT

```

For example, the default value of `async_insert` is `0`. Suppose you change its value to `1`:



```
SET async_insert = 1;

SELECT value FROM system.settings where name='async_insert';

```

The response is:



```
┌─value──┐
│ 1      │
└────────┘

```

The following command sets its value back to 0:



```
SET async_insert = DEFAULT;

SELECT value FROM system.settings where name='async_insert';

```

The setting is now back to its default:



```
┌─value───┐
│ 0       │
└─────────┘

```

## Custom settings[​](#custom_settings "Direct link to Custom settings")


In addition to the common [settings](/docs/operations/settings/settings), users can define custom settings.
Custom settings enable you to pass **session\-specific parameters** that can be referenced within queries, policies, or functions. This is useful when you need to:


- Filter data based on user identity or organization
- Apply different business logic based on context
- Maintain stateful information across queries in a session


A custom setting name must begin with one of a number of predefined prefixes from a list you define.
The list of prefixes can be specified using the [`custom_settings_prefixes`](/docs/operations/server-configuration-parameters/settings#custom_settings_prefixes) server setting, defined in your server configuration file.


In the example below, `SQL_` is chosen as the custom prefix:



```
<custom_settings_prefixes>SQL_</custom_settings_prefixes>

```

NoteIn ClickHouse Cloud it is not possible to specify a custom prefix.
All custom user settings begin with prefix `SQL_`.


To define a custom setting use the `SET` command:



```
SET SQL_a = 123;

```

To get the current value of a custom setting use `getSetting()` function:



```
SELECT getSetting('SQL_a');

```

## Examples[​](#examples "Direct link to Examples")


These examples all set the value of the `async_insert` setting to `1`, and
show how to examine the settings in a running system.


### Using SQL to apply a setting to a user directly[​](#using-sql-to-apply-a-setting-to-a-user-directly "Direct link to Using SQL to apply a setting to a user directly")


This creates the user `ingester` with the setting `async_inset = 1`:



```
CREATE USER ingester
IDENTIFIED WITH sha256_hash BY '7e099f39b84ea79559b3e85ea046804e63725fd1f46b37f281276aae20f86dc3'
-- highlight-next-line
SETTINGS async_insert = 1

```

#### Examine the settings profile and assignment[​](#examine-the-settings-profile-and-assignment "Direct link to Examine the settings profile and assignment")



```
SHOW ACCESS

```


```
┌─ACCESS─────────────────────────────────────────────────────────────────────────────┐
│ ...                                                                                │
# highlight-next-line
│ CREATE USER ingester IDENTIFIED WITH sha256_password SETTINGS async_insert = true  │
│ ...                                                                                │
└────────────────────────────────────────────────────────────────────────────────────┘

```

### Using SQL to create a settings profile and assign to a user[​](#using-sql-to-create-a-settings-profile-and-assign-to-a-user "Direct link to Using SQL to create a settings profile and assign to a user")


This creates the profile `log_ingest` with the setting `async_inset = 1`:



```
CREATE
SETTINGS PROFILE log_ingest SETTINGS async_insert = 1

```

This creates the user `ingester` and assigns the user the settings profile `log_ingest`:



```
CREATE USER ingester
IDENTIFIED WITH sha256_hash BY '7e099f39b84ea79559b3e85ea046804e63725fd1f46b37f281276aae20f86dc3'
-- highlight-next-line
SETTINGS PROFILE log_ingest

```

### Using XML to create a settings profile and user[​](#using-xml-to-create-a-settings-profile-and-user "Direct link to Using XML to create a settings profile and user")



```
<clickhouse>
# highlight-start
    <profiles>
        <log_ingest>
            <async_insert>1</async_insert>
        </log_ingest>
    </profiles>
# highlight-end

    <users>
        <ingester>
            <password_sha256_hex>7e099f39b84ea79559b3e85ea046804e63725fd1f46b37f281276aae20f86dc3</password_sha256_hex>
# highlight-start
            <profile>log_ingest</profile>
# highlight-end
        </ingester>
        <default replace="true">
            <password_sha256_hex>7e099f39b84ea79559b3e85ea046804e63725fd1f46b37f281276aae20f86dc3</password_sha256_hex>
            <access_management>1</access_management>
            <named_collection_control>1</named_collection_control>
        </default>
    </users>
</clickhouse>

```

#### Examine the settings profile and assignment[​](#examine-the-settings-profile-and-assignment-1 "Direct link to Examine the settings profile and assignment")



```
SHOW ACCESS

```


```
┌─ACCESS─────────────────────────────────────────────────────────────────────────────┐
│ CREATE USER default IDENTIFIED WITH sha256_password                                │
# highlight-next-line
│ CREATE USER ingester IDENTIFIED WITH sha256_password SETTINGS PROFILE log_ingest   │
│ CREATE SETTINGS PROFILE default                                                    │
# highlight-next-line
│ CREATE SETTINGS PROFILE log_ingest SETTINGS async_insert = true                    │
│ CREATE SETTINGS PROFILE readonly SETTINGS readonly = 1                             │
│ ...                                                                                │
└────────────────────────────────────────────────────────────────────────────────────┘

```

### Assign a setting to a session[​](#assign-a-setting-to-a-session "Direct link to Assign a setting to a session")



```
SET async_insert =1;
SELECT value FROM system.settings where name='async_insert';

```


```
┌─value──┐
│ 1      │
└────────┘

```

### Assign a setting during a query[​](#assign-a-setting-during-a-query "Direct link to Assign a setting during a query")



```
INSERT INTO YourTable
-- highlight-next-line
SETTINGS async_insert=1
VALUES (...)

```

## See also[​](#see-also "Direct link to See also")


- View the [Settings](/docs/operations/settings/settings) page for a description of the ClickHouse settings.
- [Global server settings](/docs/operations/server-configuration-parameters/settings)
[PreviousServer overload](/docs/operations/settings/server-overload)[NextSettings profiles](/docs/operations/settings/settings-profiles)- [Overview](#overview)- [Order of priority](#order-of-priority)- [Converting a setting to its default value](#converting-a-setting-to-its-default-value)- [Custom settings](#custom_settings)- [Examples](#examples)
	- [Using SQL to apply a setting to a user directly](#using-sql-to-apply-a-setting-to-a-user-directly)- [Using SQL to create a settings profile and assign to a user](#using-sql-to-create-a-settings-profile-and-assign-to-a-user)- [Using XML to create a settings profile and user](#using-xml-to-create-a-settings-profile-and-user)- [Assign a setting to a session](#assign-a-setting-to-a-session)- [Assign a setting during a query](#assign-a-setting-during-a-query)- [See also](#see-also)
Was this page helpful?

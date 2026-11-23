---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"What's
topic: what-s-new-in-clickhousectl-v0-6-0-clickhouse
ch_version_introduced: '203.0'
last_updated: '2026-11-23'
chunk_index: 6
total_chunks_in_doc: 17
---

`list` show the count. **Deletion protection.** `postgres update --deletion-protection true` makes the API reject `delete` for that service until you turn it off. It applies to organisations with deletion protection enabled, and `get` and `list` show the setting.

```
1clickhousectl cloud postgres create --name app-db --region us-east-1 --size <size> \
2  --pg-version 19 --ha-type sync --standby-count 2
3clickhousectl cloud postgres private-endpoint create <postgres-id>
4clickhousectl cloud postgres private-endpoint update <postgres-id> \
5  --add-vpc-endpoint 'vpce-0123456789abcdef0=Production VPC'
6clickhousectl cloud postgres update <postgres-id> --deletion-protection true
```
Copy command
Smaller changes:

- `logs`, `metrics`, `slow-queries list`, `slow-queries get` and `backup list` take `--name <postgres-name>` in place of the service ID.
- `slow-queries list` shows each pattern's database, user, operation and app, which are the keys `slow-queries get` needs.
- `logs --severity` is checked against the supported levels before the request.
- `config patch` and `config replace` read the document from stdin with `--file -`.
- New GCP local\-SSD sizes are accepted by `--size`, and its help names a small size per provider.
- Help for `switchover` now describes what it does. It also works on a service without HA, by moving the primary onto a newly provisioned server.

See the [ClickHouse Managed Postgres guide](https://github.com/ClickHouse/clickhousectl/blob/main/docs/guides/managed-postgres.md).

## ClickHouse service configuration \#

**Deletion protection.** Turn it on with `clickhouse create --deletion-protection`, or change it later with `clickhouse update --deletion-protection true|false`. `clickhouse delete` refuses a protected service with the error code `deletion_protected`, and the error's `command` field holds the `update` command that turns protection off. With `--force`, the service is checked before it is stopped, so a protected service is never stopped either.

```
1clickhousectl cloud clickhouse create --name prod --deletion-protection
2clickhousectl cloud clickhouse update <service-id> --deletion-protection false
3clickhousectl cloud clickhouse delete <service-id>
```
Copy command
**JWT authentication providers (Beta).** `cloud clickhouse jwt-provider` lets users sign in to a service with a JWT from your identity provider, on the Enterprise tier. A token holder receives the ClickHouse roles listed in the token's roles claim. `update` replaces the whole configuration, so pass `--roles-claim` again to keep it.

```
1clickhousectl cloud clickhouse jwt-provider create <service-id> corp-sso \
2  --issuer https://auth.example.com --audience analytics \
3  --jwks-url https://auth.example.com/.well-known/jwks.json \
4  --roles-claim clickhouse:roles
```
Copy command
**Instance profiles.** Enterprise and BYOC organisations can change the instance profile with `clickhouse scale --profile`. `clickhouse profile list` shows the available profiles.

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"What's
topic: what-s-new-in-clickhousectl-v0-6-0-clickhouse
ch_version_introduced: '203.0'
last_updated: '2026-11-23'
chunk_index: 11
total_chunks_in_doc: 17
---

with no reliable completion signal, such as a Postgres switchover or an HA change, carry no `next`, and the [automation reference](https://github.com/ClickHouse/clickhousectl/blob/main/docs/reference/automation.md) says what to check for those. ### Exit codes and error codes you can branch on \#

- **A 403 is no longer an auth error.** Every Cloud API 403 used to exit 4 with `auth_required`, so a quota or policy refusal sent agents to log in again with a valid key. A 403 now exits 1 with `http_4xx` and the server's message. Exit 4 stays for a 401, missing credentials and rejected credential checks.
- **Invalid input always exits 2\.** Input that is checked after parsing but can never succeed, such as an unknown `--provider`, a malformed `--ip-allow` or a `--file` body with unknown fields, used to exit 1\. An empty resource ID, often an unset shell variable, is also a usage error, and nothing is sent.
- **`resource_not_found` means what it says.** It is reported consistently for missing resources selected by ID or `--name`, and its `command` field lists what does exist in that scope. A delete the API rejects for a service that still exists reports `http_4xx`.
- **Errors name the problem.** A `--file` that can't be read names the flag and path. A body with the wrong shape names the JSON path of the offending value, such as `policies[0].permissions[0]`. Help lists `--file` body fields, and enum errors list the accepted values.
- **One JSON error envelope.** `update` and `skills` failures, and `auth login`, `logout` and `signup`, now follow JSON mode. Local errors keep clickhousectl's own summary in `message` and put text from other programs (ClickHouse, Docker, the OS) in `details`.

### Smaller changes \#

- `CLICKHOUSECTL_AUTO_JSON=0` keeps human output under a detected coding agent. An explicit `--json` still wins.
- Resize, HA and CDC scaling updates say the change was accepted, not completed.
- Pagination cursors that start with `-` are accepted, and every list command a hint suggests is checked to parse.

## Verified installs and safer updates \#

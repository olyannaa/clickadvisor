---
source: blog
url: https://clickhouse.com/cli
topic: getting-started-with-clickhousectl-the-clickhouse-cli-for-local-and-cloud
ch_version_introduced: '26.2'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 6
---

scaffold the project - start a dev server - write out files like `clickhouse/tables/page_views.sql`, `sessions.sql`, and `conversions.sql` - seed data - run verification Follow up with: > Push this to ClickHouse Cloud. Create a service in AWS us\-east\-1\.

and it switches to `clickhousectl-cloud-deploy`: `cloud auth login`, `cloud service create`, then `cloud service client --queries-file` against the same SQL files it just wrote locally. The local project is the source of truth. Cloud is just another target.

## Use clickhousectl in CI/CD [\#](/blog/getting-started-clickhousectl#use-clickhousectl-in-cicd)

`chctl` is a static binary with JSON output and env\-var auth, so it drops into pipelines without a lot of wrapper scripting.

Here's a GitHub Actions workflow that spins up ClickHouse, applies your schema, and runs test queries on every push:

```
name: Schema validation
on: [push]

env:
  CLICKHOUSE_VERSION: "26.3"

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install clickhousectl
        run: curl https://clickhouse.com/cli | sh

      - name: Install ClickHouse
        run: chctl local install ${{ env.CLICKHOUSE_VERSION }}

      - name: Start server
        run: chctl local server start --name ci

      - name: Apply schema
        run: |
          for f in clickhouse/tables/*.sql; do
            chctl local client --name ci --queries-file "$f"
          done

      - name: Run test queries
        run: |
          for f in clickhouse/queries/test_*.sql; do
            chctl local client --name ci --queries-file "$f"
          done

      - name: Stop server
        run: chctl local server stop ci

```

Pin `CLICKHOUSE_VERSION` to match production. Upgrade it in one place and CI validates your whole schema against the new release on the next push, which is most of the confidence you need before an upgrade.

For Cloud writes from CI, set `CLICKHOUSE_API_KEY` and `CLICKHOUSE_API_SECRET` as secrets in your workflow and `chctl` picks them up automatically. Or pass them explicitly:

```
chctl cloud auth login --api-key $CLICKHOUSE_API_KEY --api-secret $CLICKHOUSE_API_SECRET

```

`--json` gives you machine\-readable output for anything scripted downstream:

```
chctl cloud service list --json | jq '.[0].id'

```

## What's next [\#](/blog/getting-started-clickhousectl#whats-next)

clickhousectl is open source at [github.com/ClickHouse/clickhousectl](https://github.com/ClickHouse/clickhousectl). For the design thinking behind it, see [Introducing clickhousectl](/blog/introducing-clickhousectl).

If you don't have a ClickHouse Cloud account yet, [sign up](https://clickhouse.cloud) and run the last two sections against a real service.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

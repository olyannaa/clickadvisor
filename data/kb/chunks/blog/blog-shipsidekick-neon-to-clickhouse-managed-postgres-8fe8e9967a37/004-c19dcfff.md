---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-shipsidekick-replaced-neon-with-clickhouse-managed-postgres-for-10x-faster-queries-and-better-reliability-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 4
total_chunks_in_doc: 8
---

committing your writes, they just stream the writes to the standby,” he explains. “Maybe you lose a second of writes if you have to fail over. I’m okay with that for a third cheaper and increased write performance.”

Another draw was the [documentation](https://clickhouse.com/docs/products/managed-postgres/overview). “The docs that ClickHouse has put together for Postgres are incredible,” Sawyer says. “This does not feel like a new product. Nothing in the docs was ever incorrect, out of date, or led us astray.”

And then there were the people. Researching the product, Sawyer found a Reddit thread where [Sai Srirampur](https://www.linkedin.com/in/sai-krishna-srirampur-1741b019), who leads ClickHouse Managed Postgres after the acquisition of his former company PeerDB, was answering questions in public. “Seeing the ClickHouse team talking openly with commenters,” Sawyer says, “that gave us a lot of confidence.”

## “The migration process was dead simple” \#

Sawyer created an account on July 16th. Sai personally emailed him the same day, and within a couple of hours they were in a shared Slack channel. That responsiveness is a welcome change. “I have no doubt that if we were down with ClickHouse, we would have a response within minutes, if not seconds,” Sawyer says.

He calls the migration process “dead simple.” The team followed ClickHouse’s [Neon Postgres source setup guide](https://clickhouse.com/docs/integrations/clickpipes/postgres/source/neon-postgres): enable logical replication on Neon, create a ClickPipe from the Data Sources panel in the ClickHouse console, and let it replicate. Shipsidekick had around 500 GB of data at the time. Sai estimated replication would take a day and a half. It ended up taking four or five hours.

At the Vancouver meetup, Sawyer flagged one hiccup for anyone following the same path. A cron job in the application ran multiple transactions that, replicated mid\-flight rather than in their end state, tripped a partial unique index on the invoices table. “The solution was very simple,” Sawyer says: drop the offending index, let replication finish, then re\-create it.

[ClickPipes](https://clickhouse.com/cloud/clickpipes), he notes, handled the interruption gracefully. “Even though there was an error in the replication, it didn’t lose anything,” he says. “It literally just waited until the error was resolved, and then everything continued as if nothing was wrong.”

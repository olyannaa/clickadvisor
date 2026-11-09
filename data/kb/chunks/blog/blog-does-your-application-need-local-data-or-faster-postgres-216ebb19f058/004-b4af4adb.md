---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Does
topic: does-your-application-need-local-data-or-faster-postgres-clickhouse
ch_version_introduced: auto
last_updated: '2026-11-09'
chunk_index: 4
total_chunks_in_doc: 8
---

from other clients touching the same rows. When its own write shows up in the stream, the provisional copy is dropped. If the write is rejected, the provisional copy has to be rolled back and the view corrected.

Postgres remains the authoritative source throughout, and it is still the place where [concurrent writes](https://www.postgresql.org/docs/current/transaction-iso.html) are ordered, through transactions. An application that reads committed state directly from Postgres gets that ordering for free. It never waits for a local copy to catch up and never holds two versions of the same row. A local copy gives fast reads in exchange for a reconciliation problem the application has to own. Pending local changes, committed data arriving asynchronously, and the view the user sees all have to agree.

## Agents make the working set harder to predict \#

A traditional application works with a bounded working set because people navigate it in predictable patterns. A product page loads product information, a billing page loads one specific account, and a search page queries a given set of fields. An AI agent behaves differently: it could load a product, identify the customers who bought it, and then look for similar products, all based on the prompts and context provided at runtime.

The paradigm is different now. With agents, a developer cannot always predict the application’s working set or accurately define its boundaries. Declared subsets remain possible, but the working\-set boundary must be broad enough to support the agent’s possible query paths. On\-demand and progressive loading can avoid synchronizing the entire subset upfront, but data that has not been materialized still requires a remote request before it becomes locally queryable.

This creates several trade\-offs:

- Synchronize broadly and transfer data the agent may never use.
- Load progressively and put synchronization back in the read path.
- Create task\-specific subsets and manage their lifecycle individually.

A sync layer’s fan\-out is most effective when many consumers reuse the same subset. When agents require different, changing subsets of data, there is less reuse across local copies and fewer opportunities to amortize synchronization work. The question becomes: if the dataset is a moving target, keeps growing, and continually requires new data to be synchronized locally, is this architecture still relevant?

## What if Postgres is already fast enough? \#

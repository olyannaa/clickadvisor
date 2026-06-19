# How we built fast UPDATEs for the ClickHouse column store – Part 2: SQL\-style UPDATEs


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How we built fast UPDATEs for the ClickHouse column store – Part 2: SQL\-style UPDATEs

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jul 24, 2025 · 28 minutes read
> **TL;DR**  
>   
> 
> We reimagined SQL\-style UPDATEs from the ground up for ClickHouse’s column store. In this post, we’ll walk through how we did it, from heavyweight mutations to lightweight updates powered by patch parts that scale. Benchmarks are in Part 3\.



**This post is part of our series on fast UPDATEs in ClickHouse:**

- **[Part 1: Purpose\-built engines](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines)**  

 Learn how ClickHouse sidesteps slow row\-level updates using insert\-based engines like ReplacingMergeTree, CollapsingMergeTree, and CoalescingMergeTree.
- **This part: Declarative SQL\-style UPDATEs**  

 Explore how we brought standard UPDATE syntax to ClickHouse with minimal overhead using patch parts.
- **[Part 3: Benchmarks](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks)**  

 See how fast it really is. We benchmarked every approach, including declarative UPDATEs, and got up to **1,000× speedups**.
- **[Bonus: ClickHouse vs PostgreSQL](https://clickhouse.com/blog/update-performance-clickhouse-vs-postgresql)**  

 We put ClickHouse’s new SQL UPDATEs head\-to\-head with PostgreSQL on identical hardware and data—parity on point updates, up to **4,000× faster** on bulk changes.


## The update they said you couldn’t have [\#](/blog/updates-in-clickhouse-2-sql-style-updates#the-update-they-said-you-couldnt-have)


**Column stores weren’t supposed to have fast updates.**


For years, systems built for analytics sacrificed update performance for read speed. Row\-level changes were considered incompatible with high\-throughput, scan\-optimized architectures.


ClickHouse was no exception, until we broke that rule by *rethinking what an update really is*.


In [Part 1](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines), we showed how ClickHouse embraced a radically different model: turning updates into inserts. With purpose\-built engines like ReplacingMergeTree and CollapsingMergeTree, we let merges resolve updates later, asynchronously, while maintaining blazing ingest speeds.


But not everyone wants to think in merge semantics. Many users just want to write:



```

```
1UPDATE orders
2SET discount = 0.2
3WHERE quantity >= 40;
```


```

So we set out to make that possible, without losing what makes ClickHouse fast.


**This post is about how we did it.**


We’ll walk through the evolution of SQL\-style updates in ClickHouse:


1. Classic **mutations**, simple but heavyweight.
2. A step forward: **on\-the\-fly updates** that avoided waiting for mutations to finish.
3. Finally closing the loop with fast, declarative SQL updates, powered by **patch parts**, a scalable, columnar\-native update mechanism purpose\-built for high\-frequency workloads.



> Curious how fast patch\-part updates really are?  
> In [Part 3](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks), we benchmarked them, and saw speedups of up to 1,000×, sometimes even 1,600× or more.


Let’s first look at the original mutation\-based UPDATEs that ClickHouse has supported for years.


## Stage 1: Classic mutations and column rewrites [\#](/blog/updates-in-clickhouse-2-sql-style-updates#stage-1-classic-mutations-and-column-rewrites)


Since 2018, ClickHouse has supported SQL\-style updates using [ALTER TABLE ... UPDATE](https://clickhouse.com/docs/sql-reference/statements/alter/update) statements.


We’ll use the same orders table from our [example in Part 1](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#replacingmergetree-replace-rows-by-inserting-new-ones) to illustrate how UPDATEs work via mutations:



```

```
1CREATE TABLE orders (
2    order_id   Int32,
3    item_id    String,
4    quantity   UInt32,
5    price      Decimal(10,2),
6    discount   Decimal(5,2)
7)
8ENGINE = MergeTree
9ORDER BY (order_id, item_id);
```


```

Let’s walk through how a simple UPDATE triggers a mutation behind the scenes, starting with an initial insert.


### Initial insert [\#](/blog/updates-in-clickhouse-2-sql-style-updates#initial-insert)


We start with a part containing two items from the same order:



```

```
1INSERT INTO orders VALUES
2    (1001, 'kbd',  10, 45.00, 0.00),
3    (1001, 'mouse', 6, 25.00, 0.00);
```


```

This creates a data part [named](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#how-to-read-a-part-name) `all_1_1_0`:


![Blog-updates Part 2.001.png](/uploads/Blog_updates_Part_2_001_8013fe2a98.png)
### UPDATE triggers a mutation [\#](/blog/updates-in-clickhouse-2-sql-style-updates#update-triggers-a-mutation)


We update the quantity and discount for the mouse item:



```

```
1ALTER TABLE orders
2UPDATE quantity = 60, discount = 0.20
3WHERE order_id = 1001 AND item_id = 'mouse';
```


```


> The `ALTER TABLE ... UPDATE` syntax differs intentionally from [standard SQL UPDATE](https://www.w3schools.com/sql/sql_update.asp) to reflect what’s happening under the hood: instead of modifying rows in place, ClickHouse rewrites (“mutates”) data parts.


**Because of the UPDATE, ClickHouse now runs a [mutation](https://clickhouse.com/docs/sql-reference/statements/alter#mutations) behind the scenes.** This triggers three internal steps:


1. **A new block number** is [allocated](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#how-blocks-make-up-a-part) for the update (e.g. `2`), which ClickHouse uses to track which parts need rewriting.
2. **A new mutated part** is created on disk, named `all_1_1_0_2`, where 2 is the **mutation version**.
3. The mutation is applied only to parts with a block number less than 2 like the original part `all_1_1_0`.


The diagram below shows what changes: the updated columns (`quantity`, `discount`) are **fully rewritten**, and the unchanged columns (`order_id`, `item_id`, `price`) are **[hard linked](https://en.wikipedia.org/wiki/Hard_link)**. No data is copied for those columns, the new part simply reuses the same underlying files via hard links on disk:


![Blog-updates Part 2.002.png](/uploads/Blog_updates_Part_2_002_e61e7d0c11.png)
Once the mutation completes, the mutated part `all_1_1_0_2` replaces the original `all_1_1_0`, and the original part is removed. Although this deletes the original [folder](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#whats-inside-a-part) and its file entries, any column files that the new part `all_1_1_0_2` hard links to remain safely on disk, because hard links ensure the data isn’t deleted until no part references it.


### Summary and tradeoffs [\#](/blog/updates-in-clickhouse-2-sql-style-updates#summary-and-tradeoffs)


The classic mutation model is reliable, but comes with tradeoffs:


- **Heavyweight updates**: Every UPDATE rewrites the affected columns, which can be costly at scale.
- **Delayed visibility**: Changes don’t appear in query results until the background mutation completes.
- **Merge dependency**: Mutations must wait for prior merges and mutations to finish before they run. *(We haven’t covered this behavior in detail here, but it’s a real and sometimes surprising constraint.)*



> By [default](https://clickhouse.com/docs/operations/settings/settings#mutations_sync), `ALTER TABLE … UPDATE` statements run asynchronously, allowing ClickHouse to fuse multiple updates into a single mutation. This helps amortize the rewrite cost.


Before we move on to on\-the\-fly mutations, let’s pause to look at one more stopgap optimization built on this model: **lightweight deletes**.


## Stage 1\.5: Lightweight DELETEs (still mutations, but faster) [\#](/blog/updates-in-clickhouse-2-sql-style-updates#stage-15-lightweight-deletes-still-mutations-but-faster)


Before on\-the\-fly mutations, ClickHouse introduced a simpler optimization to make DELETE faster under the classic mutation model.


Instead of removing rows immediately, DELETE is rewritten as an ALTER TABLE ... UPDATE that sets a special mask column `_row_exists = 0`. This triggers a **lightweight mutation** that (re)writes\* only the `_row_exists` column, **all other columns are hard\-linked**, avoiding unnecessary I/O.


\**If this is the **first delete mutation** on a part, the `_row_exists` column is **created** in the mutated part. If it’s a **subsequent delete mutation** (before the part has been merged), `_row_exists` is **rewritten**.*


The next diagram shows the original part and the mutated result of a [lightweight DELETE](https://clickhouse.com/docs/guides/developer/lightweight-delete). Below, we walk through each step in the process:


![Blog-updates Part 2.003.png](/uploads/Blog_updates_Part_2_003_96fff00c29.png)
*(For clarity, we show \_row\_exists in the original part, but as explained earlier, that column doesn’t exist yet and is added by the first delete mutation.)*
  
1\. **Initial insert**: We reuse the same small orders example from Stage 1: two rows inserted, creating the original part `all_1_1_0`:



```

```
1INSERT INTO orders VALUES
2    (1001, 'kbd',  10, 45.00, 0.00),
3    (1001, 'mouse', 6, 25.00, 0.00);
```


```

2. **DELETE issued**: The mouse item is deleted:



```

```
1DELETE FROM orders WHERE order_id = 1001 AND item_id = 'mouse';
```


```

Internally, ClickHouse updates `_row_exists = 0`:



```

```
1ALTER TABLE orders
2UPDATE _row_exists = 0
3WHERE order_id = 1001 AND item_id = 'mouse';
```


```

3. **Mutation created**: A new part `all_1_1_0_2` is created, rewriting only `_row_exists`.
4. **Query behavior**: Rows where `_row_exists = 0` are excluded from results.
5. **Cleanup**: The row is permanently dropped during the next regular background merge.


### Summary and tradeoffs [\#](/blog/updates-in-clickhouse-2-sql-style-updates#summary-and-tradeoffs-1)


This approach made DELETE significantly faster without changing the core mutation model, but it still required background rewrites.


The next stage didn’t eliminate background rewrites, but it made updates visible immediately, without waiting for the mutation to run.


## Stage 2: On\-the\-fly updates for instant visibility [\#](/blog/updates-in-clickhouse-2-sql-style-updates#stage-2-on-the-fly-updates-for-instant-visibility)


Classic mutations are heavyweight: they rewrite full data columns and take time to finish, especially on large datasets. To reduce the latency between issuing an UPDATE and seeing the result, ClickHouse introduced [on\-the\-fly mutations](https://clickhouse.com/docs/guides/developer/on-the-fly-mutations), an optimization that makes updates visible immediately, even before any part is rewritten.



> This was a natural first step on the path to patch parts. It didn’t avoid rewrites, but it made updates feel instant.


The diagram below illustrates the mechanism: the UPDATE is stored in memory and applied on read, while the actual mutation runs asynchronously in the background:


![Blog-updates Part 2.004.png](/uploads/Blog_updates_Part_2_004_e4bdb4f086.png)
1. **Insert**: As before, two rows are ① inserted into the orders table, ② creating the initial part `all_1_1_0`.
2. **UPDATE issued**: We ③ update the mouse row. ClickHouse stores the update expression in memory.
3. **SELECT issued**: The ④ query reads the original data part, but ClickHouse ⑤ applies the update on the fly in memory.
4. **Result**: The updated row is visible immediately in the ⑥ query result.
5. **Mutation runs**: In the background, ClickHouse ⑦ rewrites the part as `all_1_1_0_2` and drops the old one.


### Summary and tradeoffs [\#](/blog/updates-in-clickhouse-2-sql-style-updates#summary-and-tradeoffs-2)


On\-the\-fly mutations improve responsiveness, but they don’t eliminate background rewrites. They can also slow down SELECTs if many updates accumulate, and [support for subqueries and non\-determinism is limited](https://clickhouse.com/docs/guides/developer/on-the-fly-mutations#support-for-subqueries-and-non-deterministic-functions).


This was a practical stopgap, an easier, faster optimization that gave us breathing room to build something better. The real breakthrough was still ahead: **patch parts**, a fundamentally different mechanism designed to handle frequent updates efficiently at scale.


## Stage 3: Patch parts – updates the ClickHouse way [\#](/blog/updates-in-clickhouse-2-sql-style-updates#stage-3-patch-parts--updates-the-clickhouse-way)


Earlier approaches weren’t good enough, so we built something better.


### Why classic mutations weren’t enough [\#](/blog/updates-in-clickhouse-2-sql-style-updates#why-classic-mutations-werent-enough)


Even with optimizations like on\-the\-fly updates, the core model had limits:


- Rewrites of entire columns, even if just a few rows have changed, which is wasteful at scale.
- Blocking behind previous merges and mutations, adding latency and unpredictability.


That’s why we built a new mechanism from scratch — **patch parts** — named for what they do:
**they patch source parts during merges, applying only the changed data.**


### A model built on what works [\#](/blog/updates-in-clickhouse-2-sql-style-updates#a-model-built-on-what-works)


Patch parts borrow two proven ideas from our [specialized engines](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines), **fast inserts** and **background merges**, and generalize them, fully encapsulated for flexible, SQL\-style updates:


1. **Fast inserts**: ClickHouse handles inserts at [high throughput](/blog/updates-in-clickhouse-1-purpose-built-engines#inserts-are-so-fast-we-turned-updates-into-inserts) (e.g., in one production setup, over [ClickHouse ingests over 1 billion rows per second](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#proving-the-system-at-scale)). We use this to model updates and deletes as lightweight inserts.
2. **Background merges**: MergeTree is already scanning and rewriting data. Applying updates or deleting rows during this process adds [near\-zero overhead](/blog/updates-in-clickhouse-1-purpose-built-engines#merges-are-fast-thanks-to-sorted-parts).


Let’s walk through a simple example to understand how this works. (*We’ll start small to build intuition, then go through the internals in the next section.)*


## How patch parts work [\#](/blog/updates-in-clickhouse-2-sql-style-updates#how-patch-parts-work)


Let’s understand how patch parts behave and why they’re so efficient.


We’ll reuse the small orders table from earlier to walk through a simple update:



```

```
1CREATE TABLE orders (
2    order_id   Int32,
3    item_id    String,
4    quantity   UInt32,
5    price      Decimal(10,2),
6    discount   Decimal(5,2)
7)
8ENGINE = MergeTree
9ORDER BY (order_id, item_id);
```


```


> **UPDATEs powered by patch parts are still experimental in 25\.7**  
> To try this out in ClickHouse 25\.7, you’ll need to enable the feature manually:  
>   
> `SET allow_experimental_lightweight_update = 1;`  
>  `ALTER TABLE orders MODIFY SETTING enable_block_number_column = 1, enable_block_offset_column = 1;`  
>   
> *(It is expected to enter beta in 25\.8\)*


We’ll also reuse the same initial order from earlier: two items (kbd, mouse). These rows are inserted into a data part named `all_1_1_0` (shown in a diagram further below):



```

```
1INSERT INTO orders VALUES
2    (1001, 'kbd',  10, 45.00, 0.00),
3    (1001, 'mouse', 6, 25.00, 0.00);
```


```

Let’s say the mouse quantity is later increased to 60 units, qualifying for a 20% bulk discount. We update the row:



```

```
1UPDATE orders
2SET quantity = 60, discount = 0.20
3WHERE order_id = 1001 AND item_id = 'mouse';
```


```

This UPDATE triggers a **lightweight update**, powered by patch parts.



> [Patch part based updates use standard SQL UPDATE syntax](https://www.w3schools.com/sql/sql_update.asp). This new feature is called a [lightweight update](https://clickhouse.com/docs/sql-reference/statements/update) in ClickHouse. Unlike classic mutations, it behaves more like a row\-level update: small, frequent changes are efficient and performant.


At this point, the updated values are **already visible to queries**, no need to wait for any background work to complete. We’ll explain how that works [shortly](/blog/updates-in-clickhouse-2-sql-style-updates#how-patch-on-read-works).


### A patch part is a delta, not a replacement [\#](/blog/updates-in-clickhouse-2-sql-style-updates#a-patch-part-is-a-delta-not-a-replacement)


Unlike classic mutations, ClickHouse doesn’t rewrite the entire column or part. Instead, it creates a new, compact **patch part** that contains only:


- The **changed column values** (quantity \= 60, discount \= 0\.20\)
- **Metadata to locate the original row** inside the source part



> Think of a patch part as a “diff”: a small delta that says “update just this row, just these columns.” That’s why we call them **lightweight updates** in ClickHouse: they’re **compact and efficient**.


### Visual walkthrough: how patch parts update rows [\#](/blog/updates-in-clickhouse-2-sql-style-updates#visual-walkthrough-how-patch-parts-update-rows)


Let’s visualize what happens during the update from above:


*(We’ve simplified the real implementation slightly to focus on the core concept; we’ll walk through the full details in the next section.)*


![Blog-updates Part 2.005.png](/uploads/Blog_updates_Part_2_005_1842c7cbff.png)
**① Original data part**:   
Contains both the keyboard and mouse orders, explicitly sorted by the table’s sorting key `(order_id, item_id)`. Each row also has a *[virtual](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree#virtual-columns)* `_part_offset` system column that reflects its position inside the part, so the part is implicitly sorted by `_part_offset` as well.


**② Patch part**:   
Created by the UPDATE. It contains only the changed values (`quantity`, `discount`) for the second row of the source part `all_1_1_0`, plus metadata system columns: `_part` \= `all_1_1_0`, `_part_offset` \= `1`.


**③ Merged result**:   
During a background merge, ClickHouse merges the original and patch part together, replacing matching rows with updated values.


### They’re compact [\#](/blog/updates-in-clickhouse-2-sql-style-updates#theyre-compact)


Patch parts minimize what’s written, by design:


- Only the **updated values** are written.
- **Unchanged columns** (e.g. `order_id`, `item_id`, `price`) are skipped entirely; they don’t appear in the patch part at all.
*(With a specialized engine like ReplacingMergeTree, updates require re\-inserting the full row, including unchanged values.)*


### They’re efficient [\#](/blog/updates-in-clickhouse-2-sql-style-updates#theyre-efficient)


Patch parts **piggyback on [merges already happening in the background](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#merges-happen-in-the-background)**, they hook into the process ClickHouse already runs continuously, with almost zero overhead:


- **All parts are naturally aligned**: the original part is sorted by the table’s sorting key (and implicitly by `_part_offset`), and the patch is sorted by `(_part, _part_offset)`.
- **That means merges can align rows seamlessly** using `_part_offset`, without extra indexing, resorting, or rewrites.
- **Updates just fall into place**, applied in a single, efficient merge pass: the engine simply *interleaves the part’s data with a single linear scan of the parts*, with no temp buffers or random access


*(This mirrors the specialized engines, but patch parts rely on `_part_offset` instead of the sorting key.)*


We’ve intentionally simplified things slightly to focus on how patch parts work in principle, on a single update.


Now let’s unfold the full picture and see how they scale.


## Patch parts at scale: tracking, targeting, merging [\#](/blog/updates-in-clickhouse-2-sql-style-updates#patch-parts-at-scale-tracking-targeting-merging)


To understand how ClickHouse supports **scalable, production\-grade updates**, we’ll go through the internal system columns and metadata structures that power patch parts.



> Real\-world updates rely on these internals to efficiently target rows across parts and support **non\-blocking** updates at scale.


Let’s zoom in.


Suppose we want to apply a 20% discount to all items in all orders where quantity is 40 or more:



```

```
1UPDATE orders
2SET discount = 0.2
3WHERE quantity >= 40;
```


```

This kind of SQL statement can affect **many rows across many parts**. But you don’t need to worry about how. It just works.



> **Declarative updates matter**  
> Unlike [specialized engines](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines) like ReplacingMergeTree, where you’d need to insert a new row per updated row, declarative SQL updates handle the mechanics for you. Just express your intent.


To show how patch parts efficiently target rows across **multiple parts**, the diagram below uses an extended example with more inserts and the update above.



> **Note:** To keep things focused, we **dim** all system columns and structures *not used in this example*.  
>   
> •**Orange** highlights system columns that are used.  
> •**Blue** highlights indexes that are used.  
> •**Light gray** indicates unused structures.  
>   
> This lets us highlight the essentials while still giving you a full view of what exists under the hood.


![Blog-updates Part 2.006.png](/uploads/Blog_updates_Part_2_006_326f03e9ec.png)
**① Initial order**: Our base example with two items.


**② Another order**: A new `order_id`, inserted separately.


**③ Extended order**: Adds two more items to the initial order.


These are just regular inserts, resulting in **three data parts** created over time.


**④ Patch part**: Created by the UPDATE. Contains just the new column values (discount \= 0\.2 for two rows) and enough metadata to target the exact rows being changed


**⑤ Merged data part**: Combines the old rows and patch values into one output part


**Cleanup:** After the merge, the original parts ① to ③ (and eventually also ④) are dropped. Only ⑤, the merged result, remains.


Now let’s walk through the system columns and internal data structures sketched on the diagram above.


### System columns in original rows [\#](/blog/updates-in-clickhouse-2-sql-style-updates#system-columns-in-original-rows)


To enable patch part mechanics, every row in an original data part carries **three system columns**:




| System column(s) | Description and purpose |
| --- | --- |
| `_part_offset` | The row’s ordinal position within its part; used to align rows during merges and apply patch updates efficiently. |
| `_block_number`, `_block_offset` | The insert\-time [block number](/blog/updates-in-clickhouse-1-purpose-built-engines#how-blocks-make-up-a-part) and row’s offset within that block; used to locate the row after merges when `_part_offset` is no longer valid. (*not used in this example*) |


*(These system columns are [virtual](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree#virtual-columns) by default. Like in the earlier simplified example, we show them materialized here for clarity; in reality, they’re only stored physically after a merge.)*


### Precise targeting metadata in patch parts [\#](/blog/updates-in-clickhouse-2-sql-style-updates#precise-targeting-metadata-in-patch-parts)


Each patch part row includes **just enough metadata** to find the row it updates:




| System column(s) | Purpose |
| --- | --- |
| `_part`, `_part_offset` | Identify the original row |
| `_block_number`, `_block_offset` | Support tracking through merges (*not used here*) |
| `_data_version` | Track the update version: used to skip already\-applied patches and merge patch parts with other patch parts (*explained later*) |


The rest is just:




| `<updated columns>` | New values that replace old ones (e.g. `discount = 0.2`) |
| --- | --- |


### Patch part indexes [\#](/blog/updates-in-clickhouse-2-sql-style-updates#patch-part-indexes)


Once the patch part exists, ClickHouse needs to know when and where to apply it. For that, it builds two lightweight indexes (per patch part), one forward, one reverse:




| `Index name` | Purpose |
| --- | --- |
| `Source part index` | Maps each affected source part to the min/max data version. Used to ask: *Should I apply this patch to this part?* |
| `Reverse index` | Maps the patch's data version to all parts and blocks that need it. Used to find patch targets even after merges. |


These indexes enable **efficient targeting** even when data parts are merged in the background.


### Fast source part matching via index [\#](/blog/updates-in-clickhouse-2-sql-style-updates#fast-source-part-matching-via-index)


ClickHouse uses the patch part’s `source part index` to quickly determine which source parts the update applies to. In our example, only `all_1_1_0` and `all_3_3_0` match, the update doesn’t touch `all_2_2_0`.


### Fast patch merge via system column–driven sorting [\#](/blog/updates-in-clickhouse-2-sql-style-updates#fast-patch-merge-via-system-columndriven-sorting)


As explained earlier, **[patch parts piggyback on merges already running in the background](/blog/updates-in-clickhouse-2-sql-style-updates#theyre-efficient)**. Since all parts are sorted by \_part\_offset (either implicitly or explicitly), ClickHouse can apply the patch in a **single, efficient merge pass**.


### Preserving row identity during merges [\#](/blog/updates-in-clickhouse-2-sql-style-updates#preserving-row-identity-during-merges)


In the merged part (⑤), `_part_offset` values are **recreated** to reflect each row’s new position. But `_block_number` and `_block_offset` are **copied over unchanged** from the original parts.



> This detail is **crucial** for supporting updates that run **concurrently with merges** of the affected parts.


Let’s explore how that works in the next section.


## Updates don’t wait for merges [\#](/blog/updates-in-clickhouse-2-sql-style-updates#updates-dont-wait-for-merges)


ClickHouse updates are **non\-blocking**: they don’t wait for merges to finish. Instead, each update runs against a [snapshot](https://clickhouse.com/blog/clickhouse-release-25-06#single-snapshot-for-select) of the parts that exist when the UPDATE begins.



> Classic mutations must wait for prior merges and mutations to finish before they run.


In most cases, that snapshot is still valid when the patch part is later applied. But if those parts are **merged away** before that happens, ClickHouse automatically falls back to a different matching strategy.


Let’s look at how that fallback works.


### What happens if the parts are merged before a patch is applied? [\#](/blog/updates-in-clickhouse-2-sql-style-updates#what-happens-if-the-parts-are-merged-before-a-patch-is-applied)


The next diagram picks up the same extended example from the previous section, but shows what happens when the parts are merged **before** the patch is applied.



> In the previous diagram, we dimmed `_block_number` and `_block_offset`. This time, we dim (show in light gray) `_part`, `_part_offset`, and the patch’s `source part index`; they’re not used here.


![Blog-updates Part 2.007.png](/uploads/Blog_updates_Part_2_007_4ed2800064.png)
**What changes in this scenario?**


**①–③**: **The same inserts** and ⑤ UPDATE run as before, those steps are unchanged.


**④**: But this time, **a background merge** combines the original parts into a single part before the patch can be applied. The source parts (①–③) are then removed, as usual for merges.


**⑤**: The original `_part` and `_part_offset` values referenced by the patch part are no longer valid. So ClickHouse falls back to `_block_number` and `_block_offset`, which are preserved during merges.


**⑥–⑧**: **ClickHouse applies the patch using a hash join** based on those preserved values, producing a merged data part with the patch applied.


Let’s take a closer look at how that fallback patching path works.


### Source part matching via reverse index [\#](/blog/updates-in-clickhouse-2-sql-style-updates#source-part-matching-via-reverse-index)


The reverse index shows that this patch applies to **data version 4**, and targets parts `all_1_1_0` and `all_3_3_0`, which (based on their [names](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#how-to-read-a-part-name)) contained **block numbers 1 and 3**.


The merged part `all_1_3_1` (based on its name) spans **block numbers 1 to 3**, so it’s a valid match. Also, its data version is `1` (inferred from its lowest block number), which is less than the patch’s version `4`, so the patch can be applied.


This reverse mapping lets ClickHouse match and patch data even after merges invalidate the original part names.


### Patch application via join on block\-based system columns [\#](/blog/updates-in-clickhouse-2-sql-style-updates#patch-application-via-join-on-block-based-system-columns)


We can’t use `_part` and `_part_offset` anymore to efficiently apply the patch in a merge, since the source parts are gone and their original values no longer match the corresponding rows in the merged output.


Instead, ClickHouse applies the patch using a **hash join\-based algorithm**, loading the patch part into memory as a hash table keyed by `(_block_number, _block_offset)`, and joins it with the merged part using the same key to update the rows.


This fallback is slower and more memory\-hungry than the fast path in the previous section. The patch must fit entirely in memory, but in the future, ClickHouse may support a `full merge join` that isn’t memory\-bound, though that’s not yet implemented.


Thankfully, this rarely happens in practice, since the source data parts usually live long enough for fast patching.


Now that we’ve seen how ClickHouse handles UPDATEs, even during merges, let’s talk about how DELETEs have gotten just as efficient.


## Lightweight deletes are now even lighter [\#](/blog/updates-in-clickhouse-2-sql-style-updates#lightweight-deletes-are-now-even-lighter)


In [Stage 1\.5](/blog/updates-in-clickhouse-2-sql-style-updates#stage-15-lightweight-deletes-still-mutations-but-faster), **lightweight DELETEs** already gave us a win: they rewrote only the `_row_exists` deletion mask via an ALTER UPDATE, avoiding full\-row rewrites.


But we can go even lighter.


When [`lightweight_delete_mode`](https://clickhouse.com/docs/operations/settings/settings#lightweight_delete_mode) \= `lightweight_update`, DELETEs aren’t ALTERs at all. ClickHouse simply creates a patch part that sets `_row_exists = 0` for the deleted rows. The rows are then dropped during the next background merge.


The diagram below reuses the same example from Stage 1\.5: we delete the mouse item from the original order. (*Unused system columns like \_block\_number, \_block\_offset, etc. are omitted for clarity.*)


![Blog-updates Part 2.008.png](/uploads/Blog_updates_Part_2_008_1825514794.png)
① The initial part contains two rows.


② A patch part sets `_row_exists = 0` for the deleted row (the mouse).


③ During the next merge, that row disappears.


ClickHouse applies the patch instantly. Until the merge happens, queries simply ignore rows where `_row_exists = 0`. This is the heart of **patch\-on\-read query execution**.


## How patch\-on\-read works [\#](/blog/updates-in-clickhouse-2-sql-style-updates#how-patch-on-read-works)


ClickHouse doesn’t wait to materialize patch parts before returning updated results. Instead:



> Patch parts are applied automatically and on the fly in memory during query execution, [like an implicit FINAL](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines#getting-up-to-date-results-with-final).


**This patch\-on\-read mechanism is designed to minimize performance impact.**


Usually, the data selected for a query (after [index analysis](https://clickhouse.com/docs/primary-indexes)) is located in several **data ranges** (consecutive blocks of rows) in several data parts. These ranges are dynamically spread by the [query engine](https://clickhouse.com/docs/academic_overview#4-query-processing-layer) across ① separate and **parallel stream stages** (data streams) and then processed by ② **[parallel processing lanes](https://clickhouse.com/docs/optimize/query-parallelism#distributing-work-across-processing-lanes)** that filter, aggregate, sort, and limit the data into its final result:


![Blog-updates Part 2.009.png](/uploads/Blog_updates_Part_2_009_bfefb2e8c3.png)
Not\-yet\-merged patch parts are ③ matched and **applied independently for each data range** in each data stream, ensuring that updates are applied correctly without disrupting parallelism.


*(If needed, you can fully materialize all accumulated not\-yet\-merged changes with `ALTER TABLE … APPLY PATCHES`, but that’s optional.)*


To fully understand patch parts, we also need to look at their lifecycle: how ClickHouse merges, deduplicates, and cleans them up in the background.


## What happens to patch parts over time? [\#](/blog/updates-in-clickhouse-2-sql-style-updates#what-happens-to-patch-parts-over-time)


Patch parts may seem special, but under the hood, they’re just regular parts in ClickHouse. That means:


- They are **merged with other patch parts** using the *[ReplacingMergeTree](/blog/updates-in-clickhouse-1-purpose-built-engines#replacingmergetree-replace-rows-by-inserting-new-ones)* algorithm, with `_data_version` as a [version column](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree#replacingmergetree-parameters). This ensures each patch part stores only the latest version of each updated row.
- They’re **automatically cleaned up** once their changes are fully materialized into all affected data parts, or when merged with another patch part. Background cleanup threads handle this safely.
- **[They count toward the TOO\_MANY\_PARTS threshold](https://clickhouse.com/docs/operations/settings/merge-tree-settings#parts_to_throw_insert)**, which applies **per partition**. To mitigate this, patch parts are stored in **separate partitions based on the set of updated columns**. So if you run multiple UPDATE statements that affect different columns, like `SET x = …`, `SET y = …`, and `SET x = …, y = …`, you’ll get separate patch partitions, each with its own part count.


This design keeps patch parts fast, efficient, and deeply integrated with MergeTree mechanics.


So far, we’ve focused on how patch parts behave in isolation. But what happens when multiple updates arrive at the same time? Let’s look at how ClickHouse coordinates concurrent updates safely.


## Coordinating concurrent updates [\#](/blog/updates-in-clickhouse-2-sql-style-updates#coordinating-concurrent-updates)


**ClickHouse runs updates in parallel by default.** If two updates touch the same columns, it automatically runs them in the correct order. You don’t need to configure anything; it just works.


You can tweak this behavior with a few settings:


- **[`update_parallel_mode`](https://clickhouse.com/docs/operations/settings/settings#update_parallel_mode)**:


	- `auto` (default): Serializes dependent updates (e.g. `UPDATE a=3 WHERE b=2` and `UPDATE b=2 WHERE a=1`). Runs others in parallel.
	- `sync`: Runs all updates one at a time.
	- `async`: Runs all updates with no coordination.
- **[`update_sequential_consistency`](https://clickhouse.com/docs/operations/settings/settings#update_sequential_consistency)** (off by default): Ensures each update sees the latest visible state, at some performance cost.


But for most workloads, the default is fast, safe, and does the right thing.


All of this coordination happens behind the scenes, so that from the outside, updates just feel like SQL. It just works.


As we reach the end of this post, let’s step back and look at the bigger picture.


## From engine\-specific tricks to familiar SQL [\#](/blog/updates-in-clickhouse-2-sql-style-updates#from-engine-specific-tricks-to-familiar-sql)


Patch parts bring efficient SQL\-style UPDATEs to ClickHouse, not by breaking the rules of columnar storage, but by embracing them.


We leaned into what makes ClickHouse fast:  

**Inserts are fast. Merges are continuous. Parts are immutable and sorted.**


And because **inserts are so fast**, we turned updates into inserts.  

ClickHouse inserts compact **patch parts** behind the scenes and applies them efficiently during merges.


**Merges are already happening, so we made them do more. Without really doing more.**  

Since the engine is already merging data parts in the background, it now applies updates with minimal overhead.


**Patch parts slide in instantly with minimal impact on query performance.**  

Updates show up right away, with not\-yet\-merged patches applied in a way that preserves parallelism.


This is the core mechanism that now powers *lightweight updates* in ClickHouse.


They build on the same principles as engines like ReplacingMergeTree, but in a fully general way, encapsulated behind flexible, standard SQL syntax:



```

```
1UPDATE orders
2SET discount = 0.2
3WHERE quantity >= 40;
```


```

The result: Updates show up instantly. Queries stay fast. Nothing blocks. It’s UPDATE, the ClickHouse way. All in familiar SQL.


**In [Part 3](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks), we’ll put it to the test.**  

We benchmark every update method, mutations, on\-the\-fly mutations, and lightweight patch parts updates, and show just how fast standard SQL UPDATEs in ClickHouse can get.  

**Spoiler: it’s not just faster. It’s up to 1,000× faster. Sometimes even more.**

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

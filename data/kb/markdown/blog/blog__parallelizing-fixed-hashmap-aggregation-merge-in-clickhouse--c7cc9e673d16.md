# Parallelizing ClickHouse aggregation merge for fixed hash map


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Parallelizing ClickHouse aggregation merge for fixed hash map

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[Jianfei Hu](/authors/jianfei-hu)Dec 16, 2025 · 8 minutes read## Editor’s note [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#editors-note)


In ClickHouse 25\.11, we introduced **parallel merge for small GROUP BY**, an optimization that significantly speeds up aggregations on 8\-bit and 16\-bit keys by parallelizing the merge phase for FixedHashMap\-based aggregations. The feature is described briefly in the [25\.11 release post](https://clickhouse.com/blog/clickhouse-release-25-11#parallel-merge-for-small-group-by). ￼


What follows is the original engineering write\-up by [Jianfei Hu](https://github.com/incfly), who implemented this optimization. Jianfei initially published this as a personal deep dive while working through the problem, exploring false starts, internal mechanics of ClickHouse aggregation, and the subtle concurrency and memory\-management issues involved.


We’re publishing it here largely unchanged, because it captures something release notes can’t:



> What it actually felt like to build this optimization, and what it taught along the way.


## **Background** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#background)


I recently worked on<https://github.com/ClickHouse/ClickHouse/pull/87366>. The idea is simple but learned a lot of ClickHouse aggregation, so want to jot it down.


The original [issue](https://github.com/ClickHouse/ClickHouse/issues/63666) stated it clear, if you run almost identical queries, their performances varies a lot!



```

```
1SELECT
2    number % 10000 AS k,
3    uniq(number) AS u
4FROM numbers_mt(1000000000.)
5GROUP BY k
6ORDER BY u DESC
7LIMIT 10
```

```


```
    ┌────k─┬──────u─┐
 1. │ 4759 │ 101196 │
 2. │ 4587 │ 101079 │
 3. │ 6178 │ 101034 │
 4. │ 6567 │ 101032 │
 5. │ 9463 │ 101013 │
 6. │  298 │ 101009 │
 7. │ 2049 │ 100993 │
 8. │ 8167 │ 100989 │
 9. │ 5530 │ 100973 │
10. │ 1968 │ 100973 │
    └──────┴────────┘

10 rows in set. Elapsed: 62.793 sec. Processed 1.00 billion rows, 8.00 GB (15.93 million rows/s., 127.40 MB/s.)
Peak memory usage: 11.30 GiB.

```


```

```
1SELECT
2    0 + (number % 10000) AS k,
3    uniq(number) AS u
4FROM numbers_mt(1000000000.)
5GROUP BY k
6ORDER BY u DESC
7LIMIT 10
```

```


```
    ┌────k─┬──────u─┐
 1. │ 4759 │ 101196 │
 2. │ 4587 │ 101079 │
 3. │ 6178 │ 101034 │
 4. │ 6567 │ 101032 │
 5. │ 9463 │ 101013 │
 6. │  298 │ 101009 │
 7. │ 2049 │ 100993 │
 8. │ 8167 │ 100989 │
 9. │ 5530 │ 100973 │
10. │ 1968 │ 100973 │
    └──────┴────────┘

10 rows in set. Elapsed: 8.547 sec. Processed 1.00 billion rows, 8.00 GB (116.99 million rows/s., 935.95 MB/s.)
Peak memory usage: 10.09 GiB.

```

1. The only difference is that second query is using `0 + (number % 10000)` for the group by value `k`.
2. ClickHouse treats the k as UInt16 in first query and UInt64 in the second query.


But why does this matter? Let's delve into the aggregation technical details a bit in ClickHouse.


## **How Aggregation Works** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#how-aggregation-works)


When we group by a number smaller than UInt16, we could use array for hashmap:


![525537392-b69eefa7-f88c-4c03-aa0d-9d61390bcbda.jpg](/uploads/525537392_b69eefa7_f88c_4c03_aa0d_9d61390bcbda_35356ef388.jpg)
Otherwise use standard hash map, and potentially converted to two level hash map:


![526131500-2b0a604b-7483-4d98-9bd4-a48e5fe36a13.jpg](/uploads/526131500_2b0a604b_7483_4d98_9bd4_a48e5fe36a13_45b94911b8.jpg)
What does it mean for merging the aggregation state?


![526067696-4c177f87-85cc-48b6-9475-a95de5ed3dfc.jpg](/uploads/526067696_4c177f87_85cc_48b6_9475_a95de5ed3dfc_aa36d41e95.jpg)
Now it's clear why first query is slow


- When each thread has a two level hash table. Merge can be parallel: T1 works on 0\-7 bucket, and T2 8\-15, etc.
- When fixed hash map is used, every aggregation state is stored in a single one dimension array. Such bucket based parallel merge is not possible.


## **Improvement** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#improvement)


- Initial idea is to convert the one dimension array to two level, but that turns out to be slow.
- Nikita T. proposed the idea: let the each merge worker thread working on disjoint subsets of the group by keys in\-place, no race condition, no conversion needed.
- Hence my implementation. But still lots of to learn.


### **Range based segmentation not working well** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#range-based-segmentation-not-working-well)


The first intuitive idea is to segment the keys into different range:


![526067695-9db4e53b-e1e1-4512-9924-0a4c8688e459.jpg](/uploads/526067695_9db4e53b_e1e1_4512_9924_0a4c8688e459_03f90e7e3b.jpg)
Faster but not so much. Flamegrapah remains the same! Because while the wall clock time is different due to parallelism, the CPU time for the stacktrace is the same. You can't figure it out by looking at stack trace. I figured this out via logging and checking timespent along with the thread id.


Once knowing this, I decided to distribute the merge work to differently:


![525537386-e440bf78-143c-47ab-8c24-4c737f8c6e1b.jpg](/uploads/525537386_e440bf78_143c_47ab_8c24_4c737f8c6e1b_6a5f837c62.jpg)
### **Weird memory corruption error** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#weird-memory-corruption-error)


At one point CI [fails](https://pastila.nl/?cafebabe/a1b797aa9779c26c0391865cf208e5ad#mHyGN0/Fr3pxD/QVGRymwg==) with errors from memory deallocation. Certain assertions checks of the size failed.



```
2025.09.22 01:04:58.132587 [ 906517 ] {} <Fatal> BaseDaemon: 10. /home/incfly/workspace/github.com/ClickHouse/ClickHouse/src/Common/Exception.h:58: DB::Exception::Exception(PreformattedMessage&&, int) @ 0x000000000b549785
2025.09.22 01:04:58.243209 [ 906517 ] {} <Fatal> BaseDaemon: 11. /home/incfly/workspace/github.com/ClickHouse/ClickHouse/src/Common/Exception.h:141: DB::Exception::Exception<unsigned long&>(int, FormatStringHelperImpl<std::type_identity<unsigned long&>::type>, unsigned long&) @ 0x000000000bce6cab
2025.09.22 01:04:58.248715 [ 906517 ] {} <Fatal> BaseDaemon: 12.0. inlined from /home/incfly/workspace/github.com/ClickHouse/ClickHouse/src/Common/Allocator.cpp:119: (anonymous namespace)::checkSize(unsigned long)
2025.09.22 01:04:58.248738 [ 906517 ] {} <Fatal> BaseDaemon: 12. /home/incfly/workspace/github.com/ClickHouse/ClickHouse/src/Common/Allocator.cpp:144: Allocator<false, false>::free(void*, unsigned long) @ 0x000000001272c82e
2025.09.22 01:04:58.265559 [ 906517 ] {} <Fatal> BaseDaemon: 13. /home/incfly/workspace/github.com/ClickHouse/ClickHouse/src/Common/Arena.h:94: DB::Arena::MemoryChunk::~MemoryChunk() @ 0x000000000c8858a2
2025.09.22 01:04:58.281901 [ 906517 ] {} <Fatal> BaseDaemon: 14.0. inlined from /home/incfly/workspace/github.com/ClickHouse/ClickHouse/contrib/llvm-project/libcxx/include/__memory/unique_ptr.h:80: std::default_delete<DB::Arena::MemoryChunk>::operator()[abi:se190107](DB::Arena::MemoryChunk*) const
2025.09.22 01:04:58.281922 [ 906517 ] {} <Fatal> BaseDaemon: 14.1. inlined from /home/incfly/workspace/github.com/ClickHouse/ClickHouse/contrib/llvm-project/libcxx/include/__memory/unique_ptr.h:292: std::unique_ptr<DB::Arena::MemoryChunk, std::default_delete<DB::Arena::MemoryChunk>>::reset[abi:se190107](DB::Arena::MemoryChunk*)

```

I have no clue how the memory management gets into trouble from my changes. Reading the code, I found `DB::Arena` is a very interesting technique for memory management.


Imagine you need to create lots of small sized string in a query execution for intermediate results (such as our aggregation state). They are short lived and would be all removed together. Traditional way to handle that would be maintaining a region of free memory and bookkeep the allocated and free memory regions using a linked list:


![525537388-8215e7b6-68aa-4fe3-9a52-76ee5992fef8.jpg](/uploads/525537388_8215e7b6_68aa_4fe3_9a52_76ee5992fef8_8f7be1ac7b.jpg)
`DB::Arena` however, just using a single offset index variable to record the next free memory location. Every time when allocating sized M bytes, Arena just returns `offset` as pointer and increment by M:


![525537389-10f6b3ae-eaab-494d-8d34-c32932d89777.jpg](/uploads/525537389_10f6b3ae_eaab_494d_8d34_c32932d89777_15a7f7f736.jpg)
- This is extremely fast: no traversal to find slot.
- Cannot free individual memory which is fine to this use case, as all objects would be deallocated together. Just free the entire Arena region.


Come back to my issue. I noticed a few different but related failures


- Running large number of aggregation can ended up with segmentation fault, stack trace also showing from relevant Arena code.
- Query results can also be wrong sometimes.


All these pointed out to the race condition of the memory allocation. Re\-checking the code, Arena is not thread safe and existing two level aggregation uses one Arena per thread during merge. Fixing my mis\-usage of using the same Arena, resolves the issue.


### **Trivial count/select performance degrade** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#trivial-countselect-performance-degrade)


I found that if I replace aggregation function to trivial ones such as count/sum/min/max in the example query above, not only it does not speed up but even become slower. I figured it would because the overhead of parallel merge cannot be justified when the merge work itself is too trivial. Therefore I disabled the optimization for those cases.


However reviewer carefully point out that we should try to understand the reason:


1. Fixed hash map records a min / max index to speed up iterations and other operations. We disabled that to avoid race condition.
2. This means that we have to iterate the whole array instead of the ones that is populated, imagine `k % 100` .
3. All slowed down queries are slowed down by the same amount of time, 3ms always.


Solution: extract the min/max index before parallel merge to limit the range of iteration.


## **Misc. technical details** [\#](/blog/parallelizing-fixed-hashmap-aggregation-merge-in-clickhouse#misc-technical-details)


ClickHouse CI [performance](https://github.com/ClickHouse/ClickHouse/pull/87366#discussion_r2426184017) test provides differential flame graph. This is how we identify the introduced small perf penalty. In example below:


![fixed_hash_table_parallel_merge_1_CPU_SELECT-number---10000-AS-k--count-number--AS-u-FROM-numbers_mt-1e7--GROUP-BY-k-ORD.diff.svg](/uploads/fixed_hash_table_parallel_merge_1_CPU_SELECT_number_10000_AS_k_count_number_AS_u_FROM_numbers_mt_1e7_GROUP_BY_k_ORD_diff_a170be3862.svg)
1. `FixedHashMap.h:123# Aggregator::mergeDataImpl` was identified slight increase. This points to the `isZero` function. But why still annotated with Aggregator function? Some compiler trick recognized while being inlined in the same function the original source code is still in another file.
2. I still don't fully understand why the new function `mergeSingleLevelDataImplFixedMap` and others are identified as white. Some tricks in the flamegraph differential calculation.
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

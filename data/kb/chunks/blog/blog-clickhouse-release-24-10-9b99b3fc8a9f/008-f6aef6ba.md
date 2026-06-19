---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-24-10
ch_version_introduced: '922.460'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 10
---

... count: 693137012, storageSize: 746628136960 ``` The document count is the same as in ClickHouse, and the storage size is slightly larger, at 695\.35 GiB. We can also check the structure of one of the stored JSON documents:

```
github> db.events.aggregate([{ $sample: { size: 1 } }]);
[
  {
    _id: ObjectId('672ab1430e44c2d6ce0433ee'),
    id: '28105983813',
    type: 'DeleteEvent',
    actor: {
      id: 10810283,
      login: 'direwolf-github',
      display_login: 'direwolf-github',
      gravatar_id: '',
      url: 'https://api.github.com/users/direwolf-github',
      avatar_url: 'https://avatars.githubusercontent.com/u/10810283?'
    },
    repo: {
      id: 183051410,
      name: 'direwolf-github/my-app',
      url: 'https://api.github.com/repos/direwolf-github/my-app'
    },
    payload: { ref: 'branch-58838bda', ref_type: 'branch', pusher_type: 'user' },
    public: true,
    created_at: '2023-03-31T00:43:36Z'
  }
]


```

Now we want to analyze the data set and get an overview of the different GitHub event types and rank them by their document count. In ClickHouse, this can be done with a simple Aggregation SQL query:

```
SELECT
    docs.type,
    count() AS count
FROM events
GROUP BY docs.type
ORDER BY count DESC

    ┌─docs.type─────────────────────┬─────count─┐
 1. │ PushEvent                     │ 378108538 │
 2. │ CreateEvent                   │  95054342 │
 3. │ PullRequestEvent              │  55578642 │
 4. │ WatchEvent                    │  41269499 │
 5. │ IssueCommentEvent             │  32985638 │
 6. │ DeleteEvent                   │  22395484 │
 7. │ PullRequestReviewEvent        │  17029889 │
 8. │ IssuesEvent                   │  14236189 │
 9. │ PullRequestReviewCommentEvent │  10285596 │
10. │ ForkEvent                     │   9926485 │
11. │ CommitCommentEvent            │   6569455 │
12. │ ReleaseEvent                  │   3804539 │
13. │ PublicEvent                   │   2352553 │
14. │ MemberEvent                   │   2304020 │
15. │ GollumEvent                   │   1235200 │
    └───────────────────────────────┴───────────┘

15 rows in set. Elapsed: 7.324 sec. Processed 693.14 million rows, 20.18 GB (94.63 million rows/s., 2.76 GB/s.)
Peak memory usage: 7.33 MiB.

```

The query aggregates and sorts the complete data set (\~700 million JSON documents). The query's runtime is 7\.3 seconds, and the peak memory usage is 7\.33 MiB. This low memory usage is attributed to ClickHouse’s [true column\-oriented storage](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-1-true-column-oriented-storage) for JSON documents, enabling independent access to sub\-columns for JSON paths. Additionally, ClickHouse retrieves only the columns required for a query. In our example, it reads, aggregates, and sorts data exclusively from the `docs.type` column. Also note the query throughput of 94 million rows/s., and 2\.76 GB/s.

An [aggregation pipeline](https://www.mongodb.com/resources/products/capabilities/aggregation-pipeline) is the recommended way of doing aggregations in MongoDB. We ran an aggregation pipeline in MongoDB that is equivalent to our ClickHouse SQL query from above:

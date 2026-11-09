---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Window
topic: window-and-array-functions-for-git-commit-sequences-clickhouse
ch_version_introduced: '9.1'
last_updated: '2026-11-09'
chunk_index: 6
total_chunks_in_doc: 7
---

author's longest sequence of commits. The [arrayMax](https://clickhouse.com/docs/en/sql-reference/functions/array-functions/#arraymax) function makes this trivial. ![Bite-sized_git-array-functions_v2.png](/_next/image?url=%2Fuploads%2FBite_sized_git_array_functions_v2_4dec386f4a.png&w=2048&q=75) Putting this all together, we need to sort by the largest consecutive count first. So who is the committer with the longest sequence of uninterrupted work?

```

WITH commit_days AS
    (
        SELECT
            author,
            toDate(day) AS day,
            any(day) OVER (PARTITION BY author ORDER BY day ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS previous_commit,
            dateDiff('day', previous_commit, day) AS days_since_last,
            if(days_since_last = 1, 1, 0) AS consecutive
        FROM
        (
            SELECT
                author,
                toStartOfDay(time) AS day
            FROM git.commits
            GROUP BY
                author,
                day
            ORDER BY
                author ASC,
                day ASC
        )
    )
SELECT
    author,
    arrayMax(arrayMap(x -> length(x), arraySplit(x -> (x = 0), groupArray(consecutive)))) - 1 AS max_consecutive_days
FROM commit_days
GROUP BY author
ORDER BY max_consecutive_days DESC
LIMIT 5


┌─author───────────┬─max_consecutive_days─┐
│ kssenii          │                   32 │
│ Alexey Milovidov │                   30 │
│ alesapin         │                   26 │
│ Azat Khuzhin     │                   23 │
│ Nikolai Kochetov │                   15 │
└──────────────────┴──────────────────────┘

5 rows in set. Elapsed: 0.028 sec. Processed 61.90 thousand rows, 389.87 KB (2.19 million rows/s., 13.78 MB/s.)
 [✎](https://sql.clickhouse.com?query_id=S3E64UYCAMDAYJRSXINVFR)

```

Well done to [Kssenii](https://github.com/kssenii) !

## Conclusion \#

In this post, we’ve demonstrated how window and array functions can be used to solve sequence problems in ClickHouse. In our case, we’ve identified the author with the longest consecutive days of commits to our own repository. Similar techniques can, however, be applied to other datasets to find sequential patterns.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=0)

---

Share this post

- Copy URL
- [![Y Combinator icon](/_next/static/immutable/media/ycombinator.37q2g-no9bowl.svg)](https://news.ycombinator.com/submitlink?u= "Share on Y Combinator")
- [![X icon](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/intent/tweet?text= "Share on X")
- [![Bluesky icon](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/intent/compose?text= "Share on Bluesky")
- [![Facebook icon](/_next/static/immutable/media/facebook.32ysyflv7kktz.svg)](https://www.facebook.com/sharer/sharer.php?u= "Share on Facebook")
- [![LinkedIn icon](/_next/static/immutable/media/linkedin.37911rnwi-sdg.svg)](https://www.linkedin.com/sharing/share-offsite/?url= "Share on LinkedIn")
### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!

## Recent posts

[View all Blogs](/blog)![img 5912](/_next/image?url=%2Fuploads%2FIMG_5912_4fde8778dc.jpg&w=750&q=75)Engineering### [What I learned from a month with WalShadow on ClickHouse Managed Postgres](/blog/a-month-with-walshadow-clickhouse-managed-postgres)

Hidehiko ASAHI · Nov 6, 2026![blog cover 1200x630 14](/_next/image?url=%2Fuploads%2FBlog_Cover_1200x630_14_380a4d0d49.png&w=750&q=75)Engineering### [ClickHouse release 26\.10](/blog/clickhouse-release-26-10)

ClickHouse · Nov 6, 2026![mongodb clickpipes ga](/_next/image?url=%2Fuploads%2FMongo_DB_Click_Pipes_GA_28ee291c8e.png&w=750&q=75)Product### [MongoDB CDC connector for ClickPipes is now generally available](/blog/mongodb-cdc-connector-clickpipes-ga)

Marta Paes · Nov 4, 2026![postgres fencing nov2026 banner](/_next/image?url=%2Fuploads%2Fpostgres_fencing_nov2026_banner_fd0fdfefc0.png&w=750&q=75)Engineering### [Fencing a Postgres primary that might still be alive](/blog/fencing-a-postgres-primary-that-might-still-be-alive)

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-projections-now-behave-like-true-secondary-indexes-clickhouse
ch_version_introduced: '0.084'
last_updated: '2026-11-16'
chunk_index: 6
total_chunks_in_doc: 6
---

is \<\= this value, projection index can be applied. - min\_table\_rows\_to\_use\_projection\_index: If the estimated number of rows to read from the table is \>\= this value, projection index will be considered. ## A cleaner syntax in 26\.1 \#

Starting with ClickHouse 26\.1, defining these lightweight \_part\_offset projections becomes even simpler.

Instead of writing:

```
1PROJECTION by_time (
2    SELECT _part_offset ORDER BY date
3),
4PROJECTION by_town (
5    SELECT _part_offset ORDER BY town
6)
```
Copy command
You can now define them using a more compact syntax:

```
1PROJECTION by_time INDEX date TYPE basic,
2PROJECTION by_town INDEX town TYPE basic
```
Copy command
This syntax expresses the same idea: we define a projection whose primary index behaves like a secondary index on the specified column.

Functionally, nothing changes; the projections still store only the sorting key and \_part\_offset, and they still participate in granule\-level pruning exactly as described above.

## Key takeaway \#

ClickHouse tables once had only *one* primary index.

Now they can have **many**, each behaving like a primary index, and ClickHouse will use *all of them* when your query has multiple filters.

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

[View all Blogs](/blog)![jsonbench is back](/_next/image?url=%2Fuploads%2FJSON_Bench_is_back_6ea1528bec.png&w=750&q=75)Engineering### [JSONBench is back, and ClickHouse still leads](/blog/jsonbench-is-back-clickhouse-still-leads)

Tom Schreiber and Mark Needham · Nov 16, 2026![infinitas oct2026 banner yellow](/_next/image?url=%2Fuploads%2Finfinitas_oct2026_banner_yellow_136951726e.png&w=750&q=75)User stories### [How Infinitas Learning uses ClickHouse Managed Postgres to process billions of events for 1\.6M unique learners](/blog/infinitas-learning-clickhouse-managed-postgres)

ClickHouse · Nov 16, 2026![introducing loom agent memory that keeps up with your code](/_next/image?url=%2Fuploads%2FIntroducing_Loom_agent_memory_that_keeps_up_with_your_code_d2c2c52e54.jpg&w=750&q=75)Product### [Introducing Loom: agent memory that keeps up with your code](/blog/introducing-loom-agent-memory-that-keeps-up-with-your-code)

James Cunningham and Lareb Zafar · Nov 13, 2026![preview features nov2026 banner](/_next/image?url=%2Fuploads%2Fpreview_features_nov2026_banner_0f14a41e64.jpg&w=750&q=75)Product### [SET allow\_preview\_features \= 1: Self\-service previews in ClickHouse Cloud](/blog/self-service-previews-in-clickhouse-cloud)

Amy Chen · Nov 13, 2026[View all Blogs](/blog)## Follow us

[![X](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/ClickhouseDB "X")[![Bluesky](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/_next/static/immutable/media/slack.2_pspehyws_jz.svg)](/slack "Slack")[![Github](/_next/static/immutable/media/github.3ofxqpa2uzt_a.svg)](https://github.com/ClickHouse/ClickHouse "Github")[![Telegram](/_next/static/immutable/media/telegram.0054ol1lpoidb.svg)](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/_next/static/immutable/media/meetup.2tf1x11zaaepo.svg)](https://www.meetup.com/pro/clickhouse "Meetup")[![RSS](/_next/static/immutable/media/rss.1pu3aqlsglh-q.svg)](/rss.xml "RSS")

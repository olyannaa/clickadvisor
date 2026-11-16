---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-26-6-clickhouse
ch_version_introduced: '26.6'
last_updated: '2026-11-16'
chunk_index: 10
total_chunks_in_doc: 10
---

command ``` 1┌─dequantizeIn⋯(quantized)─┐ 2│ 1.5 │ 3└──────────────────────────┘ ``` Copy command We could use this function to shrink vector indexes 4x (or more) for cheaper similarity search. ## Memory reservations for workloads \# ### Contributed by Sergei Trifonov \#

The workload scheduler, which already manages CPU, I/O and concurrency, now manages memory as well as of ClickHouse 26\.6\.

We start by creating a resource:

```
1CREATE RESOURCE memory (MEMORY RESERVATION);
```
Copy command
And then, we can define various workloads:

```
1CREATE WORKLOAD all;
2CREATE WORKLOAD prod IN all SETTINGS max_memory = '100G';
3CREATE WORKLOAD reports IN all SETTINGS max_memory = '20G';
4CREATE WORKLOAD vasya IN reports SETTINGS weight = 1;
5CREATE WORKLOAD petya IN reports SETTINGS weight = 2;
```
Copy command
When we write a query, we can route it to a workload like this:

```
1SELECT … 
2SETTINGS workload = 'prod';
```
Copy command### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-1336-get-started-today-sign-up&utm_blogctaid=1336)### Get started today

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

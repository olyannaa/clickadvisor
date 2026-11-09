---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-26-10-clickhouse
ch_version_introduced: '26.10'
last_updated: '2026-11-09'
chunk_index: 18
total_chunks_in_doc: 18
---

| --- | --- | | 1 | 1\.204 s | 128\.66 MiB | | 2 | 1\.303 s | 127\.93 MiB | | 3 | 1\.251 s | 129\.05 MiB | Changing `apply_string_filters_during_scan` to `1` gives us:

| Run | Query time | Peak memory |
| --- | --- | --- |
| 1 | 1\.091 s | 2\.54 MiB |
| 2 | 1\.333 s | 2\.54 MiB |
| 3 | 1\.232 s | 2\.54 MiB |


Every run returns the same 293,115 matches. Execution time is similar, but peak memory drops from around 129 MiB to 2\.54 MiB, a reduction of about 98%.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-2892-get-started-today-sign-up&utm_blogctaid=2892)### Get started today

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

Hidehiko ASAHI · Nov 6, 2026![mongodb clickpipes ga](/_next/image?url=%2Fuploads%2FMongo_DB_Click_Pipes_GA_28ee291c8e.png&w=750&q=75)Product### [MongoDB CDC connector for ClickPipes is now generally available](/blog/mongodb-cdc-connector-clickpipes-ga)

Marta Paes · Nov 4, 2026![postgres fencing nov2026 banner](/_next/image?url=%2Fuploads%2Fpostgres_fencing_nov2026_banner_fd0fdfefc0.png&w=750&q=75)Engineering### [Fencing a Postgres primary that might still be alive](/blog/fencing-a-postgres-primary-that-might-still-be-alive)

Furkan Sahin · Nov 4, 2026![clickstack whatsnew nov2026 banner](/_next/image?url=%2Fuploads%2Fclickstack_whatsnew_nov2026_banner_1fc0bc6417.png&w=750&q=75)Product### [What's new in ClickStack \- September and October '26](/blog/whats-new-in-clickstack-october-2026)

The ClickStack Team · Nov 3, 2026[View all Blogs](/blog)## Follow us

[![X](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/ClickhouseDB "X")[![Bluesky](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/_next/static/immutable/media/slack.2_pspehyws_jz.svg)](/slack "Slack")[![Github](/_next/static/immutable/media/github.3ofxqpa2uzt_a.svg)](https://github.com/ClickHouse/ClickHouse "Github")[![Telegram](/_next/static/immutable/media/telegram.0054ol1lpoidb.svg)](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/_next/static/immutable/media/meetup.2tf1x11zaaepo.svg)](https://www.meetup.com/pro/clickhouse "Meetup")[![RSS](/_next/static/immutable/media/rss.1pu3aqlsglh-q.svg)](/rss.xml "RSS")

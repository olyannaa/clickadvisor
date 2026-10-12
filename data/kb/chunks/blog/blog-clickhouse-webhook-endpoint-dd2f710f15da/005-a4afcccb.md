---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Using
topic: using-clickhouse-as-a-webhook-endpoint-with-hmac-verification-clickhouse
ch_version_introduced: '0.001'
last_updated: '2026-10-12'
chunk_index: 5
total_chunks_in_doc: 5
---

in both, which confirms the HMAC validation passed. Now make a change to your repository \-commit to a branch, open a PR, merge it \-and push events will appear in both tables. ![2026-02-20_16-11-08.png](/_next/image?url=%2Fuploads%2F2026_02_20_16_11_08_fbcc3df256.png&w=2048&q=75) ### Testing signature validation \#

To confirm the validation is working, go back to GitHub, change the webhook secret to something different, then make another commit.

`webhook_staging` will have the new rows but `webhook_logs` won't \- the materialized view computed a different HMAC and filtered them out.

![Webhook Diagram for Blog.jpg](/_next/image?url=%2Fuploads%2FWebhook_Diagram_for_Blog_ae59da5240.jpg&w=2048&q=75)

### Ready to create your own webhook endoint?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-77-ready-to-create-your-own-webhook-endoint-sign-up&utm_blogctaid=77)### Get started today

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

[View all Blogs](/blog)![isam customer story blog cover white](/_next/image?url=%2Fuploads%2Fi_SAM_Customer_Story_blog_cover_white_9d07b4b15f.jpg&w=750&q=75)User stories### [How iSAM Funds built an options research platform for a 10,000x data problem with ClickHouse Cloud](/blog/isam-market-data-research-platform)

ClickHouse · Oct 9, 2026![clera customer story blog cover yellow](/_next/image?url=%2Fuploads%2FClera_Customer_Story_blog_cover_yellow_608efd06bc.png&w=750&q=75)User stories### [How we migrated Clera’s 500 GB production database to ClickHouse Managed Postgres overnight](/blog/clera-migrates-to-clickhouse-managed-postgres)

Daniel Wintermeyer · Oct 8, 2026![introducing jwt authentication in clickhouse cloud](/_next/image?url=%2Fuploads%2FIntroducing_JWT_authentication_in_Click_House_Cloud_22fed5798e.jpg&w=750&q=75)Product### [Introducing JWT authentication in ClickHouse Cloud](/blog/introducing-jwt-authentication-in-clickhouse-cloud)

ClickHouse team · Oct 8, 2026![why bigquery can t match clickhouse cloud for real time analytics](/_next/image?url=%2Fuploads%2FWhy_Big_Query_can_t_match_Click_House_Cloud_for_real_time_analytics_4baf359921.jpg&w=750&q=75)Engineering### [Why BigQuery can’t match ClickHouse Cloud for real\-time analytics](/blog/clickhouse-vs-bigquery-real-time-performance-per-dollar)

Tom Schreiber and Lionel Palacin · Oct 8, 2026[View all Blogs](/blog)## Follow us

[![X](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/ClickhouseDB "X")[![Bluesky](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/_next/static/immutable/media/slack.2_pspehyws_jz.svg)](/slack "Slack")[![Github](/_next/static/immutable/media/github.3ofxqpa2uzt_a.svg)](https://github.com/ClickHouse/ClickHouse "Github")[![Telegram](/_next/static/immutable/media/telegram.0054ol1lpoidb.svg)](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/_next/static/immutable/media/meetup.2tf1x11zaaepo.svg)](https://www.meetup.com/pro/clickhouse "Meetup")[![RSS](/_next/static/immutable/media/rss.1pu3aqlsglh-q.svg)](/rss.xml "RSS")

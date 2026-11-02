---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-an-agentic-app-with-clickhouse-mcp-and-copilotkit-clickhouse
ch_version_introduced: '2406.12045'
last_updated: '2026-11-02'
chunk_index: 8
total_chunks_in_doc: 9
---

In this example, we're using the SQL Playground to host the UK Market dataset. We have configured the MCP Server to authenticate to the Playground using the demo user. You can see the configuration of this user [here](https://github.com/ClickHouse/sql.clickhouse.com/blob/main/setup.sql).

The demo user has read\-only access and is restricted to a specific set of databases. This allows us to limit the data the LLM can reach. On top of that, we apply quota settings and assign a limited profile to the user to prevent the model from overloading the server with too many or overly expensive queries. This setup gives us fine\-grained control over both the scope and cost of what the model can do.

## Conclusion \#

In this blog post, we explored how to build an agentic application using ClickHouse MCP Server and CopilotKit.

By leveraging the capabilities of LLMs, we created an application that allows users to build their own analytics dashboard on UK market data.

The use of a fast, scalable and secure analytics database like ClickHouse is crucial for the efficiency and effectiveness of such applications. This approach opens up new possibilities for creating AI\-powered tools that provide deeper insights and better user experiences.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

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

[View all Blogs](/blog)![meet groeneai](/_next/image?url=%2Fuploads%2FMeet_Groene_AI_8c18bb498d.jpg&w=750&q=75)Engineering### [Meet GroeneAI: our autonomous contributor to ClickHouse](/blog/meet-groeneai-our-autonomous-contributor-to-clickhouse)

James Cunningham, Artem Brustovetskii and Alex Soffronow Pagonidis · Oct 29, 2026![blog banner joins](/_next/image?url=%2Fuploads%2FBlog_banner_JOI_Ns_cf288c62ee.jpg&w=750&q=75)Engineering### [The new cost\-based join optimizer with reordering support for non\-inner joins](/blog/the-new-cost-based-join-optimizer-with-reordering-support-for-non-inner-joins)

Fisnik Kastrati · Oct 28, 2026![why clickhouse cloud wins at real time analytics](/_next/image?url=%2Fuploads%2FWhy_Click_House_Cloud_wins_at_real_time_analytics_56f70ab630.jpg&w=750&q=75)Engineering### [Why ClickHouse Cloud wins at real\-time analytics](/blog/why-clickhouse-cloud-wins-at-real-time-analytics)

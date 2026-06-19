---
source: blog
url: https://clickhouse.com/cloud/clickpipes
topic: the-new-clickhouse-cloud-experience
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 3
---

# The new ClickHouse Cloud experience

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The new ClickHouse Cloud experience

![](/_next/image?url=%2Fuploads%2Fgareth_head3_2225812acd.jpg&w=96&q=75)[Gareth Jones](/authors/gareth-jones)Apr 8, 2024 · 4 minutes readtl;dr

This week, we're releasing a major update to ClickHouse Cloud. Over the last nine months, we've worked hard to rethink, redesign, and reimplement the Cloud user experience, and we're excited to share these changes with you today.

---

The ClickHouse SQL console is integral to the way many Cloud users interact with their data. To reflect its importance, the SQL console is now fully integrated and prominently located at the top of the service navigation menu, allowing for easy access at all times. The SQL console itself has undergone a significant revamp, with the team working hard to eliminate countless UI and networking bugs and to enhance the user experience of common workflows. We've added information on running queries, and performance enhancements, and improved the capabilities of our AI\-powered SQL generator. When using the SQL console, the main navigation can be easily collapsed, providing you with the entire screen to fully immerse yourself in your work. These changes combine to create an experience that feels responsive, snappy, and more intuitive.
  

Demo of the ClickHouse SQL console

There is much more to this update than just the SQL console, though. We've concentrated a huge amount of effort on making the process of data ingestion much more approachable and streamlined. In the new Cloud experience, Data Sources are located right below the SQL console in the navigation, again reflecting how central they are to the ClickHouse experience. Uploading a file now supports seven different popular file types and, along with importing from a URL, has been reduced to a sleek two\-step, single\-page task. Another area that really shines in the new UI is the simple step\-by\-step workflows for ingesting and managing streaming data in ClickHouse. We call these [ClickPipes](https://clickhouse.com/cloud/clickpipes), and we believe that the ease with which continuous data can be imported into ClickHouse Cloud will prove to be a game\-changer.

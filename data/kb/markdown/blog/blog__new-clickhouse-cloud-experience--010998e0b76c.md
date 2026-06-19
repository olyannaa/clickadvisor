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





Data ingestion in ClickHouse Cloud


  

Performing common operational actions such as starting and stopping your service, adjusting autoscaling settings, or creating traffic filtering rules have been combined into a new Settings area, again, accessible from the main navigation. This gives you one single place to go and manage your infrastructure. If you have multiple services, there's a handy shortcut for switching between them in the navigation sidebar.


Outside of service\-specific actions, there are Account and Organization\-level controls that we've ensured are still just a click away. Items such as User Management, API Keys, and Billing, are all neatly located in the new Organization menu, while your Account profile and Security settings can be accessed from the menu triggered by the user avatar.


Providing both light and dark themes has become essential in modern web app development, and if you ask ten people which they prefer, there's a good chance you'll end up with an even split. For this reason, we felt it was important to give ClickHouse Cloud users the choice of how they want to experience the app.





Dark and Light themes available in ClickHouse Cloud


  

Building off our new design system and component library, [Click UI](https://click-ui.vercel.app), we've been able to create a modern, elegant, and consistent aesthetic throughout the Cloud experience. We firmly believe that in addition to being attractive and usable, the leading UI's are predictable. We felt that the best way to achieve that predictability was to implement and maintain a strict design system and consistent UX patterns.


While this was a lot of upfront work, it now allows us to design and develop at a rapid pace while staying on\-brand and uniform in everything we do. This becomes ever\-more important as teams grow and so it was important to establish this early in the ClickHouse company journey.


This is just the start, we have even more big improvements right around the corner. We'd love to hear your thoughts, so join our [slack channel](https://clickhouse.com/slack) if you have feedback or would like to follow along in our journey.


There's lots more I could say about the new, improved Cloud user experience, but why not take it for a spin yourself?

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

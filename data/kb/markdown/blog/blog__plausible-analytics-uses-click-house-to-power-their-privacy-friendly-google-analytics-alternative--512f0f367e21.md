# Plausible Analytics uses ClickHouse to power their privacy\-friendly Google Analytics alternative


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Plausible Analytics uses ClickHouse to power their privacy\-friendly Google Analytics alternative

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Dec 8, 2021 · 4 minutes read
Plausible Analytics is a lightweight, open source web analytics tool that has quickly gained popularity as the privacy\-friendly alternative to Google Analytics. By using Plausible Analytics, customers keep 100% ownership of their website data and protect the privacy of their visitors since there are no cookies and it is fully compliant with GDPR.


Since its launch in April 2019, the analytics platform has scaled to service 5000\+ paying subscribers. With an annual recurring revenue of half a million dollars, Plausible Analytics currently tracks 28,000 different websites and more than 1 billion page views per month.


Marko Saric, co\-founder at Plausible Analytics, said to handle this increase in volume, it became clear early on that the original architecture using Postgres to store analytics data could not handle the platform’s future growth.


“We knew that if we’re going to go anywhere in the future we needed something better,” Saric said.


## **“Best technical decision we ever made”** [\#](/blog/plausible-analytics-uses-click-house-to-power-their-privacy-friendly-google-analytics-alternative#best-technical-decision-we-ever-made-)


Through word of mouth, the Plausible team received the recommendation to try ClickHouse. They quickly noticed significant improvements in the loading speed of their dashboards. With Postgres, their dashboards were taking 5 seconds to load; Now with ClickHouse, it took less than a second.


Plausible co\-founder Uku Täht said the team also tried a couple of other solutions, but “Clickhouse came on top in terms of both performance and features that we would make use of,” he said.


“Plausible Analytics is a lightweight product, so it is important that everything loads quickly—the dashboard, segmentation of the data, and all the cool stuff in the background. Customers don’t know what we’re doing in the background, but they know that they want a fast experience,” Saric added.


“Plausible Analytics is a lightweight product, so it is important that everything loads quickly—the dashboard, segmentation of the data, and all the cool stuff in the background. Customers don’t know what we’re doing in the background, but they know that they want a fast experience,” Saric added. Using ClickHouse, Plausible Analytics is able to serve even its largest customers with ease, including the biggest customer, with 150 million pages per month. “This would not have been possible previously, it would have crashed everything, it would not have been able to load.,” Saric said. “There would have been no chance we could have had that kind of customer.”


According to Täht, switching to ClickHouse was the best technical decision their team ever made. “Clickhouse is amazingly efficient, not just in terms of compute power needed but also the time that it saves us. It’s very easy to work with Clickhouse. It does exactly what we need and it does it exceptionally well. It’s one of those technologies that feels really simple to use but also has a rich feature set.”


“I don’t think we would be able to be where we are today without ClickHouse,” Saric said. “Without switching from Postgres, Plausible would not have all this growth and new customers.”


## **About Plausible** [\#](/blog/plausible-analytics-uses-click-house-to-power-their-privacy-friendly-google-analytics-alternative#about-plausible-)


Plausible Analytics is an open\-source project dedicated to making web analytics more privacy\-friendly. Our mission is to reduce corporate surveillance by providing an alternative web analytics tool which doesn’t come from the AdTech world.


Visit [plausible.io](https://plausible.io/) for more information or to start a free trial.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

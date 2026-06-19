# ClickHouse Community Meetup in Berlin on July 3, 2018


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Community Meetup in Berlin on July 3, 2018

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Jul 5, 2018 · 3 minutes readJust a few months ago Brenno Oliveira from Delivery Hero has dropped us an email saying that they want to host a meetup of ClickHouse community in their HQ and together we made it happen. Actually, renting a suitable room is one of the main limiting factors on how often ClickHouse meetups can happen worldwide and it was very kind of Delivery Hero to provide it for free. Bringing interesting speakers was the easy part as there are more and more companies adopting ClickHouse and willing to share their stories. Being an open\-source product has its advantages after all. About 50 people have shown up from 75 sign\-ups, which is way above the typical rate.


To get started Alexander Zaitsev from Altinity gave an overview of ClickHouse for those who are not that familiar with the technology yet. He was using use cases from his personal experience and their clients as examples. Here are [the slides](https://presentations.clickhouse.com/meetup16/introduction.pdf), unfortunately, no video this time.


Gleb Kanterov talking about the usage of ClickHouse for experimentation metrics at Spotify:


![2018-clickhouse-meetup-berlin-1.jpeg](/uploads/2018_clickhouse_meetup_berlin_1_5e03a97583.jpeg)
![2018-clickhouse-meetup-berlin-2.jpeg](/uploads/2018_clickhouse_meetup_berlin_2_0344da3b90.jpeg)
Spotify relies heavily on what Google Cloud Platform provides, but nevertheless found a spot in their infrastructure where only ClickHouse appeared to satisfy the requirements. Gleb Kanterov has demonstrated their approach to conducting experiments and measuring if they are worth being promoted to production solutions. Using ClickHouse has allowed them to build a framework scalable to thousands of metrics, which in the end makes them move even faster and break fewer things. Checking out [full slides](https://presentations.clickhouse.com/meetup16/spotify.pdf) is highly recommended and here are a few quotes:


- **Requirements**
	- Serve 100\-s of QPS with sub\-second latency
	- We know in advance what are queries and data
	- Maintain 10x metrics with the same cost
	- Thousands of metrics
	- Billions of rows per day in each of 100\-s of tables
	- Ready to be used out of the box
	- Leverage existing infrastructure as much as feasible
	- Hide unnecessary complexity from internal users
- **Why ClickHouse?**
	- Build proof of concept using various OLAP storages (ClickHouse, Druid, Pinot,...)
	- ClickHouse has the most simple architecture
	- Powerful SQL dialect close to Standard SQL
	- A comprehensive set of built\-in functions and aggregators
	- Was ready to be used out of the box
	- Superset integration is great
	- Easy to query using clickhouse\-jdbc and jooq


The last talk by Alexey Milovidov was pretty technical and mostly intended for a deeper understanding of what's going on inside ClickHouse, see [the slides](https://presentations.clickhouse.com/meetup16/internals.pdf). There were many experienced users in the audience who didn't mind staying late to hear that and ask very relevant questions. Actually, we had to leave the building way before people were out of topics to discuss.


If your company regularly hosts technical meetups and you are looking for interesting topics to talk about, ClickHouse might be in pretty high demand. Feel free to write ClickHouse team via [this form](https://clickhouse.com) if you are interested to host a similar event in your city and we'll find a way to cooperate and bring in other ClickHouse community members.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

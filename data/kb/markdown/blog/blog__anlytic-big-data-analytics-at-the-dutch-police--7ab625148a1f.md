# Anlytic.com \- Big\-Data Analytics at the Dutch Police


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Anlytic.com \- Big\-Data Analytics at the Dutch Police

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 1, 2025 · 7 minutes read
*In this interview, we enjoyed sitting down with [Anlytic.com](https://www.anlytic.com/) to delve into their experience with our ClickHouse and ClickHouse Cloud on AWS. We discussed the challenges they faced before discovering ClickHouse, the impact it has had on their data analytics, and how it has transformed the way their team operates. Their insights offer a firsthand look at how ClickHouse's speed, scalability, and flexibility drive innovation and efficiency in their organization. Enjoy this deep dive into their journey with ClickHouse, and perhaps find inspiration for your own data challenges.*



### Do you mind introducing yourself? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#do-you-mind-introducing-yourself)



My name is Martijn Witteveen. I am 28 years old, and I live with my wife in Amsterdam. After I was kicked out of high school, I started my first company selling energy contracts to businesses. During that time, I realized the need to have passion in what you do. That passion is needed to keep your energy levels as high as possible. Needless to say, selling energy contracts wasn't my passion. I finished high school and then started studying math at an applied university. I was surprised how good I was at this, and after a year, I continued studying Econometrics. After a year, I switched to a double bachelor's degree combining Econometrics with Business economics. During this time, I was an automation engineer, where, after 1\.5 years, I managed 13\+ engineers, wrote style guides for the company, and gave masterclasses in software development. 



### What is the origin story of the company or the team within the company? What problem are you solving? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#what-is-the-origin-story-of-the-company-or-the-team-within-the-company-what-problem-are-you-solving)



Although the automation engineering job was technically challenging, my passion lies in data. During COVID, I started freelancing as a data engineer. After six months, I was introduced to the National Police in the Netherlands. They had built a handful of dashboards for the Head of the Police and ministers in the parliament. They asked for my help to take these dashboards to production. While working on the data infrastructure, I realized a massive duplication of work was occurring. Not directly in this process, but the reporting flow, as the industry standard, has an enormous productivity issue. The de facto way of working is by pre\-building data assets to be used in dashboards. Then, these dashboards are stripped apart into separate Word documents, where, in turn, implications are discussed. If we look at that process and the communication flows required, we face two major issues. The first is that pre\-building data assets lack the flexibility required to make an extensive range of analyses. That means that instead of sharing data around an organization, we share insights on dashboards, for which in\-depth analysis requires another layer of building data assets. Previous BI tools are built upon that assumption. With the rise of ClickHouse this assumption is no longer required, but previous BI systems are still working under this assumption. We shouldn't distribute dashboards but the data itself. When we do this, a second issue arises: communication around the data itself. Copy and paste charts into Word documents to write reports disconnects those reports from the data itself. Resulting in a massive duplication of work. 




At Anlytic.com, we remove the data accessibility barrier by directly distributing data around an organization. With our reporting features, we keep this data connected in one place, which we are calling a Data Hub. 



### What is most important when you tell your, or your team’s, story? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#what-is-most-important-when-you-tell-your-or-your-teams-story)



We are going against all odds; we are creating a category in an established market in which our product functions as a substitute. And I love it! I genuinely believe that we can impact how companies are run in the future. 




### What requirements did you have for the database/store component(s) in your architecture? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#what-requirements-did-you-have-for-the-databasestore-components-in-your-architecture)


- By limiting pre\-processing of data, performance is our most significant barrier.
- On\-demand scaling of our database plays a large role in ad\-hoc advanced calculations
- To guarantee data quality, we wanted to stay as close as possible to a fully structured SQL database
- On\-premise option


### Discovery of ClickHouse \- how did you hear about it, and what made you excited to give it a try? What were your hesitations? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#discovery-of-clickhouse---how-did-you-hear-about-it-and-what-made-you-excited-to-give-it-a-try-what-were-your-hesitations)



> If we are looking at high\-performance database systems for these types of workloads, the only two options are ClickHouse and Snowflake. ClickHouse is significantly faster. Before ClickHouse, we were using Postgres. Here, we had one query that was taking 80\+ seconds to load. I tried everything to get the performance up for this query. When I switched to ClickHouse, the runtime dropped to 0\.3 seconds.



My most considerable hesitation was the majority of the application. One clear signal of this is the quality of the client libraries. We are using Golang, and the GitHub page already shows that they are not implementing the Golang standard database interface. This would and is resulting in much extra code on our side. But the performance is unprecedented and is worth it.



### How did you evaluate ClickHouse? How did ClickHouse perform against the alternatives considered? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#how-did-you-evaluate-clickhouse-how-did-clickhouse-perform-against-the-alternatives-considered)



As I mentioned before, the performance update when switching from Postgres was extreme. The same holds for the runtime of the data pipelines. At this moment, we are processing around 1 billion rows per month, reducing the cost of these pipelines significantly. 



### What alternative databases did you consider? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#what-alternative-databases-did-you-consider)



The main alternative was Snowflake. One major issue with Snowflake is the lack of an On\-Prem solution. Some of our clients run a complete Anlytic.com instance on their cloud for, them having the option to spin up ClickHouse ourselves saves us a lot of extra work.



### What were the considerations when weighing the use of cloud vs self\-managed ClickHouse? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#what-were-the-considerations-when-weighing-the-use-of-cloud-vs-self-managed-clickhouse)



The cloud instance has an excellent sleeping mode. This makes the cost go down significantly while still having a heavy instance running during working hours. As I said, we are using both self\-managed instances for our On\-Prem solution and the Cloud instance for our cloud\-hosted instances. 



### Can you share some quantitative metrics about ClickHouse's performance (e.g., ingest/query latency/overall data volumes/cost efficiency)? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#can-you-share-some-quantitative-metrics-about-clickhouses-performance-eg-ingestquery-latencyoverall-data-volumescost-efficiency)



We are still in the early stages. For now, we see that on our primary cloud instance, we read more than 1\.8TB per month. With over 90 billion rows monthly read. All with an average query time of around 0\.3 seconds.



### Looking forward, what's next for you (and your use of ClickHouse)? [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#looking-forward-whats-next-for-you-and-your-use-of-clickhouse)



Soon, we will add a managed ClickHouse option to Anlytic.com. Together with our managed databases, we will start writing data connectors. 




Next to managed databases, we are working on adding metrics and real\-time data to the system. 




My goal is to create predefined data hubs. For example, I want to make a SaaS data hub that connects to Stripe, a CRM, Google Analytics, and Application metrics. Then, we can combine Postgres for low data volumes and ClickHouse for large data volumes. 



### How would you describe ClickHouse in 3 words?  [\#](/blog/anlytic-big-data-analytics-at-the-dutch-police#how-would-you-describe-clickhouse-in-3-words--)


- Unprecedented Fast
- Heavyweight
- Flexible


Interested in learning more? [Watch Anlytic's Meetup presentation.](https://www.youtube.com/watch?v=NJ99IsdfMSs)

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

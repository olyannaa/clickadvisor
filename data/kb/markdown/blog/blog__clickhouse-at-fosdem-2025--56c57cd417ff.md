# ClickHouse at FOSDEM 2025: talks, tech, and a community dinner


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse at FOSDEM 2025: talks, tech, and a community dinner

![photo-tyler-hannan.jpeg](/_next/image?url=%2Fuploads%2Fphoto_tyler_hannan_250918fdc5.jpeg&w=96&q=75)[Tyler Hannan](/authors/tyler-hannan)Feb 25, 2025 · 5 minutes readThis year, ClickHouse made a strong showing at FOSDEM 2025, with several team members traveling to Belgium and multiple talks covering everything from powerful new JSON data types to the challenges of fuzzing databases. If you weren’t able to attend (or just want a recap), here’s what went down in Brussels.


## What is FOSDEM? [\#](/blog/clickhouse-at-fosdem-2025#what-is-fosdem)


For those unfamiliar, **FOSDEM** (Free and Open Source Developers' European Meeting) is one of the biggest open\-source conferences in the world. Every year, thousands of developers, engineers, and open\-source enthusiasts gather in Brussels to share knowledge, showcase projects, and engage in deep technical discussions. It's a place where open\-source software meets innovation, and where deep\-dive technical talks are the norm.


And this year, ClickHouse was **well represented**.


## The ClickHouse Talks [\#](/blog/clickhouse-at-fosdem-2025#the-clickhouse-talks)


### How We Built a New Powerful JSON Data Type for ClickHouse [\#](/blog/clickhouse-at-fosdem-2025#how-we-built-a-new-powerful-json-data-type-for-clickhouse)


JSON support is a hot topic for ClickHouse users, and at FOSDEM, we shared details about the **new JSON data type** we built. This talk covered **why** we introduced it, how it **differs from traditional JSON handling**, and what kind of performance benefits users can expect. If you're working with semi\-structured data at scale, this was a must\-watch.


**Speaker:** Robert Schulze


**Abstract:** JSON has become the lingua franca for handling semi\-structured and unstructured data in modern data systems. Whether it’s in logging and observability scenarios, real\-time data streaming, mobile app storage, or machine learning pipelines, JSON’s flexible structure makes it the go\-to format for capturing and transmitting data across distributed systems.


At ClickHouse, we’ve long recognized the importance of seamless JSON support. But as simple as JSON seems, leveraging it effectively at scale presents unique challenges. In this talk we will discuss how we built a new powerful JSON data type for ClickHouse with true column\-oriented storage, support for dynamically changing data structure and ability to query individual JSON paths really fast.


Links related to the topic:


- [RFC: Semistructured Columns \#54864](https://github.com/ClickHouse/ClickHouse/issues/54864)
- [Implement Variant data type \#58047](https://github.com/ClickHouse/ClickHouse/pull/58047)
- [Implement Dynamic data type \#63058](https://github.com/ClickHouse/ClickHouse/pull/63058)
- [Implement new JSON data type. \#66444](https://github.com/ClickHouse/ClickHouse/pull/66444)



### Fuzzing Databases is Difficult [\#](/blog/clickhouse-at-fosdem-2025#fuzzing-databases-is-difficult)


Database reliability and security are always important priorities, and fuzz testing is one way to uncover hidden bugs. But as it turns out, **fuzzing databases is hard**. This talk dove into the complexities of fuzz testing, why traditional approaches don't always work well for databases, and what strategies can improve effectiveness. If you’re interested in database internals or security, this one was for you.


**Speaker:** Pedro Ferreira


**Abstract:** After fuzzing databases for the last 3 years, I learned that simple design decisions on a fuzzer impact on the issues it can ever find. In this talk I would to address some of those decisions. As an example, I would to discuss about the design of BuzzHouse, a new database fuzzer to test ClickHouse.


Links related to the topic:
[First iteration of Buzzhouse \#71085](https://github.com/ClickHouse/ClickHouse/pull/71085)



### \*\* rDNS Map: The Internet in Your Hands\*\* [\#](/blog/clickhouse-at-fosdem-2025#-rdns-map-the-internet-in-your-hands)


Reverse DNS (rDNS) is an often\-overlooked but powerful tool for understanding the structure of the internet. This talk explored how we can **map out rDNS data** at scale and why it's useful for network monitoring, security research, and even performance optimization.


**Speaker:** Alexey Milovidov


**Abstract:** I've created an rDNS map, available at <https://reversedns.space/>, and I want to tell you how. It was not hard to do, but there was a lot of unusual and amusing stuff in the process.



## Wrapping Up with a Community Dinner [\#](/blog/clickhouse-at-fosdem-2025#wrapping-up-with-a-community-dinner)


Of course, no ClickHouse event is complete without some time with the community. After a full day of talks, we gathered with our community members for dinner and drinks in Brussels. It was a chance to meet users, discuss database internals, and share ideas over great food and drinks. If you were there, thanks for joining us! If not, we hope to see you at the next one.


In the meantime, feel free to join us on [Slack](https://clickhouse.com/slack) or give the [ClickHouse repository](https://github.com/ClickHouse/clickhouse) a star.


## Some Photos [\#](/blog/clickhouse-at-fosdem-2025#some-photos)


![FOSDEM_Robert.png](/uploads/FOSDEM_Robert_7ae18824d8.png)
![FOSDEM_Pedro.png](/uploads/FOSDEM_Pedro_281eabed62.png)
![FOSDEM_Alexey.png](/uploads/FOSDEM_Alexey_f71f4433fb.png)
![FOSDEM_Room_Full.png](/uploads/FOSDEM_Room_Full_42d27aab9b.png)
![FOSDEM_Dinner_Venue.jpg](/uploads/FOSDEM_Dinner_Venue_2d60dbbefb.jpg)
![FOSDEM_Dinner_Full.jpg](/uploads/FOSDEM_Dinner_Full_bbae49afa6.jpg)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

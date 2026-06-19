# Transforming Ad Tech: How Cognitiv Uses ClickHouse to Build Better Machine Learning Models


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Transforming Ad Tech: How Cognitiv Uses ClickHouse to Build Better Machine Learning Models

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 6, 2024 · 8 minutes read![Cognitive - yellow.png](/uploads/Cognitive_yellow_328a90384a.png)
Since 2015, Cognitiv has used deep learning to optimize real\-time bidding on advertising opportunities. Its Deep Learning Advertising Platform sees millions of opportunities every second. As web pages load and ad space becomes available, Cognitiv’s algorithms explore these opportunities and bid on behalf of clients, optimizing performance based on KPIs.


At the core of Cognitiv’s success are the sophisticated machine learning models that power their bidding algorithms. These models rely on massive volumes of data, which must be efficiently managed, processed, and analyzed to allow Cognitiv’s data team to quickly iterate.



> “Anyone who’s done any machine learning will tell you that data is the most important part of the model,” says engineer Jason Ruckman. “Architecture is one thing. But it’s your data that really matters.”


Cognitiv transformed its approach to data management, integrating ClickHouse in an effort to improve performance and simplify operations. The implementation has not only allowed Cognitiv to handle their massive data volumes with ease; it has empowered their data team to develop more advanced machine learning models, solidifying the company’s position as a leader and innovator in programmatic ad buying.


## A More Efficient Offline Feature Store [\#](/blog/transforming-ad-tech-how-cognitiv-uses-clickhouse-to-build-better-machine-learning-models#a-more-efficient-offline-feature-store)


When someone visits a website, platforms like Cognitiv instantly analyze data to determine the best ad to display, using complex algorithms and machine learning to optimize targeting and bidding in real time. Training these models requires immense computational power and the ability to handle and analyze vast quantities of data quickly and efficiently.


When Jason joined Cognitiv in 2021, the company’s existing data solutions were costly and inefficient. Queries often took too long to complete, causing delays and driving up costs. The systems were also cumbersome to manage and required extensive maintenance and tuning. These shortcomings limited Cognitiv’s ability to experiment and improve their models, which are essential to their ad buying algorithms.



> “Data science as a discipline is not like engineering, where you can build in phases methodically,” Jason says. “Iteration time is incredibly key to a data science team workflow.”


In search of a better solution, the Cognitiv team began evaluating database systems that could power their [offline feature store](https://clickhouse.com/blog/powering-featurestores-with-clickhouse), important for engineering workflows in training new machine learning models. They considered several alternatives, but each of these solutions, while powerful, came with significant drawbacks. Namely, the high costs and added latency in data ingestion and queries were prohibitive at the scale Cognitiv required.


Finally, they discovered ClickHouse, an open\-source columnar database known for its lightning\-fast performance and efficiency. Jason says he was drawn to ClickHouse’s ability to handle large\-scale data ingestion and complex queries with minimal latency. Its background as an ad tech product also meant it came with features that were relevant to Cognitiv’s use case. Most importantly, it promised major cost savings due to its efficient use of resources.


“As a smaller company with large datasets, cost is important to us,” Jason says. “ClickHouse is fast, but its real value is in letting us better utilize our resources. Basically, we don’t need to spend as much money to solve the same problem.”


## Building a Proof of Concept [\#](/blog/transforming-ad-tech-how-cognitiv-uses-clickhouse-to-build-better-machine-learning-models#building-a-proof-of-concept)


In September of 2021, the Cognitiv team kicked off a proof of concept (POC) phase. They began by setting up a small ClickHouse cluster to test its capabilities. The POC focused on a specific use case: finding data that matched certain patterns. This involved scanning large datasets and performing complex joins, which Jason says “wasn’t really feasible” with their previous architecture and database management systems.



> The reason ClickHouse was good for this is because we would have very large histories of data and we might be interested in a specific sequence over a long period of time, but only for a few identifiers.”


Jason explains. He suspected ClickHouse’s indexing structures and data compression capabilities would make it an ideal fit for this particular use case, allowing them to perform these operations much more quickly and accurately.


He was right. ClickHouse was able to efficiently process queries that previously had taken hours or even days to complete. This was hugely valuable for Cognitiv’s data team, allowing them to rapidly iterate and refine their machine learning models. The team was particularly impressed with ClickHouse’s ability to maintain high performance even as data volumes increased.


The successful POC suggested that ClickHouse could meet Cognitiv’s needs not just for this specific use case, but across their entire data infrastructure.


## Transitioning to ClickHouse Cloud [\#](/blog/transforming-ad-tech-how-cognitiv-uses-clickhouse-to-build-better-machine-learning-models#transitioning-to-clickhouse-cloud)


The original POC cluster continued to grow throughout 2022\. By the end of the year, the Cognitiv team had identified more use cases where ClickHouse could be beneficial, deciding to fully transition to ClickHouse. They built their own production cluster using the Kubernetes operator. While this setup worked well, it came with its own set of challenges.


“The issue is upgrading it, scaling it, managing the hardware outlays, all that kind of stuff,” Jason says. “And when you’re running into bugs on a Kubernetes operator, you’re on our own. You’ve got to figure it out yourself. At a certain point, we got tired of it.”


While the ClickHouse team was in the process of [building ClickHouse Cloud](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year), Cognitiv began weighing the potential benefits of a managed service. They waited until January of 2024, after the cloud service’s official release on AWS, to make the switch.


Not wanting to run two parallel clusters, Jason knew that one of the main challenges would be ensuring that Cognitiv’s vast amounts of data — around two petabytes — could be migrated smoothly into ClickHouse Cloud without disrupting ongoing operations.



> “We knew it was going to be a live\-fire exercise,” he says. “The product and engineering teams at ClickHouse were really responsive. We didn’t expect them to get it perfectly right out of the gate. All you can ask is that they work hard on your behalf, which they did.”


Cognitiv’s move to ClickHouse Cloud paid off. From a business standpoint, it resulted in better efficiency and streamlined operations. For the data team specifically, it alleviated the challenges of managing their own database, allowing them to iterate faster and focus on Cognitiv’s core business: delivering the best AI\-powered advertising solution on the market.


## The Road Ahead [\#](/blog/transforming-ad-tech-how-cognitiv-uses-clickhouse-to-build-better-machine-learning-models#the-road-ahead)


![Quote.png](/uploads/Quote_994997f0ef.png)
Cognitiv has ambitious plans to expand their use of ClickHouse. They’re currently redesigning their schema to optimize data storage and processing capabilities. From there they plan to explore more of ClickHouse’s features and advanced functionalities, including optimizing queries, reducing data volumes, and adopting ClickHouse for even more data science use cases, such as data exploration and preparation for building machine learning models.


“ClickHouse is the center of our data strategy,” Jason says. “It’s really fast and cost\-efficient, but most importantly it connects to everything. It’s really easy to get to all of our different data. If it’s out there, you can probably connect it to ClickHouse. That’s super helpful for us.”


Jason is quick to praise the service he’s received from ClickHouse, especially his team’s experience onboarding ClickHouse Cloud. “The support team has been awesome,” he says. “It’s nice having someone to call when we need help.” The managed service has taken a lot of work and stress off his team’s collective plates, freeing them up for higher\-value activities like improving their models and delivering a better experience for clients.


“With ClickHouse, you already have this great core technology and a great surrounding ecosystem,” Jason says. “But with ClickHouse Cloud what you’re getting is an excellent support team, an excellent engineering team, and an excellent product team. That’s what has really helped us.”


By transitioning to ClickHouse, Cognitiv has streamlined their data processing and made operations more user\-friendly. With a focus on continuous improvement and innovation, Cognitiv is well\-positioned to maintain its position as leaders in programmatic ad buying, delivering value to its clients through cutting\-edge technology and expert data management.


To find out how ClickHouse Cloud can benefit your business, [sign up for a free trial](https://clickhouse.com/cloud).

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_partner_advertising_and_marketing_technology_f168923363.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

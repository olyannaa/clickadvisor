# OpenMeter \- How we learned ClickHouse and became certified ClickHouse Developers


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# OpenMeter \- How we learned ClickHouse and became certified ClickHouse Developers

![](/_next/image?url=%2Fuploads%2Fmark_openmeter_2d9f17caf8.jpg&w=96&q=75)Márk Sági\-KazárJun 11, 2024 · 8 minutes readClickHouse is at the heart of [OpenMeter](https://openmeter.io/)'s architecture, serving our customers' real\-time usage metering needs with remarkable efficiency and reliability. Although we've been leveraging ClickHouse for a while, I only recently had the time to complete the official ClickHouse Developer training.


I'd like to share my experience completing the training and becoming a certified ClickHouse Developer in this post.


## Why Learn ClickHouse? [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#why-learn-clickhouse)


ClickHouse is an excellent fit for real\-time data and analytics. It is one of the fastest\-growing databases, powering production use cases at Cloudflare, Netflix, OpenMeter, and many more. Even if you don't have a use case today, it's worth learning ClickHouse to familiarize yourself with a columnar database.


Most software engineers use some database during their careers. Often, it's a relational database management system (RDBMS) like Postgres, a document store like MongoDB, or, occasionally, a graph database. ClickHouse, as a columnar database, stands out from all of these.


While most databases are designed to model data, store, and manage state, ClickHouse's real power lies in its ability to analyze large datasets quickly. In today's fast\-paced, data\-driven world, businesses base their decisions on all the information they accumulate.


So, even if you don't need ClickHouse today and never will in your current job, you will likely encounter use cases where it excels. Even if ClickHouse is not your solution, it is an excellent model for effectively teaching you how to work with large datasets. Learning ClickHouse can also broaden your understanding of database technologies and enhance your data handling skills, preparing you for a wide range of challenges in data analytics.


If that doesn't convince you, I have one last argument: ClickHouse is fun. It's easy to run locally, load in some data, and run analytical queries against it.


I highly recommend you give it a shot.


## How not to learn ClickHouse? [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#how-not-to-learn-clickhouse)


When I first encountered ClickHouse, I thought, "SQL, but column\-oriented. Gotcha…" Which put me on the wrong course first. While the familiar syntax helps initially, there are fundamental differences between ClickHouse and relational databases like Postgres. It's important to keep an open mind about these differences and prepare yourself to redefine some of the concepts you've learned and understood in other database management systems.


For example, primary keys, indices, and table alterations work differently in ClickHouse. Understanding these nuances is crucial for leveraging ClickHouse's full potential.


With that out, let's move on to how to get started with ClickHouse.


## How to get started? [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#how-to-get-started)


The ClickHouse team offers several resources to help you learn ClickHouse effectively.


The obvious starting point is the documentation, where you can read about the basic concepts. The documentation is excellent, and that's where I began my journey with ClickHouse. [ClickHouse training](https://clickhouse.com/learn) is another great resource I can't recommend enough.


ClickHouse offers two types of training:


1. **On\-Demand Training**: This allows you to learn at your own pace.
2. **Instructor\-Based, Live Training**: This provides a more interactive learning experience with a live instructor.


Both training options are free at the time of this writing.


Choose the one that better suits your learning style. I prefer tinkering with what I'm learning and taking the time to experiment, so I opted for the on\-demand training.


The on\-demand course consists of 12 modules. It starts by explaining the basic concepts of ClickHouse and walks you through everything you need to become an effective user. Each module includes a 15 to 30\-minute video lesson, followed by one or two hands\-on exercises, each taking about an hour.


It's been a while since I completed a training program like this, mostly because I often find it hard to stay engaged. However, I thoroughly enjoyed the ClickHouse training. It was easy to follow, and the explanations and examples provided by the instructor were beneficial.


I recommend starting by exploring the documentation and then checking out the training. Twelve hours is not that much, especially given its value.


## Tips for completing the training [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#tips-for-completing-the-training)


### Use ClickHouse Cloud [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#use-clickhouse-cloud)


The instructor recommends using [ClickHouse Cloud](https://clickhouse.cloud/) throughout the training, and I highly recommend the same. Although running ClickHouse locally is super easy, ClickHouse Cloud provides a few benefits that come in handy during the training.


First, the SQL console in ClickHouse Cloud is superior to the open\-source version. While you can use the CLI or any other GUI client, I found using the one in the Cloud easier. It also allows you to save your queries and revisit them later.


Some modules, especially those explaining sharding and replication, require more complex setups. While these setups are not impossible to achieve locally, they are probably not something you want to spend time on during your initial learning phase. Using the cloud, you get all that functionality without any additional effort.


ClickHouse offers a free trial that is more than enough to complete the training, so it doesn't cost you anything to get started.


### The documentation is your friend [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#the-documentation-is-your-friend)


The [documentation](https://clickhouse.com/docs) was excellent and helpful during the training in multiple ways.


First, it provides additional information on the topics discussed in the training modules. After reviewing the documentation and reading the relevant sections, I found they were helpful in each lesson. Although the instructor gave excellent explanations, the additional context helped me better understand how ClickHouse works.


The documentation also proved helpful during the hands\-on labs. I'm slow at learning new syntaxes, so I kept the SQL reference open in a tab to quickly switch to it and search for the keyword or the function I needed to use.


### Take a break from time to time [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#take-a-break-from-time-to-time)


It might be tempting to grind through all twelve modules in one go. I did that with a few modules, which later proved wrong.


Give the new information time to settle in your mind, especially when completing modules explaining familiar concepts (like primary keys) that work differently in ClickHouse.


Take a few minutes or even an hour between modules. It's a marathon, not a sprint.


## Taking the certification exam [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#taking-the-certification-exam)


ClickHouse [recently announced](https://clickhouse.com/blog/first-official-clickhouse-certification) its first certification exam for the ClickHouse Developer course days after I completed it, so naturally, I also took the exam.


Overall, the exam is not challenging. The tasks I had the most difficulty with required analytical queries, mainly because ClickHouse is still relatively new to me. It has many functions you can't find in other SQL databases, and I'm not great at remembering names.


Here are some tips that may help you get through the exam successfully.


### Be comfortable with the documentation [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#be-comfortable-with-the-documentation)


Unless your superpower is memorizing function definitions and syntax, consider becoming comfortable with navigating the documentation. Knowing where to look for a specific function is often faster than using the search. It certainly isn't mine, so I usually refer to the documentation during the exam.


### Go through the lab solutions one more time [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#go-through-the-lab-solutions-one-more-time)


It shouldn't come as a surprise, but the exam relies heavily on what you've learned during the course. Although the examples and datasets are different, the types of questions are very similar to the lab exercises. So, even if you don't go through the labs again as practice, check out the code samples to prepare for what to expect during the exam.


### Read through all the tasks first [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#read-through-all-the-tasks-first)


This may feel cliché, but I strongly recommend reading through all the tasks and solving the easy ones first. Doing so will allow you to spend more time on the difficult ones (yes, some are more difficult than others). This approach also helps reduce pressure if you're short on time.


## Conclusion [\#](/blog/how-to-learn-clickhouse-and-become-a-certified-clickhouse-developer#conclusion)


These tips will help you succeed in learning ClickHouse (and completing the certification). Most importantly, I hope you will have as much fun as I did.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

# Langfuse and ClickHouse: A new data stack for modern LLM applications


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Langfuse and ClickHouse: A new data stack for modern LLM applications

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 23, 2025 · 8 minutes readBuilding an AI demo application is easy, but making it work reliably is hard. Open\-ended user inputs, model reasoning, and agentic tool use require a new workflow to iteratively measure, evaluate, and improve these systems as a team.


[Langfuse](https://langfuse.com/) helps developers solve that problem. Its open\-source LLM engineering platform gives teams the tools to trace, evaluate, and improve performance, whether they’re debugging prompts, testing model responses, or analyzing billions of interactions.


For companies working with sensitive or large\-scale data, part of Langfuse’s appeal lies in its flexibility: it can be self\-hosted or used as a managed cloud service. This flexibility helped Langfuse gain early traction with large enterprises—but it also created a scaling challenge. By mid\-2024, the simple Postgres\-based architecture that powered both their cloud and self\-hosted offerings was under pressure. The platform was handling billions of rows, fielding complex queries across multiple UIs, and struggling to keep up with rapidly scaling customers generating massive amounts of data. Something had to change.


At a [March 2025 ClickHouse meetup in San Francisco](https://www.youtube.com/watch?v=AnghkoucpN0), Langfuse co\-founder Clemens Rawert shared how the team [re\-architected their platform](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution) with ClickHouse as the “centerpiece” of their data operations. He also explained how they rolled out that change to thousands of self\-hosted users, turning a major infrastructure change into a win for the entire community.


## Too much data, too fast [\#](/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications#too-much-data-too-fast)


Langfuse launched in March 2023 with a lightweight, developer\-friendly setup: a single Docker container backed by a Postgres database. “That simple architecture allowed us to get off the ground quickly and prove we had something people wanted to use in those early days of working with LLMs,” Clemens says.


While many early users opted for Langfuse Cloud, the team was surprised to find that a growing number of larger enterprises, including those in regulated industries, chose to self\-host the open\-source version. The platform’s MIT license, combined with rising interest in LLM infrastructure, made Langfuse an attractive choice for teams that needed observability but couldn’t send data outside their own environments, Clemens explains.


![Langfuse User Story 01.png](/uploads/Langfuse_User_Story_01_8f94e0a3f0.png)
Langfuse’s original Postgres\-based data architecture struggled to scale as demand grew.


But that wave of adoption brought new challenges. As more companies integrated Langfuse into their production workflows, ingestion volumes surged. A handful of rapidly scaling customers were putting increasing strain on the Postgres backend. “Like many data\-heavy industries, ours is very outlier\-driven,” Clemens says.


The demands on the system were growing in every direction. Langfuse was handling billions of rows, with high I/O and traces that updated frequently as LLM processes unfolded. The same underlying data was being accessed through multiple UIs: single trace views, real\-time charts, dashboards, and a metrics API that aggregated hundreds of millions of traces. As usage patterns grew more complex, the original architecture struggled to keep up.


“My co\-founder and CTO Max started losing a lot of sleep,” Clemens says. “We knew we had to do something.”


## A new foundation with ClickHouse [\#](/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications#a-new-foundation-with-clickhouse)


By the summer of 2024, the team had reached a crossroads. “We had to decide whether to continue with Postgres and try to make it work with extensions and optimizations, or go for an OLAP database straight away,” Clemens says.


ClickHouse quickly emerged as an ideal fit. With its [columnar architecture](https://clickhouse.com/docs/en/faq/general/columnar-database), it offered the performance and scalability Langfuse needed to handle their growing workloads. It also came highly recommended by peers at PostHog and Better Stack. “They really advised us to go for ClickHouse,” Clemens says. “We haven’t regretted that decision.”


While Clemens already had a high degree of trust in ClickHouse as a “super modern database,” the availability of [ClickHouse Cloud](https://clickhouse.com/cloud) made the transition even easier. “Our experience with ClickHouse Cloud has been really great,” he says. “The support team is amazing.” Regional deployments and managed backups were especially valuable given Langfuse’s global user base and growing enterprise footprint.


Over the next six months, Langfuse rebuilt its platform around ClickHouse. The new architecture uses Redis for caching, S3 for storing large payloads, and an async event processor to handle high\-ingestion workloads. ClickHouse sits at the center of it all, powering everything from trace storage to complex analytics.


![Langfuse User Story 02.png](/uploads/Langfuse_User_Story_02_4933d11743.png)
Langfuse’s new ClickHouse\-based architecture is built for performance and scale.


“We’ve come a long way,” Clemens says, reflecting on the new setup. With a strong foundation built around ClickHouse, they have the architecture they need for scalable, long\-term growth.


## Supporting the self\-hosted community [\#](/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications#supporting-the-self-hosted-community)


Of course, rebuilding their own architecture was only one part of the equation. “We weren’t just doing this for our own service,” Clemens explains. The shift to ClickHouse would also have major implications for Langfuse’s [self\-hosted](https://langfuse.com/self-hosting) users. Thousands of teams were running Langfuse in their own environments, many in production. A change to the database backend meant Langfuse had to roll it out carefully, without disrupting those deployments.


The first step was communication. The team published an open [GitHub discussion](https://github.com/orgs/langfuse/discussions/1902) in April 2024, outlining their plans and inviting feedback. Over the next several months, the thread grew to more than 120 comments as they shared updates, explained their reasoning, and responded to community questions. “We communicated very early, transparently, and frequently about what we were planning to do and how Langfuse was going to change," Clemens says.


They also invited key users into a private focus group and released early versions for testing. When the official version shipped in December 2024, Langfuse provided a guided migration experience with a UI and background script to help users move from Postgres to ClickHouse without downtime. “A bunch of our users really appreciated that,” Clemens says.


Adoption of the new version, Langfuse v3, has been swift and promising. As of March 2025, more than a thousand self\-hosted deployments are running ClickHouse in production. “Some of our largest users ingest billions of rows,” Clemens says. “They told us they expected this migration to be a nightmare, but in the end, they were very happy.”


## Making ClickHouse easy to adopt [\#](/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications#making-clickhouse-easy-to-adopt)


As part of the shift to ClickHouse, the Langfuse team also had to rethink how new users, especially self\-hosted ones, would get up and running. Compared to Postgres, ClickHouse introduces a few new moving parts, and some teams were naturally hesitant about managing a more involved database setup. “There are definitely some concerns when you roll out a new database that’s not as familiar for developers,” Clemens says.


To ease the transition, Langfuse created what Clemens calls a “menu” of [options](https://langfuse.com/self-hosting/infrastructure/clickhouse) tailored to different use cases. For small\-scale or proof\-of\-concept deployments, they recommend running Langfuse with Docker Compose on a virtual machine. This setup is easy to spin up and suitable for teams ingesting fewer than a million traces per month. For production use, Langfuse provides Helm charts and deployment templates for AWS, Azure, and GCP.


For teams that want a managed experience, Langfuse points users to ClickHouse Cloud (“It’s amazing; we use it ourselves,” Clemens says) or ClickHouse’s [Bring Your Own Cloud (BYOC)](https://clickhouse.com/cloud/bring-your-own-cloud) offering, where the ClickHouse team operates the instance within the customer’s own cloud environment. The latter, Clemens says, is “super attractive for enterprises that want to keep data in their own perimeter.” And of course, Langfuse Cloud remains an option for customers who want a fully hosted solution.


This flexibility has made it easier to onboard companies of all sizes, whether they’re spinning up a quick internal test or preparing to ingest billions of rows in production.


## A data stack built for growth [\#](/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications#a-data-stack-built-for-growth)


Langfuse’s move to Clickhouse marks a turning point in how the company supports its users, both in the cloud and in self\-hosted environments. By rebuilding around a faster, more scalable database and offering flexible deployment options, the platform can handle enterprise\-scale LLM workloads without losing the ease of adoption that made it popular in the first place.


With ClickHouse as the centerpiece, Langfuse is now better equipped to grow alongside its community. Whether teams want a plug\-and\-play cloud service or the control of hosting in their own environment, they can count on the same architecture powering Langfuse’s own infrastructure—built for scale, proven in production, and ready to grow.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

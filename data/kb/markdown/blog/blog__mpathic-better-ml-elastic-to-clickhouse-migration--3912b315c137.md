# How mpathic built better ML workflows by switching from Elasticsearch to ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How mpathic built better ML workflows by switching from Elasticsearch to ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 10, 2025 · 7 minutes readBringing a new drug to market is a decade\-long highwire act. From preclinical animal studies to three phases of human trials to FDA review and approval, the process can cost healthcare and life sciences companies billions of dollars. A single rejection on the grounds of bias or misconduct can derail years of progress.


That’s exactly the kind of scenario [mpathic](https://mpathic.ai/) works to prevent. It uses AI to analyze thousands of hours of therapy sessions, flagging issues before they jeopardize a trial. “How do you ensure safety and compliance?” says Caraline Bruzinski, Senior Machine Learning Engineer. “You could hire a bunch of people to listen in. Or you could work with our company.”


Founded in 2021, the 20\-person, pre\-Series A startup is focused on two outcomes. “One is patient safety—we want to ensure the patient’s being treated well and there’s no misconduct,” Caraline says. “The other is compliance—making sure therapists are saying the things they’re required to say when administering drug trials and speaking with patients.”


At a [July 2025 ClickHouse meetup in New York](https://clickhouse.com/videos/meetupny_July2_2025), Caraline described the challenges of modeling noisy clinical conversations, why Elasticsearch and EC2\-based pipelines were holding the team back, and how switching to [ClickHouse Cloud](https://clickhouse.com/cloud) helped them build faster, leaner ML workflows.


## The reality of clinical data [\#](/blog/mpathic-better-ml-elastic-to-clickhouse-migration#the-reality-of-clinical-data)


When people hear “therapy session,” they often picture the version we see in movies and TV—clean back\-and\-forth dialogues ala Robin Williams and Matt Damon in *Good Will Hunting* or Tony Soprano’s sessions with Dr. Jennifer Melfi.


The reality is far messier. “There’s people crying, asking for tissues. There’s background music with people singing in the background. We’ve had sessions where the recorder was covered, so you can’t really hear it for eight hours,” Caraline says. These aren’t calm, linear conversations. They’re unpredictable, emotional interactions captured on imperfect equipment.


That noise makes every downstream step harder. “Before we can figure out *what* was said, we have to figure out *who* was talking at any given time,” she says. Was it the therapist hitting a compliance checkpoint, or the patient reacting emotionally? Sorting that out means running speaker segmentation and fingerprinting on thousands of hours of raw audio, then layering transcription and classification models on top.


From raw audio to transcription to model training to analytics, mpathic’s pipeline is designed to answer a deceptively simple yet high\-stakes question: did the therapist say what they were supposed to? The outcome can make or break a decade\-long, billion\-dollar trial.


## The pains of Elasticsearch [\#](/blog/mpathic-better-ml-elastic-to-clickhouse-migration#the-pains-of-elasticsearch)


Before moving to ClickHouse, mpathic was running its ML pipelines on Elasticsearch. But as Caraline explains, that setup presented a number of problems.


“You obviously can’t do joins, which made it difficult to understand trends or relationships in our data,” she says. The team often had to pull data down into local databases just to run aggregations. “It was a really miserable experience.”


Experimentation was just as unwieldy. Each new test meant spinning up an EC2 instance and rebuilding pandas environments from scratch—a process that took 10 minutes before any real work began. Developers would spend 60% of their time just running data jobs. “It was a lot of time and waiting,” Caraline says. “And you have to pay for that.”


For a lean startup, the “real cost” went beyond wasted hours and pricy compute bills. “It honestly just killed our ability to innovate,” she says. “We were not happy developers.”


If nothing else, the experience clarified what they *did* want in a database. “We need the ability to build and manage complex ML pipelines fast,” Caraline says. They also wanted aggregate functions and a columnar store powerful enough to let them analyze data quickly without exporting it into other tools.


Just as important, the team needed a system that freed them from managing infrastructure. As Caraline puts it, “I want to innovate on the fly. We’re a small company of 20 people. I want something that just works, because I don’t want to be a DBA anymore.”


## Easier, smarter, and faster with ClickHouse [\#](/blog/mpathic-better-ml-elastic-to-clickhouse-migration#easier-smarter-and-faster-with-clickhouse)


The team first adopted [ClickHouse](https://clickhouse.com/cloud) as a simple data store, using it to build machine learning models off annotated transcripts. But as they dug deeper, they saw it could do much more. “We started to realize how useful the [aggregate functions](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference) are, and how it could help us with a lot of the analytical work we’re doing,” Caraline says. What began as a replacement for Elasticsearch evolved into what she calls the “backbone of all our ML infrastructure.”


ClickHouse lets them run tasks inside the database that previously required separate compute environments. “String extraction was the easiest thing ever to set up,” Caraline says. The same goes for aggregating labels across sessions and trials, or for undersampling datasets. “We can do these things directly in ClickHouse, so we don’t have to pay for additional compute. We don’t have to spin anything up or wait for it. We don’t even use EC2 instances anymore. That’s a really nice win for my team.”


The speed gains have been impressive, too. Pipelines that once dragged on for 15 minutes now complete in just four. Developers can experiment faster, run jobs in parallel, and spend time on modeling instead of waiting around for infrastructure. “We have faster pipelines, faster dev cycles,” Caraline says. “We can experiment in a flash.”


Maybe the biggest win: “ClickHouse helps us understand our data better.” With [joins](https://clickhouse.com/docs/guides/joining-tables) and clustering, they can do things like distinguish between confrontational data—patients swearing or lashing out—and more passive\-aggressive exchanges. That clarity feeds back into their models, making them smarter and more accurate. “It really acts as a central hub for ML,” Caraline says. “It’s what we use to do all our work.”


## “It lightens our stack and wallet” [\#](/blog/mpathic-better-ml-elastic-to-clickhouse-migration#it-lightens-our-stack-and-wallet)


Caraline and the team are exploring ways to push their data infrastructure even further. One priority is analyzing concept drift—how patterns in therapy data evolve over time—so models stay accurate as trials progress. They’re also planning to expand into multimodal analysis, combining transcripts with metadata, biomarkers, and eventually even the audio itself to build a fuller picture of patient\-therapist interactions.


As the company grows, ClickHouse will remain central to that vision. Caraline is especially excited about [integrating with ClickHouse MCP](https://clickhouse.com/blog/integrating-clickhouse-mcp), which she says could help the team “understand deeper, more advanced analysis for better clinical outcomes.”


Switching from Elasticsearch to ClickHouse has freed engineers from constant infrastructure chores and simplified how they run ML pipelines. “We do all our pipelining through ClickHouse,” Caraline says. “It lightens our stack and wallet, and we’re using more and more aggregate functions as we get comfortable with them.”


Now, instead of babysitting systems, mpathic’s engineers can focus on the problems that matter most: improving patient safety and therapist compliance. As Caraline puts it: “I don’t have to think about DBA work, which is awesome for me, because it unblocks me and enables me to do more of my job effectively.”


Looking to make your data workflows leaner and faster? [Try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

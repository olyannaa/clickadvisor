---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-solarwinds-uses-clickhouse-byoc-for-real-time-observability-at-scale-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 5
---

# How SolarWinds uses ClickHouse BYOC for real\-time observability at scale \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"How SolarWinds uses ClickHouse BYOC for real\-time observability at scale","description":"Read about how SolarWinds leverages ClickHouse to process millions of telemetry messages per second, optimizing query performance for real\-time observability at scale.","image":"/uploads/Customer\_Story\_blog\_cover\_yellow\_1fe40b2c5c.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2025\-03\-11T16:03:36\.146Z","dateModified":"2026\-03\-03T12:30:39\.394Z","author":{"@context":"https://schema.org","@type":"Person","name":"Tony Burke, SolarWinds"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# How SolarWinds uses ClickHouse BYOC for real\-time observability at scale

![tony burke](/_next/image?url=%2Fuploads%2Ftony_burke_fb4882ba26.jpg&w=96&q=75)Tony Burke, SolarWindsMar 11, 2025 · 7 minutes readWhen software engineer Tony Burke joined SolarWinds in 2023, he brought nearly three decades of experience solving complex technical issues and architecting solutions for cloud and SaaS companies. But even with Tony’s expertise, the scale and high\-stakes nature of SolarWinds’ data operations posed a series of unique challenges.

For over 25 years, the Austin\-based company has been a leader in observability and IT management, serving more than 300,000 customers around the world. Its simple but powerful tools help IT teams monitor everything from servers and applications to Kubernetes clusters in real time, providing the insights they need to act quickly when systems falter.

Behind the scenes, SolarWinds processes 3 million telemetry messages per second, averaging 550 megabytes per second and peaking at bursts of a gigabyte. This relentless flow powers the real\-time dashboards and alerts that IT teams depend on to keep their infrastructure running smoothly. One of Tony’s first major tasks upon joining SolarWinds’ platform engineering team: make sure it could scale to meet demand without sacrificing performance.

At a [September 2024 meetup in Austin](https://www.youtube.com/watch?v=YB12NLAQG5U), Tony described how he and the team turned to ClickHouse to tackle these challenges. By fine\-tuning their system and optimizing queries for time\-sensitive metrics, SolarWinds built a data platform capable of scaling with speed and precision, handling millions of real\-time messages without missing a beat.

## The heat is on \#

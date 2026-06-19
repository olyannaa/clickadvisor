---
source: blog
url: https://en.wikipedia.org/wiki/Catalan_Atlas
topic: the-state-of-sql-based-observability
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 13
---

in this blog post, we will use the acronym SQL interchangeably to refer to the query language itself as well as its application in the OLAP use case. ## From dynamic systems to syslog and ... Twitter [\#](/blog/the-state-of-sql-based-observability#from-dynamic-systems-to-syslog-and--twitter)

Surprisingly, the observability roots are even older than SQL. The engineer Rudolf E. Kálmán [was the first](https://en.wikipedia.org/wiki/Observability) to use the term in the 1960s as a measure of how well the internal states of a system can be inferred from knowledge of its external outputs. The advent of computers and IT systems then led to a proliferation of monitoring and logging approaches. What I consider another major milestone happened in the 1980s with the advent of "syslog", developed by Eric Allman as part of the Sendmail project. In 1998, Joshua Weinberg described how to use syslog to centralize logs from heterogeneous systems to help system administrators in their daily tasks [with the help of a couple of Perl scripts](https://www.google.com/url?q=https://webcache.googleusercontent.com/search?q%3Dcache:VpVagABdgJQJ:mkweb.bcgsc.ca/intranet/sapj/html/v07/i10/a2.htm%26hl%3Den%26gl%3Des&sa=D&source=docs&ust=1701440627069514&usg=AOvVaw2aNqIveewPyIl_2WH9QrJ_). Thus, the idea of centralized logging was born, which would later become the first pillar of Observability. It’s worth noting that this initial approach was more focused on the mechanics of shipping logs in IT networks and didn’t address the question of storage, treating logs as plain files.

![img02.png](/uploads/img02_973757f66b.png)
Fast forward to 2013, when Twitter’s rapid growth was leading to unprecedented scalability challenges. This forced its engineering team to move fast, shifting away from a monolithic architecture to massively distributed systems, all while keeping the service up and running. Twitter captured their approach back then in the influential blog post ["Observability at Twitter"](https://blog.twitter.com/engineering/en_us/a/2013/observability-at-twitter.html):

*“It is the Observability team’s mission to analyze such problems with our unified platform for collecting, storing, and presenting metrics … As Twitter continues to grow, it is becoming more complex and services are becoming more numerous. Thousands of service instances with millions of data points require high\-performance visualizations and automation for intelligently surfacing interesting or anomalous signals to the user”*.

![hero.png](/uploads/img03_3abd8f5cd7.png)From: [https://blog.twitter.com/engineering/en\_us/a/2013/observability\-at\-twitter](https://blog.twitter.com/engineering/en_us/a/2013/observability-at-twitter)

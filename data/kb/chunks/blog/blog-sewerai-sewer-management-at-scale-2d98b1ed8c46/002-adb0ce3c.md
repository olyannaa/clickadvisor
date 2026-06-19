---
source: blog
url: https://www.sewerai.com/
topic: how-sewerai-is-using-clickhouse-to-modernize-sewer-management-at-scale
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 6
---

bad,” Sabrina jokes. “Somebody has to watch those videos and go, ‘Hey, there's a crack here, there's tree roots there. Wow, there’s a lot of water—hopefully just water—in this pipe. And what are all these rats doing here?’”

Municipalities rely on that footage to decide what to fix and when. But in an industry long underserved by technology, they’re often working with outdated systems. “We’ve seen DVDs, stacks of CDs, major cities still using fax machines,” Sabrina says. And with an aging workforce nearing retirement, the next generation isn’t exactly trained to handle a fax line.

SewerAI was founded in 2019 to fix this problem. As Sabrina puts it, the company’s founders asked, “Why do humans have to watch these videos? It’s really boring, and you have to identify consistent patterns. Sounds like a perfect job for AI, right?”

That's where [ClickHouse](https://clickhouse.com/cloud) came into the picture. “We had loads and loads of data, and we wanted to use it to train AI to identify problems in video,” Sabrina says. “That's what we started using ClickHouse for, and it works great.”

But as the team began digging in, it became clear the industry needed more than smarter video review. It needed a modern data platform. The team began building a full cloud\-based system for underground infrastructure management. They started with Postgres, an age\-old choice for transactional workflows. But when it came to analytics, it didn’t hold up.

“Say you're a city municipal worker,” Sabrina says. “You've got a meeting in half an hour, and based on the last nine months of data that you loaded into SewerAI, you need to make a case that you need more trucks. You don't have time to run a query across nine months of data and 40\-odd relational Postgres tables. You need your answers now.”

## Postgres to PeerDB to ClickPipes [\#](/blog/sewerai-sewer-management-at-scale#postgres-to-peerdb-to-clickpipes)

The first challenge was getting all that Postgres data into ClickHouse. Their initial setup used Confluent with Debezium and Kafka streams. “This worked fine—right up until we did our SOC\-2 compliance,” Sabrina says. “Then they said, ‘Nope, Confluent needs to go.’”

Plan B was to self\-host Debezium and use AWS Kinesis. “I do not recommend this solution,” she says. “It does not scale well, and you will spend a lot of time debugging your Debezium server.”

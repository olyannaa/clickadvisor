---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-26-2-clickhouse
ch_version_introduced: '26.2'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 10
---

# ClickHouse Release 26\.2 \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"ClickHouse Release 26\.2","description":"ClickHouse 26\.2 is here! In this post, text\-index and QBit data type become production\-ready.","image":"/uploads/Blog\_Cover\_1200x630\_49ceb5f5e1\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-03\-16T10:47:57\.285Z","dateModified":"2026\-03\-17T11:50:31\.823Z","author":{"@context":"https://schema.org","@type":"Person","name":"ClickHouse","url":"https://clickhouse.com/authors/clickhouse","@id":"https://clickhouse.com/authors/clickhouse\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 26\.2

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 16, 2026 · 17 minutes readAnother month goes by, which means it’s time for another release!

ClickHouse Winter Release contains 25 new features 🧤 43 performance optimizations 🛷 183 bug fixes ⛄

This release sees the text\-index and QBit data type become production\-ready. It’s also now possible to batch "infinite" inserts by time, and there are performance improvements for joins, JSON parsing, and inserts with min\-max indices.

## New contributors \#

A special welcome to all the new contributors in 26\.2! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.

Below are the names of the new contributors:

*4ertus2,Aaron Knudtson,AlyHKafoury,Andre Hora,Andrey Tarasov,Ashwath,Ben Wu,Christoph Viebig,Dan McCombs,Dmitry Kovalev,Dmitry Plotnikov,Federico Ginosa,Gerald Latkovic,Hasyimi Bahrudin,Ivan Gorin,Kien Nguyen Tuan,Mostafa Mohamed Salah,MyeongjunKim,Padraic Slattery,Rahul,Raquel Barbadillo,Visakh Unnikrishnan,daun\-gatal,dimbo4ka,dk\-github,jayvenn21,murphy\-4o,phulv94,sunyeongchoi,vanchaklar,Álvaro Niño*

Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).

You can also [view the slides from the presentation](https://presentations.clickhouse.com/2026-release-26.2/).

## Batching of "infinite" inserts by time \#

### Contributed by Mostafa Mohamed Salah \#

One of my favorite real\-time datasets is the Wikimedia recent changes feed, which streams changes across various Wikimedia properties.

You can see how it works by navigating to <https://stream.wikimedia.org/v2/stream/recentchange>. An example of an event is shown below:

```
1event: message
2id: [{"topic":"eqiad.mediawiki.recentchange","partition":0,"offset":-1},{"topic":"codfw.mediawiki.recentchange","partition":0,"timestamp":1772536525049}]
3data: {"$schema":"/mediawiki/recentchange/1.0.0","meta":{"uri":"https://commons.wikimedia.org/wiki/Category:Taken_with_Nikon_D3100","request_id":"55711a7f-6053-4592-97c4-45d54e6319f7","id":"9106b913-64f9-4dff-a325-ac43492cc81d","domain":"commons.wikimedia.org","stream":"mediawiki.recentchange","dt":"2026-03-03T11:15:25.048Z","topic":"codfw.mediawiki.recentchange","partition":0,"offset":2029032842},"id":3219900521,"type":"categorize","namespace":14,"title":"Category:Taken with Nikon D3100","title_url":"https://commons.wikimedia.org/wiki/Category:Taken_with_Nikon_D3100","comment":"[[:File:Ferrari 550 Maranello - Flickr - Alexandre Prévot (3).jpg]] added to category","timestamp":1772536523,"user":"Rkieferbot","bot":true,"notify_url":"https://commons.wikimedia.org/w/index.php?diff=1175166536&oldid=1019467923&rcid=3219900521","server_url":"https://commons.wikimedia.org","server_name":"commons.wikimedia.org","server_script_path":"/w","wiki":"commonswiki","parsedcomment":"File:Ferrari 550 Maranello - Flickr - Alexandre Prévot (3).jpg added to category"}
```
Copy command
Each event has three properties;

- `event` \- The event type, which is almost always `message`.
- `id` \- An identifier for the event.
- `data` \- A JSON object representing the change itself.

We can use cURL at the terminal to stream just the `data` part of each event:

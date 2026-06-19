---
source: blog
url: https://metrica.yandex.com/
topic: evolution-of-data-structures-in-yandex-metrica
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 10
---

vs. visitors from Moscow), change your set of metrics, etc. These features demanded a completely different approach to data storage than what we used with MyISAM, we will further discuss this transition from technical perspective. ## MyISAM [\#](/blog/evolution-of-data-structures-in-yandexmetrica#myisam)

Most SELECT queries that fetch data for reports are made with the conditions WHERE CounterID \= AND Date BETWEEN min\_date AND max\_date. Sometimes there is also filter by region, so it made sense to use complex primary key to turn this into primary key range is read. So table schema for Metrica looks like this: CounterID, Date, RegionID \-\> Visits, SumVisitTime, etc. Now we'll take a look at what happens when it comes in.

A MyISAM table is comprised of a data file and an index file. If nothing was deleted from the table and the rows did not change in length during updating, the data file will consist of serialized rows arranged in succession in the order that they were added. The index (including the primary key) is a B\-tree, where the leaves contain offsets in the data file. When we read index range data, a lot of offsets in the data file are taken from the index. Then reads are issued for this set of offsets in the data file.

Let's look at the real\-life situation when the index is in RAM (key cache in MySQL or system page cache), but the table data is not cached. Let's assume that we are using HDDs. The time it takes to read data depends on the volume of data that needs to be read and how many Seek operations need to be run. The number of Seek's is determined by the locality of data on the disk.

Data locality illustrated:
![Data locality](/en/2016/evolution-of-data-structures-in-yandex-metrica/1.jpg)

Metrica events are received in almost the same order in which they actually took place. In this incoming stream, data from different counters is scattered completely at random. In other words, incoming data is local by time, but not local by CounterID. When writing to a MyISAM table, data from different counters is also placed quite randomly. This means that to read the data report, you will need to perform about as many random reads as there are rows that we need in the table.

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Vector
topic: vector-search-with-clickhouse-part-2-clickhouse
ch_version_introduced: '0.33110910654067993'
last_updated: '2026-09-07'
chunk_index: 15
total_chunks_in_doc: 29
---

and search for conceptually similar results. To do so, we repeat the above query using the `text_embedding` column. The full embedding can be found [here](https://pastila.nl/?ffffffff/c764acc01aa4ab87b3a8fe5e40f8b4bc). ``` 1python generate.py --image images/ridgeback.jpg 2 3[0.17179889976978302, 0.6171532273292542, ..., -0.21313616633415222] ``` Copy command

```
1SELECT
2	url,
3	caption,
4	L2Distance(text_embedding, [0.17179889976978302, ..., -0.21313616633415222]
5) AS score
6FROM laion_10m WHERE similarity >= 0.2
7ORDER BY score ASC
8LIMIT 2
9FORMAT Vertical
10
11Row 1:
12──────
13url: 	https://i.pinimg.com/236x/ab/85/4c/ab854cca81a3e19ae231c63f57ed6cfe--submissive--year-olds.jpg
14caption: Lenny is a 2 to 3 year old male hound cross, about 25 pounds and much too thin. He has either been neglected or on his own for a while. He is very friendly if a little submissive, he ducked his head and tucked his tail a couple of times when I...
15score:   17.903361349936052
16
17Row 2:
18──────
19url: 	https://d1n3ar4lqtlydb.cloudfront.net/c/a/4/2246967.jpg
20caption: American Pit Bull Terrier/Rhodesian Ridgeback Mix Dog for adoption in San Clemente, California - MARCUS = Quite A Friendly Guy!
21score:   17.90681696075351
22
232 rows in set. Elapsed: 1.516 sec. Processed 9.92 million rows, 32.52 GB (6.54 million rows/s., 21.45 GB/s.)
```
Copy command
For convenience, we’ve provided a simple result generator [search.py](https://github.com/ClickHouse/laion/blob/main/search.py), which encodes the passed image or text and executes the query, rendering the query results as a local html file. This file is then automatically opened in the local browser. The result file for the above query is shown below:

```
1python search.py search --image images/ridgeback.jpg --table laion_10m
```
Copy command
![ridgebacks.png](/_next/image?url=%2Fuploads%2Fridgebacks_25a29f60f3.png&w=2048&q=75)

In both of these examples, we have matched embeddings for different [modals](https://en.wikipedia.org/wiki/Multimodal_learning), i.e. embeddings from image inputs are matched against the `text_embedding` column and vice versa. This aligns with the original model training as described earlier, and is the intended application. While matching input embeddings against the same type has been explored, previous attempts have resulted in [mixed results](https://github.com/openai/CLIP/issues/1).

## The benefits of SQL \#

Oftentimes, in practice with vector search, we don’t just search across embeddings. Frequently, there is additional utility in combining search with filtering or aggregating on metadata.

### Filtering with metadata \#

As an example, suppose we wish to perform vector search on images that are non\-copyrighted. This kind of query would combine vector search with filtering based on copyright metadata.

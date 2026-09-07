---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Analyzing
topic: analyzing-wimbledon-tennis-data-with-chdb-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 8
---

--path wimbledon.chdb ``` Copy command We’ll provide the `path` parameter so that any data we insert will be persisted to our local disk. ## Writing a function to compute the points needed to win a tennis game \#

Now that we’ve got ClickHouse up and running, it’s time to write a function to compute the points a player needs to win the game based on the current score.

The finalized function is shown below:

```
1CREATE OR REPLACE FUNCTION pointsToWinGame AS (p1Score, p2Score) -> 
2  multiIf(
3    p1Score = '40' AND p2Score = 'AD', 3,
4    p1Score = '40' AND p2Score = '40', 2,
5    p1Score = '40' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 1,
6    p1Score = '30' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 2,
7    p1Score = '30' AND p2Score = '40', 3,
8    p1Score = '15' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 3,
9    p1Score = '15' AND p2Score = '40', 4,
10    p1Score = '0' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 4,
11    p1Score = '0' AND p2Score = '40', 5,
12    p1Score = 'AD', 1,
13    0
14    );
```
Copy command
The function takes in the current game score for both players and returns the number of points the first player is away from winning the game.

For example, if the score is 15\-40, they would need to win four points \- two points to get the score back to 40\-40 and another two points to win the game.

We can call this function just like any other built\-in function, and I was initially testing the function by running it manually with various scores:

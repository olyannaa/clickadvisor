# Analyzing Wimbledon tennis data with chDB


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Analyzing Wimbledon tennis data with chDB

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Jul 3, 2025 · 10 minutes readThe 2025 Sinner\-Alcaraz final at Roland Garros perfectly captured tennis's razor\-thin margins. Sinner stood just one point from victory, with three championship points in the 4th set \- yet somehow saw the match snatched from his grasp, [as illustrated in Andy Marshall’s impressive animation](https://x.com/AndyMarshall86/status/1931993645378658533).


While watching Carlos Alcaraz's first\-round match at Wimbledon, I was reminded of Andy's animation. I had a hunch that Alcaraz was never truly in danger of losing despite going to five sets. But I wanted to see if the data would back up my intuition.


I initially tried to build something using AI coding assistants, but quickly ran into a wall. Neither Claude nor ChatGPT seemed to grasp tennis's unique scoring system. Their generated code simply didn't work, and even with my guidance, I found myself more frustrated than productive.


I was initially going to write something in Python, but then I thought, why not do it in ClickHouse instead?! Below is what I ended up with:


![2025-07-03_10-20-29.png](/uploads/2025_07_03_10_20_29_6a6a209642.png)

> Spoiler: Alcaraz was not really in any danger of losing!


## How the tennis scoring system works [\#](/blog/analyzing-wimbledon-2025-chdb#how-the-tennis-scoring-system-works)


We'll see how I built this, but first, we’ll review how the tennis scoring system works.


A match is best of 3 or best of 5 sets, which means you need to win 2 or 3 sets to win. In Grand Slam events, women’s matches are best of 3, and men’s are best of 5\.


The first player to reach six games wins the set. But if both players get to 5, you must get to 7 to win the set. If both players get to 6, they will play a tiebreak. The tiebreak will be the first to win 7 points unless it’s the final set, in which case it will be first to 10 points. And in both cases, you need to win by two clear points.


Now we get to the slightly trickier bit: the scoring of a game!


Each game starts at 0–0, and one player serves. The score goes up like this:


- First point: 15
- Second point: 30
- Third point: 40


Win the next point after 40, and you win the game \- but only if you're ahead by two points.


**What Happens at 40–40 (Deuce)?**  

If both players reach 40, that’s called deuce. From deuce, you need to win two points in a row to win the game:


- Win one point → you have Advantage (Ad).
- Win the next → you win the game.
- Lose the next → back to deuce.


This can go back and forth several times until someone wins two consecutive points from deuce.


## A brief introduction to clickhouse\-local [\#](/blog/analyzing-wimbledon-2025-chdb#a-brief-introduction-to-clickhouse-local)


Now we know how the scoring works, it’s time to start building something in ClickHouse. ClickHouse is best known for ClickHouse Server, which runs in the standard client/server architecture.


But running a server and connecting with a client seems like too much work when working on a project like this! Luckily, we can use clickhouse\-local, a standalone command\-line tool that provides the full functionality of ClickHouse without requiring you to run a server instance.


We download ClickHouse as usual:



```

```
1curl https://clickhouse.com  | sh
```

```

And then launch clickhouse\-local:



```

```
1./clickhouse -mn --path wimbledon.chdb
```

```

We’ll provide the `path` parameter so that any data we insert will be persisted to our local disk.


## Writing a function to compute the points needed to win a tennis game [\#](/blog/analyzing-wimbledon-2025-chdb#writing-a-function-to-compute-the-points-needed-to-win-a-tennis-game)


Now that we’ve got ClickHouse up and running, it’s time to write a function to compute the points a player needs to win the game based on the current score.


The finalized function is shown below:



```

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

```

The function takes in the current game score for both players and returns the number of points the first player is away from winning the game.


For example, if the score is 15\-40, they would need to win four points \- two points to get the score back to 40\-40 and another two points to win the game.


We can call this function just like any other built\-in function, and I was initially testing the function by running it manually with various scores:



```

```
1SELECT
2    p1 as player1_score,
3    p2 as player2_score,
4    pointsToWinGame(p1, p2) as points_to_win
5FROM VALUES(
6    'p1 String, p2 String',
7    ('0', '0'), ('0', '15'), ('0', '30'),
8    ('15', '30'),
9    ('30', '15'),
10    ('30', '40'),
11    ('40', '30'),
12    ('40', '40'),
13    ('AD', '40'),
14    ('0', '40'), ('15', '40'), ('30', '40'),
15    ('40', 'AD')
16);
```

```

This wasn’t a problem for this function as it’s relatively simple, but as I wrote other functions, I kept introducing bugs as I tried to get them working for different scoring scenarios.


I needed to write some automated tests that I could run against my functions to ensure they worked.


## Testing user\-defined functions with chDB [\#](/blog/analyzing-wimbledon-2025-chdb#testing-user-defined-functions-with-chdb)


One way to do this is to switch to ClickHouse Server and write tests that execute the function via one of the ClickHouse client libraries.


Alternatively, we could use [chDB](https://clickhouse.com/docs/chdb), a fast in\-process SQL OLAP Engine powered by ClickHouse, with Python, Go, Rust, NodeJS, and Bun language support.


One of the cool things about chDB is that it [works with databases created with clickhouse\-local](https://clickhouse.com/docs/chdb/guides/clickhouse-local). It should be reasonably easy to get everything wired up.


There are few enough combinations of scores to test all of them. I’m not a guru regarding the fanciest Python testing frameworks, so I’m using good old pytest.


Below is a [parameterized test](https://docs.pytest.org/en/stable/how-to/parametrize.html) that I wrote to check that the `pointsToWinGame` function works:



```

```
1from chdb import session as chs
2import pytest
3
4sess = chs.Session("wimbledon.chdb")
5
6@pytest.mark.parametrize("p1,p2,expected", [
7  ("'0'", "'40'", 5),
8  ("'0'", "'0'", 4),
9  ("'0'", "'15'", 4),
10  ("'0'", "'30'", 4),
11  ("'15'", "'40'", 4),
12  ("'15'", "'15'", 3),  
13  ("'15'", "'30'", 3),
14  ("'30'", "'40'", 3),
15  ("'40'", "'AD'", 3),
16  ("'30'", "'30'", 2),
17  ("'40'", "'40'", 2),
18  ("'40'", "'30'", 1),
19  ("'40'", "'15'", 1),
20  ("'40'", "'0'", 1),
21  ("'AD'", "'40'", 1),
22  
23])
24def test_points_to_win_normal_game(p1, p2, expected):
25    result = sess.query(f"""
26    SELECT pointsToWinGame({p1}, {p2}) as points
27    """, "DataFrame")
28
29    assert result["points"].values[0] == expected
```

```

At the top of the script, we initialize our chDB database, which points to the `wimbledon.chdb` directory, which has all the functions loaded.


If we come further down, we can see that our test takes in three parameters:


- `p1` \- The game score for the first player
- `p2` \- The game score for the other player
- `expected` \- The number of points for the first player to win the game


We can then run those tests using the [uv package manager](https://docs.astral.sh/uv/):



```

```
1uv run --with chdb pytest test_game.py
```

```


```
test_game.py .......................                                                                                                                                                                                                                                                   [100%]

===================================================================================================================================== 23 passed in 0.97s =====================================================================================================================================

```

I repeated this workflow of writing functions and tests to determine the number of points required to win the rest of the current and remaining sets.


We also have other functions, but we won’t go through each of those in turn \- instead, you can see their definitions and corresponding tests in the [wimbledon\-chdb](https://github.com/mneedham/wimbledon-chdb) GitHub repository.


We can write the following query to see a list of those functions:



```

```
1SELECT name
2FROM system.functions
3WHERE origin = 'SQLUserDefined';
```

```


```
┌─name─────────────────────┐
│ pointsToWinTiebreak      │
│ pointsToWinMatch         │
│ pointsToWinFinalSet      │
│ pointsToWinGame          │
│ pointsToWinSet           │
│ pointsToWinOtherSetsBO3  │
│ pointsToWinOtherSetsBO5  │
│ pointsToWinMatchTiebreak │
└──────────────────────────┘

```

## Storing tennis data in ClickHouse [\#](/blog/analyzing-wimbledon-2025-chdb#storing-tennis-data-in-clickhouse)


The [Wimbledon website](https://www.wimbledon.com/en_GB/scores/results/day10.html) has point\-by\-point data that we can use to explore matches and see how close Alcaraz was to losing his first\-round match.


We’ll first create a `matches` table that has a little bit of metadata about the match:



```

```
1CREATE TABLE matches
2(
3    p1Name String,
4    p2Name String,
5    match String,
6    event String
7)
8ENGINE = MergeTree
9ORDER BY match;
```

```

The `event` column indicates whether it’s a men’s or women’s match, so we know whether to use best\-of\-3 or best\-of\-5 scoring.



```

```
1SELECT * FROM matches LIMIT 3;
```

```


```
┌─p1Name─────────┬─p2Name───────────┬─match─┬─event─┐
│ Jannik Sinner  │ Luca Nardi       │ 1101  │ Men   │
│ Pedro Martinez │ George Loffhagen │ 1103  │ Men   │
│ Mariano Navone │ Denis Shapovalov │ 1104  │ Men   │
└────────────────┴──────────────────┴───────┴───────┘

```

Then, the following table, `points`, captures the points in those matches.



```

```
1CREATE TABLE points
2(
3    MatchWinner String,
4    SetWinner String,
5    GameWinner String,
6    p1 Tuple(setsWon UInt8, gamesWon UInt8, score String),
7    p2 Tuple(setsWon UInt8, gamesWon UInt8, score String),
8    ElapsedTime String,
9    PointNumber UInt16,
10    match String
11)
12ORDER BY match;
```

```

Each row contains all the data needed to determine how close a player is to winning \- we don’t need to consider any other rows. Below is the match point for Alcaraz:



```

```
1SELECT * 
2FROM points 
3WHERE match = '1164' AND MatchWinner <> '0
4FORMAT Vertical;
```

```


```
Row 1:
──────
MatchWinner: 2
SetWinner:   2
GameWinner:  2
p1:          (2,1,'0')
p2:          (3,6,'0')
ElapsedTime: 4:36:56
PointNumber: 357
match:       1164

```

## Computing points to win [\#](/blog/analyzing-wimbledon-2025-chdb#computing-points-to-win)


Now that we’ve loaded the data, we need to write the query to determine how many points a player is from victory. The query for Alcaraz’s first match is shown below:



```

```
1WITH
2  pointsToWinMatch(
3    matches.event = 'Men', MatchWinner, GameWinner, SetWinner, '1', p1.setsWon, p2.setsWon, p1.gamesWon, p2.gamesWon, p1.score, p2.score
4  ) AS p1PointsToWin,
5  pointsToWinMatch(
6    matches.event = 'Men', MatchWinner, GameWinner, SetWinner, '2', p2.setsWon, p1.setsWon, p2.gamesWon, p1.gamesWon, p2.score, p1.score
7  ) AS p2PointsToWin
8select PointNumber, p1Name, p1PointsToWin AS p1, p2PointsToWin AS p2, p2Name
9FROM points
10JOIN matches ON matches.match = points.match
11WHERE match = '1164'
12ORDER BY PointNumber;
```

```

The last five rows are shown below:



```
┌─PointNumber─┬─p1Name────────┬─p1─┬─p2─┬─p2Name─────────┐
│         353 │ Fabio Fognini │ 24 │  2 │ Carlos Alcaraz │
│         354 │ Fabio Fognini │ 23 │  2 │ Carlos Alcaraz │
│         355 │ Fabio Fognini │ 22 │  2 │ Carlos Alcaraz │
│         356 │ Fabio Fognini │ 23 │  1 │ Carlos Alcaraz │
│         357 │ Fabio Fognini │ 72 │  0 │ Carlos Alcaraz │
└─────────────┴───────────────┴────┴────┴────────────────┘

```

We can see Alcaraz closing in on victory until he has no more points left to win, and Fognini would need to play the whole match again to win!


## Visualizing proximity to victory with Streamlit and plot.ly [\#](/blog/analyzing-wimbledon-2025-chdb#visualizing-proximity-to-victory-with-streamlit-and-plotly)


Finally, I wanted to package this into a little app to explore different matches. I did this using Streamlit and [plot.ly](http://plot.ly). All the code is in the repository and was primarily written by ChatGPT with some tweaks.


You can run it locally using `uv`:



```

```
1uv run --with chdb --with plotly --with streamlit \
2streamlit run app.py  --server.headless True
```

```

Below is an animation of what the app looks like:


![2025-07-03_12-01-42 (1).gif](/uploads/2025_07_03_12_01_42_1_e33f0f1548.gif)
You can also play around with it by going to [wimbledon2025\.streamlit.app/](https://wimbledon2025.streamlit.app/)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

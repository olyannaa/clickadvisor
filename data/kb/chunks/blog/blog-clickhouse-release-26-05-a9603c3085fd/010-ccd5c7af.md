---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-26-5
ch_version_introduced: '26.5'
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 12
---

} 12}' AS conf 13SELECT JSON_VALUE(conf, ('$.name', '$.venue.name')); ``` ``` ``` ┌─JSON_VALUE(conf, ('$.name', '$.venue.name'))─┐ │ ('Open House 2026','Convene 100 Stockton') │ └──────────────────────────────────────────────┘ ``` We can also pass in the JSON paths as an array rather than a tuple:

```

```
1WITH '{
2  "name": "Open House 2026",
3  "tagline": "The real-time database for AI conference",
4  "dates": {
5    "workshops": "2026-05-26",
6    "conference": ["2026-05-27", "2026-05-28"]
7  },
8  "venue": {
9    "name": "Convene 100 Stockton",
10    "address": "40 O''Farrell St, San Francisco, CA 94108"
11  }
12}' AS conf
13SELECT JSON_VALUE(conf, ['$.name', '$.venue.name']);
```

```

```
┌─JSON_VALUE(conf, ['$.name', '$.venue.name'])─┐
│ ['Open House 2026','Convene 100 Stockton']   │
└──────────────────────────────────────────────┘

```

But `dates.conference` is an array, so if we try to retrieve that using `JSON_VALUE`, we’ll return an empty string:

```

```
1WITH '{
2  "name": "Open House 2026",
3  "tagline": "The real-time database for AI conference",
4  "dates": {
5    "workshops": "2026-05-26",
6    "conference": ["2026-05-27", "2026-05-28"]
7  },
8  "venue": {
9    "name": "Convene 100 Stockton",
10    "address": "40 O''Farrell St, San Francisco, CA 94108"
11  }
12}' AS conf
13SELECT JSON_VALUE(conf, ('$.name', '$.dates.conference'));
```

```

```
┌─JSON_VALUE(c⋯nference'))─┐
│ ('Open House 2026','')   │
└──────────────────────────┘

```

We can read the individual values from that array using zero\-based array indexing:

```

```
1WITH '{
2  "name": "Open House 2026",
3  "tagline": "The real-time database for AI conference",
4  "dates": {
5    "workshops": "2026-05-26",
6    "conference": ["2026-05-27", "2026-05-28"]
7  },
8  "venue": {
9    "name": "Convene 100 Stockton",
10    "address": "40 O''Farrell St, San Francisco, CA 94108"
11  }
12}' AS conf
13SELECT JSON_VALUE(conf, ('$.dates.conference[0]', '$.dates.conference[1]'));
```

```

```
┌─JSON_VALUE(co⋯ference[1]'))─┐
│ ('2026-05-27','2026-05-28') │
└─────────────────────────────┘

```

Alternatively, if we want to return the dates as an array and the whole venue object, we should rather use `JSON_QUERY`:

```

```
1WITH '{
2  "name": "Open House 2026",
3  "tagline": "The real-time database for AI conference",
4  "dates": {
5    "workshops": "2026-05-26",
6    "conference": ["2026-05-27", "2026-05-28"]
7  },
8  "venue": {
9    "name": "Convene 100 Stockton",
10    "address": "40 O''Farrell St, San Francisco, CA 94108"
11  }
12}' AS conf
13SELECT JSON_QUERY(conf, ('$.dates.conference', '$.venue'))
14FORMAT Raw;
```

```

The output, formatted for readability, is shown below:

```
(
  '[["2026-05-27","2026-05-28"]]',
  '[{"name":"Convene 100 Stockton","address":"40 O\'Farrell St, San Francisco, CA 94108"}]'
)

```

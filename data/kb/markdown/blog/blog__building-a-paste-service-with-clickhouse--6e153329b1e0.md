# Building a Paste Service With ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building a Paste Service With ClickHouse

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Apr 1, 2022 · 14 minutes read
I like to test ClickHouse in unusual scenarios. Whenever someone (including myself) says that ClickHouse is not good for a particular task, I immediately go and test it on exactly this task to see how it behaves. Sometimes it leads to unusual, and very interesting, outcomes.


This weekend I decided to collect most of the well recognized anti\-patterns and to build a service on top of them. In our engineering team we often need to share server logs, snippets of code, queries and other text. There are an uncountable number of “paste” sharing services like [pastebin.com](https://pastebin.com/), [gist.github.com](https://gist.github.com/) and [markify.dev](https://markify.dev/), but I want something different.


Firstly, I want it to look as a plaintext file without any decorations – totally styling free. Secondly, I want to do less clicks – I don’t want to press a “publish” button, I don’t want to make extra clicks to get the “raw” version. And most importantly, I want all the data to be stored in ClickHouse.


## **TLDR** [\#](/blog/building-a-paste-service-with-clickhouse#tldr)


[pastila.nl](https://pastila.nl/) – here is this service.


## **Basic Ideas** [\#](/blog/building-a-paste-service-with-clickhouse#basic-ideas)


Let’s create a website with a single page and a huge “text\-area”. Let’s get rid of the “publish” button – on every change to the text\-area, the data will be saved automatically. Also the page URL should also change and contain the hash of the data. The only remaining step for the user is to copy the URL – the data can be retrieved back by this URL.


For the backend of this service we will use ClickHouse, facing directly to the internet. The JavaScript code on the HTML page will directly perform INSERT and SELECT queries to this ClickHouse instance.


The data should be content\-addressable by its hash. We will calculate two hashes: 128\-bit [SipHash](https://clickhouse.com/docs/en/sql-reference/functions/hash-functions/#hash_functions-siphash128) and a 32\-bit [locality\-sensitive hash](https://en.wikipedia.org/wiki/Locality-sensitive_hashing) (fingerprint). The SipHash is distinct for distinct data and fingerprint is a number that does not change on small changes on data.


Whenever data is edited, we also track the previous hashes, so we can navigate through edit history (to some extent).


## **Servers Setup** [\#](/blog/building-a-paste-service-with-clickhouse#servers-setup)


The data is stored in a single table in ClickHouse. I created two servers for ClickHouse in AWS for replication – one in Europe (Frankfurt) and one in the US (Ohio). I used a geographically distributed setup for lower latency on SELECT queries. I then set up geo DNS in AWS Route53 to direct traffic to the nearest server. I’ve created SSL certificates with [Let’s Encrypt](https://letsencrypt.org/) and set up port 443 for listening in ClickHouse.


I have also set up an embedded [ClickHouse Keeper](https://clickhouse.com/docs/en/operations/clickhouse-keeper/) for replication to avoid the need for a separate ZooKeeper component. It is nice when you don’t have to install anything else, only ClickHouse – it is packaged in a single binary and can be installed anywhere as easy as `curl https://clickhouse.com/ | sh`.


[ClickHouse Keeper](https://clickhouse.com/docs/en/operations/clickhouse-keeper/) works faster and more reliably than ZooKeeper, but the problem is that I have only two servers. Three servers is a minimum required for proper operation of distributed consensus. In fact, you can install it on two servers, but it gives almost no advantages over a single server – it will become unavailable for writes if any of the two servers goes offline. But if one of two servers goes offline forever, the data will still be safe, because it is replicated. So, I accepted even this anti\-pattern and installed ClickHouse Keeper across two nodes on the different sides of the Atlantic Ocean, just to observe how miserable the experience will be


## **Table Structure** [\#](/blog/building-a-paste-service-with-clickhouse#table-structure)


I created a Replicated database:



```
CREATE DATABASE paste ENGINE = Replicated('/clickhouse/databases/paste/', '{shard}', '{replica}');

```

It is an [experimental database engine](https://clickhouse.com/docs/en/engines/database-engines/replicated/) under development. It enables replication of all the changes in tables (DDL queries) across the cluster.


Then I created a table:



```
CREATE TABLE paste.data
(
    fingerprint UInt32 DEFAULT reinterpretAsUInt32(unhex(fingerprint_hex)),
    hash UInt128 DEFAULT reinterpretAsUInt128(unhex(hash_hex)),
    prev_fingerprint UInt32 DEFAULT reinterpretAsUInt32(unhex(prev_fingerprint_hex)),
    prev_hash UInt128 DEFAULT reinterpretAsUInt128(unhex(prev_hash_hex)),
    content String,

    size UInt32 MATERIALIZED length(content),
    time DateTime64 MATERIALIZED now64(),
    query_id String MATERIALIZED queryID(),

    fingerprint_hex String EPHEMERAL '',
    hash_hex String EPHEMERAL '',
    prev_fingerprint_hex String EPHEMERAL '',
    prev_hash_hex String EPHEMERAL '',

    CONSTRAINT length CHECK length(content) < 10 * 1024 * 1024,
    CONSTRAINT hash_is_correct CHECK sipHash128(content) = reinterpretAsFixedString(hash),
    CONSTRAINT not_uniform_random CHECK length(content) < 10000 OR arrayReduce('entropy', extractAll(content, '.')) < 7,
    CONSTRAINT not_constant CHECK length(content) < 10000 OR arrayReduce('uniqUpTo(1)', extractAll(content, '.')) > 1,

    PRIMARY KEY (fingerprint, hash)
)
ENGINE = ReplicatedMergeTree;

```

Some magic is happening there… Let’s look in more detail.



```
hash UInt128 DEFAULT reinterpretAsUInt128(unhex(hash_hex)),
fingerprint_hex String EPHEMERAL '',

```

We will store 128\-bit hash as UInt128 number – this is natural. But JavaScript code will send us hashes in hex, like ‘001122334455667788aabbccddeeff’ (16 bytes, 32 nibbles). We want to allow INSERT query with hex representation of the hash, but to convert it into UInt128 during insert. That’s why we use one of the most recent ClickHouse features – [EPHEMERAL](https://clickhouse.com/docs/en/sql-reference/statements/create/table/#ephemeral) columns. They are the columns you can reference and use on INSERT, but they are not stored in the table and only used to calculate the values of other columns during INSERTs. There are other options to make these calculations, for example: [INSERT SELECT … FROM input(…)](https://clickhouse.com/docs/en/sql-reference/table-functions/input/) and [INSERT SELECT … FROM format(…)](https://github.com/ClickHouse/ClickHouse/pull/34125).



```
prev_fingerprint UInt32 DEFAULT reinterpretAsUInt32(unhex(prev_fingerprint_hex)),
prev_hash UInt128 DEFAULT reinterpretAsUInt128(unhex(prev_hash_hex)),

```

Previous hashes are used to link to the previous version if the content was edited.



```
content String,

```

The data is stored in the String field. Note that String data type can store arbitrary bytes of arbitrary size, like BLOB.



```
size UInt32 MATERIALIZED length(content),
time DateTime64 MATERIALIZED now64(),
query_id String MATERIALIZED queryID(),

```

Here we use [MATERIALIZED](https://clickhouse.com/docs/en/sql-reference/statements/create/table/#materialized) columns. These columns are always calculated on INSERT query by provided expressions. The user cannot insert different data to them. The `query_id` field can be used for reference to the [system.query\_log](https://clickhouse.com/docs/en/operations/system-tables/query_log/) table.



```
CONSTRAINT length CHECK length(content) < 10 * 1024 * 1024,

```

Here we limit the data size on INSERT. 10 megabytes is quite generous. It should be enough to paste a stack trace from a Java application if needed.



```
CONSTRAINT hash_is_correct CHECK sipHash128(content) = reinterpretAsFixedString(hash),

```

Just in case, we check that the hash calculated on the client side is actually a hash of the data. Otherwise someone can connect to ClickHouse directly and send arbitrary garbage. In fact they still can. But this constraint will constrain the kinds of garbage that we are going to receive.



```
CONSTRAINT not_uniform_random CHECK length(content) < 10000 OR arrayReduce('entropy', extractAll(content, '.')) < 7,

```

Here I tried to improvise a rudimentary kind of anti\-fraud protection. If the content is longer than 10K, we split the content in bytes into array: `extractAll(content, '.')`, then aggregate this array with `entropy` aggregate function: `arrayReduce('entropy', extractAll(content, '.'))` – it will give us the amount of information per byte. And if it is approaching 8 bits, we can say that it looks like random garbage and reject it.


After I told you about this rudimentary anti\-fraud, it no longer has any effect and you can go and make DoS of our service (I will have a pleasure watching).



```
CONSTRAINT not_constant CHECK length(content) < 10000 OR arrayReduce('uniqUpTo(1)', extractAll(content, '.')) > 1,

```

This will check that the content is not entirely repeated with one byte – we use `uniqUpTo` aggregate function.



```
PRIMARY KEY (fingerprint, hash)

```

Let’s remember: `hash` is a 128\-bit cryptographic hash and `fingerprint` is a short [locality\-sensitive hash](https://en.wikipedia.org/wiki/Locality-sensitive_hashing). Why is `fingerprint` needed, why don’t you just use `hash`? It is an optimization. The data in the table will be ordered by `fingerprint` first and then by `hash`. This will place similar data close to each other and it will be compressed better. Remember that we are going to store *every edit on every keypress* in our table. But thanks to locality sensitive hashing and compression, the excessive data will occupy almost zero storage.


And it is worth noting a nice recent improvement of ClickHouse – you can write the PRIMARY KEY near the column list in the table, similarly to other relational DBMS.



```
ENGINE = ReplicatedMergeTree;

```

If you use a Replicated database, you don’t have to write any parameters for ReplicatedMergeTree. This is very liberating.


There were two options to choose: ReplicatedMergeTree and ReplicatedReplacingMergeTree for deduplication of data when the same content has been stored more than once. I decided to keep the duplicates, because I want to keep the earliest record of the `time` field.


## **Frontend Implementation** [\#](/blog/building-a-paste-service-with-clickhouse#frontend-implementation)


The frontend is a single static HTML with no dependencies. It has less than 100 lines of JavaScript code, let’s review all of them.


The implementation of SipHash: <https://pastila.nl/?01b7bd64/ab243265ec739fb9373b81ea5fb5c973>


It is the same as the reference implementation but adapted for JavaScript. We use modern features like BigInt and TypedArray. I’m not a JS developer, so I spend half a day in MDN and Stackoverflow debugging this implementation.


The implementation of locality sensitive hash is more interesting:



```
function getFingerprint(text) {
    return text.match(/\p{L}{4,100}/gu).
        map((elem, idx, arr) => idx + 2 < arr.length ? [elem, arr[idx + 1], arr[idx + 2]] : []).
        filter(elem => elem.length === 3).map(elem => elem.join()).
        filter((elem, idx, arr) => arr.indexOf(elem) === idx).
        map(elem => sipHash128(encoder.encode(elem)).substr(0, 8)).
        reduce((min, curr) => curr < min ? curr : min, 'ffffffff');
}

```

First we extract something like words from the text `text.match(/\p{L}{4,100}/gu)` (sequences of Unicode code points that have “letter” character class). Note that code point classification depends on the Unicode standard version and consequently on the browser and OS version. If the content has unusual new characters, the fingerprint can be calculated differently on old browsers. But the old browsers won’t be able to display these characters, so it’s not a problem.


Second we transform the array of words to the array of [shingles](https://en.wikipedia.org/wiki/N-gram) (sequences of three consecutive words). Shingling is a well known method in classic NLP.


And we calculate a SipHash for every shingle and get a [minimum](https://en.wikipedia.org/wiki/MinHash), truncated to 32 bits (we don’t need many).


If I’d say it simply in pseudocode, it would be: min(hashes(shingles(text))). This is not the best locality sensitive hash, I just improvised something decent.



```
document.getElementById('data').addEventListener('input', (event) => {

    prev_fingerprint = curr_fingerprint;
    prev_hash = curr_hash

    const text = document.getElementById('data').value;

    curr_hash = sipHash128(encoder.encode(text));
    curr_fingerprint = getFingerprint(text);

    save(text);
});

```

This code subscribes to the changes in the textarea and saves them to ClickHouse.



```
async function save(text) {
    const my_request_num = ++request_num;

    show(wait);

    const response = await fetch(
        clickhouse_url,
        {
            method: "POST",
            body: "INSERT INTO data (fingerprint_hex, hash_hex, prev_fingerprint_hex, prev_hash_hex, content) FORMAT JSONEachRow " + JSON.stringify(
            {
                fingerprint_hex: curr_fingerprint,
                hash_hex: curr_hash,
                prev_fingerprint_hex: prev_fingerprint,
                prev_hash_hex: prev_hash,
                content: text
            })
        });

    if (!response.ok) {
        show(error);
        throw new Error(`Saving failed\nHTTP status ${response.status}`);
    }

    if (my_request_num == request_num) {
        history.pushState(null, null, window.location.pathname.replace(/(\?.+)?$/, `?${curr_fingerprint}/${curr_hash}`));
        show(check);
    }
}

```

The data is POSTed to ClickHouse with a simple INSERT statement with JSON data.


If data is successfully saved, we change the URL in the browser’s address bar with the [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API).


The only trick is to check request\_num to avoid race conditions – the URL in the address bar should not point to older results if requests were completed out of order. I see this type of race condition in about half of the websites, so I always remember about it.



```
function restore() {
    const components = window.location.search.match(/^\?([0-9a-f]{8})\/([0-9a-f]{32})(\.md|\.markdown|\.html?)?/);
    if (components) load(components[1], components[2], components[3]);
}

```

When the page is opened we look at the hashes in the URL and load the content.



```
async function load(fingerprint, hash, type) {
    show(wait);

    const response = await fetch(
        clickhouse_url,
        { method: "POST", body: `SELECT content, lower(hex(reinterpretAsFixedString(prev_hash))) AS prev_hash, lower(hex(reinterpretAsFixedString(prev_fingerprint))) AS prev_fingerprint FROM data WHERE fingerprint = reinterpretAsUInt32(unhex('${fingerprint}')) AND hash = reinterpretAsUInt128(unhex('${hash}')) ORDER BY time LIMIT 1 FORMAT JSON` });

    function onError() {
        show(error);
        throw new Error(`Load failed\nHTTP status ${response.status}\nMessage: ${response.body}`);
    }

    if (!response.ok) onError();
    const json = await response.json();

```

To query ClickHouse, we use the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). The query is sent with the POST method to the ClickHouse endpoint.



```
SELECT 
    content, 
    lower(hex(reinterpretAsFixedString(prev_hash))) AS prev_hash, 
    lower(hex(reinterpretAsFixedString(prev_fingerprint))) AS prev_fingerprint 
FROM data 
WHERE fingerprint = reinterpretAsUInt32(unhex('${fingerprint}')) 
  AND hash = reinterpretAsUInt128(unhex('${hash}'))
ORDER BY time LIMIT 1 
FORMAT JSON

```

We convert hashes from numbers to hexadecimal for JavaScript and back.


The hashes are substituted directly to the query. It looks like an [SQL injection](https://owasp.org/www-community/attacks/SQL_Injection). In fact this code is run on the client side in the browser and we allow arbitrary SQL queries to be sent to the endpoint, and it puts the question about SQL injections out of scope. The server will not allow dangerous queries nevertheless.


The tricky part is to select the first record by time – this is better for navigating through edit history if the history has loops (like if a character is added and then backspace pressed).



```
if (type === '.html' || type == '.htm') {
        document.open();
        document.write(content);
        document.close();
    } else if (type === '.md' || type === '.markdown') {
        await loadMarkdownRenderer();
        document.body.className = 'markdown';
        document.body.innerHTML = marked.parse(content);
    } else {
        document.getElementById('data').value = content;

```

One neat trick: if `.md` is added to the URL, we will load the markdown renderer and display the content formatted.


And if `.html` is added, we will render the HTML as is. This is very insecure, because arbitrary HTML can contain [redirects to malicious resources](https://www.youtube.com/watch?v=dQw4w9WgXcQ), set cookies, display cat videos and do weird stuff. Do not open these URLs.



```
/// Huge JS libraries should be loaded only if needed.
function loadJS(src, integrity) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        if (integrity) {
            script.crossOrigin = 'anonymous';
            script.integrity = integrity;
        } else {
            console.warn('no integrity for', src)
        }
        script.addEventListener('load', function() { marked.setOptions({ gfm: true, breaks: true }); resolve(true); });
        document.head.appendChild(script);
    });
}

let load_markdown_promise;
function loadMarkdownRenderer() {
    if (load_markdown_promise) { return load_markdown_promise; }

    return loadJS('https://cdnjs.cloudflare.com/ajax/libs/marked/4.0.2/marked.min.js',
        'sha512-hzyXu3u+VDu/7vpPjRKFp9w33Idx7pWWNazPm+aCMRu26yZXFCby1gn1JxevVv3LDwnSbyKrvLo3JNdi4Qx1ww==');
}

```

The third\-party dependency is loaded lazily, because I don’t want users to do an extra request if they don’t need it.


## **Users and Quotas** [\#](/blog/building-a-paste-service-with-clickhouse#users-and-quotas)


Creating a dedicated user for the service:



```
CREATE USER paste IDENTIFIED WITH no_password
DEFAULT DATABASE paste
SETTINGS
    add_http_cors_header = 1,
    async_insert = 1,
    wait_for_async_insert = 0,
    limit = 1,
    offset = 0,
    max_result_rows = 1,
    force_primary_key = 1,
    max_query_size = '10M';

```

It has no password, because setting a password does not make sense (it should be accessible from the client side).


There are many settings to constraint this user:


`add_http_cors_header` – this to enable [Cross Origin Request Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) (when doing requests from a page to a different domain, the server should tell the browser that it is actually ok).


`async_insert` and `wait_for_async_insert` – this is the most questionable part. Enabling [asynchronous INSERTs](https://clickhouse.com/docs/en/operations/settings/settings/#async-insert) will allow the server to accumulate data in its own buffer from multiple clients before INSERTion and wait for at most 200ms by default for a batch to be accumulated and written to a table. If `wait_for_async_insert` is set to 1, this is safe, because the client will wait for writing confirmation. But if you set `wait_for_async_insert` to 0, ClickHouse will instantly transform itself to MongoDB.


I set up replication over the Atlantic Ocean, the RTT between servers is [around 100ms](https://www.cloudping.co/grid), but the metadata about every INSERT in ClickHouse is committed to RAFT distributed consensus, and it takes multiple roundtrips. I found real numbers to be as high as 800ms.


Even if `wait_for_async_insert` is enabled, asynchronous INSERTs have one downside: constraints are being checked after data has been collected in batches. It means that concurrent INSERTs of different clients may cause constraint violation in other clients. Asynchronous INSERTs also prevent having the correct query\_id field in the table.


`limit` and `offset`. Usually you limit the result set with LIMIT and OFFSET clauses in the SELECT statement. ClickHouse also has support for “out of band” limit and offset settings to ensure the limits for all SQL queries.


`force_primary_key` – to make sure that queries always use the primary index.



```
CREATE QUOTA paste
KEYED BY ip_address
FOR RANDOMIZED INTERVAL 1 MINUTE MAX query_selects = 100, query_inserts = 1000, written_bytes = '10M',
FOR RANDOMIZED INTERVAL 1 HOUR MAX query_selects = 1000, query_inserts = 10000, written_bytes = '50M',
FOR RANDOMIZED INTERVAL 1 DAY MAX query_selects = 5000, query_inserts = 50000, written_bytes = '200M'
TO paste;

```

ClickHouse has rate limiting for users. Here we define a quota that will limit the number of operations and the amount of loaded data per interval.



```
GRANT SELECT, INSERT ON paste.data TO paste;

```

Finally we allow our users to do INSERTs and SELECTs, but not DROP TABLE, ALTER and similar.


## **Summary** [\#](/blog/building-a-paste-service-with-clickhouse#summary)


This service works and I successfully applied the following antipatterns:


1. ClickHouse is facing directly to the internet.
2. Replication across the Atlantic Ocean.
3. Two nodes in the RAFT ensemble instead of three.
4. Using an experimental Replicated database engine.
5. Writing JavaScript code.


Should you do the same?


Probably not.


But it is interesting to learn from.


“[Paste Copy Paste Copy](https://www.flickr.com/photos/14136614@N03/5904308311)” by [wiredforlego](https://www.flickr.com/photos/14136614@N03) is marked with [CC BY\-SA 2\.0](https://creativecommons.org/licenses/by-sa/2.0/?ref=openverse).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

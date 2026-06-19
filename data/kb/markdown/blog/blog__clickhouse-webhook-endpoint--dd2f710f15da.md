# Using ClickHouse as a webhook endpoint with HMAC verification


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Using ClickHouse as a webhook endpoint with HMAC verification

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Mar 3, 2026 · 8 minutes readOne of my favorite features of ClickHouse 25\.12 was the [`HMAC` function](https://clickhouse.com/blog/clickhouse-release-25-12#hmac) for message authentication using a shared key.


ClickHouse has always been able to act as a webhook endpoint, but with the HMAC function we can now verify webhook requests, filtering out those that didn't come from the expected source.
We'll start by seeing how this works with a local example, before moving onto a real\-life example using ClickHouse Cloud as a GitHub webhook endpoint.


## The webhook pattern [\#](/blog/clickhouse-webhook-endpoint#the-webhook-pattern)


One cool thing about ClickHouse is the ability to chain tables together using materialized views. Data gets ingested into one table, a materialized view acts as a SQL trigger, and the results are written to another table.


This becomes especially powerful when combined with the Null table engine. Rather than storing data, the Null table engine forwards
everything it receives to any connected materialized views — making it the perfect staging layer.


The result is a clean three\-step pattern:


1. A staging table receives all incoming data
2. A materialized view validates and transforms it
3. A final table stores only the verified data


![Webhook Diagram Issue 1399.jpg](/uploads/Webhook_Diagram_Issue_1399_0e9e53eb69.jpg)
## Create the tables [\#](/blog/clickhouse-webhook-endpoint#create-the-tables)


Let's have a look at how to set this all up in ClickHouse.
If you want to follow along, you'll need to have a ClickHouse server or ClickHouse Cloud service running.


First, let's create the staging table:



```

```
1CREATE TABLE webhook_staging (
2    received_at DateTime DEFAULT now(),
3    raw_payload String,
4    signature String DEFAULT getClientHTTPHeader('X-Hub-Signature-256')
5) ENGINE = MergeTree()
6ORDER BY received_at
7SETTINGS allow_get_client_http_header=1;
```

```

The `allow_get_client_http_header` setting is required because reading client headers is disabled by default.



> We're creating the `webhook_staging` table with the `MergeTree` engine, so that we can debug incoming requests. In a production system we would use the `Null` engine and might also have a second materialized view that captures invalid requests.


Next, we have a table that's going to store only verified rows:



```

```
1CREATE TABLE webhook_logs (
2    received_at DateTime,
3    payload JSON
4) ENGINE = MergeTree()
5ORDER BY received_at;
```

```

And finally, we have a materialized view that validates the data:



```

```
1CREATE MATERIALIZED VIEW webhook_validator TO webhook_logs AS
2SELECT
3    received_at,
4    raw_payload::JSON as payload
5FROM webhook_staging
6WHERE signature = 'sha256=' || lower(hex(HMAC('SHA256', raw_payload, 'my_secret_key')));
```

```

We're comparing the signature from the request header to the expected signature computed using the shared secret key.
Our shared secret key is `my_secret_key`.


If the incoming row doesn't match the expected signature, it won't be written to the `webhook_logs` table.


## Create a restricted user [\#](/blog/clickhouse-webhook-endpoint#create-a-restricted-user)


When experimenting on our own machine, we could use the default admin user, but for a production system it's safer to create a dedicated user with minimal permissions.
The user that we create will be used in the webhook URL that we construct later.


First, let's create the user:



```

```
1CREATE USER webhook_receiver
2IDENTIFIED WITH sha256_hash
3BY 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';
```

```

The hash is the SHA256 of an empty string, so no password is needed when we construct the webhook URL.


Next, let's grant the user the permissions it needs:



```

```
1GRANT INSERT ON default.webhook_staging TO webhook_receiver;
2GRANT SELECT ON default.webhook_staging TO webhook_receiver;
3GRANT SHOW TABLES ON default.webhook_staging TO webhook_receiver;
4GRANT SHOW DATABASES ON default.* TO webhook_receiver;
```

```

If we want to be extra cautious, we could also apply rate limits to this user to guard against abuse.


## Construct the webhook URL [\#](/blog/clickhouse-webhook-endpoint#construct-the-webhook-url)


ClickHouse accepts inserts over HTTP, which means the whole webhook endpoint is a URL with the INSERT query embedded:



```
http://localhost:8123/?user=webhook_receiver&query=INSERT+INTO+webhook_staging+(raw_payload)+FORMAT+RawBLOB

```

The key parts:


- `user=webhook_receiver` \-the restricted user we created
- `query=INSERT INTO webhook_staging (raw_payload) FORMAT RawBLOB` \-the URL\-encoded query that inserts the raw request body


`FORMAT RawBLOB` tells ClickHouse to treat the entire request body as a single string value rather than trying to parse it.


We can then test it out by sending a valid request i.e. one where the signature is computed with the correct key:



```

```
1PAYLOAD='{"event":"user_login","user_id":456}'
2SIGNATURE=$(echo -n ",[object Object]," | openssl dgst -sha256 -hmac "my_secret_key" | cut -d' ' -f2)
3
4curl -X POST "http://localhost:8123/?user=webhook_receiver&allow_get_client_http_header=1&query=INSERT%20INTO%20webhook_staging%20(raw_payload)%20FORMAT%20RawBLOB" \
5  -H "X-Hub-Signature-256: sha256=,[object Object]," \
6  -d ",[object Object],"
```

```

Let's now connect to our ClickHouse Server using ClickHouse Client:



```

```
1clienthouse client
```

```

And we can return the contents of `webhook_staging` and `webhook_logs`:



```

```
1SELECT * FROM webhook_staging;
```

```


```
Row 1:
──────
received_at: 2026-02-20 15:42:22
raw_payload: {"event":"user_login","user_id":456}
signature:   sha256=5a23c796b6248c725a6ec7fc2cf0788117d69d376ee6241f411a8887297d3ca4

1 row in set. Elapsed: 0.001 sec.

```


```

```
1SELECT * FROM webhook_logs;
```

```


```
Row 1:
──────
received_at: 2026-02-20 15:42:22
payload:     {
    "event": "user_login",
    "user_id": 456
}

1 row in set. Elapsed: 0.003 sec.

```

Both tables have the data. Now how about we send a request where we've computed the signature with a different key:



```

```
1PAYLOAD='{"event":"user_login","user_id":456}'
2SIGNATURE=$(echo -n ",[object Object]," | openssl dgst -sha256 -hmac "rogue_key" | cut -d' ' -f2)
3
4curl -X POST "http://localhost:8123/?user=webhook_receiver&allow_get_client_http_header=1&query=INSERT%20INTO%20webhook_staging%20(raw_payload)%20FORMAT%20RawBLOB" \
5  -H "X-Hub-Signature-256: sha256=,[object Object]," \
6  -d ",[object Object],"
```

```

Let's run our queries against `webhook_staging`:



```
Row 1:
──────
received_at: 2026-02-20 15:43:21
raw_payload: {"event":"user_login","user_id":456}
signature:   sha256=01f65041f2505f2b245f3caff410913a22a0ff8c7e8414c9fe1e861359973a7a

Row 2:
──────
received_at: 2026-02-20 15:42:22
raw_payload: {"event":"user_login","user_id":456}
signature:   sha256=5a23c796b6248c725a6ec7fc2cf0788117d69d376ee6241f411a8887297d3ca4

2 rows in set. Elapsed: 0.002 sec.

```

And now, `webhook_logs`:



```
Row 1:
──────
received_at: 2026-02-20 15:42:22
payload:     {
    "event": "user_login",
    "user_id": 456
}

1 row in set. Elapsed: 0.004 sec.

```

`webhook_staging` gets a new row, `webhook_logs` doesn't \- the signatures didn't match so the materialized view dropped it.


## GitHub webhook [\#](/blog/clickhouse-webhook-endpoint#github-webhook)


With the pattern established locally, let's wire it up to a real GitHub repository using ClickHouse Cloud. The structure is almost identical, with just one difference \- the staging table picks up an extra `event_type` column (from the `X-GitHub-Event` header GitHub sends) and `webhook_logs` picks an `event_type` column as well.



The queries below create our tables and materialized view.



```

```
1CREATE TABLE webhook_staging (
2    received_at DateTime DEFAULT now(),
3    raw_payload String,
4    event_type String DEFAULT getClientHTTPHeader('X-GitHub-Event'),
5    signature String DEFAULT getClientHTTPHeader('X-Hub-Signature-256')
6) ENGINE = MergeTree()
7ORDER BY received_at
8SETTINGS allow_get_client_http_header=1;
```

```


```

```
1CREATE TABLE webhook_logs (
2    received_at DateTime,
3    event_type String,
4    payload JSON
5) ENGINE = MergeTree()
6ORDER BY received_at;
```

```


```

```
1CREATE MATERIALIZED VIEW webhook_validator TO webhook_logs AS
2SELECT
3    received_at,
4    event_type,
5    raw_payload::JSON as payload
6FROM webhook_staging
7WHERE signature = 'sha256=' || lower(hex(HMAC('SHA256', raw_payload, 'my_secret_key')));
```

```

In ClickHouse Cloud, click **Connect** to get your cluster URL, then build the webhook URL the same way \- just swap `localhost:8123` for your Cloud host and add `allow_get_client_http_header=1`:



```
https://<host>:8443/?user=webhook_receiver&allow_get_client_http_header=1&query=INSERT+INTO+webhook_staging+(raw_payload)+FORMAT+RawBLOB

```

### Configure the GitHub webhook [\#](/blog/clickhouse-webhook-endpoint#configure-the-github-webhook)


In your GitHub repository, go to **Settings → Webhooks → Add webhook**:


1. Paste your ClickHouse URL into **Payload URL**
2. Set **Content type** to `application/json`
3. Enter your secret key in the **Secret** field \-this must match `my_secret_key` from the materialized view
4. Choose which events to send (push events are fine to start)
5. Click **Add webhook**


![2026-02-20_15-48-01.png](/uploads/2026_02_20_15_48_01_9837c2f742.png)
GitHub will immediately send a `ping` event. Refresh the webhook page and you should see "Last delivery was successful".


![2026-02-20_15-48-31.png](/uploads/2026_02_20_15_48_31_e808d6d9c3.png)
### Verify it's working [\#](/blog/clickhouse-webhook-endpoint#verify-its-working)


We can then explore the contents of each table by clicking their name.


You should see the `ping` event in both, which confirms the HMAC validation passed. Now make a change to your repository \-commit to a branch, open a PR, merge it \-and push events will appear in both tables.


![2026-02-20_16-11-08.png](/uploads/2026_02_20_16_11_08_fbcc3df256.png)
### Testing signature validation [\#](/blog/clickhouse-webhook-endpoint#testing-signature-validation)


To confirm the validation is working, go back to GitHub, change the webhook secret to something different, then make another commit.


`webhook_staging` will have the new rows but `webhook_logs` won't \- the materialized view computed a different HMAC and filtered them out.


![Webhook Diagram for Blog.jpg](/uploads/Webhook_Diagram_for_Blog_ae59da5240.jpg)### Ready to create your own webhook endoint?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-77-ready-to-create-your-own-webhook-endoint-sign-up&utm_blogctaid=77)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

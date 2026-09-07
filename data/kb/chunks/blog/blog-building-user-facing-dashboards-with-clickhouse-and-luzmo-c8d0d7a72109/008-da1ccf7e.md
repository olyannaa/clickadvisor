---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-a-user-facing-dashboard-with-clickhouse-and-luzmo-clickhouse
ch_version_introduced: '5.1'
last_updated: '2026-09-07'
chunk_index: 8
total_chunks_in_doc: 9
---

// ... 7} ``` Copy command ### 3\. Embed the dashboard \# Now that we’ve set up a way to fetch and display data in your dashboards securely, we can go ahead and embed them inside our application.

Once you know where you want to display your dashboard inside your app, it’s literally as easy as copy\-pasting 5\-10 lines of code.

```
1<luzmo-dashboard
2  dashboardId="<ID of dashboard you want to embed>"
3  authKey="<embed key (id property) returned by step 1>"
4  authToken="<embed token (token property) returned by step 1>"
5  appServer="https://app.luzmo.com/"
6>
7</luzmo-dashboard>
8
9<script defer src="https://cdn.luzmo.com/js/luzmo-embed/5.1.5/luzmo-embed.min.js" charset="utf-8"></script>
```
Copy command
To find your unique code snippet, go to the dashboard you want to embed and click "Embed". Now select the front\-end framework your app uses and copy the code snippet. The dashboard ID will already be filled out; you'll only need to add the authKey and authToken generated in the previous step.

![](/_next/image?url=%2Fuploads%2F11_embed_code_dashboard_1de5501310.png&w=2048&q=75)

And that's it! You'll now have an interactive user\-facing dashboard added to your app, showing only the data your users are allowed to see.

To see what it would look like, try out the embedded dashboard below and switch between two users:

- Irvine Seller, the London\-based property manager
- David Brickham, the Manchester\-based real estate owner

[![](/_next/image?url=%2Fuploads%2F1_clickhouse_dashboard_62a3969883.png&w=2048&q=75)](https://app.luzmo.com/s/clickhouse-demo-uk-home-prices-16cn64omlx7s38hr)

We’ve kept it relatively simple in this example, but there are many more properties you can add to make your dashboard experience more customized:

- Which language to display your dashboard in
- Timezone of the user
- Screen mode the dashboard should load in (desktop, mobile, fixed width)
- Styling of the dashboard loader
- Connecting to different databases based on users or environment

Check out the [developer documentation](https://developer.luzmo.com/guide/embedding--component-api-reference) to see what else you can customize!

## Resources \#

If you want to get started embedding a user\-facing dashboard into your own SaaS or web app, here are a few resources that will come in handy.

Tools:

- [Free Luzmo trial (10 days)](https://app.luzmo.com/signup)
- [Free ClickHouse trial (30 days)](https://auth.clickhouse.cloud/u/signup/identifier?state=hKFo2SBiX0RSUHdkbmxhWV9UMUNGT3JlVmRmRTFkUXdXUF9GWKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIE9MWEJXZFF5a3A1eFdMd0FwZ2RDZEdjbFJvVko2N2Jzo2NpZNkgSVBwSDRSTkQwcU5YSFZheWVwZmZnc0dwYlhRbUZpa3I)

Documentation:

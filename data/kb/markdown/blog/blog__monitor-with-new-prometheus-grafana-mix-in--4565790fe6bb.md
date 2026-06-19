# Monitor your ClickHouse Cloud services with the new Prometheus/Grafana Mix\-in


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Monitor your ClickHouse Cloud services with the new Prometheus/Grafana Mix\-in

![Vlad Seliverstov Profile Picture](/_next/image?url=%2Fuploads%2Fvlad_seliverstov_cc2353fc42.jpeg&w=96&q=75)Vlad SeliverstovMay 12, 2025 · 5 minutes read![Prometheus mixin for ClickHouse monitoring new title.png](/uploads/Prometheus_mixin_for_Click_House_monitoring_new_title_d712c6d71a.png)
We're excited to announce the release of our new ClickHouse Cloud Prometheus/Grafana mix\-in, designed to make monitoring your ClickHouse Cloud services as easy as possible. This mix\-in leverages our existing Prometheus\-compatible API endpoint to scrape ClickHouse metrics into your existing Prometheus and Grafana setup, providing real\-time visibility into your services' health and performance with a pre\-configured dashboard. This mix\-in is nearly identical to our own internal dashboards used by our engineering teams to monitor every instance deployed in our cloud.


### Why we’re releasing this [\#](/blog/monitor-with-new-prometheus-grafana-mix-in#why-were-releasing-this)


Monitoring is crucial for maintaining the health and performance of your ClickHouse deployment. The monitoring pages in our Cloud Console provide a lot of useful information, but many of our customers maintain sophisticated stacks comprising dozens (or hundreds) of discrete services. Rather than using different tooling to monitor each component, solutions like Prometheus and Grafana provide an easy way to collect and view metrics from the entire stack in a single centralized location.


Scraping ClickHouse Cloud metrics into Prometheus has always been supported to varying extents. ClickHouse offers a Prometheus\-friendly output format and the system tables containing metrics can be queried directly via HTTP. However, this method is—frankly speaking—not very ergonomic. Each ClickHouse instance must be scraped independently and specifically for ClickHouse Cloud, the scraper is agnostic of service state, meaning scrapes will fail when a service is stopped and can prevent it from idling. To solve for these problems, we introduced a Prometheus endpoint in our cloud API that (1\) federates metrics emitted from all services in your ClickHouse Cloud organization; and (2\) gracefully handles state\-related corner cases.


The Prometheus API endpoint was an instant success—it is already used by our customers to monitor thousands of ClickHouse Cloud services in Production. Making these metrics more accessible very quickly uncovered another problem: ClickHouse emits *more than a thousand* metrics, and we witnessed many users struggling to figure out which ones are actually important to monitor. Scraping thousands of metrics from each replica in each ClickHouse Cloud service is (for most people) both silly and costly. For example, metrics like `ClickHouseProfileEvents_RegexpWithMultipleNeedlesGlobalCacheHit` are mostly irrelevant for day\-to\-day monitoring. We initially solved this by adding an optional `filtered_metrics` parameter to the Prometheus endpoint that pared down the 1000\+ available metrics to a more manageable 125 ‘mission critical’ metrics. These metrics are what we primarily use internally, via Grafana, for monitoring and debugging internal and customer instances in ClickHouse Cloud.


All of this, then, begs the question: *why not release our internal Grafana dashboard configuration as a publicly\-available template?* So here we are.


### Getting Started: Setting Up the Mix\-in [\#](/blog/monitor-with-new-prometheus-grafana-mix-in#getting-started-setting-up-the-mix-in)


**(Note: this section assumes you are already running both Prometheus and Grafana)**


#### Setting up Prometheus [\#](/blog/monitor-with-new-prometheus-grafana-mix-in#setting-up-prometheus)


1. **Update your Prometheus config (`prometheus.yml`)**  

Add the following scrape config. This configuration enables Prometheus to scrape metrics from all services in your organization. Remember to replace `<Organization ID>`, `<API Key ID>`, and `<API Key Secret>` with your actual credentials. `honor_labels: true` ensures that the labels provided by ClickHouse Cloud are retained, which is essential for our dashboards.



```

```
scrape_configs:
  - job_name: "My ClickHouse Org"
    static_configs:
      - targets: ["api.clickhouse.cloud"]
    scheme: https
    metrics_path: "/v1/organizations/<Organization ID>/prometheus"
    params:
      filtered_metrics: ["true"]
    basic_auth:
      username: <API Key ID>
      password: <API Key Secret>
    honor_labels: true
```

```

2. **Restart your Prometheus instance**  

After updating the configuration, restart Prometheus to apply the changes.
3. **Verify Prometheus is working**  

If everything is configured correctly, you should start seeing ClickHouse Cloud metrics being scraped by Prometheus. You can check this by navigating to Prometheus's web interface and viewing the ‘targets’ page. You should see something like:


![prom1.png](/uploads/prom1_2021803bf1.png)


#### Setting up Grafana \& Importing the Mix\-in [\#](/blog/monitor-with-new-prometheus-grafana-mix-in#setting-up-grafana--importing-the-mix-in)


1. **Add the Prometheus data source to Grafana (if you haven’t already)**  

Navigate to "Data sources" in the Grafana menu and add a new "Prometheus" data source. Input your Prometheus host and credentials:


![prom2.png](/uploads/prom2_ef6e394a56.png)
2. **Import the dashboard**  

From the dashboard creation screen, select "Import a dashboard." Paste the following URL into the input: [https://grafana.com/grafana/dashboards/23415\-prom\-exporter\-instance\-dashboard\-v2/](https://grafana.com/grafana/dashboards/23415-prom-exporter-instance-dashboard-v2/)


![import-via-grafana-url.png](/uploads/import_via_grafana_url_85f8f5903a.png)


Alternatively, you can paste the JSON content directly from our mix\-in repository:  

[https://github.com/ClickHouse/clickhouse\-mixin/blob/main/dashboard.json](https://github.com/ClickHouse/clickhouse-mixin/blob/main/dashboard.json)


![prom3.png](/uploads/prom3_dfff1eaf48.png)
3. **View your metrics**  

If everything works correctly, you should immediately see metrics for your ClickHouse Cloud services in the imported dashboard.


![prom4.png](/uploads/prom4_50347e738a.png)


### Conclusion [\#](/blog/monitor-with-new-prometheus-grafana-mix-in#conclusion)


This mix\-in should help you monitor your ClickHouse Cloud services exactly like we do. As always, we appreciate your feedback—please drop us a line if you have any requests or suggestions around improving our observability experience!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

# ClickHouse Newsletter July 2022: Geo queries for railway enthusiasts


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter July 2022: Geo queries for railway enthusiasts

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Jul 14, 2022 · 10 minutes readA warm welcome to you all. It is that time of the year when we wish our office in Amsterdam had air conditioning. Then again, that would mean it was ultramodern and on the outskirts of town rather than old and charming looking out on one of the central canals. Oh well, you can’t have it all in life, same as you can’t have a distributed database that satisfies all three guarantees of the CAP theorem.


Keep reading for our upcoming events (hope to see you in person in London or Munich), what’s new in ClickHouse 22\.6 and some fun with geo queries.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox as well? Sign up [here](https://discover.clickhouse.com/newsletter.html).


**Upcoming Events**


Mark your calendars for these:


- **ClickHouse v22\.7 Release Webinar**  

***When?*** Thursday, July 21 @ 9 am PDT / 5 pm GMT  

***How do I join?*** Register [here](https://clickhouse.com/company/events/v22-7-release-webinar/).
- **\[IN PERSON] ClickHouse London Meetup**  

Join us in the Cloudflare London office for a night full of talks. Cloudflare will share tips around schema management at scale and how they enable 100s of engineers to modify ClickHouse schemas. Hear from analytics startup Clippd about how they are using ClickHouse, and there are more talks on using ClickHouse for financial data, optimizing ClickHouse for ARM and visualizing data with ClickHouse.  

***When?*** Wednesday, July 20 @ 6 pm BST  

***How?*** Register [here](https://www.meetup.com/clickhouse-london-user-group/events/286891586/).
- **\[IN PERSON] ClickHouse Silicon Valley Meetup**  

We are very excited to be holding our next in\-person ClickHouse meetup at the Barracuda offices! Please join us for an evening of talks, food and discussion. There will be talks from ClickHouse users, and the ClickHouse team will share our latest updates and are available for plenty of questions!  

***When?*** Wednesday, July 20 @ 6 pm PDT  

***How?*** Register [here](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/287044471/).
- **\[IN PERSON] ClickHouse Munich Meetup**  

We’ll be coming together at the Metoda office in Munich for talks from Metoda, Akamai and ClickHouse. A number of ClickHouse engineers live around Munich, so we’ll have a lot of expertise present, come prepared with your questions!  

***When?*** Wednesday, July 27 @ 6 pm CEST  

***How?*** Register [here](https://www.meetup.com/clickhouse-meetup-munich/events/286891667/).


**ClickHouse v22\.6**


What’s in our regular monthly June release:


1. **ARM as a first\-class citizen** We continue to improve the experience of ClickHouse users running on ARM. This year, we introduced official Docker images, and now we’ve [made](https://github.com/ClickHouse/ClickHouse/pull/38093) tons of performance optimizations. Also, ClickHouse now [shows](https://github.com/ClickHouse/ClickHouse/pull/37797) stack traces on ARM, useful for debugging.
2. **[Search with dynamic values](https://github.com/ClickHouse/ClickHouse/pull/37251)** You can now use non\-constant parameters for LIKE and MATCH. For example, to find customers that use their first name as part of their email address use `SELECT * FROM customers WHERE match(email, firstName)`.
3. **[Parameters for external functions](https://github.com/ClickHouse/ClickHouse/pull/37720)** You can now pass parameters to external user\-defined functions.
4. **[Show server certificate](https://github.com/ClickHouse/ClickHouse/pull/37540)** Use `SELECT showCertificate()` to see the server certificate. It better match what you are seeing in your client/browser!
5. **[ZooKeeper writes](https://github.com/ClickHouse/ClickHouse/pull/37596)** You can now insert into the `system.zookeeper` table, directly manipulating data in ZooKeeper or ClickHouse Keeper. Should you? Let’s just say “it depends” and “only if you’re absolutely sure what you’re doing”.


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.6/), the [recording](https://youtu.be/0fSp9SF8N8A) and please upgrade (unless you want to stay on an LTS release).


**Query of the Month: Geo queries for railway enthusiasts**


Let’s say you are working for a multinational coffee store chain that has expanded into every corner of the world, and you’re looking to find out where you have maybe a few too many stores. And let’s assume that you have all data about your stores including their geographic coordinates in ClickHouse. You have a table and each row is one store and its latitude and longitude. How would you write a query to find the stores that are closest to each other?


Now, we’re not aware of a public dataset of coffee store locations, but there is [this dataset](https://beta-naptan.dft.gov.uk/) of all public transport stops in England and Wales. Formally known as “National Public Transport Access Nodes” (ever asked a helpful stranger for directions to the nearest access node?), when you download the CSV the much more sensible filename is “Stops.csv”.


To load it into ClickHouse, run:



```
CREATE TABLE stops ENGINE = Memory AS
SELECT * FROM file('Stops.csv', 'CSVWithNames')
SETTINGS format_csv_allow_single_quotes = 0

```

First, we have to get the data the way we need it. Many stations have many rows, one for each entrance, bus stop, taxi rank, platform, etc. To get this down to one row per station let’s filter on just London Underground platforms (there is a 211\-page [schema guide](http://naptan.dft.gov.uk/naptan/schema/2.4/doc/NaPTANSchemaGuide-2.4-v0.57.pdf) in case you’re wondering how we knew what to filter on):



```
SELECT * FROM stops
WHERE (StopType = 'PLT') AND (CommonName LIKE '%Underground%')

```

There will still be multiple rows per station but they all seem to be completely identical, so let’s just group them into one:



```
SELECT
       CommonName AS Name,
       any(Longitude) AS Lon,
       any(Latitude) AS Lat
FROM stops
WHERE (StopType = 'PLT') AND (CommonName LIKE '%Underground%')
GROUP BY CommonName

```

How do we find the stations that are closest to each other? Like this:



```
SELECT Name,Lat, Lon,
    lagInFrame(Name) OVER (Rows BETWEEN 1 PRECEDING AND 1 PRECEDING) AS PrevName,
    lagInFrame(Lat) OVER (Rows BETWEEN 1 PRECEDING AND 1 PRECEDING) AS PrevLat,
    lagInFrame(Lon) OVER (Rows BETWEEN 1 PRECEDING AND 1 PRECEDING) AS PrevLon,
    geoDistance(Lon, Lat, PrevLon, PrevLat) AS Distance
FROM (
    SELECT CommonName AS Name, any(Longitude) AS Lon, any(Latitude) AS Lat
    FROM stops
    WHERE (StopType = 'PLT') AND (Name LIKE '%Underground%')
    GROUP BY CommonName
    ORDER BY Lat * Lon ASC
)
ORDER BY Distance ASC

```

Stations close to each other will have almost exactly the same latitude and longitude, so the product of the two will be almost exactly the same. Sorting the result set by `Lat * Lon` causes each station to be sorted next to the station closest to it. Then we use a window function to find the previous row (so the closest station to this station), calculate the distance between the two and order by that.


Turns out the two closest stations are not two different stations at all! At a distance of just 4 meters, “Heathrow Terminals 1\-2\-3 Underground Station” and “Heathrow Terminals 2 \& 3 Underground Station” are really more or less the same station. The next result, however, is what we are looking for: Queensway and Bayswater are two separate stations at the opposite end of a city block. Google Maps says it takes 2 minutes to walk from one to the other. Why are there two stations so close to each other? Well, they serve different tube lines: Queensway is a stop on the Central line, Bayswater is served by the Circle and District lines. If you ever visit London and have a choice between the two, avoid the former and go with the latter. You’ll thank me, especially in summer.


**Reading Corner**


What we’ve been reading:


1. [How We Optimize Complex Queries at Processing Time](https://www.instana.com/blog/optimize-complex-columnar-queries/) Instana wrote about how they use materialized views and tagging of incoming data to speed up recurring complex queries in ClickHouse.
2. [Full\-Text Search with Quickwit and ClickHouse in a Cluster\-to\-Cluster Context](https://engineering.contentsquare.com/2022/quickwit-and-ch-in-cluster-context/) Contentsquare is using open source search engine Quickwit (written in Rust) to combine analytical queries in ClickHouse with full text search capabilities.
3. [ClickHouse scalability and power for building data\-intensive applications](https://cube.dev/blog/clickhouse-scalability-for-data-intensive-apps) Cube explains in detail how ClickHouse can be used to underpin analytics dashboards and how Cube are interacting with it in their headless BI platform.
4. [DENIC Improves Query Times By 10x with ClickHouse](https://clickhouse.com/blog/denic-improves-query-times-by-10x-with-clickhouse/): DENIC manages all registrations for the .de domain. Read about how they chose ClickHouse for their in\-house analytics platform.
5. [How QuickCheck uses ClickHouse to bring banking to the Unbanked](https://clickhouse.com/blog/how-quickcheck-uses-clickhouse-to-bring-banking-to-the-unbanked/): QuickCheck moved analytical queries from PostgreSQL to ClickHouse, query times went from “forever” to “instant”!
6. [Amsterdam Meetup With The ClickHouse Team – June 8th, 2022](https://clickhouse.com/blog/amsterdam-meetup-with-the-clickhouse-team/): Thanks to all who joined us in person in Amsterdam. Catch up on the recording here.
7. [ClickHouse Over the Years with Benchmarks](https://clickhouse.com/blog/clickhouse-over-the-years-with-benchmarks/): At ClickHouse, we are obsessed with benchmarks! Read here how we tested every ClickHouse version.
8. [Collecting Semi\-structured Data from Kafka Topics Using ClickHouse Kafka Engine](https://clickhouse.com/blog/collecting-semi-structured-data-from-kafka-topics-using-clickhouse-kafka-engine/): In a guest post, Superology writes about how to ingest protocol buffers from Kafka into ClickHouse.
9. [ClickHouse \+ Cumul.io](https://clickhouse.com/blog/optimizing-your-customer-facing-analytics-experience-with-cumul-io-and-clickhouse/): Cumul.io writes about using their customer\-facing analytics dashboarding technology with ClickHouse.
10. [ClickHouse \+ Deepnote](https://clickhouse.com/blog/clickhouse-deepnote-data-notebooks-collaborative-analytics/): Announcing a new integration between collaborative data notebook Deepnote and ClickHouse!
11. [New ClickHouse Adopters](https://clickhouse.com/docs/en/introduction/adopters/): Welcome crypto \& NFT visual explorer [Santiment](https://www.santiment.net/), security data lake [Dassana](https://lake.dassana.io/), JSON data visualization platform [GraphJSON](https://www.graphjson.com/guides/about), and privacy\-friendly tag manager [Scale8](https://scale8.com). Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team


Photo by [delfi de la Rua](https://unsplash.com/@delfidelarua7?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/map?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

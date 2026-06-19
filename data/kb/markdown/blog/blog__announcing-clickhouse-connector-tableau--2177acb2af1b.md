# Announcing the official ClickHouse Connector for Tableau


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing the official ClickHouse Connector for Tableau

![](/_next/image?url=%2Fuploads%2FLuke_Gannon_NE_4_J_5562a05272.jpeg&w=96&q=75)[Luke Gannon](/authors/luke-gannon)Feb 27, 2025 · 13 minutes readHave you been looking to visualize data stored in ClickHouse with [Tableau](https://www.tableau.com/en-gb)? Today, you can with the launch of the official [ClickHouse Tableau Connector](https://exchange.tableau.com/en-gb/products/1064)!


Businesses deal with massive amounts of data, making it challenging to spot trends and make informed decisions. This new connector bridges that gap, letting you turn data stored within your ClickHouse database into clear, actionable insights \- whether you're analyzing sales figures, user behavior, or other key metrics, the ClickHouse Connector for Tableau makes it easy to visualize data in your Tableau dashboard.


If you want to get started right away, you can download the official connector right now from the [Tableau Exchange](https://exchange.tableau.com/en-gb/products/1064).


## ClickHouse \+ Tableau \= Superfast Dashboards [\#](/blog/announcing-clickhouse-connector-tableau#clickhouse--tableau--superfast-dashboards)


Our connector has been designed and tested to provide the best\-in\-class experience for working with any data that has been stored in ClickHouse, regardless of whether you plan to use it with Tableau Desktop or [Tableau Server](https://www.tableau.com/en-gb/products/server) (see [“What about Tableau Cloud”](/blog/announcing-clickhouse-connector-tableau#what-about-tableau-cloud) for working with Tableau Cloud)


This blog will explain how to query your data in ClickHouse Cloud using Tableau Desktop and how to use data stored in ClickHouse with Tableau Cloud.


![0_tableau.png](/uploads/0_tableau_8a9390e69e.png)
*Our example worksheet in Tableau Desktop*
### 98% compatibility score in Tableau's official testing [\#](/blog/announcing-clickhouse-connector-tableau#98-compatibility-score-in-tableaus-official-testing)


The ClickHouse Tableau Connector has achieved a 98% compatibility score in Tableau's Data Source Verification Tool (TDVT) \- well above their partner requirement of 90%. This represents the **highest compatibility score for any ClickHouse connector**, demonstrating our commitment to quality and reliability.



```
Test Count: 838 tests
	Passed tests: 820
	Failed tests: 18
	Tests run: 838
	Disabled tests: 0
	Skipped tests: 0

```

For transparency, the remaining 2% relates primarily to specific Time and Date formats not currently supported in ClickHouse's underlying database.


We plan to continue to invest in the connector as we unlock more features within the ClickHouse database for compatibility with Tableau.


## How to use the Tableau Connector? [\#](/blog/announcing-clickhouse-connector-tableau#how-to-use-the-tableau-connector)


The simplest way to get started with the connector is to use [ClickHouse Cloud](https://clickhouse.com/docs/cloud/get-started/cloud-quick-start) and [Tableau Desktop](https://www.tableau.com/en-gb/support/releases). Let me walk you through getting the connector set up and creating a quick and simple dashboard based on the [UK property price dataset](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid) that is easily accessible to play along with.


You can find the connector in the [Tableau Exchange](https://exchange.tableau.com/en-GB/products/1064) or directly within Tableau Desktop. We will show you how you can install the connector below from within Tableau Desktop.


![1_tableau.png](/uploads/1_tableau_3e2df020b8.png)
*The ClickHouse connector is available within the [Tableau Exchange](https://exchange.tableau.com/)*
### Prerequisites [\#](/blog/announcing-clickhouse-connector-tableau#prerequisites)


The first thing you’ll need to verify is that you have access to the following versions or above, use the links provided below to download:


- [Tableau Desktop](https://www.tableau.com/en-gb/support/releases) **2020\.4\+**
- [ClickHouse JDBC Driver](https://github.com/ClickHouse/clickhouse-java/releases/latest) **0\.8\.1\+**
- ClickHouse Cloud **24\.10\+**


You can [sign up for a trial](https://console.clickhouse.cloud/signUp) with ClickHouse Cloud and get started right away with $300 of credit to familiarize yourself with the service on either AWS, GCP, or Azure.


### Get your connection details [\#](/blog/announcing-clickhouse-connector-tableau#get-your-connection-details)


Once you’ve created your service or if you’re using an existing one, you will first need to gather your connection details to the ClickHouse service.


The quickest way to do this is to copy your connection details that are located behind the connect button within ClickHouse Cloud. Make a note of the following credentials and keep them ready for in a few steps:


- Host
- Port
- Username
- Password


![2_tableau.png](/uploads/2_tableau_d15464c911.png)
Note: It’s worth downloading your credentials for use later when you create your service, otherwise, if you lose your password, you’ll need to use the reset functionality found in the `connect` modal.


We will create a quick dashboard for this blog post using the `uk_price_paid` dataset. If you want to follow along, follow the [dataset tutorial](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid) located within our documentation, which walks you through table creation, loading the data, and validating what has been loaded.


### Prepare your environment [\#](/blog/announcing-clickhouse-connector-tableau#prepare-your-environment)


The Tableau Connector utilizes our JDBC Driver under the covers to establish and maintain a connection between Tableau Desktop, the ClickHouse Connector, and your ClickHouse service.  

Next, you will need to download our JDBC driver from our [Official GitHub repository](https://github.com/ClickHouse/clickhouse-java/releases) and locate our [latest release](https://github.com/ClickHouse/clickhouse-java/releases/latest) (at the time of writing, [jdbc\-v2\-0\.8\.1\.jar](https://github.com/ClickHouse/clickhouse-java/releases/download/v0.8.1/jdbc-v2-0.8.1.jar) is available for download).


Once this is downloaded and located, you will need to add the JDBC driver to the correct location. This step is dependent on your operating system and the system paths are outlined below:


- macOS: `~/Library/Tableau/Drivers`
- Windows: `C:\Program Files\Tableau\Drivers`


If the `Drivers` folder doesn’t already exist on your machine, you will need to create a path like the ones outlined above.


### Adding the connector to Tableau Desktop [\#](/blog/announcing-clickhouse-connector-tableau#adding-the-connector-to-tableau-desktop)


Now we’ve set up a service within ClickHouse cloud and loaded the property dataset as a Table; [installed Tableau Desktop](https://www.tableau.com/en-gb/products/desktop/download) along with the [ClickHouse JDBC Driver](/blog/announcing-clickhouse-connector-tableau#prepare-your-environment) placed in the correct location; we can now install the Connector.


From the Connect page, click ‘More’ under the ‘To a Server’ section and search for ‘ClickHouse’.


![3_tableau.png](/uploads/3_tableau_be9c612772.png)
*Locating the ClickHouse connector from within Tableau Desktop*
This will install the connector and prompt you to enter the connection details that you gathered in the prerequisite step.


![4_tableau.png](/uploads/4_tableau_9e2658e6fd.png)
*ClickHouse connection details*
Once connected, you can add multiple connections to different databases, choose whether to keep a live connection, extract the data, view related tables, and more. I suggest using a live connection to update the data displayed in real\-time.


![5_tableau.png](/uploads/5_tableau_2d5892725d.png)
*Tableau Desktop Data Source Connector Management Screen*
## Creating a dashboard [\#](/blog/announcing-clickhouse-connector-tableau#creating-a-dashboard)


Now that we have connected Tableau to ClickHouse, we can create our first dashboard! We’re going to create a couple of visualizations to plot on our dashboard.


In this dashboard, I’ll create a filter that when I select a particular district within the UK, displays the areas within that district on an interactive map and displays the median property prices for that district by property type.


### Understanding median properties by district [\#](/blog/announcing-clickhouse-connector-tableau#understanding-median-properties-by-district)


The first thing we’d like to have on our dashboard is an understanding of how different property types (flats vs detached houses) vary in prices. It’s really simple to create a chart from within Tableau.


I’m just going to drag my different columns available from my data source from the right hand side into my columns and rows within the worksheet.


![6_tableau.png](/uploads/6_tableau_009876f338.png)
*Available columns in our UK price data table*
By default, Tableau sums up integers, but in our example, we’re going to find the median property price by property type. To change this, you can use the dropdown menu from the Price pill within Rows, changing the measure from Sum to Median.


![7_tableau.png](/uploads/7_tableau_6d9e5fd817.png)
*Changing the Price aggregation type to Median*
Great! Now we have our table view that shows the median property price by property type.


![8_tableau.png](/uploads/8_tableau_8cdf95e26f.png)
*Median Property Price by Property Type Table*
I will add `District` to the filters so that when we add this worksheet to our dashboard when I filter one visualization, it will also filter the other.


### Plotting our data on a Map [\#](/blog/announcing-clickhouse-connector-tableau#plotting-our-data-on-a-map)


Tableau is great for making interactive visualization dashboards and our dataset has postcode data, Tableau is great at providing utilities to convert address data (postcode1\) into longitude and latitude, along with plotting these on a map. You’ll notice that underneath our Table data fields, there are green ones that Tableau generates for us, we can drag the longitude and latitude onto a new worksheet’s columns and rows.


![9_tableau.png](/uploads/9_tableau_b850b3ae07.png)
*Utilizing Tableau\-generated data fields for our visualization*
Because Tableau recognizes what type of data we’re using, you can see that it instantly plots these lat longs onto a map. This is cool but not very useful just yet.


![10_tableau.png](/uploads/10_tableau_e89f64ee15.png)
*Generated longitudes and latitudes plotted from our UK price data*
Changing the Marks type from automatic to specifically be Map and attaching that to Postcodes, Tableau now creates colored areas representing the different postcodes located within the UK. This is super neat!


![11_tableau.png](/uploads/11_tableau_7204fd46bc.png)
*Coloring the map randomly by postcode*
Having each of the postcodes colored isn’t too useful, so instead of the postcode data dictating the color of each area. Let’s drag over from the left hand navigation some more data fields to use within our visualization and aggregate them differently.


Adding an extra postcode data fields and counting them will tell us how many properties have been sold within that postcode. We can also drag the price data fields twice and compute the min and max values for that postcode. This will be added to our tooltip when we hover over the map.


![12_tableau.png](/uploads/12_tableau_414fb52a2c.png)
*Map visualization that increases colour intensity based on the number of sold properties within a postcode*
Setting the color, we can see that in the southern region of the UK, the London borough of Croydon (CR0\) is a property hotspot with 69K entries, meaning it's a high turnover area in London.


#### Plotting Median Prices [\#](/blog/announcing-clickhouse-connector-tableau#plotting-median-prices)


We can go a step further and calculate the median property price for a postcode. As you can see, when we use the median price, we don't get too much of a visual distinction between areas because of the skew in property prices.


![13_tableau.png](/uploads/13_tableau_04db066c12.png)
*Bad visualization: Plotting median price on a map*
#### Calculation to the rescue [\#](/blog/announcing-clickhouse-connector-tableau#calculation-to-the-rescue)


To overcome this, I will use a rudimentary log function to help flatten the prices out by scaling the median price. Creating a new Data Field is really simple by right\-clicking in the Data area and selecting “Calculated Data Field”. We can use many built\-in functions to achieve this, so we’re going to wrap the Median price as a Log function using base 2\.


![20_tableau.png](/uploads/20_tableau_95371e1e75.png)
*Calculated data field modal*
In the dataset, we store UK postcodes as two separate fields. We can also use calculated fields for other neat tricks, like merging two columns together. This allows us to make things more human\-readable or add prefixes/suffixes without modifying the database directly.


![14_tableau.png](/uploads/14_tableau_153ba7c7f1.png)
*Calculation example of joining our two postcode columns together easily*
Now we have our new Calculated Data Field with our price data log scaled, we can set the map color in Marks to use that data field. You will notice that we are given a legend on the right hand side showing a scale of color to value. When you hover over it, there is a drop\-down menu selector where Edit Colours is an option.


![15_tableau.png](/uploads/15_tableau_11639ad35a.png)
*Setting the steps of the scale for color intensity*
Having played around a little bit with the style, changing the steps to 10 gave me a nicer distinction compared to 5\. I encourage you to play around with the number of steps and the color palette depending on your use case and preference.


![16_tableau.png](/uploads/16_tableau_2e35b8c41a.png)
*Better Visualization: Plotting Median Price on a Map*
I will also add `District` to the filters so that when we add this worksheet to our dashboard, when I filter one visualization, it will also filter the other.


### Adding to Dashboard and Linking Filters [\#](/blog/announcing-clickhouse-connector-tableau#adding-to-dashboard-and-linking-filters)


Now, we can drag over our two worksheets onto a new dashboard. This will give us two filter sections, we only need one and can link it. You have finer\-grained controls to select which worksheet it controls, but for simplicity, I’m going to have a single filter for any worksheet that uses this related data source.


![17_tableau.png](/uploads/17_tableau_2838fa29f2.png)
*Changing the filter to modify all worksheets within our dashboard*
#### Voila! Simple Prices Dashboard [\#](/blog/announcing-clickhouse-connector-tableau#voila-simple-prices-dashboard)


Now that we have added our two worksheets to the same dashboard, made our filter affect any worksheet using the data source we can give it a road test:


![18_tableau.gif](/uploads/18_tableau_dca9d9e5c4.gif)
*Dashboard made with the Tableau ClickHouse Connector*
There we have it, a simple dashboard in Tableau within 10 minutes! I hope this gives you some ideas for how you can get started visualizing your data from ClickHouse in Tableau Desktop or Server.


## What about Tableau Cloud? [\#](/blog/announcing-clickhouse-connector-tableau#what-about-tableau-cloud)


When working with Tableau Cloud, you will need to use the MySQL interface. This has to be enabled within ClickHouse Cloud on the Connect your app screen. When you have enabled the interface, it will expose port 3306 and create a MySQL user. The MySQL user will inherit the Default user password and privileges. If you want to [create multiple MySQL users](https://clickhouse.com/docs/integrations/tableau-online#creating-multiple-mysql-users-in-clickhouse-cloud), follow the steps outlined in the documentation.


![19_tableau.png](/uploads/19_tableau_f9aeb33052.png)
*[Enabling the MySQL interface in ClickHouse Cloud](https://clickhouse.com/docs/integrations/tableau-online#clickhouse-cloud-setup)*
We’re working to get a native Tableau Cloud connector available for usage, if this is something you’re interested in, please [reach out](https://clickhouse.com/company/contact). In the meantime, you can access ClickHouse in Tableau Cloud through our MySQL interface.


## Get in touch! [\#](/blog/announcing-clickhouse-connector-tableau#get-in-touch)


We’re excited to hear what dashboards and visualizations you’ll create with Tableau. If you have any [questions](https://clickhouse.com/company/contact) or want to provide future enhancement requests, please raise an issue in the [ClickHouse Tableau Connector GitHub repository](https://github.com/ClickHouse/clickhouse-tableau-connector-jdbc).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

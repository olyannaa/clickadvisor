# Global weather data from flying airplanes


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Global weather data from flying airplanes

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Nov 3, 2025 · 8 minutes readRecently, I read the blog post by [Niklas Oberhuber](https://obrhubr.org/adsb-weather-model) showing that it is possible to derive weather data from airplane telemetry. Airplanes don't broadcast temperature or wind data, but it can be calculated on the fly from other parameters. I immediately decided to reproduce these calculations to show something beautiful!


[ADS\-B Massive Visualizer](https://adsb.exposed/) collects telemetry from airplanes, such as their position, altitude, speed, and heading. This data is saved in the ClickHouse database. The service provides access to custom reports on top of over 150 billion data points and counting, accumulating them in real time.


You can read more about the service in the previous [blog post](https://clickhouse.com/blog/interactive-visualization-analytics-adsb-flight-data-with-clickhouse).


![title2.png](/uploads/title2_f2f62c67b6.png)
## Sensors [\#](/blog/planes-weather#sensors)


Aircraft have many air pressure sensors, named "pitot tubes", which measure how the aircraft moves through the air. Static air pressure will show the altitude, and dynamic air pressure will show the airspeed relative to the air. These pressure sensors are the most important for flying dynamics.


Aircraft also have various navigation systems, which can show the altitude, speed, and heading, relative to the Earth. These measurements are less important to how the aircraft flies, but more important to navigation.


If we compare the values of these measurements to each other, we can derive more data. For example, comparing the airspeed with geometric speed will show us the speed of the tailwind (or headwind). Comparing the altitude from the pressure sensors with the geometric altitude could give some information about the local pressure changes and, maybe, temperature. Finally, comparing the heading relative to the air with the geometric heading will give us information about the wind direction.


## Visualizations [\#](/blog/planes-weather#visualizations)


Let's suppose we want to visualize the angle (0\..360 degrees) on the map. How to do it? We can use the color circle! So, different angles will be shown as different hues of color. For this purpose, ClickHouse provides functions for [conversions between color spaces](https://presentations.clickhouse.com/2025-release-25.7/#9): `colorOKLCHToSRGB` and `colorSRGBToOKLCH`.


The color space that most of the displays and graphic cards use is named sRGB, and contains three channels (Red, Green, and Blue) that are Gamma\-corrected (they are non\-linear to provide more resolution to darker colors, as they are easier to distinguish relatively to each other than the brighter colors).


There is another color space, named [OKLCH](https://oklch.com/). It contains three channels: Lightness, Chroma, and Hue. It is cylindrical, because the L and C channels range in the line (say, between 0 and 1; however, some of the values can be out of range of the display device), and the Hue channel is circular (represents an angle between 0 and 360\). It is designed to be linear (which means, if we do a linear gradient in that color space, the gradient will look okay, hence the name) and intended to be perceptually uniform (which means, if you average between two colors in that space, the resulting color is also perceived as the average; if you fix the Lightness and Chroma and change the Hue, the result will be perceived as having the same brightness).


Let's map aircraft headings using this color space:


[![heading.png](/uploads/heading_87061b8bfa.png)](https://adsb.exposed/?dataset=Planes&zoom=5&lat=36.0314&lng=-98.4165&query=ed99deb24cc4f2a2026034df3d7dd447)


## Pressure [\#](/blog/planes-weather#pressure)


Let's filter data for airplanes at least at 10,000 feet and map the difference between the `altitude` and `geometric_altitude` for a certain day:


[![pressure.png](/uploads/pressure_4c97106659.png)](https://adsb.exposed/?dataset=Planes&zoom=5&lat=37.1785&lng=-95.2295&query=d095cd7b312291b682d3c9f1dafad188)


This looks surprisingly beautiful! Even more interesting, the picture changes if you select a different day.



Visualization of the air pressure difference across the US during 25 days starting from Apr 2, 2025\. Each frame represents a 24\-hour sliding window, and frames advance by 6 hours.
I didn't derive the actual temperature from this data. The formula from Wikipedia looks complex, and I didn't want to apply it. Niklas Oberhuber also didn't use the formula but created a model instead. And I was just satisfied with nice pictures.


## Crabbing angle [\#](/blog/planes-weather#crabbing-angle)


When there is a strong but consistent crosswind, airplanes fly pointed into the wind. They can even land while pointed into the wind, which is called "crabbing". In the ADS\-B data, there are two fields: one is `track_degrees`, which means the angle the plane points to, and another is `aircraft_true_heading`, which means the angle relative to the moving air around the airplane. If we subtract one angle from another, we will get the "crabbing" angle. Let's visualize it:


[![crabbing.png](/uploads/crabbing_319dc835ee.png)](https://adsb.exposed/?dataset=Planes&zoom=5&lat=45.4119&lng=4.8697&query=6b7872ee6c34260ef470f5fd675f7d58)


Unfortunately, most of the data is not available in the US, but it is available in the EU. Probably, it is due to some local regulations.


## Wind [\#](/blog/planes-weather#wind)


Now let's calculate the wind direction and speed. It will require some trigonometry, and trying to understand these formulas is difficult without a pen and paper.


Here is the "crabbing angle" (or name it "drift angle") we calculated in the previous step:



```
positiveModulo(track_degrees - aircraft_true_heading + 180, 360) - 180 AS drift_angle,

```

The wind speed can be calculated in the following way: draw a triangle with the `ground_speed` as one side and the `aircraft_tas` (airspeed) as the other side, with the angle `drift_angle` between these two sides. The length of the other side (the difference between the vectors of `ground_speed` and `aircraft_tas`) is the wind speed:



```
sqrt(
    pow(ground_speed, 2) + pow(aircraft_tas, 2) -
    2 * ground_speed * aircraft_tas * cos(radians(drift_angle))
) AS wind_speed,

```

Use a similar rule to calculate the absolute wind direction angle:



```
positiveModulo(track_degrees +
    if(drift_angle < 0, -1, 1) * degrees(acos(
        greatest(-1, least(1,
            (pow(ground_speed, 2) + pow(wind_speed, 2) - pow(aircraft_tas, 2)) /
            (2 * ground_speed * if(wind_speed > 0.1, wind_speed, 1))
        ))
    )) + 180, 360
) AS wind_direction,

```

We would like to show the wind direction on the map. But sometimes one pixel on the map will contain multiple data points, and we need to aggregate them to calculate the average. How to calculate the average of angles, e.g., what is the average between 10 degrees and 350 degrees? (The answer should be zero.) Actually, we need even more: calculate the weighted average of wind direction angles with the wind speed as the weight, so the stronger wind will have a bigger contribution.


To do this, let's say that the wind direction and wind speed are polar coordinates of the wind vector. And what we need in the result is the average wind vector. The average is a function in the linear coordinate space, which is why we can't apply it simply in the polar coordinates. We can do a coordinate transform of the function, but put it more simply, we should convert our (direction, speed) coordinates to linear (x, y), then do the average across both x and y coordinates, then convert it back to the polar space and take the angle back as the average:



```
positiveModulo(degrees(atan2(
    avg(sin(radians(wind_direction)) * wind_speed),
    avg(cos(radians(wind_direction)) * wind_speed)
)), 360) AS avg_wind_direction,

```

Now, given the wind angle and wind speed, it will be natural to map the angle to the color hue and the speed to the color lightness:


[![wind.png](/uploads/wind_edc9f29b7d.png)](https://adsb.exposed/?dataset=Planes&zoom=5&lat=45.4119&lng=4.8697&query=ec1376e91336d70a77914a6ea2c22acc)


I compared the resulting picture to the actual weather data at <https://earth.nullschool.net/> and it looked exactly as expected!



Visualization of the wind across Europe during 25 days starting from Jan 1, 2025\. Each frame represents a 24\-hour sliding window, and frames advance by 6 hours.
## Bottom line [\#](/blog/planes-weather#bottom-line)


ADS\-B is a treasure trove of data, and it really shines when it is queryable in real\-time with ClickHouse.


Bonus: how to do video visualizations. Prepare a query [as follows](https://pastila.nl/?03f73efc/6e0a10a5586f9a049a6747c36feb7373#oCbctgncESvUFSUc8eteyg==). Copy it to adsb.exposed. Open the browser console. Copy and run the following snippet: `frame = 0; const id = setInterval(() => { query_elem.value = query_elem.value.replace(/(\d+) AS frame/,` ${frame} AS frame`); updateMap(); if (frame >= 100) { clearInterval(id) }; ++frame; }, 10000)`. The first run is needed to bring the images to the cache. After it finishes, replace the update interval to one second, start `recordmydesktop` and repeat the run. The generated video can be processed with ffmpeg as follows: `ffmpeg -y -i out.ogv -ss 4.5 -to 105 -filter:v "crop=2149:1218:893:666,thumbnail=15,setpts=0.1*PTS" -qscale:v 10 -an pressure.ogv`, where the time offsets are found manually by looking at the video, and crop frame is determined by taking a screenshot and using the selection tool in the graphic editor. The ffmpeg invocation is constructed by Claude.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

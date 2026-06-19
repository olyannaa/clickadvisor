---
source: blog
url: https://ensembleanalytics.io/blog/forecasting-using-clickhouse
topic: forecasting-using-clickhouse-machine-learning-functions
ch_version_introduced: '0.002'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 8
---

as Dummy8, if(toMonth(toDate(MONTH)) = 9, 1, 0) as Dummy9, if(toMonth(toDate(MONTH)) = 10, 1, 0) as Dummy10, if(toMonth(toDate(MONTH)) = 11, 1, 0) as Dummy11, if(toMonth(toDate(MONTH)) = 12, 1, 0) as Dummy12 FROM flight_data ORDER BY AIRLINE, DEPARTURE_AIRPORT, MONTH ```

This creates the following view which summarises our dependent and independent variables:

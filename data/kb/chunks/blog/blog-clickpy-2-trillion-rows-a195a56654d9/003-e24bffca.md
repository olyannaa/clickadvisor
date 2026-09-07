---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickPy
topic: clickpy-at-2-trillion-rows-scaling-ingestion-and-fixing-the-past-clickhouse
ch_version_introduced: '2.21'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 6
---

the new pipeline from production. We cloned all table schemas and materialized views from the `pypi` database into a separate database called `pypi_clickpipes`. This allowed us to validate ingestion, transformations, and aggregations without affecting existing queries or dashboards.

```
-- Create the database
CREATE DATABASE pypi_clickpipes;

-- Clone the table schemas
CREATE TABLE pypi_clickpipes.pypi AS pypi.pypi;
CREATE TABLE pypi_clickpipes.pypi_downloads AS pypi.pypi_downloads;
CREATE TABLE pypi_clickpipes.pypi_downloads_by_version AS pypi.pypi_downloads_by_version;
CREATE TABLE pypi_clickpipes.pypi_downloads_max_min AS pypi.pypi_downloads_max_min;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day AS pypi.pypi_downloads_per_day;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_installer AS pypi.pypi_downloads_per_day_by_installer;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version AS pypi.pypi_downloads_per_day_by_version;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_country AS pypi.pypi_downloads_per_day_by_version_by_country;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_file_type AS pypi.pypi_downloads_per_day_by_version_by_file_type;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_installer_by_type AS pypi.pypi_downloads_per_day_by_version_by_installer_by_type;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_installer_by_type_by_country AS pypi.pypi_downloads_per_day_by_version_by_installer_by_type_by_country;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_python AS pypi.pypi_downloads_per_day_by_version_by_python;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_python_by_country AS pypi.pypi_downloads_per_day_by_version_by_python_by_country;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_system AS pypi.pypi_downloads_per_day_by_version_by_system;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_day_by_version_by_system_by_country;
CREATE TABLE pypi_clickpipes.pypi_downloads_per_month AS pypi.pypi_downloads_per_day_by_version_by_system_by_country;
```
Copy command
With the clone table in place, we configured ClickPipes to ingest data from GCS to a new target table `pypi_raw`. ClickPipes automatically creates the table and infer the schema at the first ingestion. This table acts as a transient staging layer.

![CleanShot 2026-01-21 at 11.54.40.png](/_next/image?url=%2Fuploads%2FClean_Shot_2026_01_21_at_11_54_40_4c69f7d87b.png&w=2048&q=75)

In the configuration, we intentionally use the `Null` engine for the target table. We do not need to persist raw rows in ClickHouse. Instead, a materialized view performs the transformation and writes directly to the `pypi` table, which contains the main dataset.

A new materialized view encapsulates all transformation logic that previously lived in the custom script: field normalization, type conversions, and schema alignment. Moving this logic into ClickHouse makes it easier to reason about and evolve over time.

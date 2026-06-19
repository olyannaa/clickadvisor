---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/embedded-dict-functions.md)#
topic: functions-for-working-with-embedded-dictionaries-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 6
---

— Dictionary key. See [Multiple Geobases](#multiple-geobases). [String](/docs/sql-reference/data-types/string). Optional. **Returned value** - Region ID for the appropriate area, if it exists. [UInt32](/docs/sql-reference/data-types/int-uint). - 0, if there is none. **Example** ``` SELECT DISTINCT regionToName(regionToArea(toUInt32(number), 'ua')) FROM system.numbers LIMIT 15 ```

```
┌─regionToName(regionToArea(toUInt32(number), \'ua\'))─┐
│                                                      │
│ Moscow and Moscow region                             │
│ St. Petersburg and Leningrad region                  │
│ Belgorod region                                      │
│ Ivanovsk region                                      │
│ Kaluga region                                        │
│ Kostroma region                                      │
│ Kursk region                                         │
│ Lipetsk region                                       │
│ Orlov region                                         │
│ Ryazan region                                        │
│ Smolensk region                                      │
│ Tambov region                                        │
│ Tver region                                          │
│ Tula region                                          │
└──────────────────────────────────────────────────────┘

```

### regionToDistrict[​](#regiontodistrict "Direct link to regionToDistrict")

Converts a region to a federal district (type 4 in the geobase). In every other way, this function is the same as 'regionToCity'.

**Syntax**

```
regionToDistrict(id [, geobase])

```

**Parameters**

- `id` — Region ID from the geobase. [UInt32](/docs/sql-reference/data-types/int-uint).
- `geobase` — Dictionary key. See [Multiple Geobases](#multiple-geobases). [String](/docs/sql-reference/data-types/string). Optional.

**Returned value**

- Region ID for the appropriate city, if it exists. [UInt32](/docs/sql-reference/data-types/int-uint).
- 0, if there is none.

**Example**

```
SELECT DISTINCT regionToName(regionToDistrict(toUInt32(number), 'ua'))
FROM system.numbers
LIMIT 15

```

```
┌─regionToName(regionToDistrict(toUInt32(number), \'ua\'))─┐
│                                                          │
│ Central federal district                                 │
│ Northwest federal district                               │
│ South federal district                                   │
│ North Caucases federal district                          │
│ Privolga federal district                                │
│ Ural federal district                                    │
│ Siberian federal district                                │
│ Far East federal district                                │
│ Scotland                                                 │
│ Faroe Islands                                            │
│ Flemish region                                           │
│ Brussels capital region                                  │
│ Wallonia                                                 │
│ Federation of Bosnia and Herzegovina                     │
└──────────────────────────────────────────────────────────┘

```

### regionToCountry[​](#regiontocountry "Direct link to regionToCountry")

Converts a region to a country (type 3 in the geobase). In every other way, this function is the same as 'regionToCity'.

**Syntax**

```
regionToCountry(id [, geobase])

```

**Parameters**

- `id` — Region ID from the geobase. [UInt32](/docs/sql-reference/data-types/int-uint).
- `geobase` — Dictionary key. See [Multiple Geobases](#multiple-geobases). [String](/docs/sql-reference/data-types/string). Optional.

**Returned value**

- Region ID for the appropriate country, if it exists. [UInt32](/docs/sql-reference/data-types/int-uint).
- 0, if there is none.

**Example**

```
SELECT regionToName(number::UInt32, 'en'), regionToCountry(number::UInt32) AS id, regionToName(id, 'en') FROM numbers(13);

```

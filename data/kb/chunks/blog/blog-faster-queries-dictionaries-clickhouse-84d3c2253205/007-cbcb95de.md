---
source: blog
url: https://clickhouse.com/blog/real-world-data-noaa-climate-data
topic: using-dictionaries-to-accelerate-queries
ch_version_introduced: '45.8'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 15
---

However, it is limited in that the key size can also not exceed 500k \- although this is configurable via the setting [`max_array_size`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#flat). It is also inherently less efficient on large sparse distributions, wasting memory in such cases.

For cases where you have a very large number of entries, large key values, and/or a sparse distribution of values, then [`flat`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#flat) layout becomes less optimal. At this point, we would typically recommend a hash\-based dictionary \- specifically the [`hashed_array`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#dicts-external_dicts_dict_layout-hashed-array) dictionary, which can efficiently support millions of entries. This layout is more memory efficient than the [`hashed`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#dicts-external_dicts_dict_layout-hashed) layout and almost as fast. For this type, a hash table structure is used to store the primary key, with values providing offset positions into the attribute\-specific arrays. This is in contrast [`hashed`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#dicts-external_dicts_dict_layout-hashed) layout, which, although a little faster, requires a hash table to be allocated for each attribute \- thus consuming more memory. In most cases, we, therefore, recommend the [`hashed_array`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#dicts-external_dicts_dict_layout-hashed-array) layout \- although users should experiment with [`hashed`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#dicts-external_dicts_dict_layout-hashed) if they have only a few attributes.

All of these types also require the keys to be castable to UInt64\. If not, e.g., they are Strings, we can use the complex variants of the hashed dictionaries: [`complex_key_hashed`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#complex-key-hashed) and [`complex_key_hashed_array`](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout/#complex-key-hashed-array), following the same rules above otherwise.

We try to capture the above logic with a flow chart below to help you choose the right layout (most of the time):

[![choosing_layout.png](/uploads/choosing_layout_c187d7c55d.png)](/uploads/choosing_layout_c187d7c55d.png)
For our data, where our primary key is the String `country_code`, we choose the `complex_key_hashed_array` type since our dictionaries have at least three attributes in each case.

Note: We also have sparse variants of the `hashed` and `complex_key_hashed` layouts. This layout aims to achieve constant time operations by splitting the primary key into groups and incrementing a range within them. We rarely recommend this layout, which is only efficient if you have only one attribute. Although operations are constant time, the actual constant is typically higher than the non\-sparse variants. Finally, ClickHouse offers specialized layouts such as [polygon](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-polygon/) and [ip\_trie](https://clickhouse.com/docs/en/sql-reference/dictionaries/external-dictionaries/external-dicts-dict-layout#ip_trie). We explored the former in the [original blog](https://clickhouse.com/blog/real-world-data-noaa-climate-data), and will save others for future posts since they represent more advanced use cases.

### Choosing a lifetime [\#](/blog/faster-queries-dictionaries-clickhouse#choosing-a-lifetime)

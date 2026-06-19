---
source: blog
url: https://clickhouse.cloud/signUp?loc=blog-cta-header&utm_source=clickhouse&utm_medium=web&utm_campaign=blog
topic: ip-based-geolocation-in-clickhouse
ch_version_introduced: '4.0'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 8
---

``` ![cidr_suffix_query.png](/uploads/cidr_suffix_query_13217669e9.png) In the results above, we can see that the `unmatched` field is effectively calculating the position of the first `1` bit from our `bitXor()` output. Subtracting this value from 32 yields our CIDR block size (suffix).

![cidr_bitwise_not_and.png](/uploads/cidr_bitwise_not_and_29f829107b.png)
Next, we’ll determine the address at which the CIDR block begins, as this will often differ from the address at the beginning of our range, especially for larger blocks. To do this, we’ll need to perform a [bitwise NOT operation](https://docs.oracle.com/cd/E41183_01/DR/Bitnot.html) `bitNot()` on the total number of addresses contained in our CIDR block, which can be expressed as `pow(2, n) - 1` where `n` is equal to the value of our `unmatched` field above. Then, we’ll compare the result with the beginning of our IP range using a [bitwise AND operation](https://support.apple.com/guide/functions/bitand-ffae6d40a070/web#:~:text=The%20BITAND%20function%20returns%20the%20bitwise%20AND%20of%20two%20numbers.&text=value%2D1%3A%20The%20first%20number,%2D2%3A%20The%20second%20number.) `bitAnd()` to determine which bits in both expressions are equal to 1\. The result can then be converted back into an IPv4 address by first casting it to `UInt64` and then applying the `toIPv4()` function:

```
select
    ip_range_start,
    ip_range_end,
    bitXor(ip_range_start, ip_range_end) as xor,
    bin(xor) as xor_binary,
    if(xor != 0, ceil(log2(xor)), 0) as unmatched,
    32 - unmatched as cidr_suffix,
    toIPv4(bitAnd(bitNot(pow(2, unmatched) - 1), ip_range_start)::UInt64) as cidr_address
from
    geoip_url
limit
    20;

```

![cidr_range_query.png](/uploads/cidr_range_query_1c3caa65d1.png)
Finally, we can concatenate our CIDR address and suffix into a single string. To make this clean, we’ll also move all of our intermediary expressions into a `WITH` clause.

```
with 
    bitXor(ip_range_start, ip_range_end) as xor,
    if(xor != 0, ceil(log2(xor)), 0) as unmatched,
    32 - unmatched as cidr_suffix,
    toIPv4(bitAnd(bitNot(pow(2, unmatched) - 1), ip_range_start)::UInt64) as cidr_address
select
    ip_range_start,
    ip_range_end,
    concat(toString(cidr_address),'/',toString(cidr_suffix)) as cidr    
from
    geoip_url
limit
    20;

```

![cidr_final_query.png](/uploads/cidr_final_query_f5a8fb03d9.png)
### Importing the transformed GeoIP Data [\#](/blog/geolocating-ips-in-clickhouse-and-grafana#importing-the-transformed-geoip-data)

For our purposes, we’ll only need the IP range, country code and coordinates, so let’s create a new table and insert our GeoIP data:

```
create table geoip (
   cidr String,
   latitude Float64,
   longitude Float64,
   country_code String
) 
engine = MergeTree() 
order by cidr;

insert into 
    geoip
with 
    bitXor(ip_range_start, ip_range_end) as xor,
    if(xor != 0, ceil(log2(xor)), 0) as unmatched,
    32 - unmatched as cidr_suffix,
    toIPv4(bitAnd(bitNot(pow(2, unmatched) - 1), ip_range_start)::UInt64) as cidr_address
select
    concat(toString(cidr_address),'/',toString(cidr_suffix)) as cidr,
    latitude,
    longitude,
    country_code    
from
    geoip_url

```

## Creating an `ip_trie` Dictionary for GeoIP Data [\#](/blog/geolocating-ips-in-clickhouse-and-grafana#creating-an-ip_trie-dictionary-for-geoip-data)

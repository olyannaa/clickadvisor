# Functions for working with URLs \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- URLs
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/url-functions.md)# Functions for working with URLs

## Overview[​](#overview "Direct link to Overview")


NoteThe functions mentioned in this section are optimized for maximum performance and for the most part do not follow the RFC\-3986 standard.
Functions which implement RFC\-3986 have `RFC` appended to their function name and are generally slower.


You can generally use the non\-`RFC` function variants when working with publicly registered domains that contain neither user strings nor `@` symbols.
The table below details which symbols in a URL can (`✔`) or cannot (`✗`) be parsed by the respective `RFC` and non\-`RFC` variants:




| Symbol non\-`RFC` `RFC`| ' ' ✗ ✗| \\t ✗ ✗| \< ✗ ✗| \> ✗ ✗| % ✗ ✔\*| { ✗ ✗| } ✗ ✗| \| ✗ ✗| \\\\ ✗ ✗| ^ ✗ ✗| \~ ✗ ✔\*| \[ ✗ ✗| ] ✗ ✔| ; ✗ ✔\*| \= ✗ ✔\*| \& ✗ ✔\* | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


symbols marked `*` are sub\-delimiters in RFC 3986 and allowed for user info following the `@` symbol.


There are two types of URL functions:


- Functions that extract parts of a URL. If the relevant part isn't present in a URL, an empty string is returned.
- Functions that remove part of a URL. If the URL does not have anything similar, the URL remains unchanged.


NoteThe functions below are generated from the `system.functions` system table.


## URLHierarchy[​](#URLHierarchy "Direct link to URLHierarchy")


Introduced in: v1\.1\.0


Returns an array containing the URL, truncated at the end by the symbols `/`, `?` and `#` in the path and query string. Consecutive separator characters are counted as one. The result includes the protocol and host as the first element, with progressively longer paths forming a hierarchy.


**Syntax**



```
URLHierarchy(url)

```

**Arguments**


- `url` — The URL to process. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array of progressively longer URLs forming a hierarchy. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
SELECT URLHierarchy('https://example.com/a/b?c=1')

```


```
['https://example.com/','https://example.com/a/','https://example.com/a/b','https://example.com/a/b?c=1']

```

## URLPathHierarchy[​](#URLPathHierarchy "Direct link to URLPathHierarchy")


Introduced in: v1\.1\.0


Returns an array containing the path component of the URL, truncated at the end by the symbols `/`, `?` and `#`. Unlike `URLHierarchy`, the result does not include the protocol and host — it starts from the path. Consecutive separator characters are counted as one.


**Syntax**



```
URLPathHierarchy(url)

```

**Arguments**


- `url` — The URL to process. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array of progressively longer URL path components forming a hierarchy. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
SELECT URLPathHierarchy('https://example.com/a/b?c=1')

```


```
['/a/','/a/b','/a/b?c=1']

```

## cutFragment[​](#cutFragment "Direct link to cutFragment")


Introduced in: v1\.1\.0


Removes the fragment identifier, including the number sign, from a URL.


**Syntax**



```
cutFragment(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the URL with fragment identifier removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT cutFragment('http://example.com/path?query=value#fragment123');

```


```
┌─cutFragment('http://example.com/path?query=value#fragment123')─┐
│ http://example.com/path?query=value                            │
└────────────────────────────────────────────────────────────────┘

```

## cutQueryString[​](#cutQueryString "Direct link to cutQueryString")


Introduced in: v1\.1\.0


Removes the query string, including the question mark from a URL.


**Syntax**



```
cutQueryString(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the URL with query string removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT cutQueryString('http://example.com/path?query=value&param=123#fragment');

```


```
┌─cutQueryString('http://example.com/path?query=value&param=123#fragment')─┐
│ http://example.com/path#fragment                                         │
└──────────────────────────────────────────────────────────────────────────┘

```

## cutQueryStringAndFragment[​](#cutQueryStringAndFragment "Direct link to cutQueryStringAndFragment")


Introduced in: v1\.1\.0


Removes the query string and fragment identifier, including the question mark and number sign, from a URL.


**Syntax**



```
cutQueryStringAndFragment(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the URL with query string and fragment identifier removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT cutQueryStringAndFragment('http://example.com/path?query=value&param=123#fragment');

```


```
┌─cutQueryStringAndFragment('http://example.com/path?query=value&param=123#fragment')─┐
│ http://example.com/path                                                             │
└─────────────────────────────────────────────────────────────────────────────────────┘

```

## cutToFirstSignificantSubdomain[​](#cutToFirstSignificantSubdomain "Direct link to cutToFirstSignificantSubdomain")


Introduced in: v1\.1\.0


Returns the part of the domain that includes top\-level subdomains up to the [first significant subdomain](/docs/sql-reference/functions/url-functions#firstSignificantSubdomain).


**Syntax**



```
cutToFirstSignificantSubdomain(url)

```

**Arguments**


- `url` — URL or domain string to process. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain if possible, otherwise returns an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    cutToFirstSignificantSubdomain('https://news.clickhouse.com.tr/'),
    cutToFirstSignificantSubdomain('www.tr'),
    cutToFirstSignificantSubdomain('tr');

```


```
┌─cutToFirstSignificantSubdomain('https://news.clickhouse.com.tr/')─┬─cutToFirstSignificantSubdomain('www.tr')─┬─cutToFirstSignificantSubdomain('tr')─┐
│ clickhouse.com.tr                                                 │ tr                                       │                                      │
└───────────────────────────────────────────────────────────────────┴──────────────────────────────────────────┴──────────────────────────────────────┘

```

## cutToFirstSignificantSubdomainCustom[​](#cutToFirstSignificantSubdomainCustom "Direct link to cutToFirstSignificantSubdomainCustom")


Introduced in: v21\.1\.0


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain. Accepts custom [TLD list](https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains) name. This function can be useful if you need a fresh TLD list or if you have a custom list.


**Configuration example**



```
<!-- <top_level_domains_path>/var/lib/clickhouse/top_level_domains/</top_level_domains_path> -->
<top_level_domains_lists>
    <!-- https://publicsuffix.org/list/public_suffix_list.dat -->
    <public_suffix_list>public_suffix_list.dat</public_suffix_list>
    <!-- NOTE: path is under top_level_domains_path -->
</top_level_domains_lists>

```

**Syntax**



```
cutToFirstSignificantSubdomainCustom(url, tld_list_name)

```

**Arguments**


- `url` — URL or domain string to process. [`String`](/docs/sql-reference/data-types/string)
- `tld_list_name` — Name of the custom TLD list configured in ClickHouse. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Using custom TLD list for non\-standard domains**



```
SELECT cutToFirstSignificantSubdomainCustom('bar.foo.there-is-no-such-domain', 'public_suffix_list')

```


```
foo.there-is-no-such-domain

```

## cutToFirstSignificantSubdomainCustomRFC[​](#cutToFirstSignificantSubdomainCustomRFC "Direct link to cutToFirstSignificantSubdomainCustomRFC")


Introduced in: v22\.10\.0


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain.
Accepts custom [TLD list](https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains) name.
This function can be useful if you need a fresh TLD list or if you have a custom list.
Similar to [cutToFirstSignificantSubdomainCustom](#cutToFirstSignificantSubdomainCustom) but conforms to RFC 3986\.


**Configuration example**



```
<!-- <top_level_domains_path>/var/lib/clickhouse/top_level_domains/</top_level_domains_path> -->
<top_level_domains_lists>
    <!-- https://publicsuffix.org/list/public_suffix_list.dat -->
    <public_suffix_list>public_suffix_list.dat</public_suffix_list>
    <!-- NOTE: path is under top_level_domains_path -->
</top_level_domains_lists>

```

**Syntax**



```
cutToFirstSignificantSubdomainCustomRFC(url, tld_list_name)

```

**Arguments**


- `url` — URL or domain string to process according to RFC 3986\. \- `tld_list_name` — Name of the custom TLD list configured in ClickHouse.


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT cutToFirstSignificantSubdomainCustomRFC('www.foo', 'public_suffix_list');

```


```
┌─cutToFirstSignificantSubdomainCustomRFC('www.foo', 'public_suffix_list')─────┐
│ www.foo                                                                      │
└──────────────────────────────────────────────────────────────────────────────┘

```

## cutToFirstSignificantSubdomainCustomWithWWW[​](#cutToFirstSignificantSubdomainCustomWithWWW "Direct link to cutToFirstSignificantSubdomainCustomWithWWW")


Introduced in: v21\.1\.0


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain without stripping 'www'. Accepts custom TLD list name. It can be useful if you need a fresh TLD list or if you have a custom list.


**Configuration example**



```
<!-- <top_level_domains_path>/var/lib/clickhouse/top_level_domains/</top_level_domains_path> -->
<top_level_domains_lists>
    <!-- https://publicsuffix.org/list/public_suffix_list.dat -->
    <public_suffix_list>public_suffix_list.dat</public_suffix_list>
    <!-- NOTE: path is under top_level_domains_path -->
</top_level_domains_lists>
    

**Syntax**

```sql
cutToFirstSignificantSubdomainCustomWithWWW(url, tld_list_name)

```

**Arguments**


- `url` — URL or domain string to process. \- `tld_list_name` — Name of the custom TLD list configured in ClickHouse.


**Returned value**


Part of the domain that includes top\-level subdomains up to the first significant subdomain without stripping 'www'. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT cutToFirstSignificantSubdomainCustomWithWWW('www.foo', 'public_suffix_list');

```


```
┌─cutToFirstSignificantSubdomainCustomWithWWW('www.foo', 'public_suffix_list')─┐
│ www.foo                                                                      │
└──────────────────────────────────────────────────────────────────────────────┘

```

## cutToFirstSignificantSubdomainCustomWithWWWRFC[​](#cutToFirstSignificantSubdomainCustomWithWWWRFC "Direct link to cutToFirstSignificantSubdomainCustomWithWWWRFC")


Introduced in: v22\.10\.0


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain without stripping `www`.
Accepts custom TLD list name.
It can be useful if you need a fresh TLD list or if you have a custom list.
Similar to [cutToFirstSignificantSubdomainCustomWithWWW](#cutToFirstSignificantSubdomainCustomWithWWW) but conforms to [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).


**Configuration example**



```
<!-- <top_level_domains_path>/var/lib/clickhouse/top_level_domains/</top_level_domains_path> -->
<top_level_domains_lists>
    <!-- https://publicsuffix.org/list/public_suffix_list.dat -->
    <public_suffix_list>public_suffix_list.dat</public_suffix_list>
    <!-- NOTE: path is under top_level_domains_path -->
</top_level_domains_lists>
    

**Syntax**

```sql
cutToFirstSignificantSubdomainCustomWithWWWRFC(url, tld_list_name)

```

**Arguments**


- `url` — URL or domain string to process according to RFC 3986\. \- `tld_list_name` — Name of the custom TLD list configured in ClickHouse.


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain without stripping `www`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**RFC 3986 parsing preserving www with custom TLD list**



```
SELECT cutToFirstSignificantSubdomainCustomWithWWWRFC('https://www.subdomain.example.custom', 'public_suffix_list')

```


```
www.example.custom

```

## cutToFirstSignificantSubdomainRFC[​](#cutToFirstSignificantSubdomainRFC "Direct link to cutToFirstSignificantSubdomainRFC")


Introduced in: v22\.10\.0


Returns the part of the domain that includes top\-level subdomains up to the ["first significant subdomain"](/docs/sql-reference/functions/url-functions#firstSignificantSubdomain). Similar to [`cutToFirstSignificantSubdomain`](#cutToFirstSignificantSubdomain) but conforms to [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).


**Syntax**



```
cutToFirstSignificantSubdomainRFC(url)

```

**Arguments**


- `url` — URL or domain string to process according to RFC 3986\. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain if possible, otherwise returns an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    cutToFirstSignificantSubdomain('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080'),
    cutToFirstSignificantSubdomainRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080');

```


```
┌─cutToFirstSignificantSubdomain('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080')─┬─cutToFirstSignificantSubdomainRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080')─┐
│                                                                         │ example.com                                                                │
└─────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────┘

```

## cutToFirstSignificantSubdomainWithWWW[​](#cutToFirstSignificantSubdomainWithWWW "Direct link to cutToFirstSignificantSubdomainWithWWW")


Introduced in: v20\.12\.0


Returns the part of the domain that includes top\-level subdomains up to the "first significant subdomain", without stripping '[www](http://www).'.


Similar to [`cutToFirstSignificantSubdomain`](#cutToFirstSignificantSubdomain) but preserves the '[www](http://www).' prefix if present.


**Syntax**



```
cutToFirstSignificantSubdomainWithWWW(url)

```

**Arguments**


- `url` — URL or domain string to process. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain (with www) if possible, otherwise returns an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    cutToFirstSignificantSubdomainWithWWW('https://news.clickhouse.com.tr/'),
    cutToFirstSignificantSubdomainWithWWW('www.tr'),
    cutToFirstSignificantSubdomainWithWWW('tr');

```


```
┌─cutToFirstSignificantSubdomainWithWWW('https://news.clickhouse.com.tr/')─┬─cutToFirstSignificantSubdomainWithWWW('www.tr')─┬─cutToFirstSignificantSubdomainWithWWW('tr')─┐
│ clickhouse.com.tr                                                        │ www.tr                                          │                                             │
└──────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────┴─────────────────────────────────────────────┘

```

## cutToFirstSignificantSubdomainWithWWWRFC[​](#cutToFirstSignificantSubdomainWithWWWRFC "Direct link to cutToFirstSignificantSubdomainWithWWWRFC")


Introduced in: v22\.10\.0


Returns the part of the domain that includes top\-level subdomains up to the "first significant subdomain", without stripping 'www'. Similar to [`cutToFirstSignificantSubdomainWithWWW`](#cutToFirstSignificantSubdomainWithWWW) but conforms to [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).


**Syntax**



```
cutToFirstSignificantSubdomainWithWWWRFC(url)

```

**Arguments**


- `url` — URL or domain string to process according to RFC 3986\.


**Returned value**


Returns the part of the domain that includes top\-level subdomains up to the first significant subdomain (with 'www') if possible, otherwise returns an empty string [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    cutToFirstSignificantSubdomainWithWWW('http:%2F%[[email protected]](/cdn-cgi/l/email-protection)/economicheskiy'),
    cutToFirstSignificantSubdomainWithWWWRFC('http:%2F%[[email protected]](/cdn-cgi/l/email-protection)/economicheskiy');

```


```
┌─cutToFirstSignificantSubdomainWithWWW('http:%2F%[[email protected]](/cdn-cgi/l/email-protection)/economicheskiy')─┬─cutToFirstSignificantSubdomainWithWWWRFC('http:%2F%[[email protected]](/cdn-cgi/l/email-protection)/economicheskiy')─┐
│                                                                                       │ mail.ru                                                                                  │
└───────────────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────┘

```

## cutURLParameter[​](#cutURLParameter "Direct link to cutURLParameter")


Introduced in: v1\.1\.0


Removes the `name` parameter from a URL, if present.
This function does not encode or decode characters in parameter names, e.g. `Client ID` and `Client%20ID` are treated as different parameter names.


**Syntax**



```
cutURLParameter(url, name)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)
- `name` — Name of URL parameter. [`String`](/docs/sql-reference/data-types/string) or [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


URL with `name` URL parameter removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    cutURLParameter('http://bigmir.net/?a=b&c=d&e=f#g', 'a') AS url_without_a,
    cutURLParameter('http://bigmir.net/?a=b&c=d&e=f#g', ['c', 'e']) AS url_without_c_and_e;

```


```
┌─url_without_a────────────────┬─url_without_c_and_e──────┐
│ http://bigmir.net/?c=d&e=f#g │ http://bigmir.net/?a=b#g │
└──────────────────────────────┴──────────────────────────┘

```

## cutWWW[​](#cutWWW "Direct link to cutWWW")


Introduced in: v1\.1\.0


Removes the leading `www.`, if present, from the URL's domain.


**Syntax**



```
cutWWW(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the URL with leading `www.` removed from the domain. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT cutWWW('http://www.example.com/path?query=value#fragment');

```


```
┌─cutWWW('http://www.example.com/path?query=value#fragment')─┐
│ http://example.com/path?query=value#fragment               │
└────────────────────────────────────────────────────────────┘

```

## decodeURLComponent[​](#decodeURLComponent "Direct link to decodeURLComponent")


Introduced in: v1\.1\.0


Takes a URL\-encoded string as input and decodes it back to its original, readable form.


**Syntax**



```
decodeURLComponent(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the decoded URL. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT decodeURLComponent('http://127.0.0.1:8123/?query=SELECT%201%3B') AS DecodedURL;

```


```
┌─DecodedURL─────────────────────────────┐
│ http://127.0.0.1:8123/?query=SELECT 1; │
└────────────────────────────────────────┘

```

## decodeURLFormComponent[​](#decodeURLFormComponent "Direct link to decodeURLFormComponent")


Introduced in: v1\.1\.0


Decodes URL\-encoded strings using form encoding rules ([RFC\-1866](https://www.rfc-editor.org/rfc/rfc1866.html)), where `+` signs are converted to spaces and percent\-encoded characters are decoded.


**Syntax**



```
decodeURLFormComponent(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the decoded URL. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT decodeURLFormComponent('http://127.0.0.1:8123/?query=SELECT%201+2%2B3') AS DecodedURL;

```


```
┌─DecodedURL────────────────────────────────┐
│ http://127.0.0.1:8123/?query=SELECT 1 2+3 │
└───────────────────────────────────────────┘

```

## domain[​](#domain "Direct link to domain")


Introduced in: v1\.1\.0


Extracts the hostname from a URL.


The URL can be specified with or without a protocol.


**Syntax**



```
domain(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the host name if the input string can be parsed as a URL, otherwise an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT domain('svn+ssh://some.svn-hosting.com:80/repo/trunk');

```


```
┌─domain('svn+ssh://some.svn-hosting.com:80/repo/trunk')─┐
│ some.svn-hosting.com                                   │
└────────────────────────────────────────────────────────┘

```

## domainRFC[​](#domainRFC "Direct link to domainRFC")


Introduced in: v22\.10\.0


Extracts the hostname from a URL.
Similar to [`domain`](#domain), but [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986) conformant.


**Syntax**



```
domainRFC(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the host name if the input string can be parsed as a URL, otherwise an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    domain('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment'),
    domainRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment');

```


```
┌─domain('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment')─┬─domainRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment')─┐
│                                                                           │ example.com                                                                  │
└───────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

```

## domainWithoutWWW[​](#domainWithoutWWW "Direct link to domainWithoutWWW")


Introduced in: v1\.1\.0


Returns the domain of a URL without leading `www.` if present.


**Syntax**



```
domainWithoutWWW(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the domain name if the input string can be parsed as a URL (without leading `www.`), otherwise an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT domainWithoutWWW('http://[[email protected]](/cdn-cgi/l/email-protection):80/');

```


```
┌─domainWithoutWWW('http://[[email protected]](/cdn-cgi/l/email-protection):80/')─┐
│ example.com                                         │
└─────────────────────────────────────────────────────┘

```

## domainWithoutWWWRFC[​](#domainWithoutWWWRFC "Direct link to domainWithoutWWWRFC")


Introduced in: v1\.1\.0


Returns the domain without leading `www.` if present. Similar to [`domainWithoutWWW`](#domainWithoutWWW) but conforms to [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).


**Syntax**



```
domainWithoutWWWRFC(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the domain name if the input string can be parsed as a URL (without leading `www.`), otherwise an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    domainWithoutWWW('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment'),
    domainWithoutWWWRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment');

```


```
┌─domainWithoutWWW('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment')─┬─domainWithoutWWWRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/path?query=value#fragment')─┐
│                                                                                         │ example.com                                                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────┘

```

## encodeURLComponent[​](#encodeURLComponent "Direct link to encodeURLComponent")


Introduced in: v22\.3\.0


Takes a regular string and converts it into a URL\-encoded (percent\-encoded) format where special characters are replaced with their percent\-encoded equivalents.


**Syntax**



```
encodeURLComponent(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the encoded URL. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT encodeURLComponent('http://127.0.0.1:8123/?query=SELECT 1;') AS EncodedURL;

```


```
┌─EncodedURL───────────────────────────────────────────────┐
│ http%3A%2F%2F127.0.0.1%3A8123%2F%3Fquery%3DSELECT%201%3B │
└──────────────────────────────────────────────────────────┘

```

## encodeURLFormComponent[​](#encodeURLFormComponent "Direct link to encodeURLFormComponent")


Introduced in: v22\.3\.0


Encodes strings using form encoding rules ([RFC\-1866](https://www.rfc-editor.org/rfc/rfc1866.html)), where spaces are converted to \+ signs and special characters are percent\-encoded.


**Syntax**



```
encodeURLFormComponent(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the encoded URL. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT encodeURLFormComponent('http://127.0.0.1:8123/?query=SELECT 1 2+3') AS EncodedURL;

```


```
┌─EncodedURL────────────────────────────────────────────────┐
│ http%3A%2F%2F127.0.0.1%3A8123%2F%3Fquery%3DSELECT+1+2%2B3 │
└───────────────────────────────────────────────────────────┘

```

## extractURLParameter[​](#extractURLParameter "Direct link to extractURLParameter")


Introduced in: v1\.1\.0


Returns the value of the `name` parameter in the URL, if present, otherwise an empty string is returned.
If there are multiple parameters with this name, the first occurrence is returned.
The function assumes that the parameter in the `url` parameter is encoded in the same way as in the `name` argument.


**Syntax**



```
extractURLParameter(url, name)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)
- `name` — Parameter name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the value of the URL parameter with the specified name. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT extractURLParameter('http://example.com/?param1=value1&param2=value2', 'param1');

```


```
┌─extractURLPa⋯, 'param1')─┐
│ value1                   │
└──────────────────────────┘

```

## extractURLParameterNames[​](#extractURLParameterNames "Direct link to extractURLParameterNames")


Introduced in: v1\.1\.0


Returns an array of name strings corresponding to the names of URL parameters.
The values are not decoded.


**Syntax**



```
extractURLParameterNames(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array of name strings corresponding to the names of URL parameters. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT extractURLParameterNames('http://example.com/?param1=value1&param2=value2');

```


```
┌─extractURLPa⋯m2=value2')─┐
│ ['param1','param2']      │
└──────────────────────────┘

```

## extractURLParameters[​](#extractURLParameters "Direct link to extractURLParameters")


Introduced in: v1\.1\.0


Returns an array of `name=value` strings corresponding to the URL parameters.
The values are not decoded.


**Syntax**



```
extractURLParameters(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array of `name=value` strings corresponding to the URL parameters. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT extractURLParameters('http://example.com/?param1=value1&param2=value2');

```


```
┌─extractURLParame⋯&param2=value2')─┐
│ ['param1=value1','param2=value2'] │
└───────────────────────────────────┘

```

## firstSignificantSubdomain[​](#firstSignificantSubdomain "Direct link to firstSignificantSubdomain")


Introduced in: v1\.1\.0


Returns the "first significant subdomain".


The first significant subdomain is a second\-level domain if it is 'com', 'net', 'org', or 'co'.
Otherwise, it is a third\-level domain.


For example, firstSignificantSubdomain('<https://news.clickhouse.com/>') \= 'clickhouse', firstSignificantSubdomain ('<https://news.clickhouse.com.tr/>') \= 'clickhouse'.


The list of "insignificant" second\-level domains and other implementation details may change in the future.


**Syntax**



```
firstSignificantSubdomain(url)

```

**Arguments**


- None.


**Returned value**


**Examples**


**firstSignificantSubdomain**



```
SELECT firstSignificantSubdomain('https://news.clickhouse.com/')

```


## firstSignificantSubdomainCustom[​](#firstSignificantSubdomainCustom "Direct link to firstSignificantSubdomainCustom")


Introduced in: v21\.1\.0


Returns the first significant subdomain of a URL using a custom TLD (Top\-Level Domain) list. The custom TLD list name refers to a configuration that defines which domain suffixes should be treated as top\-level domains. This is useful for non\-standard TLD hierarchies. The function uses a simplified URL parsing algorithm that assumes the protocol and everything following are stripped.


**Syntax**



```
firstSignificantSubdomainCustom(url, tld_list_name)

```

**Arguments**


- `url` — The URL to extract the subdomain from. [`String`](/docs/sql-reference/data-types/string)
- `tld_list_name` — Name of the custom TLD list from the configuration. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the first significant subdomain. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT firstSignificantSubdomainCustom('https://news.example.com', 'public_suffix_list')

```


```
example

```

## firstSignificantSubdomainCustomRFC[​](#firstSignificantSubdomainCustomRFC "Direct link to firstSignificantSubdomainCustomRFC")


Introduced in: v22\.10\.0


Similar to `firstSignificantSubdomainCustom` but uses RFC 3986 compliant URL parsing instead of the simplified algorithm.


**Syntax**



```
firstSignificantSubdomainCustomRFC(url, tld_list_name)

```

**Arguments**


- `url` — The URL to extract the subdomain from. [`String`](/docs/sql-reference/data-types/string)
- `tld_list_name` — Name of the custom TLD list from the configuration. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the first significant subdomain. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT firstSignificantSubdomainCustomRFC('https://news.example.com', 'public_suffix_list')

```


```
example

```

## firstSignificantSubdomainRFC[​](#firstSignificantSubdomainRFC "Direct link to firstSignificantSubdomainRFC")


Introduced in: v22\.10\.0


Returns the "first significant subdomain" according to RFC 1034\.


**Syntax**



```
firstSignificantSubdomainRFC(url)

```

**Arguments**


- None.


**Returned value**


**Examples**


## fragment[​](#fragment "Direct link to fragment")


Introduced in: v1\.1\.0


Returns the fragment identifier without the initial hash symbol.


**Syntax**



```
fragment(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the fragment identifier without the initial hash symbol. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT fragment('https://clickhouse.com/docs/getting-started/quick-start/cloud#1-create-a-clickhouse-service');

```


```
┌─fragment('http⋯ouse-service')─┐
│ 1-create-a-clickhouse-service │
└───────────────────────────────┘

```

## netloc[​](#netloc "Direct link to netloc")


Introduced in: v20\.5\.0


Extracts network locality (`username:password@host:port`) from a URL.


**Syntax**



```
netloc(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `username:password@host:port` from a given URL. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT netloc('http://[[email protected]](/cdn-cgi/l/email-protection):80/');

```


```
┌─netloc('http⋯e.com:80/')─┐
│ [[email protected]](/cdn-cgi/l/email-protection):80  │
└──────────────────────────┘

```

## path[​](#path "Direct link to path")


Introduced in: v1\.1\.0


Returns the path without query string from a URL.


**Syntax**



```
path(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the path of the URL without query string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT path('https://clickhouse.com/docs/sql-reference/functions/url-functions/?query=value');

```


```
┌─path('https://clickhouse.com/en/sql-reference/functions/url-functions/?query=value')─┐
│ /docs/sql-reference/functions/url-functions/                                         │
└──────────────────────────────────────────────────────────────────────────────────────┘

```

## pathFull[​](#pathFull "Direct link to pathFull")


Introduced in: v1\.1\.0


The same as [`path`](#path), but includes the query string and fragment of the URL.


**Syntax**



```
pathFull(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the path of the URL including query string and fragment. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT pathFull('https://clickhouse.com/docs/sql-reference/functions/url-functions/?query=value#section');

```


```
┌─pathFull('https://clickhouse.com⋯unctions/?query=value#section')─┐
│ /docs/sql-reference/functions/url-functions/?query=value#section │
└──────────────────────────────────────────────────────────────────┘

```

## port[​](#port "Direct link to port")


Introduced in: v20\.5\.0


Returns the port of a URL, or the `default_port` if the URL contains no port or cannot be parsed.


**Syntax**



```
port(url[, default_port])

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)
- `default_port` — Optional. The default port number to be returned. `0` by default. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the port of the URL, or the default port if there is no port in the URL or in case of a validation error. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT port('https://clickhouse.com:8443/docs'), port('https://clickhouse.com/docs', 443);

```


```
┌─port('https://clickhouse.com:8443/docs')─┬─port('https://clickhouse.com/docs', 443)─┐
│                                     8443 │                                      443 │
└──────────────────────────────────────────┴──────────────────────────────────────────┘

```

## portRFC[​](#portRFC "Direct link to portRFC")


Introduced in: v22\.10\.0


Returns the port or `default_port` if the URL contains no port or cannot be parsed.
Similar to [`port`](#port), but [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986) conformant.


**Syntax**



```
portRFC(url[, default_port])

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)
- `default_port` — Optional. The default port number to be returned. `0` by default. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the port or the default port if there is no port in the URL or in case of a validation error. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT port('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/'), portRFC('http://user:[[email protected]](/cdn-cgi/l/email-protection):8080/');

```


```
┌─port('http:/⋯com:8080/')─┬─portRFC('htt⋯com:8080/')─┐
│                        0 │                     8080 │
└──────────────────────────┴──────────────────────────┘

```

## protocol[​](#protocol "Direct link to protocol")


Introduced in: v1\.1\.0


Extracts the protocol from a URL.


Examples of typical returned values: http, https, ftp, mailto, tel, magnet.


**Syntax**



```
protocol(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the protocol of the URL, or an empty string if it cannot be determined. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT protocol('https://clickhouse.com/');

```


```
┌─protocol('https://clickhouse.com/')─┐
│ https                               │
└─────────────────────────────────────┘

```

## queryString[​](#queryString "Direct link to queryString")


Introduced in: v1\.1\.0


Returns the query string of a URL without the initial question mark, `#` and everything after `#`.


**Syntax**



```
queryString(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the query string of the URL without the initial question mark and fragment. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT queryString('https://clickhouse.com/docs?query=value&param=123#section');

```


```
┌─queryString(⋯3#section')─┐
│ query=value&param=123    │
└──────────────────────────┘

```

## queryStringAndFragment[​](#queryStringAndFragment "Direct link to queryStringAndFragment")


Introduced in: v1\.1\.0


Returns the query string and fragment identifier of a URL.


**Syntax**



```
queryStringAndFragment(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the query string and fragment identifier of the URL. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT queryStringAndFragment('https://clickhouse.com/docs?query=value&param=123#section');

```


```
┌─queryStringAnd⋯=123#section')─┐
│ query=value&param=123#section │
└───────────────────────────────┘

```

## topLevelDomain[​](#topLevelDomain "Direct link to topLevelDomain")


Introduced in: v1\.1\.0


Extracts the the top\-level domain from a URL.


NoteThe URL can be specified with or without a protocol.
For example:
```
svn+ssh://some.svn-hosting.com:80/repo/trunk
some.svn-hosting.com:80/repo/trunk
https://clickhouse.com/time/

```



**Syntax**



```
topLevelDomain(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the domain name if the input string can be parsed as a URL. Otherwise, an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT topLevelDomain('svn+ssh://www.some.svn-hosting.com:80/repo/trunk');

```


```
┌─topLevelDomain('svn+ssh://www.some.svn-hosting.com:80/repo/trunk')─┐
│ com                                                                │
└────────────────────────────────────────────────────────────────────┘

```

## topLevelDomainRFC[​](#topLevelDomainRFC "Direct link to topLevelDomainRFC")


Introduced in: v22\.10\.0


Extracts the the top\-level domain from a URL.
Similar to [`topLevelDomain`](#topLevelDomain), but conforms to [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986).


**Syntax**



```
topLevelDomainRFC(url)

```

**Arguments**


- `url` — URL. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Domain name if the input string can be parsed as a URL. Otherwise, an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT topLevelDomain('http://foo:foo%[[email protected]](/cdn-cgi/l/email-protection)'), topLevelDomainRFC('http://foo:foo%[[email protected]](/cdn-cgi/l/email-protection)');

```


```
┌─topLevelDomain('http://foo:foo%[[email protected]](/cdn-cgi/l/email-protection)')─┬─topLevelDomainRFC('http://foo:foo%[[email protected]](/cdn-cgi/l/email-protection)')─┐
│                                                │ com                                               │
└────────────────────────────────────────────────┴───────────────────────────────────────────────────┘

```
[PreviousuniqTheta](/docs/sql-reference/functions/uniqtheta-functions)[NextUUIDs](/docs/sql-reference/functions/uuid-functions)- [Overview](#overview)- [URLHierarchy](#URLHierarchy)- [URLPathHierarchy](#URLPathHierarchy)- [cutFragment](#cutFragment)- [cutQueryString](#cutQueryString)- [cutQueryStringAndFragment](#cutQueryStringAndFragment)- [cutToFirstSignificantSubdomain](#cutToFirstSignificantSubdomain)- [cutToFirstSignificantSubdomainCustom](#cutToFirstSignificantSubdomainCustom)- [cutToFirstSignificantSubdomainCustomRFC](#cutToFirstSignificantSubdomainCustomRFC)- [cutToFirstSignificantSubdomainCustomWithWWW](#cutToFirstSignificantSubdomainCustomWithWWW)- [cutToFirstSignificantSubdomainCustomWithWWWRFC](#cutToFirstSignificantSubdomainCustomWithWWWRFC)- [cutToFirstSignificantSubdomainRFC](#cutToFirstSignificantSubdomainRFC)- [cutToFirstSignificantSubdomainWithWWW](#cutToFirstSignificantSubdomainWithWWW)- [cutToFirstSignificantSubdomainWithWWWRFC](#cutToFirstSignificantSubdomainWithWWWRFC)- [cutURLParameter](#cutURLParameter)- [cutWWW](#cutWWW)- [decodeURLComponent](#decodeURLComponent)- [decodeURLFormComponent](#decodeURLFormComponent)- [domain](#domain)- [domainRFC](#domainRFC)- [domainWithoutWWW](#domainWithoutWWW)- [domainWithoutWWWRFC](#domainWithoutWWWRFC)- [encodeURLComponent](#encodeURLComponent)- [encodeURLFormComponent](#encodeURLFormComponent)- [extractURLParameter](#extractURLParameter)- [extractURLParameterNames](#extractURLParameterNames)- [extractURLParameters](#extractURLParameters)- [firstSignificantSubdomain](#firstSignificantSubdomain)- [firstSignificantSubdomainCustom](#firstSignificantSubdomainCustom)- [firstSignificantSubdomainCustomRFC](#firstSignificantSubdomainCustomRFC)- [firstSignificantSubdomainRFC](#firstSignificantSubdomainRFC)- [fragment](#fragment)- [netloc](#netloc)- [path](#path)- [pathFull](#pathFull)- [port](#port)- [portRFC](#portRFC)- [protocol](#protocol)- [queryString](#queryString)- [queryStringAndFragment](#queryStringAndFragment)- [topLevelDomain](#topLevelDomain)- [topLevelDomainRFC](#topLevelDomainRFC)
Was this page helpful?

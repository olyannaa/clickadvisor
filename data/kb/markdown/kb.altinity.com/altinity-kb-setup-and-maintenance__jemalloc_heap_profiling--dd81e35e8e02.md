# Jemalloc heap profiling \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Jemalloc heap profiling
# Jemalloc heap profiling

Example of .xml config to enable remote pprof style access## Config


```
<!-- cat config.d/jemalloc_dict.xml -->
<clickhouse>
	<dictionaries_config>/etc/clickhouse-server/config.d/*_dict.xml</dictionaries_config>
	<http_handlers>
		<rule>
			<url>/pprof/heap</url>
			<methods>GET,POST</methods>
			<handler>
				<type>static</type>
				<response_content>file://jemalloc_clickhouse.heap</response_content>
			</handler>
		</rule>
		<rule>
			<url>/pprof/cmdline</url>
			<methods>GET</methods>
			<handler>
				<type>predefined_query_handler</type>
				<query>SELECT '/var/lib/clickhouse' FORMAT TSVRaw</query>
			</handler>
		</rule>
		<rule>
			<url>/pprof/symbol</url>
			<methods>GET</methods>
			<handler>
				<type>predefined_query_handler</type>
				<query>SELECT 'num_symbols: ' || count() FROM system.symbols FORMAT TSVRaw SETTINGS allow_introspection_functions = 1</query>
			</handler>
		</rule>
		<rule>
			<url>/pprof/symbol</url>
			<methods>POST</methods>
			<handler>
				<type>predefined_query_handler</type>
				<query>WITH arrayJoin(splitByChar('+', {_request_body:String})) as addr SELECT addr || '    ' || demangle(addressToSymbol(reinterpretAsUInt64(reverse(substr(unhex(addr),2))))) SETTINGS allow_introspection_functions = 1 FORMAT TSVRaw</query>
			</handler>
		</rule>
		<defaults/>
	</http_handlers>
	<dictionary>
		<name>jemalloc_ls</name>
		<structure>
			<key>
				<attribute>
					<name>id</name>
					<type>String</type>
				</attribute>
			</key>
			<attribute>
				<name>file</name>
				<type>String</type>
				<null_value />
			</attribute>
			<attribute>
				<name>size</name>
				<type>UInt32</type>
				<null_value />
			</attribute>
			<attribute>
				<name>time</name>
				<type>DateTime</type>
				<null_value />
			</attribute>
		</structure>
		<source>
			<executable>
				<command>for f in /tmp/jemalloc_clickhouse.*; do [ -f &quot;$f&quot; ] || continue; echo -e &quot;$(basename &quot;$f&quot; | cut -d. -f2-3)\t$f\t$(stat -c%s &quot;$f&quot;)\t$(stat -c%Y &quot;$f&quot;)&quot;; done</command>
				<execute_direct>false</execute_direct>
				<format>TSV</format>
			</executable>
		</source>
		<layout>
			<complex_key_direct/>
		</layout>
		<lifetime>300</lifetime>
	</dictionary>
	<dictionary>
		<name>jemalloc_cp</name>
		<structure>
			<id>
				<name>id</name>
				<type>UInt32</type>
			</id>
			<attribute>
				<name>status</name>
				<type>UInt32</type>
				<null_value />
			</attribute>
		</structure>
		<source>
			<executable>
				<command>ver=${1:-$(head -n1 | tr -d &quot;[:space:]&quot;)}; file=$(ls -t -- /tmp/jemalloc_clickhouse.*.&quot;$ver&quot;.heap 2&gt;/dev/null | head -n1); if [ -n &quot;$file&quot; ] &amp;&amp; cp -- &quot;$file&quot; /var/lib/clickhouse/user_files/jemalloc_clickhouse.heap; then printf &apos;1\t\n&apos;; else printf &apos;0\t\n&apos;; fi</command>
				<execute_direct>false</execute_direct>
				<format>TSV</format>
			</executable>
		</source>
		<layout>
			<direct/>
		</layout>
		<lifetime>300</lifetime>
	</dictionary>
</clickhouse>

```

```
$ curl https://user:password@cluster.env.altinity.cloud:8443/pprof/cmdline
/var/lib/clickhouse

$ curl https://user:password@cluster.env.altinity.cloud:8443/pprof/symbol
num_symbols: 702648

$ curl -d '0x0F99B044+0x008512D0' https://user:password@cluster.env.altinity.cloud:8443/pprof/symbol
0x0F99B044    DB::StorageSystemFilesystemCache::getColumnsDescription()
0x008512D0    icudt75_dat

```

```
cluster :) SYSTEM JEMALLOC ENABLE PROFILE;

SYSTEM JEMALLOC ENABLE PROFILE

Ok.

0 rows in set. Elapsed: 0.270 sec.

cluster :) SELECT uniqExact(number) FROM numbers_mt(1000000000);

SELECT uniqExact(number)
FROM numbers_mt(1000000000)

┌─uniqExact(number)─┐
│        1000000000 │ -- 1.00 billion
└───────────────────┘

1 row in set. Elapsed: 6.585 sec. Processed 1.00 billion rows, 8.00 GB (151.86 million rows/s., 1.21 GB/s.)
Peak memory usage: 25.19 GiB.

cluster :) SYSTEM JEMALLOC FLUSH PROFILE;

SYSTEM JEMALLOC FLUSH PROFILE

Ok.

0 rows in set. Elapsed: 0.272 sec.

cluster :) SELECT * FROM dictionary('jemalloc_ls');

SELECT *
FROM dictionary('jemalloc_ls')

┌─id─────┬─file──────────────────────────────┬───size─┬────────────────time─┐
│        │                                   │      0 │ 1970-01-01 00:00:00 │
│ -e 8.0 │ /tmp/jemalloc_clickhouse.8.0.heap │ 108004 │ 2025-09-01 00:44:13 │
│ -e 8.1 │ /tmp/jemalloc_clickhouse.8.1.heap │ 111115 │ 2025-09-01 00:46:46 │
│ -e 8.2 │ /tmp/jemalloc_clickhouse.8.2.heap │ 128098 │ 2025-09-01 00:47:07 │
│ -e 8.3 │ /tmp/jemalloc_clickhouse.8.3.heap │ 123980 │ 2025-09-01 00:48:14 │
│ -e 8.4 │ /tmp/jemalloc_clickhouse.8.4.heap │ 124230 │ 2025-09-01 00:48:15 │
│ -e 8.5 │ /tmp/jemalloc_clickhouse.8.5.heap │ 117733 │ 2025-09-01 12:18:53 │
└────────┴───────────────────────────────────┴────────┴─────────────────────┘

7 rows in set. Elapsed: 0.021 sec.

cluster :) SELECT dictGet('jemalloc_cp', 'status', 4);

SELECT dictGet('jemalloc_cp', 'status', 4)

┌─dictGet('jem⋯status', 4)─┐
│                        0 │
└──────────────────────────┘

1 row in set. Elapsed: 0.014 sec.

```

```
$ jeprof --svg https://user:password@cluster.env.altinity.cloud:8443/pprof/heap > ./mem.svg
Fetching /pprof/heap profile from https://user:password@cluster.env.altinity.cloud:8443/pprof/heap to
  /home/user/jeprof/clickhouse.1756728952.user.pprof.heap
Wrote profile to /home/user/jeprof/clickhouse.1756728952.user.pprof.heap
Dropping nodes with <= 90.7 MB; edges with <= 18.1 abs(MB)

```

```
cluster :) SELECT dictGet('jemalloc_cp', 'status', 5);

SELECT dictGet('jemalloc_cp', 'status', 5)

┌─dictGet('jem⋯status', 5)─┐
│                        0 │
└──────────────────────────┘

1 row in set. Elapsed: 0.014 sec.

```

```
$ jeprof --svg https://user:password@cluster.env.altinity.cloud:8443/pprof/heap --base /home/user/jeprof/clickhouse.1756728952.user.pprof.heap > ./mem_diff.svg
Fetching /pprof/heap profile from https://user:password@cluster.env.altinity.cloud:8443/pprof/heap to
  /home/user/jeprof/clickhouse.1756729237.user.pprof.heap
Wrote profile to /home/user/jeprof/clickhouse.1756729237.user.pprof.heap

```

```
cluster :) SYSTEM JEMALLOC DISABLE PROFILE;

SYSTEM JEMALLOC DISABLE PROFILE

Ok.

0 rows in set. Elapsed: 0.271 sec.

```
Last modified 2025\.09\.01: [Update jemalloc\_heap\_profiling.md (3bbbc60\)](https://github.com/Altinity/altinityknowledgebase/commit/3bbbc60562941f2f688b3feeaa8529e7d64764ac)

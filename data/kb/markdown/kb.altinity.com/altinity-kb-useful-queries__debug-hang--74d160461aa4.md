# Debug hanging thing \| Altinity® Knowledge Base for ClickHouse®


1. [Useful queries](/altinity-kb-useful-queries/)
2. Debug hanging thing
# Debug hanging thing

Debug hanging / freezing things## Debug hanging / freezing things

If ClickHouse® is busy with something and you don’t know what’s happening, you can easily check the stacktraces of all the thread which are working


```
SELECT
 arrayStringConcat(arrayMap(x -> concat('0x', lower(hex(x)), '\t', demangle(addressToSymbol(x))), trace), '\n') as trace_functions,
 count()
FROM system.stack_trace
GROUP BY trace_functions
ORDER BY count()
DESC
SETTINGS allow_introspection_functions=1
FORMAT Vertical;

```
If you can’t start any queries, but you have access to the node, you can sent a signal


```
# older versions
for i in $(ls -1 /proc/$(pidof clickhouse-server)/task/); do kill -TSTP $i; done
# even older versions
for i in $(ls -1 /proc/$(pidof clickhouse-server)/task/); do kill -SIGPROF $i; done

```
Last modified 2025\.05\.05: [Update debug\-hang.md (06b4062\)](https://github.com/Altinity/altinityknowledgebase/commit/06b406273082616501bdc0d92cf544ee4c5346fa)

---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Instrumenting
topic: instrumenting-my-espresso-machine-with-opentelemetry-clickhouse
ch_version_introduced: '0.1'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 14
---

potentially mid\-shot. The fix is the same snapshot pattern, applied to metadata: the main thread, which owns those Strings, refreshes a cached copy whenever they change, and the export task only ever copies the cache under the lock.

```
1void OpenTelemetryPlugin::refreshMetadata() {
2// Runs on the main thread, which owns the controller's Strings.
3std::vector<otel::Attribute> attrs = buildResourceAttributes();
4lock();
5resourceAttrs = attrs;  // the export task copies this under the same lock
6unlock();
7}
```
Copy command
The second was quieter: the export task's 12KB stack was occasionally not enough for an mbedTLS handshake with full CA\-bundle verification, which is a stack overflow and another reset. It now runs with 16KB; the extra 4KB is cheap insurance against a crash that only shows up when the TLS library takes its deepest path. Observability that takes down the thing it observes is worse than no observability at all.

### 3\. Clocks lie until proven otherwise \#

A freshly booted ESP32 thinks it's 1970\. OTLP timestamps are unix nanoseconds, and traces timestamped in the Nixon era are effectively unfindable in any backend, so the device refuses to export anything until NTP confirms the wall clock has advanced past 2020:

```
1// SNTP has set the wall clock (post 2020-09). Until then, unix-nano
2// timestamps would be garbage, so we hold off exporting.
3static bool clockValid() { return time(nullptr) > 1600000000L; }
```
Copy command
A small guard, but it's the difference between data you can query and data you'll never see again.

## Computing the interesting numbers on\-device \#

This is the fun part. The machine doesn't just stream raw readings; it computes derived metrics live, without buffering full timeseries on a device that doesn't have the memory for it.

The headline example: **channeling detection**. When water finds a low\-resistance path through the puck, it gushes through that channel and under\-extracts the rest, the espresso equivalent of a hot shard taking all the traffic. You detect it by watching how *variable* the puck resistance is during extraction. The right statistic is the [coefficient of variation](https://en.wikipedia.org/wiki/Coefficient_of_variation) of the resistance readings, and you can compute it in constant memory by carrying a running sum and sum\-of\-squares, then reconstructing the variance from them, no need to store the full series:

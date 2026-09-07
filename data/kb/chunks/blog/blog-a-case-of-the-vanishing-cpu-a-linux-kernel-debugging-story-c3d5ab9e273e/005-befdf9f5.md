---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"The
topic: the-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story-clickhouse
ch_version_introduced: '100.0'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 25
---

involved. Here is how you could measure the duration of any syscall using [`bpftrace`](https://github.com/bpftrace/bpftrace/blob/master/man/adoc/bpftrace.adoc): a tool that helps you run eBPF code inside the kernel to trace what it does and get useful insights into the kernel behavior.

```
tracepoint:syscalls:sys_enter_mincore /pid==$1/ {
    @start[tid] = nsecs;
}

tracepoint:syscalls:sys_exit_mincore /pid==$1 && @start[tid]/ {
    @latency_us = hist((nsecs - @start[tid]) / 1000);
    delete(@start[tid]);
}
```
Copy command
But running `bpftrace` requires privileges and cannot be done inside a standard Kubernetes pod. Instead, you should go to the node where your pod is running. From there, the easiest way to run `bpftrace` is the following (with an example of the healthy output):

```
# docker-bpf() { docker run -ti --rm --privileged -v /lib/modules:/lib/modules -v /sys/fs/bpf:/sys/fs/bpf -v /sys/kernel/debug:/sys/kernel/debug --pid=host quay.io/iovisor/bpftrace bpftrace "$@"; }

 # docker-bpf -e 'tracepoint:syscalls:sys_enter_mincore /pid==$1/ { @start[tid] = nsecs; } tracepoint:syscalls:sys_exit_mincore /pid==$1 && @start[tid]/ { @latency_us = hist((nsecs - @start[tid]) / 1000); delete(@start[tid]); }' $PID
Attaching 2 probes...
^C

@latency_us:
[0]                10402 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[1]                 1452 |@@@@@@@                                             |
[2, 4)               113 |                                                    |
[4, 8)               220 |@                                                   |
[8, 16)              123 |                                                    |
[16, 32)              17 |                                                    |
[32, 64)               5 |                                                    |
```
Copy command
Note that there might be a lot of unrelated pods running on the node \- you therefore need to identify the PID for the process of interest. Here are helpers I use for identifying PID using Kubernetes pod names:

`pod-pids() {
 ps ax | grep "/usr/bin/clickhouse" | grep -v grep \
 | awk '{print $1}' \
 | while read pid; do
 echo $pid `nsenter -t ${pid} -u hostname`;
 done;
}
# Outputs the PID of POD whose name match given argument substring
ppgrep() { pod-pids | grep $1 | cut -f 1 -d ' '; }`
However, despite my initial assumption, the `mincore` syscalls did not appear to be a significant factor. They did not appear at all, with not a single `mincore` syscall this time.

## Why is perf unresponsive? \#

When dealing with high CPU consumption, `perf` is one of the most effective tools for identifying where CPU time is spent. Unlike stack traces obtained using `gdb`, which provide a snapshot of execution at a single moment, `perf` continuously samples the program over time, allowing to build a more comprehensive profile of CPU usage.

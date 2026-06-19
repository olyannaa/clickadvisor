# The case of the vanishing CPU: A Linux kernel debugging story


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The case of the vanishing CPU: A Linux kernel debugging story

![](/_next/image?url=%2Fuploads%2Fsergei_fb38203a5b.png&w=96&q=75)Sergei TrifonovMar 5, 2025 · 40 minutes readA mysterious CPU spike in ClickHouse Cloud on GCP led to months of debugging, revealing a deeper issue within the Linux kernel’s memory management. What started as random performance degradation turned into a deep dive into kernel internals, where engineer Sergei Trifonov uncovered a hidden livelock. His journey through `eBPF` tracing, `perf` analysis, and a reproducible test case ultimately led to a surprising fix \- only for another kernel bug to surface right after. Curious, read on…


## The mystery begins [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#the-mystery-begins)


It started as an anomaly—an occasional hiccup in [ClickHouse Cloud](https://clickhouse.com/cloud) infrastructure that engineers struggled to explain. Occasionally, a random ClickHouse instance would max out its CPU consumption, become unresponsive, and remain frozen in that state indefinitely. Our monitoring system detected performance degradation, triggering alerts that paged our engineers, and in the worst cases, their instances went down entirely. Restarting the affected pods was the only fix, but it didn’t tell us why it happened or when it would strike again.


Something was wrong, but at first, we had no idea what. Worse, the problem was intermittent. Days would go by without incident, only for it to appear again unpredictably. The issue was consuming valuable engineering hours with each occurrence, and our support team was actively engaged, communicating with customers to gather additional context and provide updates.


The more we observed, the clearer the pattern became. Affected instances showed alarmingly high CPU usage, always reaching their quota and becoming throttled. Memory consumption was equally concerning, hovering just below the `cgroup` limit, yet pods were not restarting due to OOMs.


But the strangest revelation came when we started comparing environments. Every single case occurred in the Google Cloud Platform (GCP). Not once did it appear in AWS or Azure.


## Early investigation attempts [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#early-investigation-attempts)


In ClickHouse Cloud, we have a simple tool to collect all current stack traces from the ClickHouse server process running in the pod. It is based on `gdb`, a popular debugger on Linux. We just attach gdb to the process, gather backtraces from all the threads, and detach. We use it whenever the ClickHouse server hangs. It is invaluable in detecting deadlocks. Using this tool, we quickly gathered insights that deepened our investigation. The number of active threads was unusually high—more than a thousand, all working on either queries or some background activities. Many threads appeared to be waiting to enter critical sections, but it was not a deadlock—other threads were actively working while holding corresponding locks. Even more bizarre, many stack traces pointed to unexpected locations, such as `libunwind`, the library responsible for building stack traces required during handling exceptions.


The problem affected random pods, rendering them nearly non\-functional. They became so slow that every query sent to the server would hang indefinitely, yet the server did not restart automatically. This meant that each incident required a rapid manual restart to restore service. However, every investigation attempt was met with resistance—affected pods were so unresponsive that even basic debugging tools like `perf` and `ps aux` struggled to function. It was particularly unusual that `ps aux` itself would hang when executed. At first, we thought this was just another consequence of the extreme CPU load, but we did not yet realize that this would later turn out to be a crucial clue in unraveling the mystery.


Complicating matters, the problem was unpredictable. One day it would appear in one cluster, the next in another, with no discernible pattern. Different services were impacted at different times, making it impossible to correlate with recent deployments or changes. And with so many potential culprits—CPU spikes, high memory usage, excessive threads, too many exceptions \- it was difficult to determine what was a symptom and what was the root cause.


## Might it be a system call with unexpected consequences [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#might-it-be-a-system-call-with-unexpected-consequences)


We chased many theories. The stack traces we initially collected showed a significant amount of stack unwinding, suggesting a large number of exceptions were occurring during the issue. Naturally, we thought optimizing these operations might help. We tried improving stack trace symbolization by optimizing the internal symbol cache of ClickHouse, reducing contention on the cache’s global lock. It did not help.


Additionally, we looked into `[mincore](https://www.google.com/url?q=https://man7.org/linux/man-pages/man2/mincore.2.html&sa=D&source=docs&ust=1740570106684048&usg=AOvVaw0_vOA4df9q7q-OEQ93JTbq)` syscalls, which we knew could sometimes cause contention. The reason? Two months before the first occurrence of the mysterious CPU stalls, we had another incident involving service degradation. The investigation quickly discovered `mincore` syscalls to be the culprit, and we had completely disabled profilers globally for the time being.


In the ClickHouse server, there is an internal [query profiler](https://clickhouse.com/docs/en/operations/optimizing-performance/sampling-query-profiler). This profiler works by periodically sending signals to every thread of a query to obtain stack traces.



> There are actually two kinds of profilers: CPU and real\-time. The former only sends signals to active threads, which is similar to what most CPU profilers do. The latter sends signals to all (active and inactive) threads which reveals also [off\-CPU](https://www.brendangregg.com/offcpuanalysis.html) events like waiting on a mutex or other blocking syscalls.


At the time, ClickHouse linked a customized version of `libunwind`. It used `mincore` syscall to verify whether an address was valid in the process's address space. This was necessary to prevent crashes in some corner cases, but it had an unintended consequence: `mincore` syscalls require the `[mmap_lock](https://docs.kernel.org/mm/process_addrs.html)`.


This is a read\-write semaphore that the kernel maintains per process to protect memory mappings. Contention on this lock is problematic because any allocation could trigger a `mmap` syscall, introducing changes to the mappings and slowing down the process due to waiting on `mmap_lock`. When many threads are running while the real\-time profiler is enabled, this could lead to contention and overall performance degradation due to slow memory allocations.


It was [fixed](https://github.com/ClickHouse/ClickHouse/pull/60468) later, and now our `libunwind` does not use `mincore` anymore. After disabling it, we assumed the issue was resolved. However, we missed one crucial detail. The performance degradations related to the profiler had only been observed on GCP instances, not AWS. At the time, we didn't know why and assumed it was simply due to different workload patterns used by new customers running ClickHouse Cloud on GCP. With the profiler disabled, we were confident that this was no longer a factor. Yet, months later, a completely different issue emerged that was also GCP\-specific, telling us that we had missed something important.


## Digging deeper into mincore syscalls [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#digging-deeper-into-mincore-syscalls)


I was responsible for investigating the root cause of the previous issue with the profiler and started to work on the current issue as well. Firstly, I checked `mincore` syscalls—how many of them were happening and how slow they were. Since we had previously seen stack traces revealing a lot of stack unwinding, it was natural to suspect that these syscalls might be involved.


Here is how you could measure the duration of any syscall using [`bpftrace`](https://github.com/bpftrace/bpftrace/blob/master/man/adoc/bpftrace.adoc): a tool that helps you run eBPF code inside the kernel to trace what it does and get useful insights into the kernel behavior.



```

```
tracepoint:syscalls:sys_enter_mincore /pid==$1/ {
    @start[tid] = nsecs;
}

tracepoint:syscalls:sys_exit_mincore /pid==$1 && @start[tid]/ {
    @latency_us = hist((nsecs - @start[tid]) / 1000);
    delete(@start[tid]);
}
```

```

But running `bpftrace` requires privileges and cannot be done inside a standard Kubernetes pod. Instead, you should go to the node where your pod is running. From there, the easiest way to run `bpftrace` is the following (with an example of the healthy output):



```

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

```

Note that there might be a lot of unrelated pods running on the node \- you therefore need to identify the PID for the process of interest. Here are helpers I use for identifying PID using Kubernetes pod names:



```
pod-pids() {
    ps ax | grep "/usr/bin/clickhouse" | grep -v grep \
          | awk '{print $1}' \
          | while read pid; do
                echo $pid `nsenter -t ${pid} -u hostname`;
            done;
}
# Outputs the PID of POD whose name match given argument substring
ppgrep() { pod-pids | grep $1 | cut -f 1 -d ' '; }
```

However, despite my initial assumption, the `mincore` syscalls did not appear to be a significant factor. They did not appear at all, with not a single `mincore` syscall this time.


## Why is perf unresponsive? [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#why-is-perf-unresponsive)


When dealing with high CPU consumption, `perf` is one of the most effective tools for identifying where CPU time is spent. Unlike stack traces obtained using `gdb`, which provide a snapshot of execution at a single moment, `perf` continuously samples the program over time, allowing to build a more comprehensive profile of CPU usage.


We attempted to gather more data using `perf top`. Most of the time, it simply didn’t work \- no output, no errors, just an unresponsive terminal. This in itself was unusual, but we lacked an explanation. Then, in one incident that initially seemed no different from the others, we managed to get `perf` running, and what we saw was very interesting.



```

```
PerfTop:    8062 irqs/sec  kernel:100.0%  exact:  0.0% lost: 0/0 drop: 0/0 [4000Hz cpu-clock]
-----------------------------------------------------------------------------------

    64.28%  [kernel]       [k] shrink_lruvec
    28.81%  [kernel]       [k] lru_note_cost
     2.91%  [kernel]       [k] shrink_node
     1.84%  [kernel]       [k] _raw_spin_unlock_irqrestore
     0.38%  [kernel]       [k] count_shadow_nodes
     0.33%  [kernel]       [k] shrink_page_list
     0.15%  [kernel]       [k] _find_next_bit
     0.15%  [kernel]       [k] __remove_mapping
```

```

The CPU wasn’t being consumed by ClickHouse itself. Instead, all the processing power was being spent inside the kernel. A single function stood out: `shrink_lruvec`. This function is responsible for memory reclamation, but it was consuming an overwhelming amount of CPU cycles. Was the kernel itself the problem? It is important to note one difference between `gdb` and `perf`. When you stop the process with `gdb` (or internal profiler based on signals) you will never see a kernel function in your `backtrace` output, only a user\-space function. According to this, the previous `gdb` stack traces led us on the wrong path, they showed only the user\-space part of the full stack trace. With 100% samples hitting the kernel instead of user\-space code this leads to complete nonsense.


We still weren’t sure. Was this a cause or a side effect? Was ClickHouse simply pushing the system into memory pressure, or was the kernel behaving unexpectedly? Adding to the uncertainty, we had only managed to get `perf` working once. Maybe that particular incident was different in some way, or maybe we had stumbled upon a key factor without realizing it. This required another confirmation before we could arrive at any conclusions.


## Providing a runbook to investigate the issue [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#providing-a-runbook-to-investigate-the-issue)


The issue had been occurring sporadically for five months, appearing and disappearing across random GCP instances, eluding every effort to understand it. To check any new hypothesis we made a note for on\-call engineers about steps to perform if the problem reappeared and waited for a few days or sometimes a week for it to reoccur.


Desperate for answers, I compiled a runbook covering every diagnostic method at our disposal—`dmesg`, eBPF\-based kernel stack tracing, `pidstat`, `mpstat`, `perf`, even `sar` and `iostat` \- anything that might provide new insights. The approach was inspired by Brendan Gregg’s well\-known [60\-Second Linux Performance Analysis](https://www.brendangregg.com/blog/2015-12-03/linux-perf-60s-video.html), as any degraded service required rapid assessment. The goal was to quickly gather critical data without further impacting customers. It wasn’t long before the problem reappeared, and this time, we were ready.


We discovered that affected pods had 30 CPUs fully occupied running kernel code and entirely dedicated to handling page faults. But these page faults were happening at an unusually slow rate \- only 90 in 10 seconds, despite all CPUs being engaged. This wasn’t just inefficient \- something seemed completely broken.



```

```
# perf stat -p $PODPID -- sleep 10

 Performance counter stats for process id '864720':

         304675.80 msec task-clock                #   29.130 CPUs utilized          
             97934      context-switches          #    0.321 K/sec                  
               175      cpu-migrations            #    0.001 K/sec                  
                90      page-faults               #    0.000 K/sec
```

```

Using `perf`, we captured the key kernel stack trace that finally revealed what was happening.



```

```
#0  shrink_lruvec
#1  shrink_node
#2  do_try_to_free_pages
#3  try_to_free_mem_cgroup_pages
#4  try_charge_memcg
#5  charge_memcg
#6  __mem_cgroup_charge
#7  __add_to_page_cache_locked
#8  add_to_page_cache_lru
#9  page_cache_ra_unbounded
#10 do_sync_mmap_readahead
#11 filemap_fault
#12 __do_fault
#13 handle_mm_fault
#14 do_user_addr_fault
#15 exc_page_fault
#16 asm_exc_page_fault
```

```

And we managed to build a flamegraph. This is the reversed flamegraph, showing frame \#0 at the bottom.


![flamegraph_1.png](/uploads/flamegraph_1_3846bc2a5c.png)
An easy way for on\-call engineers was found to check for the problem using `pidstat` and looking into `%system` consumption:



```

```
# nsenter -a -t $PODPID pidstat 1
14:35:24      UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
14:35:25      101        66    0.00 3000.00    0.00    0.00 3000.00    39  clickhouse-serv
```

```

This enabled faster reaction times and reduced stress for on\-call engineers, ensuring immediate remediation while deeper analysis continued. At one point, we considered adding a liveness probe to all instances that would detect the issue and automatically restart affected pods. However, we realized that this approach would merely sweep the problem under the carpet along with any future issues leading to unresponsiveness. Instead, we decided to focus on understanding and fixing the root cause.


## A deeper dive into the kernel using bpftrace [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#a-deeper-dive-into-the-kernel-using-bpftrace)


Dealing with kernel bugs is never straightforward, but there are some common strategies engineers can follow.


First, gathering kernel stack traces using tools like `bpftrace` or `perf` is crucial to identifying bottlenecks. This step was already done. Tools based on eBPF are particularly powerful, not only for identifying bottlenecks but also for understanding what the kernel is doing and why. These tools allow engineers to trace almost any component in the kernel, from system calls and memory management to process scheduling and network activity, helping to understand the exact reasons behind the kernel's behavior.


Second, when analyzing a kernel stack trace, look for trace points in the kernel that might provide useful insights. In our case, we knew page reclaiming consumes all the CPU. To reclaim the page the kernel should first scan it using the `vmscan` subsystem. It has a few tracepoints:



```
# bpftrace -l 'tracepoint:vmscan:*'
tracepoint:vmscan:mm_vmscan_direct_reclaim_begin
tracepoint:vmscan:mm_vmscan_direct_reclaim_end
tracepoint:vmscan:mm_vmscan_lru_shrink_inactive
tracepoint:vmscan:mm_vmscan_lru_shrink_active
tracepoint:vmscan:mm_vmscan_writepage
tracepoint:vmscan:mm_vmscan_wakeup_kswapd
```

Kernel tracepoints have arguments that could be easily accessed from `bpftrace` scripts. For example, here is the script that collects the duration of every reclaiming procedure and also outputs their results: how many pages were reclaimed, what were the input parameters of the reclaiming procedure, etc.



```

```
tracepoint:vmscan:mm_vmscan_memcg_reclaim_begin /pid == $1/ {
    printf("%-8d %-8d %-8d %-16s mm_vmscan_memcg_reclaim_begin  order=%-10d gfp_flags=%-10ld\n",
        (nsecs - @epoch) / 1000000,
        pid,
        tid,
        comm,
        args.order,
        args.gfp_flags
    );
    @memcg_begin[tid] = nsecs
}

tracepoint:vmscan:mm_vmscan_memcg_reclaim_end /pid == $1/ {
    $elapsed = -1;
    if (@memcg_begin[tid] > 0) {
        $elapsed = nsecs - @memcg_begin[tid];
        @mm_vmscan_memcg_reclaim_ns = hist($elapsed);
        @memcg_begin[tid] = 0;
    }
    printf("%-8d %-8d %-8d %-16s mm_vmscan_memcg_reclaim_end    nr_reclaimed=%-10ld elapsed_ns=%-10ld\n",
        (nsecs - @epoch) / 1000000,
        pid,
        tid,
        comm,
        args.nr_reclaimed,
        $elapsed
    );
}
```

```

Below are the results that I obtained upon running this script against an unresponsive server process. For example, for one of the threads (note the first column is time in milliseconds), it means that it spent most of its time inside a reclaim before reentering another reclaim almost immediately after finishing the previous one. Also note that the number of reclaimed pages is not very large, although the procedure takes 1\-4 seconds every time:



```

```
346   874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=28  elapsed_ns=4294967295
346   874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
3545  874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=14  elapsed_ns=3199515681
3545  874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
7345  874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=56  elapsed_ns=3799726515
7345  874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
10145 874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=15  elapsed_ns=2800475796
10145 874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
13946 874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=17  elapsed_ns=3799783134
13946 874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
14849 874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=60  elapsed_ns=903085555
14849 874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
15645 874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=45  elapsed_ns=795982877
15645 874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
17442 874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=4   elapsed_ns=1796359224
17442 874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666
19941 874011 874761 Fetch mm_vmscan_memcg_reclaim_end    nr_reclaimed=16  elapsed_ns=2499699344
19941 874011 874761 Fetch mm_vmscan_memcg_reclaim_begin  order=0          gfp_flags=17902666

@mm_vmscan_memcg_reclaim_ns:
[128K, 256K)          11 |@                                                   |
[256K, 512K)          28 |@@@                                                 |
[512K, 1M)            11 |@                                                   |
[1M, 2M)              36 |@@@@                                                |
[2M, 4M)              16 |@@                                                  |
[4M, 8M)               8 |@                                                   |
[8M, 16M)              6 |                                                    |
[16M, 32M)             4 |                                                    |
[32M, 64M)             1 |                                                    |
[64M, 128M)           36 |@@@@                                                |
[128M, 256M)          58 |@@@@@@@                                             |
[256M, 512M)         161 |@@@@@@@@@@@@@@@@@@@@                                |
[512M, 1G)           354 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       |
[1G, 2G)             403 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[2G, 4G)             300 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@              |
[4G, 8G)             139 |@@@@@@@@@@@@@@@@@                                   |
[8G, 16G)             29 |@@@                                                 |
```

```

We opened a case with Google Cloud Support, reporting that some pods appeared to be running out of memory but were not being OOM\-killed as expected. Their first request was for a [sosreport](https://cloud.google.com/container-optimized-os/docs/how-to/sosreport), a diagnostic tool that collects system logs, hardware information, and kernel state for troubleshooting. We collected and provided several reports, expecting deeper insights. However, after analyzing the data, Google Cloud Support responded that they did not see any anomalies and that the pods were simply running out of memory and being OOM\-killed.


This response didn’t align with what we were observing. To prove that the issue was deeper than just an application misbehavior, we needed to provide a more detailed analysis. Google Cloud Support then requested a reproducible test case to help them better understand the problem, which ultimately moved the investigation forward.


## Why we couldn't simply upgrade the kernel [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#why-we-couldnt-simply-upgrade-the-kernel)


One of the immediate thoughts when dealing with a kernel issue is to upgrade or downgrade to a different version to see if the problem persists. However, in our case, upgrading was not a straightforward option due to the way Google Kubernetes Engine (GKE) manages its underlying operating system.


GKE nodes run on Container\-Optimized OS (COS), a specialized Linux distribution that is tightly integrated with GKE. The kernel version is not something users can freely select; instead, COS is tested and validated by Google, and each GKE release ships with a specific COS version. This means that when running on GKE, we cannot simply build an image with a different kernel version—we are limited to the versions that are officially supported and bundled with specific Kubernetes releases.
The closest thing to kernel selection is choosing a GKE release channel and picking a version within that channel. However, even this does not allow arbitrary kernel selection. Our clusters were running on GKE 1\.27, which came with COS\-105 and kernel 5\.15\. The nearest available upgrade option was GKE 1\.28, which shipped with COS\-109 and kernel 6\.1\. While upgrading to this version might have been an option, it was not an immediate fix—it required provisioning a new region with a newer Kubernetes version and migrating workloads, a non\-trivial task.
While running a fully custom kernel image was theoretically possible, it would no longer be COS, which was not an acceptable solution for our environment.


Even if an upgrade had been feasible, there was still uncertainty regarding whether it would resolve the issue. We assumed that kernel 5\.10 was unaffected, as we did not observe the problem on AWS, but there was no guarantee that kernel 6\.1 would be free from the bug. Ideally, support would have provided insights on whether newer versions were affected. However, at that stage, they were still investigating, and we had no confirmation on when (or if) a fix was available.


## Creating a reproducible test case for the issue [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#creating-a-reproducible-test-case-for-the-issue)


To fully understand and reliably trigger the problem, I experimented with multiple approaches based on what I knew at the time. I tried different stress patterns, varying memory access behaviors, and exploring thread contention scenarios. In ClickHouse Cloud, we disable swap and use [mlock](https://man7.org/linux/man-pages/man2/mlock.2.html) to lock the binary in memory, preventing it from being paged out and avoiding reclaiming penalties. While we generally avoid memory\-mapped files in most scenarios, completely eliminating the use of the Linux page cache remains challenging.


Any I/O your process performs, even reading configuration files, results in a page being cached by the kernel’s page cache. After numerous failed attempts at reproducing, I started tinkering with memory\-mapped files—this led to a breakthrough!


Although not used in production, memory\-mapped files are a simple way to create file\-backed pages to reclaim. I developed a [small C\+\+ program](https://github.com/serxa/stress_memcg) that reproduced the issue in 100% of the cases within a one\-minute runtime. The program runs inside a Docker container with 4 CPUs and 4 GB of memory. It follows a two\-phase execution pattern:


1. First Phase (0\-30 seconds):
	- Spawns 1,000 threads, each writing 1,000 files (totaling 4GB).
	- These files are then memory\-mapped and continuously iterated over in sequential order.
2. Second Phase (after 30 seconds):
	- Spawns another 1,000 threads that allocate anonymous memory.
	- These threads access memory randomly, triggering page faults.


Once the second batch of threads started running, we observed the following system behaviors, matching our production issue:


1. `ps aux` hangs system\-wide, indicating a stalled process information query.
2. `perf` stops functioning, failing to profile system activity.
3. The process stops making progress but consumes all available CPU resources.


With the code consistently triggering the issue, I examined what was happening during the stall. Running `strace ps aux` revealed that it was stuck while reading `/proc/$PODPID/cmdline`. Digging into the kernel source code for `procfs`, I found that the process attempts to lock `mmap_lock` of the target process, but this lock was held for an extraordinarily long time—ranging from 10 seconds to 2 hours in my tests.


This explained why `ps aux` was freezing: it needed to acquire `mmap_lock`, but the lock was held indefinitely. Since `perf` also requires information about running processes, it similarly hung, clarifying the second symptom.


To understand why `mmap_lock` was being held for so long, I wrote several `bpftrace` scripts to inspect kernel activity. These analyses provided key insights.


The first confirmed that `mmap_lock` was held for an exceptionally long time in a single thread:



```

```
# docker-bpf -e '
   tracepoint:mmap_lock:mmap_lock_acquire_returned /pid == $1/ {
       @start[tid] = nsecs;
   }
   tracepoint:mmap_lock:mmap_lock_released /pid == $1 && @start[tid] > 0/ {
       $us = (nsecs - @start[tid])/1000;
       if ($us > 50000) { // Print if held longer than 50ms
           printf("mmap_lock hold duration in PID %d TID %d COMM %s: %d us\n", pid, tid, comm, $us);
       }
       @hold_us = hist($us); // Collect histogram of locking duration
       @hold_avg_us = avg($us); // Aggregate average hold time
   }
   END { clear(@start); }
' $PODPID

mmap_lock hold duration in PID 2395806 TID 2396744 COMM r_file: 101349 us
mmap_lock hold duration in PID 2395806 TID 2396804 COMM r_file: 97864 us
mmap_lock hold duration in PID 2395806 TID 2396852 COMM r_file: 97305 us
mmap_lock hold duration in PID 2395806 TID 2396906 COMM r_file: 195284 us
mmap_lock hold duration in PID 2395806 TID 2396943 COMM r_file: 97771 us
mmap_lock hold duration in PID 2395806 TID 2396976 COMM r_file: 81960 us
mmap_lock hold duration in PID 2395806 TID 2396885 COMM r_file: 100698 us
mmap_lock hold duration in PID 2395806 TID 2396979 COMM r_file: 76614 us
mmap_lock hold duration in PID 2395806 TID 2396980 COMM r_file: 87041 us
mmap_lock hold duration in PID 2395806 TID 2397036 COMM r_file: 1297950 us
mmap_lock hold duration in PID 2395806 TID 2397378 COMM r_file: 199357 us
mmap_lock hold duration in PID 2395806 TID 2397385 COMM r_file: 118996 us
mmap_lock hold duration in PID 2395806 TID 2397409 COMM r_file: 791663 us
mmap_lock hold duration in PID 2395806 TID 2397286 COMM r_file: 93871 us
mmap_lock hold duration in PID 2395806 TID 2397959 COMM r_memory: 401062 us
mmap_lock hold duration in PID 2395806 TID 2398050 COMM r_memory: 230818460 us <---- 230 seconds
mmap_lock hold duration in PID 2395806 TID 2397984 COMM r_memory: 5490031 us
mmap_lock hold duration in PID 2395806 TID 2398045 COMM r_memory: 81746 us
mmap_lock hold duration in PID 2395806 TID 2397972 COMM r_memory: 387430 us
mmap_lock hold duration in PID 2395806 TID 2398040 COMM r_memory: 75750 us
mmap_lock hold duration in PID 2395806 TID 2397975 COMM r_memory: 76566 us
mmap_lock hold duration in PID 2395806 TID 2398142 COMM r_memory: 71836 us
mmap_lock hold duration in PID 2395806 TID 2398056 COMM r_memory: 77675 us
...
^C

@hold_avg_us: 1190

@hold_us:
[0]                 6949 |@@@                                                 |
[1]                98632 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
[2, 4)             40750 |@@@@@@@@@@@@@@@@@@@@@                               |
[4, 8)             31606 |@@@@@@@@@@@@@@@@                                    |
[8, 16)            27092 |@@@@@@@@@@@@@@                                      |
[16, 32)            7208 |@@@                                                 |
[32, 64)            1305 |                                                    |
[64, 128)            244 |                                                    |
[128, 256)           123 |                                                    |
[256, 512)           303 |                                                    |
[512, 1K)            276 |                                                    |
[1K, 2K)             151 |                                                    |
[2K, 4K)              62 |                                                    |
[4K, 8K)              47 |                                                    |
[8K, 16K)             16 |                                                    |
[16K, 32K)             4 |                                                    |
[32K, 64K)             0 |                                                    |
[64K, 128K)           53 |                                                    |
[128K, 256K)           8 |                                                    |
[256K, 512K)          13 |                                                    |
[512K, 1M)             5 |                                                    |
[1M, 2M)               2 |                                                    |
[2M, 4M)               0 |                                                    |
[4M, 8M)               1 |                                                    |
[8M, 16M)              0 |                                                    |
[16M, 32M)             0 |                                                    |
[32M, 64M)             0 |                                                    |
[64M, 128M)            0 |                                                    |
[128M, 256M)           1 |                                 | <---- 230 seconds
```

```

The second identified that the lock was acquired during page fault handling:



```

```
# docker-bpf -e '
   tracepoint:mmap_lock:mmap_lock_acquire_returned /pid == $1/ {
       @start[tid] = nsecs;
   }
   tracepoint:mmap_lock:mmap_lock_released /pid == $1 && @start[tid] > 0/ {
       $us = (nsecs - @start[tid])/1000;
       if ($us > 1000000) { // Save stack if lock was held longer than 1 second
           @[kstack] = count();
       }
   }
   END { clear(@start); }
' $PODPID

@[
   __mmap_lock_do_trace_released+113
   __mmap_lock_do_trace_released+113
   do_user_addr_fault+727
   exc_page_fault+120
   asm_exc_page_fault+34
]: 1
```

```

Finally, the third investigated CPU activity while the `mmap_lock` was held. Below, we show an interesting trick that could be used for such an investigation—profiling CPU through `bpftrace` and only collecting samples when the lock is held:



```

```
tracepoint:mmap_lock:mmap_lock_acquire_returned /pid == $1/ {
   @is_holding[tid] = 1;
}
tracepoint:mmap_lock:mmap_lock_released /pid == $1 && @is_holding[tid] == 1/ {
   @is_holding[tid] = 0
}
profile:hz:99 /pid == $1 && @is_holding[tid] == 1/ {
   @under_lock[kstack, comm] = count();
}
END { clear(@start); }
```

```

There is a [simple way](https://github.com/brendangregg/FlameGraph/blob/master/stackcollapse-bpftrace.pl) to build a flamegraph given stack traces obtained from `bpftrace`, and in our case, we can observe that most of the time was indeed spent on reclaiming using `shrink_lruvec`. This means that reclaiming for the group is done under the `mmap_lock` for the specific process that hits the memory limit. However, the cgroup may include many processes, and reclaimed pages do not necessarily belong to the process for which the `mmap_lock` is held. There is no real reason to hold the lock, besides page fault handling.


![flame_graph_2.png](/uploads/flame_graph_2_71729a27e9.png)
Another key finding explains why the issue only occurs when running thousands of threads. The thread that holds the `mmap_lock` may release the CPU by calling `__cond_resched()`. This kernel function yields CPU if needed to avoid long stalls and ensure fairness. But with a thousand threads running, the `mmap_lock` holding thread is only allocated CPU time after all other threads exhaust their CPU quanta (up to 4ms each) or block. This renders this long `shrink_lruvec` very inefficient. Every good programmer knows that it is a recipe for disaster to block while holding the lock! And yet, here we are, tinkering with Linux kernel 5\.15 that is doing something like this.


This investigation clarified many of the behaviors we had observed. Slow `mincore` calls in GCP turned out to be another symptom of excessive `mmap_lock` contention.


However, some mysteries remained:


- Why did `mmap_lock` occasionally last for extremely long periods (e.g., 2 hours) in rare cases?
- Why was `shrink_lruvec` taking an abnormally long time specifically on GCP but not AWS?


Running the test case in different environments allowed us to verify which setups were affected by the bug. AWS Elastic Kubernetes Service (EKS) uses its own Amazon Linux 2 (kernel 5\.10\) or Amazon Linux 2023 (kernel 6\.1\), and both kernels showed no signs of the issue. I shared the code with Google Support, and they checked that the Container\-Optimized OS exhibited the issue in versions COS 101 (5\.10\), 105 (5\.15\), and 109 (6\.1\), but it was not present in COS 113 (6\.1\). In Azure, we use Azure Linux based on 5\.15 and the test case suggested it should trigger the bug, but we never saw it in a production environment.



> As you can see, all Kubernetes providers use their forks of Linux that differ from one another and the vanilla kernel. This highlights the complexity of debugging such issues, as the same kernel version can behave differently depending on the distribution. Although all major cloud providers open\-source their forks, the kernel usually has patches and may be built with an unusual configuration.


## Understanding page reclaiming in Linux [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#understanding-page-reclaiming-in-linux)


To understand the issue we encountered, it helps to first explain how Linux manages memory and reclaims pages when under pressure. Pages in Linux are organized into Least Recently Used ([LRU](https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU)) lists. There are two kinds of pages that require separate lists: anonymous memory (such as heap and stack memory allocations) and file\-backed memory (page cache, mmap files, binaries). Note that swap is disabled in the ClickHouse Cloud, thus, anonymous memory cannot be reclaimed.


Each type has two LRU lists: ➀ active and ➁ inactive. The reason for having two lists is to track page usage over time efficiently. One key difference between Linux’s memory management and what a non\-kernel developer might expect is how pages are tracked for access. Unlike application\-level caches, where accessing an item could immediately move it to the head of a list, the Linux kernel does not execute code on every memory access. Instead, the processor sets an accessed bit (A bit) in the ➂ Page Table Entry ([PTE](https://en.wikipedia.org/wiki/Page_table#Page_table_entry)) when a page is read or written. Note, this process is handled by the hardware, which sets the access bit when a page is used. Later, the kernel scans memory and clears this bit to track whether the page is accessed again. The kernel can only observe and reset these bits during memory scanning to determine if a page remains in use.


![Blog_VanishingCPUDiagrams_202503_1_FNL.png](/uploads/Blog_Vanishing_CPU_Diagrams_202503_1_FNL_6b74cf6ea9.png)
If you are interested in looking into the current state of the `cgroup` your process belongs to, here is a command that prints out the contents of all related files (works for `cgroup` v1 only):



```

```
(cd /sys/fs/cgroup/memory/$(cat /proc/$PODPID/cgroup | grep memory | cut -d : -f 3); tail -n 100 *)
```

```

There are a lot of files describing the state of the memory controller of a `cgroup`. But here are the most interesting ones:



```

```
==> memory.failcnt <==
31 # the number of times cgroup hit the limit

==> memory.limit_in_bytes <==
4294967296 # the cgroup limit

==> memory.usage_in_bytes <==
4294967296 # current memory usage of the cgroup

==> memory.max_usage_in_bytes <==
4294967296 # maximum memory usage observed over cgroup lifetime
```

```

We can see that current usage equals the limit. So any memory allocation attempt triggers reclaiming. There is also a file showing the total size of every LRU list in bytes:



```

```
==> memory.stat <==
cache 4001792000
rss 128729088
mapped_file 4001792000
inactive_anon 128729088
active_anon 0
inactive_file 2411884544
active_file 1589776384
unevictable 0
```

```

The interesting thing I observed when the issue was occurring was that none of the values were changing besides `inactive_file` and `active_file`. It looked like the `cgroup` was completely frozen, doing nothing but reclaiming.


In Linux, page reclaiming is handled by the **vmscan** subsystem, which is responsible for freeing memory when needed. There are two main types of vmscan operations:


- **Asynchronous reclaim**: Triggered by system\-wide memory pressure, handled by the `kswapd` kernel thread. It proactively reclaims memory if memory\-pressure is present and is not designed to enforce `cgroup` memory limits. Note that there is no asynchronous reclaiming for cgroups.
- **Synchronous reclaim**: Triggered when a specific `cgroup` exceeds its memory limit (memcg reclaim) or system\-wide memory pressure is very high (direct reclaim). It is handled in the context of the process that requests memory. The requesting thread stalls until enough memory is reclaimed.


No matter what type of reclaim happens, it always initiates the scan. First, the kernel scans pages in the **inactive list**. If a page has its accessed bit set, it is marked as **referenced ➀** and moved to the head of the same **inactive list** instead of being immediately promoted. On a subsequent scan, if the page is accessed again, it is then moved to the **active list ➁**, meaning it was recently used and should not be reclaimed. Pages from the inactive list which are not accessed are reclaimed ➃ during vmscan. If during the scan there were no inactive pages to reclaim, then vmscan inspects active pages and can deactivate them ➂ regardless of the accessed bit. Note that every time a page is scanned, the kernel resets its accessed bit regardless of the page state.


![Blog_VanishingCPUDiagrams_202503_2_FNL (1).png](/uploads/Blog_Vanishing_CPU_Diagrams_202503_2_FNL_1_bb5e12e5a5.png)
It is important to note that there is no way for a page to be reclaimed unless it is scanned at least twice, because the page is brought to the inactive list by the initial pagefault with the set accessed bit. Moreover scans are never done for a cgroup unless it hits the memory limit. And at this point all pages are indistinguishable, they are all inactive with the accessed bit set.


## The livelock explained [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#the-livelock-explained)


To inspect what the kernel was doing during the excessively long hangups in the reproducing example, I developed a [`bpftrace` script](https://github.com/serxa/stress_memcg/blob/de6cb9e9cbaff258d503013bab522f7501b0cd29/env.sh.inc#L155-L452) that collects all related events and metrics on a per `mmap_lock` basis, i.e. during each acquire\-release cycle. Running this script on a GKE node with COS 109 successfully captured the issue.



```

```
=== [READ] mmap_lock hold stats in TID 1891547 COMM r_memory ===
    number of context switches: 2569
         number of preemptions: 0
      reclaim_throttle() calls: 0 WRITEBACK, 0 ISOLATED, 0 NOPROGRESS, 0 CONGESTED
        __cond_resched() calls: 2255178
         shrink_lruvec() calls: 13
           shrink_list() calls: 34172
                      nr_taken: 0
                     nr_active: 0
                nr_deactivated: 0         ⓷
                 nr_referenced: 0
                    nr_scanned: 1093267   ⓵ + ⓶ + ⓷ + ⓸
                  nr_reclaimed: 32        ⓸
                      nr_dirty: 0
                  nr_writeback: 0
                  nr_congested: 0
                  nr_immediate: 0
                  nr_activate0: 0       
                  nr_activate1: 564142    ⓶
                   nr_ref_keep: 529093    ⓵    
                 nr_unmap_fail: 0
                       runtime: 3699226 us
                      duration: 563997395 us
```

```

From this output, we can see that the thread was holding `mmap_read_lock`. While a read lock may not seem problematic at first, it becomes an issue when a writer starts waiting for it. At that point, all new readers are blocked until the writer acquires the lock, leading to a situation where a single reader monopolizes `mmap_lock`. Generally, `mmap_lock` is acquired for reading during page faults and for writing during operations like `mmap` or `munmap`.


The lock was held for 564 wall\-clock seconds, yet the actual CPU execution time was only 3\.7 seconds, meaning the thread was competing with around 150 other threads on average. This aligns with the fact that 1000 threads were scanning file memory within a container limited to 4 CPUs (an expected equal distribution is 250 threads per CPU). The thread was never preempted involuntarily; it voluntarily yielded CPU via `__cond_resched()`, which sometimes resulted in context switches, allowing other threads to run.


During this single critical section from acquire to release, the kernel scanned 1,093,267 pages (\~4\.27 GB) in an effort to reclaim memory for the `cgroup`. However, only 32 pages ⓸ were successfully reclaimed. The rest were either retained in the inactive LRU list ⓵ or moved to the active list ⓶.


I confirmed that the kernel was moving pages around the inactive and active lists, due to the way Linux handles memory management. Scans are never done before the process hits the limit, and because a page must be scanned at least twice before it can be reclaimed, we have to scan all the pages. Whether a page is moved to the active list or reclaimed depends on whether it is accessed in between scans.


The evidence was clear when I compared different events. In the first scan, we see a high count of cases where pages remain in the inactive LRU list ⓵. In the second scan, many of these pages were promoted ⓶, meaning they were accessed in between scans. There was a 3\-minute delay between the first and second scans, allowing background threads to access almost all pages at least once. This resulted in nearly all pages being activated. The reclaiming process only stops when it finds something to reclaim. If it does not succeed then OOM is triggered, but in our case, it did succeed and reclaimed 32 pages. This finally explains why there was no OOM.


## What can be done to fix the issue [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#what-can-be-done-to-fix-the-issue)


While we now understand what’s going on inside the kernel, it seems that the whole machinery used by Linux is not good enough to deal with this extreme case. It seems the kernel memory management capabilities need improvement or some rework. And indeed, we know that this kernel bug does not reproduce in newer kernels. Why is that?


The easiest way to unravel the reason is to repeat the same experiment on the healthy kernel and compare the results. After going through the same procedure of checking statistics per acquire\-release cycle I found that in a healthy kernel, two things are different.


The first one is that `mmap_lock` is no longer held during reclaiming procedures. This obviously wrong behavior has been fixed: `mmap_lock` is released before the new kernel starts reclaiming pages. Everything suggests that Amazon Linux 2 has such a fix, but direct observation in the production environment is impossible because it is based on the kernel 5\.10 \- which does not have the vmscan tracepoints used above.


The second one is that newer kernels are using another process for reclaiming. A significant change in memory management is the introduction of [Multi\-Gen LRU (MGLRU)](https://docs.kernel.org/mm/multigen_lru.html), a complete redesign of the LRU\-based page reclaim mechanism. It was introduced in Linux kernel 6\.1 and since then more and more distributions have enabled it by default. I decided to give it a try and enabled this feature. And it turned out to be the cure for COS 109!


If your distribution was built with `CONFIG_LRU_GEN` you could [enable](https://docs.kernel.org/admin-guide/mm/multigen_lru.html) it as easy as:



```

```
echo y >/sys/kernel/mm/lru_gen/enabled
cat /sys/kernel/mm/lru_gen/enabled
0x0007
```

```

It takes effect immediately without requiring a server restart. We verified that it does not cause any performance degradation in ClickHouse Cloud and have enabled it across the entire GCP fleet. Everything went smoothly, and the issue did not reappear for a week. I also gave a brief presentation to the team, explaining my findings and the fix. This story is finally over after 8 months of investigations with a simple and easy to apply fix.


At least, I thought this way. Until the same alert happened again!


## One final issue [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#one-final-issue)


I was disappointed, but I had to analyze the issue once more. What I found was entirely different—a new bug causing almost the same behavior. The CPU was throttled, running only the kernel code. It was reclaiming memory again, but this time, the reclaiming logic was fundamentally different: it was MGLRU. Tools like `perf` and `ps` were working just fine without any hangups. And as I later checked `shrink_lruvec` had very few calls to `mmap_lock`, with most not requiring this lock.


Realizing I was facing an entirely new situation, I had to start from scratch. I began with CPU profiling:



```

```
55.47% [kernel] [k] _raw_spin_unlock_irq
12.05% [kernel] [k] _raw_spin_unlock_irqrestore
```

```

This issue suggested some kind of spinlock eating all the CPU instead of shrink\_lruvec. This was unexpected. Further investigation took a few weeks because the issue was happening completely random and my earlier code to reproduce was useless for this particular case.


Although not everything was wrong. The good news is that with MGLRU, alerts for the issue were much less frequent. After investigating a few more cases I managed to find a clue.


I obtained kernel stack traces again and the most common one was the following:



```

```
#0  _raw_spin_unlock_irq  
#1  evict_folios        
#2  shrink_lruvec
#3  shrink_node
#4  do_try_to_free_pages
#5  try_to_free_mem_cgroup_pages
#6  try_charge_memcg
#7  charge_memcg
#8  __mem_cgroup_charge
#9  __filemap_add_folio
#10 filemap_add_folio
#11 page_cache_ra_unbounded
#12 do_sync_mmap_readahead
#13 filemap_fault
#14 __do_fault
#15 handle_mm_fault
#16 do_user_addr_fault
#17 exc_page_fault
#18 asm_exc_page_fault
```

```

Rebuilding the reverse flamegraph (frame \#0 is at the bottom), we can see there are a few paths leading to this spinlock and they all are very similar:


![flamegraph_3.png](/uploads/flamegraph_3_18dfff4943.png)
It is a bit of a mystery why `unlock` shows up in the flamegraph and not `lock`, which is where CPU should be spent while waiting on a spinlock. Anyway, given the stack trace I checked the kernel code. The easiest way to do this is to use an online kernel source browser like this [one](https://elixir.bootlin.com/linux). This allows you to easily switch between different kernel versions and lookup symbols appearing in the stacktrace. Although it does not index kernel code used by GCP or AWS it is still very handy.


I found the culprit: a spinlock called [lru\_lock](https://elixir.bootlin.com/linux/v6.1.85/source/include/linux/mmzone.h#L511), which is responsible for protecting the struct lruvec. The kernel creates this structure for each cgroup and node. It contains fields used by both MGLRU and the older mechanism of active and inactive lists. The function `evict_folios`, specific to MGLRU, acquires this spinlock during page reclamation.


A folio is a small group of contiguous pages managed together to reduce overhead, hence the name. The kernel allows concurrent scanning of pages in LRU lists. First, a thread [isolates](https://elixir.bootlin.com/linux/v6.1.85/source/mm/vmscan.c#L5025) a private list of pages to scan. Once scanning and reclaiming are complete, pages that should be kept are returned to the original LRU list.


Within the `evict_folios` function, there are two points where `lru_lock` is used. We observed that this lock is heavily contended due to constant locking and unlocking—but why?


Well, it is not very surprising \- if we recall that we have a lot of concurrently running threads and that every thread could be doing its own memory reclaim procedure independently. Every good programmer knows that spinlocks should be used in low contention scenarios if you want your CPU consumption to be sane. I did a quick check with `top` and found that during 3 seconds there were at least 138 threads active. 84% of stacktraces have `evict_folios` frame according to the flamegraph, so it is very likely that more than 100 threads are constantly trying to do something with the spinlock.


A week after this investigation, Google Support advised us to enable MGLRU but pointed out that it might not resolve the problem completely. Also, there is now a [public issue](https://issuetracker.google.com/363324206), created for the slow page reclaim problem in COS 105\. I shared our findings with them and the case was closed. I see no activity on fixing the kernel, so there are two options left. Either upgrade to a newer kernel or add automation to detect such livelocks and restart pods. For now, we have created liveness detection and restart systems. If you are using cgroups v2, there are [tools](https://facebookmicrosites.github.io/psi/docs/overview) that could help you do something similar.


## Conclusion [\#](/blog/a-case-of-the-vanishing-cpu-a-linux-kernel-debugging-story#conclusion)


Kernel bugs are notoriously difficult to handle. Identifying them is a challenge—your go\-to tools might fail, like `ps aux` and `perf` hanging, or they might mislead you, like `gdb` backtraces that never reveal kernel stack frames. Fixing kernel bugs is an even greater challenge, especially for those of us who aren't kernel developers. I'm not a kernel developer. But the software we create always runs on top of an operating system, and understanding how the kernel works is crucial.


Even if you identify the issue, rolling out kernel fixes presents another hurdle. In managed Kubernetes environments, you're often tied to a specific kernel version that can't be upgraded independently.


Kernel bugs will always exist—after all, the kernel is just another piece of software. The best we can do is to be prepared. This journey taught me a lot, not just about debugging but about the inner workings of the Linux kernel. I hope this story was both interesting and educational, shedding light on the tools, techniques, and insights that can help navigate similar challenges in the future.


If you’d like to try out ClickHouse Cloud on GCP (or AWS and Azure, for that matter), start your free $300 trial here: <https://clickhouse.com/cloud>

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

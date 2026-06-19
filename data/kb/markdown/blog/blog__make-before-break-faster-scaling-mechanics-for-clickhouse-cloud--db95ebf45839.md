# Make Before Break \- Faster Scaling Mechanics for ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Make Before Break \- Faster Scaling Mechanics for ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FImage_512x512_10_28e7c58ce2.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_2_fac5916c8f.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fjayme_29091e45c1.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmanish_bf5b64cc28.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_13_d97452778c.jpeg&w=96&q=75)[Ashwath Singh](/authors/ashwath-singh), [Manas Alekar](/authors/manas-alekar), [Jayme Bird](/authors/jayme-bird), [Manish Gill](/authors/manish-gill) and [Francesco Ciocchetti](/authors/francesco-ciocchetti)Apr 2, 2025 · 22 minutes read![make_before_break.png](/uploads/make_before_break_38e22d6ab7.png)
When ClickHouse Cloud was being created, the major factor in terms of making technical decisions was velocity. To that end, it was decided that our in\-house clickhouse\-operator will leverage StatefulSets to control server pods.


This was a reasonable choice \- Kubernetes StatefulSets are the go\-to choice for running stateful workloads like clickhouse server. And it served us well. StatefulSets give us a lot of advantages: we could attach PVCs (Persistent Volume Claims), we could do rolling restarts, and we could scale them out by just increasing the replica count.


However, one key decision that the clickhouse\-operator made was that all ClickHouse server replicas were managed by a single StatefulSet. Once again \- a reasonable choice. This is precisely how stateful workloads are meant to be handled.


With manual and automatic scaling coming into the picture, this decision proved to be a fateful one. When the decision to build auto\-scaling foundations was being taken, it was decided that the majority of ClickHouse workloads are better served with scaling up (vertically) rather than scaling out (horizontally). Hence, the existing scaling systems were created with vertical scaling in mind.


When a service needs more memory or CPU resources \- based either on the autoscaler’s decision making recommendations, or the customer’s manual trigger \- we do not increase or decrease the number of replicas. Instead, we do a rolling restart 1\-replica at a time. Upon restarting, the server pods come up with the new size.



> The CPU:Memory shape is currently preserved.


## Understanding pod evictions [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#understanding-pod-evictions)


It is worth our time to understand precisely how this happens. Below is an architecture diagram which gives a glimpse at how pods were historically resized in ClickHouse Cloud.


![pod_scaling.png](/uploads/pod_scaling_59ddb8e08c.png)
In the above diagram, the 2 interesting components are the autoscaler and the mutating webhook. The resizing operation for a pod can only happen upon a pod termination / restart. This is because it is precisely the moment of pod creation that the mutating webhook intercepts the pod and mutates the spec. This mutation causes the actual pod to be created with our desired size. As is clear from the diagram, the “right size” is something that gets decided based on 2 factors: customer\-set vertical scaling min and max limits, as well as recommendations coming from our recommender system based on historical usage data.


It should also be evident that we cannot restart all replicas at the same time. In order to minimise disruptions in the replicas, we have a Pod Disruption Budget (PDB). The PDB enforces certain constraints, such as only 1 pod is allowed to restart at any given time. The obvious consequence of this is that for a 3 replica cluster, we will have a sequential, rolling restart.


Another important factor to consider is the fact that a replica termination is rarely instantaneous. Usually there are various workloads running on the server pods \- from long running queries to backups etc. And we have to be cognizant of those while trying to evict pods. For example, we never evict a pod if a backup is running on it. And for long\-running queries (our definition is any query which has been running for over 10 minutes), we wait for up to 60 minutes for the query to finish. If the query is not finished by that time and scaling is really needed, we then go ahead and evict the pod.


The implications of the above are important \- in the worst case, when we evict a replica to resize it, it can take up to 1 hour to terminate gracefully before it comes back up again. When a ClickHouse replica restarts, it must also initialize and load tables and dictionaries \- a process whose duration depends on the number of tables and dictionaries in the cluster. Consequently, for a 3 replica cluster, it means resizing the entire cluster can take over 3 hours. Clearly, vertical scaling can be a slow process.


## Resource crunch [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#resource-crunch)


![resource_crunch.png](/uploads/resource_crunch_d03acf72b8.png)
There are additional implications of rolling restarts during scaling. Occasionally, the act of vertical scaling can make a cluster undergo more pressure than it otherwise would be under. This is due to the fact that when a replica is getting evicted, we first take it out of the load balancer \- we do not want the replica to accept any new queries when we know it is marked for termination. What this means is that the traffic that was being distributed across say 3 replicas will now be distributed only across the remaining 2 replicas. This of course is based on the assumption that upon replica termination, the client will retry the query \- and re\-establish the connection to ClickHouse Cloud in the process.


This might not be a huge problem if the cluster is not running heavy workloads \- say the utilisation is trending downwards and we are going to scale down anyway. However, if the utilisation is trending up and the cluster needs more resources (via vertical scaling), taking away a replica for 1 hour can be harmful for the cluster. Indeed, in the worst case scenarios, the remaining replicas can crumble under the pressure and might also get OOM\-killed or the CPU might get throttled.


## Make Before Break [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#make-before-break)


### And the limitations of StatefulSets [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#and-the-limitations-of-statefulsets)


For the reasons outlined above, it became clear that we needed a more efficient method of scaling vertically. We came up with something we call Make\-Before\-Break scaling. The idea here is fairly simple.


![limitations_stateful_sets.png](/uploads/limitations_stateful_sets_d00ef2e1fb.png)
Instead of doing a rolling restart, just immediately add more capacity to the existing cluster. This immediately solves both problems we described above \- there are no more rolling restarts and there is no more resource crunch.


- We do the "Make" operation, new pods get added to the cluster, and they come up with the correct size thanks to the webhook.
- We then do the "Break" operation which condemns the old pods and they eventually get terminated.


This is a simple idea in theory but in practice, the limitations of vanilla StatefulSets prevented us from achieving it.



> **Why?**
> 
>  Because Kubernetes StatefulSets are based on Ordinals. StatefulSets assign each pod a fixed ordinal index (like server\-0, server\-1, server\-2\), which determines its identity and startup order. This strict ordinal sequencing means you can’t easily add or remove arbitrary pods \- changing the set of replicas without disrupting this sequence becomes complex. For Make\-Before\-Break scaling, where we want to spin up new replicas (e.g., server\-3, server\-4\) before removing existing ones (e.g., server\-0, server\-1\), this rigidity becomes a fundamental limitation.


![ordinals.png](/uploads/ordinals_361d9e45f1.png)
So when we add replicas server\-3, server\-4 and server\-5 (our Make operation), removing server\-0, server\-1 and server\-2 are not trivial operations. For MBB to work, we need the ability to break arbitrary pods.


There are some workarounds like [StatefulSet Start Ordinals](https://kubernetes.io/blog/2023/04/28/statefulset-start-ordinal/) but they have caveats \- like the fact that moving the start ordinal would still mean we are breaking in a strict order, instead of breaking arbitrary pods. We also explored [Advanced StatefulSet](https://docs.pingcap.com/tidb-in-kubernetes/stable/advanced-statefulset)  and [CloneSets](https://openkruise.io/docs/next/user-manuals/cloneset/), but these had certain limitations, so we decided it was better to build this functionality in\-house.


The solution we landed on was a fairly simple one conceptually \- we refactored our Kubernetes operator to have a separate code\-path which would allow us to create multiple StatefulSets \- each StatefulSet owning its own server pod.


![sts.png](/uploads/sts_df308bf747.png)
With this approach, we get the flexibility of breaking any StatefulSet we want with the benefits of a StatefulSet controller still owning each individual pod. This approach is also much more advantageous vs directly owning the pods, because it means that potential bugs in our operator are much less likely to impact the running server pods \- as long as the STS objects are around, the server pods will keep running.


## Live migrations [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#live-migrations)


### Custom Kubernetes controllers and Temporal [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#custom-kubernetes-controllers-and-temporal)


We rolled out the MultiSTS approach in ClickHouse Cloud behind a feature flag last year. All new services came up in MultiSTS mode. However, we still had a significant amount of our existing fleet running in the old SingleSTS way. Migrating these services while allowing queries to run was the next big task.


### Live migration requirements [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#live-migration-requirements)


The migration from SingleSTS to MultiSTS needed to be \*\*Live \*\*because we wanted to avoid downtime for our customers. While a stop\-start migration would probably have been easier, it was actually a good idea to do the migrations live \- precisely because the migration itself would also be MBB style (we will \*Make \*new MultiSTS Pods and \*Break \*the old SingleSTS Pods). This was a crucial test for the MBB strategy itself. If it did not work for a one\-time migration of a cluster, we could hardly have expected it to work on a regular basis on every single Scale or Upgrade event.


So the requirements for the Live Migrations were as follows:


1. All customer queries (INSERTS/SELECTS/DDLs) should continue to work as is.
2. We needed to sync the catalog from old replicas to the new ones.
3. We needed to sync the metadata to avoid any potential data loss.
4. The migration should be reversible \- in case we run into an issue.
5. It should be possible to handle the intermediary state of 2 clusters: (SingleSTS \+ MultiSTS) during the migration.


This required us to write a new controller. Why do this, instead of refactoring the existing one?


- It provided us with a better de\-coupling of the main sync loop from the migration codepath.
- Isolating the complexity of the migration from the regular reconciliation is quite beneficial \- otherwise you could potentially introduce bugs in your main sync loop.
- Simplified development, maintenance and testing is much easier when it is isolated.


### Migration in action: MBB style [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#migration-in-action-mbb-style)


This custom controller responsible for moving the orchestration from singleSTS to multiSTS also worked MBB style \- the controller temporarily blocked operator reconciliations for a service, created MultiSTS replicas, removed its SingleSTS replicas from the load balancer and eventually used horizontal scaling mechanics to scale them in (aka “break” them).


Once the migration was complete, the migration controller handed over control back to the clickhouse\-operator for regular reconciliation operations. At this point the target service was running in MultiSTS mode. There was no downtime \- either SingleSTS or MultiSTS replicas were available for serving queries throughout the duration of the migration!


![Blog_MakeBeforeBreakAnimation_202503_V4.0.gif](/uploads/Blog_Make_Before_Break_Animation_202503_V4_0_cf8f29b50c.gif)
### Building Maintenance Mode [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#building-maintenance-mode)


Despite the careful orchestration steps of this controller, a lot of things could go wrong during a migration. Cloud operations \- some triggered by customers (like stopping the service), and some automatic (scheduled backups, idling based on service activity) can interfere with migrations \- that could lead to a very complicated scenario.


To avoid this, we created the concept of "Maintenance Mode" inside Clickhouse Cloud \- with the idea of leveraging Partial Maintenance \- a mode in which SQL queries directly hitting the replicas via our shared proxy would continue to work, but cloud operations would be temporarily disabled for the time of the maintenance.


![table.png](/uploads/table_585f04cc38.png)
### Migration orchestration \- Temporal [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#migration-orchestration---temporal)


There is another important aspect of these migrations \- coordination with other systems. The signal to trigger the migration needed to be communicated to the Kubernetes controller, and the result of a successful or failed migration needed to be communicated back.


The orchestration of these maintenance was done via Molen \- our in\-house [Temporal](https://temporal.io/)\-based automation system. Temporal comes with a lot of out\-of\-the\-box features that we leveraged in our workflow:


- **Durable Execution** \- This is a critical capability of Temporal that we leveraged. Once the migrations were finished, we wanted to restore the cluster back to its original configuration \- so we needed a place to store these configurations. Thanks to [Temporal’s Activity Inputs and Outputs](https://docs.temporal.io/activities), which are always durable and can be referenced further down in the workflow, we got all of this out of the box without doing any manual database operations.
- **Failure Detection** \- If a migration fails, we want to be notified and take action. This was made quite easy thanks to Temporal.
- **Retry Policies and Timeouts** \- Operations such as disabling idling, autoscaling, backups etc were handled via our internal management API. These operations could fail, and so with Temporal, we got automatic failure detections.
- **Scheduling Capabilities** \- Because we had 1000s of migrations that needed to happen, we wanted to schedule them in batches and perform these migrations at the rate of say 10\-20 per day. This was easily doable with the scheduling capabilities of Temporal.
- **Composable** \- We really liked the fact that with Temporal, you could chain activities together \- so the output of one activity could become the input of the next one. This kind of composability made for a very pleasant programming experience.
- **Scalable** \- At no point was the scalability of the temporal workers itself a concern. Once a workflow gets kicked off, the jobs get scheduled on the Temporal workers running on our internal tooling K8s cluster and everything "just worked".


We created 2 workflows:


- A "Watcher" parent workflow, which would run on a periodic schedule, check which clusters are scheduled for maintenance, and launch the child Migration workflow for each of them concurrently in Temporal.
- The child "Migration Workflow" \- responsible for triggering the migration for a single service.
	- Performs some sanity checks re: maintenance, checks configuration drifts and some other internal configuration details before placing the service into “Partial Maintenance Mode”.
	- Captures instance "state" (because the state itself changes during the migration)
	- Communicates with the migration\-controller.
	- Waits for various Kubernetes Events (Start, PodsReady, Finished) to be emitted from the controller itself.
	- Once the migration has finished, we remove the instance from “Partial Maintenance Mode” \- and the cluster state is restored to what it was before.


![migration_orchestration.png](/uploads/migration_orchestration_69d7d8ea4d.png)
### Migration controller design [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#migration-controller-design)


#### Reusing operator primitives [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#reusing-operator-primitives)


The migration controller is implemented as a wrapper around the main operator, designed specifically to orchestrate migration activities independently from regular operations. Within the migration controller, existing logic from the primary operator is reused for standard tasks such as synchronizing databases and tables, and configurations of the cluster. Meanwhile, the migration\-specific orchestration logic responsible for coordinating and sequencing migration steps is encapsulated entirely within the migration controller itself. This clear separation allows migration concerns to remain isolated and reduces operational risk. This design also allowed us to easily reverse migrations if necessary, reverting to the regular operator if needed.


![operator_primitives.png](/uploads/operator_primitives_848bcdb41d.png)
### Synchronisation with Kubernetes controllers [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#synchronisation-with-kubernetes-controllers)


The problem with having a wrapper controller while also having the primary operator reconciling the Custom Resource (CR) is that you now have 2 control loops acting on the same resource. This could be disastrous as you can no longer reason about the logic of the reconciliation. So we wanted to control this behaviour by only allowing one single controller to be “in charge” at any given time.


In order to achieve this, we implemented a mutex mechanism to ensure that only one controller process executes at any given time. This ensures serialized execution and prevents concurrency issues with two controllers reconciling the same resource.


![synchronization.png](/uploads/synchronization_cad3213649.png)
### Migration challenges [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#migration-challenges)


While it might sound fairly standard on paper, the fact that each ClickHouse Cloud customer is running a unique workload meant migrations were no easy feat. This was also our first major stress test of ClickHouse’s ability to add and remove replicas dynamically, as well as our own MultiSTS implementation. We ran into a lot of interesting challenges. At the time this migration was being developed, ClickHouse Server had not been tested in such an elastic environment, and we assumed that there would be a lot of new and interesting issues that could come up as a result of running clusters in which replicas are continuously getting added and removed.


Lets discuss some of the challenges here:


1. **Dropping replicas with unfinished `ON CLUSTER DDL` queries** If a replica was dropped while pending DDL operations were still in the queue, DNS lookups for the replica’s hostname could fail because the hostname no longer existed.


**Resolution:** We contributed fixes to ensure DDL queries better handle removed replicas and do not block the entire cluster.





2. **External Table Engines and Missing Connections** Some clusters used [external table engines](https://clickhouse.com/docs/engines/table-engines/integrations) (e.g., PostgreSQL, RabbitMQ, NATS) that no longer had active connections. In a traditional restart, these issues are often ignored; but in MBB migrations \- when entirely new replicas come online \- they would attempt to replicate these external dependencies and fail.


**Resolution:** We placed clusters in debug mode to identify broken connections, sometimes fixing them ourselves; in other cases, we worked with customers to restore the missing external dependencies.





3. **External Dictionaries with External Dependencies.** External dictionaries in ClickHouse can reference external tables or storage (like S3\). Missing or misconfigured references created failures when provisioning new replicas.


**Resolution:** We partnered with the ClickHouse core team, which addressed some of these problems in ClickHouse itself, making future migrations more robust.





4. **Materialized Views with Dropped Underlying Tables** If the underlying table for a Materialized View was dropped at some point, newly added replicas failed to recreate the table properly.


**Resolution:** Another fix contributed by the Core team, ensuring the system can correctly reestablish the necessary base tables during MBB migrations.


![mvs_tables.png](/uploads/mvs_tables_da1f1661af.png)
5. **Part Metadata Sync Issues** In ReplicatedMergeTree, local part metadata is stored on EBS. During a scale\-in operation with MBB, we run `SYSTEM SYNC REPLICA LIGHTWEIGHT` on a replica that remains live. This command originally attempted to sync parts from all other replicas, including newly created ones with ongoing inserts, leading to a stalemate.


**Resolution:** We added a `FROM` modifier, syncing only from the “breaking” replicas that were no longer handling traffic. This allowed us to gracefully sync part metadata without blocking.


![part_sync.png](/uploads/part_sync_174ee1687a.png)
6. **MultiSTS Topology Glitches** Our MultiSTS approach aims to spread replicas across zones (or availability domains). However, certain scenarios broke the desired `maxSkew` constraints (for example, going from replicas `[a, b]` to `[a, b, c, c]`, then removing `[a, b]` and ending up with `[c, c]` \- results in an invalid spread).


**Resolution:** We refined our topology logic to ensure that both new and old replicas satisfy zone constraints during transitions.


![multi_sts.png](/uploads/multi_sts_aedc165a84.png)
A lot of times, the solution was to put the cluster in debug mode and fix the issues from our side. But other times, the fix was to reach out to the customer and work with them to resolve the issue. We discovered some interesting ClickHouse core issues during this exercise that were fixed by the core team. All of this work ended up making ClickHouse more elastic and resilient to such operations. Importantly, the principle of “make before break” meant these issues were at no time ever disruptive to customer production workloads.


It took us a long time to finish these migrations, and it has been a painstaking exercise. Eventually we developed a muscle for identifying migration issues and quickly triaging them \- they were typically known and the fixes were simple (not easy), with a few exceptions that required special handling.


With MultiSTS migrations eventually finishing, ClickHouse Cloud customers could fully leverage Make Before Break!


Or could they?


## System tables [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#system-tables)


If you are a regular ClickHouse user, you must have come across the [system tables](https://clickhouse.com/docs/operations/system-tables) that clickhouse maintains. These tables are primarily meant for debugging purposes \- when something goes wrong with a query, a backup or the entire cluster, these tables are the first place a ClickHouse engineer looks.


Many system tables are in\-memory and hence not persistent. However, even the ones that are persisted (typically tables with `Engine = MergeTree` and a `_log` suffix, such as [`system.query_log`](https://clickhouse.com/docs/operations/system-tables/query_log) and [`system.text_log`](https://clickhouse.com/docs/operations/system-tables/text_log)) have been local to a replica. This means that system tables are not using the [SharedMergeTree Engine](https://clickhouse.com/docs/cloud/reference/shared-merge-tree) that is normally available for customers using ClickHouse Cloud. The reason for this is fairly simple \- if something goes wrong with SharedMergeTree, the ability to debug it via system tables needs to be preserved.


But at the same time, we really want to preserve system tables while performing Make Before Break operations. To that end, the ClickHouse Core team (specifically [Julia Kartseva](https://github.com/jkartseva)) implemented a new type of S3\-based Disk \- [s3\_plain\_rewritable](https://clickhouse.com/docs/en/operations/storing-data#s3-plain-rewritable-storage). By moving the system tables from the old disk type to the new `s3_plain_rewritable`, we were able to retain all system table data on object storage. Combined with the command to \*\*ATTACH \*\*a table based on its name, uuid and path on object storage, we can now preserve system tables during MBB operations.


![system_tables.png](/uploads/system_tables_045684441a.png)
### System table attachments [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#system-table-attachments)


While attachments seem like a simple enough operation, it requires very fine\-grained tracking of system tables. We modified the clickhouse\-operator to start tracking the tables along with their replica names. This is important because each replica has its own replica\-local copy of say `system.query_log`. Once the old 3 replicas go away, we want the ability to attach the system tables from those 3 replicas to the newly made replicas (ideally preserving the same table distribution).


It is also important for retention purposes. Currently we have a hard\-limit of 30 days. As more and more MBB operations happen in our cloud (for both Upgrades and Scaling), more and more system tables get accumulated. This has an impact on replica startup time. We are currently exploring avenues to improve this.


## Conclusion [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#conclusion)


Building MultiSTS, Make Before Break and Live Migrations has been a \~2 year project. This involved a long tail of a lot of customers who had unique challenges. We ended up with a lot of stragglers who took quite some time to migrate due. The typical flow would be to migrate a few customers \-\> encounter issues \-\> fix said issues \-\> continue again. We also had to be very proactive in communicating the impact of these migrations to our customers (via our UI and sending emails to critical customers).


We had to handle some customers with special requirements, and our engineers were hands\-on in managing those cases. Importantly, the principle of “make before break” meant these issues were at no time ever disruptive to customer production workloads.


In the end, it took us over 1 year to migrate the last customer and we are happy to report that now the entire fleet is running on MultiSTS. We were able to successfully enable the Make Before Break feature for our new Scale and Enterprise Tier customers. MBB is already running on thousands of clusters during scaling as well as upgrade operations. As a consequence, our scaling times have significantly improved and these clusters no longer suffer from the issues we described above, such as disruptions or long scale times. Capacity is now available relatively quickly.


If you are interested in working on similar challenges at the intersection of Cloud Infrastructure and Databases, please apply. We are hiring!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

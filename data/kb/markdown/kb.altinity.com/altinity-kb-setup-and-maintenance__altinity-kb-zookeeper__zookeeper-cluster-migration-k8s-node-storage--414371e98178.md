# ZooKeeper cluster migration when using K8s node local storage \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. [ZooKeeper](/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/)
3. ZooKeeper cluster migration when using K8s node local storage
# ZooKeeper cluster migration when using K8s node local storage

Describes how to migrate a ZooKeeper cluster when using K8s node\-local storage such as static PV, `local-path`, `TopoLVM`.

Requires HA setup (3\+ pods).

This solution is more risky than [migration by adding followers](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/altinity-kb-zookeeper-cluster-migration/)
because it reduces
the number of active consensus members but is operationally simpler. When running with `clickhouse-keeper`, it can be
performed gracefully so that quorum is maintained during the whole operation.

1. Find the leader pod and note its name
	1. To detect leader run `echo stat | nc 127.0.0.1 2181 | grep leader` inside pods
2. Make sure the ZK cluster is healthy and all nodes are in sync
	1. (run on leader) `echo mntr | nc 127.0.0.1 2181 | grep zk_synced_followers` should be N\-1 for N member cluster
3. Pick the first **non\-leader** pod and delete its `PVC`,
	1. `kubectl delete --wait=false pvc clickhouse-keeper-data-0` \-\> status should be `Terminating`
	2. Also delete `PV` if your `StorageClass` reclaim policy is set to `Retain`
4. If you are using dynamic volume provisioning make adjustments based on your k8s infrastructure (such as moving labels and taints or cordoning node) so that after pod delete the new one will be scheduled on the planned node
	1. `kubectl label node planned-node dedicated=zookeeper`
	2. `kubectl label node this-pod-node dedicated-`
	3. `kubectl taint node planned-node dedicated=zookeeper:NoSchedule`
	4. `kubectl taint node this-pod-node dedicated=zookeeper:NoSchedule-`
5. For manual volume provisioning wait till a new `PVC` is created and then provision volume on the planned node
6. Delete the first non\-leader pod and wait for its PV to be deleted
	1. `kubectl delete pod clickhouse-keeper-0`
	2. `kubectl wait --for=delete pv/pvc-0a823311-616f-4b7e-9b96-0c059c62ab3b --timeout=120s`
7. Wait for the new pod to be scheduled and volume provisioned (or provision manual volume per instructions above)
8. Ensure new member joined and synced
	1. (run on leader) `echo mntr | nc 127.0.0.1 2181 | grep zk_synced_followers` should be N\-1 for N member cluster
9. Repeat for all other non\-leader pods
10. (ClickHouse® Keeper only), for Zookeeper you will need to force an election by stopping the leader
	1. Ask the current leader to yield leadership
	2. `echo ydld | nc 127.0.0.1 2181` \-\> should print something like `Sent yield leadership request to ...`
	3. - Make sure a different leader was elected by finding your new leader
11. Finally repeat for the leader pod

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)

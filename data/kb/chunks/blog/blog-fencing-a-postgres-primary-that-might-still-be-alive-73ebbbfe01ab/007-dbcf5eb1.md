---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Fencing
topic: fencing-a-postgres-primary-that-might-still-be-alive-clickhouse
ch_version_introduced: '00.1'
last_updated: '2026-11-09'
chunk_index: 7
total_chunks_in_doc: 9
---

control plane also has no access to the host, so outside the guest it can only call the Compute Engine API. We have evaluated multiple ways, and none of the obvious Compute Engine options works as a fence:

| Option | What happens |
| --- | --- |
| Firewall deny rule | "Existing connections persist, and their associated traffic remains unaffected." ([docs](https://docs.cloud.google.com/firewall/docs/firewalls)) |
| Remove the external IP | Replication on the internal address keeps going, and on a VM with one NIC, the control plane also loses its SSH, which uses that address |
| Stop or delete the VM | The guest gets "up to a maximum of 120 seconds" to shut down ([docs](https://docs.cloud.google.com/compute/docs/instances/suspend-stop-reset-instances-overview)), and the Local SSD data is discarded. [skipGuestOsShutdown](https://docs.cloud.google.com/compute/docs/instances/decrease-shutdown-time) skips the wait, but in our tests, Google marked the stop as done 16 to 19 seconds after the call |
| Add a secondary NIC | A regular secondary NIC cannot be detached |


Thankfully, Dynamic NICs have become [generally available](https://docs.cloud.google.com/vpc/docs/release-notes) on GCP on October 30, 2025\. A Dynamic NIC is a VLAN sub\-interface of a regular NIC. The [GCP documentation](https://docs.cloud.google.com/vpc/docs/multiple-interfaces-concepts) says: "Adding or removing Dynamic NICs doesn't require restarting or recreating the instance." It also says that a Dynamic NIC shares the bandwidth and the queues of its parent NIC.

On GCP, nic0 is the management NIC, in a separate VPC (virtual private cloud network) that lets the control plane's SSH in and denies all egress. The user NIC is a Dynamic NIC on VLAN 2 in the database's private subnet, and it carries the public addresses, replication and the default routes. The fence deletes the user NIC with one call to [deleteNetworkInterface](https://docs.cloud.google.com/compute/docs/reference/rest/v1/instances/deleteNetworkInterface).

The documentation gives the usual delay for adding a Dynamic NIC and nothing about when traffic stops after a delete, so we measured it. In our trials, the last packet on any user flow came 0\.7 to 2\.5 seconds after the request, and Google marked the operation as done 5\.0 to 7\.0 seconds after it.

## When all options fail \#

The old primary's state machine starts one child job per mechanism, all at the same time:

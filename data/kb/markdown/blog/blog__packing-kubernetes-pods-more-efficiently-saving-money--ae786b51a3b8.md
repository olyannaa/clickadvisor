# Saving Millions of Dollars by Bin\-Packing ClickHouse Pods in AWS EKS


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Saving Millions of Dollars by Bin\-Packing ClickHouse Pods in AWS EKS

Vinay Suryadevara \& Jianfei HuOct 12, 2023 · 13 minutes read![K8s_scheduler_more_text.png](/uploads/K8s_scheduler_more_text_78920b874d.png)
## Introduction [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#introduction)


At ClickHouse Cloud, we love Kubernetes and we run our customer ClickHouse clusters (servers and keepers) in Kubernetes. We use [Elastic Kubernetes Service](https://aws.amazon.com/eks/) (EKS) for ClickHouse clusters hosted in AWS. Server pods from different ClickHouse clusters can be scheduled onto the same EKS node. We use Kubernetes Namespaces \+ Cilium for isolation. With EKS clusters being provisioned in new regions to support our customers, our fleet size has been growing considerably, and so have the infrastructure costs for EC2 instances.


To optimize the cost, we analyzed our EKS node utilization. EC2 instances are charged by the hour and not based on usage, so an underutilized node/fleet meant we were leaving money on the table. Costs can be lowered by improving utilization and reducing the total number of EC2 nodes required. Read on to learn how we improved our pod allocation and saved millions of dollars.


## Evaluating EKS node utilization [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#evaluating-eks-node-utilization)


In wanting to make our resource consumption as efficient as possible we undertook an exercise to identify how our pods were allocated. We analyzed CPU/Memory utilization in our EKS cluster nodes. The screenshots below are from [eks\-node\-viewer](https://github.com/awslabs/eks-node-viewer), a tool to visualize the EKS resources utilization by node.


![previous_k8s_cpu.jpg](/uploads/previous_k8s_cpu_3c4ab350de.jpg)

![previous_k8s_cpu_2.jpg](/uploads/previous_k8s_cpu_2_27d8d192e1.jpg)
Picture 1 shows the CPU utilization percentage in one of our larger EKS clusters. The entire cluster’s CPU utilization was around 50%. Additionally, many large and expensive nodes (shown in picture 2\) were not fully utilized. Based on the `eks-node-viewer` results for our clusters, we concluded that server pods were not tightly packed among nodes. Two ClickHouse pods that could have been scheduled onto the same node were instead scheduled on different nodes, leading to us needing a higher number of EC2 nodes for the same amount of pods, lower resource utilization per node, and higher fleet costs. CPU/Memory resources on a lot of the nodes in our cluster were mostly idle, but we were still being charged for the nodes.


## Root cause analysis [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#root-cause-analysis)


After some investigation, we identified the root cause of the low utilization.


1. The Kubernetes default scheduler uses ***[LeastAllocated](https://kubernetes.io/docs/reference/scheduling/config/)*** scoring policy to score nodes when scheduling a pending pod onto available nodes. ***[LeastAllocated](https://kubernetes.io/docs/reference/scheduling/config/)*** scoring policy favors nodes that have a higher amount of resources available, which leads to a sparse distribution of pods on cluster nodes.
2. This ***[LeastAllocated](https://kubernetes.io/docs/reference/scheduling/config/)*** scoring policy makes a node scale's scaling down very unlikely. Imagine an old pod is terminated on a node. This node will then be preferred by the scheduler for the new pods to be scheduled. Therefore, the node utilization is hard to drop below the cluster autoscaler's threshold to be reclaimed.


Meanwhile, we also had three additional requirements and constraints for the new solution:


1. Increase the resource (CPU/Memory) utilization across our fleet (and reduce our EC2 footprint and costs).
2. Do not impact customer experience, such as increasing ClickHouse instance provisioning time.
3. Minimize the disruption for our customer's running instances.


Taking these factors into account, we explored a few potential solutions.


## Tuning cluster autoscaler and overprovisioning (Abandoned) [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#tuning-cluster-autoscaler-and-overprovisioning-abandoned)


One obvious approach is to tune down the [cluster autoscaler scale\-down threshold](https://aws.github.io/aws-eks-best-practices/cluster-autoscaling/#additional-parameters). However, this means more customer pods will be evicted frequently, and this did not meet requirement \#3 (disruption to customer queries).


We also briefly considered overprovisioning the node by tuning the resource request and limit. However, overprovisioning resources can cause contention. But neither CPU contention (query being throttled) or memory contention (potentially OOM killed) is acceptable in terms of meeting our customer experience.


## Proactive packing of pods (abandoned) [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#proactive-packing-of-pods-abandoned)


We also considered adding the annotation [cluster\-autoscaler.kubernetes.io/safe\-to\-evict](https://kubernetes.io/docs/reference/labels-annotations-taints/#cluster-autoscaler-kubernetes-io-safe-to-evict) to ClickHouse pods. This allows the Kubernetes cluster autoscaler to evict pods when a node utilization falls below a certain threshold. However, pod evictions can bring disruption to our customers. For example, a long\-running query will be interrupted.


We had already configured the [PodDisruptionBudget](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/#pod-disruption-budgets) for ClickHouse servers to limit only one pod in a [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) to be unavailable at any time. But from our experience, making a cluster autoscaler terminate some pods at a random time is still too disruptive for a stateful workload like ClickHouse.


Hence, we decided not to choose this approach.


## [Bin\-packing](https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/) pods using the MostAllocated scoring policy [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#bin-packing-pods-using-the-mostallocated-scoring-policy)


Instead, we decided to change the kube\-scheduler (default Kubernetes scheduler) scoring policy from LeastAllocated to [MostAllocated](https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/) to pack our clusters more efficiently. This solution implements the [bin\-packing](https://en.wikipedia.org/wiki/Bin_packing_problem) paradigm for our pods. Why does this help?


1. When a new pod needs to be created, the scheduler now prefers a node with a higher utilization ratio. This makes the cluster's overall utilization higher over time.
2. When old pods are terminated on a node, that node is less likely to be considered and, therefore, more likely to reach a low utilization threshold. Eventually, the cluster autoscaler can remove this node from the cluster, reducing total cost.


This policy is part of the **NodeResourcesFit** plugin that is enabled by default in Kubernetes. Once this setting is enabled, during the pod scheduling phase, Kubernetes scheduler performs the following actions:


- First, it identifies the nodes in the cluster that have the resources available, as specified in the pod request spec. This is the "filtering phase."
- Next, it will rank the filtered nodes in descending order of their combined resource utilization (CPU and Memory). This is called the "scoring phase."
- The node picked for the pod will always be the one that can fit the pod and has the highest resource utilization.


With a solution that fits all our requirements, we decided to investigate how to specify this scheduling policy in EKS.


## EKS settings support for kube\-scheduler customization [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#eks-settings-support-for-kube-scheduler-customization)


As we started investigating how to set this policy for the kube\-scheduler in EKS, we discovered that EKS does not have support for customizing the kube\-scheduler via EKS settings/config. This [feature has been requested](https://github.com/aws/containers-roadmap/issues/1468) by a number of users, but there is currently no indication from AWS about adding support in the near future. Since we couldn’t do this through EKS settings, we opted to set up a custom scheduler ourselves in our Kubernetes cluster.


## Custom scheduler with `most-allocated` scoring policy [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#custom-scheduler-with-most-allocated-scoring-policy)


In order to set up a custom scheduler for pods in our cluster, we mainly followed the [handy guide provided by Kubernetes](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/). Kubernetes lets you create your own scheduler binary as well, though this was not necessary in our case, as the existing kube\-scheduler image with the `most-allocated` scoring policy satisfied our requirements. In order to create this scheduler within our cluster, we took the following steps:


1. Built and deployed the kube\-scheduler image to our container registry. We couldn’t find a public registry that hosted this image. It is not ideal for us to maintain this image, but there is no alternate solution currently.
2. Created a deployment for the scheduler, as mentioned in the [guide](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/). In the configMap, we provided the relevant settings for the scoring strategy \- ‘MostAllocated’ along with the weights for CPU/Memory when considering the allocation. The profile section of the configMap looked like this:



```
 profiles:
        - pluginConfig:
            - args:
                apiVersion: kubescheduler.config.k8s.io/v1beta3
                kind: NodeResourcesFitArgs
                scoringStrategy:
                    resources:
                        - name: cpu
                          weight: 1
                        - name: memory
                          weight: 1
                    type: MostAllocated
              name: NodeResourcesFit
          plugins:
            score:
                enabled:
                    - name: NodeResourcesFit
                      weight: 1
          schedulerName: <schedulerName>

```

1. In order to ensure high availability, we chose to define three pods in our custom scheduler deployment, with leader election enabled, so that only one pod would do the active scheduling with the other two pods on standby.
2. We deployed this scheduler to our cluster and then updated our pods to use this most\-allocated scheduler by specifying the schedulerName in the [PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#podspec-v1-core).


With this setup, we could ensure that the throughput of scheduling is similar to the existing kube\-scheduler, as well as having redundancy built into the custom scheduler setup. We can also increase the cluster resource utilization with minimum disruption.


## System utility workloads [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#system-utility-workloads)


Our EKS cluster has a few system pods that are responsible for utility workloads, such as CoreDNS, ArgoCD, Cilium Cluster Mesh, etc. Sometimes, these are the only remaining pods on a low\-utilization node. The cluster autoscaler has problems evicting some of these because they use local storage. These occupied nodes, in turn, can’t be scaled down.


To solve this, we annotated all such system utility workloads with [safe\-to\-evict: true](https://kubernetes.io/docs/reference/labels-annotations-taints/#cluster-autoscaler-kubernetes-io-safe-to-evict).


## Over provisioning for smoother scale out [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#over-provisioning-for-smoother-scale-out)


The EKS cluster autoscaler pod itself can also block a node being reclaimed. For the autoscaler, we chose to make it run on a small node instead of configuring `safe-to-evict: true`. This provided better stability.


In ClickHouse Cloud, we use an [overprovisioning](https://aws.github.io/aws-eks-best-practices/cluster-autoscaling/#overprovisioning) workload recommended by the EKS cluster autoscaler. We create workloads with similar resource requirements but lower [PriorityClass](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass). This lower priority allows the eviction of the overprovisioning pods for the ClickHouse pods.


We noticed that when overprovisioning pods use the `default-scheduler`, and ClickHouse pods use the custom scheduler, the preemption does not work. Because each scheduler only preempts the pods scheduled by itself. In this case, the cluster autoscaler also falsely thinks that scaling up is not needed. To solve this and make things more consistent, we made the overprovisioning pods also use the custom scheduler.


## Testing and rollout [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#testing-and-rollout)


In order to ensure no performance degradation with the custom scheduler, we also conducted some pod scheduling stress tests. We created a job to continuously create pods to be scheduled by the custom scheduler. We then killed the custom scheduler pod that holds the lease lock. We observed that other scheduler standby pods quickly took over. The pod scheduling was not impacted significantly, and the throughput of scheduling was also not a concern based on our tests.


Another potential risk was the increasing of the pod cold start\-up time. Now that clusters are more packed, *in theory*, new instance creation is more likely to trigger a nodegroup scale\-up to schedule the pending pods. In order to observe this, we measured the P90 and P99 cold start\-up times to check the impact. We verified that this impact is negligible. This can be due to node provisioning for accommodating ClickHouse service does not happen frequently enough to have a big impact.


When it came to the final rollout, we still proceeded with caution:


1. We rolled out the scheduler change region by region and started with a few small regions.
2. Within a single region, we first only updated smaller ClickHouse instances before gradually applying this scheduler to all the instances in the cluster.
3. Once the pod spec is updated with this custom scheduler for *‘schedulerName’* field, running Clickhouse pods will be rescheduled using the new scheduler. Since we already configured our stateful sets with a pod disruption budget along with graceful shutdown (to avoid disrupting running queries), we did not experience any disruption for our customer instances when scheduler was changed. After this one time rescheduling, running pods will never be affected again by scheduler change which satisfies requirement \#3 in a way previous solutions do not.


## Cluster Utilization After Rollout [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#cluster-utilization-after-rollout)


As a direct result of these changes, cluster utilization went up to 70%.


![new_k8s_cpu.jpg](/uploads/new_k8s_cpu_26536b948a.jpg)
We noticed about a 10% reduction in the number of nodes, with the highest savings coming due to a few large 24xl nodes being cleaned up. Together with the large node reduction, we achieved more than 20% reduction in EC2 cost.


Finally, we also cross\-referenced with our [AWS Cost and Usage Report](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html), which confirmed a similar amount of savings.


## Conclusion [\#](/blog/packing-kubernetes-pods-more-efficiently-saving-money#conclusion)


To summarize, we significantly reduced our EKS infrastructure cost by changing the Kubernetes scheduler scoring policy to `MostAllocated`. We achieved this by setting up a custom scheduler (kube\-scheduler image with `MostAllocated` scoring policy) in our EKS clusters. This approach nicely balanced both cost reduction and maintaining the stability of our customers’ workloads. We also thoroughly annotated a few preemptable system workloads to ensure nodes can be timely reclaimed.


For us, the success of this project was measured in cost savings achieved as well as having no drop in reliability or performance for customers.


With the aforementioned changes, we were able to increase our EKS cluster resource utilization by 20 \- 30% and also achieve commensurate cost savings on EC2 instances in our EKS clusters.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

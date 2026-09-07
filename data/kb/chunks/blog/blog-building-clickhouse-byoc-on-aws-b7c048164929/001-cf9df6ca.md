---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-clickhouse-byoc-bring-your-own-cloud-on-aws-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 10
---

# Building ClickHouse BYOC (Bring Your Own Cloud) on AWS \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Building ClickHouse BYOC (Bring Your Own Cloud) on AWS","description":"Learn how we built ClickHouse BYOC (Bring Your Own Cloud) on AWS, tackling challenges like infrastructure automation, network security, and resource management to deliver a seamless, fully managed deployment within customer\-controlled environments.","image":"/uploads/blog\_byoc\_on\_aws\_c11d27abe3\.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2025\-03\-12T15:09:23\.933Z","dateModified":"2026\-03\-03T12:30:39\.608Z","author":\[{"@context":"https://schema.org","@type":"Person","name":"Jianfei Hu","url":"https://clickhouse.com/authors/jianfei\-hu","@id":"https://clickhouse.com/authors/jianfei\-hu\#person","image":"/uploads/neutral\_avatar\_400804ae96\_5c370e757b.png"},{"@context":"https://schema.org","@type":"Person","name":"Yiyang Shao","url":"https://clickhouse.com/authors/yiyang\-shao","@id":"https://clickhouse.com/authors/yiyang\-shao\#person","image":"/uploads/Image\_512x512\_5\_330c6e9bbc.png"}]}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Building ClickHouse BYOC (Bring Your Own Cloud) on AWS

![neutral avatar 400804ae96](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)![image 512x512 5](/_next/image?url=%2Fuploads%2FImage_512x512_5_330c6e9bbc.png&w=96&q=75)[Jianfei Hu](/authors/jianfei-hu) and [Yiyang Shao](/authors/yiyang-shao)Mar 12, 2025 · 17 minutes read![Blog_BYOC_202502_V1.0-02.png](/_next/image?url=%2Fuploads%2FBlog_BYOC_202502_V1_0_02_6b231bf877.png&w=2048&q=75)

In this blog post, we’ll discuss in detail how we built this new product offering, including the challenges we faced, and how we worked through them.

## Introduction to BYOC \#

The concept of Bring Your Own Cloud (BYOC) is becoming increasingly popular as organizations seek greater control over their cloud environments, while also benefiting from the flexibility and scalability that cloud platforms provide. At ClickHouse, we recognized this trend and saw an opportunity to offer our customers a way to deploy ClickHouse in their own cloud infrastructure, specifically on AWS.

BYOC allows customers to deploy ClickHouse Cloud in their own Virtual Private Cloud (VPC) , thereby they are in control of networking, security, and compliance, while still leveraging the benefits of a fully managed offering. This deployment model provides a balance between the autonomy of self\-managed infrastructure and the convenience of a fully managed database service.

When designing this offering, we tackled a few interesting challenges to ensure a seamless integration of ClickHouse with the customer’s cloud environment. These challenges included setting up and managing the VPC, ensuring network connectivity, implementing auto\-provisioning mechanisms for cloud resources, and providing the right level of abstraction to make the solution both user\-friendly and flexible.

## Key challenges \#

Implementing a BYOC model introduces several challenges that must be addressed to ensure a seamless and secure experience for customers.

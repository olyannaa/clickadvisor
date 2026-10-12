---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Executable
topic: executable-udfs-are-now-generally-available-on-clickhouse-cloud-clickhouse
ch_version_introduced: '3.25'
last_updated: '2026-10-12'
chunk_index: 1
total_chunks_in_doc: 18
---

# Executable UDFs are now generally available on ClickHouse Cloud \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Executable UDFs are now generally available on ClickHouse Cloud","description":"Executable UDFs are now generally available on ClickHouse Cloud across AWS, GCP, and Azure, with native runtimes, network access, observability, and API and Terraform support.","image":"/uploads/UD\_Fs\_GA\_3d5009e61d.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2026\-10\-05T14:46:00\.886Z","dateModified":"2026\-10\-05T14:46:00\.765Z","author":\[{"@context":"https://schema.org","@type":"Person","name":"Francisco Neves","url":"https://clickhouse.com/authors/author\-francisco\-neves","@id":"https://clickhouse.com/authors/author\-francisco\-neves\#person","image":"/uploads/Francisco\_Neves\_407b3f3902\.png","jobTitle":"Full Stack Engineer "},{"@context":"https://schema.org","@type":"Person","name":"San Tran","url":"https://clickhouse.com/authors/san\-tran","@id":"https://clickhouse.com/authors/san\-tran\#person","image":"/uploads/216\_0\_2\_4d92aea0d9\.jpg","jobTitle":"Principal Product Security Engineer"},{"@context":"https://schema.org","@type":"Person","name":"Jia Xu","url":"https://clickhouse.com/authors/jia\-xu","@id":"https://clickhouse.com/authors/jia\-xu\#person","image":"/uploads/T02\_EM\_6\_F031\_P\_U0745\_SR\_32\_V7\_8cc6d2a629c9\_512\_7d7b8e0c15\.jpg","jobTitle":"Senior Software Engineer"},{"@context":"https://schema.org","@type":"Person","name":"Zach Naimon","url":"https://clickhouse.com/authors/zach\-naimon","@id":"https://clickhouse.com/authors/zach\-naimon\#person","image":"/uploads/Zach\_Naimon\_2f4cfc668e.jpeg"},{"@context":"https://schema.org","@type":"Person","name":"Ilya Andreev","url":"https://clickhouse.com/authors/ilya\-andreev","@id":"https://clickhouse.com/authors/ilya\-andreev\#person","image":"/uploads/T02\_EM\_6\_F031\_P\_U06\_DLSR\_8\_K6\_H\_4bfdbed89520\_512\_cbff481702\.jpg","jobTitle":"Senior Software Engineer"},{"@context":"https://schema.org","@type":"Person","name":"Hanzi Jiang","url":"https://clickhouse.com/authors/hanzi\-jiang","@id":"https://clickhouse.com/authors/hanzi\-jiang\#person","image":"/uploads/T02\_EM\_6\_F031\_P\_U0\_AFX\_7180\_SJ\_4e05006047b5\_512\_d901e206d9\.png","jobTitle":"Software Engineer"},{"@context":"https://schema.org","@type":"Person","name":"Kevin Zhang","url":"https://clickhouse.com/authors/kevin\-zhang","@id":"https://clickhouse.com/authors/kevin\-zhang\#person","image":"/uploads/T02\_EM\_6\_F031\_P\_U043\_R4\_LCRFS\_e0746edacb29\_512\_078317ee8d.jpg","jobTitle":"Principal Software Engineer"}]}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Executable UDFs are now generally available on ClickHouse Cloud

![francisco neves](/_next/image?url=%2Fuploads%2FFrancisco_Neves_407b3f3902.png&w=96&q=75)![216 0 2](/_next/image?url=%2Fuploads%2F216_0_2_4d92aea0d9.jpg&w=96&q=75)![t02em6f031p u0745sr32v7 8cc6d2a629c9 512](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U0745_SR_32_V7_8cc6d2a629c9_512_7d7b8e0c15.jpg&w=96&q=75)![zach naimon](/_next/image?url=%2Fuploads%2FZach_Naimon_2f4cfc668e.jpeg&w=96&q=75)![t02em6f031p u06dlsr8k6h 4bfdbed89520 512](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U06_DLSR_8_K6_H_4bfdbed89520_512_cbff481702.jpg&w=96&q=75)![t02em6f031p u0afx7180sj 4e05006047b5 512](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U0_AFX_7180_SJ_4e05006047b5_512_d901e206d9.png&w=96&q=75)![t02em6f031p u043r4lcrfs e0746edacb29 512](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U043_R4_LCRFS_e0746edacb29_512_078317ee8d.jpg&w=96&q=75)[Francisco Neves](/authors/author-francisco-neves), [San Tran](/authors/san-tran), [Jia Xu](/authors/jia-xu), [Zach Naimon](/authors/zach-naimon), [Ilya Andreev](/authors/ilya-andreev), [Hanzi Jiang](/authors/hanzi-jiang) and [Kevin Zhang](/authors/kevin-zhang)Oct 5, 2026 · 22 minutes read
> TL;DR
> Executable UDFs are GA on ClickHouse Cloud across AWS, GCP, and Azure, with a Native runtime for compiled Rust/Go/C\+\+/JavaScript, network access, memory limits, a `deterministic` flag, Cloud API \+ Terraform support, and per\-query UDF metrics in 26\.6\+. Below, we use them to count and price LLM tokens and grade completions inside ClickHouse.

*Note: companion code here \- *[*github.com/ClickHouse/llm\-token\-udf*](https://github.com/ClickHouse/llm-token-udf)*.*

Four months ago we put executable UDFs into public beta on ClickHouse Cloud: write a function in Python, upload it as a zip, call it from SQL like any built\-in. The requests we got during the beta were pretty consistent. People wanted to upload compiled code rather than Python, wanted UDFs on Azure, wanted network access without opening a support ticket, and wanted to see what their UDFs were doing to the cluster.

Today, we are happy to announce that **executable UDFs are generally available on ClickHouse Cloud** on AWS, GCP, and Azure. Since the beta announcement, we have added:

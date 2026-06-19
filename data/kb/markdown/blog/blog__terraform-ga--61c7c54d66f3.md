# Terraform \& OpenAPI for ClickPipes is now Generally Available


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Terraform \& OpenAPI for ClickPipes is now Generally Available

![](/_next/image?url=%2Fuploads%2FMarta_Paes_Moreira_no_background_9853166ee2.png&w=96&q=75)[Marta Paes](/authors/marta-paes)Apr 20, 2026 · 8 minutes read
/\* Expandable metric boxes \*/
details.metric\-box {
 background: \#2B2B2B;
 border\-radius: 12px;
 margin: 28px 0;
 padding: 0;
 color: \#E2E8F0;
 box\-shadow: 0 0 0 1px rgba(255,255,255,0\.05\), 0 4px 12px rgba(0,0,0,0\.2\);
 border\-left: 5px solid rgba(255, 255, 255, 0\.1\);
}

/\* Summary bar \*/
details.metric\-box summary {
 cursor: pointer;
 list\-style: none;
 padding: 16px 24px;
 font\-weight: 600;
 font\-size: 14px;
 letter\-spacing: 0\.3px;
 text\-transform: uppercase;
 color: \#E2E8F0;
 position: relative;
 transition: background 0\.2s;
}

details.metric\-box summary:hover {
 background: rgba(255,255,255,0\.05\);
}

/\* Rotating arrow \*/
details.metric\-box summary::after {
 content: \&quot;▶\&quot;;
 position: absolute;
 right: 20px;
 transition: transform 0\.2s;
 font\-size: 12px;
 color: \#A0AEC0;
}

details.metric\-box\[open] summary::after {
 transform: rotate(90deg);
}

/\* Inner content \*/
details.metric\-box p {
 padding: 0 24px 12px 24px;
 margin: 0;
 font\-size: 15px;
 line\-height: 1\.55;
}

details.metric\-box .notes {
 margin: 12px 24px 16px 24px;
 padding: 10px 12px;
 background: rgba(255,255,255,0\.05\);
 border\-radius: 6px;
 font\-size: 14px;
}

details.metric\-box a { color: inherit; text\-decoration: none; }
details.metric\-box code {
 background: rgba(255,255,255,0\.06\);
 padding: 2px 5px;
 border\-radius: 4px;
 font\-family: ui\-monospace, SFMono\-Regular, monospace;
}

/\* Metrics table inside expandable boxes \*/
details.metric\-box.metrics .metric\-row {
 display: flex;
 padding: 6px 0;
 border\-bottom: 1px solid rgba(255,255,255,0\.05\);
 font\-size: 14px;
 margin: 0 24px;
}
details.metric\-box.metrics .metric\-row:last\-child { border\-bottom: none; }

details.metric\-box.metrics .metric\-label {
 width: 180px;
 text\-align: right;
 padding\-right: 16px;
 color: \#A0AEC0;
 flex\-shrink: 0;
}
details.metric\-box.metrics .metric\-value { flex: 1; }


> **TL;DR**  
> Provision and manage ClickPipes resources “as code” using Terraform and OpenAPI, now with full connector coverage and improved usability.


  

ClickOps (*i.e.* clicking buttons in a user interface) is useful for onboarding into a new product, but as you progress towards production, it’s common to switch to an approach that allows managing resources in a more automated and version\-controlled way: “infrastructure\-as\-code”.


As we build out ClickHouse Cloud, one of our goals is to make it API\-first: every action you can perform through the user interface should also be available via a programmatic interface that can blend into your existing deployment workflows (and be leveraged by agents 🤖). ClickPipes, ClickHouse Cloud’s managed data ingestion platform, is no exception.

### Get started today

Sign up for ClickHouse Cloud today to try out seamless data ingestion with ClickPipes![Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-475-get-started-today-sign-up&utm_blogctaid=475)Today, we’re announcing the general availability of ClickPipes resources in Terraform and endpoints in OpenAPI! Although we [introduced beta support for these interfaces last year](https://clickhouse.com/blog/evolution-of-clickpipes), there were some feature and usability gaps that prevented *all* users from managing their ClickPipes as code. Most notably, we were missing full connector coverage: well, now you can also create CDC ClickPipes (Postgres, MySQL, MongoDB) as code, too!


## **What is supported?** [\#](/blog/terraform-ga#what_is_supported)


In addition to support for CDC ClickPipes, we’ve worked on adding new ClickPipes connectors and features to both interfaces on launch (*e.g.* BigQuery and Azure Blob Storage connectors, S3 and GCS unordered mode), as well as backfilling important gaps like support for creating and managing reverse private endpoints. This means that you’re unlikely to find something in the ClickPipes UI that isn’t exposed via OpenAPI or Terraform. Unless that something is SSH tunneling, but we’re [working on it](#bookmark=id.uz6whn8nwd37)!


Every operation now cleanly maps to a resource in the [ClickHouse Terraform provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs) or an [OpenAPI endpoint](https://clickhouse.com/docs/cloud/manage/api/swagger):




| Action | Terraform | OpenAPI |
| --- | --- | --- |
| List | `terraform state list` | `GET /clickpipes` |
| Create | Add resource \+ `terraform apply` | `POST /clickpipes` |
| Read | `terraform show / refresh` | `GET /clickpipes/{id}` |
| Update | Change config \+ `terraform apply` | `PATCH /clickpipes/{id}` |
| Stop | `stopped = true` \+ `terraform apply` | `PATCH /clickpipes/{id}/state {"action": "stop"}` |
| Resume | `stopped = false` \+ terraform apply | `PATCH /clickpipes/{id}/state {"action": "start"}` |
| Update settings | Update `settings` block \+ `terraform apply` | `PUT /clickpipes/{id}/settings` |
| Scale | Update `scaling` block \+ `terraform apply` | `PATCH /clickpipes/{id}/scaling` |
| Trigger resync | `trigger_resync = true` \+ `terraform apply` | `PATCH /clickpipes/{id}` |
| Delete | `terraform destroy` | `DELETE /clickpipes/{id}` |


If you're provisioning a ClickPipe from scratch, start with [*How to: configure a new ClickPipe*](#bookmark=id.qa1u83ivk9g1). If you already have pipes running and want to bring them under version control, check [*How to: import existing ClickPipes*](#bookmark=id.1fs3jt8zn01g).


## How to: configure a new ClickPipe [\#](/blog/terraform-ga#how-to-configure-a-new-clickpipe)


#### Create a Cloud API key [\#](/blog/terraform-ga#create-a-cloud-api-key)


**1\.** The ClickHouse Terraform provider uses the [Cloud API](https://clickhouse.com/docs/cloud/manage/cloud-api) to interact with your ClickHouse Cloud service, so you’ll need a valid API key for authentication. If you’re new to the provider, the first step is to create a new API key. Navigate to **Organization \> API keys \> New API key**, and note (or download) the provided **Key ID** and a **Key Secret** pair.


![](/uploads/terraform_clickpipes_apr2026_image2_c51c42d023.png)
**2\.** Next, configure the provider. To keep credentials out of source control, we recommend using [Terraform variables](https://developer.hashicorp.com/terraform/language/values/variables) and a `terraform.tfvars` file that you can add to `.gitignore`:


**variables.tf**



```

```
1variable "organization_id" {
2  description = "ClickHouse Cloud organization ID"
3  type        = string
4}
5
6variable "service_id" {
7  description = "ClickHouse Cloud service ID"
8  type        = string
9}
10
11variable "token_key" {
12  description = "ClickHouse Cloud API key ID"
13  type        = string
14  sensitive   = true
15}
16
17variable "token_secret" {
18  description = "ClickHouse Cloud API key secret"
19  type        = string
20  sensitive   = true
21}
22...
```

```

**terraform.tfvars**



```

```
1organization_id   = "" # your org ID from cloud.clickhouse.com
2service_id        = "" # target ClickHouse service ID
3token_key         = "" # API key ID
4token_secret      = "" # API key secret
5...
```

```

#### Configure a ClickPipes resource [\#](/blog/terraform-ga#configure-a-clickpipes-resource)


In this example, we’ll configure a resource for a [Postgres CDC ClickPipe](https://clickhouse.com/docs/integrations/clickpipes/postgres) to continuously ingest changes from a Postgres database into ClickHouse in near real time. Remember: before creating a CDC ClickPipe, make sure to follow the [configuration guides](https://clickhouse.com/docs/integrations/clickpipes/postgres#prerequisites) for your data source, which guide you through enabling replication upstream.


**1\.** Once you’re ready to create a ClickPipe, add a new [`clickhouse_clickpipe` resource](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs/resources/clickpipe) to your Terraform configuration using `postgres` as the source attribute. Below is a basic configuration example that creates a single ClickPipe to sync a single Postgres table (`public.firenibble`) and propagate any new changes in the `source_table` (*i.e.* inserts, updates, deletes) to the `target_table` in ClickHouse Cloud using `cdc`.


**main.tf**



```

```
1terraform {
2 required_providers {
3   clickhouse = {
4     source  = "ClickHouse/clickhouse"
5     version = ">= 3.14.0"
6   }
7 }
8}
9
10provider "clickhouse" {
11 organization_id = var.organization_id
12 token_key       = var.token_key
13 token_secret    = var.token_secret
14}
15
16resource "clickhouse_clickpipe" "pg_pipe" {
17 name       = "tf-postgres-clickpipe"
18 service_id = var.service_id
19
20 source = {
21   postgres = {
22     host     = var.postgres_host
23     port     = 5432
24     database = var.postgres_database
25
26     credentials = {
27       username = var.postgres_user
28       password = var.postgres_password
29     }
30
31     settings = {
32       replication_mode = "cdc"
33     }
34
35     table_mappings = [
36       {
37         source_schema_name = "public"
38         source_table       = "firenibble"
39         target_table       = "public_firenibble"
40       }
41     ]
42   }
43 }
44
45 destination = {
46   database = "default"
47 }
48}
```

```

**2\.** Now that you’ve passed your Cloud API credentials and resource configuration to Terraform, you’re ready to deploy. Run `terraform init` to install the ClickHouse provider, then `terraform apply` to provision the pipe. Terraform will output a plan and prompt you to confirm the planned changes before deploying:



```

```
1terraform apply
2
3...
4Plan: 1 to add, 0 to change, 0 to destroy.
5
6Do you want to perform these actions?
7  Terraform will perform the actions described above.
8  Only 'yes' will be accepted to approve.
9
10  Enter a value: yes
11
12clickhouse_clickpipe.pg_pipe: Creating...
13clickhouse_clickpipe.pg_pipe: Still creating... [00m10s elapsed]
14clickhouse_clickpipe.pg_pipe: Creation complete after 11s [id=10128f88-100c-4830-b480-e242fa89570f]
```

```

All done! Your first CDC ClickPipe created programmatically is now up and running. Head over to the ClickHouse Cloud console and double\-check it is indeed there (under **Data sources \> ClickPipes**), churning through data ingestion.


![](/uploads/terraform_clickpipes_apr2026_image1_1ac36961ee.png)
You can find examples on how to configure ClickPipes in Terraform for different pipe types, ingestion modes and network setups in the [provider repo](#bookmark=id.1fs3jt8zn01g).


## **How to: import existing ClickPipes** [\#](/blog/terraform-ga#how-to-import-existing-clickpipes)


*The following steps were tested with HashiCorp Terraform v1\.5\+. The import workflow should be broadly compatible with alternative implementations (e.g. OpenTofu), but minimum versions and base methods might differ.*


If you already have a project that uses the ClickHouse Terraform provider, you can import existing ClickPipes into your Terraform state and start managing them as code, instead of manually configuring them.


**1\.** Use the Cloud API to retrieve existing ClickPipes for the organization and service in scope:



```
curl -s \
  "https://api.clickhouse.cloud/v1/organizations/$ORG_ID/services/$SERVICE_ID/clickpipes" \
  -u "$KEY_ID:$KEY_SECRET" | jq -r '.result[] | "\(.id)\t\(.name)"'

1667855d-1646-4693-8cac-60e1c386ccb1    existing_pg_pipe
2e4c3974-025e-47a0-861b-4c200b6c0249    existing_mysql_pipe
76a42195-ef25-40fc-ae3d-31733d377f77    existing_mongo_pipe

```

**2\.** Edit your configuration file to include import blocks for any ClickPipes you want to import into Terraform:



```

```
1...
2import {
3  to = clickhouse_clickpipe.existing_pg_pipe
4  id = "<service_id>:1667855d-1646-4693-8cac-60e1c386ccb1"
5}
6...
```

```

**3\.** Generate the Terraform resource configuration from the existing resources:



```
terraform plan -generate-config-out=generated.tf

```

Review `generated.tf` and fill in any sensitive fields (like credentials) that Terraform can't retrieve from state.



```

```
1# __generated__ by Terraform
2# Please review these resources and move them into your main configuration files.
3
4# __generated__ by Terraform
5resource "clickhouse_clickpipe" "pg_pipe" {
6…
7credentials    = {
8username = var.postgres_user
9password = var.postgres_password
10}
11…}
```

```

**4\.** Run `terraform plan` to verify there are no unexpected diffs, then `terraform apply` to finalize.


*Note: For Postgres CDC ClickPipes, you’ll need to set `stopped = true` in the resource config before running `terraform apply`. Terraform will pause the pipe and write credentials to state in one pass. Once complete, set `stopped = false` and apply again to resume. This is a [known limitation](https://github.com/ClickHouse/terraform-provider-clickhouse/issues/497).*


## What’s next? [\#](/blog/terraform-ga#whats-next)


ClickPipes resources are available in stable releases of the ClickHouse Terraform provider from [v3\.14\.0](https://github.com/ClickHouse/terraform-provider-clickhouse/releases/tag/v3.14.0), and OpenAPI endpoints have also graduated out of beta ([spec](https://clickhouse.com/docs/cloud/manage/api/swagger)). As ClickPipes evolves, we’ll continue treating Terraform and OpenAPI as first\-class interfaces that are part of our “definition of done”. We’re actively working on some complex usability limitations like the one mentioned above, as well as the much\-requested support for **SSH tunneling** configuration!


If you have feedback or run into any snags while configuring and managing ClickPipes using Terraform and OpenAPI, reach out to our team. Soon, we’ll also make ClickPipes available in the [recently released ClickHouse CLI](https://clickhouse.com/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud); more on this in a few weeks!

### Try ClickPipes today

Ready to eliminate your ETL complexity and reduce your data movement costs? Try ClickPipes today and experience a fully managed, native integration experience with ClickHouse Cloud — the world’s fastest analytics database.[Try ClickPipes](https://clickhouse.com/cloud/clickpipes?loc=blog-cta-476-try-clickpipes-today-try-clickpipes&utm_blogctaid=476)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

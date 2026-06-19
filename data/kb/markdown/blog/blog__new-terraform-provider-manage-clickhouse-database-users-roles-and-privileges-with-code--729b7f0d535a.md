# New Terraform provider: Manage ClickHouse database users, roles, and privileges with code


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# New Terraform provider: Manage ClickHouse database users, roles, and privileges with code

![](/_next/image?url=%2Fuploads%2Fryan_sickles_e15dde8293.jpeg&w=96&q=75)Ryan SicklesJun 20, 2025 · 8 minutes readWe’re excited to announce the general availability of our new Terraform provider, [clickhousedbops](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest), to help customers manage database users, roles, and grant roles and privileges. This new provider supports ClickHouse instances running on both [ClickHouse Cloud](https://clickhouse.com/) or self hosted.


We have already seen adoption from many ClickHouse Cloud customers for using Terraform to programmatically automate the configuration and management of their ClickHouse services. These customers see major ease of use benefits using Terraform to manage the state of all their ClickHouse services across different environments. This Terraform functionality has been supported with our existing [Clickhouse Terraform provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest) for managing and deploying services, private endpoints, and Transparent Data Encryption keys for services. Now customers can extend their Terraform use cases with our [clickhousedbops](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest) provider. After defining a direct connection to their clickhouse instance, customers can build databases and then define users and roles with privilege grants on that database’s tables or columns.


![Terraform.png](/uploads/Terraform_5c3b11375a.png)
## Getting started with the Terraform provider [\#](/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code#getting-started-with-the-terraform-provider)


### Step 1: Provisioning a ClickHouse Cloud Service [\#](/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code#step-1-provisioning-a-clickhouse-cloud-service)


Imagine you are an engineering team lead and you are interested in building a new ClickHouse database so your team can store and analyze your business unit’s email and phone log data. You already manage all your other infrastructure programmatically using Terraform and so you are interested in doing the same with ClickHouse.


You want to first login to your ClickHouse Cloud account. Then once you login, you can create an [API token and secret](https://clickhouse.com/docs/cloud/manage/openapi) from your ClickHouse cloud organization in order to allow terraform to connect.


Now you want to define a new ClickHouse Cloud service called “Log Analytics” using Terraform. You can create a main.tf file to configure the [Clickhouse provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs#example-usage). You want to define your new ClickHouse Cloud [service resource](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs/resources/service#example-usage) in the AWS us\-east\-1 region named “Log Analytics” in the same file.



> Note: We do not recommend storing credentials in your terraform files, see docs [here](https://developer.hashicorp.com/terraform/language/values/variables) for help creating a separate variables file.


Main.tf file



```

```
terraform {
  required_providers {
    clickhouse = {
      source  = "ClickHouse/clickhouse"
    }
   }
}

locals {
  # Please don't do this :)
  password = "test"
}

# Configuration-based authentication, replace with your own values
provider "clickhouse" {
  organization_id = ""
  token_key       = ""
  token_secret    = ""
}

resource "clickhouse_service" "service" {
  name           = "Log Analytics"
  cloud_provider = "aws"
  region         = "us-east-1"
  idle_scaling   = true
  min_replica_memory_gb  = 8
  max_replica_memory_gb  = 16
  num_replicas = 3
  idle_timeout_minutes = 5

  # for this example this service will be open to all internet connections
  ip_access = [
    {
      source      = "0.0.0.0/0"
      description = "Test IP"
    }
  ]
  password_hash = sha256(local.password)
}
```

```

### Step 2: Managing users, roles, and privileges [\#](/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code#step-2-managing-users-roles-and-privileges)


Now that you have your new service defined you want to add your team to a new database called “logs” in the new “Log Analytics” service you created. The following are the requirements for your team to define in Terraform:


1. Your team has 3 users \- Ryan, Jill, and Carol.
2. Ryan is responsible for running analytic queries only on the email logs table in the database, but does not need read access to any other tables.
3. Jill and Carol are responsible for running analytic queries only on the phone logs table in the database, but do not need read access to any other tables.


In order to satisfy these requirements, you decide to use Terraform and the new [Clickhousedbops provider](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest/docs#example-usage) to configure these users, roles, and grant privileges. First you add the terraform provider to the required\_providers block at the top of the same main.tf terraform file.



```

```
terraform {
  required_providers {
    clickhouse = {
      source  = "ClickHouse/clickhouse"
    }
    clickhousedbops = {
      source  = "ClickHouse/clickhousedbops"
    }
   }
}
...
```

```

Next, you configure the provider and the resources for [database](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest/docs/resources/database), [users](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest/docs/resources/user), [roles](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest/docs/resources/role), and [grant privileges](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest/docs/resources/grant_privilege) according to the requirements. These resources are appended at the end of the same main.tf file.



```

```
provider "clickhousedbops" {
  protocol = "nativesecure"      
  host = clickhouse_service.service.endpoints.nativesecure.host
  port = clickhouse_service.service.endpoints.nativesecure.port
  auth_config = {
    strategy = "password"
    username = "default"
    password = local.password
  }
}
resource "clickhousedbops_database" "logs" {
  name = "logs"
  comment = "Database for logs"
}

resource "clickhousedbops_user" "ryan" {
  name = "ryan"
  # You'll want to generate the password and feed it here instead of hardcoding.
  password_sha256_hash_wo = sha256("test1")
  password_sha256_hash_wo_version = 1
}


resource "clickhousedbops_user" "jill" {
  name = "jill"
  # You'll want to generate the password and feed it here instead of hardcoding.
  password_sha256_hash_wo = sha256("test2")
  password_sha256_hash_wo_version = 1
}

resource "clickhousedbops_user" "carol" {
  name = "carol"
  # You'll want to generate the password and feed it here instead of hardcoding.
  password_sha256_hash_wo = sha256("test3")
  password_sha256_hash_wo_version = 1
}

resource "clickhousedbops_role" "reader_email_logs" {
  name = "reader_email_logs"
}

resource "clickhousedbops_role" "reader_phone_logs" {
  name = "reader_phone_logs"
}

resource "clickhousedbops_grant_privilege" "grant_select_on_email_logs_to_user" {
  privilege_name    = "SELECT"
  database_name     = "logs"
  table_name        = "email_logs"
  grantee_role_name = clickhousedbops_role.reader_email_logs.name
  grant_option      = true
}

resource "clickhousedbops_grant_privilege" "grant_select_on_phone_logs_to_user" {
  privilege_name    = "SELECT"
  database_name     = "logs"
  table_name        = "phone_logs"
  grantee_role_name = clickhousedbops_role.reader_phone_logs.name
  grant_option      = true
}

resource "clickhousedbops_grant_role" "role_to_user_ryan" {
  role_name         = clickhousedbops_role.reader_email_logs.name
  grantee_user_name = clickhousedbops_user.ryan.name
}

resource "clickhousedbops_grant_role" "role_to_user_jill" {
  role_name         = clickhousedbops_role.reader_phone_logs.name
  grantee_user_name = clickhousedbops_user.jill.name
}

resource "clickhousedbops_grant_role" "role_to_user_carol" {
  role_name         = clickhousedbops_role.reader_phone_logs.name
  grantee_user_name = clickhousedbops_user.carol.name
}
```

```

### Step 3: Deploying to ClickHouse Cloud [\#](/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code#step-3-deploying-to-clickhouse-cloud)


Finally, in order to deploy your terraform configuration into your ClickHouse Cloud organization, run “terraform init” to download the providers and then “terraform apply“. In a few minutes you will have the clickhouse service and the database resources created.



```

```
% terraform apply
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # clickhouse_service.service will be created
  + resource "clickhouse_service" "service" {
      + backup_configuration        = (known after apply)
      + cloud_provider              = "aws"
      + endpoints                   = (known after apply)
      + iam_role                    = (known after apply)
      + id                          = (known after apply)
      + idle_scaling                = true
      + idle_timeout_minutes        = 5
...
clickhouse_service.service: Creating...
clickhouse_service.service: Still creating... [10s elapsed]
...
clickhouse_service.service: Creation complete after 6m36s 
...
clickhousedbops_role.reader_email_logs: Creating...
clickhousedbops_role.reader_phone_logs: Creating...
clickhousedbops_database.logs: Creating...
clickhousedbops_user.ryan: Creating...
clickhousedbops_user.carol: Creating...
clickhousedbops_user.jill: Creating...
...
Apply complete! Resources: 12 added, 0 changed, 0 destroyed.
```

```

After this you can use the [ClickHouse Client CLI](https://clickhouse.com/docs/interfaces/cli) to login as the default user and create two tables “email\_logs” and “phone\_logs” in this logs database, load the intended data into each, and then confirm that the correct users were created and that each user has the correct role and database privileges.


Tip: connect to the database and run the SQL command “SELECT \* FROM system.role\_grants” to see all database users and roles for each.


Congratulations! You have successfully used both of the officially supported ClickHouse Terraform providers for configuring your ClickHouse Cloud service, database, users, roles, and database privileges.


### Managing self\-hosted ClickHouse with Terraform [\#](/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code#managing-self-hosted-clickhouse-with-terraform)


Now let’s say that you are not a ClickHouse Cloud customer (free trial offered [here!](https://clickhouse.com/)). This new clickhousedbops provider also has support for our customers who want to use Terraform for managing their self\-hosted ClickHouse database users, roles, and grant privileges in their own self hosted cloud or on\-prem environment.


To support these open source ClickHouse deployments, if users have multiple replicas then a “cluster\_name” variable (database resource [example](https://registry.terraform.io/providers/ClickHouse/clickhousedbops/latest/docs/resources/role#optional)) can be defined in each of the clickhousedbops resource definitions. This will create the resources in all of the replicas in that cluster. If omitted, that resource will be created on the replica hit by the query. We recommend that this should always be set when hitting a cluster with more than one replica.



> Note: This field must be left null when using a ClickHouse Cloud cluster. When using a self hosted ClickHouse instance, this field should only be set for non database resources when there is more than one replica and you are not using 'replicated' storage for [user\_directory](https://clickhouse.com/docs/operations/server-configuration-parameters/settings#user_directories).


You would define your clickhousedbops database resource as such:



```

```
resource "clickhousedbops_database" "logs" {
  name = "logs"
  cluster_name = "cluster1"
  comment = "Database for logs"
}
```

```

## Try it out and give us feedback [\#](/blog/new-terraform-provider-manage-clickhouse-database-users-roles-and-privileges-with-code#try-it-out-and-give-us-feedback)


We hope our new Terraform support makes managing ClickHouse infrastructure easier and more reliable. We encourage users who are interested to try out our terraform providers and give us feedback directly through opening an issue in either GitHub repository \- [ClickHouse](https://github.com/ClickHouse/terraform-provider-clickhouse) or [Clickhousedops](https://github.com/ClickHouse/terraform-provider-clickhousedbops).

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

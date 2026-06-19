# Using ClickHouse Cloud and Terraform for CI/CD


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Using ClickHouse Cloud and Terraform for CI/CD

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Jul 13, 2023 · 16 minutes read## Introduction [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#introduction)


At ClickHouse, we aspire to an API\-first approach to development for ClickHouse Cloud. Every action that a user can perform through the user interface should also be possible via a scripting language and thus available for other systems to leverage. This means our recently released Cloud API is also a product with a contract (via swagger) on how it will behave and on which our users can depend. While our existing users much anticipated the release of this API to address requirements such as automated provisioning and de\-provisioning, scheduled scaling, and flexible configuration management, it also allowed us to begin integrating with tooling: starting with Terraform.


In this blog post, we explore our new [Terraform provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs) and how this can be used to address a common requirement: CI/CD for systems needing to test against a ClickHouse instance. For our example, we look at how we migrated our go client tests away from a monolithic ClickHouse Cloud service to use Terraform and provision ephemeral services for the period of a test only. This not only allows us to reduce costs but also isolates our tests across clients and invocations. We hope others can benefit from this pattern and bring cost savings and simplicity to their test infrastructure!


## Terraform [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#terraform)


Terraform is an open\-source infrastructure\-as\-code software tool created by HashiCorp, which allows users to define infrastructure using a declarative configuration language known as HashiCorp Configuration Language (HCL) or, optionally, JSON.



> Infrastructure as code is the process of managing and provisioning computing resources through machine\-readable definition files rather than physical hardware configuration or interactive configuration tools. This approach has achieved almost universal acceptance as the means of managing cloud computing resources. Terraform has gained a wide user base and broad adoption as a tool that implements this process declaratively.


In order to integrate with Terraform and allow users to provision ClickHouse Cloud services, a [provider plugin](https://developer.hashicorp.com/terraform/language/providers) must be implemented and ideally made available via the [Hashicorp registry](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs).


## Authentication [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#authentication)


Since the ClickHouse provider relies on the ClickHouse API, an authentication key is required to provision and manage services. Users can create a token, along with a secret, via the ClickHouse Cloud interface. This simple process is shown below:


[![](/uploads/create_api_key_0f1c1acf18.gif)](/uploads/create_api_key_0f1c1acf18.gif)


Users should also record their organization id as shown.


## Using the provider [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#using-the-provider)


Once a token and secret have been created, users can create a `.tf` file and declare the usage of the provider. Wanting to avoid placing credentials in the main file, the `token_key`, `token_secret` and `organization_id` are replaced with [Terraform variables](https://developer.hashicorp.com/terraform/language/values/variables). These can in turn be specified in a `secret.tfvars` file, which should not be submitted to source control.


**main.tf**



```
terraform {
 required_providers {
   clickhouse = {
     source = "ClickHouse/clickhouse"
     version = "0.0.2"
   }
 }
}

variable "organization_id" {
  type = string
}

variable "token_key" {
  type = string
}

variable "token_secret" {
  type = string
}

provider clickhouse {
  environment 	= "production"
  organization_id = var.organization_id
  token_key   	= var.token_key
  token_secret	= var.token_secret
}

```

**secret.tfvars**



```
token_key = "<token_key>"
token_secret = "<token_secret>"
organization_id = "<organization_id>"

```

Assuming users have [installed Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli), the provider can be installed with a `terraform init`.



```
terraform init

Initializing the backend...

Initializing provider plugins...
- Finding clickhouse/clickhouse versions matching "0.0.2"...
- Installing clickhouse/clickhouse v0.0.2...
- Installed clickhouse/clickhouse v0.0.2 (self-signed, key ID D7089EE5C6A92ED1)

Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://www.terraform.io/docs/cli/plugins/signing.html

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

```

With our provider configured, we can deploy a ClickHouse Cloud service by adding a few lines of HCL to our above file.



```
variable "service_password" {
  type = string
}

resource "clickhouse_service" "service" {
  name       	= "example-service"
  cloud_provider = "aws"
  region     	= "us-east-2"
  tier       	= "development"
  idle_scaling   = true
  password  = var.service_password
  ip_access = [
	{
    	source  	= "0.0.0.0/0"
    	description = "Anywhere"
	}
  ]
}

output "CLICKHOUSE_HOST" {
  value = clickhouse_service.service.endpoints.0.host
}

```

Here we specify our desired cloud provider, region, and tier. The tier can either be development or production. A development tier represents the entry offering in ClickHouse Cloud, appropriate for smaller workloads and starter projects. For the above example, we enable idling, such that our service doesn’t consume costs if unused.



> Enabling idle\_scaling is the only valid value for development tier instances, i.e., it cannot be disabled. Future versions of the provider will validate this setting.


We must also specify a service name and list of IP addresses from which this service will be accessible (anywhere in our example), as well as a password for the service. We again abstract this as a variable to our secrets file.
Our output declaration captures the endpoint of our service in a `CLICKHOUSE_HOST` output variable, ensuring obtaining the connection details once the service is ready is simple. The full example main.tf file can be found [here](https://pastila.nl/?025ef1fd/d369943908f299267b8b8d488c230380).


Provisioning this service requires only a single command, `terraform apply`, with the option `-var-file` to pass our secrets.



```
terraform apply -var-file=secrets.tfvars

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

# clickhouse_service.service will be created
  + resource "clickhouse_service" "service" {
  	+ cloud_provider = "aws"
  	+ endpoints  	= (known after apply)
  	+ id         	= (known after apply)
  	+ idle_scaling   = true
  	+ ip_access  	= [
      	+ {
          	+ description = "Anywhere"
          	+ source  	= "0.0.0.0/0"
        	},
    	]
  	+ last_updated   = (known after apply)
  	+ name       	= "example-service"
  	+ password   	= (sensitive value)
  	+ region     	= "us-east-2"
  	+ tier       	= "development"
	}

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

clickhouse_service.service: Creating...
clickhouse_service.service: Still creating... [10s elapsed]
clickhouse_service.service: Still creating... [20s elapsed]
clickhouse_service.service: Still creating... [30s elapsed]
clickhouse_service.service: Still creating... [40s elapsed]
clickhouse_service.service: Still creating... [50s elapsed]
clickhouse_service.service: Still creating... [1m0s elapsed]
clickhouse_service.service: Still creating... [1m10s elapsed]
clickhouse_service.service: Creation complete after 1m12s [id=fd72178b-931e-4571-a0d8-6fb1302cfd4f]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

CLICKHOUSE_HOST = "gx75qb62bi.us-east-2.aws.clickhouse.cloud"

```

As shown, Terraform constructs a plan based on the definition before provisioning the service. The hostname assigned to our service is also printed, thanks to our earlier output configuration. `terraform destroy` can be used to delete the above service.



> In order for Terraform to apply changes to a set of resources, it requires a means of obtaining its current state, including the resources that are provisioned and their configuration. This is described within a "state", which contains a full description of the resources. This allows changes to be made to resources over time, with each command able to determine the appropriate actions to take. In our simple case, we hold this state locally in the folder in which the above command was run. State management, however, is a [far more involved topic](https://developer.hashicorp.com/terraform/language/state) with a number of means of maintaining it appropriate for real\-world environments, including using [HashiCorp's cloud offering](https://developer.hashicorp.com/terraform/language/state/remote). This is particularly relevant when more than an individual, or system, is expected to operate on the state at any given time and concurrency control is required.


## CI/CD \- a practical example [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#cicd---a-practical-example)


### Adding Terraform to Github actions [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#adding-terraform-to-github-actions)


Testing against ClickHouse Cloud is essential to providing high\-quality clients to our users. Until the availability of the Terraform provider, our ClickHouse clients were tested against a single service in ClickHouse Cloud with tests orchestrated by [Github actions](https://github.com/features/actions). This instance was shared amongst our clients, each creating their databases and tables whenever a PR or commit was made against the repository. While this was sufficient, it suffered from some limitations:


- **Central point of failure**. Any issues with this service, e.g., due to regional availability, would cause all tests to fail.
- **Conflicting resources**. While avoided by ensuring all resources, e.g., tables, followed a naming convention using the client name and timestamp, this had consequences (see below).
- **Resource Growth \& Test Complexity**. Ensuring tests could be run concurrently meant ensuring tables, databases, and users used by a specific test were unique to avoid conflicts \- this needed consistent boilerplate code across clients. When combined with clients needing a [significant number of tests](https://github.com/ClickHouse/clickhouse-go/tree/main/tests) to ensure feature coverage in ClickHouse, this meant the creation of potentially hundreds of tables. Further testing orchestration was needed to ensure each client removed these on completion to avoid table explosion \- maybe unsurprisingly, ClickHouse isn’t designed for 10k tables!
- **Cost inefficiency** \- While the query load of the above testing is not substantial, our service was effectively always active and subject to potentially high zookeeper load due to a significant number of concurrent DDL operations. This meant we used a production service. Furthermore, our tests needed to be robust to idling in the event the service was able to shut down.
- **Observability complexity** \- With many clients, and multiple tests running, debugging test failures using server logs became more complex.


The Terraform provider promised to provide a simple solution to these problems, with each client simply creating a service at the start of testing, running its test suite, and destroying the service on completion. Our test services thus become ephemeral.


![github_actions_architectures.png](/uploads/github_actions_architectures_80aab4421c.png)
This approach has a number of advantages:


- **Test isolation**\- While the tests are still vulnerable to the unavailability of ClickHouse Cloud in a region, they have become robust to service issues, e.g., a client triggering a ClickHouse bug causing a service\-wide issue or a client test making a service\-wide configuration change. The tests for our clients are immediately isolated.
- **No resource growth and simpler tests** \- Our services only exist for the lifetime of the test run. Client developers now only need to consider potential conflicts of resources as a result of their own test concurrency. They can also make configuration changes to entire services, potentially simplifying tests.
- **Cost inefficiency** \- Smaller (dev) services can be created and exist for minutes (\<10 in most cases) only, minimizing cost.
- **Simple Observability** \- While we destroy services on completion of the test, the service id is logged. This can be used to retrieve server logs in our Observability system if needed.


### Existing workflow [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#existing-workflow)


For our first client, we selected [Clickhouse Go](https://github.com/ClickHouse/clickhouse-go) with simple Github [actions](https://github.com/ClickHouse/clickhouse-go/blob/f476287762b28be1de5f7996a775c882c1aa0dd5/.github/workflows/run-tests.yml#L1) and a lot of the test complexity encapsulated in the code’s testing suite.



> Github actions provide a simple workflow\-based CI/CD platform. With tight integration into Github, users simply create workflows declaratively in yml files beneath a `.github/workflow` directory, with each containing jobs to run. These jobs, which consist of steps, can be configured to [run on schedules or for specific events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows), e.g., PRs.


The existing Cloud tests consisted of a job configured to run against the monolithic service described above. The test suite already supported specifying a ClickHouse instance on which tests should be executed via the environment variables `CLICKHOUSE_HOST` and `CLICKHOUSE_PASSWORD`. These are populated through Github secrets. This also requires the environment variable `CLICKHOUSE_USE_DOCKER` to be set to false to disable existing docker\-based testing.


Other than these specific changes, the cloud tests are similar to the docker\-based single node testing \- using a matrix to test the client against different go versions and steps to check out the code and install go prior to the tests being run.



```
integration-tests-cloud:
  runs-on: ubuntu-latest
  strategy:
	max-parallel: 1
	fail-fast: true
	matrix:
  	go:
    	- "1.19"
    	- "1.20"
  steps:
	- uses: actions/checkout@main

	- name: Install Go ${{ matrix.go }}
  	uses: actions/setup-go@v2.1.5
  	with:
    	stable: false
    	go-version: ${{ matrix.go }}

	- name: Run tests
  	env:
    	CLICKHOUSE_HOST: ${{ secrets.INTEGRATIONS_TEAM_TESTS_CLOUD_HOST }}
    	CLICKHOUSE_PASSWORD: ${{ secrets.INTEGRATIONS_TEAM_TESTS_CLOUD_PASSWORD }}
    	CLICKHOUSE_USE_DOCKER: false
    	CLICKHOUSE_USE_SSL: true
  	run: |
    	CLICKHOUSE_DIAL_TIMEOUT=20 CLICKHOUSE_TEST_TIMEOUT=600s CLICKHOUSE_QUORUM_INSERT=3 make test

```

### New workflow [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#new-workflow)


Prior to migrating our workflow, we need a simple Terraform resource definition for the Clickhouse service. The following builds on the same example earlier, creating a service in the development tier, but introduces variables for the `organization_id`, `token_key`, `token_secret`, `service_name`, and `service_password`. We also output the service id to assist with later debugging and allow our service to be available from anywhere \- the ephemeral nature means the security risk is low. The following `main.tf` file is stored in the [root directory of the `clickhouse-go` client](https://github.com/ClickHouse/clickhouse-go/blob/main/main.tf).



```
terraform {
  required_providers {
	clickhouse = {
  	source = "ClickHouse/clickhouse"
  	version = "0.0.2"
	}
  }
}

variable "organization_id" {
  type = string
}

variable "token_key" {
  type = string
}

variable "token_secret" {
  type = string
}

variable "service_name" {
  type = string
}

variable "service_password" {
  type = string
}

provider clickhouse {
  environment 	= "production"
  organization_id = var.organization_id
  token_key   	= var.token_key
  token_secret	= var.token_secret
}

resource "clickhouse_service" "service" {
  name       	= var.service_name
  cloud_provider = "aws"
  region     	= "us-east-2"
  tier       	= "development"
  idle_scaling   = true
  password  = var.service_password

  ip_access = [
	{
    	source  	= "0.0.0.0/0"
    	description = "Anywhere"
	}
  ]
}

output "CLICKHOUSE_HOST" {
  value = clickhouse_service.service.endpoints.0.host
}

output "SERVICE_ID" {
  value = clickhouse_service.service.id
}

```

Terraform supports specifying variable values through environment variables prefixed with `TF_VAR_`. For example, to populate the organization id, we simply need to set `TF_VAR_organization_id`.


Similar to our previous workflow, the values of these environment variables can be populated with [Github encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets). In our case, we create these at an organizational level so they can be shared across clients and services created in the same ClickHouse Cloud account for simple administration.


![repo_secrets.png](/uploads/repo_secrets_7d10bed607.png)
Note: we don’t have a value here for the service name. As well as not being sensitive, we want to make sure these are unique for the test run, so we can identify the origin and creation time of the service.


To make Terraform available on the runner, we use the [`hashicorp/setup-terraform`](https://github.com/hashicorp/setup-terraform) action. This installs Terraform on the Github actions CLI runner and exposes its CLI so we can make calls like we would from a terminal.


Our final workflow is shown below:



```
integration-tests-cloud:
  runs-on: ubuntu-latest
  defaults:
	run:
  	shell: bash
  strategy:
	max-parallel: 1
	fail-fast: true
	matrix:
  	go:
    	- "1.19"
    	- "1.20"
  steps:
	- name: Check Out Code
  	uses: actions/checkout@v3

	- name: Setup Terraform
  	uses: hashicorp/setup-terraform@v2.0.3
  	with:
    	terraform_version: 1.3.4
    	terraform_wrapper: false

	- name: Terraform Init
  	id: init
  	run: terraform init

	- name: Terraform Validate
  	id: validate
  	run: terraform validate -no-color

	- name: Set Service Name
  	run: echo "TF_VAR_service_name=go_client_tests_$(date +'%Y_%m_%d_%H_%M_%S')" >> $GITHUB_ENV

	- name: Terraform Apply
  	id: apply
  	run: terraform apply -no-color -auto-approve
  	env:
    	TF_VAR_organization_id: ${{ secrets.INTEGRATIONS_TEAM_TESTS_ORGANIZATION_ID }}
    	TF_VAR_token_key:  ${{ secrets.INTEGRATIONS_TEAM_TESTS_TOKEN_KEY }}
    	TF_VAR_token_secret:  ${{ secrets.INTEGRATIONS_TEAM_TESTS_TOKEN_SECRET }}
    	TF_VAR_service_password: ${{ secrets.INTEGRATIONS_TEAM_TESTS_CLOUD_PASSWORD }}

	- name: Set Host
  	run: echo "CLICKHOUSE_HOST=$(terraform output -raw CLICKHOUSE_HOST)" >> $GITHUB_ENV

	- name: Service Id
  	run: terraform output -raw SERVICE_ID

	- name: Install Go ${{ matrix.go }}
  	uses: actions/setup-go@v2.1.5
  	with:
    	stable: false
    	go-version: ${{ matrix.go }}

	- name: Run tests
  	env:
    	CLICKHOUSE_PASSWORD: ${{ secrets.INTEGRATIONS_TEAM_TESTS_CLOUD_PASSWORD }}
    	CLICKHOUSE_USE_DOCKER: false
    	CLICKHOUSE_USE_SSL: true
  	run: |
    	CLICKHOUSE_DIAL_TIMEOUT=20 CLICKHOUSE_TEST_TIMEOUT=600s CLICKHOUSE_QUORUM_INSERT=2 make test

	- name: Cleanup
  	if: always()
  	run: terraform destroy -no-color -auto-approve
  	env:
    	TF_VAR_organization_id: ${{ secrets.INTEGRATIONS_TEAM_TESTS_ORGANIZATION_ID }}
    	TF_VAR_token_key:  ${{ secrets.INTEGRATIONS_TEAM_TESTS_TOKEN_KEY }}
    	TF_VAR_token_secret:  ${{ secrets.INTEGRATIONS_TEAM_TESTS_TOKEN_SECRET }}
    	TF_VAR_service_password: ${{ secrets.INTEGRATIONS_TEAM_TESTS_CLOUD_PASSWORD }}

```

In summary, this workflow consists of the following steps:


1. Checks out existing code to the runner via `uses: actions/checkout@v3`.
2. Installs terraform on the runner via `uses: hashicorp/setup-terraform@v2.0.3`.
3. Invokes `terraform init` to install the ClickHouse provider.
4. Validates the terraform resource definition file in the root of the checked\-out code via the`terraform validate` command.
5. Sets the environment variable `TF_VAR_service_name` to a date string prefixed with `go_client_tests_`. This ensures our services have unique names across clients and test runs and assists with debugging.
6. Run `terraform apply` to create a Cloud service with a specified password, with the organization id, token, and key passed via environment variables.
7. Sets the CLICKHOUSE\_HOST environment variable to the value of the output from the previous apply step.
8. Captures the service id for debugging purposes.
9. Installs go based on the current matrix version.
10. Run the tests \- note the `CLICKHOUSE_HOST` has been set above. An astute reader will notice we pass environment variables to `make test` like our earlier workflow, to increase timeouts. However, we lower `CLICKHOUSE_QUORUM_INSERT` to `2`. This is required as some tests need data to be present on all nodes prior to querying. While our previous monolithic service had three nodes, our smaller development service has only two.
11. Destroys the service irrespective of the success (`if: always()`) of the workflow via the `terraform destroy` command.


These changes are now live! Whenever a PR or commit is issued to the repository, changes will be tested against an ephemeral ClickHouse Cloud cluster!


![git_actions.png](/uploads/git_actions_a428225503.png)

> Currently, these tests do not run for PRs raised from forks and only branches (this requires members of the ClickHouse organization). This is a [standard Github policy](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/) for pull\_request events, as it potentially allows secrets to be leaked. We plan to address this with future enhancements.


## Conclusion [\#](/blog/clickhouse-cloud-terraform-for-continuous-integration-and-continuous-delivery-deployment-ci-cd#conclusion)


In this blog post, we have used the new Terraform provider for ClickHouse Cloud to build a CI/CD workflow in Github actions which provisions ephemeral clusters for testing. We use this approach to reduce the cost and complexity of our client testing with ClickHouse Cloud.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

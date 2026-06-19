# How to create reproducible ZIPs for AWS Lambda


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How to create reproducible ZIPs for AWS Lambda

![](/_next/image?url=%2Fuploads%2Fmisha_3ac4306654.png&w=96&q=75)[Misha Shiryaev](/authors/misha-shiryaev)Aug 28, 2025 · 6 minutes readIn our CI/CD system at ClickHouse we use [lambda functions](https://docs.aws.amazon.com/lambda/) a lot. AWS provides two ways to deploy a lambda function: Docker images and ZIP archives.


The latter is much lighter, so we have used it exclusively since [November 2022](https://github.com/ClickHouse/ClickHouse/pull/43769). Besides the artifact size, it was easier to automate it in a simple [script](https://github.com/ClickHouse/ClickHouse/blob/1443e490ea5287175f031eaee567fe5024cd7306/tests/ci/team_keys_lambda/build_and_deploy_archive.sh).


In late 2023, we started using Terraform/OpenTofu to manage the CI/CD infrastructure. This raised the question of "how should we manage artifacts to deploy?"


The question contains two different points:


- The artifact should not change the content after each rebuild; otherwise, it would be redeployed on each execution of the `tofu apply` command.
- Ideally, it should be built on the fly, without any additional infrastructure on top, like pushing it to S3 or so


## Building metadata\-independent ZIP archive on linux [\#](/blog/zip-archive-aws-lambda#building-metadata-independent-zip-archive-on-linux)


![zip-archive-blog-1.png](/uploads/zip_archive_blog_1_7a0fb214e9.png)
### Challenge one: the order matters [\#](/blog/zip-archive-aws-lambda#challenge-one-the-order-matters)


There are many factors affecting the ZIP archive content. One of the unexpected (for me) things is the order of archived files. Here's the example:



```
# create files 1 2 3 4 5
$ touch {1..5}

# archive them in sorted and reserved order
$ ls [1-5] | sort    | zip -q -0 --names-stdin sorted.zip
$ ls [1-5] | sort -r | zip -q -0 --names-stdin reversed.zip

# compare two files byte-by-byte
$ cmp -l sort.zip rev.zip
 31  61  65
 62  62  64
124  64  62
155  65  61
202  61  65
249  62  64
343  64  62
390  65  61

```

And here's the very first issue to solve. The order of files must be the same.


Besides that, we should omit passing the directories to the zip command. Otherwise, it could cause inconsistency. The argument `-D` helps here.


So, here's the very first solved issue.



```
export LC_ALL=c
# zip uses random files order by default, so we sort the files alphabetically
find . ! -type d -print0 | sort -z | tr '\0' '\n' | zip -XD -0 ../"$PACKAGE".zip --names-stdin

```

The found files are null\-divided and sorted, and then null is replaced by a new line and passed to the ZIP.


### Challenge two: age matters [\#](/blog/zip-archive-aws-lambda#challenge-two-age-matters)


This is the part of the man zip about one of the arguments above:



```
   -X
   --no-extra
           Do not save extra file attributes (Extended Attributes on OS/2,
           uid/gid and file times on Unix).  The  zip  format  uses  extra
           fields  to include additional information for each entry.  Some
           extra fields are specific to particular  systems  while  others
           are applicable to all systems.  Normally when zip reads entries
           from  an  existing archive, it reads the extra fields it knows,
           strips the rest, and adds the extra fields applicable  to  that
           system.   With  -X, zip strips all old fields and only includes
           the Unicode and Zip64 extra fields (currently these  two  extra
           fields cannot be disabled).

```

So, it should ignore timestamps.. But!



```
$ touch -t 201212121212 {1..5}
$ zip -XD0q older.zip {1..5}
$ touch -t 201212121213 {1..5}
$ zip -XD0q newer.zip {1..5}
$ cmp -l older.zip newer.zip
 11 200 240
 42 200 240
 73 200 240
104 200 240
135 200 240
168 200 240
215 200 240
262 200 240
309 200 240
356 200 240

```

Somebody lies. So, before archiving the files, we need to change the last modification time.


`find "$PACKAGE" ! -type d -exec touch -t 201212121212 {} +`


### Challenge three: Python byte\-code [\#](/blog/zip-archive-aws-lambda#challenge-three-python-byte-code)


According to the [recommendations](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-pycache), including `.pyc` files in the lambda archive speeds\-up the cold start of the lambdas, but can cause issues with the byte\-code version. The byte\-code version depends on the Python version and the system architecture.


After some experiments, we found that the best way to skip the `.pyc` files is to use the `-x,--exclude` option of the zip command.


### Final challenge: the OS matters [\#](/blog/zip-archive-aws-lambda#final-challenge-the-os-matters)


The last challenge is the OS. The ZIP archive format depends on the OS on which it was created. MacOS and Linux produce different ZIP archives, even if the content is the same. At this point we were already too tired of finding out what was going on. It was clear that any difference in `zip` binary could cause a bit\-difference in the archives. 


The best way we came up with is using Python to create the ZIP archive. Python's `zipfile` module creates a consistent ZIP archive, regardless of the OS. But to be completely sure, we use Python from the `public.ecr.aws/lambda/python` image, which is the same as the one used by AWS Lambda.



```
docker_cmd=(
  docker run -i --net=host --rm --user="${UID}" -e HOME=/tmp --entrypoint=/bin/bash
  --volume="${WORKDIR}/..:/ci" --workdir="/ci/${DIR_NAME}" "${DOCKER_IMAGE}"
)

"${docker_cmd[@]}" -ex <<EOF
cd '$PACKAGE'
find ! -type d -exec touch -t 201212121212 {} +

python <<'EOP'
import zipfile
import os
files_path = []
for root, _, files in os.walk('.'):
    files_path.extend(os.path.join(root, file) for file in files)
# persistent file order
files_path.sort()
with zipfile.ZipFile('../$PACKAGE.zip', 'w') as zf:
    for file in files_path:
        zf.write(file)
EOP
EOF

```

## Building the virtual environment for the lambda [\#](/blog/zip-archive-aws-lambda#building-the-virtual-environment-for-the-lambda)


The code to address this challenge is quite simple. The only thing to remember is that the virtual environment should be created with the same Python version as the one used by AWS Lambda.



```
docker_cmd=(
  docker run -i --net=host --rm --user="${UID}" -e HOME=/tmp --entrypoint=/bin/bash
  --volume="${WORKDIR}/..:/ci" --workdir="/ci/${DIR_NAME}" "${DOCKER_IMAGE}"
)
rm -rf "$PACKAGE" "$PACKAGE".zip
mkdir "$PACKAGE"
cp app.py "$PACKAGE"
if [ -f requirements.txt ]; then
  VENV=lambda-venv
  rm -rf "$VENV"
  "${docker_cmd[@]}" -ex <<EOF
    '$PY_EXEC' -m venv '$VENV' &&
    source '$VENV/bin/activate' &&
    pip install -r requirements.txt &&
    # To have consistent pyc files
    find '$VENV/lib' -name '*.pyc' -delete
    cp -rT '$VENV/lib/$PY_EXEC/site-packages/' '$PACKAGE'
    rm -r '$PACKAGE'/{pip,pip-*,setuptools,setuptools-*}
    chmod 0777 -R '$PACKAGE'
EOF
fi

```

Here we check if the lambda function has a `requirements.txt` file. If it does, we create a virtual environment with the same Python version as the one used by AWS Lambda, install the dependencies, and copy the site\-packages to the lambda package directory. To remove the unnecessary files, we delete the `pip` and `setuptools` directories as well as Python byte\-code files.


## Conclusion [\#](/blog/zip-archive-aws-lambda#conclusion)


The full script doing the job is available [here](https://github.com/ClickHouse/ClickHouse/blob/1443e490ea5287175f031eaee567fe5024cd7306/tests/ci/team_keys_lambda/build_and_deploy_archive.sh). Later it was moved into the private repository, but it is still used in Terraform/OpenTofu configuration to deploy the lambda functions.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

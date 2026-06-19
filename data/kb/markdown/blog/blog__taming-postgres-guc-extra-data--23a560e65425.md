# Taming PostgreSQL GUC “extra” Data


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Taming PostgreSQL GUC “extra” Data

![](/_next/image?url=%2Fuploads%2FImage_512x512_1_8bc569c360.png&w=96&q=75)[David Wheeler](/authors/david-wheeler)Dec 18, 2025 · 11 minutes readWhile building [pg\_clickhouse](https://pgxn.org/dist/pg_clickhouse/ "pg_clickhouse on PGXN"), I developed a PostgreSQL setting (or "[GUC](https://github.com/postgres/postgres/blob/master/src/backend/utils/misc/README "PostgreSQL Source: GUC Implementation Notes")")
that takes a list of key/value pairs and sets them as [session settings](https://clickhouse.com/docs/operations/settings/settings "ClickHouse Docs: Session Settings") in
every query sent to ClickHouse. The [v0\.1\.0](https://github.com/ClickHouse/pg_clickhouse/releases/tag/v0.1.0 "pc_clickhouse Release v0.1.0") release kept the list of settings
as a string, and parsed it for every query. We wanted to reduce that overhead
by parsing them into a key/value data structure when the GUC is set.


This post
goes into the implementation weeds for this work, released in [v0\.1\.1](https://github.com/ClickHouse/pg_clickhouse/releases/tag/v0.1.1 "pc_clickhouse Release v0.1.1"),
covering the various attempts and ultimate solution. It will hopefully be
helpful to other PostgreSQL extension developers.


Just want to try querying ClickHouse from PostgreSQL with [pg\_clickhouse](https://pgxn.org/dist/pg_clickhouse/ "pg_clickhouse on PGXN") and
tune out all this C code and internals stuff? Check out [the tutorial](https://pgxn.org/dist/pg_clickhouse/doc/tutorial.html "pg_clickhouse Tutorial on PGXN").


## The Challenge [\#](/blog/taming-postgres-guc-extra-data#the-challenge)


I wanted to optimize away parsing the key/value pairs from the [pg\_clickhouse](https://pgxn.org/dist/pg_clickhouse/ "pg_clickhouse on PGXN")
`pg_clickhouse.session_settings` GUC for every query by pre\-parsing it on
assignment and assigning it to a separate variable. It took a few tries, as
the GUC API requires quite specific memory allocation for extra data to work
properly. It took me a few tries to land on a workable and correct solution.


Here's the `pg_clickhouse.session_settings` setup:



```
DefineCustomStringVariable(
    "pg_clickhouse.session_settings",
    "Sets the default ClickHouse session settings.",
    NULL,
    &ch_session_settings,
    "join_use_nulls 1, group_by_use_nulls 1, final 1",
    PGC_USERSET,
    0,
    chfdw_check_settings_guc,
    chfdw_settings_assign_hook,
    NULL
);

```

So many arguments! Here's the [public declaration](https://github.com/postgres/postgres/blob/bfe5c4b/src/include/utils/guc.h#L393-L402):



```
extern void DefineCustomStringVariable(
    const char *name,
    const char *short_desc,
    const char *long_desc,
    char **valueAddr,
    const char *bootValue,
    GucContext context,
    int flags,
    GucStringCheckHook check_hook,
    GucStringAssignHook assign_hook,
    GucShowHook show_hook
) pg_attribute_nonnull(1, 4);

```

Quick explanations:


- **`name`:** The name of the GUC, a used by `SET`. Extension GUCs should
start with a prefix and a dot; hence `pg_clickhouse.session_settings`
- **`short_desc`:** A short description of the GUC.
- **`long_desc`:** A long description of the GUC.
- **`valueAddr`:** A pointer to the variable in which the GUC API stores
the value. The pg\_clickhouse GUC uses a global `char *` variable.
- **`bootValue`:** The default value for the GUC when the extension loads.
- **`context`:** Determines who can set the GUC and when. We want to allow
any users to set `pg_clickhouse.session_settings`, but there are a number
of [other options](https://github.com/postgres/postgres/blob/bfe5c4bec75091d5c91813ff9c6994a169ceb8ef/src/include/utils/guc.h#L39-L80).
- **`flags`:** A bitmask of [GUC flags](https://github.com/postgres/postgres/blob/bfe5c4bec75091d5c91813ff9c6994a169ceb8ef/src/include/utils/guc.h#L210-L257) that modify behavior, determine
formatting and parsing.
- **`check_hook`:** A callback function that validates a value and
optionally sets `extra` data to be passed to the assign hook. Our code
points to `chfdw_check_settings_guc`, which raises an error if a new value
fails to parse as a valid key/value list.
- **`assign_hook`:** A callback function that assigns a GUC value to a
variable other than `valueAddr`. May use `extra` data set by the check
hook.
- **`show_hook`:** A callback that reformats a GUC for display. Used by
some GUCs to normalize or canonicalize values, such as time zones.


The `check_hook` and `assign_hook` parameters allow the extra data parsing we
need. The idea is that the check hook can point `extra` at a data structure
and that value is passed to the assign hook, which assigns it to a variable.


## First Attempt [\#](/blog/taming-postgres-guc-extra-data#first-attempt)


For my first attempt, I created a pointer to a list of key/value pairs,
assuming that I could point `extra` at it in the check hook and then assign it
in the assign hook. Something like:



```
static bool
chfdw_check_settings_guc(char **newval, void **extra, GucSource source)
{
    if (*newval == NULL || *newval[0] == '\0')
        return true;

    kv_list * settings = parse_and_malloc_kv_list(*newval);
    if (!settings)
        return false;

    *extra = settings;
    return true;
}

```

Note that `parse_and_malloc_kv_list()` uses `malloc()` to allocate memory for
the list, each item in the list, and each key and value. It uses `malloc()`
because we're going to store the value in a global, so it must not be cleaned
up by the GUC memory context.


Then, in the assign hook:



```
static void
chfdw_settings_assign_hook(const char *newval, void *extra)
{
    if (ch_session_settings_list)
        kv_list_free(ch_session_settings_list);
    ch_session_settings_list = (kv_list *) extra;
}

```

Free the existing settings list, if it's set, then assign the new list from
`extra`.


Seems pretty simple, right? Alas, I could never get the assignment to work; I
need to better understand memory allocation, pointers, pointers to pointers,
etc.


## Second Attempt [\#](/blog/taming-postgres-guc-extra-data#second-attempt)


So I tried just doing the assignment in the check hook and doing away with the
assign hook. Something like:



```
static bool
chfdw_check_settings_guc(char **newval, void **extra, GucSource source)
{
    if (*newval == NULL || *newval[0] == '\0')
        return true;

    kv_list * pairs = parse_and_malloc_kv_list(*newval);
    if (!pairs)
        return false;

   if (ch_session_settings_list)
        kv_list_free(ch_session_settings_list);
    ch_session_settings_list = pairs;

    return true;
}

```

I asked about this approach on the Postgres Discord, where Tom Lane kindly
responded with:



> You absolutely must not change any session state in a check hook. That's
> called when we're merely speculating about whether (eg) a proposed ALTER
> DATABASE SET command is okay; there is no guarantee that we are about to
> apply the setting.


I also noticed that `RESET` wouldn't work, as the check hook isn't called for
a reset. So much for that idea!


## Third Attempt [\#](/blog/taming-postgres-guc-extra-data#third-attempt)


Next I switched to a double parse in order to avoid these issues. The check
hook simplified to:



```
static bool
chfdw_check_settings_guc(char **newval, void **extra, GucSource source)
{
    if (*newval == NULL || *newval[0] == '\0')
        return true;

    kv_list * settings = parse_and_malloc_kv_list(*newval);
    if (!settings)
        return false
    kv_list_free(ch_session_settings_list);

    /* No errors, return true. */
    return true;
}

```

And the assign hook became:



```
static void
chfdw_settings_assign_hook(const char *newval, void *extra)
{
    if (ch_session_settings_list)
        kv_list_free(ch_session_settings_list);
    PG_TRY();
    {
        ch_session_settings_list = parse_and_malloc_kv_list(newval);
    }
    PG_CATCH();
    {
        ereport(LOG,
                (errcode(ERRCODE_FDW_ERROR),
                 errmsg("unexpected error parsing \"%s\"", newval)));
    }
    PG_END_TRY();
}

```

Now both hooks execute `parse_and_malloc_kv_list()`. This double parsing
seemed acceptable, given that it replaces parsing the settings for every
query. This solution became [pg\_clickhouse\#95](https://github.com/ClickHouse/pg_clickhouse/issues/95 "ClickHouse/pg_clickhouse#95 Add kv_list and refactor session_settings with it"). I was, however, dissuaded from
applying it because its memory management is more complicated than the
eventual solution, and also by this offhand Discord comment, again from Tom
Lane:



> I do not recommend doing new allocations inside the assign hook. It is
> expected to be incapable of failing.


Which makes me think that the risk of actually raising an error that escapes
`PG_TRY()`, while low, renders this approach suboptimal, to say the least.


## Interlude: Proper use of Extra [\#](/blog/taming-postgres-guc-extra-data#interlude-proper-use-of-extra)


Back in my [first attempt](#first-attempt), `parse_and_malloc_kv_list()` would
`malloc()` memory for each bit of the structure it built: the `kv_list`, a
pointer to a list of key/value pairs, each of those pairs, plus the key and
value strings themselves. The pattern still holds in [pg\_clickhouse\#95](https://github.com/ClickHouse/pg_clickhouse/issues/95 "ClickHouse/pg_clickhouse#95 Add kv_list and refactor session_settings with it")'s
[`kv_list.c`](https://github.com/ClickHouse/pg_clickhouse/pull/95/files#diff-e6e6afea9fa95db0fb2d8a3afe3b757c1a5c66e54c071f0bf315ad862473a512R20-R70). But it made use of `extra` impossible \-\-\- or at least it
surpassed my C expertise. Tom educated me about how to properly use `extra`:



> You're supposed to use guc\_malloc, and the extra data has to be a single
> malloc block, not a list.   
>   
> 
> The general principle with GUC extra data is that once your check\_hook hands
> it back, it's guc.c's responsibility to free it when no longer needed. The
> single\-chunk restriction is because guc.c wouldn't know about other
> components of the data structure.


This approach allows correct use of the `extra` data, does no other assignment
in the check hook, and does nothing but assign in the assign hook, eliminating
the error risk. All I had to do was figure out how to do a single
`guc_malloc()` with a list of key/value pairs.


## Fourth Attempt [\#](/blog/taming-postgres-guc-extra-data#fourth-attempt)


The solution submitted in [pg\_clickhouse\#94](https://github.com/ClickHouse/pg_clickhouse/issues/94 "ClickHouse/pg_clickhouse#94 Add kv_list and refactor session_settings with it") follows the example of
`ConvertTimeZoneAbbrevs()` in PostgreSQL's [datetime.c](https://github.com/postgres/postgres/blob/84d5efa7e3ebcf04694d312b0f14ceb35dcdfb8e/src/backend/utils/adt/datetime.c#L4986-L5071) to calculate the total
memory required for all the key/value pairs and allocate that memory as a
single block. The struct's definition:



```
typedef struct kv_list
{
    int            length;
    char data[];
}            kv_list;

```

Note the use of a [flexible array](https://en.wikipedia.org/wiki/Flexible_array_member "Wikipedia: Flexible array member"), `data[]`. It serves as a pointer to the
keys and values, which the constructor simply writes from its address as a
list of null\-terminated strings. It is not actually a C structure at all. How
is the memory allocated? Once the constructor sums up the memory required for
all the keys and values like so:



```
kv_list * list = guc_malloc(ERROR, offsetof(kv_list, data) + summed_size);

```

It requires the size of the `kv_list` struct up to the `data` field, and adds
the total it summed for the key and value strings. Once the `kv_list` has been
allocated, the code iterates over the key/value pairs again and simply appends
them all, one after another, to the point starting at the `data` field.\`


Now, iterating over these pairs is tricky, so the resulting [kv\_list API](https://github.com/ClickHouse/pg_clickhouse/pull/94/files#diff-c9b377b9fa916c6c3a0afa9faf1f36ef5a6a89570aa508ee7c71ed3dbde18023) also
provides an iterator structure to simplify it.



```
for (kv_iter iter = new_kv_iter(settings); !kv_iter_done(&iter); kv_iter_next(&iter))
{
    printf("%s => %s\n", iter.name, iter.value);
}

```

This keeps things simple for the places in the code that need to process the
setting, namely setting them up for [binary](https://github.com/ClickHouse/pg_clickhouse/blob/1ac05a319d94b41140ce7ce113646d308bdba997/src/binary.cpp#L179-L182) and [http](https://github.com/ClickHouse/pg_clickhouse/blob/1ac05a319d94b41140ce7ce113646d308bdba997/src/http.c#L179-L187) queries.


With all that in place and a single `guc_malloc()`ed block of memory,
[pg\_clickhouse\#94](https://github.com/ClickHouse/pg_clickhouse/issues/94 "ClickHouse/pg_clickhouse#94 Add kv_list and refactor session_settings with it") finally uses the check and assign hooks properly:



```
static bool
chfdw_check_settings_guc(char **newval, void **extra, GucSource source)
{
    if (*newval == NULL || *newval[0] == '\0')
        return true;

    kv_list * settings = parse_and_guc_malloc_kv_list(*newval);
    if (!settings)
        return false;

    *extra = settings;
    return true;
}

```

This is almost identical to the [First Attempt](#first-attempt), except that
`parse_and_guc_malloc_kv_list()` uses `guc_malloc()` to allocates `settings`
as a single block of memory, later assigned to `extra`. The assign hook then
becomes error\-prone\-free:



```
static void
chfdw_settings_assign_hook(const char *newval, void *extra)
{
	ch_session_settings_list = (kv_list *) extra;
}

```

It no longer frees the previous values of `ch_session_settings_list`; instead
the GUC API cleans it up at the appropriate time.


## More to Learn [\#](/blog/taming-postgres-guc-extra-data#more-to-learn)


This solution satisfies me, in that it minimizes the memory required for the
settings values, leaves memory management to the GUC API, provides a simple
interface for iterating over settings, and correctly uses the check and assign
hooks. Plus I learned a ton about that API and how to coerce C memory to bend
away from strict `struct`\-based allocation.


Although I've also kept a local copy of [pg\_clickhouse\#95](https://github.com/ClickHouse/pg_clickhouse/issues/95 "ClickHouse/pg_clickhouse#95 Add kv_list and refactor session_settings with it") to return to as I
learn more about pointers, pointers to pointers (and pointers to pointers to
pointers?) in C. I would think there could be a way to point `extra` and a
point in memory such that the GUC API just removes the pointer, not the memory
it points to. That would allow the data to be `malloc()`ed in the check hook
and assigned in the assigned hook, something like this in the check hook:



```
    kv_list * settings = parse_and_malloc_kv_list(*newval);
    if (!settings)
        return false;

    /* Allocate just the memory needed to point to a kv_list. */
    extra = guc_malloc(ERROR, sizeof(kv_list *));
    extra = &settings;
    return true;

```

Then the assign hooks would be something like:



```
	ch_session_settings_list = (kv_list *) *extra;

```


But I haven't figured out the proper incantation yet; as I said. Not that I
would ever merge a solution along these lines; it would again prevent `RESET`
from working, since GUC assumes it actually has the complete extra value. But
it challenges me, creates the opportunity to learn more and better C
techniques. And maybe, someday, how to abuse them more effectively. 😈


Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")

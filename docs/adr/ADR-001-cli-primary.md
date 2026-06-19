# ADR-001: CLI as Primary Interface; Web as Optional Thin Wrapper

## Status

Accepted

## Context

ClickAdvisor is being built for a user group that already works inside terminal
and automation-heavy environments. The core audience is DBA, database platform
engineers, and performance-minded backend engineers who treat the shell as a
primary workspace rather than as a secondary utility. Their normal operating
loop includes direct query work, configuration review, CI jobs, SSH sessions,
incident tooling, and scripted verification. For this audience, a command-line
tool is not a compromise; it is the most natural integration point.

The project also has a strong compliance and deployment constraint. The product
must be able to operate in local or tightly controlled environments where moving
customer SQL or environment context into an external service is undesirable or
prohibited. A CLI package with explicit inputs and outputs is easier to audit,
easier to run on hardened hosts, and easier to embed into existing enterprise
change-management flows than a web-first application that implies a persistent
service layer. The fewer always-on components the MVP requires, the easier it is
to explain the system boundary to security reviewers.

Another important factor is CI/CD integration. One of the project’s intended
usage patterns is “query review as part of delivery flow”: developers or DBA can
run the advisor in local pre-merge checks, in repository automation, or in a
batch analysis mode against a curated set of SQL files. This mode is
substantially easier to support when the primary product surface is a
deterministic, scriptable CLI with stable exit codes, plain text or structured
output, and no GUI dependency. If the first-class interface were a browser UI,
the team would still need to design a CLI-compatible automation surface later,
which would create duplicated product surface area from the beginning.

The project needs room for lightweight demos and fast feedback collection.
Product stakeholders may still want a simple web experience to show sample
analysis results or let non-terminal users paste a query and see the output.
However, that need is secondary and should not distort the architecture. If a
web interface becomes the place where the real logic lives, the project risks
turning into two products: a browser app that is “real,” and a CLI that is a
limited export path. That split would be especially harmful for a tool whose
credibility depends on strict trust semantics and reproducible local behavior.

We also considered whether a richer terminal interface would add value. A TUI
can be compelling when the product requires persistent interaction state,
keyboard navigation across dense panels, or interactive drill-down workflows.
ClickAdvisor does not yet have that shape. The MVP needs composable commands,
machine-friendly outputs, and straightforward integration into scripts, not an
interactive terminal dashboard. A TUI at this stage would add implementation and
maintenance cost without solving the primary workflow better than a normal CLI.

## Decision

The primary interface for ClickAdvisor is a Typer-based CLI.

The CLI is the canonical surface through which the product contract is defined:

- inputs are provided explicitly through flags, files, stdin, or referenced
  metadata sources
- analysis is executed locally by the core package
- outputs are returned as terminal-readable text and, where needed, structured
  machine-readable formats
- mode selection, including LLM behavior, is expressed through CLI flags

All core functionality must be implemented in reusable application modules that
are independent from the CLI presentation layer. The CLI is responsible for
argument parsing, output formatting, and command orchestration, but it must not
contain business logic that cannot be reused elsewhere.

If and when a web experience is built, it will be implemented as an optional,
thin FastAPI-based wrapper over the same core modules. That wrapper is intended
for demonstration, internal feedback loops, and low-friction product discovery.
It is not a separate decision engine. The web layer must call the same analysis
entry points, use the same rule engine, preserve the same tier semantics, and
avoid introducing a parallel configuration model that diverges from the CLI.

This means the product hierarchy is fixed as follows:

1. core analysis library
2. CLI as primary interface
3. optional web wrapper as secondary interface

The CLI remains the source of truth for capabilities and feature completeness.
The web layer, if present, is allowed to be narrower than the CLI. The reverse
is not allowed.

## Consequences

The most immediate consequence is architectural clarity. The team can design the
core package around explicit function boundaries and stable input/output
contracts without coupling those decisions to browser concerns such as sessions,
frontend state, live updates, or deployment topology. That keeps the first
implementation steps aligned with the actual user workflow and reduces the risk
of spending early effort on infrastructure rather than optimizer value.

This choice also improves the compliance story. Packaging a CLI that runs
locally and only consumes SQL, plans, schema, and metadata is simpler to defend
than deploying a web service in environments with sensitive workload context.
The product’s zero-data-egress stance becomes easier to validate when there is
no mandatory server process exposed through HTTP.

There is also a beneficial testing consequence. A CLI-first product naturally
encourages deterministic invocation patterns that can be captured in unit tests,
snapshot tests, benchmark harnesses, and CI workflows. This supports the
project’s long-term need for reproducible evaluation on curated query cases.

The decision imposes discipline on any future web work. Because the browser
interface is explicitly secondary, it cannot introduce product semantics that do
not already exist in the core or CLI. This prevents drift, but it also means
the web experience may feel intentionally limited in early phases. That is an
acceptable tradeoff because the goal of the wrapper is feedback and demo value,
not full product parity on day one.

Another consequence is that user experience work in the MVP will primarily focus
on command ergonomics, output readability, error messages, and report formats
instead of visual interaction design. This is consistent with the audience, but
it means adoption among non-terminal users may depend on the optional wrapper
later.

## Alternatives Considered

### Web-first application

A web-first architecture was rejected because it would optimize the system for a
secondary distribution path instead of the main operator workflow. It would also
complicate compliance review by introducing an always-on service boundary and
would delay scriptability, CI integration, and local reproducibility. Most
importantly, it would create pressure to treat the browser layer as the true
product surface and the CLI as an afterthought, which is opposite to the
project’s intended operating model.

### Terminal UI (TUI)

A richer TUI was rejected as overkill for the MVP use case. The initial value of
ClickAdvisor comes from deterministic analysis and trustworthy recommendations,
not from an interactive terminal shell with panels and navigation state. A TUI
would raise implementation complexity and maintenance cost without materially
improving the primary workflow of “analyze this query in local or CI context.”

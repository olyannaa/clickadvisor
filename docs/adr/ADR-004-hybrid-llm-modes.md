# ADR-004: Hybrid LLM Architecture (`none` / `local` / `remote`)

## Status

Accepted

## Context

ClickAdvisor is intentionally not an LLM-centric product, but it still benefits
from controlled language-model assistance in some parts of the workflow. LLMs
can help generate explanations, summarize retrieved documentation, propose
candidate rewrites for later verification, and improve the readability of
user-facing reports. The challenge is that the project’s users operate under
very different constraints. Some environments cannot allow any model inference
that involves outbound data transfer. Some teams have strong local hardware and
want a fully self-hosted workflow. Others care more about convenience and model
quality than about hard local-only execution, as long as sensitive data can be
handled safely.

If the product tied itself to a single LLM deployment model, it would
unnecessarily narrow its applicability. A remote-only design would conflict with
the compliance and local-first posture that motivates the product in the first
place. A local-only design would be difficult for teams without suitable
hardware, and it would make the quality of explanatory features depend heavily
on what can be hosted on a laptop or internal GPU box. A design that always
expects an LLM, regardless of where it runs, would also send the wrong message
about the architecture: it would imply that the rules are secondary and that the
system degrades into near-uselessness when models are disabled.

That implication is unacceptable. One of the core product claims is that the
advisor remains valuable without any LLM at all because its center of gravity is
the rule engine and the ClickHouse-aware cost analysis pipeline. The no-LLM
mode is therefore not a fallback for degraded deployments; it is a first-class
expression of the product thesis.

At the same time, the team wants a pragmatic story for when LLMs are allowed.
Some users will prefer local model hosting because it preserves control and can
still enrich the experience. Others will accept a remote provider for stronger
model quality or lower operational overhead. These realities argue for an
explicit multi-backend architecture instead of one hidden inference path.

## Decision

ClickAdvisor supports three LLM backends exposed as explicit CLI modes:

- `--llm=none`
- `--llm=local`
- `--llm=remote`

### `--llm=none`

This mode disables LLM participation entirely. The system runs on rules,
metadata interpretation, cost-based reasoning, retrieval where applicable, and
deterministic report construction only. The expected target is that roughly 70%
of useful product functionality remains available in this mode. This is not a
degraded emergency path. It is a deliberate feature that demonstrates the core
engine works independently of generative assistance.

### `--llm=local`

This mode enables local inference through self-hosted backends such as Ollama or
vLLM. The initial model family target is a coding- and reasoning-capable model
in the class of Qwen2.5-Coder-7B. The purpose of local mode is to provide
advisory and explanation features while preserving a local execution boundary
for organizations that allow model use but require data residency and direct
operational control.

### `--llm=remote`

This mode enables inference through remote API providers such as Anthropic
Claude or OpenAI models. Before any request is sent, SQL literals and other
sensitive values must be processed through redaction logic based on `sqlglot`
parsing so that outbound content is minimized and structurally preserved. Remote
mode exists for users who prioritize model quality, convenience, or lack of
local inference infrastructure, while still requiring an explicit privacy
boundary.

The LLM layer remains advisory regardless of backend. Enabling a model does not
change the trust tier semantics of recommendations.

## Consequences

The main consequence is architectural honesty. The product can now support a
range of deployment realities without pretending that one inference model fits
all environments. Teams with strict compliance requirements can run with
`--llm=none` or `--llm=local`; teams with more flexible policies can use
`--llm=remote`. The CLI makes this choice explicit instead of burying it in
configuration or build-time behavior.

This decision also reinforces the core claim that ClickAdvisor is not “just an
AI wrapper.” Because `--llm=none` is a first-class mode, the codebase must
preserve real value in the deterministic rule and estimation pipeline. That is a
healthy architectural constraint. It prevents the project from quietly shifting
toward LLM dependence as features accumulate.

Local mode introduces operational complexity, especially around model setup,
hardware availability, and runtime performance. That is an accepted tradeoff
because local inference is essential for organizations that want advisory
capability without data egress. Remote mode, meanwhile, introduces privacy and
redaction responsibilities that must be handled carefully. The redaction layer
is not optional polish; it is part of the trust boundary.

The three-mode design also improves testing and product communication. Behavior
can be validated per mode, and documentation can clearly state what guarantees
change when a user selects one backend over another. Most importantly, the
product can communicate that model usage is a policy decision, not a hidden
implementation detail.

## Alternatives Considered

### Always require an LLM

This was rejected because it would violate the project’s core premise. A system
that stops being useful without a language model is architecturally centered on
the model, not on the rule engine. That would weaken the differentiation,
complicate compliance, and make the local-first story much less credible.

### Remote-only LLM integration

This was rejected because it would exclude the very environments that most need
local execution guarantees. Even with redaction, some organizations will not
permit outbound inference at all. A remote-only design would turn those users
into second-class citizens and would clash with the project’s zero-data-egress
orientation.

### Local-only LLM integration

This was also rejected because not every target user will have the hardware or
operational appetite to run local inference. The project benefits from keeping a
remote option available as long as it is explicit and protected by redaction and
mode-aware trust semantics.

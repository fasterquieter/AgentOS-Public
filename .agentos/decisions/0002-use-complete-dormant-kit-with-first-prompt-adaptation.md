# Use complete dormant kit with first-prompt adaptation

Status: accepted
Date: 2026-08-26

## Context

AgentOS must serve two roles in one checkout: its own master development project
and a self-contained seed that can become an unrelated product after an ordinary
first project prompt. Selective installation would force the human or first
agent to predict future needs. Leaving framework source, examples, and AgentOS
self-history intermixed at the product root would contaminate project identity
and context. Evidence from existing repositories also showed that small mandatory routers
work, dormant complexity must stay out of normal context, and deterministic
tools earn their place mainly on mechanical checks.

## Decision

Keep the complete reusable framework in the hidden `.agentos-kit/` directory.
Use `.agentos/seed-state.md` plus the task subject as a simple identity gate:
AgentOS work remains in master mode, while a substantive specification for a
different product triggers the repository-native adaptation protocol without a
human command. Adaptation replaces AgentOS self-memory with earned active
project memory, keeps one archived origin marker, and preserves the complete kit
as a dormant capability library.

The root `AGENTS.md` and Markdown adaptation guide own the judgment. The Python
helper previews the exact mechanical transaction, validates lifecycle
invariants, and keeps dormant records out of ordinary routing; it does not apply
semantic adaptation, classify the product prompt, or choose modules.
The individual capability inventory has one canonical representation in
`.agentos-kit/CAPABILITIES.md`, not a duplicated JSON catalog.

## Alternatives

- Require `agentos init` — rejected because the intended human workflow contains
  no Terminal or framework-specific step.
- Copy only selected modules — rejected because first-use relevance cannot
  reliably predict later product needs and dormant disk cost is negligible.
- Keep reusable and AgentOS-self material together — rejected because a new
  project could route AgentOS decisions, plans, and examples as its own truth.
- Build a deterministic initializer/classifier — rejected because extracting
  product meaning and judging earned memory are frontier-agent judgment tasks.
  A read-only transaction preview is retained because exact file operations and
  changed-target detection are mechanical safety questions.
- Duplicate every capability in the JSON catalog — removed during review because
  it created two inventories that could drift without improving discovery.

## Consequences

- A complete clone is self-contained and future capabilities survive without
  entering normal context.
- The exact start experience becomes clone, ordinary project prompt, and no
  AgentOS-specific human action.
- An adapted product feels project-native because root self-development material
  is removed while reusable infrastructure remains hidden.
- The first agent must faithfully follow a one-time Markdown protocol; tests can
  verify that the instructions and outputs are coherent, but cannot prove every
  future vendor model will comply.
- Before editing, the first agent can compare a generated replace/remove/review/
  preserve report with Git changes and must name deliberate deviations.
- `.agentos-kit/` is an architectural boundary that maintainers must preserve.
  Project copies may deliberately evolve it and need not track the master.

## Revisit when

Reopen if several capable agents fail the ordinary-prompt transition, if the
first-use context repeatedly exceeds the measured budget, if hidden-kit naming
causes tool incompatibility, or if projects fail to discover needed dormant
guidance from the capability map. Prefer instruction or representation fixes
before adding orchestration.

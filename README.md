# AgentOS: project memory for coding agents

[![CI](https://github.com/fasterquieter/AgentOS-Public/actions/workflows/ci.yml/badge.svg)](https://github.com/fasterquieter/AgentOS-Public/actions/workflows/ci.yml)

AgentOS helps a coding assistant remember what a software project is, what is
happening now, what must not be broken, and what the evidence actually proves.
It keeps that memory beside the code and routes only the useful slice into each
task.

This repository has two supported roles:

1. the master AgentOS framework-development project; and
2. a complete, self-contained seed that can be cloned or duplicated to start a
   different project.

## AgentOS in plain English

Imagine a very clever builder who arrives each morning with no memory of
yesterday. Source code shows the builder what exists, but not every promise,
reason, unfinished job, or past mistake. One enormous handbook would be just as
unhelpful: the warning that matters could disappear in the pile.

AgentOS gives the project a small front desk. It tells the builder what matters,
what is happening now, what must not be broken, what has actually been proved,
and where to find deeper notes for this particular job. The guiding rule is:
write down what is expensive to forget, label it honestly, and route it only
when useful. Keep the memory system smaller than the confusion it prevents.

## How it works

Three layers do the work, and all of them are plain files in the repository:

1. **`AGENTS.md`** is a small, always-visible router. Claude Code, Gemini CLI,
   and Cursor reach it through thin adapters (`CLAUDE.md`, `GEMINI.md`,
   `.cursor/rules/`); Codex reads it directly. Project truth is never copied
   into an adapter.
2. **`.agentos/index.json`** is an explicit, human-readable catalog. Each entry
   says what a document is, which task words and target paths make it relevant,
   what must be read with it, what kind of authority it carries (`contract`,
   `decision`, `evidence`, `working`, `historical`), whether it is `active` or
   `dormant`, when it should be reviewed, and how large it may grow.
3. **Markdown under `.agentos/`** holds the knowledge itself: project
   definition, current state, architecture, invariants, decisions, plans, failed
   approaches, raw feedback, and other records created only when they earn
   their place.

An agent can navigate the catalog by hand. The optional CLI makes the same
navigation deterministic: it ranks candidates by baseline flags, task-term
overlap, and path globs, follows `depends_on` edges, and reports every relevant
document that did not fit the requested token budget instead of hiding it.

## What is implemented

- **`.agentos-kit/src/agentos/`** — a Python 3.10+ package with no third-party
  dependencies:
  - `context` — explainable, omission-safe context recommendations with
    `--json` output;
  - `validate` — structural checks for catalog fields, missing files, broken
    Markdown links, dependency cycles, paths escaping the repository, overdue
    reviews, oversized documents, incomplete plans, seed/adapted-state
    invariants, and behavior-proof-map authority boundaries;
  - `adapt --preview` — a read-only transaction report for turning a fresh
    clone into another project's repository, including detection of
    working-tree changes on paths it would touch;
  - `eval-routing` — replay of routing regression cases captured from observed
    misses or noisy inclusions;
  - `init` — conservative installation into an existing repository that
    preserves an existing `AGENTS.md`;
  - `new` — indexed record scaffolding for plans, decisions, handoffs,
    feedback, failed approaches, personas, insights, findings, and upstream
    proposals.
- **`.agentos-kit/ADAPTATION.md` and `CAPABILITIES.md`** — the agent-led
  first-prompt adaptation protocol and a tiny map of dormant capabilities.
- **`.agentos-kit/docs/` and `reviews/`** — operating guides (knowledge model,
  workflows, bootstrap, governance, parallel-work reconciliation, testing
  evidence, behavior proof maps, personas and feedback, portability) and
  reusable review perspectives.
- **`.agentos-kit/examples/trailcache/`** — a fictional local-first app's
  mature memory: an active plan, a counterintuitive decision, a failed approach,
  personas, raw feedback, an insight, and a captured routing regression.
- **`.agentos-kit/tests/`** — 32 standard-library `unittest` cases covering
  routing, validation, change control, adaptation previews, routing
  evaluations, the example corpus, and full clone-to-project lifecycle
  simulations against temporary copies of this repository.
- **`.agentos/`** — this repository's own active memory, maintained with the
  same conventions it asks other projects to follow.

## Try it

No installation is needed; the CLI runs from the checkout:

```sh
git clone https://github.com/fasterquieter/AgentOS-Public.git
cd AgentOS-Public

# Ask for context on a task in this repository
PYTHONPATH=.agentos-kit/src python3 -m agentos context "change context routing budgets" --path .agentos-kit/src/agentos/catalog.py

# Ask for context in the TrailCache example
PYTHONPATH=.agentos-kit/src python3 -m agentos context "resume photo upload retry work" \
  --root .agentos-kit/examples/trailcache --path src/sync/queue.ts

# Replay the example's captured routing regression
PYTHONPATH=.agentos-kit/src python3 -m agentos eval-routing --root .agentos-kit/examples/trailcache

# Preview what adapting this clone into another project would touch (read-only)
PYTHONPATH=.agentos-kit/src python3 -m agentos adapt --preview --name "My Product"
```

To install the `agentos` command instead, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Run the tests and validation

```sh
PYTHONPATH=.agentos-kit/src python3 -m unittest discover -s .agentos-kit/tests -v
PYTHONPATH=.agentos-kit/src python3 -m agentos validate --strict
```

The same commands run in [CI](.github/workflows/ci.yml). Measured results of the
continuity simulations are recorded in
[`.agentos-kit/docs/simulations.md`](.agentos-kit/docs/simulations.md).

## Start a project without installing anything

1. Duplicate or clone this complete repository.
2. Make the copy the repository for the new project.
3. Open it with Codex, Cursor, Claude Code, Gemini, or another capable agent.
4. Prompt: `Read AGENTS.md. I want you to build ...`
5. The first agent previews the exact seed-file transaction, protects any local
   changes, adapts the active memory, and continues into the product. No
   AgentOS-specific command or setup prompt is required from the human.

The root router and [seed state](.agentos/seed-state.md) tell the first agent that
a substantive specification for any product other than AgentOS triggers the
one-time adaptation protocol. The agent replaces AgentOS's active project memory
with project-specific memory, keeps only justified active documents, and
preserves the complete reusable library under `.agentos-kit/` as dormant local
capability.

## Why the complete kit stays in every project

Repository storage is cheap; model context is scarce. The kit therefore remains
available on disk without entering ordinary task context. A tiny
[capability map](.agentos-kit/CAPABILITIES.md) lets a future agent discover one
relevant guide when the project gains a new need such as a behavioral proof gap,
hardware experiments, real-user feedback, authentication, terminology drift, or
architecture debt.

## Trust as the project grows

Optional `change_control` policies distinguish memory an agent may maintain from
contract or decision changes that need review or explicit authorization.
Parallel branches keep workstream-owned plans and converge through one
integration pass that rewrites shared current state from the merged repository.
When context routing fails, the observed miss can become a repeatable
`agentos eval-routing` case rather than an anecdote or a reason to add opaque
retrieval machinery.

## Design principles

Why not put everything in `AGENTS.md`?

- **The router stays small.** Every line of an always-loaded file costs context
  on every task, and long instruction files are followed less reliably.
  `AGENTS.md` carries identity, universal rules, and the route to deeper memory.
- **The catalog is explicit, not inferred.** A JSON graph with stable IDs is
  inspectable, offline, diffable, and validated mechanically. Embeddings or
  generated summaries add a second representation that can drift from the
  source.
- **Authority and lifecycle are separate fields.** A `contract` says what was
  accepted; `evidence` says what was observed; `working` says what is still a
  hypothesis. `active`, `draft`, `dormant`, `stale`, `superseded`, and
  `archived` say whether a record currently applies.
- **Omissions are visible.** A relevant document that does not fit a budget is
  reported with its size and match reason, never silently dropped.
- **Tools check mechanics; agents judge meaning.** Validation can prove that
  paths resolve and dependencies form a DAG. It cannot decide whether a product
  prompt defines a new project or whether a documented claim is true, so the
  framework never pretends it can.
- **Current truth replaces stale truth.** Active documents describe now; Git
  keeps history. Finished plans and absorbed handoffs are deleted, not
  accumulated.
- **Prune context, not capability.** Reusable guidance stays on disk as
  `dormant` capability and enters context only when a project activates it.

The reasoning is developed further in
[`.agentos-kit/docs/design.md`](.agentos-kit/docs/design.md) and in this
repository's own [decision records](.agentos/decisions).

## Develop AgentOS itself

An AgentOS-specific task does **not** trigger seed adaptation. The master uses
its active `.agentos/` memory and develops the reusable implementation inside
`.agentos-kit/`:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos context "<task>" --path <target>
PYTHONPATH=.agentos-kit/src python3 -m unittest discover -s .agentos-kit/tests -v
PYTHONPATH=.agentos-kit/src python3 -m agentos validate
```

The full framework reference is
[`.agentos-kit/README.md`](.agentos-kit/README.md). AgentOS's own active
development records remain outside the dormant kit and are removed from a new
project's active tree during adaptation.

## Repository structure

```text
AGENTS.md                    dual-use master/seed identity gate
CLAUDE.md, GEMINI.md,        thin vendor adapters pointing at AGENTS.md
.cursor/rules/
.agentos/                    active memory for AgentOS-the-project
  index.json                 knowledge catalog
  project.md, state.md,      current truth
  architecture.md,
  invariants.md
  decisions/                 accepted design decisions
  seed-state.md              unadapted/adapted marker
.agentos-kit/                reusable dormant capability and optional tooling
  ADAPTATION.md              first-prompt adaptation protocol
  CAPABILITIES.md            dormant capability map
  src/agentos/               CLI, starter templates, record templates
  tests/                     unittest suite
  docs/, reviews/            operating guides and review perspectives
  examples/trailcache/       customized example memory
  seed/                      minimal adapted catalog and origin template
  pyproject.toml             installable package metadata
.github/workflows/ci.yml     tests and validation
```

After adaptation, `AGENTS.md` and `.agentos/` become the new project's router and
active memory. `.agentos-kit/` stays local and dormant. The project may evolve
its own information architecture without synchronizing with this master.

## Status

AgentOS is an alpha. The CLI, catalog format, and adaptation protocol are
implemented and tested, and the repository maintains itself with them. Evidence
from real projects beyond this repository and its simulations is still limited;
the open questions are listed honestly in [`.agentos/state.md`](.agentos/state.md).

The project is AI-assisted: it was designed, directed, tested, and iterated by
its creator using coding agents.

MIT licensed.

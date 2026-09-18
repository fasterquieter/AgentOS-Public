# AgentOS: project memory for coding agents

AgentOS keeps the durable project knowledge a coding assistant needs beside the
code, then routes only the useful slice into each task. The complete repository
is also a project seed: a human can clone it, provide an ordinary product prompt,
and let the first agent transform the generic active memory into a project-native
system while retaining this capability kit dormant on disk.

The Markdown memory is the product. The optional zero-dependency CLI helps find, validate, and scaffold it; the CLI does not manage the agent, interpret the first product prompt, or replace its judgment. AgentOS is intentionally not an agent runtime, a vector database, or a giant prompt.

## The idea in one minute

Think of `AGENTS.md` as a small front desk, `.agentos/index.json` as its map,
and the Markdown under `.agentos/` as the project notebook. The front desk does
not hand every visitor the whole archive. It finds the few pages needed for the
job: what matters, what is next, and what evidence supports the claim. The
separate `.agentos-kit/` is a cupboard of optional guides and tools that stays
closed until a real need appears.

```text
AGENTS.md                    tiny, always-visible router
    │
    ▼
.agentos/index.json          human-readable knowledge catalog
    │
    ├── project.md           current product truth
    ├── architecture.md      expensive-to-rediscover system map
    ├── invariants.md        things that must not break
    ├── state.md             now, incomplete, active, next
    └── optional records     plans, decisions, feedback, personas… only when useful

.agentos-kit/                dormant reusable capability; never normal project truth
```

The catalog records why a document is relevant, what authority it has, what it depends on, when it needs review, and how large it may become. An agent can inspect it directly. The optional CLI ranks candidates deterministically and makes size tradeoffs visible:

```console
$ agentos context "fix retries in the photo upload queue" --path src/sync/queue.py
Context recommendations (~1170 selected tokens, budget 2000)
1. .agentos/project.md [baseline; contract/active; change=review] — baseline (~310)
2. .agentos/state.md [baseline; working/active; change=agent] — baseline (~220)
3. .agentos/sync.md [match; evidence/active; change=agent] — task: photo, retries; path: src/sync/queue.py (~420)
4. .agentos/invariants.md [dependency; contract/active; change=review] — required by sync (~220)
```

Every inclusion is explainable. If a relevant candidate does not fit the requested budget, it is reported rather than silently hidden. The agent decides whether to search it selectively, raise the budget, or proceed without it.

`--json` returns `budget`, `selected_tokens`, `selected_over_budget`, `selected`, and `omitted`; omitted entries include an `omission_reason`. This shape makes machine consumers acknowledge incomplete recommendations.

## Quick start: clone plus product prompt

1. Duplicate or clone the complete AgentOS repository.
2. Make that copy the new project's repository.
3. Open it with a capable coding agent.
4. Say: `Read AGENTS.md. I want you to build ...`
5. The agent runs a read-only adaptation preview, protects any changed targets,
   performs the semantic transition, and continues into product work. The human
   does nothing AgentOS-specific.

The inherited root router reads the seed marker and treats a substantive
non-AgentOS specification as the one-time transition trigger. The agent follows
[`ADAPTATION.md`](ADAPTATION.md), replaces AgentOS's active self-project memory,
keeps only earned project memory, and preserves `.agentos-kit/` dormant. No human
installation, terminal command, setup questionnaire, or module selection is part
of this experience.

The older `agentos init` command remains available for a capable agent performing
a conservative installation into an unrelated existing repository, but it is
not the cloned-seed experience. See [bootstrap alternatives](docs/bootstrap.md).

## Daily workflow

Before substantial work, read `AGENTS.md`, use the catalog as a map, and let the task and target paths guide what to open. The finder is useful when the catalog is no longer trivial:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos context "add conflict handling to offline sync" --path src/sync/conflicts.py
```

For work that may cross a session:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos new plan "Conflict handling rollout" \
  --tag sync --tag migration --path 'src/sync/**' \
  --depends-on invariants
```

Keep the plan executable, not diaristic: `Done`, `Now`, `Next`, `Evidence`, `Risks`, and `Resume` are the handoff. At completion, move durable discoveries into current architecture/decision/invariant docs and archive or delete the transient plan.

When branches or agents run concurrently, give each workstream its own plan and
choose one integration owner for shared current truth. See
[`docs/collaboration.md`](docs/collaboration.md). Honor the effective catalog
`change_control` before editing project memory; see
[`docs/governance.md`](docs/governance.md).

After an observed routing miss or noisy inclusion, preserve the failing task as
a local regression case and replay it:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos eval-routing
```

Create other records only when evidence warrants them:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos new decision "Keep the local journal authoritative"
PYTHONPATH=.agentos-kit/src python3 -m agentos new feedback "Entry vanished after tapping save"
PYTHONPATH=.agentos-kit/src python3 -m agentos new failed "Persisting signed URLs as queue identity"
```

Select proportionate perspectives using [the review rubric](reviews/orchestration.md) and state why they apply. A tiny internal rename may need only targeted verification. A persistence rewrite usually needs QA, architecture/craftsmanship, simplification, and knowledge reconciliation; user-facing, security, and performance reviews apply only when the actual change warrants them.

## Knowledge model

AgentOS separates lifecycle from authority:

| Catalog field | Values | Meaning |
|---|---|---|
| `status` | `active`, `draft`, `dormant`, `stale`, `superseded`, `archived` | Whether this record currently applies or is reusable capability excluded from normal routing |
| `authority` | `contract`, `decision`, `evidence`, `working`, `historical` | What kind of claim the record is allowed to make |
| `change_control` | `agent`, `review`, `protected` | Who may accept a change; optional, with conservative defaults |
| `review_after` | ISO date | Freshness signal, not automatic invalidation |
| `read_when` / `tags` / `paths` | triggers | Why a task should retrieve it |
| `depends_on` | stable document IDs | Context that must accompany it |
| `max_tokens` | advisory size budget | Pressure against documentation sprawl |

`contract` does not mean “more correct than evidence.” It means accepted product or safety intent. `evidence` describes what was observed in code, tests, devices, or users. `working` contains plans, questions, and hypotheses that require verification. See [Knowledge model](docs/knowledge-model.md).

Validation also protects the authority/routing boundary of an activated behavior
proof map: `type: "behavior-proof-map"` requires `authority: "evidence"` and may
not be `always` loaded. It deliberately does not judge whether the map is
complete, its oracle is true, or a source control is a semantic behavior.

## What is included

- A small canonical `AGENTS.md` router and non-divergent Claude, Gemini, and Cursor adapters.
- A self-identifying unadapted-seed state and agent-led first-product adaptation protocol.
- A preview-only adaptation transaction report that detects changed target paths
  without pretending to infer project meaning.
- A tiny dormant capability map with later evolutionary activation.
- A validated JSON knowledge catalog with task, path, dependency, freshness, lifecycle, and size metadata.
- An optional zero-dependency CLI for conservative bootstrap, advisory context discovery, hygiene validation, and record creation.
- Lightweight decisions, resumable implementation plans, ephemeral handoffs, open questions, failed-approach guidance, and upstream framework suggestions.
- Optional knowledge governance, explicit parallel-work reconciliation, and
  routing regression cases derived from observed misses.
- QA, UX, accessibility, security/privacy, performance, knowledge-curation, craftsmanship/architecture, and curiosity/simplification review perspectives.
- Synthetic persona and raw-feedback workflows that preserve the distinction between user evidence and causal interpretation.
- A testing evidence ladder that prevents “it compiles” from becoming “it works.”
- An optional progressive behavior proof map that connects important product
  claims to semantic behaviors, routes/states, falsifiable oracles, and actual
  capability/route/environment/human evidence.
- A realistic, partially completed [TrailCache example](examples/trailcache) and documented [continuity simulations](docs/simulations.md).

## Design choices

AgentOS uses an explicit catalog rather than embeddings because the first useful system should be inspectable, portable, offline, and hard to desynchronize. The finder is a convenience, not an authority: semantic relevance remains an agent judgment. Observed routing failures can become deterministic regression cases before semantic retrieval is considered. AgentOS uses source documents rather than generated summaries because every duplicated representation becomes another stale truth. It keeps temporary handoffs inside active plans whenever possible because append-only session logs become a landfill.

These are defaults, not dogma. A very large project can split subsystem docs, add scoped routers, or introduce semantic retrieval after measured failures. Stable IDs and source documents make that evolution possible. The reasoning is in [Why the architecture works](docs/design.md).

## Portability

`AGENTS.md` is canonical. Tool-specific files contain only imports or pointers:

- Codex reads hierarchical `AGENTS.md` files directly.
- Claude Code uses `CLAUDE.md`, which imports `AGENTS.md`.
- Gemini CLI uses `GEMINI.md`, which imports `AGENTS.md`.
- Cursor gets a short always-on rule pointing at `AGENTS.md`; Cursor CLI also recognizes the root file.

The `.agentos/` knowledge system is vendor-neutral. Adapters may add a short, genuinely tool-specific instruction, but project truth must not be copied into them. See [Agent portability](docs/portability.md) and [research notes](docs/research.md).

## Repository map

```text
src/agentos/                 CLI, conservative starter, and record templates
seed/                        minimal adapted catalog and origin template
docs/                        framework rationale and operating guides
reviews/                     reusable specialist perspectives
examples/trailcache/         customized local-first app example
tests/                       standard-library tests
```

## Status

This directory is the dormant kit carried by each cloned project. In the master
repository, contribution instructions live at `../CONTRIBUTING.md`. Its central
contracts are small-router discovery, honest uncertainty, explainable context
recommendations, current-truth hygiene, dormant capability, and vendor-neutral
source documents.

MIT licensed.

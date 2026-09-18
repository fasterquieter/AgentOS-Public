# Continuity simulations

Run: 2026-09-10 against `.agentos-kit/examples/trailcache` and temporary
complete-seed copies. Reproduce from the repository root with:

```sh
PYTHONPATH=.agentos-kit/src python3 -m unittest discover -s .agentos-kit/tests -v
```

The fixture contains 3,002 estimated tokens across 13 indexed documents. Evaluations give the simulated fresh context only the router query and selected recommendations; assertions prevent unrelated knowledge from silently entering the selection. Token estimates use the CLI's deterministic word-based approximation and are comparison signals, not model-specific tokenizer counts.

## Handoff test

Task: `resume photo upload retry work`, target `src/sync/queue.ts`.

Result: 1,644 tokens, seven documents in this order: project, state, active plan, sync map, invariants, decision, failed approach.

From that pack a fresh agent can answer:

| Question | Located in |
|---|---|
| What are we doing? | Plan objective: resume encrypted photo chunks after kill/disconnect |
| Why? | Product offline promise, sync evidence, and device-authoritative decision |
| What happened already? | Plan `Done`, including schema/client/reducer work and 4 MiB deviation |
| What remains? | Plan `Now` and ordered `Next` simulator/review steps |
| What should I read? | Ordered pack with inclusion reasons and explicit dependencies |
| What must not break? | Offline readability, non-destructive sync, idempotency, compatibility invariants |
| Where exactly to resume? | Android expiration callback and named integration test in `Resume` |

The selection is 54.8% of this deliberately compact example's entire indexed memory and stays below the 2,000-token target. In a real repository, source and historical feedback volume would make the relative reduction larger. The budget is an advisory comparison signal; relevant candidates that do not fit must remain visible.

## Task-routing test

Task: `change the journal list empty-state copy`, target `src/journal/EntryList.tsx`.

Result: 1,246 tokens. It retrieves project/state plus the directly relevant save/filter feedback, insight, and two journal personas. It excludes sync architecture, upload failure history, the local-authority decision, invariants, and the active upload plan.

Initial simulation revealed that one generic task word (`journal` or `photo`) could activate an unrelated node even when the target path disagreed. Routing was changed so a concrete path suppresses a weak single-term match; explicit path matches, two-term semantic matches, baselines, and dependencies still apply. A regression test preserves this behavior.

The observed failure now also lives in TrailCache's
`.agentos/routing-evaluations.json`. `agentos eval-routing` replays the original
task and path, asserts the useful journal records remain selected, and asserts
that sync history remains absent. This is the first corpus case; no speculative
examples were added merely to make the benchmark look larger.

## Decision-memory test

Task: `make server absence delete local entries`, target `src/sync/reconcile.ts`.

Result: 1,210 tokens. The accepted device-authoritative decision appears before the sync implementation map and states both the historical destructive failure and why server absence has no deletion meaning. The invariant and failed approach accompany it. A new agent sees the “unintuitive” constraint before implementing the reversal.

## Failed-approach test

Task: `persist signed upload URL and retry credentials`, target `src/sync/queue.ts`.

Result: 1,644 tokens. The pack contains the failed signed-URL approach, its proven cause, retry condition, current plan, and sync state. The record explains that a credential refresh must not create new logical work.

## Persona test

The `distracted-first-run` persona has a scenario, use context, assumptions, and evidence basis. It does not claim demographic truth. Its filtered-save behavior was added from a reviewed insight; its one-handed/low-attention behavior remains explicitly synthetic. The persona runner requires operating the product and separates observed behavior from persona inference. Because the example contains no executable app, this repository validates scenario construction and evidence flow, not an actual UI run.

## Feedback-learning test

Task: `investigate entry disappearing after save under a filter`, target `src/journal/EntryList.tsx`.

Result: 1,246 tokens. The raw frustrated report remains verbatim and distinct from a medium-confidence filter hypothesis. The insight links three reports, separates two causal hypotheses, proposes a UI validation, and records an explicitly accepted persona scenario update. The raw evidence was not rewritten to fit the insight.

## Framework-learning test

Task: `review AgentOS generated code routing proposal`.

Result: the pack includes downstream proposal `upstream-0003`, remains under budget, and the catalog keeps it `draft`. The project proposes exclusion paths with evidence and counterexamples; it does not alter the AgentOS master schema or router automatically.

## Structural and safety tests

Automated tests also cover conservative initialization, a read-only and
deterministic seed-adaptation preview, optional knowledge change control,
preservation of an existing router, path/task/dependency routing, replay of an
observed routing failure, visible oversized candidates, prevention of orphaned
dependencies, invalid dependencies, dependency cycles, catalog paths escaping
the repository, plan section completeness, and validation of both AgentOS and
TrailCache catalogs.

## Mature-project omission regression

Run: 2026-08-26 after inspecting several existing repositories. A temporary
hypothetical catalog used copies of seven real documents from a mature,
document-heavy private application rather than synthetic token padding: the
product contract, current roadmap, visual principles, a subsystem map, a backup
subsystem note, the QA strategy, and one very large (48,226-token) investigation
roadmap. The simulation did not modify that repository, and its contents are not
included here.

With a 5,000-token advisory budget:

| Task | Selected IDs | Visible omitted IDs | Selected tokens |
|---|---|---|---:|
| Subsystem change with a matching source path | project, state | subsystem map | 1,905 |
| Backup import | project, state, backup | none | 4,323 |
| Feature work with a path under the large roadmap's scope | project, state | roadmap | 1,905 |
| Platform regression with a test path | project, state, QA | none | 4,182 |
| List wording with a UI path | project, state, visual | none | 2,604 |
| “Why did a saved object disappear after search?” | project, state | roadmap | 1,905 |

Before the correction, the two oversized primary matches (a 7,346-token
subsystem map and the 48,226-token roadmap) disappeared silently; the roadmap
case could still return its QA dependency. After the correction, each primary
remains visible as an omitted candidate with its match reason and size, and QA
is not selected merely as a prerequisite for an omitted document. This does not
make the 48,226-token roadmap acceptable context. It lets the agent see that it
must search or split the relevant source.

## Complete-clone seed lifecycle

Run: 2026-09-10 against temporary copies of the complete master tree, excluding
only `.git`, caches, and OS metadata. The evaluation harness follows the written
adaptation operations; it is test code, not a production initializer.

### Test A: complex native application

The ordinary product specification describes FieldLens, a native iPhone app for
museum conservators that captures artifact condition offline and synchronizes
later. The adapted copy contains active project, state, architecture, invariants,
one resumable plan, one device-evidence record, and a 137-token behavior proof
map with only two claims: offline capture and reconnect/sync. Its explicit
stateful, physical-service proof obligations earn the map at adaptation; no
action census, route manifest, generated view, feedback, or persona record is
created. An unrelated appearance-label route excludes the proof map. AgentOS's
own project memory disappears from the active tree, while every
`.agentos-kit/` file remains byte-for-byte present.
Validation reports no errors and the project router remains below 120 lines.

### Test B: tiny utility

The ordinary specification describes HashDrop, a one-purpose macOS file-hashing
drop utility with no accounts, sync, network, or history. Active memory contains
only project, state, and the non-baseline capability map. A normal implementation
route selects only project and state—49 estimated tokens in the compact fixture.
The adapted project router adds 439 tokens, so normal orientation is about 488
tokens before source inspection.
No architecture, invariant, plan, persona, feedback, evidence ledger, or
behavior proof map is created. The dormant guide exists on disk and costs zero
normal context.

### Test C: later activation

After HashDrop receives a real beta report, the fresh project router points to
the 656-token capability map, which points directly to the 624-token
feedback/persona guide. The simulated agent creates one active raw-feedback
record. The generic capability library remains `dormant` and is excluded from
subsequent feedback routing. Discovery plus the one guide costs about 1,280
tokens, not the full kit.

### Test D: later proof-map activation

After a HashDrop Finder-drop regression escapes its unit suite, the same tiny
project activates one local Markdown proof map with one claim. It distinguishes
the already-proved hashing capability from the unproved Finder route and states
a falsifiable oracle: exactly one file remains, named by its digest, with
identical bytes. The relevant source path routes the map; it remains non-baseline
and the generic guide remains dormant.

### Test E: fresh-agent handoff

A fresh FieldLens route for `resume offline artifact photo sync` selects project,
state, the active plan, architecture, invariants, the relevant two-claim proof
map, and its device-evidence dependency—413 tokens in the compact fixture. It
contains the literal resume action and no dormant guide. The agent does not need
the adaptation conversation. Including the 439-token adapted router, the
handoff orientation is about 852 tokens.

### Test F: initial context sanity

The complete on-disk kit is about 248 KB in this checkout. Mandatory first-run
reading is only root `AGENTS.md`, the seed state, and the adaptation protocol:
about 2,466 estimated tokens. A complex prompt that immediately justifies a
dormant capability can add the 759-token map, for about 3,225 tokens total. The
presence of tests, examples, reviews, templates, tooling, and all other guides
adds zero normal context unless deliberately opened.

## What the simulations do not prove

- They do not prove every agent will obey the router; instruction following remains probabilistic.
- The seed harness verifies that the written transformation is coherent and
  mechanically valid; it cannot prove every vendor model will interpret every
  future ambiguous product prompt identically.
- Word-based token estimates are not an exact bill for a particular model.
- The example is smaller and cleaner than a mature product, so larger-repository routing needs continued measurement.
- Persona structure is validated, but the nonexistent TrailCache UI cannot supply interaction evidence.
- The behavior-proof evaluation validates activation, authority, routing, and
  lifecycle shape. Its hypothetical products have no implementation, so every
  claim correctly remains unproved.
- Documentation truth still requires source, test, environment, user, or human-product evidence; deterministic validation proves structure only.

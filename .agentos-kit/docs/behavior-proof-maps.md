# Behavior proof maps

A behavior proof map is an optional account of the consequential claims a product
makes and the evidence that does—or does not—prove them. It answers a question a
test list cannot: **which important user-visible behaviors are we claiming, through
which routes and states, with what discriminating oracle, and what remains
unproved?**

AgentOS uses *behavior proof map* for the reusable concept and *proof map* as a
convenient local short form. A mature project may keep an established name such as
behavior ledger. Names matter less than preserving the authority and evidence
boundaries below.

## Authority

A proof map is evidence accounting, not product contract authority.

- Product contracts and accepted invariants own what the product promises.
- Source and deployed/runtime state provide implementation evidence.
- Tests and observations prove only the claims they actually discriminate.
- The proof map connects those layers and exposes missing or stale proof.

Index an active proof map with `type: "behavior-proof-map"` and `authority:
"evidence"`. Never mark it `always`; route it by behavior, risk, and affected source
or test paths. Add relevant contract or invariant records as dependencies when they
are not already baseline context.

When contract, source, observation, executable evidence, and the map disagree, the
disagreement is a finding to investigate. Do not silently make the implementation
match the map. Correct the map when its row is false; change product intent only
through its actual authority.

## Smallest useful form

Start with one Markdown file and only the few claims whose proof is expensive to
reconstruct. Stable claim IDs help tests, plans, and commits refer to a claim without
copying it.

```markdown
# Behavior proof map

Verified: 2026-09-10 against contract, source, and cited evidence.

## Authority

Evidence accounting only. Product promises live in project.md and invariants.md.

## Claims

### B-01 — Save an entry offline

- Promise: `project.md#local-first`.
- Behavior: saving creates one durable entry without a network connection.
- Routes/states: editor Save; offline; first save and retry after interruption.
- Oracle: exactly one entry with the submitted fields exists after relaunch; no
  success state appears before the durable write.
- Capability evidence: `tests/test_entries.py::test_offline_save` — passed on the
  current commit.
- Route evidence: unproved; the editor button has not been driven.
- Environment evidence: offline simulator only; physical device not run.
- Human evidence: not applicable to persistence; success copy not reviewed.
- Recheck: after storage migration or OS networking changes.
```

The claim is the semantic behavior, not every control that can reach it. Add a route
when a person or external system has a materially distinct door to the same behavior.
Do not turn several labels for the same operation into several claims. Conversely,
keep operations separate when their consequences differ: forgiving delete,
delete-with-contents, removing a list reference, and permanent deletion are not one
behavior merely because their controls all say Delete.

References should identify existing tests, commands, reports, commits, devices, or
artifacts. The map says what each reference proves and what it does not; it does not
repeat the suite's setup documentation or store raw output.

## Evidence axes

Keep these axes separate whenever they are material:

| Axis | Question | A common overclaim |
|---|---|---|
| Capability | Does executable evidence discriminate the underlying semantic outcome? | A function was called, but its consequential state was not asserted |
| Route | Did the actual UI, URL, intent, API, import, or system door reach that capability and report truthfully? | A unit test for the core is treated as proof of the button |
| Environment | Was the required device, OS, browser, network, service, migration source, scale, or deployment exercised? | A simulator or fake service silently stands in for hardware or production |
| Human | Was comprehension, usability, accessibility flow, motion, or taste judged by a person when the claim requires it? | An agent screenshot inspection is called human evidence |

Use `proved`, `partial`, `unproved`, or `not applicable` only beside the evidence or
reason that earns the state. A bare adjective is not accounting. A project may add
closed vocabularies later when queries or multiple writers justify them.

Evidence freshness matters when the subject can move independently of the code:
physical devices, OS/platform behavior, third-party APIs, production configuration,
network conditions, migrations from old data, and performance at representative
scale. Record the observation date, environment/version, and a concrete recheck
trigger. Old evidence remains historical evidence; it must not silently continue to
prove the current environment. Use the catalog's `review_after` for whole-document
hygiene and claim-local triggers for volatile evidence.

## Oracles

An oracle must distinguish the broken system from the working one. State the
consequential postcondition and, where useful, the important non-change. Common
high-value shapes are:

- **representation consistency:** every representation of one user fact agrees;
- **absence:** a destructive act proves the subject is gone everywhere it must be,
  not merely from the edited screen;
- **identity:** an edit preserves stable identity, relationships, ordering, or other
  facts it is not supposed to replace;
- **recovery:** restore or undo has its own semantics and is not assumed to be the
  implementation inverse;
- **unchanged state:** unrelated records, counts, permissions, or artifacts remain
  untouched;
- **two-sided authorization/failure:** prove both what is withheld on denial and what
  remains available after authorization or retry;
- **structural/performance bounds:** state a work-count or measured bound at a named
  scale rather than saying “fast.”

Test the oracle itself when feasible: introduce a bounded fault and confirm the
named assertion fails. If a deliberate fault stays green, strengthen or correct the
oracle rather than counting the existing test.

## When to activate

Do not create a proof map because AgentOS supports one. Activate it when at least one
of these signals makes the accounting independently useful:

- a consequential regression escaped green tests and the missing proof link should
  be remembered;
- one semantic behavior is exposed through several routes or surfaces that can
  diverge;
- destructive/recovery, persistence, migration, offline/sync, concurrency, or other
  important sequences share state;
- hardware, platform, third-party, performance, authorization, or human evidence is
  required and cannot be substituted honestly;
- agents repeatedly cannot answer which important behavior remains unproved;
- the product is mature enough that a bounded behavior census is cheaper than
  repeated rediscovery.

At seed adaptation, create one only when the initial specification already contains
multiple consequential stateful claims, materially different routes/environments,
or explicit verification obligations that deserve durable accounting. A tiny utility
with one obvious path starts without one. Project size, file count, or framework
availability alone never triggers activation; the agent makes the semantic judgment
from product and defect evidence.

## How it evolves

Grow the representation only after the current form produces a concrete maintenance
or query problem:

1. **Few claims:** one short Markdown file with claim, route/state, oracle, evidence,
   and gap lines.
2. **Repeated routes or risky state:** stable behavior and route IDs; selected
   transitions for shared state, recovery, persistence, async boundaries, or known
   failures. Do not create the Cartesian product of all actions.
3. **Complex fixtures or environments:** shared fixture/evidence references and
   explicit capability/route/environment/human axes.
4. **Mature finite census:** split independently routed domains, add structured
   records, queries, generated views, and drift checks only when several agents or
   surfaces make manual reconciliation unreliable.

A finite census becomes worthwhile when the consequential action set is reasonably
stable, omissions have escaped more than once, multiple routes or environments must
be compared, and the team needs repeatable gap queries. This is an agent/human
judgment guided by evidence. A script can identify source constructs not yet reviewed;
it cannot decide whether a button is a new semantic behavior, another route, internal
implementation, or decoration.

## Important sequences

Record an edge only when the sequence carries a claim that isolated actions cannot:
shared mutable state, recovery, identity, asynchronous work, persistence/relaunch,
cross-surface agreement, failure/retry, a product invariant, or a sequence that has
failed before. Examples include delete → restore, move → undo, pack → move → put back,
offline edit → reconnect, permission denied → retry, and migration → subsequent edit.

Each selected sequence needs its own oracle and evidence. “A passes” plus “B passes”
does not prove “A then B.”

## Escaped-regression loop

For a bug that escaped existing evidence:

1. Preserve the smallest reproducer and identify the violated contract/invariant.
2. Locate the failed link: missing behavior, route/state, transition, fixture or
   environment, discriminating oracle, evidence attachment, or freshness claim.
3. Fix the smallest owning implementation layer and add proportionate regression
   evidence.
4. Reconcile the proof map in the same coherent change. Record only the evidence axis
   actually earned.
5. If the map or oracle was wrong, correct it explicitly. Do not weaken an oracle to
   make the implementation green and do not repair code to satisfy false prose.
6. Check nearby routes, representations, and sequences for the same class of gap.
7. Update contract, invariants, architecture, or test strategy only if their own
   authority changed; let Git or a bounded finding retain the bug's history.

The verification model should learn from the escape, not merely gain another test.

## Boundaries with other project memory

| Owner | Keeps | Proof map behavior |
|---|---|---|
| Product contract / invariants | Accepted promises and must-not-break rules | Links to the owning statement; never redefines it |
| Architecture | Components, seams, data flow, implementation authorities | Names only the seam needed to verify or route a claim |
| Testing/QA strategy | Evidence levels, selection, cadence, release gates | Applies the strategy to specific behavioral claims |
| Plan / current state | Work now, next steps, blockers | Links to proof gaps being changed; no permanent coverage matrix |
| Bug history / findings | Reproducer, diagnosis, historical explanation | Absorbs the durable proof lesson; Git keeps ordinary chronology |
| Raw evidence | Reports, logs, screenshots, measurements, device artifacts | Cites exact artifacts and limits without copying them |

If the proof map mostly repeats one of these owners, merge or delete the duplicate.

## Deterministic helpers

AgentOS core checks only two proof-map-specific mechanics: an indexed
`behavior-proof-map` must have `authority: "evidence"` and must not be always-loaded.
Existing validation also checks its path, catalog fields, local Markdown links,
dependencies, size, and review date.

A mature structured map may earn project-local checks for unique IDs, closed
vocabularies, resolved references, evidence-level/axis compatibility, source-pointer
existence, generated-view synchronization, and candidate source drift. Keep these
checks deterministic and deliberately falsify them before trusting them.

No deterministic helper may decide that an arbitrary source construct is a semantic
behavior, that the census is complete, that an oracle describes the right product, or
that cited evidence actually discriminates the claim. Those require source, contract,
evidence, and often human comparison.

## Routing and maintenance

Give a small map task terms such as behavior, regression, route, transition, oracle,
coverage, and the named risky domains. Give it paths only for the product/test seams it
accounts for. A large map should split by independently useful domain before it becomes
always-loaded or exceeds routine context budgets.

Review the relevant claims when behavior, routes, or evidence change; when an escaped
bug exposes a proof gap; when a cited environment moves; and at meaningful release
boundaries. During curation, sample high-risk oracles against contract, source, and
executable evidence independently. A mechanically valid map can still be semantically
false, and a stale proof map is more dangerous than no map because agents will rely on
it.

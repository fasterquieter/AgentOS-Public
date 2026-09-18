# Knowledge model

The catalog is the canonical inventory and a human-readable discovery map. A document not indexed there is invisible to the optional finder and will be flagged by validation; a capable agent may still read it when repository evidence makes it relevant.

Each active document should have one useful job. If two records claim the same
job, merge them or name the authority boundary that makes both necessary.

## Catalog entry

```json
{
  "id": "sync",
  "path": ".agentos/sync.md",
  "title": "Offline synchronization",
  "type": "subsystem",
  "authority": "evidence",
  "status": "active",
  "change_control": "agent",
  "tags": ["sync", "offline", "conflict", "queue"],
  "read_when": ["changing retry, merge, or upload behavior"],
  "paths": ["src/sync/**", "tests/sync/**"],
  "depends_on": ["architecture", "invariants", "decision-0004"],
  "review_after": "2026-11-30",
  "max_tokens": 1400
}
```

IDs are stable references and should survive file renames. Paths are repository-relative. Task descriptions should be concrete enough to overlap with how a user naturally asks for work. Globs route target files. Dependencies express conceptual prerequisites, not every hyperlink.

## Authority

| Value | May assert | Must not silently become |
|---|---|---|
| `contract` | Accepted product, safety, compatibility, or invariant intent | An inferred requirement |
| `decision` | A deliberate choice, rationale, alternatives, consequences | A claim that implementation matches it |
| `evidence` | Observed code, test, environment, device, or user behavior | Product intent or causal certainty |
| `working` | Plans, hypotheses, open questions, handoffs, proposals | Durable fact without verification/promotion |
| `historical` | Superseded context useful for explanation | Current guidance |

Within a document, label meaningful uncertainty in prose: `Unknown`, `Hypothesis`, `Verified`, or `Accepted`. Avoid a label on every sentence; use it at a claim boundary where an agent could otherwise act incorrectly.

## Change control

Authority describes what a document may claim. The optional `change_control`
field describes who may accept an edit:

- `agent`: an agent may keep it current within the authorized task;
- `review`: an agent may propose a patch, but a human or delegated owner accepts
  the new authoritative claim;
- `protected`: explicit user authorization for that document or policy change is
  required.

When omitted, contract and decision records default to `review`; evidence,
working, and historical records default to `agent`. The old policy governs a
policy-changing edit. See [Knowledge change control](governance.md).

## Lifecycle

- `draft`: proposed or incomplete and safe to challenge.
- `active`: currently applies within its stated authority.
- `dormant`: reusable capability retained locally but not normal project context;
  consult it only through the capability map and activate a project-specific
  adaptation rather than making generic guidance project truth.
- `stale`: potentially useful but must be verified before reliance.
- `superseded`: replaced by a named newer record; retained only when rationale is valuable.
- `archived`: not part of current routing.

Normal routing considers `active` and `draft` records. It excludes `dormant`,
`stale`, `superseded`, and `archived` material unless an agent deliberately
inspects it. When an accepted decision changes, add a new decision that names the
old one, mark the old record `superseded`, and update dependents. Do not rewrite
the old rationale as if the earlier decision never existed.

## Knowledge types

Every cloned-seed project begins with only project, state, the tiny capability
map, and the dormant library record. Architecture, invariants, questions, and
every optional knowledge type are activated only when the specification or
later evidence makes them independently useful.

Create optional types when their trigger occurs:

| Type | Create when | Remove, merge, or archive when |
|---|---|---|
| Subsystem map | A boundary/data flow is repeatedly expensive to reconstruct | It becomes obvious from code or overlaps architecture |
| Decision | A significant, counterintuitive, or costly choice is accepted | Never delete accepted rationale casually; supersede it |
| Failed approach | A tempting approach failed and recurrence would be costly | Constraint disappears or lesson is absorbed by a decision |
| Behavior proof map | Consequential behaviors, routes/states, or evidence gaps are repeatedly expensive to account for | The map duplicates contract/test strategy, becomes cheaper to reconstruct, or splits into independently routed domains |
| Plan | Work may outlive the current context/session | Completed knowledge is promoted and plan has no live value |
| Handoff | Transfer state does not fit an active plan | Recipient absorbs it or work closes |
| Persona | A meaningful behavior/use context needs exploratory testing | It stops representing evidence or a useful risk |
| Raw feedback | A real user's experience is reported | Preserve as evidence subject to privacy/retention policy |
| Feedback insight | Multiple reports or strong evidence support a pattern | Refuted, resolved, or merged with a stronger insight |
| Upstream suggestion | A local lesson plausibly improves all AgentOS projects | Accepted upstream, rejected with reason, or proven local-only |

A behavior proof map is an `evidence` record, never `contract`: it links accepted
promises and observed implementation to the evidence that proves particular
behavioral claims. See [Behavior proof maps](behavior-proof-maps.md). Do not add
one to the starter set; activate it only when consequential route, state,
transition, environment, or escaped-regression evidence makes the accounting
independently useful.

## Freshness

`review_after` is a prompt to verify, not an expiry date. Choose an interval based on volatility:

- active implementation state: days or weeks;
- subsystem maps: one to three months or after boundary changes;
- product contracts and invariants: quarterly or after product decisions;
- accepted ADR rationale: long intervals, revisited by named evidence;
- raw feedback: no truth-expiry, but privacy retention may apply.

Validation warns when active material is overdue. The curator either verifies and advances the date, updates it, marks it stale, supersedes it, archives it, or deletes it.

## Size and splitting

Set `max_tokens` to the amount that is usually reasonable to add to one focused task. It is a size signal, not permission to hide a relevant source. The finder reports matched candidates that exceed the requested context budget so the agent can search them selectively. Split a document only when readers regularly need different parts independently and routing can distinguish them. Merge documents when they share triggers, repeat context, or are usually loaded together. A deep directory tree is not evidence of good information architecture.

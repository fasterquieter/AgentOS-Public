# Why the architecture works

AgentOS treats continuity as an information-architecture problem, not a prompt-writing problem. A new model does not need the previous model's internal state; it needs a trustworthy route to the intent, constraints, reasoning, current work, and evidence that are expensive to reconstruct.

In plain language, the design test is:

1. write down what is expensive to forget;
2. label promises, decisions, evidence, and uncertainty honestly;
3. show each task only the useful slice; and
4. keep the memory system smaller than the confusion it prevents.

## Active memory and dormant capability have different jobs

The complete clone keeps reusable AgentOS guidance and tooling under
`.agentos-kit/`. That directory is deliberately cheap on disk and expensive only
if read, so ordinary agents must not browse it. Root `AGENTS.md` points to the
tiny capability map only when active project memory does not cover a newly
encountered need. Detailed generic guides remain `dormant`; activation creates a
project-specific active record.

In the master repository, `.agentos/` describes AgentOS itself. In an unadapted
clone, a non-AgentOS product specification triggers replacement of that active
layer while preserving the kit. This semantic decision belongs to the agent
reading the prompt. Deterministic validation checks the resulting state but does
not classify the product.

### The router is for universal behavior

`AGENTS.md` is likely to enter every agent context, so every sentence has rent. It contains the project identity, rules that always matter, a pointer to the catalog, context-selection instructions, and closeout obligations. Putting architecture history, every command, or every role here would penalize unrelated tasks and reduce instruction adherence.

Nested routers are appropriate only when a directory has durable local rules that differ from the root. A subsystem's explanatory map still belongs in an indexed document; behavioral constraints close to the code may belong in a scoped `AGENTS.md`.

### The catalog is for discovery

`.agentos/index.json` is a small explicit graph. Each node answers:

- What is this document?
- Under which task words or target paths is it useful?
- What must be read with it?
- What kind of authority does it carry?
- Who may turn a proposed edit into current knowledge?
- Is it active, tentative, stale, or historical?
- When should it be reviewed?
- How large may it grow before it needs editing or splitting?

Separating routing metadata from prose makes candidate discovery cheap without creating generated summaries. JSON is deliberately boring: every language and coding agent can inspect it, deterministic validation is straightforward, and the CLI needs no YAML dependency. The catalog is also a readable map when the CLI is unavailable.

### Documents are for durable knowledge

Documents contain only facts that are expensive to rediscover from source, decisions whose rationale prevents reversals, explicit uncertainty, and work state needed for resumption. Code remains the best description of ordinary implementation detail. Git remains the history of old documentation. The active tree should say what is true now.

An optional behavior proof map fills one specific gap between product intent and
test evidence: it accounts for consequential semantic behaviors, meaningful
routes/states, discriminating oracles, and the evidence each claim has actually
earned. It is an `evidence` document, not a second contract or test strategy, and
it stays dormant until route, state, environment, or escaped-regression complexity
makes the accounting cheaper than rediscovery.

## Retrieval is simple and advisory on purpose

The router uses a union of three signals:

1. baseline documents marked `always`;
2. task-term overlap with titles, tags, and `read_when` descriptions;
3. path-glob matches against files likely to change.

It then expands explicit `depends_on` edges and applies an advisory token budget. The result includes reasons, roles, estimated size, and every relevant candidate omitted by the budget. A capable agent decides whether to search an oversized source selectively, raise the budget, or proceed without it. The finder must never imply that an omission makes a source irrelevant.

This is less magical than embeddings and correspondingly easier to debug: a missed document means its trigger or dependency is wrong, not that an opaque similarity threshold drifted. It is still only a lexical/path finder. A concise Markdown map and agent judgment remain the primary fallback and may outperform it on unfamiliar vocabulary or unusually large documents.

### Routing failures become regression cases

When a real task misses an important document, reports it only as an unusable
budget omission, or repeatedly selects distracting context, a project may
capture that observation in `.agentos/routing-evaluations.json`:

```json
{
  "schema_version": 1,
  "cases": [
    {
      "id": "miss-2026-09-10-upload-recovery",
      "origin": "Upload retry work omitted the signed-URL failed approach.",
      "task": "repair resumable photo upload retries",
      "paths": ["src/sync/queue.ts"],
      "budget": 2000,
      "expect_selected": ["failed-0001", "sync"],
      "expect_absent": ["persona-screen-reader"]
    }
  ]
}
```

Run `agentos eval-routing`. The runner replays the normal deterministic router
and fails when expected selections, visible omissions, or exclusions change.
`expect_omitted` is also available for a deliberately visible budget omission.
Every case requires an `origin` describing the observed failure. This is a
local regression corpus, not a speculative relevance specification and not a
training-data collector.

Semantic retrieval becomes justified only when representative task-routing failures persist after catalog hygiene and subsystem splitting. If added later, it should propose catalog nodes rather than synthesize another truth layer.

## Continuity without a session diary

The active implementation plan is the default handoff. Its stable sections force the minimum information another agent needs: objective, completed state, current action, ordered remainder, evidence, risks, and one explicit resume instruction. Discoveries either change the plan while work is live or get promoted into permanent knowledge.

A separate handoff is useful when an investigation or external coordination does not fit a plan. It is intentionally disposable. Completed handoffs are not a project archive; Git can recover them.

## Honest authority

Confidence numbers look precise but mix several questions: who decided this, what evidence supports it, and whether it is current. AgentOS uses two orthogonal fields instead:

- `authority` names the epistemic role: contract, decision, evidence, working, or historical;
- `status` names lifecycle: active, draft, dormant, stale, superseded, or archived.
- `change_control` optionally names who may accept a change: agent, review, or
  protected. Without it, contract/decision default to review and other
  authorities to agent maintenance.

A draft contract is proposed intent. Active evidence is a verified observation. An active decision can intentionally constrain an implementation even when another design looks fashionable. A stale evidence record is a verification task, not automatically false.

Change control governs mutation, not truth. A protected document can still be
wrong, and an agent-maintained evidence note cannot redefine product intent.
The policy in force before an edit governs that edit, so an agent cannot grant
itself permission by weakening the field first.

## Deterministic checks and judgment

Scripts are good at broken paths, unknown dependencies, duplicate IDs, oversized routers, overdue reviews, and incomplete plan structure. They are bad at deciding whether an architecture description is honest, whether feedback clusters reveal a real user pattern, which review perspective is warranted, or whether a refactor is worth its blast radius.

The same boundary applies to behavior proof maps. Core validation can prevent one
from claiming contract authority or entering every task, and a mature project may
check references or evidence-level compatibility. No script can decide whether a
source control represents a new semantic behavior or whether an oracle states the
right product outcome.

AgentOS therefore automates mechanics and provides Markdown review perspectives for agent judgment. The executable layer is optional: losing it must reduce convenience, not make the memory unintelligible. AgentOS does not pretend an LLM conclusion is a deterministic check or that a deterministic candidate list is complete semantic context.

## Designed to shrink

The framework has explicit deletion pressure:

- replace current truth instead of appending updates;
- resolve and remove open questions;
- archive or delete finished plans and handoffs after promotion;
- merge overlapping documents before adding a new category;
- keep failed approaches only when repetition would be costly;
- keep raw feedback because it is evidence, but consolidate interpretations into revisable insights;
- instantiate optional modules only after a real need appears.

This is what makes long-lived memory different from long-lived clutter.

## Parallel branches converge explicitly

AgentOS remains repository memory rather than a scheduler. Parallel workers own
their branch-local plans and evidence; one integration owner reconciles shared
current truth after source and tests merge. `state.md` is rewritten from the
combined repository instead of line-merged, while incompatible contract or
decision edits remain proposals until their change-control owner resolves them.
The detailed sequence lives in `collaboration.md` and requires no lock service.

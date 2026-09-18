# Operating workflows

## Start a task

1. Inspect git state.
2. Read the root router and inspect the catalog's plain-language triggers. When useful, run `agentos context` with the objective and likely target paths.
3. Read relevant recommendations in order, inspect any omitted candidates selectively, and verify working/stale claims against code or tests.
4. If an active behavior proof map covers the area, read only its relevant claims
   and treat its coverage as evidence accounting rather than product authority.
5. Decide whether the work fits the current session. Create a plan only when continuity risk is real.
6. Classify the actual change and select proportionate review perspectives using `.agentos-kit/reviews/orchestration.md`; state why each applies.

If routing misses an important document or repeatedly includes noise, read the
right context for the task, fix the catalog trigger or dependency during
closeout, and consider preserving the observed failure as a routing evaluation.
Do not invent evaluation cases merely to increase a test count. The finder
recommends candidates; it does not overrule agent judgment.

If the task introduces a class of need absent from active memory, consult
`.agentos-kit/CAPABILITIES.md`, then one relevant dormant guide. Adapt only the
project-specific piece and index that piece as active; never activate the generic
guide itself. This is an evolution of the project, not a reinstall.

## Maintain a resumable plan

The plan is a state machine, not a transcript:

- `Objective`: stable outcome and acceptance evidence.
- `Done`: completed facts only; mention important deviations.
- `Now`: one bounded current action.
- `Next`: ordered executable remainder.
- `Evidence`: exact checks, environments, and results.
- `Risks`: unresolved uncertainty, blockers, and traps.
- `Resume`: one instruction a fresh agent can execute immediately.

Update after a meaningful state transition or before context exhaustion. Do not append time-stamped narration. Rewrite sections so they describe the current handoff state.

When complete, promote decisions, architecture discoveries, invariants, vocabulary, or failed approaches. Remove the active plan from routing; archive it only if its implementation history remains unusually valuable, otherwise delete it.

## Record a decision

Create a decision when the choice is architecturally significant, product-defining, counterintuitive, hard to reverse, or likely to be “improved” back into a rejected alternative. Include context, the decision, real alternatives, consequences, and concrete revisit evidence.

Implementation details with an obvious local answer do not need ADRs. A decision's status can be proposed, accepted, superseded, or rejected; the catalog lifecycle should agree.

## Record a failed approach

Keep the failed attempt concise:

- what was tried;
- observable result;
- why it failed, clearly separating proven cause from hypothesis;
- the durable condition that makes retrying unwise;
- what evidence would make it worth retrying.

Failed approaches are exception memory, not a bug diary.

## Leave a handoff

Prefer updating an active plan. Use a separate handoff for an investigation, incident, or coordination state that cannot cleanly live there. Capture objective, current state, discoveries, touched areas, evidence, next action, blockers, and traps. Never use “look at the conversation” as a resume step.

The receiving agent should absorb durable material and delete/archive the handoff. Validation may flag old active handoffs through `review_after`.

## Reconcile parallel work

When several agents, branches, or worktrees are active, read
`collaboration.md`. Give each workstream its own plan and choose one integration
owner for shared `state.md`, architecture, invariants, and catalog truth. Merge
behavior and evidence first, then rewrite shared current memory from the merged
repository. A text conflict between product promises is a decision for the
authorized owner, not a “keep both” merge.

## Close a task

1. Run evidence proportional to claims.
2. Run only relevant review perspectives.
3. Reconcile current truth in place.
4. Resolve questions or promote meaningful answers.
5. Fix catalog triggers discovered during work. If the failure is likely to
   recur, add an observed case to the project's routing evaluation file and run
   `agentos eval-routing`.
6. When a behavior or route changed—or a regression escaped existing evidence—
   reconcile the relevant proof-map claim and the failed link in its proof chain.
7. Run `agentos validate`.
8. If unfinished, make the plan independently resumable.

Before editing routed knowledge, honor its effective `change_control`. The
defaults allow agent maintenance of working/evidence records and require review
for contract/decision changes. Read `governance.md` when a project needs named
owners or stricter protection.

No documentation update is required when the change teaches the project nothing durable and current docs remain accurate.

## Periodic curation

Run after meaningful release boundaries or when agents repeatedly encounter stale/duplicated context:

- validate links, budgets, dates, and active plans;
- compare architecture and commands with repository evidence;
- merge overlapping context nodes;
- remove resolved questions and absorbed handoffs;
- review accepted decisions whose revisit evidence has occurred;
- synthesize feedback patterns and deliberately evolve personas;
- review downstream upstream-suggestions across projects;
- produce prioritized findings rather than autonomously rewriting stable code.

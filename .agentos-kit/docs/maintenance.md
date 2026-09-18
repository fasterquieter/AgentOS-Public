# Knowledge hygiene and framework evolution

## Curator questions

For each active node, ask:

- Does it still describe current reality within its authority?
- Would source code communicate this more cheaply?
- Is its `read_when` specific enough for a task to find it?
- Does it duplicate another node that is usually read alongside it?
- Has a working hypothesis quietly become “fact” without evidence?
- Has an accepted decision been implemented, violated, or made obsolete?
- Does the effective `change_control` still match the project's real ownership
  and review practice?
- Did a context miss or noisy inclusion recur without becoming a routing
  evaluation?
- Can history be deleted because Git already preserves it?

## Create, split, merge, archive, delete

Create when a recurring information need is expensive to reconstruct and independently routable. Split when tasks repeatedly need different sections and those sections have distinct triggers. Merge when nodes repeat prerequisites or always travel together. Archive only when historical context has real explanatory value. Delete absorbed plans, handoffs, resolved questions, obsolete summaries, and low-value historical detail.

Good institutional memory includes deliberate forgetting. Git keeps ordinary
history; the active tree should keep the present knowledge that still earns an
agent's attention.

Prefer a smaller catalog with high-quality triggers over fine-grained document fragmentation.

Routing evaluations should remain a small fossil record of actual failures.
Delete cases whose source documents or task class no longer exist; do not keep a
large speculative relevance suite merely because it is executable.

## Dormant capability versus archive

`dormant` is reusable generic capability that has not become project truth.
`archived` is project-specific knowledge that used to matter and retains unusual
explanatory value. Do not archive AgentOS self-history during seed adaptation;
delete it from the active project tree because Git already preserves it. Do not
delete dormant capability merely to reduce file count; prune what enters context.

When a need appears, read the capability map and one guide, create the minimum
project-specific active memory, and leave the generic guide dormant. Projects may
later evolve or remove their own adapted convention without upgrading from the
AgentOS master.

## Staleness response

An overdue `review_after` warning requires one of five actions:

1. verify and advance the date;
2. correct current truth;
3. mark `stale` and require verification before use;
4. supersede/archive with an explicit successor;
5. delete because the knowledge no longer earns its maintenance cost.

Never advance dates mechanically without checking evidence.

## Project versus framework evolution

Projects may freely improve their own AgentOS structure: add a subsystem, retire irrelevant personas, change routes, or define a project-specific reviewer. A lesson that seems general goes to `.agentos/upstream/` with evidence, generality, a suggested change, and counterexamples.

The downstream project does not automatically edit the master framework. Periodic framework review compares proposals across projects, accepts or rejects them deliberately, and may offer a backport/migration. This prevents one project's accidental complexity from becoming global boilerplate.

## Periodic holistic review

Use only relevant passes, typically at releases, after several large iterations, or when signals show drift:

- architecture health and dependency direction;
- accidental complexity and simplification opportunities;
- test-suite signal, gaps, and flakiness;
- active behavior proof maps sampled against contract, source, and executable
  evidence, with volatile environment claims downgraded when stale;
- UX vocabulary and journey coherence;
- feedback/persona synthesis;
- documentation accuracy and token budgets;
- dependency, security, privacy, performance, or compatibility health where material.

Output prioritized findings. Each finding should state `must fix`, `should fix`, `worthwhile eventually`, `speculative`, or `leave alone`, plus impact, risk, effort, confidence, evidence, and suggested next action. A review that finds a coherent area should say to leave it alone.

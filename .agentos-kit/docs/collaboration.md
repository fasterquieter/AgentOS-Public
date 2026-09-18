# Parallel work and memory reconciliation

AgentOS does not schedule agents, lock files, or merge branches. It defines a
small convergence rule for projects that already use branches or worktrees:

> Each workstream owns its temporary plan. One integration pass owns shared
> current truth.

## Before parallel work

Choose an integration owner: a person or agent responsible for the final merge.
Create one plan per workstream when continuity risk warrants it. Add a compact
coordination block only for concurrent work:

```markdown
## Coordination

- Workstream: upload-retry
- Base revision: 7d91c2a
- Integration owner: main-worktree
- Shared knowledge likely to change: architecture, state, decision-0012
```

Workers may update their own plans, findings, and branch-local evidence. Avoid
opportunistic edits to shared baseline documents such as `project.md`,
`state.md`, architecture, or invariants when a workstream-local record can carry
the discovery safely to integration. Honor each document's `change_control`.

## What belongs on a worker branch

- implementation and tests for that workstream;
- its own current plan and exact evidence;
- a proposed decision or contract change when the work reveals one;
- a short integration finding when shared current truth must change.

Do not copy the whole project state into every plan. Do not make a branch look
globally complete merely because its local task is complete.

## Integration order

The integration owner reconciles in this order:

1. Merge source and tests, resolving behavior before prose.
2. Run the evidence appropriate to the combined result.
3. Review proposed contract and decision changes under their change-control
   policies. Supersede accepted decisions instead of blending incompatible
   rationales.
4. Rewrite shared `state.md` from the merged repository. Do not resolve a state
   conflict by keeping both branches' “Now” sections.
5. Reconcile architecture, invariants, proof maps, and the catalog against the
   merged behavior and evidence.
6. Archive or delete absorbed workstream plans and findings.
7. Run `agentos validate` and any project routing evaluations.

If two workstreams changed the same product promise or invariant differently,
that is a product decision, not a text merge. Keep both proposals visible and
ask the authorized owner. If evidence conflicts, preserve the environments and
methods until the disagreement is explained.

## Failure and abandonment

An abandoned workstream leaves no claim in shared current truth. Preserve a
failed-approach note only when the failure is likely to be repeated and the
evidence is durable. Otherwise Git keeps the branch history.

This model deliberately has no central lock service. Projects that need live
coordination can add one, but repository memory should still converge through a
single reviewed integration state.

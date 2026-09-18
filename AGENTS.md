# AgentOS master and project-seed router

This repository is both the AgentOS framework project and a complete seed for a
different project. Resolve that identity before loading project context.

## Identity gate — do this first

Read `.agentos/seed-state.md`.

- If the user's substantive objective is to build or maintain **AgentOS itself**,
  this is the master framework checkout. Follow **Master mode** below.
- If the seed is `unadapted` and the user supplies a substantive specification
  for **any other product**, that ordinary product prompt triggers the one-time
  `.agentos-kit/ADAPTATION.md` protocol. Do not ask the user to initialize
  AgentOS, choose modules, run commands, or restate the prompt. Adapt the clone,
  then continue into product work in the same task.
- Housekeeping with no new product specification does not trigger adaptation.

The task subject is decisive. Directory name, inherited Git history, and a
copied AgentOS remote do not make a non-AgentOS product into AgentOS work.
Before resolving the gate, do not read the current `.agentos/` tree, framework
history, examples, or `.agentos-kit/` beyond the adaptation file it names.

## Master mode

AgentOS is Markdown-first institutional memory plus optional deterministic
helpers. It is not an agent runtime or a documentation dump.

### Always

- Inspect Git state before editing and preserve unrelated work.
- Keep root `AGENTS.md` a router; durable detail belongs in indexed memory.
- Honor effective catalog `change_control`; an agent cannot weaken a governing
  policy to authorize its own edit.
- Preserve `.agentos/invariants.md`.
- Separate observed evidence, accepted decisions, working hypotheses, and
  history.
- Never claim behavior from compilation alone.
- Replace obsolete current truth instead of appending another version.
- Treat `.agentos-kit/` as reusable framework source, not AgentOS project state.

### Find context

Inspect `.agentos/index.json`. The optional local finder is:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos context "<task>" --path <target-path>
```

Treat its result as recommendations. Read relevant documents in order, inspect
reported omissions selectively, and never read the full memory or capability kit
by default.

### Development

- Runtime: Python 3.10+, standard library only.
- Tests: `PYTHONPATH=.agentos-kit/src python3 -m unittest discover -s .agentos-kit/tests -v`.
- Validate: `PYTHONPATH=.agentos-kit/src python3 -m agentos validate`.
- Public behavior changes require tests and README/help reconciliation.
- Seed changes require complex, tiny, later-activation, fresh-handoff, and context
  evaluations.

### Closeout

- Update an active plan before stopping unfinished substantial work.
- Reconcile durable discoveries into current knowledge or a decision.
- Archive/delete absorbed transient handoffs; Git holds implementation history.
- Put a general framework lesson in `.agentos/upstream/` only with project
  evidence and explicit craftsmanship/simplification review.

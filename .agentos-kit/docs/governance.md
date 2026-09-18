# Knowledge change control

AgentOS keeps project memory editable, but “editable” does not mean every agent
may silently redefine every promise. Mature projects can use the optional
catalog field `change_control` to say how a knowledge document may change.

## The three policies

| Policy | Meaning |
|---|---|
| `agent` | An agent may update the document within the authorized task, while preserving evidence and unrelated work. |
| `review` | An agent may prepare a proposal or patch, but the new claim does not become accepted authority until a named human or delegated owner reviews it. |
| `protected` | Do not edit the document unless the current user request explicitly authorizes that document or policy change. Record a separate proposal when useful. |

When the field is absent, `contract` and `decision` default to `review`; other
authorities default to `agent`. Add the field only when the default is
insufficient. The context command displays the effective policy beside each
recommended document.

The policy in force before a change governs that change. An agent cannot grant
itself permission by first weakening `change_control`, changing an owner, or
relabeling contract as working memory.

## A small project policy

A mature project may place a short governance block in `project.md`:

```markdown
## Knowledge governance

- Product promises and invariants: review by the product owner.
- Accepted architecture decisions: supersede with a reviewed decision; do not rewrite history.
- Current state, plans, findings, and test evidence: agent-maintained.
- Privacy and data-retention policy: protected; explicit user direction required.
```

Name a role or repository owner only when one actually exists. `review` does not
require a committee, and `protected` is not a substitute for normal Git access
controls. Teams may reinforce important paths with `CODEOWNERS`, protected
branches, or required reviews; AgentOS records the meaning but does not enforce
hosting permissions.

## What agents do with each authority

- Working and evidence documents should stay current. Update them when the task
  supplies better observations, and state limitations honestly.
- A product contract can receive a proposed edit, but existing accepted intent
  remains authoritative until the required review occurs.
- An accepted decision is normally superseded by a new decision rather than
  rewritten to erase the old rationale.
- Historical records may be corrected for factual errors, but should not be
  polished into a different history.

Keep this proportional. A solo experiment may need no explicit fields because
the defaults are enough. Add governance when silent self-modification would cost
more than the policy takes to understand.

# {{PROJECT_NAME}} agent router

This repository uses AgentOS for durable, progressively disclosed project memory.

## Always

- Inspect git state before editing; preserve unrelated work.
- Treat source and tests as implementation evidence, not product intent.
- Preserve the invariants named in `.agentos/invariants.md`.
- Honor effective catalog `change_control`; contract and decision edits require
  review by default.
- Never turn an uncertainty into a fact. Record meaningful unknowns.
- Claim only the evidence actually obtained; compilation is not behavioral proof.

## Find context

The canonical knowledge catalog is `.agentos/index.json`. Read its plain-language
`read_when`, path, and dependency routes. For a non-trivial catalog, optionally run:

```sh
agentos context "<task>" --path <target-path>
```

Treat the output as recommendations, not a complete semantic judgment. Read
relevant files in order, inspect any omitted candidates selectively, and add
context when the task reveals a missing dependency. Do not read all of
`.agentos/` by default. The Markdown memory remains usable without the CLI.

## During and after work

- Use an indexed active plan for work that may cross a session.
- Update current truth in place; Git holds the old truth.
- Record only architecturally significant, counterintuitive, or costly-to-rediscover decisions.
- Before stopping unfinished substantial work, update the plan's Done/Now/Next/Evidence/Risks/Resume sections.
- On completion, reconcile durable discoveries into permanent docs and archive/delete transient handoffs.
- Run `agentos validate` after knowledge changes when the optional CLI is available.

## Authority

Catalog authority is ordered by meaning, not rank: `contract`, `decision`,
`evidence`, `working`, `historical`. Working notes and hypotheses must be
verified. Active decisions remain intentional until superseded. Source proves
behavior; tests prove only what they exercise. Optional `change_control` values
are `agent`, `review`, and `protected`.

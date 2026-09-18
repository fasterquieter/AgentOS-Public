# {{PROJECT_NAME}} agent router

{{PROJECT_NAME}} uses repository-local, progressively disclosed project memory.

## Always

- Inspect git state before editing; preserve unrelated work.
- Treat source and tests as implementation evidence, not product intent.
- Preserve any active invariants indexed for the area being changed.
- Honor effective catalog `change_control`; contract and decision edits require
  review by default.
- Never turn an uncertainty into a fact. Record meaningful unknowns.
- Claim only the evidence actually obtained; compilation is not behavioral proof.

## Find context

The canonical knowledge catalog is `.agentos/index.json`. Read its plain-language
`read_when`, path, and dependency routes. For a non-trivial catalog, optionally run:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos context "<task>" --path <target-path>
```

Treat the output as recommendations, not a complete semantic judgment. Read
relevant files in order, inspect any omitted candidates selectively, and add
context when the task reveals a missing dependency. Do not read all of
`.agentos/` by default. The Markdown memory remains usable without the CLI.

## Dormant capabilities

If a task introduces a class of need not covered by active project memory—such
as real-user feedback, an escaped behavioral regression, several routes to one
capability, hardware experiments, authentication/security, terminology drift, or
architecture debt, parallel branches, governance, or a routing miss—read
`.agentos-kit/CAPABILITIES.md` and
then only the one relevant guide. Activate the smallest project-specific pattern;
never make the generic kit project truth or read the kit wholesale.

## During and after work

- Use an indexed active plan for work that may cross a session.
- Update current truth in place; Git holds the old truth.
- Record only architecturally significant, counterintuitive, or costly-to-rediscover decisions.
- Before stopping unfinished substantial work, update the plan's Done/Now/Next/Evidence/Risks/Resume sections.
- On completion, reconcile durable discoveries into permanent docs and archive/delete transient handoffs.
- Run `PYTHONPATH=.agentos-kit/src python3 -m agentos validate` after knowledge
  changes when the optional local helper is available.

## Authority

Catalog authority is ordered by meaning, not rank: `contract`, `decision`,
`evidence`, `working`, `historical`. `dormant` is lifecycle, not project
authority. Working notes and hypotheses must be verified. Active decisions remain
intentional until superseded. Optional `change_control` values are `agent`,
`review`, and `protected`. Source proves behavior; tests prove only what they exercise.

# AgentOS architecture

Verified: 2026-08-26 from source.

## System shape

AgentOS has four layers:

1. Root `AGENTS.md` is the universally discoverable identity gate and small behavioral router. Vendor adapters import or point to it.
2. `.agentos/seed-state.md` distinguishes unadapted clone state from an adapted project while allowing AgentOS-specific prompts to develop the master safely.
3. `.agentos/index.json` and indexed Markdown are the active project memory and readable discovery graph.
4. `.agentos-kit/` is the self-contained dormant capability library: guides, reviews, templates, examples, tests, and optional tooling. Its capability map is cheap to discover; detailed entries do not enter normal routing.

## Runtime components

- `.agentos-kit/ADAPTATION.md` and `src/agentos/adaptation.py`: agent-led
  first-prompt transition plus a deterministic, preview-only transaction report;
  no human command, automatic semantic rewrite, or product classifier.
- `.agentos-kit/CAPABILITIES.md`: tiny trigger-to-guide map and activation protocol.
- `.agentos-kit/docs/behavior-proof-maps.md`: dormant guidance for progressively
  accounting for consequential behaviors, routes/states, oracles, and evidence.
- `.agentos-kit/seed/`: minimum adapted catalog and origin template.
- `.agentos-kit/src/agentos/catalog.py`: catalog loading, advisory routing, size estimation, and mechanical validation including seed-state checks.
- `.agentos-kit/src/agentos/routing_eval.py`: opt-in replay of routing cases
  captured from observed project failures.
- `.agentos-kit/src/agentos/bootstrap.py`: optional legacy/conservative initializer for other adoption paths.
- `.agentos-kit/src/agentos/cli.py`: optional `init`, `adapt --preview`, `context`, `validate`, `eval-routing`, and `new` commands.
- `.agentos-kit/src/agentos/templates/`: project memory and record templates.

## Dependency direction

CLI commands call small domain modules. Catalog logic depends only on the Python standard library. Templates never import runtime code. The active `.agentos/` layer may evolve per project; the dormant kit is local infrastructure and never a source of current project truth.

## Routing

Routing scores baseline documents, task-term overlap, and target-path globs. It then follows explicit `depends_on` edges. The token budget is soft for dependencies and otherwise limits lower-ranked primary matches. A result explains every inclusion and exposes every budget omission so discovery remains auditable. The result is advisory; agent judgment may add or reject context.

Catalog authority and lifecycle remain separate from optional change control.
`agent`, `review`, and `protected` describe who may accept a knowledge edit;
contract and decision records default to review, while other authorities default
to agent maintenance. Parallel branches use workstream-local plans and one
integration reconciliation pass rather than a lock service or shared runtime.

## Trust boundary

Deterministic validation can prove structure, references, lifecycle vocabulary,
plan completeness, size/freshness signals, and mechanical seed/adapted-state
requirements. For an activated behavior proof map it also enforces evidence
authority and routed—not baseline—context. It cannot decide whether a prompt
defines another product, which memory that product earns, whether a source
construct is a semantic behavior, or whether an oracle/document is true. Those
remain agent judgments grounded in the user specification and project evidence.

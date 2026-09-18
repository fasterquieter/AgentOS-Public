# Dormant AgentOS capability map

This is a discovery map, not project truth and not an orientation manual. Read
it only when the current project develops a need that active project memory does
not already cover. Never read `.agentos-kit/` wholesale.

| New signal in the project | Read only this first | Possible project-specific activation |
|---|---|---|
| Work may cross sessions; a fresh agent must resume | `.agentos-kit/docs/workflows.md` | One active plan; separate handoff only when a plan does not fit |
| Several agents or branches may change shared project memory concurrently | `.agentos-kit/docs/collaboration.md` | Workstream-owned plans plus one explicit integration owner and reconciliation pass |
| A mature team needs to control who may change promises, decisions, or evidence | `.agentos-kit/docs/governance.md` | A small governance block and selective catalog `change_control` fields |
| An important behavior escaped green tests, has several routes, or depends on a risky state/sequence | `.agentos-kit/docs/behavior-proof-maps.md` | A small behavior proof map linking claims, routes/states, oracles, and actual evidence |
| A strange choice or tempting reversal needs durable rationale | `.agentos-kit/docs/knowledge-model.md` | A bounded decision record |
| An approach failed and is likely to be repeated | `.agentos-kit/docs/workflows.md` and the `failed.md` template | A concise failed-approach record |
| Hardware, devices, media, performance, or regime-dependent experiments begin | `.agentos-kit/docs/testing-evidence.md` | An evidence ledger or experiment block with environment and controls |
| Real user reports arrive or a user model is needed | `.agentos-kit/docs/personas-feedback.md` | Raw feedback first; insight/persona only when evidence earns it |
| An important product concept is renamed or vocabulary drifts | `.agentos-kit/docs/terminology.md` | A small terminology/retired-name section or record |
| Code, database, CMS content, external documents, or production may disagree | `.agentos-kit/docs/authority.md` | An authority map in project or architecture memory |
| Boundaries or iterative patches are becoming hard to reason about | `.agentos-kit/reviews/craftsmanship.md` | A scoped architecture/craftsmanship review |
| The project may have accumulated unnecessary machinery | `.agentos-kit/reviews/curiosity.md` | A simplification review with deletion experiments |
| A change affects UX, accessibility, privacy/security, reliability, or performance | `.agentos-kit/reviews/orchestration.md`, then one relevant section of `specialists.md` | A proportionate review; do not instantiate reviewer personas |
| Agent discovery differs across Codex, Claude, Cursor, or Gemini | `.agentos-kit/docs/portability.md` | A thin vendor pointer, never copied project truth |
| A project lesson may improve AgentOS generally | `.agentos-kit/docs/maintenance.md` | An upstream proposal with project evidence and counterexamples |
| Catalog routing, validation, or record scaffolding needs adjustment | `.agentos-kit/README.md` and `.agentos-kit/docs/design.md` | Adapt the local convention; upgrades from master are optional |
| A context recommendation missed an important note or repeatedly included noise | `.agentos-kit/docs/design.md` | One routing evaluation case derived from the observed failure |

## Activate a capability

1. Check whether active project memory already covers the need.
2. Read this map and one directly relevant guide—nothing else by default.
3. Inspect project evidence and terminology before adopting the generic pattern.
4. Create or adapt only the smallest project-specific document or rule needed.
5. Add that project-specific material to active discovery. Keep the generic guide
   `dormant`; it is reference, not authority about the project.
6. Verify that ordinary unrelated tasks still exclude the capability.
7. Propose an upstream AgentOS change only for a genuinely general lesson.

Activation is evolutionary, not a reinstall. The project's conventions may
diverge from this kit, and normal use never requires synchronizing with the
AgentOS master repository.

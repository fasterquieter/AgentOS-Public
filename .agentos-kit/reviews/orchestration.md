# Review orchestration

Reviews are perspectives, not employees. Select them from the change, not from a fixed ceremony.

## Classify the change

- **Scope:** tiny, component, or system.
- **Risk:** low, medium, or high based on reversibility and failure consequence.
- **User-facing:** behavior, language, navigation, visual hierarchy, or interaction changed.
- **Architecture:** boundaries, dependencies, data flow, or core representation changed.
- **Data:** persistence, migration, deletion, compatibility, sync, or recovery changed.
- **Security/privacy:** trust boundary, authorization, secrets, personal data, or exposure changed.
- **Performance:** latency, memory, battery, network, throughput, or large-scale behavior is material.

Use these dimensions to choose the smallest useful set from the review documents, and state the evidence that makes each perspective relevant. A fixed selector cannot know the product or failure mode well enough to replace this judgment.

## Typical pipelines

| Change | Useful sequence |
|---|---|
| Tiny internal change | implement → targeted evidence |
| Component behavior | implement → focused tests → QA if stateful/risky → knowledge reconciliation |
| Persistence rewrite | plan → implement/migrate → integration and recovery evidence → QA → architecture/craftsmanship → security/performance as relevant → curator |
| Onboarding redesign | implement → UI/E2E evidence → UX → selected personas → accessibility → curator |
| Dependency/config update | build/integration evidence → security/compatibility as relevant → curator if commands/architecture changed |

Review findings should be prioritized: must fix, should fix, worthwhile eventually, speculative, or leave alone. Include evidence, impact, risk, effort, confidence, and a bounded next action. Reviewers surface changes; they do not autonomously refactor unrelated stable code.

## Periodic reviews

Periodic reviews look across individually reasonable changes. Trigger them at a release boundary, after a major architectural phase, when complexity/staleness signals accumulate, or on an explicit cadence appropriate to the project. Their default output is findings, not rewrites.

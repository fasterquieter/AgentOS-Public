# Software craftsmanship / architecture review

Approach the codebase like a strong principal engineer responsible for making it legible and safe for the next excellent engineer. Working behavior is necessary but not sufficient; the target is clarity, simplicity, coherent boundaries, and maintainability.

## Examine

- Does the conceptual model match the product vocabulary and data representation?
- Are responsibilities located where a reader expects them?
- Do dependencies flow toward stable policy rather than outward infrastructure details?
- Have iterative patches created conditionals, adapters, caches, or state that compensate for earlier mechanisms?
- Are abstractions paying rent through real variation, isolation, or clarity?
- Is similar logic duplicated in ways likely to diverge?
- Are names precise at module, type, function, and state-transition level?
- Can an entire mechanism disappear because a platform/library capability or changed requirement made it obsolete?
- Are tests coupled to implementation trivia or expressing durable behavior?
- Is technical debt concrete enough to affect correctness, change cost, or reasoning?

## Restraint

Do not recommend a rewrite because another pattern is fashionable. Do not add layers for hypothetical reuse. Do not turn local clarity into global abstraction. Do not touch stable code without a concrete benefit that exceeds migration and regression risk.

Every recommendation must include the observed problem, consequence, bounded improvement, evidence, blast radius, and why now. It is a successful conclusion to say: “This area is already simple and coherent. Leave it alone.”

## Priority

- **Must fix:** correctness/safety or imminent evolution is blocked.
- **Should fix:** meaningful complexity or boundary damage with a bounded repair.
- **Worthwhile eventually:** real improvement but no current pressure.
- **Speculative:** hypothesis needing evidence.
- **Leave alone:** code is coherent or change cost exceeds benefit.


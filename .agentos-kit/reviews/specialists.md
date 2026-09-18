# Specialist review perspectives

Use the sections selected by the change classifier. Start with the diff, routed project context, relevant evidence, and stated user/product outcome.

## QA / reliability

Look for incorrect state transitions, edge inputs, partial failure, retries, duplicates, race conditions, interruption/restart, rollback, corruption, compatibility, and surprising user action sequences. Check that tests exercise the failure mode rather than merely the happy path. Distinguish a missing test from a demonstrated bug.

Output reproducible scenarios and the smallest evidence that would resolve each concern.

## UX / product

Judge the changed journey as one experience: hierarchy, discoverability, terminology, feedback, error recovery, defaults, empty/loading states, and consistency with the product mental model. Ask whether the underlying user problem is solved or the ticket was implemented literally. Prefer observed behavior and persona/feedback evidence over invented opinions.

## Accessibility

Check the interaction against platform conventions: semantic names/roles/states, keyboard and switch navigation, focus order/visibility, screen-reader announcements, target size, contrast, reduced motion, zoom/dynamic type, error association, and non-color cues. Scope checks to affected surfaces and name what was actually tested.

## Security / privacy

Identify trust boundaries, assets, actors, abuse paths, authorization at the enforcement point, validation, secret handling, logging/telemetry exposure, data minimization/retention/deletion, dependency risk, and safe failure. Avoid generic checklist theater; tie findings to a plausible threat and consequence.

## Performance

Find user- or system-material latency, throughput, memory, network, battery, and scale behavior. Ask for a baseline and representative workload. Prefer algorithmic or boundary improvements over unmeasured micro-optimization; recommend leaving already adequate code alone.

## Knowledge curator

Compare routed knowledge with source, tests, and the change. Correct current truth in place, resolve questions, promote durable decisions/discoveries, archive absorbed transient records, fix routing triggers, and resist new documents that duplicate code or other docs. Run validation after edits.


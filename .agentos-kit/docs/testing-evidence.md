# Testing and evidence

Evidence must match the claim. “The project compiles” supports type/build integrity, not a user's successful journey, migration safety, or device behavior.

A green test proves only what its assertion can actually tell apart. A test of
underlying logic proves only that path; a real button, device, service, or human
claim needs evidence from that route or environment.

## Evidence ladder

Record the strongest level actually obtained:

1. **Inspected** — source/configuration supports an inference; not executed.
2. **Static** — format, lint, type, or build check passed.
3. **Unit** — isolated behavior exercised.
4. **Integration** — component boundaries exercised with real or representative dependencies.
5. **UI/component** — rendered interaction exercised in a component harness.
6. **End-to-end** — user path exercised through the assembled system.
7. **Simulator/emulator** — platform runtime exercised without physical hardware.
8. **Physical device/environment** — named hardware, OS, browser, network, or deployment exercised.
9. **Real user evidence** — observed behavior from an actual user; useful but not automatically causal.

Levels are not universal rankings. A parser change may be fully evidenced by focused unit/property tests; a camera permission flow needs device evidence. Report environment and important fixtures.

## Strategy, claims, and evidence accounting

A test strategy says how the project selects and runs evidence. It does not by
itself inventory the consequential behaviors that evidence is meant to prove.
When a project repeatedly loses that connection, activate the optional
[behavior proof map](behavior-proof-maps.md):

```text
accepted product promise → semantic behavior → route/state → oracle → evidence
```

Keep underlying capability evidence separate from actual route, environment, and
human evidence. A headless test can prove the semantic operation while proving
nothing about the button, URL, system intent, migration door, or physical service
a person uses. The map references this guide and existing evidence; it does not
copy the test strategy or raw reports.

## Select evidence by change

| Change characteristic | Minimum questions |
|---|---|
| Pure calculation | Boundary cases, invalid inputs, deterministic unit tests |
| API/data boundary | Contract compatibility, integration test, failure and retry behavior |
| Persistence/migration | Forward/backward compatibility, representative old data, rollback/recovery, destructive-path review |
| User interaction | Rendered behavior, keyboard/screen-reader implications, loading/error/empty states |
| Concurrency/offline | Interleavings, idempotency, retry duplication, clock/network failure, recovery |
| Performance-sensitive | Representative scale, baseline, measurement method, acceptable threshold |
| Security/privacy | Threat boundary, authorization failures, data exposure/logging, dependency/config evidence |
| Hardware/platform | Simulator versus physical device stated explicitly, OS/device matrix where material |

Compilation can be one item in the evidence list; it cannot stand in for these questions.

## Evidence in plans and findings

Use exact commands and outcomes:

```text
- Unit: `python -m unittest tests.test_queue` — 18 passed on Python 3.12.
- E2E: offline create → reconnect → upload exercised in iOS 19 simulator; entry uploaded once.
- Physical device: not run.
- Remaining inference: Android background scheduling uses the same queue, but was not exercised.
```

Do not write “tests pass” when only a filtered suite ran. Do not convert an agent's visual inspection into an accessibility audit. Negative evidence—could not reproduce, device unavailable, flaky result—is worth recording honestly.

## Empirical investigations

Use a compact experiment block when a conclusion is expensive to reproduce or
depends on hardware, OS/vendor behavior, performance conditions, media, network,
or another test regime. Put it in the existing canonical evidence or
failed-approach document before creating another record type.

Record only the fields that determine trust and reproduction:

- **Question:** the bounded claim being tested.
- **Environment:** device/model, OS or firmware, versions, configuration, input,
  and other material conditions.
- **Method and controls:** what changed, what stayed fixed, and any positive or
  negative control that proves the instrument can detect the effect.
- **Observation and artifacts:** measurements, logs, media, hashes, or exact
  commands; keep observation separate from explanation.
- **Interpretation:** what the result supports, its confidence, and the regime to
  which it applies. An accepted or echoed API value is not automatically physical
  behavior; a screenshot is not automatically optical proof.
- **Safety and cleanup:** packages, settings, fixtures, media, credentials, or
  physical state changed and whether each was restored.
- **Correction/reproduction:** how to rerun it and which earlier conclusion this
  supersedes, if any.

A narrow negative result means “not observed under these conditions,” not “the
platform cannot do this.” Do not require this form for ordinary deterministic
unit tests.

## Exploratory and persona tests

Exploratory and persona runs discover confusion, unanticipated sequences, and weak mental models. Their observations become findings or raw evidence. They do not replace deterministic regression tests. When a persona exposes a reproducible defect, add a deterministic test at the lowest useful level.

When any defect escapes green evidence, also ask why the proof model missed it:
was the behavior, route/state, important sequence, fixture/environment, oracle,
evidence attachment, or freshness claim absent or wrong? Reconcile an active
behavior proof map in the same coherent change. A regression test without this
question can preserve the fix while preserving the blind spot that let it escape.

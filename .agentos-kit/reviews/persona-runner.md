# Persona test runner

Use with a project-specific persona and a runnable product. The persona changes how the test is attempted; it does not predetermine findings.

## Inputs

- Persona file and evidence basis.
- One realistic goal, starting state, environment, and data scale.
- Product access and authorization boundaries.
- Relevant deterministic test coverage so exploratory results are not confused with regression proof.

## Run

1. State what the persona expects before acting.
2. Operate the product using available UI/device/browser tools.
3. Record actions and observed results without silently correcting the product.
4. Note hesitation, unread text, misunderstood terminology, missed controls, failed recovery, and surprising state.
5. Try a plausible error or interruption if safe and relevant.
6. Separate reproducible product behavior from persona inference.

## Report

For each finding: scenario, expectation, action, observation, recovery, severity, confidence, evidence artifact, affected journey, and next validation. Recommend a deterministic regression test when the issue is reproducible. Avoid statements about entire demographic groups.


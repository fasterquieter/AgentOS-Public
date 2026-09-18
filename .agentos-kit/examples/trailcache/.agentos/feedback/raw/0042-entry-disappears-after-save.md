# Entry appears to disappear after save

Received: 2026-08-11
Status: raw

## Original report

“Why does this stupid thing disappear when I press save? I did it twice and now I can't tell if either one is there.”

## Observed context

- Support screen recording shows Save completed and editor dismissed.
- Journal then showed “No entries on Pine Loop.”
- Pine Loop filter was already selected; the new Entry used Ridge North.
- App 4.8.1 on iPhone; network state unknown.

## Interpretation (hypothesis)

The Entry probably persisted but was excluded by the already-active Trail filter. Duplicate creation is possible because Save was tapped twice; exact database state was not included.

## Triage

- Feature: Journal save confirmation and filters
- Severity: medium; perceived data loss
- Related reports: support 0038 and beta note B-17 describe similar filter confusion
- Interpretation confidence: medium


# Active filters make successful saves look lost

Status: accepted insight
Reviewed: 2026-08-22

## Evidence

- Raw report 0042 includes a recording with Pine Loop filter active and a Ridge North Entry saved.
- Support 0038: user found the Entry after clearing a date filter.
- Beta note B-17: user created a second Entry after returning to an unchanged filtered list.

## Pattern

After a successful save, returning to a list whose existing filters exclude the Entry creates perceived data loss. All three users expected immediate visibility or an explanation.

## Causal hypotheses

- High confidence: unchanged filters hide the Entry; directly observed in two reports.
- Medium confidence: subtle save feedback increases duplicate attempts; reported twice but not instrumented.

## Impact

Perceived data loss damages trust in an offline journal and can create duplicates. The content itself was recovered in the two inspected databases.

## Next validation or action

Prototype a post-save notice that states “Saved — hidden by Pine Loop filter” with a Clear filters action. Test with the distracted first-run and screen-reader personas, then add a UI regression test for announcement and action.

## Persona evolution proposal

Accepted 2026-08-22: the distracted first-run persona now explicitly assumes Save should produce immediate visible confirmation under an old filter. Do not generalize beyond journal/filter behavior without more evidence.


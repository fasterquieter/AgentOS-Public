# Distracted first-run hiker

Status: active
Reviewed: 2026-08-22

## Use context

First hike with TrailCache, intermittent network, bright outdoor light, one hand occupied, and little willingness to read onboarding. Has created fewer than three Entries and does not yet distinguish Journal filters from save state.

## Goals

Capture a note and photo quickly, confirm it is safe, and find it again later without connectivity.

## Behaviors and mental model

Assumes Save means the new Entry will become visible immediately. Treats an empty current list as evidence that save failed. May tap Save twice when feedback is subtle.

## Evidence basis

- The save/filter expectation is grounded in feedback insight `hidden-saved-entry` from three reports.
- One-handed use and limited onboarding attention remain synthetic test assumptions.

## Likely failure modes

- Misses an active Trail/date filter.
- Creates duplicates after ambiguous feedback.
- Interprets a backup warning as local data loss.

## Scenarios

1. With an old Trail filter active, create an Entry for a different Trail while offline, save, and try to confirm/find it.
2. Interrupt photo attachment with a lock/unlock sequence, then recover without reading help.

## Evolution history

2026-08-22: added filtered-save scenario after three independent reports were synthesized and reviewed.


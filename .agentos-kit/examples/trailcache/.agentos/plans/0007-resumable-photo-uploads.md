# Make photo uploads resumable

Status: active
Owner: upload implementation agent
Updated: 2026-08-25

## Objective

A killed or disconnected app resumes each encrypted photo from the last server-confirmed chunk without duplicate objects, lost local content, or infinite credential retry. Acceptance requires unit/integration evidence plus iOS and Android simulator process-death runs.

## Done

- Added upload-session identity and committed offset to the queue schema.
- Added backward migration: existing whole-object queue rows start with no session and offset zero.
- Implemented service create-session and query-offset clients.
- Implemented queue reducer tests for expired lease, stale local offset, server-ahead offset, URL expiry, and duplicate completion response.
- Deviated from the original fixed 1 MiB design: service requires all non-final chunks to be 4 MiB aligned.

## Now

- Wire the Android background adapter's expiration callback to release the lease without clearing session ID or committed offset.

## Next

1. Add Android adapter integration test for expiration and process restart.
2. Run Android emulator upload → kill after two chunks → relaunch → verify one object and resumed bytes.
3. Run equivalent iOS simulator background-expiration scenario.
4. Check diagnostics for URL/token redaction.
5. Update sync evidence gaps and close/archive this plan after review.

## Evidence

- `sync_queue_reducer_test`: 27 passed, including five new recovery cases.
- `upload_service_contract_test`: 8 passed against local service container.
- Database migration fixture from schema v11 to v12: passed; downgrade not supported by invariant.
- Simulator/physical device: not yet run.

## Risks

- Android callback may arrive after the OS has already suspended persistence work; transaction placement needs evidence.
- Server offset is authoritative for committed bytes, but a server-behind response must never rewind a locally encrypted stream incorrectly.
- Logs from the prototype included signed query parameters; redaction is not yet rechecked.

## Resume

Read the routed sync, invariant, decision, and failed-approach context. Inspect `src/sync/android/BackgroundUploadAdapter.kt` and its integration test, then implement the expiration lease release. Do not create a replacement queue item when credentials expire.


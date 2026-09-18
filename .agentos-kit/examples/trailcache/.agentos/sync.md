# Photo and journal synchronization

Verified: 2026-08-24 against coordinator tests and iOS simulator traces.

## State model

Each mutation moves through `pending → leasing → uploaded` or returns to `pending` with an attempt record. Leases expire after process death. Entry metadata and each photo have stable idempotency keys derived from local immutable IDs, not signed upload URLs.

## Photo upload

The queue stores photo ID, encrypted file path, byte size, object key, committed byte offset, attempt count, and next eligible time. Signed URLs are credentials, not durable work identity; they may be refreshed without creating a new queue item.

Current implementation uploads a whole object and records completion. Plan 0007 introduces chunk checkpoints. The service accepts `Content-Range` only for upload sessions created through `/photo-uploads`; generic object URLs do not support resume.

## Retry

- Authentication and expired URLs refresh immediately without consuming the transient-network retry budget.
- 408/429/5xx and connectivity failures use capped exponential backoff with jitter.
- Payload/schema rejection is terminal and surfaced to diagnostics; it does not loop.
- Background-task expiration releases the lease and preserves the last server-confirmed offset.

## Conflict and deletion

Entry merge is field-aware and non-destructive. Explicit local/remote tombstones are mutations; missing server records are not deletions. Photo objects are garbage-collected only after every retained Entry version no longer references them and the 30-day recovery window has elapsed.

## Evidence gaps

- Chunk recovery has unit coverage in the current branch but no physical-device evidence yet.
- Android process-death recovery is inferred from shared queue logic plus adapter tests; an end-to-end emulator run remains in plan 0007.


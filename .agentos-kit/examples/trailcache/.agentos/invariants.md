# TrailCache invariants

Accepted: 2026-07-12 product and architecture review.

1. An Entry is readable and editable without network access after its local save succeeds.
2. Server absence or expired credentials never cause automatic deletion of local Entry or photo data.
3. Entry and photo upload operations are idempotent across retries and process restarts.
4. A released database schema remains readable through a documented migration path; downgrade is not promised.
5. An explicit user deletion propagates as a tombstone and is recoverable locally for 30 days.
6. Sync never silently merges two edits to the same field; it preserves both versions for conflict resolution.


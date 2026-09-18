# Failed synchronization approaches

Last verified: 2026-08-24

## Persisting signed upload URLs as work identity

**Attempt.** The first queue stored the signed object URL and retried that URL after interruption.

**Observed result.** Background retries commonly resumed after the URL's 15-minute expiry. The queue treated 403 as permanent failure, or a patch generated a second queue item with a fresh URL and occasionally uploaded twice.

**Proven cause.** Signed URLs are short-lived credentials and generic object URLs do not carry stable idempotency or resumable-session identity.

**Durable lesson.** Persist local photo/object identity and upload-session/checkpoint state. Acquire credentials at attempt time. A credential refresh must not create new logical work.

**Retry only when.** The storage provider offers a durable, idempotent session token whose lifetime and refresh semantics are explicitly longer than background suspension.


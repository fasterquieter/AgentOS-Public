# TrailCache architecture

Verified: 2026-08-18 against mobile and service source.

## Components

- Journal domain owns Entry identity, edits, and local ordering.
- SQLite storage is the durable device store and records an append-only mutation sequence for sync.
- Sync coordinator reads pending mutations, transfers encrypted payloads/photos, and applies non-destructive remote merges.
- Cloud API stores user-scoped encrypted Entry envelopes and issues short-lived object upload URLs.
- Platform adapters provide background scheduling, connectivity, filesystem, and secure key storage.

## Data flow

UI writes an Entry to SQLite before reporting save success. That transaction appends a mutation. The coordinator uploads metadata idempotently, then photos. Remote changes merge into the device journal; a remote absence becomes a tombstone only when it carries an explicit user deletion mutation.

## Boundary rule

Platform background APIs schedule and transport work but do not decide domain retry, identity, merge, or deletion policy. Those rules stay in shared sync/domain code.


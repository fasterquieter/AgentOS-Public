# Device journal remains authoritative

Status: accepted
Date: 2026-05-03

## Context

TrailCache promises useful capture where connectivity is absent or intermittent. Early server-mirror behavior treated a missing remote record as deletion and removed a hiker's locally saved Entry after a partial restore.

## Decision

The device journal is the authority for content visible on that device. The cloud carries explicit mutations and convergence state; remote absence alone has no destructive meaning. User deletion is represented by a signed tombstone with a recovery window.

## Alternatives

- Server-authoritative mirror — simpler reconciliation but violates offline ownership and made partial backups destructive.
- Last-write-wins records — compact but silently discards concurrent field edits and depends on unreliable clock ordering.

## Consequences

- Local content survives incomplete backups, credential changes, and server restoration gaps.
- Sync needs explicit tombstones, mutation identity, retained conflicts, and garbage-collection rules.
- A fresh device restores only confirmed cloud state; “device authoritative” does not invent content on a device that never received it.

## Revisit when

The product deliberately ends offline-first capture or adopts collaborative ownership with a reviewed migration and recovery design. Storage cost alone is not sufficient.


# Allow exclusion paths in routing

Status: proposed
Date: 2026-08-24

## Proposed framework improvement

Allow catalog path routes to exclude generated and fixture trees, for example include `src/sync/**` but exclude `src/sync/generated/**`.

## Evidence from this project

The sync client contains generated API models under the same directory as hand-written coordinator code. Tasks that only update a generated schema file currently retrieve the full sync decision/failure context even though regeneration is mechanical.

## Generality

Generated code inside subsystem directories is common, but only one AgentOS project has supplied evidence so far.

## Suggested implementation

Add optional `exclude_paths` with the same glob syntax. A matching exclusion should suppress only that entry's path score, never a task-term or dependency inclusion.

## Risks and counterexamples

Generated changes can still alter contracts. Exclusion must not hide an explicit dependency or task match, and the extra field may be unnecessary if repositories keep generated code at a separate boundary.


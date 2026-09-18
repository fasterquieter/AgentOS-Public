# Terminology and retired names

Create terminology memory only when inconsistent vocabulary could cause product,
compatibility, migration, routing, or support errors. A glossary for a project
with no terminology problem is bureaucracy.

For each material change, record:

| Concept | Current user-facing term | Retired term | Legacy identifier retained? | Reason or compatibility boundary |
|---|---|---|---|---|

Distinguish user language from code, storage, API, route, analytics, and import
identifiers. A legacy identifier may remain intentionally even when the UI term
changes. Do not mechanically rename it without checking compatibility.

Put a short table in `project.md` when vocabulary is central and small. Create a
separate active terminology record only when several tasks need it independently.
Replace current terms in place; Git retains the old table. Keep a retired mapping
only while it prevents a plausible reversal or integration error.

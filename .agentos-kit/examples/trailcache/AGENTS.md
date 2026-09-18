# TrailCache agent router

TrailCache is a local-first mobile hiking journal. Its device journal remains authoritative while cloud sync provides backup and multi-device convergence.

## Always

- Preserve offline create/edit/read behavior.
- Never delete local user content automatically to match server absence.
- Keep upload operations idempotent and schema changes backward-readable.
- Do not rename product terms without an explicit vocabulary/product decision.
- Inspect git state and report the exact evidence obtained.

## Find context

The canonical catalog is `.agentos/index.json`.

```sh
agentos context "<task>" --path <target-path>
```

Treat returned context as recommendations, inspect reported omissions selectively, and read other evidence when the task makes it relevant. Update the active plan before stopping unfinished work. Reconcile durable discoveries into current docs; delete absorbed handoffs. Run `agentos validate` after memory changes.

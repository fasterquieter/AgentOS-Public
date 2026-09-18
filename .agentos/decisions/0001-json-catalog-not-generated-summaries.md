# Use a JSON catalog and source documents

Status: accepted
Date: 2026-08-26

## Context

AgentOS needs machine-readable routing and dependency relationships, but a knowledge graph service or generated summary layer would add synchronization failure modes before retrieval complexity is justified.

## Decision

Use `.agentos/index.json` as a small explicit graph whose nodes point to source Markdown. Store triggers, paths, dependencies, lifecycle, authority, freshness, and budgets in the catalog. Keep substantive knowledge only in the document.

## Alternatives

- One giant `AGENTS.md` — always consumes context and mixes unrelated knowledge.
- YAML front matter in every document — pleasant locally, but requires parsing dependencies and duplicates global discovery work.
- Generated summaries or embeddings — potentially valuable at very large scale, but introduce build state, opacity, and another stale representation.

## Consequences

- Routing is auditable and requires no dependency.
- Catalog entries need maintenance when documents move or split.
- JSON is less prose-friendly than YAML but universally parsed and straightforward to validate mechanically.
- A future retrieval index may be added only after measured routing failures; source documents and stable IDs remain canonical.

## Revisit when

Representative projects cannot stay within context budgets using tags, path scopes, and explicit dependencies, and measured failures show semantic retrieval would materially outperform the catalog.

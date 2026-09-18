# Bootstrap and adaptation paths

## Primary path: complete clone as project seed

For a new project, the supported human experience is:

1. clone or duplicate the complete AgentOS repository;
2. open it with a capable coding agent; and
3. give an ordinary non-AgentOS product specification after asking it to read
   root `AGENTS.md`.

The unadapted seed marker makes that specification the transition trigger. The
agent follows `.agentos-kit/ADAPTATION.md`, generates a read-only transaction
preview, protects any changed target paths, preserves this kit dormant, replaces
AgentOS self-memory, creates only earned project memory, validates the result,
and continues into product work. The human never installs or runs AgentOS.

The rest of this guide describes a secondary path for adding AgentOS to an
unrelated existing repository. Initialization has a deterministic phase and an
agent-judgment phase. The split prevents a script—or an overconfident agent—from
manufacturing knowledge merely to fill templates. Markdown remains usable without
installing the CLI; the command is a conservative convenience, not repository
understanding.

## Existing-repository path: install the starter

From an AgentOS checkout, use pipx or an activated virtual environment:

```sh
pipx install /path/to/AgentOS/.agentos-kit
agentos init /path/to/target --name "Product name"
```

The command detects only observable markers such as manifests, test configuration, root documentation, and top-level directories. It stores these in `.agentos/bootstrap-observations.json`. A manifest proves that a technology is present, not that it is deployed, canonical, or still used.

If `AGENTS.md` already exists, initialization preserves it and writes `.agentos/router-snippet.md`. A human or agent must merge the routing behavior without deleting existing project constraints. `--force` is for replacing AgentOS-owned starter files in a controlled test or blank project, not routine mature-repository upgrades.

## 2. Investigate in bounded passes

A capable agent should inspect, in this order:

1. existing instructions, README files, manifests, CI, and deploy configuration;
2. test entry points and actual runnable commands;
3. application entry points and major module boundaries;
4. persistence, network, authentication, migration, and destructive paths;
5. current git state, open plans/issues already stored in the repository;
6. mutable data/content/configuration and deployment sources that may be more current than repository files;
7. only then, product vocabulary, invariants, architectural data flow, and technical debt supported by evidence.

For a huge repository, sample by subsystem and label uninvestigated areas. Do not produce a confident whole-system map from directory names.

## 3. Customize the core

- Replace unknown project purpose only from product evidence or human confirmation.
- Name accepted product principles and current user vocabulary when they constrain implementation. Record retired names only when a rename could confuse users, routes, storage, or intentionally retained code identifiers.
- Identify separate authorities for source, generated code, mutable data, content, configuration, external documents, and deployed state when they can disagree. Do not assume the newest or largest dump is current.
- Record verified build/test/run commands and their working directory/environment.
- Describe architecture at component and data-flow level, not class-by-class.
- Accept invariants only with an owner, requirement, existing protective test, or clear implementation evidence.
- Add path routes for boundaries that a task can target independently.
- Add existing significant decisions when their rationale is discoverable; mark uncertain reconstructions as working hypotheses.
- Remove starter questions as they are resolved.

## 4. Activate optional modules by need

Examples:

- Create a sync subsystem map when sync work recurs and crosses multiple modules.
- Create a persona set before a meaningful onboarding redesign, not because personas exist in the template library.
- Create feedback folders when the first real report arrives.
- Create a failed-approach record when an obvious solution was tried, failed for a durable reason, and is likely to be repeated.
- Create a small behavior proof map when consequential behaviors have several
  routes/states, require distinct environments, or an escaped regression shows
  that existing tests do not account for the product claim. Do not generate a
  speculative census during migration.
- Create no security role document if the shared framework checklist is sufficient; projects add local security constraints only when specific.

## 5. Verify the installation

```sh
agentos validate
agentos context "change a small user-facing label" --path path/to/ui/file
agentos context "modify persistence migration" --path path/to/storage/file
```

The first recommendation should stay small and omit storage history. The second should include invariants, architecture/decision context, and appropriate state. If both return the same documents, routing is not customized enough. If either reports a relevant omitted candidate, verify that a fresh agent can find the needed section without loading the entire file.

Finally, ask a fresh agent—without the bootstrap conversation—to summarize purpose, current state, key invariants, and one subsystem from routed context. Record failures as routing or knowledge-hygiene work, not as a reason to enlarge `AGENTS.md`.

# Adapt an AgentOS clone to its first real project

Read this only when root `AGENTS.md` and `.agentos/seed-state.md` establish both:

1. the seed is still `unadapted`; and
2. the user has supplied a substantive specification for a product other than
   AgentOS.

The product prompt is the authorization and input for this transition. Do not
ask the human to initialize AgentOS, choose modules, run Terminal, or restate the
prompt in framework language. Adapt the repository and continue into useful
product work in the same task.

## Context boundary for the first agent

Before adapting, read only:

- root `AGENTS.md`;
- `.agentos/seed-state.md`;
- this file;
- the user's product specification; and
- `.agentos-kit/CAPABILITIES.md` only far enough to recognize a capability the
  specification already justifies.

Do **not** orient by reading all of `.agentos/`, `.agentos-kit/`, `docs/`, the
TrailCache example, framework tests, or AgentOS's own development records. Those describe the
framework, its development, or optional future capabilities—not the new product.

## 1. Establish facts without manufacturing certainty

Extract from the user specification and label the result by meaning:

- accepted product identity and purpose;
- users and use context actually stated or unavoidably implied;
- explicit non-goals and product principles;
- accepted constraints and vocabulary;
- likely technical environment, labeled as working direction until repository
  or executable evidence exists;
- evidence/testing needs already demanded by the product or platform;
- unresolved questions that materially block or could reverse implementation;
- the first bounded implementation objective and acceptance evidence.

The user's specification is product authority, not proof of implementation or
platform behavior. Do not invent personas, architectural facts, build commands,
security requirements, hardware conclusions, or certainty merely to fill a
template.

## 2. Protect the repository before the transition

- Inspect Git status and preserve any user-created material not inherited from
  AgentOS.
- Before changing files, generate the deterministic transaction preview:

  ```sh
  PYTHONPATH=.agentos-kit/src python3 -m agentos adapt --preview --name "<project name>"
  ```

  It lists the exact seed paths to replace, master-only files to remove, thin
  adapters to review, preserved boundaries, and target paths with working-tree
  changes. It never applies changes or invents project meaning. Reconcile any
  protected changes before continuing; do not bypass a warning by deleting the
  evidence.
- Record the current AgentOS revision when available; absence of a Git revision
  is acceptable and must be stated honestly.
- Never delete `.git/` or rewrite history as part of adaptation.
- Treat the exact paths below as AgentOS-owned only after verifying this is still
  the fresh seed. If the user has already modified one, reconcile rather than
  blindly replacing it.

## 3. Preserve capability; remove self-project contamination

Preserve `.agentos-kit/` intact. It is the dormant, versioned capability library
and optional local tool. Do not copy its detailed guides into active project
memory.

Replace AgentOS's active project layer:

- rebuild `.agentos/index.json` from
  `.agentos-kit/seed/minimal-index.json`, substituting the project name/date;
- replace AgentOS's `.agentos/project.md` and `.agentos/state.md` with concise
  project-specific documents;
- remove AgentOS's old `.agentos/architecture.md`, `invariants.md`, `decisions/`,
  `plans/`, and `upstream/` unless a same-named project document is independently
  justified now;
- rewrite `.agentos/seed-state.md` from
  `.agentos-kit/seed/adapted-origin.md` and keep its catalog entry archived;
- replace root `AGENTS.md` using `.agentos-kit/seed/project-AGENTS.md` as a
  structure, not as text to leave generic;
- replace root `README.md` with the new product's identity, current setup, and
  only verified commands.

Remove or replace AgentOS-master material outside the kit:

- `docs/` self-development reports;
- `CONTRIBUTING.md` for AgentOS;
- `.github/workflows/ci.yml` for AgentOS;
- root `LICENSE` unless the new product intentionally adopts that license.

Preserve and adapt thin `CLAUDE.md`, `GEMINI.md`, and Cursor pointers so they
route only to the new root `AGENTS.md`. Preserve useful generic ignore/attribute
rules and merge later project-specific rules. Git already retains deleted
AgentOS history; do not create an archive directory for it.

After this step, normal root paths are available for the product. Reusable
AgentOS code, tests, guides, reviews, templates, and the TrailCache example live
only under `.agentos-kit/` and therefore cannot be mistaken for product source,
tests, or examples.

## 4. Create only earned active memory

Every project starts with:

- short project truth in `.agentos/project.md`;
- short current state in `.agentos/state.md`;
- a concise project-specific root `AGENTS.md`;
- the active, tiny capability-map catalog entry; and
- one dormant catalog entry for the bundled capability library; the tiny
  capability map is the canonical inventory of individual guides.

That is enough for a tiny utility. Add another active document only when the
first specification already creates an independently useful information need:

| Evidence in the specification | Possible active memory |
|---|---|
| Several real components or non-obvious data flow | `architecture.md` |
| Product/safety/compatibility behavior agents could accidentally violate | `invariants.md` |
| Work clearly spans sessions | One active plan with Done/Now/Next/Evidence/Risks/Resume |
| Material ambiguity | `questions.md` or a short Questions section in state |
| A naming migration or several domain terms | A terminology section/record |
| Physical or regime-dependent testing is already required | Project-specific evidence protocol/ledger |
| Several consequential stateful behaviors, routes, environments, or explicit proof obligations already need accounting | A small behavior proof map; never a speculative census |
| Mutable content/runtime authority can differ from Git | Authority section in project or architecture |

Do not create personas, feedback collections, decision archives, handoffs,
security records, glossaries, experiment ledgers, behavior proof maps, or
subsystem maps merely because templates exist. Dormant files are preserved
precisely so that this decision is reversible later.

## 5. Build the project-specific router

Keep root `AGENTS.md` below 120 lines and preferably far below. It should contain:

- one sentence identifying the product;
- rules that truly apply to every task;
- how to inspect the active catalog or use the optional local finder;
- the active-memory closeout rule;
- one short pointer to `.agentos-kit/CAPABILITIES.md` for a new, uncovered class
  of need.

It must not contain the capability table, product history, completed milestones,
source-file encyclopedia, or the AgentOS adaptation protocol. Once adapted, the
seed transition is finished and the router should feel native to the product.

## 6. Validate the transition mechanically

The human does not run tools. The coding agent may use the repository-local
helper without installation:

```sh
PYTHONPATH=.agentos-kit/src python3 -m agentos validate
PYTHONPATH=.agentos-kit/src python3 -m agentos context "<first task>" --path <target>
```

Also verify:

- `.agentos/seed-state.md` says `adapted` and names the project;
- no active catalog entry describes AgentOS as the product;
- the generic capability-library entry remains `dormant`; the tiny capability
  map is active but not always loaded;
- a normal first task does not select detailed kit guidance;
- a task introducing feedback, hardware, auth/security, terminology, or
  architecture debt can find the capability map;
- a tiny project has no behavior proof map, while an initially stateful project
  gets only the few consequential claims its specification already justifies;
- root `AGENTS.md` remains concise;
- a fresh agent can recover purpose, state, next work, and applicable constraints
  without the bootstrap conversation.
- the applied transition matches the preview, with any deliberate deviation
  named in the completion summary.

If the helper is unavailable, inspect the JSON and Markdown directly. Tool
failure must not block adaptation.

## 7. Continue into the product

Do not stop after producing documentation unless implementation is genuinely
blocked by a missing product decision. Establish the smallest trustworthy memory
needed for the work, then begin the first bounded implementation objective from
the user's ordinary prompt.

## Later capability activation

After adaptation, a new need does not rerun this protocol. The future agent reads
the one relevant entry in `.agentos-kit/CAPABILITIES.md`, adapts the minimum
project-specific pattern, indexes that project record as active, and leaves the
generic capability dormant. The project may later combine, split, rename, or
remove its own memory. It never needs to synchronize with AgentOS master for
normal use.

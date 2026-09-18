# Agent portability

AgentOS keeps project knowledge independent of the tool loading it. The root `AGENTS.md` is canonical behavioral guidance; `.agentos/index.json` and source documents are canonical memory.

The plain-language rule is **one truth, several doors**. Different assistants may
enter through different instruction files, but they should reach the same
project memory rather than carry separate copies of it.

## Adapter policy

An adapter may:

- import or point to `AGENTS.md`;
- state a short tool-only behavior that cannot live canonically elsewhere;
- use native path scoping to activate a local router.

It must not copy architecture, invariants, commands, decisions, or workflow policy. Duplication will drift.

## Current discovery behavior

### Codex

Codex natively discovers `AGENTS.md` from the project root down to the working directory, with closer guidance later in the chain. Root AgentOS works directly; a subsystem may add a small nested router where local behavioral rules justify it.

### Claude Code

Claude Code uses `CLAUDE.md` and supports imports. AgentOS supplies:

```md
@AGENTS.md
```

Claude also supports scoped `.claude/rules/`, but adding generated copies of every catalog entry would defeat progressive disclosure and consume startup context. Use a scoped rule only for genuine always-on behavior tied to paths.

### Cursor

Cursor project rules can be always-on, path-attached, agent-requested, or manual. The included `.cursor/rules/agentos.mdc` is a short always-on pointer to `AGENTS.md`; current Cursor CLI also reads a root `AGENTS.md`. Projects may use agent-requested or path-attached rules to point to a subsystem node, but the node stays canonical in `.agentos/`.

### Gemini CLI

Gemini CLI uses hierarchical `GEMINI.md` files and supports Markdown imports. AgentOS supplies:

```md
@./AGENTS.md
```

Gemini can also configure `AGENTS.md` as a context filename, but repository defaults should not assume a user's global configuration.

## Other agents

For a tool that natively reads `AGENTS.md`, add nothing. For a tool with a repository instruction file and import syntax, create a one-line import. Without imports, create a short pointer that instructs the agent to read `AGENTS.md` first. Avoid symlinks as the only portable strategy because Windows permissions and some packaging/checkout environments complicate them.

Discovery behavior changes faster than project knowledge. Review adapters periodically and keep dated source links in [research.md](research.md).

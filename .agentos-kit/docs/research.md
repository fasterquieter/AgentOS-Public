# Research basis

Reviewed: 2026-08-26. Vendor behavior is time-sensitive; project knowledge architecture should outlive it.

## Agent instruction discovery

- [OpenAI: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) documents Codex's hierarchical root-to-working-directory discovery, closer-file precedence, and default combined size limit. AgentOS adopts a small root router and permits small nested behavioral routers rather than duplicating all memory into the prompt.
- [Anthropic: How Claude remembers your project](https://code.claude.com/docs/en/memory) recommends concise `CLAUDE.md` instructions, supports imports, loads descendant files on demand, and explicitly documents importing `AGENTS.md`. AgentOS uses a one-line adapter and keeps optional knowledge out of startup context.
- [Cursor: Rules](https://docs.cursor.com/context/rules) distinguishes always-on, path-attached, agent-requested, and manual project rules. AgentOS borrows scoped activation as a principle while keeping one vendor-neutral catalog.
- [Gemini CLI: GEMINI.md context files](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) documents hierarchical context and imports. AgentOS uses a one-line `GEMINI.md` import rather than divergent instructions.
- [AGENTS.md open format](https://agents.md/) provides the cross-tool convention and nested-file model. AgentOS treats it as the discoverable router, not the entire institutional memory.

## Decisions and durable reasoning

- [AWS Prescriptive Guidance: ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) defines ADRs around context, decision, consequences, lifecycle, and skimmable decision logs. AgentOS adds alternatives and explicit revisit evidence while restricting ADRs to significant choices.
- [MADR](https://adr.github.io/madr/) demonstrates concise Markdown decision records. AgentOS keeps its template intentionally lighter than a formal approval process.

## Specifications, plans, and repository maps

- [GitHub Spec Kit](https://github.github.com/spec-kit/) uses a durable Spec → Plan → Tasks → Implement sequence and supports many agent integrations. AgentOS adopts the durable-intent and resumable-plan principle, but remains an institutional-memory layer rather than a mandatory feature-development process.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) separates behavioral requirements and scenarios from design and tasks, and emphasizes brownfield adoption. AgentOS's `contract` authority can point to an existing OpenSpec/Spec Kit artifact instead of copying it; implementation plans remain distinct from product behavior.
- [Aider's repository map](https://github.com/Aider-AI/aider/blob/main/aider/website/docs/repomap.md) demonstrates token-budgeted, graph-ranked code symbols for structural code context. AgentOS solves a complementary problem: human/agent intent, decisions, state, evidence, and user learning that cannot be reliably derived from symbols. A future code map can feed task investigation without becoming project authority.

## Context engineering conclusions

Across the tools, persistent instruction files consume or influence context and work best when concise, specific, scoped, and non-contradictory. Tool discovery differs, but source-controlled hierarchical guidance and on-demand files recur. AgentOS therefore separates always-loaded behavior from task-retrieved knowledge and uses deterministic path/task/dependency routing.

We deliberately did not adopt a repository knowledge graph service, embeddings, or generated summaries in the first release. Those approaches may improve recall in very large repositories, but add hidden retrieval behavior and synchronization surfaces. Decision 0001 defines measured conditions for revisiting this choice.

## Ongoing review

Before changing adapters, verify current official vendor documentation. Before changing the vendor-neutral knowledge model, require evidence from routing/handoff evaluations or downstream projects rather than a new tool's fashion.

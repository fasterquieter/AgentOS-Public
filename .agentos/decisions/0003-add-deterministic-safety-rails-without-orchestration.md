# Add deterministic safety rails without orchestration

Status: accepted
Date: 2026-09-10

## Context

The clone-first transition, editable repository memory, parallel branches, and
lexical routing all create real trust boundaries. Pure prose leaves avoidable
mechanical ambiguity, while automatic semantic rewriting, locks, or opaque
retrieval would cross AgentOS's product boundary.

## Decision

- Add a preview-only adaptation command that reports exact replace/remove/review
  and preserve sets and detects changed targets. It never applies the semantic
  transition.
- Add optional catalog `change_control` with `agent`, `review`, and `protected`.
  Contract and decision default to review; other authorities default to agent.
- Define parallel work as branch-local plans and evidence followed by one
  integration owner reconciling shared current truth after source/tests merge.
- Add a routing evaluation runner whose cases must name the observed miss or
  noisy inclusion that earned them.
- Keep the public description consistently “project memory for coding agents.”

## Alternatives

- Fully automatic adaptation — rejected because product meaning and earned
  memory remain judgment tasks.
- A central lock, scheduler, or multi-agent database — rejected because AgentOS
  is repository memory, not an orchestration runtime.
- Mandatory review metadata on every document — rejected as ceremony; defaults
  cover ordinary projects.
- Embeddings before a failure corpus — rejected because there is no measured
  evidence that opaque retrieval earns its synchronization cost.

## Consequences

The CLI gains two bounded deterministic operations, while Markdown remains the
source of meaning. Teams can make self-modification rules explicit without
pretending the local validator enforces hosting permissions. Parallel work has a
clear convergence protocol but no false promise of live coordination. Routing
changes can be tested against real regressions before a more complex retrieval
layer is considered.

## Revisit when

Preview reports repeatedly fail to prevent adaptation damage, change-control
defaults block ordinary maintenance, repository reconciliation cannot handle
real concurrent work, or an observed routing corpus demonstrates that explicit
tags, paths, and dependencies cannot meet representative needs.

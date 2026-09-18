# Repository identity and seed state

Seed state: **unadapted**

Current framework-project identity: **AgentOS**

Adapted project: **none**

## Identity gate

This checkout deliberately has two roles until the seed is adapted:

- A task whose subject is AgentOS itself means this is the master framework
  project. Use the current `.agentos/index.json` and do not adapt the seed.
- A substantive user specification for another product means this is an
  unadapted clone being used as that product's repository. The specification
  itself triggers `.agentos-kit/ADAPTATION.md`; do not require the user to say
  “initialize AgentOS” or operate a tool.
- Repository housekeeping with no new product specification does not trigger
  adaptation.

The task's subject is the decisive signal. A copied Git remote, directory name,
or inherited AgentOS history must not override an explicit non-AgentOS product
specification.

## Transition invariant

Adaptation replaces AgentOS's active project identity and self-history, preserves
`.agentos-kit/` as dormant capability, creates only justified project memory,
rewrites this file as historical origin metadata, and then continues into the
product work.

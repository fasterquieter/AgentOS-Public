# Contributing

AgentOS should become more useful by becoming clearer, more economical, and better evidenced—not merely larger.

## Before changing the framework

1. Read `AGENTS.md` and the seed identity gate. For AgentOS work, inspect the catalog routes and optionally run `PYTHONPATH=.agentos-kit/src python3 -m agentos context "<your task>" --path <target>`.
2. Inspect `git status` and preserve unrelated changes.
3. For a new framework mechanism, provide a concrete project failure or simulation it resolves.
4. Prefer extending an existing document or command over creating a parallel concept.

## Verification

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .agentos-kit
PYTHONPATH=.agentos-kit/src python -m unittest discover -s .agentos-kit/tests -v
PYTHONPATH=.agentos-kit/src python -m agentos validate --strict
agentos --version
```

Documentation changes should also run representative `context` queries. CLI behavior changes need a test, help-text review, and starter-kit compatibility check. Seed changes additionally require the complex, tiny, later-activation, fresh-handoff, and context-budget evaluations.

## Knowledge closeout

- Update `.agentos/state.md` when project reality changes.
- Update the active plan if substantial work remains unfinished.
- Create an ADR only for an architecturally significant or counterintuitive choice.
- Add `.agentos/upstream/` evidence when a lesson arose in a downstream project; do not automatically change the framework from one anecdote.
- Delete or archive knowledge that has been absorbed elsewhere.

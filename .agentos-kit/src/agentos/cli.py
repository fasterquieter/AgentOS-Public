from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from importlib import resources
from pathlib import Path

from . import __version__
from .adaptation import build_adaptation_preview, format_adaptation_preview
from .bootstrap import initialize
from .catalog import (
    AgentOSError,
    load_catalog,
    next_number,
    project_root,
    route_with_diagnostics,
    save_catalog,
    slugify,
    validate,
)
from .routing_eval import evaluate_routing_cases, routing_results_json


TYPE_CONFIG = {
    "plan": ("plans", "plan", "working"),
    "decision": ("decisions", "decision", "decision"),
    "handoff": ("handoffs", "handoff", "working"),
    "feedback": ("feedback/raw", "feedback", "evidence"),
    "upstream": ("upstream", "upstream", "working"),
    "failed": ("failed", "failed", "evidence"),
    "persona": ("personas", "persona", "working"),
    "insight": ("feedback/insights", "insight", "working"),
    "finding": ("findings", "finding", "working"),
}


def render_record(kind: str, title: str, today: str) -> str:
    template = resources.files("agentos").joinpath("templates", "records", f"{kind}.md")
    return template.read_text(encoding="utf-8").replace("{{TITLE}}", title).replace("{{DATE}}", today)


def _json_document(document: object) -> dict[str, object]:
    return {key: value for key, value in vars(document).items() if value is not None}


def _command_context(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    result = route_with_diagnostics(root, load_catalog(root), args.task, args.path, args.budget)
    selected_tokens = sum(doc.estimated_tokens for doc in result.selected)
    over_budget = max(0, selected_tokens - args.budget)
    if args.json:
        print(
            json.dumps(
                {
                    "budget": args.budget,
                    "selected_tokens": selected_tokens,
                    "selected_over_budget": over_budget,
                    "selected": [_json_document(doc) for doc in result.selected],
                    "omitted": [_json_document(doc) for doc in result.omitted],
                },
                indent=2,
            )
        )
    else:
        print(f"Context recommendations (~{selected_tokens} selected tokens, budget {args.budget})")
        for index, doc in enumerate(result.selected, 1):
            print(
                f"{index}. {doc.path} "
                f"[{doc.role}; {doc.authority}/{doc.status}; change={doc.change_control}] "
                f"— {doc.reason} (~{doc.estimated_tokens})"
            )
        if over_budget:
            print(f"The advisory selection exceeds the budget by ~{over_budget} tokens.")
        if result.omitted:
            print("Relevant candidates not selected:")
            for doc in result.omitted:
                print(
                    f"- {doc.path} "
                    f"[{doc.role}; {doc.authority}/{doc.status}; change={doc.change_control}] "
                    f"— {doc.reason}; "
                    f"{doc.omission_reason} (~{doc.estimated_tokens})"
                )
            print("Search omitted candidates selectively or rerun with a deliberate higher --budget.")
    return 0 if result.selected or result.omitted else 1


def _command_validate(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    findings = validate(root, load_catalog(root))
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    elif not findings:
        print("AgentOS valid: no findings")
    else:
        for finding in findings:
            print(f"{finding.level.upper():7} {finding.code}: {finding.message}")
        errors = sum(f.level == "error" for f in findings)
        warnings = sum(f.level == "warning" for f in findings)
        print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if any(f.level == "error" or (args.strict and f.level == "warning") for f in findings) else 0


def _command_init(args: argparse.Namespace) -> int:
    written, warnings = initialize(Path(args.path), args.name, args.force)
    for warning in warnings:
        print(f"WARNING: {warning}")
    print(f"Initialized AgentOS with {len(written)} file(s)")
    for path in written:
        print(path)
    return 0


def _command_adapt(args: argparse.Namespace) -> int:
    if not args.preview:
        raise AgentOSError("AgentOS does not apply semantic adaptation automatically; use adapt --preview")
    root = project_root(args.root)
    preview = build_adaptation_preview(root, args.name)
    if args.json:
        print(json.dumps(preview, indent=2))
    else:
        print(format_adaptation_preview(preview))
    return 1 if preview["changed_targets"] else 0


def _command_eval_routing(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    results = evaluate_routing_cases(root, args.file)
    if args.json:
        print(json.dumps(routing_results_json(results), indent=2))
    else:
        for result in results:
            status = "PASS" if result.passed else "FAIL"
            print(f"{status} {result.id} — {result.origin}")
            for failure in result.failures:
                print(f"  - {failure}")
        passed = sum(result.passed for result in results)
        print(f"{passed}/{len(results)} routing evaluation(s) passed")
    return 0 if all(result.passed for result in results) else 1


def _command_new(args: argparse.Namespace) -> int:
    root = project_root(args.root)
    catalog = load_catalog(root)
    directory_name, doc_type, authority = TYPE_CONFIG[args.kind]
    directory = root / ".agentos" / directory_name
    directory.mkdir(parents=True, exist_ok=True)
    number = next_number(directory)
    filename = f"{number:04d}-{slugify(args.title)}.md"
    path = directory / filename
    path.write_text(render_record(args.kind, args.title, date.today().isoformat()), encoding="utf-8")
    relative = str(path.relative_to(root))
    catalog.setdefault("documents", []).append(
        {
            "id": f"{doc_type}-{number:04d}",
            "path": relative,
            "title": args.title,
            "type": doc_type,
            "authority": authority,
            "status": "active" if args.kind in {"plan", "handoff"} else "draft",
            "tags": args.tag,
            "read_when": [args.read_when or f"working on {args.title.lower()}"],
            "paths": args.path,
            "depends_on": args.depends_on,
            "review_after": (date.today() + timedelta(days=30)).isoformat(),
            "max_tokens": 1800,
        }
    )
    save_catalog(root, catalog)
    print(relative)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentos", description="Inspect and maintain project memory for coding agents")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Conservatively initialize a repository")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--name")
    init.add_argument("--force", action="store_true", help="Replace AgentOS-owned starter files")
    init.set_defaults(func=_command_init)

    adapt = sub.add_parser("adapt", help="Preview the mechanical part of first-project seed adaptation")
    adapt.add_argument("--preview", action="store_true", help="Print the transaction without changing files")
    adapt.add_argument("--name", required=True, help="New project's name")
    adapt.add_argument("--root", default=".")
    adapt.add_argument("--json", action="store_true")
    adapt.set_defaults(func=_command_adapt)

    context = sub.add_parser("context", help="Recommend relevant context candidates")
    context.add_argument("task")
    context.add_argument("--root", default=".")
    context.add_argument("--path", action="append", default=[], help="Changed or target path; repeatable")
    context.add_argument("--budget", type=int, default=2000, help="Advisory selected-token target")
    context.add_argument("--json", action="store_true")
    context.set_defaults(func=_command_context)

    check = sub.add_parser(
        "validate",
        help="Check structure, freshness, links, budgets, and proof-map boundaries",
    )
    check.add_argument("--root", default=".")
    check.add_argument("--strict", action="store_true")
    check.add_argument("--json", action="store_true")
    check.set_defaults(func=_command_validate)

    routing_eval = sub.add_parser(
        "eval-routing",
        help="Replay routing cases captured from observed misses or noisy inclusions",
    )
    routing_eval.add_argument("--root", default=".")
    routing_eval.add_argument("--file", default=".agentos/routing-evaluations.json")
    routing_eval.add_argument("--json", action="store_true")
    routing_eval.set_defaults(func=_command_eval_routing)

    new = sub.add_parser("new", help="Create and index a resumable record")
    new.add_argument("kind", choices=sorted(TYPE_CONFIG))
    new.add_argument("title")
    new.add_argument("--root", default=".")
    new.add_argument("--tag", action="append", default=[])
    new.add_argument("--path", action="append", default=[])
    new.add_argument("--depends-on", action="append", default=[])
    new.add_argument("--read-when")
    new.set_defaults(func=_command_new)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except AgentOSError as exc:
        print(f"agentos: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

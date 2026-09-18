from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .catalog import AgentOSError, load_catalog, route_with_diagnostics


CASE_FIELDS = {
    "id",
    "origin",
    "task",
    "paths",
    "budget",
    "expect_selected",
    "expect_omitted",
    "expect_absent",
}


@dataclass(frozen=True)
class RoutingCaseResult:
    id: str
    origin: str
    passed: bool
    selected: tuple[str, ...]
    omitted: tuple[str, ...]
    failures: tuple[str, ...]


def _string_list(case_id: str, case: dict[str, Any], field: str) -> list[str]:
    value = case.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise AgentOSError(f"Routing case {case_id}: {field} must be an array of non-empty strings")
    return value


def evaluate_routing_cases(root: Path, relative_file: str) -> list[RoutingCaseResult]:
    root = root.resolve()
    path = (root / relative_file).resolve()
    if not path.is_relative_to(root):
        raise AgentOSError(f"Routing evaluation file leaves project root: {relative_file}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AgentOSError(f"Missing routing evaluation file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AgentOSError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise AgentOSError("Routing evaluation root must be an object with schema_version 1")
    unknown_root = set(value) - {"schema_version", "cases"}
    if unknown_root:
        raise AgentOSError(f"Unknown routing evaluation fields: {sorted(unknown_root)}")
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases:
        raise AgentOSError("Routing evaluation must contain at least one observed case")

    catalog = load_catalog(root)
    known_ids = {entry.get("id") for entry in catalog.get("documents", [])}
    seen: set[str] = set()
    results: list[RoutingCaseResult] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise AgentOSError(f"Routing case {index + 1} must be an object")
        unknown_fields = set(case) - CASE_FIELDS
        if unknown_fields:
            raise AgentOSError(f"Routing case {index + 1}: unknown fields {sorted(unknown_fields)}")
        case_id = case.get("id")
        origin = case.get("origin")
        task = case.get("task")
        if not isinstance(case_id, str) or not case_id:
            raise AgentOSError(f"Routing case {index + 1} needs a non-empty id")
        if case_id in seen:
            raise AgentOSError(f"Duplicate routing case id: {case_id}")
        seen.add(case_id)
        if not isinstance(origin, str) or not origin.strip():
            raise AgentOSError(f"Routing case {case_id}: origin must describe the observed miss or noise")
        if not isinstance(task, str) or not task.strip():
            raise AgentOSError(f"Routing case {case_id}: task must be non-empty")
        paths = _string_list(case_id, case, "paths")
        expect_selected = _string_list(case_id, case, "expect_selected")
        expect_omitted = _string_list(case_id, case, "expect_omitted")
        expect_absent = _string_list(case_id, case, "expect_absent")
        if not (expect_selected or expect_omitted or expect_absent):
            raise AgentOSError(f"Routing case {case_id}: at least one expectation is required")
        expected_ids = set(expect_selected) | set(expect_omitted) | set(expect_absent)
        unknown = sorted(expected_ids - known_ids)
        if unknown:
            raise AgentOSError(f"Routing case {case_id}: unknown document ids {unknown}")
        budget = case.get("budget", 2000)
        if not isinstance(budget, int) or budget < 100:
            raise AgentOSError(f"Routing case {case_id}: budget must be an integer >= 100")

        routed = route_with_diagnostics(root, catalog, task, paths, budget)
        selected = tuple(document.id for document in routed.selected)
        omitted = tuple(document.id for document in routed.omitted)
        visible = set(selected) | set(omitted)
        failures: list[str] = []
        for document_id in expect_selected:
            if document_id not in selected:
                suffix = " (recognized but omitted by budget)" if document_id in omitted else ""
                failures.append(f"expected {document_id} to be selected{suffix}")
        for document_id in expect_omitted:
            if document_id not in omitted:
                failures.append(f"expected {document_id} to be reported as omitted")
        for document_id in expect_absent:
            if document_id in visible:
                failures.append(f"expected {document_id} to remain unrelated")
        results.append(
            RoutingCaseResult(
                id=case_id,
                origin=origin,
                passed=not failures,
                selected=selected,
                omitted=omitted,
                failures=tuple(failures),
            )
        )
    return results


def routing_results_json(results: list[RoutingCaseResult]) -> list[dict[str, Any]]:
    return [asdict(result) for result in results]

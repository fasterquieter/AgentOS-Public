from __future__ import annotations

import fnmatch
import json
import math
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

AUTHORITY = {"contract", "decision", "evidence", "working", "historical"}
STATUS = {"active", "draft", "dormant", "stale", "superseded", "archived"}
CHANGE_CONTROL = {"agent", "review", "protected"}
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLAN_SECTIONS = {"objective", "done", "now", "next", "evidence", "risks", "resume"}
ENTRY_FIELDS = {
    "id", "path", "title", "type", "authority", "status", "always", "fallback", "priority",
    "tags", "read_when", "paths", "depends_on", "review_after", "max_tokens", "change_control",
}


class AgentOSError(RuntimeError):
    pass


def project_root(start: Path | str = ".") -> Path:
    current = Path(start).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".agentos" / "index.json").exists():
            return candidate
    raise AgentOSError(f"No .agentos/index.json found from {current}")


def load_catalog(root: Path) -> dict[str, Any]:
    path = root / ".agentos" / "index.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AgentOSError(f"Missing catalog: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AgentOSError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AgentOSError("Catalog root must be an object")
    return value


def save_catalog(root: Path, catalog: dict[str, Any]) -> None:
    path = root / ".agentos" / "index.json"
    path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def terms(value: str) -> set[str]:
    stop = {
        "a", "an", "and", "any", "before", "change", "changing", "continue", "continuing",
        "for", "in", "make", "making", "modify", "modifying", "of", "on", "start", "starting",
        "task", "the", "to", "update", "updating", "with", "work", "working",
    }
    return {match.group(0).lower() for match in TOKEN_RE.finditer(value)} - stop


def estimate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text.split()) * 1.33))


def document_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise AgentOSError(f"Catalog path escapes the project root: {relative}")
    return path


@dataclass(frozen=True)
class RoutedDocument:
    id: str
    path: str
    role: str
    reason: str
    score: int
    estimated_tokens: int
    authority: str
    status: str
    change_control: str
    omission_reason: str | None = None


@dataclass(frozen=True)
class RoutingResult:
    selected: tuple[RoutedDocument, ...]
    omitted: tuple[RoutedDocument, ...]


def effective_change_control(entry: dict[str, Any]) -> str:
    """Return an explicit policy or the conservative authority-based default."""
    configured = entry.get("change_control")
    if isinstance(configured, str) and configured in CHANGE_CONTROL:
        return configured
    if entry.get("authority") in {"contract", "decision"}:
        return "review"
    return "agent"


def _entry_text(entry: dict[str, Any]) -> str:
    values: list[str] = [str(entry.get("id", "")), str(entry.get("title", ""))]
    values.extend(str(v) for v in entry.get("tags", []))
    values.extend(str(v) for v in entry.get("read_when", []))
    return " ".join(values)


def _matches_path(pattern: str, changed_path: str) -> bool:
    normalized = changed_path.removeprefix("./")
    return fnmatch.fnmatch(normalized, pattern) or fnmatch.fnmatch("/" + normalized, pattern)


def route_with_diagnostics(
    root: Path,
    catalog: dict[str, Any],
    task: str,
    changed_paths: Iterable[str] = (),
    budget: int = 2000,
) -> RoutingResult:
    task_terms = terms(task)
    paths = tuple(changed_paths)
    entries = {entry["id"]: entry for entry in catalog.get("documents", []) if "id" in entry}
    scored: dict[str, tuple[int, list[str]]] = {}

    for entry_id, entry in entries.items():
        if entry.get("status") not in {"active", "draft"}:
            continue
        score = 0
        reasons: list[str] = []
        if entry.get("always"):
            score += 100
            reasons.append("baseline")
        matching_paths = [
            path
            for path in paths
            if any(_matches_path(pattern, path) for pattern in entry.get("paths", []))
        ]
        if matching_paths:
            score += 30 + 5 * len(matching_paths)
            reasons.append("path: " + ", ".join(matching_paths[:2]))
        overlap = task_terms & terms(_entry_text(entry))
        # A concrete target path is a stronger signal than one generic shared word.
        # Keep single-term discovery when no path is known; with a path, require either
        # a path match or two semantic terms.
        if overlap and (not paths or matching_paths or len(overlap) >= 2 or entry.get("always")):
            score += 7 * len(overlap)
            reasons.append("task: " + ", ".join(sorted(overlap)))
        if score:
            scored[entry_id] = (score, reasons)

    fallback_ids: set[str] = set()
    if not scored:
        for entry_id, entry in entries.items():
            if entry.get("fallback") and entry.get("status") == "active":
                scored[entry_id] = (5, ["fallback for an unclassified task"])
                fallback_ids.add(entry_id)

    primary_ids = set(scored)
    queue = list(scored)
    while queue:
        entry_id = queue.pop()
        score, _ = scored[entry_id]
        for dependency in entries[entry_id].get("depends_on", []):
            if dependency not in entries:
                continue
            dependency_score = max(20, score - 1)
            current = scored.get(dependency)
            if current is None or current[0] < dependency_score:
                reasons = list(current[1]) if current else []
                requirement = f"required by {entry_id}"
                if requirement not in reasons:
                    reasons.append(requirement)
                scored[dependency] = (dependency_score, reasons)
                queue.append(dependency)

    ordered = sorted(
        scored,
        key=lambda entry_id: (
            0 if entries[entry_id].get("always") else 1,
            entries[entry_id].get("priority", 50) if entries[entry_id].get("always") else 0,
            -scored[entry_id][0],
            entry_id,
        ),
    )
    token_counts: dict[str, int] = {}
    for entry_id in ordered:
        entry = entries[entry_id]
        path = document_path(root, entry["path"])
        token_counts[entry_id] = estimate_tokens(path.read_text(encoding="utf-8")) if path.exists() else 0

    selected_ids: set[str] = set()
    omitted_ids: list[tuple[str, str]] = []
    used = 0

    def select_with_dependencies(entry_id: str) -> None:
        nonlocal used
        if entry_id in selected_ids or entry_id not in entries:
            return
        selected_ids.add(entry_id)
        used += token_counts.get(entry_id, 0)
        for dependency in entries[entry_id].get("depends_on", []):
            select_with_dependencies(dependency)

    # Budget primary matches as units of agent attention. Dependencies become
    # required only after their primary match is selected. This avoids returning
    # a prerequisite for a primary document that was silently dropped.
    for entry_id in ordered:
        if entry_id not in primary_ids or entry_id in selected_ids:
            continue
        entry = entries[entry_id]
        token_count = token_counts[entry_id]
        if selected_ids and used + token_count > budget and not entry.get("always"):
            over_by = used + token_count - budget
            omitted_ids.append(
                (entry_id, f"candidate alone would exceed the remaining budget by ~{over_by} tokens")
            )
            continue
        select_with_dependencies(entry_id)

    # Present primary matches first, followed by their dependencies in declared
    # order. Baseline documents remain first via priority. This makes the pack a
    # useful reading sequence while keeping every dependency nearby.
    emitted: set[str] = set()
    reading_order: list[str] = []

    def emit(entry_id: str) -> None:
        if entry_id in emitted or entry_id not in selected_ids:
            return
        emitted.add(entry_id)
        reading_order.append(entry_id)
        for dependency in entries[entry_id].get("depends_on", []):
            emit(dependency)

    for entry_id in ordered:
        emit(entry_id)

    selected: list[RoutedDocument] = []
    for entry_id in reading_order:
        entry = entries[entry_id]
        selected.append(
            RoutedDocument(
                id=entry_id,
                path=entry["path"],
                role=(
                    "baseline"
                    if entry.get("always")
                    else "fallback"
                    if entry_id in fallback_ids
                    else "match"
                    if entry_id in primary_ids
                    else "dependency"
                ),
                reason="; ".join(scored[entry_id][1]),
                score=scored[entry_id][0],
                estimated_tokens=token_counts[entry_id],
                authority=entry.get("authority", "working"),
                status=entry.get("status", "draft"),
                change_control=effective_change_control(entry),
            )
        )

    omitted: list[RoutedDocument] = []
    for entry_id, omission_reason in omitted_ids:
        entry = entries[entry_id]
        omitted.append(
            RoutedDocument(
                id=entry_id,
                path=entry["path"],
                role="fallback" if entry_id in fallback_ids else "match",
                reason="; ".join(scored[entry_id][1]),
                score=scored[entry_id][0],
                estimated_tokens=token_counts[entry_id],
                authority=entry.get("authority", "working"),
                status=entry.get("status", "draft"),
                change_control=effective_change_control(entry),
                omission_reason=omission_reason,
            )
        )
    return RoutingResult(tuple(selected), tuple(omitted))


def route(
    root: Path,
    catalog: dict[str, Any],
    task: str,
    changed_paths: Iterable[str] = (),
    budget: int = 2000,
) -> list[RoutedDocument]:
    """Return selected documents for compatibility with the original Python API."""
    return list(route_with_diagnostics(root, catalog, task, changed_paths, budget).selected)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str


def validate(root: Path, catalog: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    documents = catalog.get("documents")
    if catalog.get("schema_version") != 1:
        findings.append(Finding("error", "catalog.version", "schema_version must be 1"))
    if not isinstance(catalog.get("project"), str) or not catalog.get("project", "").strip():
        findings.append(Finding("error", "catalog.project", "project must be a non-empty string"))
    unknown_root = set(catalog) - {"schema_version", "project", "documents"}
    if unknown_root:
        findings.append(Finding("error", "catalog.fields", f"Unknown catalog fields: {sorted(unknown_root)}"))
    if not isinstance(documents, list):
        return [*findings, Finding("error", "catalog.documents", "documents must be an array")]

    ids: set[str] = set()
    paths: set[str] = set()
    entries: dict[str, dict[str, Any]] = {}
    today = date.today().isoformat()
    for index, entry in enumerate(documents):
        where = f"documents[{index}]"
        if not isinstance(entry, dict):
            findings.append(Finding("error", "catalog.entry", f"{where} must be an object"))
            continue
        missing = {
            "id", "path", "title", "type", "authority", "status", "tags", "read_when", "paths", "depends_on"
        } - entry.keys()
        if missing:
            findings.append(Finding("error", "catalog.fields", f"{where} missing {sorted(missing)}"))
            continue
        unknown = set(entry) - ENTRY_FIELDS
        if unknown:
            findings.append(Finding("error", "catalog.fields", f"{where} has unknown fields {sorted(unknown)}"))
        scalar_fields = ("id", "path", "title", "type", "authority", "status")
        if not all(isinstance(entry[field], str) and entry[field] for field in scalar_fields):
            findings.append(Finding("error", "catalog.field-type", f"{where}: core fields must be non-empty strings"))
            continue
        entry_id, relative = entry["id"], entry["path"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", entry_id):
            findings.append(Finding("error", "catalog.id", f"{where}: invalid id {entry_id!r}"))
        for field in ("tags", "read_when", "paths", "depends_on"):
            if not isinstance(entry[field], list) or not all(isinstance(value, str) for value in entry[field]):
                findings.append(Finding("error", "catalog.field-type", f"{entry_id}: {field} must be strings"))
        if entry_id in ids:
            findings.append(Finding("error", "catalog.duplicate-id", f"Duplicate id: {entry_id}"))
        if relative in paths:
            findings.append(Finding("error", "catalog.duplicate-path", f"Duplicate path: {relative}"))
        ids.add(entry_id)
        paths.add(relative)
        entries[entry_id] = entry
        if entry["authority"] not in AUTHORITY:
            findings.append(Finding("error", "catalog.authority", f"{entry_id}: invalid authority"))
        if entry["status"] not in STATUS:
            findings.append(Finding("error", "catalog.status", f"{entry_id}: invalid status"))
        change_control = entry.get("change_control")
        if change_control is not None and (
            not isinstance(change_control, str) or change_control not in CHANGE_CONTROL
        ):
            findings.append(
                Finding(
                    "error",
                    "catalog.change-control",
                    f"{entry_id}: change_control must be one of {sorted(CHANGE_CONTROL)}",
                )
            )
        if entry["type"] == "behavior-proof-map":
            if entry["authority"] != "evidence":
                findings.append(
                    Finding(
                        "error",
                        "proof-map.authority",
                        f"{entry_id}: a behavior proof map is evidence accounting, not "
                        f"{entry['authority']} authority",
                    )
                )
            if entry.get("always"):
                findings.append(
                    Finding(
                        "error",
                        "proof-map.routing",
                        f"{entry_id}: a behavior proof map must be routed, not always loaded",
                    )
                )
        try:
            path = document_path(root, relative)
        except AgentOSError as exc:
            findings.append(Finding("error", "doc.outside-root", str(exc)))
            continue
        if not path.is_file():
            findings.append(Finding("error", "doc.missing", f"{entry_id}: missing {relative}"))
            continue
        text = path.read_text(encoding="utf-8")
        token_budget = entry.get("max_tokens", 2500)
        if not isinstance(token_budget, int) or token_budget < 100:
            findings.append(Finding("error", "catalog.max-tokens", f"{entry_id}: max_tokens must be >= 100"))
            token_budget = 2500
        tokens = estimate_tokens(text)
        if tokens > token_budget:
            findings.append(
                Finding("warning", "doc.oversize", f"{relative}: ~{tokens} tokens exceeds {token_budget}")
            )
        review_after = entry.get("review_after")
        if review_after:
            try:
                date.fromisoformat(review_after)
            except (TypeError, ValueError):
                findings.append(Finding("error", "catalog.date", f"{entry_id}: invalid review_after {review_after!r}"))
            else:
                if review_after < today and entry["status"] == "active":
                    findings.append(Finding("warning", "doc.stale", f"{relative}: review due {review_after}"))
        if entry["type"] == "plan" and entry["status"] == "active":
            headings = {match.lower() for match in re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)}
            missing_sections = PLAN_SECTIONS - headings
            if missing_sections:
                findings.append(
                    Finding(
                        "error",
                        "plan.sections",
                        f"{relative}: missing plan sections {sorted(missing_sections)}",
                    )
                )
        for target in LINK_RE.findall(text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()):
                findings.append(Finding("warning", "link.outside-root", f"{relative}: link leaves project {target}"))
                continue
            if not resolved.exists():
                findings.append(Finding("warning", "link.broken", f"{relative}: broken link {target}"))

    for entry_id, entry in entries.items():
        for dependency in entry.get("depends_on", []):
            if dependency not in ids:
                findings.append(
                    Finding("error", "catalog.dependency", f"{entry_id}: unknown dependency {dependency}")
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(entry_id: str, chain: list[str]) -> None:
        if entry_id in visiting:
            cycle = chain[chain.index(entry_id):] + [entry_id]
            findings.append(Finding("error", "catalog.cycle", "Dependency cycle: " + " -> ".join(cycle)))
            return
        if entry_id in visited:
            return
        visiting.add(entry_id)
        for dependency in entries.get(entry_id, {}).get("depends_on", []):
            if dependency in entries:
                visit(dependency, [*chain, dependency])
        visiting.remove(entry_id)
        visited.add(entry_id)

    for entry_id in entries:
        visit(entry_id, [entry_id])

    agent_file = root / "AGENTS.md"
    if not agent_file.exists():
        findings.append(Finding("error", "router.missing", "AGENTS.md is missing"))
    else:
        lines = agent_file.read_text(encoding="utf-8").splitlines()
        if len(lines) > 120:
            findings.append(Finding("warning", "router.oversize", f"AGENTS.md has {len(lines)} lines; target <=120"))
        if ".agentos/index.json" not in "\n".join(lines):
            findings.append(Finding("error", "router.catalog", "AGENTS.md does not point to .agentos/index.json"))

    seed_file = root / ".agentos" / "seed-state.md"
    seed_guide = root / ".agentos-kit" / "ADAPTATION.md"
    if seed_guide.exists() and not seed_file.exists():
        findings.append(
            Finding("error", "seed.state", "A repository carrying the AgentOS seed kit needs .agentos/seed-state.md")
        )
    elif seed_file.exists():
        seed_text = seed_file.read_text(encoding="utf-8")
        state_match = re.search(
            r"^Seed state:\s*\*\*(unadapted|adapted)\*\*\s*$",
            seed_text,
            re.IGNORECASE | re.MULTILINE,
        )
        if not state_match:
            findings.append(
                Finding("error", "seed.state", ".agentos/seed-state.md must declare adapted or unadapted")
            )
        else:
            seed_state = state_match.group(1).lower()
            agent_text = agent_file.read_text(encoding="utf-8") if agent_file.exists() else ""
            capability_map = entries.get("capability-map")
            if seed_state == "unadapted":
                for required_path in (
                    root / ".agentos-kit" / "ADAPTATION.md",
                    root / ".agentos-kit" / "CAPABILITIES.md",
                ):
                    if not required_path.is_file():
                        findings.append(
                            Finding(
                                "error",
                                "seed.kit",
                                f"Unadapted seed is missing {required_path.relative_to(root)}",
                            )
                        )
                if ".agentos-kit/ADAPTATION.md" not in agent_text:
                    findings.append(
                        Finding("error", "seed.router", "Unadapted AGENTS.md must route to adaptation")
                    )
            else:
                if str(catalog.get("project", "")).strip().lower() == "agentos":
                    findings.append(
                        Finding("error", "seed.identity", "Adapted seed still names AgentOS as the project")
                    )
                if not capability_map or capability_map.get("status") != "active":
                    findings.append(
                        Finding("error", "seed.capability-map", "Adapted project needs an active capability map")
                    )
                if not any(entry.get("status") == "dormant" for entry in entries.values()):
                    findings.append(
                        Finding("error", "seed.dormant", "Adapted project has no dormant capability entries")
                    )
                origin = entries.get("seed-origin")
                if not origin or origin.get("status") != "archived":
                    findings.append(
                        Finding("error", "seed.origin", "Adapted seed origin must be archived")
                    )
                if ".agentos-kit/CAPABILITIES.md" not in agent_text:
                    findings.append(
                        Finding("error", "seed.router", "Adapted AGENTS.md must point to dormant capabilities")
                    )

    indexed = {(root / path).resolve() for path in paths}
    for doc in (root / ".agentos").rglob("*.md"):
        if doc.name == "router-snippet.md" or "archive" in doc.parts:
            continue
        if doc.resolve() not in indexed:
            findings.append(Finding("warning", "doc.unindexed", f"Unindexed knowledge file: {doc.relative_to(root)}"))
    return findings


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled"


def next_number(directory: Path) -> int:
    numbers = []
    for path in directory.glob("[0-9][0-9][0-9][0-9]-*.md"):
        try:
            numbers.append(int(path.name[:4]))
        except ValueError:
            pass
    return max(numbers, default=0) + 1

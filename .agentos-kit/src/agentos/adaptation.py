from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from .catalog import AgentOSError, document_path, load_catalog


REPLACE_PATHS = (
    "AGENTS.md",
    "README.md",
    ".agentos/index.json",
    ".agentos/project.md",
    ".agentos/state.md",
    ".agentos/seed-state.md",
)

REVIEW_PATHS = (
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules/agentos.mdc",
)

MASTER_ONLY_PATHS = (
    "CONTRIBUTING.md",
    "LICENSE",
    ".github/workflows/ci.yml",
)


def _relative_files(root: Path, relative: str) -> list[str]:
    target = document_path(root, relative)
    if target.is_file() or target.is_symlink():
        return [relative]
    if target.is_dir():
        return sorted(str(path.relative_to(root)) for path in target.rglob("*") if path.is_file())
    return []


def _changed_paths(root: Path) -> tuple[set[str], str | None]:
    commands = (
        ("git", "diff", "--name-only", "--relative", "HEAD"),
        ("git", "diff", "--cached", "--name-only", "--relative", "HEAD"),
        ("git", "ls-files", "--others", "--exclude-standard"),
    )
    changed: set[str] = set()
    try:
        for command in commands:
            result = subprocess.run(
                command,
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            changed.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    except (FileNotFoundError, subprocess.CalledProcessError):
        return set(), "Git changes could not be inspected; verify target files manually before adaptation."
    return changed, None


def build_adaptation_preview(root: Path, project_name: str) -> dict[str, Any]:
    """Describe a fresh-seed transition without changing the repository."""
    root = root.resolve()
    name = project_name.strip()
    if not name:
        raise AgentOSError("Adaptation preview requires a non-empty project name")

    marker = root / ".agentos" / "seed-state.md"
    try:
        marker_text = marker.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AgentOSError(f"Missing seed marker: {marker}") from exc
    match = re.search(
        r"^Seed state:\s*\*\*(unadapted|adapted)\*\*\s*$",
        marker_text,
        re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        raise AgentOSError("Seed marker does not declare an adapted or unadapted state")
    seed_state = match.group(1).lower()
    if seed_state != "unadapted":
        raise AgentOSError("Adaptation preview is only available for an unadapted AgentOS seed")
    if not (root / ".agentos-kit" / "ADAPTATION.md").is_file():
        raise AgentOSError("Repository does not contain the AgentOS adaptation kit")

    catalog = load_catalog(root)
    keep_active = {
        ".agentos/project.md",
        ".agentos/state.md",
        ".agentos/seed-state.md",
    }
    remove: set[str] = set()
    for relative in _relative_files(root, ".agentos"):
        if relative not in keep_active and relative != ".agentos/index.json":
            remove.add(relative)
    for entry in catalog.get("documents", []):
        relative = entry.get("path")
        if not isinstance(relative, str):
            continue
        if relative.startswith(".agentos-kit/") or relative in keep_active:
            continue
        remove.update(_relative_files(root, relative))
    remove.update(_relative_files(root, "docs"))
    for relative in MASTER_ONLY_PATHS:
        remove.update(_relative_files(root, relative))

    changed, git_warning = _changed_paths(root)
    target_paths = set(REPLACE_PATHS) | set(REVIEW_PATHS) | remove
    changed_targets = sorted(path for path in changed if path in target_paths)
    warnings: list[str] = []
    if git_warning:
        warnings.append(git_warning)
    if changed_targets:
        warnings.append(
            "Target paths contain working-tree changes. Reconcile them instead of replacing or removing them blindly."
        )

    return {
        "schema_version": 1,
        "mode": "preview",
        "project": name,
        "seed_state": seed_state,
        "changes_applied": False,
        "replace_with_project_content": list(REPLACE_PATHS),
        "remove_master_only": sorted(remove),
        "review_thin_adapters": [path for path in REVIEW_PATHS if (root / path).exists()],
        "preserve": [
            ".agentos-kit/",
            ".git/",
            ".gitignore",
            ".gitattributes",
            "all paths not explicitly listed above",
        ],
        "changed_targets": changed_targets,
        "warnings": warnings,
        "judgment_boundary": (
            "The preview identifies mechanical repository operations only. A capable agent still derives "
            "project purpose, earned memory, constraints, and evidence from the user's specification and repository."
        ),
    }


def format_adaptation_preview(preview: dict[str, Any]) -> str:
    sections = [
        f"Adaptation preview: AgentOS seed -> {preview['project']}",
        "No files changed.",
        "",
        "REPLACE WITH PROJECT-SPECIFIC CONTENT",
        *(f"- {path}" for path in preview["replace_with_project_content"]),
        "",
        "REMOVE AGENTOS MASTER-ONLY CONTENT",
        *(f"- {path}" for path in preview["remove_master_only"]),
        "",
        "REVIEW THIN VENDOR ADAPTERS",
        *(f"- {path}" for path in preview["review_thin_adapters"]),
        "",
        "PRESERVE",
        *(f"- {path}" for path in preview["preserve"]),
    ]
    if preview["changed_targets"]:
        sections.extend(
            [
                "",
                "PROTECTED WORKING-TREE CHANGES",
                *(f"- {path}" for path in preview["changed_targets"]),
            ]
        )
    for warning in preview["warnings"]:
        sections.extend(["", f"WARNING: {warning}"])
    sections.extend(["", str(preview["judgment_boundary"])])
    return "\n".join(sections)

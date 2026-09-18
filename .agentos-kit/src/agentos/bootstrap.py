from __future__ import annotations

import json
from datetime import date
from importlib import resources
from pathlib import Path

from .catalog import AgentOSError


STACK_MARKERS = {
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "package.json": "JavaScript/TypeScript",
    "Cargo.toml": "Rust",
    "go.mod": "Go",
    "Package.swift": "Swift",
    "Gemfile": "Ruby",
    "pom.xml": "Java/Maven",
    "build.gradle": "Java/Gradle",
}

TEST_MARKERS = {
    "pytest.ini": "pytest",
    "vitest.config.ts": "Vitest",
    "jest.config.js": "Jest",
    "playwright.config.ts": "Playwright",
    "Cargo.toml": "cargo test",
    "go.mod": "go test",
}


def inspect_repository(root: Path) -> dict[str, object]:
    stack = sorted({label for marker, label in STACK_MARKERS.items() if (root / marker).exists()})
    tests = sorted({label for marker, label in TEST_MARKERS.items() if (root / marker).exists()})
    top_dirs = sorted(path.name for path in root.iterdir() if path.is_dir() and not path.name.startswith("."))[:12]
    docs = sorted(path.name for path in root.glob("*.md"))
    return {
        "observed_on": date.today().isoformat(),
        "stack_evidence": stack,
        "test_evidence": tests,
        "top_level_directories": top_dirs,
        "existing_root_docs": docs,
        "note": "Deterministic observations only. An agent must verify architecture, invariants, and commands.",
    }


def _copy_tree(source, destination: Path, replacements: dict[str, str], force: bool) -> list[Path]:
    written: list[Path] = []
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            written.extend(_copy_tree(child, target, replacements, force))
            continue
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        text = child.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        target.write_text(text, encoding="utf-8")
        written.append(target)
    return written


def initialize(root: Path, project_name: str | None = None, force: bool = False) -> tuple[list[Path], list[str]]:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    report = inspect_repository(root)
    name = project_name or root.name
    warnings: list[str] = []
    if (root / ".agentos" / "index.json").exists() and not force:
        raise AgentOSError(f"AgentOS is already initialized in {root}")
    existing_router = (root / "AGENTS.md").exists() and not force
    if existing_router:
        warnings.append("Preserved existing AGENTS.md; merge .agentos/router-snippet.md into it.")
    for adapter in ("CLAUDE.md", "GEMINI.md"):
        if (root / adapter).exists() and not force:
            warnings.append(f"Preserved existing {adapter}; ensure it imports or points to AGENTS.md.")

    source = resources.files("agentos").joinpath("templates", "starter")
    replacements = {
        "{{PROJECT_NAME}}": name,
        "{{DATE}}": date.today().isoformat(),
        "{{DETECTION_REPORT}}": json.dumps(report, indent=2),
    }
    written = _copy_tree(source, root, replacements, force)
    report_path = root / ".agentos" / "bootstrap-observations.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    written.append(report_path)

    if existing_router:
        snippet_target = root / ".agentos" / "router-snippet.md"
        snippet_text = source.joinpath("AGENTS.md").read_text(encoding="utf-8")
        for old, new in replacements.items():
            snippet_text = snippet_text.replace(old, new)
        snippet_target.write_text(snippet_text, encoding="utf-8")
        written.append(snippet_target)
    return written, warnings

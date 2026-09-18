from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from agentos.adaptation import build_adaptation_preview
from agentos.catalog import estimate_tokens, load_catalog, route, validate


MASTER_ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-08-26"
MASTER_SEED_MARKER = MASTER_ROOT / ".agentos" / "seed-state.md"
MASTER_IS_UNADAPTED = MASTER_SEED_MARKER.is_file() and (
    "Seed state: **unadapted**" in MASTER_SEED_MARKER.read_text(encoding="utf-8")
)


def _copy_seed(destination: Path) -> Path:
    root = destination / "project"
    shutil.copytree(
        MASTER_ROOT,
        root,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store", "*.pyc"),
    )
    return root


def _render(path: Path, replacements: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _write_active_document(
    root: Path,
    catalog: dict[str, object],
    *,
    entry_id: str,
    filename: str,
    title: str,
    doc_type: str,
    authority: str,
    tags: list[str],
    read_when: list[str],
    paths: list[str],
    depends_on: list[str],
    text: str,
) -> None:
    path = root / ".agentos" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    catalog["documents"].append(  # type: ignore[index,union-attr]
        {
            "id": entry_id,
            "path": f".agentos/{filename}",
            "title": title,
            "type": doc_type,
            "authority": authority,
            "status": "active",
            "tags": tags,
            "read_when": read_when,
            "paths": paths,
            "depends_on": depends_on,
            "review_after": TODAY,
            "max_tokens": 1200,
        }
    )


def _adapt_seed(root: Path, project_name: str, project_text: str, state_text: str) -> dict[str, object]:
    preview = build_adaptation_preview(root, project_name)
    if preview["changes_applied"] or preview["project"] != project_name:
        raise AssertionError("Seed lifecycle must begin with a matching read-only adaptation preview")
    if ".agentos-kit/" not in preview["preserve"]:
        raise AssertionError("Adaptation preview must preserve the dormant capability kit")
    if "AGENTS.md" not in preview["replace_with_project_content"]:
        raise AssertionError("Adaptation preview must identify the root router transition")
    revision = "test-seed-revision"
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{DATE}}": TODAY,
        "{{AGENTOS_REVISION}}": revision,
    }
    shutil.rmtree(root / ".agentos")
    (root / ".agentos").mkdir()

    catalog = json.loads(
        _render(root / ".agentos-kit" / "seed" / "minimal-index.json", replacements)
    )
    (root / ".agentos" / "project.md").write_text(project_text, encoding="utf-8")
    (root / ".agentos" / "state.md").write_text(state_text, encoding="utf-8")
    (root / ".agentos" / "seed-state.md").write_text(
        _render(root / ".agentos-kit" / "seed" / "adapted-origin.md", replacements),
        encoding="utf-8",
    )
    (root / "AGENTS.md").write_text(
        _render(
            root / ".agentos-kit" / "seed" / "project-AGENTS.md",
            replacements,
        ),
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        f"# {project_name}\n\n{project_text.splitlines()[2]}\n",
        encoding="utf-8",
    )

    for self_path in (root / "docs", root / "CONTRIBUTING.md", root / ".github", root / "LICENSE"):
        if self_path.is_dir():
            shutil.rmtree(self_path)
        elif self_path.exists():
            self_path.unlink()
    return catalog


def _finish_catalog(root: Path, catalog: dict[str, object]) -> None:
    (root / ".agentos" / "index.json").write_text(
        json.dumps(catalog, indent=2) + "\n",
        encoding="utf-8",
    )


def _add_complex_memory(root: Path, catalog: dict[str, object]) -> None:
    _write_active_document(
        root,
        catalog,
        entry_id="architecture",
        filename="architecture.md",
        title="FieldLens architecture",
        doc_type="architecture",
        authority="working",
        tags=["offline", "photo", "sync", "architecture"],
        read_when=["changing capture, local storage, or synchronization"],
        paths=["App/**", "Tests/**"],
        depends_on=["project"],
        text=(
            "# Architecture\n\n"
            "Working direction: native SwiftUI capture writes artifact records and photos to a local "
            "store; a resumable queue syncs when connected. Platform behavior remains unverified.\n"
        ),
    )
    _write_active_document(
        root,
        catalog,
        entry_id="invariants",
        filename="invariants.md",
        title="FieldLens invariants",
        doc_type="invariants",
        authority="contract",
        tags=["offline", "delete", "artifact", "safety"],
        read_when=["changing local data, deletion, or sync semantics"],
        paths=["App/**", "Tests/**"],
        depends_on=["project"],
        text=(
            "# Invariants\n\n"
            "1. A captured artifact remains usable offline.\n"
            "2. Server absence never means delete the local artifact.\n"
            "3. Original condition photos remain attributable to their artifact.\n"
        ),
    )
    _write_active_document(
        root,
        catalog,
        entry_id="plan-0001",
        filename="plans/0001-first-capture-loop.md",
        title="First offline capture loop",
        doc_type="plan",
        authority="working",
        tags=["capture", "photo", "offline", "sync", "resume"],
        read_when=["building or resuming the first capture loop"],
        paths=["App/**", "Tests/**"],
        depends_on=["architecture", "invariants"],
        text=(
            "# First offline capture loop\n\nStatus: active\n\n"
            "## Objective\nCapture one artifact with a condition photo offline and preserve it across restart.\n\n"
            "## Done\n- Product contract and working architecture established.\n\n"
            "## Now\n- Create the local artifact model and storage boundary.\n\n"
            "## Next\n1. Add capture UI.\n2. Add resumable sync queue.\n3. Exercise restart on a physical iPhone.\n\n"
            "## Evidence\n- Not run; implementation has not begun.\n\n"
            "## Risks\n- Camera and background-transfer behavior require device evidence.\n\n"
            "## Resume\nImplement the local model and its restart persistence test first.\n"
        ),
    )
    _write_active_document(
        root,
        catalog,
        entry_id="device-evidence",
        filename="evidence/device.md",
        title="FieldLens device evidence",
        doc_type="evidence",
        authority="evidence",
        tags=["camera", "device", "measurement", "evidence"],
        read_when=["testing camera capture or background sync on physical hardware"],
        paths=["App/Capture/**", "Tests/Device/**"],
        depends_on=["architecture"],
        text=(
            "# Device evidence\n\nNo device run yet. Record device, OS, method, controls, "
            "artifacts, observed behavior, interpretation, and cleanup for each pass.\n"
        ),
    )
    _write_active_document(
        root,
        catalog,
        entry_id="behavior-proof",
        filename="behavior-proof.md",
        title="FieldLens behavior proof map",
        doc_type="behavior-proof-map",
        authority="evidence",
        tags=["behavior", "proof", "route", "oracle", "offline", "sync"],
        read_when=["changing offline capture, restart recovery, sync, or their evidence"],
        paths=["App/Capture/**", "App/Sync/**", "Tests/**"],
        depends_on=["project", "architecture", "invariants", "device-evidence"],
        text=(
            "# FieldLens behavior proof map\n\nVerified: no implementation evidence yet.\n\n"
            "## Authority\nEvidence accounting only. The product promise and safety rules live in "
            "project.md and invariants.md.\n\n## Claims\n\n"
            "### B-01 — Capture offline\n- Behavior: save one artifact and its photograph offline.\n"
            "- Route/state: capture Save while disconnected.\n- Oracle: one durable record and "
            "attributable photograph survive relaunch.\n- Evidence: unproved on every axis.\n\n"
            "### B-02 — Reconnect and sync\n- Behavior: upload a locally captured artifact once.\n"
            "- Route/state: offline capture → reconnect.\n- Oracle: the server and local store agree "
            "without duplicate or local deletion.\n- Evidence: unproved; physical service required.\n"
        ),
    )


@unittest.skipUnless(MASTER_IS_UNADAPTED, "clone lifecycle evaluations run only in the unadapted master seed")
class SeedLifecycleEvaluation(unittest.TestCase):
    def test_first_agent_can_identify_transition_from_router_and_ordinary_prompt(self) -> None:
        router = (MASTER_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        marker = (MASTER_ROOT / ".agentos" / "seed-state.md").read_text(encoding="utf-8")
        adaptation = (MASTER_ROOT / ".agentos-kit" / "ADAPTATION.md").read_text(encoding="utf-8")

        self.assertIn("substantive specification", router)
        self.assertIn(".agentos-kit/ADAPTATION.md", router)
        self.assertIn("Seed state: **unadapted**", marker)
        self.assertIn("The product prompt is the authorization", adaptation)
        self.assertNotIn("agentos init", router)

    def test_seed_validation_requires_identity_or_origin_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = _copy_seed(Path(temporary))
            (root / ".agentos" / "seed-state.md").unlink()

            findings = validate(root, load_catalog(root))
            self.assertIn("seed.state", [finding.code for finding in findings if finding.level == "error"])

    def test_complex_application_adapts_without_self_contamination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = _copy_seed(Path(temporary))
            kit_files = {
                path.relative_to(root): path.read_bytes()
                for path in (root / ".agentos-kit").rglob("*")
                if path.is_file()
            }
            project = (
                "# FieldLens\n\n"
                "FieldLens is a native iPhone app for museum conservators to photograph and record "
                "artifact condition offline, then synchronize when connectivity returns.\n\n"
                "## Product contract\n- Offline capture is primary.\n- Server absence never means local deletion.\n"
            )
            state = (
                "# Current state\n\nUpdated: 2026-08-26\n\n## Working\n- Product specification accepted.\n\n"
                "## Incomplete\n- No application code or runtime evidence yet.\n\n## Active work\n"
                "- First offline capture loop.\n\n## Next\n1. Implement the local model and persistence test.\n"
            )
            catalog = _adapt_seed(root, "FieldLens", project, state)
            _add_complex_memory(root, catalog)
            _finish_catalog(root, catalog)

            findings = validate(root, load_catalog(root))
            self.assertEqual([], [finding for finding in findings if finding.level == "error"])
            active_ids = {
                entry["id"]
                for entry in catalog["documents"]  # type: ignore[index]
                if entry["status"] in {"active", "draft"}
            }
            self.assertEqual(
                {
                    "project", "state", "capability-map", "architecture", "invariants",
                    "plan-0001", "device-evidence", "behavior-proof",
                },
                active_ids,
            )
            self.assertFalse(any(entry_id.startswith("upstream-") for entry_id in active_ids))
            self.assertFalse((root / "docs").exists())
            self.assertFalse((root / "CONTRIBUTING.md").exists())
            self.assertEqual(
                kit_files,
                {
                    path.relative_to(root): path.read_bytes()
                    for path in (root / ".agentos-kit").rglob("*")
                    if path.is_file()
                },
            )
            self.assertLessEqual(len((root / "AGENTS.md").read_text(encoding="utf-8").splitlines()), 120)
            unrelated = route(
                root,
                catalog,
                "change the application icon label",
                ["App/Settings/Appearance.swift"],
                2000,
            )
            self.assertNotIn("behavior-proof", [doc.id for doc in unrelated])

    def test_tiny_utility_keeps_active_memory_tiny(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = _copy_seed(Path(temporary))
            project = (
                "# HashDrop\n\n"
                "HashDrop is a tiny macOS utility that renames one dropped file to its SHA-256 digest.\n\n"
                "## Scope\n- One-file drag and drop.\n- No history, accounts, sync, or network.\n"
            )
            state = (
                "# Current state\n\nUpdated: 2026-08-26\n\n## Working\n- Product scope accepted.\n\n"
                "## Incomplete\n- Utility not implemented.\n\n## Active work\n- None.\n\n"
                "## Next\n1. Implement one drag-and-drop hashing path.\n"
            )
            catalog = _adapt_seed(root, "HashDrop", project, state)
            _finish_catalog(root, catalog)

            self.assertEqual([], [finding for finding in validate(root, load_catalog(root)) if finding.level == "error"])
            active_ids = {
                entry["id"]
                for entry in catalog["documents"]  # type: ignore[index]
                if entry["status"] in {"active", "draft"}
            }
            self.assertEqual({"project", "state", "capability-map"}, active_ids)
            self.assertFalse((root / ".agentos" / "behavior-proof.md").exists())
            self.assertIn(
                "behavior-proof-maps.md",
                (root / ".agentos-kit" / "CAPABILITIES.md").read_text(encoding="utf-8"),
            )
            docs = route(root, catalog, "implement file hash rename", ["Sources/HashDrop/main.swift"], 2000)
            self.assertEqual(["project", "state"], [doc.id for doc in docs])
            self.assertLess(sum(doc.estimated_tokens for doc in docs), 900)

    def test_escaped_regression_activates_a_small_local_proof_map_later(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = _copy_seed(Path(temporary))
            catalog = _adapt_seed(
                root,
                "HashDrop",
                "# HashDrop\n\nHashDrop renames a dropped file to its SHA-256 digest.\n",
                "# Current state\n\nUpdated: 2026-08-26\n\n## Working\n- Utility works locally.\n\n"
                "## Incomplete\n- Finder route regression escaped the unit suite.\n\n"
                "## Active work\n- Repair Finder drop.\n\n## Next\n1. Prove the real route.\n",
            )
            _finish_catalog(root, catalog)

            before = route(
                root,
                catalog,
                "fix escaped Finder drop route regression",
                ["Sources/HashDrop/DropView.swift"],
                2000,
            )
            self.assertNotIn("behavior-proof", [doc.id for doc in before])

            _write_active_document(
                root,
                catalog,
                entry_id="behavior-proof",
                filename="behavior-proof.md",
                title="HashDrop behavior proof map",
                doc_type="behavior-proof-map",
                authority="evidence",
                tags=["behavior", "proof", "finder", "drop", "route", "regression"],
                read_when=["changing the Finder drop route or its behavioral evidence"],
                paths=["Sources/HashDrop/DropView.swift", "Tests/**"],
                depends_on=["project"],
                text=(
                    "# HashDrop behavior proof map\n\n## Authority\nEvidence accounting only.\n\n"
                    "## Claims\n\n### B-01 — Rename a dropped file\n"
                    "- Behavior: rename one file to its SHA-256 digest.\n"
                    "- Route/state: Finder drop of a writable file.\n"
                    "- Oracle: exactly one file remains, with the digest name and identical bytes.\n"
                    "- Capability evidence: unit test passed.\n"
                    "- Route evidence: regression reproduced; replacement evidence not yet run.\n"
                ),
            )
            _finish_catalog(root, catalog)

            after = route(
                root,
                catalog,
                "fix escaped Finder drop route regression",
                ["Sources/HashDrop/DropView.swift"],
                2000,
            )
            self.assertIn("behavior-proof", [doc.id for doc in after])
            self.assertEqual([], [f for f in validate(root, load_catalog(root)) if f.level == "error"])

    def test_later_feedback_capability_is_discovered_and_activated_locally(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = _copy_seed(Path(temporary))
            catalog = _adapt_seed(
                root,
                "HashDrop",
                "# HashDrop\n\nHashDrop renames a dropped file to its SHA-256 digest.\n",
                "# Current state\n\nUpdated: 2026-08-26\n\n## Working\n- Utility works locally.\n\n## Incomplete\n- Beta feedback not reviewed.\n\n## Active work\n- None.\n\n## Next\n1. Review beta report.\n",
            )
            _finish_catalog(root, catalog)

            before = route(root, catalog, "triage beta user feedback about the result name", [], 2000)
            self.assertEqual(["project", "state"], [doc.id for doc in before])
            router = (root / "AGENTS.md").read_text(encoding="utf-8")
            capability_map = (root / ".agentos-kit" / "CAPABILITIES.md").read_text(encoding="utf-8")
            self.assertIn("real-user feedback", router)
            self.assertIn("personas-feedback.md", capability_map)

            _write_active_document(
                root,
                catalog,
                entry_id="feedback-0001",
                filename="feedback/raw/0001-result-name.md",
                title="Beta report: result filename is unclear",
                doc_type="feedback",
                authority="evidence",
                tags=["beta", "feedback", "result", "filename"],
                read_when=["changing the result filename or reviewing beta feedback"],
                paths=["Sources/HashDrop/**"],
                depends_on=["project"],
                text=(
                    "# Beta report: result filename is unclear\n\n"
                    "Observed report: the tester could not tell whether the digest replaced or accompanied the original name.\n"
                ),
            )
            _finish_catalog(root, catalog)

            after = route(root, catalog, "triage beta feedback about the result filename", [], 2000)
            after_ids = [doc.id for doc in after]
            self.assertIn("feedback-0001", after_ids)
            self.assertNotIn("capability-library", after_ids)
            generic = next(entry for entry in catalog["documents"] if entry["id"] == "capability-library")  # type: ignore[index]
            self.assertEqual("dormant", generic["status"])
            self.assertEqual([], [finding for finding in validate(root, load_catalog(root)) if finding.level == "error"])

    def test_fresh_handoff_recovers_complex_project_without_dormant_guides(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = _copy_seed(Path(temporary))
            catalog = _adapt_seed(
                root,
                "FieldLens",
                "# FieldLens\n\nFieldLens records museum artifact condition offline and syncs later.\n",
                "# Current state\n\nUpdated: 2026-08-26\n\n## Working\n- Product contract established.\n\n## Incomplete\n- Capture loop incomplete.\n\n## Active work\n- First capture loop.\n\n## Next\n1. Resume local model.\n",
            )
            _add_complex_memory(root, catalog)
            _finish_catalog(root, catalog)

            docs = route(root, catalog, "resume offline artifact photo sync", ["App/Sync/Queue.swift"], 4000)
            ids = [doc.id for doc in docs]
            self.assertIn("plan-0001", ids)
            self.assertIn("architecture", ids)
            self.assertIn("invariants", ids)
            self.assertIn("behavior-proof", ids)
            self.assertFalse(any(doc.id.startswith("capability-") for doc in docs))
            plan = (root / ".agentos" / "plans" / "0001-first-capture-loop.md").read_text(encoding="utf-8")
            self.assertIn("## Resume", plan)
            self.assertIn("local model", plan)
            proof_map = (root / ".agentos" / "behavior-proof.md").read_text(encoding="utf-8")
            self.assertEqual(2, proof_map.count("### B-"))

    def test_first_and_normal_context_costs_stay_small(self) -> None:
        first_common = sum(
            estimate_tokens(path.read_text(encoding="utf-8"))
            for path in (
                MASTER_ROOT / "AGENTS.md",
                MASTER_ROOT / ".agentos" / "seed-state.md",
                MASTER_ROOT / ".agentos-kit" / "ADAPTATION.md",
            )
        )
        capability_map = estimate_tokens(
            (MASTER_ROOT / ".agentos-kit" / "CAPABILITIES.md").read_text(encoding="utf-8")
        )
        adapted_router = estimate_tokens(
            (MASTER_ROOT / ".agentos-kit" / "seed" / "project-AGENTS.md").read_text(encoding="utf-8")
        )
        self.assertLess(first_common, 4000)
        self.assertLess(first_common + capability_map, 5000)
        self.assertLess(adapted_router, 700)


if __name__ == "__main__":
    unittest.main()

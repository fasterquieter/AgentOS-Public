from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from agentos.bootstrap import initialize
from agentos.adaptation import build_adaptation_preview
from agentos.catalog import (
    effective_change_control,
    load_catalog,
    route,
    route_with_diagnostics,
    save_catalog,
    validate,
)
from agentos.cli import main
from agentos.routing_eval import evaluate_routing_cases


class AgentOSTest(unittest.TestCase):
    def test_init_creates_minimal_valid_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "sample"
            written, warnings = initialize(root, "Sample")
            self.assertFalse(warnings)
            self.assertTrue(written)
            self.assertTrue((root / "AGENTS.md").exists())
            self.assertNotIn(
                ".agentos-kit/",
                (root / "AGENTS.md").read_text(encoding="utf-8"),
            )
            self.assertEqual([], [finding for finding in validate(root, load_catalog(root)) if finding.level == "error"])

    def test_init_preserves_existing_router(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_text("# Existing\n", encoding="utf-8")
            _, warnings = initialize(root, "Sample")
            self.assertTrue(warnings)
            self.assertEqual("# Existing\n", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertTrue((root / ".agentos" / "router-snippet.md").exists())

    def test_routing_uses_task_path_and_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"].append(
                {
                    "id": "sync",
                    "path": ".agentos/sync.md",
                    "title": "Photo synchronization",
                    "type": "subsystem",
                    "authority": "evidence",
                    "status": "active",
                    "tags": ["photo", "sync"],
                    "read_when": ["changing upload retries"],
                    "paths": ["src/sync/**"],
                    "depends_on": ["invariants"],
                }
            )
            (root / ".agentos" / "sync.md").write_text("# Sync\n", encoding="utf-8")
            docs = route(root, catalog, "fix photo upload retry", ["src/sync/queue.py"], 2000)
            ids = [doc.id for doc in docs]
            self.assertIn("sync", ids)
            self.assertIn("invariants", ids)
            self.assertLessEqual(sum(doc.estimated_tokens for doc in docs), 2000)

    def test_validation_finds_bad_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"][0]["depends_on"] = ["missing"]
            findings = validate(root, catalog)
            self.assertIn("catalog.dependency", {finding.code for finding in findings})

    def test_validation_rejects_dependency_cycle_and_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"][0]["depends_on"] = ["state"]
            catalog["documents"][1]["depends_on"] = ["project"]
            catalog["documents"][2]["path"] = "../outside.md"
            findings = validate(root, catalog)
            codes = {finding.code for finding in findings}
            self.assertIn("catalog.cycle", codes)
            self.assertIn("doc.outside-root", codes)

    def test_concrete_path_suppresses_weak_unrelated_term_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"].append(
                {
                    "id": "photos",
                    "path": ".agentos/photos.md",
                    "title": "Journal photo synchronization",
                    "type": "subsystem",
                    "authority": "evidence",
                    "status": "active",
                    "tags": ["journal", "photo", "sync"],
                    "read_when": ["changing photo synchronization"],
                    "paths": ["src/sync/**"],
                    "depends_on": [],
                }
            )
            (root / ".agentos" / "photos.md").write_text("# Photos\n", encoding="utf-8")
            docs = route(root, catalog, "change journal empty state", ["src/ui/Journal.tsx"], 2000)
            self.assertNotIn("photos", [doc.id for doc in docs])

    def test_dormant_capability_validates_but_never_routes_normally(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"].append(
                {
                    "id": "security-capability",
                    "path": ".agentos/security-capability.md",
                    "title": "Authentication and security guidance",
                    "type": "capability",
                    "authority": "working",
                    "status": "dormant",
                    "tags": ["authentication", "security"],
                    "read_when": ["adding authentication or security"],
                    "paths": ["src/auth/**"],
                    "depends_on": [],
                }
            )
            (root / ".agentos" / "security-capability.md").write_text(
                "# Generic security guidance\n",
                encoding="utf-8",
            )

            self.assertEqual([], [finding for finding in validate(root, catalog) if finding.level == "error"])
            docs = route(root, catalog, "add authentication security", ["src/auth/login.py"], 2000)
            self.assertNotIn("security-capability", [doc.id for doc in docs])

    def test_behavior_proof_map_is_evidence_accounting_and_never_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            entry = {
                "id": "behavior-proof",
                "path": ".agentos/behavior-proof.md",
                "title": "Behavior proof map",
                "type": "behavior-proof-map",
                "authority": "evidence",
                "status": "active",
                "tags": ["behavior", "route", "oracle", "evidence"],
                "read_when": ["changing a mapped behavior or escaped regression"],
                "paths": ["src/**", "tests/**"],
                "depends_on": ["project", "invariants"],
                "review_after": "2099-01-01",
                "max_tokens": 1200,
            }
            catalog["documents"].append(entry)
            (root / ".agentos" / "behavior-proof.md").write_text(
                "# Behavior proof map\n\n## Authority\nEvidence accounting only.\n",
                encoding="utf-8",
            )

            valid_codes = {finding.code for finding in validate(root, catalog)}
            self.assertNotIn("proof-map.authority", valid_codes)
            self.assertNotIn("proof-map.routing", valid_codes)

            # Deliberately falsify both mechanical boundaries. The map must not
            # promote itself to product authority or enter every task.
            entry["authority"] = "contract"
            entry["always"] = True
            falsified_codes = {finding.code for finding in validate(root, catalog)}
            self.assertIn("proof-map.authority", falsified_codes)
            self.assertIn("proof-map.routing", falsified_codes)

    def test_routing_reports_oversized_primary_without_orphaning_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"].append(
                {
                    "id": "camera-research",
                    "path": ".agentos/camera-research.md",
                    "title": "Camera experiment research",
                    "type": "evidence",
                    "authority": "evidence",
                    "status": "active",
                    "tags": ["camera", "experiment"],
                    "read_when": ["changing camera experiments"],
                    "paths": ["src/camera/**"],
                    "depends_on": ["invariants"],
                }
            )
            (root / ".agentos" / "camera-research.md").write_text(
                "# Camera research\n\n" + "measurement " * 2000,
                encoding="utf-8",
            )

            result = route_with_diagnostics(
                root,
                catalog,
                "change camera experiment",
                ["src/camera/capture.py"],
                500,
            )

            self.assertEqual(["camera-research"], [doc.id for doc in result.omitted])
            self.assertNotIn("invariants", [doc.id for doc in result.selected])
            self.assertIn("budget", result.omitted[0].omission_reason)

    def test_context_json_exposes_selected_and_omitted_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"].append(
                {
                    "id": "large-note",
                    "path": ".agentos/large-note.md",
                    "title": "Large specialist note",
                    "type": "evidence",
                    "authority": "evidence",
                    "status": "active",
                    "tags": ["specialist"],
                    "read_when": ["changing specialist behavior"],
                    "paths": [],
                    "depends_on": [],
                }
            )
            (root / ".agentos" / "large-note.md").write_text(
                "# Specialist\n\n" + "evidence " * 2000,
                encoding="utf-8",
            )
            (root / ".agentos" / "index.json").write_text(
                json.dumps(catalog),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    [
                        "context",
                        "change specialist behavior",
                        "--root",
                        str(root),
                        "--budget",
                        "500",
                        "--json",
                    ]
                )

            self.assertEqual(0, code)
            parsed = json.loads(output.getvalue())
            self.assertIn("selected", parsed)
            self.assertIn("selected_over_budget", parsed)
            self.assertEqual("agent", parsed["selected"][0]["change_control"])
            self.assertNotIn("omission_reason", parsed["selected"][0])
            self.assertEqual(["large-note"], [doc["id"] for doc in parsed["omitted"]])

    def test_change_control_defaults_by_authority_and_validates_overrides(self) -> None:
        self.assertEqual("review", effective_change_control({"authority": "contract"}))
        self.assertEqual("review", effective_change_control({"authority": "decision"}))
        self.assertEqual("agent", effective_change_control({"authority": "working"}))
        self.assertEqual(
            "protected",
            effective_change_control({"authority": "working", "change_control": "protected"}),
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"][0]["change_control"] = "silent-rewrite"
            codes = {finding.code for finding in validate(root, catalog)}
            self.assertIn("catalog.change-control", codes)

    def test_adaptation_preview_is_deterministic_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".agentos-kit").mkdir()
            (root / ".agentos-kit" / "ADAPTATION.md").write_text("# Adapt\n", encoding="utf-8")
            (root / ".agentos").mkdir()
            (root / ".agentos" / "seed-state.md").write_text(
                "Seed state: **unadapted**\n",
                encoding="utf-8",
            )
            (root / ".agentos" / "project.md").write_text("# AgentOS\n", encoding="utf-8")
            (root / ".agentos" / "state.md").write_text("# State\n", encoding="utf-8")
            (root / ".agentos" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
            (root / ".agentos" / "unindexed-cache.json").write_text("{}\n", encoding="utf-8")
            catalog = {
                "schema_version": 1,
                "project": "AgentOS",
                "documents": [
                    {
                        "id": "project",
                        "path": ".agentos/project.md",
                    },
                    {
                        "id": "state",
                        "path": ".agentos/state.md",
                    },
                    {
                        "id": "architecture",
                        "path": ".agentos/architecture.md",
                    },
                ],
            }
            (root / ".agentos" / "index.json").write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )
            (root / "AGENTS.md").write_text("# Master router\n", encoding="utf-8")
            before = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }

            preview = build_adaptation_preview(root, "FieldLens")

            after = {
                path.relative_to(root): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)
            self.assertFalse(preview["changes_applied"])
            self.assertIn(".agentos/architecture.md", preview["remove_master_only"])
            self.assertIn(".agentos/unindexed-cache.json", preview["remove_master_only"])
            self.assertIn(".agentos-kit/", preview["preserve"])
            self.assertIn("AGENTS.md", preview["replace_with_project_content"])

            output = io.StringIO()
            with redirect_stdout(output):
                code = main(
                    [
                        "adapt",
                        "--preview",
                        "--name",
                        "FieldLens",
                        "--root",
                        str(root),
                        "--json",
                    ]
                )
            self.assertEqual(0, code)
            self.assertFalse(json.loads(output.getvalue())["changes_applied"])

    def test_routing_evaluation_replays_observed_miss_and_noise_cases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            catalog = load_catalog(root)
            catalog["documents"].append(
                {
                    "id": "sync",
                    "path": ".agentos/sync.md",
                    "title": "Photo upload recovery",
                    "type": "subsystem",
                    "authority": "evidence",
                    "status": "active",
                    "tags": ["photo", "upload", "recovery"],
                    "read_when": ["changing photo upload recovery"],
                    "paths": ["src/sync/**"],
                    "depends_on": ["invariants"],
                }
            )
            (root / ".agentos" / "sync.md").write_text("# Sync\n", encoding="utf-8")
            save_catalog(root, catalog)
            evaluation = {
                "schema_version": 1,
                "cases": [
                    {
                        "id": "miss-2026-09-10-photo-retry",
                        "origin": "Observed when a photo retry task omitted the sync note.",
                        "task": "repair photo upload recovery",
                        "paths": ["src/sync/queue.py"],
                        "budget": 2000,
                        "expect_selected": ["sync", "invariants"],
                        "expect_absent": ["questions"],
                    }
                ],
            }
            evaluation_path = root / ".agentos" / "routing-evaluations.json"
            evaluation_path.write_text(json.dumps(evaluation), encoding="utf-8")

            results = evaluate_routing_cases(root, ".agentos/routing-evaluations.json")
            self.assertEqual(1, len(results))
            self.assertTrue(results[0].passed)
            with redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "eval-routing",
                        "--root",
                        str(root),
                        "--file",
                        ".agentos/routing-evaluations.json",
                    ]
                )
            self.assertEqual(0, code)

            evaluation["cases"][0]["expect_selected"] = ["questions"]
            evaluation_path.write_text(json.dumps(evaluation), encoding="utf-8")
            failed = evaluate_routing_cases(root, ".agentos/routing-evaluations.json")
            self.assertFalse(failed[0].passed)
            self.assertIn("expected questions to be selected", failed[0].failures)

    def test_catalog_is_plain_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            parsed = json.loads((root / ".agentos" / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(1, parsed["schema_version"])

    def test_starter_catalog_uses_writer_format(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            path = root / ".agentos" / "index.json"
            before = path.read_text(encoding="utf-8")

            save_catalog(root, load_catalog(root))

            self.assertEqual(before, path.read_text(encoding="utf-8"))

    def test_new_plan_is_indexed_resumable_and_routable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize(root, "Sample")
            with redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "new",
                        "plan",
                        "Repair upload retries",
                        "--root",
                        str(root),
                        "--tag",
                        "upload",
                        "--path",
                        "src/sync/**",
                        "--depends-on",
                        "invariants",
                    ]
                )
            self.assertEqual(0, code)
            catalog = load_catalog(root)
            findings = validate(root, catalog)
            self.assertEqual([], [finding for finding in findings if finding.level == "error"])
            ids = [
                doc.id
                for doc in route(root, catalog, "repair upload retries", ["src/sync/queue.py"], 2000)
            ]
            self.assertIn("plan-0001", ids)
            self.assertIn("invariants", ids)


if __name__ == "__main__":
    unittest.main()

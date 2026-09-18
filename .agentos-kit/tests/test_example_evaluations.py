from __future__ import annotations

import unittest
from pathlib import Path

from agentos.catalog import load_catalog, route, validate
from agentos.routing_eval import evaluate_routing_cases


ROOT = Path(__file__).resolve().parents[1] / "examples" / "trailcache"


class TrailCacheContinuityEvaluation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog(ROOT)

    def ids(self, task: str, path: str = "") -> tuple[list[str], int]:
        docs = route(ROOT, self.catalog, task, [path] if path else [], 2000)
        return [doc.id for doc in docs], sum(doc.estimated_tokens for doc in docs)

    def test_example_catalog_is_valid(self) -> None:
        self.assertEqual([], validate(ROOT, self.catalog))

    def test_handoff_pack_recovers_active_upload_work(self) -> None:
        ids, tokens = self.ids("resume photo upload retry work", "src/sync/queue.ts")
        self.assertEqual(
            {"project", "state", "plan-0007", "sync", "invariants", "decision-0001", "failed-0001"},
            set(ids),
        )
        self.assertLessEqual(tokens, 2000)
        self.assertNotIn("persona-screen-reader", ids)
        self.assertEqual(["project", "state", "plan-0007", "sync"], ids[:4])

    def test_small_ui_task_does_not_load_sync_history(self) -> None:
        ids, tokens = self.ids("change the journal list empty-state copy", "src/journal/EntryList.tsx")
        self.assertLessEqual(tokens, 1400)
        self.assertNotIn("sync", ids)
        self.assertNotIn("failed-0001", ids)
        self.assertNotIn("decision-0001", ids)

    def test_observed_routing_failure_stays_fixed(self) -> None:
        results = evaluate_routing_cases(ROOT, ".agentos/routing-evaluations.json")
        self.assertEqual(1, len(results))
        self.assertTrue(results[0].passed, results[0].failures)

    def test_decision_memory_blocks_destructive_reversal(self) -> None:
        ids, tokens = self.ids("make server absence delete local entries", "src/sync/reconcile.ts")
        self.assertIn("decision-0001", ids)
        self.assertIn("invariants", ids)
        self.assertLess(ids.index("decision-0001"), ids.index("sync"))
        self.assertLessEqual(tokens, 2000)

    def test_failed_approach_is_found_for_upload_credentials(self) -> None:
        ids, _ = self.ids("persist signed upload URL and retry credentials", "src/sync/queue.ts")
        self.assertIn("failed-0001", ids)
        self.assertIn("plan-0007", ids)

    def test_feedback_routes_to_evidence_insight_and_persona(self) -> None:
        ids, tokens = self.ids(
            "investigate entry disappearing after save under a filter", "src/journal/EntryList.tsx"
        )
        self.assertIn("feedback-0042", ids)
        self.assertIn("insight-hidden-saved-entry", ids)
        self.assertIn("persona-distracted-first-run", ids)
        self.assertLessEqual(tokens, 2000)

    def test_framework_lesson_stays_a_proposal(self) -> None:
        ids, tokens = self.ids("review AgentOS generated code routing proposal")
        self.assertIn("upstream-0003", ids)
        entry = next(entry for entry in self.catalog["documents"] if entry["id"] == "upstream-0003")
        self.assertEqual("draft", entry["status"])
        self.assertLessEqual(tokens, 2000)


if __name__ == "__main__":
    unittest.main()

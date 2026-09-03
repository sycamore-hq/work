#!/usr/bin/env python3
"""Prove the ledger classifies the way the record says."""

import importlib.machinery
import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_loader(
    "work_board",
    importlib.machinery.SourceFileLoader(
        "work_board", str(ROOT / "scripts" / "work-board")
    ),
)
work_board = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(work_board)

_roadmap_spec = importlib.util.spec_from_loader(
    "gh_project_roadmap",
    importlib.machinery.SourceFileLoader(
        "gh_project_roadmap", str(ROOT / "scripts" / "gh-project-roadmap")
    ),
)
roadmap = importlib.util.module_from_spec(_roadmap_spec)
assert _roadmap_spec.loader is not None
_roadmap_spec.loader.exec_module(roadmap)

LEDGER = work_board.load_ledger(ROOT / "work.json")
MODEL = work_board.model(LEDGER, "test")


class LedgerShape(unittest.TestCase):
    def test_roster_is_the_org(self):
        self.assertEqual(
            LEDGER["roster"],
            [
                "berea",
                "crossr-harness",
                "crossr-loops",
                "crossr-skills",
                "crossr-web-landing",
                "work",
            ],
        )

    def test_ids_unique(self):
        ids = [i["id"] for i in LEDGER["items"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_item_names_a_roster_repo(self):
        roster = set(LEDGER["roster"])
        for item in LEDGER["items"]:
            self.assertTrue(item["repos"], item["id"])
            for repo in item["repos"]:
                self.assertIn(repo, roster, item["id"])

    def test_blockers_exist(self):
        ids = {i["id"] for i in LEDGER["items"]}
        for item in LEDGER["items"]:
            for dep in item.get("blocked_by") or []:
                self.assertIn(dep, ids, f"{item['id']} waits on unknown {dep}")

    def test_every_item_has_a_unique_issue(self):
        issues = [i["issue"] for i in LEDGER["items"]]
        self.assertTrue(all(isinstance(n, int) and n >= 2 for n in issues))
        self.assertEqual(len(issues), len(set(issues)))

    def test_project_seed_target(self):
        project = LEDGER["github_project"]
        self.assertEqual(project["owner"], "sycamore-hq")
        self.assertEqual(project["title"], "sycamore-hq work")
        self.assertEqual(
            project["url"], "https://github.com/orgs/sycamore-hq/projects/2"
        )


class Classification(unittest.TestCase):
    def test_counts_match_literal_status_strings(self):
        raw = Counter(i["status"] for i in LEDGER["items"])
        self.assertEqual(MODEL["counts"][work_board.TODO], raw["todo"])
        self.assertEqual(MODEL["counts"][work_board.ACTIVE], raw["in_progress"])
        self.assertEqual(MODEL["counts"][work_board.BLOCKED], raw["blocked"])
        self.assertEqual(MODEL["counts"][work_board.PARKED], raw["parked"])
        self.assertEqual(MODEL["counts"][work_board.DONE], raw.get("done", 0))

    def test_pr5c_done_unblocks_5d_5e_5g(self):
        pr5c = next(i for i in LEDGER["items"] if i["id"] == "pr5c")
        self.assertEqual(pr5c["status"], "done")
        ids = {i["id"] for i in MODEL["startable"]}
        self.assertNotIn("pr5c", ids)
        for unblocked in ("pr5d", "pr5e", "landing-rtl", "landing-pages"):
            self.assertIn(unblocked, ids)

    def test_pr6_waits_on_pr5f(self):
        ids = {i["id"] for i in MODEL["startable"]}
        self.assertNotIn("pr6", ids)
        self.assertIn("pr6", {i["id"] for i in MODEL["planned"]})
        pr6 = next(i for i in LEDGER["items"] if i["id"] == "pr6")
        self.assertEqual(pr6["blocked_by"], ["pr5f"])

    def test_pr7_waits_on_pr6(self):
        self.assertNotIn("pr7", {i["id"] for i in MODEL["startable"]})

    def test_held_includes_berea_003_and_graph_runner(self):
        ids = {i["id"] for i in MODEL["held"]}
        self.assertIn("berea-003", ids)
        self.assertIn("graph-runner", ids)

    def test_parked_is_not_startable(self):
        self.assertNotIn("graph-runner", {i["id"] for i in MODEL["startable"]})

    def test_work_00_is_in_flight(self):
        ids = {i["id"] for i in MODEL["in_flight"]}
        self.assertIn("work-00", ids)
        self.assertNotIn("pr5c", ids)


class Sequence(unittest.TestCase):
    @staticmethod
    def graph(**edges):
        return {k: {"id": k, "blocked_by": list(v)} for k, v in edges.items()}

    def test_depth_counts_the_longest_chain(self):
        by_id = self.graph(a=(), b=("a",), c=("b",))
        self.assertEqual(roadmap.depth(by_id["c"], by_id), 2)

    def test_depth_walks_a_diamond_without_crying_cycle(self):
        by_id = self.graph(x=(), c=("x",), d=("c",), e=("c",), f=("d", "e"))
        self.assertEqual(roadmap.depth(by_id["f"], by_id), 3)

    def test_depth_rejects_a_real_cycle(self):
        by_id = self.graph(a=("b",), b=("a",))
        with self.assertRaises(SystemExit):
            roadmap.depth(by_id["a"], by_id)

    def test_ledger_has_no_cycles(self):
        by_id = {i["id"]: i for i in LEDGER["items"]}
        for item in LEDGER["items"]:
            roadmap.depth(item, by_id)


class Render(unittest.TestCase):
    def test_markdown_names_the_roster(self):
        text = work_board.render_markdown(MODEL)
        self.assertIn("berea", text)
        self.assertIn("`pr5d`", text)
        self.assertIn("#17", text)
        self.assertNotIn("{{", text)

    def test_html_has_no_template_holes(self):
        page = work_board.render_html(MODEL)
        self.assertNotIn("{{", page)
        self.assertIn("pr5c", page)
        self.assertIn("Startable now", page)

    def test_json_board_shape(self):
        items = MODEL["board_items"]
        self.assertEqual(len(items), len(LEDGER["items"]))
        self.assertEqual(set(items[0]), {"id", "title", "status"})

    def test_ledger_is_valid_json(self):
        json.loads((ROOT / "work.json").read_text())


if __name__ == "__main__":
    unittest.main()

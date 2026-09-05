#!/usr/bin/env python3
"""Prove the ledger classifies the way the record says.

Every check here is an invariant over whatever work.json says today. No test
names a ledger item, so a status flip edits the record, not this file.
"""

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
ITEMS = LEDGER["items"]
BY_ID = {i["id"]: i for i in ITEMS}
STATUSES = {
    work_board.DONE,
    work_board.ACTIVE,
    work_board.TODO,
    work_board.BLOCKED,
    work_board.PARKED,
}


def ids(items: list[dict]) -> set[str]:
    return {i["id"] for i in items}


def blockers(item: dict) -> list[str]:
    return item.get("blocked_by") or []


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
        listed = [i["id"] for i in ITEMS]
        self.assertEqual(len(listed), len(set(listed)))

    def test_every_item_names_a_roster_repo(self):
        roster = set(LEDGER["roster"])
        for item in ITEMS:
            self.assertTrue(item["repos"], item["id"])
            for repo in item["repos"]:
                self.assertIn(repo, roster, item["id"])

    def test_every_status_is_a_known_word(self):
        for item in ITEMS:
            self.assertIn(item["status"], STATUSES, item["id"])

    def test_blockers_exist(self):
        for item in ITEMS:
            for dep in blockers(item):
                self.assertIn(dep, BY_ID, f"{item['id']} waits on unknown {dep}")

    def test_no_item_blocks_itself(self):
        for item in ITEMS:
            self.assertNotIn(item["id"], blockers(item))

    def test_blocker_graph_is_acyclic(self):
        def walk(ident: str, path: tuple[str, ...]) -> None:
            self.assertNotIn(ident, path, f"cycle: {' -> '.join(path + (ident,))}")
            for dep in blockers(BY_ID[ident]):
                walk(dep, path + (ident,))

        for item in ITEMS:
            walk(item["id"], ())

    def test_every_item_has_a_unique_issue(self):
        issues = [i["issue"] for i in ITEMS]
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
    """Startable ⇔ todo, not parked, every blocker done. Lanes partition."""

    def test_counts_match_literal_status_strings(self):
        raw = Counter(i["status"] for i in ITEMS)
        for status in STATUSES:
            self.assertEqual(MODEL["counts"][status], raw.get(status, 0), status)

    def test_startable_items_are_todo_unparked_and_unblocked(self):
        done = ids([i for i in ITEMS if i["status"] == work_board.DONE])
        for item in MODEL["startable"]:
            self.assertEqual(item["status"], work_board.TODO, item["id"])
            self.assertNotEqual(item.get("kind"), work_board.PARKED, item["id"])
            self.assertTrue(set(blockers(item)) <= done, item["id"])

    def test_every_unblocked_todo_is_startable(self):
        done = ids([i for i in ITEMS if i["status"] == work_board.DONE])
        expected = {
            i["id"]
            for i in ITEMS
            if i["status"] == work_board.TODO
            and i.get("kind") != work_board.PARKED
            and set(blockers(i)) <= done
        }
        self.assertEqual(ids(MODEL["startable"]), expected)

    def test_waiting_items_have_an_unmet_blocker(self):
        done = ids([i for i in ITEMS if i["status"] == work_board.DONE])
        for item in MODEL["planned"]:
            self.assertEqual(item["status"], work_board.TODO, item["id"])
            self.assertFalse(work_board.is_held(item), item["id"])
            self.assertTrue(
                set(blockers(item)) - done, f"{item['id']} is waiting on nothing"
            )

    def test_startable_and_waiting_partition_unheld_todo(self):
        todo = ids(
            [
                i for i in ITEMS
                if i["status"] == work_board.TODO and not work_board.is_held(i)
            ]
        )
        startable = ids(MODEL["startable"])
        waiting = ids(MODEL["planned"])
        self.assertEqual(startable & waiting, set())
        self.assertEqual(startable | waiting, todo)

    def test_in_flight_is_exactly_in_progress(self):
        self.assertEqual(
            ids(MODEL["in_flight"]),
            ids([i for i in ITEMS if i["status"] == work_board.ACTIVE]),
        )

    def test_held_is_exactly_blocked_parked_or_parked_kind(self):
        self.assertEqual(
            ids(MODEL["held"]),
            ids(
                [
                    i for i in ITEMS
                    if i["status"] in work_board.HELD
                    or i.get("kind") == work_board.PARKED
                ]
            ),
        )

    def test_both_views_hold_a_parked_kind_todo(self):
        """A todo with kind parked lands in Held on the board and the Project."""
        item = {
            "id": "x",
            "title": "x",
            "status": work_board.TODO,
            "kind": work_board.PARKED,
            "repos": ["work"],
        }
        ledger = {"roster": ["work"], "items": [item]}
        m = work_board.model(ledger, "test")
        self.assertEqual(ids(m["held"]), {"x"})
        self.assertEqual(m["startable"], [])
        self.assertEqual(m["planned"], [])
        self.assertEqual(roadmap.lane_of(item, set()), "Held")
        self.assertIn("### Held", work_board.render_markdown(m))
        self.assertNotIn("Waiting on something", work_board.render_markdown(m))

    def test_lanes_cover_every_open_item_once(self):
        lanes = [
            ids(MODEL["startable"]),
            ids(MODEL["in_flight"]),
            ids(MODEL["held"]),
            ids(MODEL["planned"]),
        ]
        union = set().union(*lanes)
        self.assertEqual(sum(len(l) for l in lanes), len(union))
        open_items = ids([i for i in ITEMS if i["status"] != work_board.DONE])
        self.assertEqual(union, open_items)

    def test_nothing_waits_on_an_unfinished_blocker_and_starts(self):
        unfinished = ids([i for i in ITEMS if i["status"] != work_board.DONE])
        for item in MODEL["startable"]:
            self.assertEqual(set(blockers(item)) & unfinished, set(), item["id"])


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
    def test_markdown_names_roster_and_every_open_item(self):
        text = work_board.render_markdown(MODEL)
        for repo in LEDGER["roster"]:
            self.assertIn(repo, text)
        for item in ITEMS:
            if item["status"] == work_board.DONE:
                continue
            self.assertIn(f"`{item['id']}`", text)
            self.assertIn(f"#{item['issue']}", text)
        self.assertNotIn("{{", text)

    def test_markdown_counts_row_matches_model(self):
        text = work_board.render_markdown(MODEL)
        c = MODEL["counts"]
        row = (
            f"| {len(MODEL['startable'])} | {c[work_board.ACTIVE]} | "
            f"{c[work_board.BLOCKED]} | {c[work_board.PARKED]} | "
            f"{c[work_board.TODO]} | {c[work_board.DONE]} |"
        )
        self.assertIn(row, text)

    def test_html_names_every_item_and_has_no_template_holes(self):
        page = work_board.render_html(MODEL)
        self.assertNotIn("{{", page)
        self.assertIn("Startable now", page)
        for item in ITEMS:
            if item["status"] == work_board.DONE:
                continue
            self.assertIn(item["id"], page)

    def test_json_board_shape(self):
        items = MODEL["board_items"]
        self.assertEqual(len(items), len(ITEMS))
        for entry in items:
            self.assertEqual(set(entry), {"id", "title", "status"})

    def test_ledger_is_valid_json(self):
        json.loads((ROOT / "work.json").read_text())


if __name__ == "__main__":
    unittest.main()

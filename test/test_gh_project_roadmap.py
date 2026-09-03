#!/usr/bin/env python3
"""Prove the roadmap sync derives labels from the ledger, not by hand."""

import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_loader(
    "gh_project_roadmap",
    importlib.machinery.SourceFileLoader(
        "gh_project_roadmap", str(ROOT / "scripts" / "gh-project-roadmap")
    ),
)
roadmap = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(roadmap)

LEDGER = roadmap.load_ledger()
ITEMS = [i for i in LEDGER["items"] if isinstance(i, dict)]
DONE = {i["id"] for i in ITEMS if i.get("status") == "done"}


def item(status: str, *, blocked_by: list[str] | None = None, kind: str = "planned") -> dict:
    return {
        "id": "x",
        "status": status,
        "kind": kind,
        "repos": ["crossr-skills"],
        "blocked_by": blocked_by or [],
    }


class StateLabel(unittest.TestCase):
    def test_in_progress_uses_the_hyphen_spelling(self):
        self.assertEqual(roadmap.state_label(item("in_progress"), set()), "in-progress")

    def test_held_statuses_are_their_own_word(self):
        self.assertEqual(roadmap.state_label(item("blocked"), set()), "blocked")
        self.assertEqual(roadmap.state_label(item("parked"), set()), "parked")

    def test_done_carries_no_state_label(self):
        self.assertIsNone(roadmap.state_label(item("done"), set()))

    def test_todo_is_waiting_until_every_blocker_is_done(self):
        waiting = item("todo", blocked_by=["a", "b"])
        self.assertEqual(roadmap.state_label(waiting, {"a"}), "waiting")
        self.assertEqual(roadmap.state_label(waiting, {"a", "b"}), "todo")


class DesiredLabels(unittest.TestCase):
    def test_kind_repos_and_state(self):
        got = roadmap.desired_labels(
            {"id": "x", "status": "todo", "kind": "hygiene", "repos": ["work", "berea"]},
            set(),
        )
        self.assertEqual(got, {"hygiene", "repo:work", "repo:berea", "todo"})

    def test_parked_kind_and_status_collapse_to_one_label(self):
        got = roadmap.desired_labels(item("parked", kind="parked"), set())
        self.assertEqual(got, {"parked", "repo:crossr-skills"})


class Reconcile(unittest.TestCase):
    def test_drops_stale_state_words_and_legacy_spelling(self):
        current = {"planned", "in_progress", "in-progress", "todo", "repo:crossr-skills"}
        desired = {"planned", "repo:crossr-skills"}
        self.assertEqual(roadmap.reconcile_labels(current, desired), desired)

    def test_keeps_labels_the_ledger_does_not_own(self):
        current = {"good first issue", "security", "todo"}
        desired = {"hygiene", "repo:work", "waiting"}
        got = roadmap.reconcile_labels(current, desired)
        self.assertEqual(got, {"good first issue", "security"} | desired)

    def test_replaces_repo_labels_when_repos_change(self):
        current = {"repo:crossr-loops", "planned", "todo"}
        desired = {"repo:crossr-skills", "planned", "todo"}
        self.assertEqual(roadmap.reconcile_labels(current, desired), desired)

    def test_no_change_is_identity(self):
        current = {"planned", "repo:work", "todo", "extra"}
        desired = {"planned", "repo:work", "todo"}
        self.assertEqual(roadmap.reconcile_labels(current, desired), current)


class LedgerWide(unittest.TestCase):
    def test_every_open_item_gets_exactly_one_state_word(self):
        for entry in ITEMS:
            labels = roadmap.desired_labels(entry, DONE)
            states = labels & roadmap.STATE_LABELS
            if entry.get("status") == "done":
                self.assertEqual(states, set(), entry["id"])
            else:
                self.assertEqual(len(states), 1, f"{entry['id']}: {sorted(states)}")

    def test_every_item_gets_a_repo_label_per_repo(self):
        for entry in ITEMS:
            labels = roadmap.desired_labels(entry, DONE)
            repos = {n for n in labels if n.startswith(roadmap.REPO_LABEL_PREFIX)}
            self.assertEqual(len(repos), len(entry["repos"]), entry["id"])

    def test_desired_labels_are_all_managed(self):
        for entry in ITEMS:
            for name in roadmap.desired_labels(entry, DONE):
                self.assertTrue(roadmap.is_managed_label(name), f"{entry['id']}: {name}")


class IssueState(unittest.TestCase):
    def test_done_closes(self):
        self.assertEqual(roadmap.desired_issue_state(item("done")), "closed")

    def test_every_other_status_stays_open(self):
        for status in ("todo", "in_progress", "blocked", "parked"):
            self.assertEqual(roadmap.desired_issue_state(item(status)), "open", status)

    def test_ledger_wide_closed_set_is_exactly_done(self):
        closed = {i["id"] for i in ITEMS if roadmap.desired_issue_state(i) == "closed"}
        self.assertEqual(closed, DONE)

if __name__ == "__main__":
    unittest.main()

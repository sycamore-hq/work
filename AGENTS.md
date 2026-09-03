# AGENTS.md

## Plan Mode

- Make every plan extremely concise. Sacrifice grammar for scannability.
- At the end of each plan, give a bulleted list of unresolved questions.
- Always follow the Plan → Execute → Test → Commit loop.

## This remote

Org work log for `sycamore-hq`. Outstanding and planned items across every
remote. Owns no product law.

- Record: `work.json`
- View: `just status` / `just status-html` → `docs/board.html`
- This repo's own work: `features.json` + `progress.md`
- Process law: [HARNESS-SPEC.md](https://github.com/sycamore-hq/crossr-harness/blob/main/HARNESS-SPEC.md)

Do not copy skill text, loop law, or the harness spec into this tree.

## Skills

Use catalog skills from a `crossr-skills` checkout when writing or briefing.

- `code-writer`
- `chief-of-staff` (read this ledger per project via `--root`)
- `voice-dna` for anything a human reads

## Ledger rules

- `work.json` is the record. The HTML is a view. The GitHub Project is a view.
  `just project-roadmap` refreshes Status, Lane, sequence dates, issue
  `blocked_by`, and issue labels (kind, `repo:<name>`, one state word) from
  this ledger. Never edit those labels by hand.
- An item the files do not name is not on the board.
- Status words: `done`, `in_progress`, `todo`, `blocked`, `parked`.
- Startable means `todo`, no unmet `blocked_by`, not parked.
- Refresh `docs/board.html` after every ledger edit (`just status-html`).
- A project that cannot be read is unread, never on track. Say so in `notes`.

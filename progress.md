# sycamore-hq/work — progress

## board — work-00 (IN PROGRESS)

Stand up the org ledger. `work.json` is the record. The HTML and the GitHub
Project are views.

Roster read 2026-09-03 from origin after fetch:

- berea
- crossr-harness
- crossr-loops
- crossr-skills
- crossr-web-landing
- work (this remote)

Issues #2–#19 are the Project cards. Project
https://github.com/orgs/sycamore-hq/projects/2.

In progress (started 2026-09-03): `loops-lockfile` #9,
`dashboard-phase` #10, `berea-002` #13, plus `work-00` #15.

`pr5c` #2 done 2026-09-03: crossr-skills#120 rebase-merged as
`4b8601e`..`507c509`; acceptance greps zero and `harness-validate` green on
`507c509`; tag `v1-one-law` (`88d9ee2`) peels to `507c509` on the skills
remote. `pr5d` #17, `pr5e` #18, `landing-rtl` #7 are startable.

Tests assert ledger invariants (startable ⇔ todo, unparked, blockers done;
lanes partition the ledger; blocker graph acyclic; renderers name every
open item), not named ids. A status flip edits the record, not the suite.

Roadmap view is a view of this ledger (`just project-roadmap`): Status, Lane,
sequence dates, and GitHub issue `blocked_by` edges. Dates are topology, not
deadlines. Next after the four in-flight items: `landing-pages` #3,
`pr5-record` #5, `gan-close-4b` #6, `landing-pins` #8.

Plan audit 2026-09-03 against skills `origin/main` `0bd2c40`:

- Split plan: complete. Leftovers already on the board (`landing-pages`,
  `graph-runner`). Custom domain is a decision, not a card.
- Mitchell contract: landed (`mitchell-decomposition` completed). Not a card.
- GAN PR 0–4: landed. Close-out is `gan-close-4b`.
- PR 5 is the 7-PR prompt-set stack. 5a/5b/5c on main. Board now names 5c–5g
  (`pr5c`, `pr5d` #17, `pr5e` #18, `pr5f` #19, `landing-rtl` 5g). `pr5-record`
  is the overdue 5a/5b tracker note.
- PR 6 waits on `pr5f`. PR 7 waits on PR 6.
- GAN §5 "also worth doing" is not a named unit. Not on the board.

## Verification Status

- `python3 -m unittest discover -s test -v` (run before merge)
- `just status` prints startable items from the ledger

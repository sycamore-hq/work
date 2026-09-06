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

In progress (started 2026-09-03): `work-00` #15.

`pr5-record` #5 done 2026-09-06.
[crossr-skills#123](https://github.com/sycamore-hq/crossr-skills/pull/123)
rebase-merged as `3f236dc`..`e3434f1`. `pr5a`/`pr5b`/`pr5c` rows; phase
stays `in_progress` with `pending` `pr5d`. Prompt-set 5a/5b/5c Landed.
`pr5f` #19 remains the PR 5 close.

`gan-close-4b` #6 done 2026-09-06.
[crossr-loops#10](https://github.com/sycamore-hq/crossr-loops/pull/10)
rebase-merged as `2764138`..`5f31cd8`.
[crossr-harness#9](https://github.com/sycamore-hq/crossr-harness/pull/9)
rebase-merged as `310f0ff`..`c974c8b`. Phase is `completed` on those two.
Skills 0–4b children were already done. The phase stays open there
because PR 5 continues (`pr5-record` #5 / skills#123).

`dashboard-phase` #10 done 2026-09-04.
[crossr-harness#7](https://github.com/sycamore-hq/crossr-harness/pull/7)
rebase-merged as `66bb380`..`9b2ee5a`. `feature_units()` counts a leftover
`in_progress` phase. That was the generator bug. Closing the phase is #6.

`loops-lockfile` #9 done 2026-09-06. The loops work landed 2026-09-03:
[crossr-loops#8](https://github.com/sycamore-hq/crossr-loops/pull/8)
rebase-merged as `d9679e1`..`f4b5ba3`. Consumer pin, same contract as
harness and skills. `lockfile.toml` is `loops = "v1-cards"`.

`berea-002` #13 done 2026-09-06: [berea#9](https://github.com/sycamore-hq/berea/pull/9)
rebase-merged as `f62e1d6`..`f03473e`. Reviewed is deny-closed. INDEX:
`002-memory-notes | done | later | 0/4`. `bun run check` + CI green on
`f03473e`.

`pr5d` #17 done 2026-09-05:
[crossr-loops#9](https://github.com/sycamore-hq/crossr-loops/pull/9)
rebase-merged as `6f8e4e6`..`cea6e59`. Tests, `graphs-verify`,
`verify-protocol`, and `verify-skill-refs` (skills `v1-one-law` at
`507c509`) green on `cea6e59`. Tag `v1-one-law-consumers` (`69a05d2`)
peels to `cea6e59` on the loops remote.

`pr5e` #18 done 2026-09-06:
[crossr-harness#8](https://github.com/sycamore-hq/crossr-harness/pull/8)
rebase-merged as `274e315`..`0159561`. Pins `v1-one-law` /
`v1-one-law-consumers`. `books` is a disclosure filter; no-book remotes
load `code-writer` / the gate card alone. Smoke PASS on `0159561`.
`pr5f` #19 is startable.

`berea-003` #4 done 2026-09-05: [berea#8](https://github.com/sycamore-hq/berea/pull/8)
rebase-merged as `ec82658`..`bb4457e`. T020–T090 checked. INDEX:
`003 done | later | 0/10`. Article VIII amended so a finished spec is later.

`pr5c` #2 done 2026-09-03: crossr-skills#120 rebase-merged as
`4b8601e`..`507c509`; acceptance greps zero and `harness-validate` green on
`507c509`; tag `v1-one-law` (`88d9ee2`) peels to `507c509` on the skills
remote.

`landing-rtl` #7 done 2026-09-06:
[crossr-web-landing#10](https://github.com/sycamore-hq/crossr-web-landing/pull/10)
rebase-merged as `08a65f9`..`211a704`. Live-copy tests first. Door
HTML drops rust-team-lead, featured pills are decision 7, pins on the
door are `v1-gan-layers` / `v1-cards`. Check green on `211a704`.

`landing-pins` #8 done 2026-09-06:
[crossr-web-landing#11](https://github.com/sycamore-hq/crossr-web-landing/pull/11)
rebase-merged as `feb9f0a`..`1002175`. README and book bootstrap.md
name `v1-gan-layers` / `v1-cards`. Graphs are in `v1-cards`. Charter
freeze still names v0. Check green on `1002175`.

`landing-pages` #3 done 2026-09-05. The host was already Actions-backed.
The two web-05 deploys on `39084fd` 404'd because Pages was not ready.
Re-ran Deploy CrossR door
([33996527031](https://github.com/sycamore-hq/crossr-web-landing/actions/runs/33996527031)).
https://sycamore-hq.github.io/crossr-web-landing/ and `/docs/` return 200.
The skills stub can keep pointing there.

`just project-roadmap` now owns issue labels and open/closed state too.
Labels: kind, `repo:<name>` per repo, one state word (`todo` / `waiting` /
`in-progress` / `blocked` / `parked`; done carries none). State: done
closes as completed, anything else reopens. The git repository wins every
vote; a hand-closed issue whose ledger item is still open comes back (#9
at time of writing). Managed labels are replaced from the ledger, anything
else on the issue is left alone. Pure derivation + reconcile are
unit-tested; the `gh` half runs where org project write exists.

Tests assert ledger invariants (startable ⇔ todo, unparked, blockers done;
lanes partition the ledger; blocker graph acyclic; renderers name every
open item), not named ids. A status flip edits the record, not the suite.

Roadmap view is a view of this ledger (`just project-roadmap`): Status, Lane,
sequence dates, and GitHub issue `blocked_by` edges. Dates are topology, not
deadlines. Next after the in-flight items: `pr5f` #19.

Plan audit 2026-09-03 against skills `origin/main` `0bd2c40`:

- Split plan: complete. Leftover `landing-pages` is done. `graph-runner`
  stays parked. Custom domain is a decision, not a card.
- Mitchell contract: landed (`mitchell-decomposition` completed). Not a card.
- GAN PR 0–4: landed. Close-out `gan-close-4b` is done on loops and harness.
- PR 5 is the 7-PR prompt-set stack. 5a/5b/5c/5d/5e/5g on main. Board
  still names `pr5f` #19. `pr5-record` landed as skills#123.
- PR 6 waits on `pr5f`. PR 7 waits on PR 6.
- GAN §5 "also worth doing" is not a named unit. Not on the board.

## Verification Status

- `python3 -m unittest discover -s test -v` — 60 tests OK
- `python3 scripts/work-board --markdown` — startable 1 (`pr5f`), in progress 1 (`work-00`)

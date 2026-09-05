# work

Org work log for [sycamore-hq](https://github.com/sycamore-hq). Outstanding and
planned items across every remote. Owns no product law.

**Record:** [`work.json`](work.json)
**View:** [`docs/board.html`](docs/board.html) · `just status`

This is not CrossR and not Berea. Those remotes keep their own trackers.
This remote is the one place that names work that spans them, and work that
their trackers currently hide.

## Roster

| Remote | Role |
|---|---|
| [berea](https://github.com/sycamore-hq/berea) | Agent lineage. Specs are the writings. |
| [crossr-harness](https://github.com/sycamore-hq/crossr-harness) | Process, bootstrap, per-repo dashboard. |
| [crossr-loops](https://github.com/sycamore-hq/crossr-loops) | AVRIL / AXEL / BRICK. |
| [crossr-skills](https://github.com/sycamore-hq/crossr-skills) | Skills catalog. |
| [crossr-web-landing](https://github.com/sycamore-hq/crossr-web-landing) | Public CrossR door. |
| **work** (this) | Org ledger. |

## Commands

```bash
just status        # markdown
just status-html   # docs/board.html
just project-seed     # create/reuse the org GitHub Project (needs org project write)
just project-roadmap  # Status, Lane, dates, blocked_by, labels, open/closed, Roadmap + Next views
just project-roadmap --dry-run  # print planned label / open-closed changes, write nothing
just test
just check
```

## How an item lands here

1. It is outstanding or planned on a roster remote, **or** it is hygiene the
   per-repo tracker is lying about.
2. It has a stable `id`, a status word the renderer knows, and a `source`
   that a later reader can open.
3. `just status-html` is regenerated in the same commit.

Do not invent a second backlog. A GitHub Project is a view of `work.json`.
Issues [#2](https://github.com/sycamore-hq/work/issues/2)–[#19](https://github.com/sycamore-hq/work/issues/19) are the cards. Project: [sycamore-hq work](https://github.com/orgs/sycamore-hq/projects/2).

`just project-seed` creates or reuses that board (see
[`scripts/gh-project-seed`](scripts/gh-project-seed)). `just project-roadmap`
sets Status, Lane, sequence dates, and issue dependencies so the Project
Roadmap and Next views show what is outstanding and what waits on what. It
also rewrites each issue's managed labels (kind, `repo:<name>`, one state
word) and its open/closed state (done closes, anything else reopens) from
the ledger. `just project-roadmap --dry-run` prints the planned label and
open/closed changes and writes nothing.
`gh-project` is done.

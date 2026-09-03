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
just project-seed  # create/reuse the org GitHub Project (needs org project write)
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
Issues [#2](https://github.com/sycamore-hq/work/issues/2)–[#16](https://github.com/sycamore-hq/work/issues/16) are the cards.

`cursor[bot]` cannot create the Project (`createProjectV2` denied). An org
owner runs `just project-seed` (or the same commands in
[`scripts/gh-project-seed`](scripts/gh-project-seed)). That is item
`gh-project`.

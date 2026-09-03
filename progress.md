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

Seeded from the 2026-09-03 briefing plus `berea/specs/INDEX.md`. No open
GitHub issues or PRs on any remote. `gh project create` failed:
`cursor[bot]` lacks `createProjectV2` on the org. Recorded as `gh-project`.

## Verification Status

- `python3 -m unittest discover -s test -v` (run before merge)
- `just status` prints startable items from the ledger

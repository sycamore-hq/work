# sycamore-hq/work — org ledger

status:
    python3 scripts/work-board --markdown

status-html:
    python3 scripts/work-board --html --out docs/board.html

# Needs org project write. cursor[bot] cannot run this.
project-seed:
    bash scripts/gh-project-seed

# Status, dates, blocked_by, labels, issue state, Roadmap + Next views.
# --dry-run prints planned label and open/closed changes and writes nothing.
project-roadmap *args:
    python3 scripts/gh-project-roadmap {{args}}

test:
    python3 -m unittest discover -s test -v

check: test status

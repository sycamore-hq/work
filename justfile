# sycamore-hq/work — org ledger

default:
    @just --list

init:
    echo "work environment ready"

status:
    python3 scripts/work-board --markdown

status-html:
    python3 scripts/work-board --html --out docs/board.html

# Needs org project write. cursor[bot] cannot run this.
project-seed:
    bash scripts/gh-project-seed

# Status, dates, blocked_by, Roadmap + Next views.
project-roadmap:
    python3 scripts/gh-project-roadmap

test:
    python3 -m unittest discover -s test -v

check: test status

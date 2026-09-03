# sycamore-hq/work — org ledger

status:
    python3 scripts/work-board --markdown

status-html:
    python3 scripts/work-board --html --out docs/board.html

test:
    python3 -m unittest discover -s test -v

check: test status

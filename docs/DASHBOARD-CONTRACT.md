work — STATUS DASHBOARD CONTRACT (in-harness UI)

You are the agent doing the work in this project. This file tells you how to keep
its status view honest while you work. It is machine-facing.

PARAMETERS
  PROJECT_NAME     = work
  REPO             = sycamore-hq/work
  REFRESH          = just status
  PUBLISH          = just status-html
  DASHBOARD_FILE   = docs/board.html
  CONFIG           = dashboard.config.json
  SOURCES          = see SOURCES below
  CHECKPOINTS      = see CHECKPOINTS below

SOURCES OF TRUTH (read-only; the dashboard renders these, it never replaces them)
  Board          = work.json items[] (this remote's org ledger)
  Tracking file  = features.json (this remote's own phase only)
  Narrative log  = progress.md
  Status words   = done = done, completed
                   active = in_progress
                   held as themselves: blocked, parked
                   everything else counts as todo
  Startable      = status todo, kind not parked, every blocked_by id is done

CHECKPOINTS
  - After any work.json edit
  - After a roster remote's plan or features.json changes an item's facts
  - After a GitHub Project view is seeded or refreshed
  Refresh immediately. The window between the change and the refresh is the
  window in which the dashboard is lying.

RULES
  - Generated, never hand-written. Run PUBLISH. Do not hand-author DASHBOARD_FILE.
  - The dashboard is a view, not a record. work.json wins.
  - Report counts you read. If REFRESH shows zeros during known work, that is
    a defect in the ledger or the classifier.
  - Commit DASHBOARD_FILE with the ledger edit that changed it.

WHEN THE NUMBERS LOOK WRONG
  Per-repo `scripts/status-dashboard` totals count commits, not phases. That
  is why harness/loops/skills can print 100% while gan-layer-separation is
  still in_progress. This ledger names that as dashboard-phase. Do not "fix"
  it by inventing commit rows here.

FIRST ACTION
  Run `just status` and state the startable count before doing anything else.

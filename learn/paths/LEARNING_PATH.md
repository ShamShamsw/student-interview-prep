```markdown
# Learning Path (8-Week and 12-Week Tracks)

This guide tells you exactly what to do next in this repository, week by week.

Companion tracker: [LEARNING_PATH_CHECKLIST.md](../paths/LEARNING_PATH_CHECKLIST.md)

Beginner resources:
- [BEGINNER_START_HERE.md](../guides/BEGINNER_START_HERE.md)
- [WEEKLY_CONFIDENCE_CHECK.md](../checklists/WEEKLY_CONFIDENCE_CHECK.md)
- [GLOSSARY.md](../resources/GLOSSARY.md)
- [EXTERNAL_RESOURCES.md](../resources/EXTERNAL_RESOURCES.md)

## How to use this path

- Pick **one** track: 8-week (faster) or 12-week (steadier).
- Complete required problems first, then required project milestones.
- Do not skip weekly checkpoints.
- Use tests and CI as your completion gate.

---

## Track A: 8-Week Plan

### Week 1 — Core arrays/strings + setup habits

Problems:
- `01-two-sum.md`
- `02-valid-parentheses.md`
- `04-best-time-to-buy-and-sell-stock.md`
- `05-contains-duplicate.md`
- `06-valid-anagram.md`

Project milestone:
- Run and understand `sample-to-do-app/final/`.
- Start implementing TODOs in `sample-to-do-app/starter/app.py`.

Checkpoint:
- Explain two-sum and valid-parentheses from memory.
- Local tests/commands for the TODO app run successfully.

### Week 2 — Sliding window and two pointers

Problems:
- `11-longest-substring-without-repeating-characters.md`
- `12-longest-repeating-character-replacement.md`
- `13-permutation-in-string.md`
- `15-valid-palindrome.md`
- `16-two-sum-ii-input-array-is-sorted.md`

Project milestone:
- Finish `sample-to-do-app/starter/app.py`.
- Compare against final implementation.

Checkpoint:
- You can choose the right sliding-window template quickly.
- Starter TODO app is complete.

### Week 3 — Intervals and binary search patterns

Problems:
- `19-search-in-rotated-sorted-array.md`
- `20-find-minimum-in-rotated-sorted-array.md`
- `21-binary-search.md`
- `24-merge-intervals.md`
- `25-insert-interval.md`

Project milestone:
- Build `study-session-tracker/starter/app.py` end-to-end.

Checkpoint:
- You can derive binary search boundaries without trial-and-error.
- Study session tracker starter is complete.

### Week 4 — Linked lists and trees

Problems:
- `26-reverse-linked-list.md`
- `27-linked-list-cycle.md`
- `28-merge-two-sorted-lists.md`
- `29-valid-binary-search-tree.md`
- `30-binary-tree-level-order-traversal.md`

Project milestone:
- Start `interview-patterns-api/starter/app.py` TODO functions.

Checkpoint:
- You can solve linked-list pointer problems without visual confusion.
- API starter has at least two TODO functions complete.

### Week 5 — Graphs, heaps, and DP

Problems:
- `32-number-of-islands.md`
- `33-clone-graph.md`
- `34-kth-largest-element-in-an-array.md`
- `35-coin-change.md`
- `23-time-based-key-value-store.md`

Project milestone:
- Complete `interview-patterns-api/starter/app.py`.
- Run endpoint tests in `interview-patterns-api/tests/`.

Checkpoint:
- Endpoint tests pass locally.
- You can explain BFS vs DFS tradeoffs clearly.

### Week 6 — Start capstone (design-first)

Required docs:
- `languages/python/projects/interview-prep-capstone/docs/01-design-and-architecture.md`
- `languages/python/projects/interview-prep-capstone/docs/02-sprint-plan-agile.md`
- `languages/python/projects/interview-prep-capstone/docs/03-ai-and-resource-playbook.md`

Capstone milestone:
- Sprint 1 and Sprint 2 deliverables complete.

Checkpoint:
- Architecture and sprint plan are written before feature expansion.

### Week 7 — Capstone implementation + hardening

Capstone milestone:
- Complete recommendation and study-plan behavior in starter.
- Add/maintain endpoint tests.

Checkpoint:
- `pytest` passes for capstone tests.
- CI workflow passes on push/PR.

### Week 8 — Capstone closeout + interview simulation

Capstone milestone:
- Final cleanup, docs, retrospective.

Practice milestone:
- Simulate 2 interview rounds:
  - 1 easy + 1 medium each session
  - verbalize approach and complexity out loud

Checkpoint:
- You can demo your capstone and explain architecture decisions.

---

## Track B: 12-Week Plan

This is the same progression with more spacing, review, and recovery room.

### Weeks 1-2
- Foundations: problems 01-10
- Complete `sample-to-do-app` starter

### Weeks 3-4
- Sliding window + two pointers + binary search: problems 11-22
- Complete `study-session-tracker` starter

### Weeks 5-6
- Design/data structures/intervals: problems 23-35
- Complete `interview-patterns-api` starter and tests

### Weeks 7-8
- Capstone Sprint 1 and Sprint 2
- Focus on architecture, API boundaries, data model clarity

### Weeks 9-10
- Capstone Sprint 3 and Sprint 4
- Recommendation quality, reliability, and endpoint test depth

### Weeks 11-12
- Hardening, CI consistency, retrospective
- Mock interviews + targeted weak-topic remediation

---

## Weekly checkpoint template (copy each week)

- Completed problems:
- Problems I could not solve without hints:
- Project milestone completed:
- Tests run and results:
- Biggest blocker:
- What changed in my process this week:

---

## If you fall behind (catch-up protocol)

1. Keep project milestones; reduce problem count by 30% for one week.
2. Prioritize weak topics over random variety.
3. Use the AI playbook: isolate bug, create failing test, ask focused questions.
4. Recover by adding one extra focused session in the next week.

---

## Stuck? Troubleshoot and Re-approach

Use this sequence anytime you feel blocked on a problem or project task.

### 1) Diagnose the block type

- **Concept block**: you do not know which pattern applies.
- **Implementation block**: you know the pattern but code keeps failing.
- **Debug block**: code mostly works but edge cases break it.
- **Scope block**: task became too large and unclear.

### 2) 20-minute reset protocol

1. Write the exact goal in one sentence
2. Write expected input/output for one small example.
3. Shrink to the smallest failing case.
4. Add a quick test or assert for that case.
5. Try one small change only.

If still blocked after 20 focused minutes, escalate.

### 3) Re-approach patterns

- **For problems**: switch to template thinking (two pointers, sliding window, stack, binary search, DFS/BFS, DP).
- **For APIs/projects**: move logic out of endpoints into one small helper/service function and test it directly.
- **For failing tests**: rerun a single test first, then broaden once fixed.

### 4) Safe escalation ladder

1. Read your own failing code out loud.
2. Compare with one known-good solution in this repo.
3. Check official docs for the exact library behavior.
4. Ask AI with full context (goal, code, error, expected output).
5. Apply smallest fix and re-run tests.

### 5) Rules that prevent panic loops

- Do not rewrite everything at once.
- Do not skip tests just to "move on".
- Do not add new tools/frameworks while blocked.
- Always capture what failed and what changed.

### 6) When to move on

Move on and schedule a revisit if:
- you spent >90 minutes with no measurable progress,
- core weekly milestones are at risk,
- you can clearly document what remains unclear.

Use the next session to return with a fresh, smaller test case.

---

## Completion criteria for this repo

You are "repo complete" when:
- You solved at least 30/35 problems with explanation ability.
- You completed all starter projects.
- You completed the capstone and passed endpoint tests.
- You can explain 3 architecture tradeoffs from your capstone.
- You can complete medium-level problems under time pressure with clear reasoning.

```

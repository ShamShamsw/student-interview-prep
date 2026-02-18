# 03. AI and Resource Playbook (When You Are Stuck)

Use this workflow to get unstuck without losing ownership of the solution.

## 1) 15-minute solo rule

Before asking AI:
- reproduce the issue
- isolate failing input
- write what you expected vs observed

If still blocked after 15 focused minutes, escalate.

## 2) Ask high-quality AI questions

Include:
- clear goal
- current code snippet
- exact error/output
- constraints (framework/version)

Bad: "it doesn't work"
Good: "FastAPI endpoint returns 422 for valid payload in this model; why?"

## 3) Validate AI output safely

- run tests before and after
- prefer minimal diffs
- reject suggestions you cannot explain
- never merge code you do not understand

## 4) Trusted resources order

1. Official docs (FastAPI, SQLAlchemy, pytest)
2. Repository examples in this project
3. AI suggestions
4. Community posts/videos (as secondary)

## 5) Escalation ladder

When blocked:
1. simplify failing case
2. inspect logs and stacktrace
3. write a failing test first
4. ask AI with full context
5. compare with official docs
6. refactor smallest risky area

## 6) Prompt templates

### Debug prompt
"I have a failing endpoint in FastAPI. Goal: <goal>. Error: <error>. Input payload: <json>. Relevant code: <code>. Give me likely root causes and smallest safe fix."

### Design prompt
"I am implementing <feature> in a layered architecture. Current modules: <list>. Recommend boundaries and tradeoffs, but avoid adding new frameworks."

### Test prompt
"Given this function and constraints, propose 8 high-value tests including edge cases and one regression case."

## 7) Anti-patterns to avoid

- copy-pasting large AI output blindly
- architecture rewrites mid-sprint without reason
- chasing tool recommendations instead of requirements
- skipping tests to "move faster"

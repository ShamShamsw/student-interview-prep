# 02. Agile Sprint Plan (8-12 Weeks)

Use 2-week sprints. Choose either:
- **4 sprints** (8 weeks, faster pace), or
- **6 sprints** (12 weeks, steadier pace).

## Sprint rhythm

Each sprint includes:
- Planning (60-90 min)
- Build + test
- Mid-sprint checkpoint
- Demo + retrospective

## Sprint 0 (optional, 2-3 days)

- finalize architecture notes
- set up repository structure
- configure CI and baseline tests

## Sprint 1: Foundations

Goals:
- API scaffolding
- initial domain models
- health checks and baseline endpoints
- first test pipeline passing

Deliverables:
- running API
- starter data model
- CI green

## Sprint 2: Attempt tracking

Goals:
- create/read attempts
- progress aggregation by topic/difficulty
- validation + error handling

Deliverables:
- `/attempts` endpoints
- `/progress` summary endpoint
- unit + endpoint tests

## Sprint 3: Recommendations MVP

Goals:
- recommendation algorithm (next problems)
- review queue generation from attempt history
- deterministic, testable scoring rules

Deliverables:
- `/recommendations` endpoint
- documented scoring logic
- regression tests

## Sprint 4: Study plans + reliability

Goals:
- study plan creation and updates
- stronger test coverage for edge cases
- cleanup and refactor

Deliverables:
- `/study-plan` endpoints
- 80%+ meaningful coverage in core services

## Sprint 5 (only for 10-12 week track): Product hardening

Goals:
- persistence improvements
- observability and structured logging
- failure-mode handling

Deliverables:
- stable error handling strategy
- load/edge-case smoke checks

## Sprint 6 (only for 12 week track): Polish + capstone closeout

Goals:
- final demo narrative
- architecture retrospective
- future roadmap

Deliverables:
- release candidate
- postmortem document

## Backlog management

Use three columns minimum:
- Ready
- In Progress
- Done

Ticket format:
- user-facing outcome
- acceptance criteria
- test impact

## Definition of done (per ticket)

- implementation complete
- tests added/updated
- reviewed against architecture principles
- documented in sprint notes

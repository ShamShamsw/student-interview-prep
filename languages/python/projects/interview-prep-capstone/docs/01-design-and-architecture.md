# 01. Design and Architecture Before You Build

Do this section before writing significant code.

## 1) Product scope (MVP first)

Your MVP must include only:
- authentication placeholder (single-user mode acceptable for MVP)
- problem attempt logging
- progress tracking by topic/difficulty
- recommendation endpoint for next practice set

Do **not** add extras until MVP is stable.

## 2) Architecture principles

- **Separation of concerns**: API layer, service layer, repository layer.
- **Single responsibility**: each module has one reason to change.
- **Testability**: business logic should be testable without HTTP.
- **Observability**: predictable logs and clear error messages.

## 3) Suggested backend architecture

- `app/api/` — routers, request/response models
- `app/services/` — recommendation logic, scoring, scheduling
- `app/repositories/` — DB access patterns
- `app/domain/` — core entities and value objects
- `app/tests/` — unit + endpoint tests

## 4) Data model planning

Start with these entities:
- `User`
- `Problem`
- `Attempt`
- `StudyPlan`
- `ReviewQueueItem`

Design each table with:
- primary key
- created/updated timestamps
- minimal required fields only

## 5) API design rules

- Use RESTful naming (`/attempts`, `/progress`, `/recommendations`).
- Return consistent error envelopes.
- Validate inputs strictly at boundary (Pydantic).
- Keep endpoint handlers thin; push logic to services.

## 6) Quality gates before each merge

- New behavior has tests.
- Existing tests remain green.
- No dead code or unused dependencies.
- README or sprint notes updated.

## 7) Architecture review checklist

Before sprint 2 starts, answer:
- Where does recommendation logic live?
- How will you swap persistence layer later?
- Which components are hardest to test and why?
- What failure modes are most likely in production?

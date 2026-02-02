---
description: "Tasks for creating and ratifying the canonical PRD"
---

# Tasks: Project PRD (001-add-prd)

**Input**: `specs/001-add-prd/spec.md`, `specs/001-add-prd/plan.md`, `specs/001-add-prd/research.md`
**Prerequisites**: plan.md (required), spec.md (required), research.md
**Constitution Gate**: All prerequisites MUST have a passing `Constitution Check`.

## Phase 1: Setup & Drafting

- [ ] T001 [P] [US1] Draft `docs/PRD.md` using content from `specs/001-add-prd/spec.md` (path: `docs/PRD.md`). Include ratification metadata (version, ratified_date, ratified_by, change_summary).
- [ ] T002 [P] [US1] Add `Sync Impact Report` comment header to PR with list of affected files and rationale.
- [ ] T003 [P] [US1] Add a `Constitution Compliance` block to the PR description referencing the spec and the required Designated Reviewer.

## Phase 2: Review & Governance

- [ ] T004 [US3] Request review from a Designated Reviewer (pedagogy/content or security when applicable).
- [ ] T005 [US3] Obtain approvals: 1 Maintainer + 1 Designated Reviewer (or documented independent reviewer for MAJOR changes).
- [ ] T006 [US3] After approvals, merge the PR and tag the PRD with the new version in `docs/PRD.md`.

- [ ] T011 [US3][SEC] If a PRD change impacts security/privacy: update `docs/threats_v_0.md` with the assessment and mitigation, include the change summary in the PR, and obtain an explicit security-reviewer approval; PR must not be merged until these steps are complete.

## Phase 3: CI & Automation

- [ ] T007 [P] Add CI checks (if missing) to validate: tests passing, `ruff` linting, `black` formatting, and presence of `Constitution Compliance` in new specs/PRs.
- [ ] T008 [P] Create a small PR template that requires `Constitution Compliance` and `Sync Impact Report` sections.

- [ ] T012 [P] Implement CI job `prd-guards` to verify `docs/PRD.md` contains ratification metadata (`Version`, `Ratified`) and to run basic checks for `Constitution Compliance` in changed specs.
- [ ] T013 [P] Add `PULL_REQUEST_TEMPLATE.md` in `.github/` that includes `Constitution Compliance` and `Sync Impact Report` sections and instructs contributor to name the Designated Reviewer.

## Phase 4: Follow-ups (if PRD triggers functionality)

- [ ] T009 Create new specs/plans for any functional work triggered by the PRD and ensure they pass the Constitution gates.
- [ ] T010 Update `.specify/memory/constitution.md` if governance changes are ratified as part of PRD changes.

## Notes
- All tasks require passing the Constitution Check before implementation.
- The project currently has a single maintainer; see acceptance criteria in `specs/001-add-prd/spec.md` for governance details.

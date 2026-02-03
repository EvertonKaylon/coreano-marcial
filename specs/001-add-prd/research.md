# research.md — Project PRD (001-add-prd)

## Overview
This research document records decisions that resolve the Technical Context for the PRD feature and any open 'NEEDS CLARIFICATION' items from the spec. For each decision we include rationale and alternatives considered.

### Decision: Python 3.11 + Django 4.2
- Decision: Use Python 3.11 and Django 4.2 as the project baseline.
- Rationale: The repository already uses Django 4.2 and standard Python virtualenv workflows; Python 3.11 is widely supported and offers performance/stability improvements over 3.10 while remaining compatible with deps.
- Alternatives considered: Python 3.10 (backward compatibility), Python 3.12 (newer but may be less widely adopted in some CI images). Rejected due to marginal benefit vs potential CI friction.

### Decision: Testing & Tooling
- Decision: Use Django's test runner for unit/integration tests; support `pytest` + `pytest-django` for contributor preference. Adopt `ruff` and `black` for linting/formatting; add `isort` if needed.
- Rationale: Django test runner is sufficient for server-rendered app tests and integrates well with database migrations. `pytest` is optional and widely used; `ruff` is lightweight and enforces quality without heavy overhead.
- Alternatives considered: Full `pytest`-first workflow, or `pre-commit` only. Rejected because the combination of Django tests + optional pytest keeps onboarding simpler.

### Decision: Minimal External Dependencies
- Decision: Favor native Django features and defer adding libraries (HTMX optional for small client interactions only). Any new dependency must be justified by the feature plan and recorded in `plan.md`.
- Rationale: Matches Constitution principle of avoiding unnecessary complexity and keeps footprint small for modest hardware.
- Alternatives considered: Early adoption of larger JS frameworks or single-page patterns. Rejected as out-of-scope for project goals.

### Decision: CI & Quality Gates
- Decision: Add CI checks to enforce: tests passing, `ruff` linting, `black` formatting, presence of `Constitution Compliance` for new specs, and check that `docs/PRD.md` is present once merged.
- Rationale: Ensures the Constitution gates are machine-enforced as much as possible.
- Alternatives considered: Manual PR checklist only. Automated checks provide repeatable enforcement and reduce review burden.

### Decision: Governance (approved)
- Decision: PRD changes require one Maintainer and one Designated Reviewer (domain or security reviewer). Single-maintainer projects allow the maintainer to act in both roles temporarily; MAJOR changes must seek independent reviewers and document the Sync Impact Report.
- Rationale: Balances governance with current project personnel constraints.

## Research Tasks (Phase 0)
- Research 1: Confirm Python version compatibility for all CI images and add test matrix (3.11, optionally 3.12).
- Research 2: Draft initial CI workflow to run tests, ruff, and black; add a check for `Constitution Compliance` presence in new specs.
- Research 3: Define a minimal PR template that includes `Constitution Compliance` and `Sync Impact Report` sections.

## Outcome
All NEEDS CLARIFICATION items in the spec related to governance and technical stack have been resolved in this document and applied to `specs/001-add-prd/spec.md` and templates where appropriate.
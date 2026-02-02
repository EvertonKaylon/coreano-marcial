# Architectural Decisions — decisions_v_1

## DECISION-001: Constitution & PRD Governance

- **Date**: 2026-02-02
- **Context**: The project requires explicit governance for product requirements and feature alignment to avoid scope drift.
- **Decision**: Ratify the project Constitution and enforce that PRD changes require approvals from one Maintainer and one Designated Reviewer. Single-maintainer projects allow the maintainer to act in both roles temporarily; MAJOR changes must obtain an independent reviewer and document it in the Sync Impact Report.
- **Consequences**:
  - All specs must include a `Constitution Compliance` section.
  - CI and PR templates should enforce checks for PRD metadata and `Constitution Compliance` presence.
  - Security-impacting PRD changes must update `docs/threats_v_0.md` and obtain a security reviewer.

## DECISION-002: Minimal Dependencies & Django baseline

- **Date**: 2026-02-02
- **Decision**: Use Django 4.2 and Python 3.11 as the development baseline; prefer built-in Django features and avoid introducing frontend frameworks unless justified in `plan.md`.

## How to add future decisions

- Create `docs/decisions_v_X.md` where `X` increments. Each decision must reference the spec and include rationale, alternatives considered, and consequences.

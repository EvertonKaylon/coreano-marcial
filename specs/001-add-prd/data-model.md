# data-model.md — Project PRD (001-add-prd)

## Entities

### PRD Document
- **Location**: `docs/PRD.md`
- **Fields**:
  - `version` (string, semantic): e.g., 1.0.0
  - `ratified_date` (date): when ratified
  - `ratified_by` (string): approver/maintainer name or nickname
  - `change_summary` (text): short explanation of what changed
  - `content` (markdown): the PRD sections (Purpose, Problem, Audience, Value Props, Principles, Scope, Vision)
- **Behavior**:
  - Treated as the canonical product guidance document; any feature specs must reference a PRD section in their `Constitution Compliance`.
  - No database model is required for PRD; stored as repo artifact under `docs/` and tracked by git.

## Notes
- The PRD is a documentation artifact rather than a runtime entity. No database schema changes are required for this feature.

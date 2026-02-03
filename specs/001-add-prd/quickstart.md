# quickstart.md — Project PRD (001-add-prd)

This quickstart explains how to validate and deliver the PRD feature.

1. Ensure your development environment is set up (see project README).
2. Validate the spec with the requirements checklist: `specs/001-add-prd/checklists/requirements.md` (address any failing items).
3. Create `docs/PRD.md` with the content in the spec and include ratification metadata (version, ratified_date, ratified_by, change_summary).
4. Open a PR from branch `001-add-prd` with:
   - Title: `docs: add PRD vX.Y.Z`
   - A `Sync Impact Report` (see constitution governance rules) in the PR description
   - The `Constitution Compliance` block referencing the PRD sections
   - A named Designated Reviewer in the PR description
5. Ensure CI passes (tests, linting, formatting) and obtain required approvals (1 Maintainer + 1 Designated Reviewer).
6. Merge and tag the PRD version in the `docs/PRD.md` metadata.

Notes:
- This feature is documentation-only. If merging the PRD triggers functional follow-ups (e.g., new endpoints, data model changes), create new specs and plans for those features and run them through the Constitution gates.

# Feature Specification: Project PRD (Coreano Marcial)

**Feature Branch**: `001-add-prd`  
**Created**: 2026-02-02  
**Status**: Draft  
**Input**: User description: "Coreano Marcial is an educational platform focused on progressive Korean learning applied to martial contexts. The PRD captures: purpose, problem statement, target audience, value proposition, core principles, scope definition, and long-term vision."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create canonical PRD (Priority: P1)

As a product owner, I want a canonical `docs/PRD.md` that documents the project's purpose and scope so that every feature and spec can be validated against a single source of product truth.

**Why this priority**: This establishes the product boundary and prevents feature work that doesn't align with the core domain (Domain Supremacy).

**Independent Test**: Verify `docs/PRD.md` exists and contains the required sections. Confirm at least one newly created spec references a PRD section in its `Constitution Compliance` section.

**Acceptance Scenarios**:

1. **Given** the repository, **When** a maintainer opens `docs/PRD.md`, **Then** they see sections: Purpose, Problem Statement, Target Audience, Core Value Proposition, Core Principles, Scope Definition, Long-Term Vision, and Version/Ratification metadata.
2. **Given** a new feature spec is created, **When** the spec is reviewed, **Then** it includes a `Constitution Compliance` entry mapping to the relevant PRD section(s).

---

### User Story 2 - Use PRD for spec mapping (Priority: P2)

As a contributor writing a feature spec, I want a clear mapping to PRD sections so I can demonstrate domain alignment and satisfy the constitution gates.

**Why this priority**: Ensures consistently that all new work preserves domain focus and simplifies review.

**Independent Test**: Create a sample spec and confirm the `Constitution Compliance` section cites the exact PRD section(s) (e.g., "PRD: Scope Definition - Modules of learning by level").

**Acceptance Scenarios**:

1. **Given** a draft spec, **When** the contributor fills `Constitution Compliance`, **Then** the reviewer can find the cited PRD section and confirm alignment.

---

### User Story 3 - Govern and ratify PRD changes (Priority: P3)

As a maintainer/reviewer, I want a clear approval and versioning process for changes to the PRD so that product direction changes are auditable and agreed upon.

**Why this priority**: PRD changes affect downstream work; governance reduces surprise scope drift.

**Independent Test**: Submit a PR that updates `docs/PRD.md` and confirm it follows the governance rules (PR with sync impact report, correct ratification metadata, and required approvals).

**Acceptance Scenarios**:

1. **Given** a PR changing `docs/PRD.md`, **When** the PR is opened, **Then** it includes a Sync Impact Report and metadata (version bump rationale).
2. **Given** the PR, **When** reviewers approve it, **Then** the PR is merged only after required approvals are met.

---

### Edge Cases

- How are conflicts resolved when a new feature appears to contradict PRD guidance? (See Governance - changes must propose decision file and mitigation.)
- What happens if a PRD section requires immediate correction due to security or legal issues? (Emergency patch procedure must be defined.)

## Constitution Compliance (MANDATORY)

- **PRD mapping**: This document implements `docs/PRD.md` with sections: Purpose; Problem Statement; Target Audience; Core Value Proposition; Core Principles; Scope Definition; Long-Term Vision. (Addresses Domain Supremacy.)
- **Acceptance criteria & tasks**: Acceptance scenarios and derived tasks will be added to `specs/001-add-prd/tasks.md` and included in the plan. (Mandatory Spec-Driven Development.)
- **Threat assessment**: This is a documentation change (no code). No immediate new threats anticipated. NOTE: If a PRD change mandates functional changes that touch auth/data, those changes MUST add entries to `docs/threats_v_0.md` and pass security review. (Security by Default.)
- **Architecture boundaries**: Documentation-only change; no code changes expected. (Explicit Architecture Boundaries.)
- **Performance**: None expected. (Performance as Constraint.)
- **Visual tokens**: No UI change is planned. If visuals are changed in future (e.g., new PRD-based UI), update `design_tokens.json`. (Design Token Authority.)
- **Documentation list**: Add/modify `docs/PRD.md`. If governance decisions arise, add `docs/decisions_v_X.md`. Update `docs/SPEC.md` or templates if behavior changes. (Documentation Synchronization Rule.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST contain `docs/PRD.md` with the sections listed in the PRD content (Purpose, Problem Statement, Target Audience, Core Value Proposition, Core Principles, Scope Definition, Long-Term Vision, Version & Ratification metadata).
- **FR-002**: New and updated specs MUST reference the appropriate `docs/PRD.md` section(s) in their `Constitution Compliance` section.
- **FR-003**: PRs that change `docs/PRD.md` MUST include a Sync Impact Report and proposed `CONSTITUTION_VERSION` bump when relevant.
- **FR-004**: PRD changes that affect security, privacy, authentication, or data exposure MUST create or update entries in `docs/threats_v_0.md` and include a security reviewer in approvals.
- **FR-005**: `docs/PRD.md` MUST include ratification metadata: `Version`, `Ratified Date`, `Changed By`, and `Change Summary`.
- **FR-006**: Governance details: PRD changes MUST be approved by **two approvals**: (a) one **Maintainer** (a repository maintainer) AND (b) one **Designated Reviewer** (a reviewer with relevant domain expertise — pedagogy/content — or a security reviewer when the change impacts security/privacy). Acceptance criteria: PRD-change PRs MUST list the Designated Reviewer in the PR description and obtain at least one approval from a Maintainer AND one approval from the Designated Reviewer before merge. If the repository has a single maintainer, that person may temporarily act in both roles; however, for MAJOR (breaking) changes an independent reviewer MUST be obtained and documented in the Sync Impact Report.

### Key Entities *(include if feature involves data)*

- **PRD Document**: Canonical product document kept at `docs/PRD.md` (attributes: version, ratification date, author, change log).
- **Maintainer Group**: Nominal list of maintainers who are authorized to ratify PRD changes.
- **Spec**: A feature-level document that must reference PRD sections.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docs/PRD.md` exists and contains all required sections by merge time (pass/fail verification performed in PR checklist).
- **SC-002**: 100% of new feature specs created after this change include a PRD section mapping in `Constitution Compliance` for the next 3 months.
- **SC-003**: PRD is ratified by the agreed approver set (see FR-006) before being used as a gating document in reviews.
- **SC-004**: Any PRD change that introduces functional changes to the codebase triggers updates to `docs/threats_v_0.md` and includes a security reviewer as part of the PR approvals.

## Assumptions

- PRD is a living document and will evolve; changes follow the governance rules in the Constitution.
- This initial PRD is documentation-only; no code changes are included with this feature unless explicitly specified later.
- Maintainer list and ratification threshold: Currently the repository has a single maintainer (the project owner). For now, the project owner will act as the **Maintainer** and may act as the **Designated Reviewer** temporarily; for MAJOR changes an independent or additional reviewer should be sought and recorded in the Sync Impact Report.

## Deliverables

- `docs/PRD.md` (new file) with the PRD content provided in the feature description.
- `specs/001-add-prd/tasks.md` with derived tasks for review, approval, and PRD creation.
- PR with Sync Impact Report and ratification metadata.

## Next steps

1. Decide approver list and required approvals (see NEEDS CLARIFICATION markers Q1/Q2 below).
2. Create `docs/PRD.md` with content from this spec and open PR against `main`.
3. After approvals, merge and update Constitution metadata (version/rationale) and close tasks.

## Validation

- Checklists `specs/001-add-prd/checklists/requirements.md` and `specs/001-add-prd/checklists/requirements-prd-20260202.md` marked PASS and reviewed on 2026-02-03 by repository owner. See checklists for details and traceability issues (epic issues linked in checklists). This spec is ready for PR creation of `docs/PRD.md`.


```

## Zero-state and Partial-data Scenarios (Draft)

Some PRD-driven features may assume the presence of content or user progress data. Documenting zero-state and partial-data behavior prevents ambiguous UX and hidden errors.

- Zero-state: define how the system behaves for new users with no progress (e.g., show onboarding, default belt selection, placeholder lessons). Acceptance: onboarding flow displays default lesson and allows explicit level selection.
- Partial-data: when media or vocabulary items are partially available, the UI must surface fallback text and gracefully skip unavailable audio assets. Acceptance: missing audio assets do not block lesson progression; clear UI affordance shown.

Owner: `@EvertonKaylon` (spec author). Link to issue: https://github.com/EvertonKaylon/coreano-marcial/issues/2

## Fallback Behavior for External Dependencies (Draft)

When external content APIs or CDN-hosted assets are unavailable, the system must degrade gracefully:

- Serve cached content when available (stale-while-revalidate policy).
- Display non-blocking error banners with retry controls for contributors and users.
- Provide fallbacks for media: use placeholder audio or skip playback with a message.

Acceptance: Functional tests demonstrate content retrieval fallback and a visible retry affordance. Owner: `@EvertonKaylon`. Link to issue: https://github.com/EvertonKaylon/coreano-marcial/issues/3

## Accessibility & Localisation Requirements (Draft)

Accessibility (a11y) and localisation expectations for PRD-mandated content:

- Content should conform to WCAG 2.1 AA where applicable for public-facing pages.
- All user-facing strings must be prepared for translation (use Django i18n and `gettext_lazy`) and provide a default locale.
- Media assets should include captions/transcripts when content is instructional.

Acceptance: Linting or CI checks should include spot checks for gettext markers and presence of transcripts for audio-based lessons. Owner: `@EvertonKaylon`. Link to issue: https://github.com/EvertonKaylon/coreano-marcial/issues/4

```markdown
# Feature Specification: Project PRD (Coreano Marcial)

**Feature Branch**: `001-add-prd`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Coreano Marcial is an educational platform focused on progressive Korean learning applied to martial contexts. The PRD captures: purpose, problem statement, target audience, value proposition, core principles, scope definition, and long-term vision."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create canonical PRD (Priority: P1)

As a product owner, I want a canonical `docs/PRD.md` that documents the project's purpose and scope so that every feature and spec can be validated against a single source of product truth.

**Why this priority**: This establishes the product boundary and prevents feature work that doesn't align with the core domain (Domain Supremacy).

**Independent Test**: Verify `docs/PRD.md` exists and contains the required sections. Confirm at least one newly created spec references a PRD section in its `Constitution Compliance` section.

**Acceptance Scenarios**:

1. **Given** the repository, **When** a maintainer opens `docs/PRD.md`, **Then** they see sections: Purpose, Problem Statement, Target Audience, Core Value Proposition, Core Principles, Scope Definition, Long-Term Vision, and Version/Ratification metadata.
2. **Given** a new feature spec is created, **When** the spec is reviewed, **Then** it includes a `Constitution Compliance` entry mapping to the relevant PRD section(s).

---

### User Story 2 - Use PRD for spec mapping (Priority: P2)

As a contributor writing a feature spec, I want a clear mapping to PRD sections so I can demonstrate domain alignment and satisfy the constitution gates.

**Why this priority**: Ensures consistently that all new work preserves domain focus and simplifies review.

**Independent Test**: Create a sample spec and confirm the `Constitution Compliance` section cites the exact PRD section(s) (e.g., "PRD: Scope Definition - Modules of learning by level").

**Acceptance Scenarios**:

1. **Given** a draft spec, **When** the contributor fills `Constitution Compliance`, **Then** the reviewer can find the cited PRD section and confirm alignment.

---

### User Story 3 - Govern and ratify PRD changes (Priority: P3)

As a maintainer/reviewer, I want a clear approval and versioning process for changes to the PRD so that product direction changes are auditable and agreed upon.

**Why this priority**: PRD changes affect downstream work; governance reduces surprise scope drift.

**Independent Test**: Submit a PR that updates `docs/PRD.md` and confirm it follows the governance rules (PR with sync impact report, correct ratification metadata, and required approvals).

**Acceptance Scenarios**:

1. **Given** a PR changing `docs/PRD.md`, **When** the PR is opened, **Then** it includes a Sync Impact Report and metadata (version bump rationale).
2. **Given** the PR, **When** reviewers approve it, **Then** the PR is merged only after required approvals are met.

---

### Edge Cases

- How are conflicts resolved when a new feature appears to contradict PRD guidance? (See Governance - changes must propose decision file and mitigation.)
- What happens if a PRD section requires immediate correction due to security or legal issues? (Emergency patch procedure must be defined.)

## Constitution Compliance (MANDATORY)

- **PRD mapping**: This document implements `docs/PRD.md` with sections: Purpose; Problem Statement; Target Audience; Core Value Proposition; Core Principles; Scope Definition; Long-Term Vision. (Addresses Domain Supremacy.)
- **Acceptance criteria & tasks**: Acceptance scenarios and derived tasks will be added to `specs/001-add-prd/tasks.md` and included in the plan. (Mandatory Spec-Driven Development.)
- **Threat assessment**: This is a documentation change (no code). No immediate new threats anticipated. NOTE: If a PRD change mandates functional changes that touch auth/data, those changes MUST add entries to `docs/threats_v_0.md` and pass security review. (Security by Default.)
- **Architecture boundaries**: Documentation-only change; no template/view/model changes expected. (Explicit Architecture Boundaries.)
- **Performance**: None expected. (Performance as Constraint.)
- **Visual tokens**: No UI change is planned. If visuals are changed in future (e.g., new PRD-based UI), update `design_tokens.json`. (Design Token Authority.)
- **Documentation list**: Add/modify `docs/PRD.md`. If governance decisions arise, add `docs/decisions_v_X.md`. Update `docs/SPEC.md` or templates if behavior changes. (Documentation Synchronization Rule.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST contain `docs/PRD.md` with the sections listed in the PRD content (Purpose, Problem Statement, Target Audience, Core Value Proposition, Core Principles, Scope Definition, Long-Term Vision, Version & Ratification metadata).
- **FR-002**: New and updated specs MUST reference the appropriate `docs/PRD.md` section(s) in their `Constitution Compliance` section.
- **FR-003**: PRs that change `docs/PRD.md` MUST include a Sync Impact Report and proposed `CONSTITUTION_VERSION` bump when relevant.
- **FR-004**: PRD changes that affect security, privacy, authentication, or data exposure MUST create or update entries in `docs/threats_v_0.md` and include a security reviewer in approvals.
- **FR-005**: `docs/PRD.md` MUST include ratification metadata: `Version`, `Ratified Date`, `Changed By`, and `Change Summary`.
- **FR-006**: Governance details: PRD changes MUST be approved by **two approvals**: (a) one **Maintainer** (a repository maintainer) AND (b) one **Designated Reviewer** (a reviewer with relevant domain expertise — pedagogy/content — or a security reviewer when the change impacts security/privacy). Acceptance criteria: PRD-change PRs MUST list the Designated Reviewer in the PR description and obtain at least one approval from a Maintainer AND one approval from the Designated Reviewer before merge. If the repository has a single maintainer, that person may temporarily act in both roles; however, for MAJOR (breaking) changes an independent reviewer MUST be obtained and documented in the Sync Impact Report.

### Key Entities *(include if feature involves data)*

- **PRD Document**: Canonical product document kept at `docs/PRD.md` (attributes: version, ratification date, author, change log).
- **Maintainer Group**: Nominal list of maintainers who are authorized to ratify PRD changes.
- **Spec**: A feature-level document that must reference PRD sections.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docs/PRD.md` exists and contains all required sections by merge time (pass/fail verification performed in PR checklist).
- **SC-002**: 100% of new feature specs created after this change include a PRD section mapping in `Constitution Compliance` for the next 3 months.
- **SC-003**: PRD is ratified by the agreed approver set (see FR-006) before being used as a gating document in reviews.
- **SC-004**: Any PRD change that introduces functional changes to the codebase triggers updates to `docs/threats_v_0.md` and includes a security reviewer as part of the PR approvals.

## Assumptions

- PRD is a living document and will evolve; changes follow the governance rules in the Constitution.
- This initial PRD is documentation-only; no code changes are included with this feature unless explicitly specified later.
- Maintainer list and ratification threshold: Currently the repository has a single maintainer (the project owner). For now, the project owner will act as the **Maintainer** and may act as the **Designated Reviewer** temporarily; for MAJOR changes an independent or additional reviewer should be sought and recorded in the Sync Impact Report.

## Deliverables

- `docs/PRD.md` (new file) with the PRD content provided in the feature description.
- `specs/001-add-prd/tasks.md` with derived tasks for review, approval, and PRD creation.
- PR with Sync Impact Report and ratification metadata.

## Next steps

1. Decide approver list and required approvals (see NEEDS CLARIFICATION markers Q1/Q2 below).
2. Create `docs/PRD.md` with content from this spec and open PR against `main`.
3. After approvals, merge and update Constitution metadata (version/rationale) and close tasks.


```


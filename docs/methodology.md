# AI-Assisted SDLC Methodology

This document describes the core principles and phased evolution of the
AI-assisted Software Development Lifecycle workflow.

---

## Core Principles

### Human Driven Workflow

AI never starts work autonomously. A human must trigger it.

Examples:

```
/plan-feature PROJ-123
/implement-task PROJ-231
```

### Jira Is the Source of Truth

All planning and execution must remain visible in Jira.

The AI assistant must:
- Read tasks from Jira
- Create tasks and subtasks
- Update task states
- Comment with commit and PR links

### Traceable Implementation

Every commit must reference a Jira issue.

Example commit message:

```
feat: add SBOM CSV export endpoint

Implements PROJ-231
```

### Prefer Deterministic Decisions

The AI assistant should prefer real information over guessing.

Sources of truth:
- Jira
- Figma
- Repository code
- Serena LSP

### Continuous Improvement Through Root-Cause Analysis

When a PR reviewer flags a defect, the workflow does not just fix the immediate
issue — it traces the root cause back through the full workflow chain to prevent
similar mistakes in future tasks. This creates a quality flywheel: each
investigation improves an upstream phase, which produces fewer mistakes, which
generates fewer review sub-tasks.

The `verify-pr` skill spawns a sub-agent to trace each reviewer-flagged defect
through four upstream phases:
- **define-feature** — was the requirement specified in the Feature description?
- **plan-feature** — did the task's Acceptance Criteria, Implementation Notes, and
  file references capture what was needed?
- **implement-task** — did the implementation follow the task correctly, including
  conventions and sibling patterns?
- **project conventions** — does CONVENTIONS.md document the relevant pattern?

The root-cause task targets the phase where the gap originated, not always the
implementation phase. This distinction is critical: a fix applied at the wrong
phase will not prevent recurrence.

Example: a reviewer comments *"this endpoint should return paginated results"*.
The same comment could trace to four different root causes:

```
/plan-feature PROJ-100 → /implement-task PROJ-201 → /verify-pr PROJ-201

Reviewer: "this endpoint should return paginated results"

Root cause 1 (define-feature): The Feature description never mentioned pagination
  → Fix: improve Feature template guidance to prompt for pagination requirements

Root cause 2 (plan-feature): The Feature mentioned pagination, but the task's
  Acceptance Criteria omitted it
  → Fix: improve plan-feature analysis to detect pagination in Feature descriptions

Root cause 3 (implement-task): The task correctly specified pagination, but
  implement-task missed a paginated sibling endpoint in the same module
  → Fix: improve implement-task sibling analysis to detect pagination patterns

Root cause 4 (conventions): The project uses pagination everywhere but
  CONVENTIONS.md doesn't document the pattern
  → Fix: add pagination convention to CONVENTIONS.md
```

The flywheel effect: each root-cause task improves the upstream phase →
`implement-task` produces fewer mistakes → fewer review sub-tasks → a measurable
decline in the `review-feedback` metric over time = system improving.

---

## SDLC Workflow Phases

The platform evolves incrementally. The AI assistant should always
prioritize the current phase capabilities.

### Phase 0 — Minimal Planning Skill

**Goal:** Generate implementation tasks from a Jira feature.

**Inputs:**
- Jira feature
- Figma design
- Local repositories

**Workflow:**
1. Fetch feature from Jira
2. Retrieve Figma mockup
3. Inspect repositories
4. Identify impacted components
5. Generate implementation plan
6. Create Jira tasks

**Limitations:**
- No architecture index
- No shared knowledge
- Repositories scanned each run

**Output:**
- Jira tasks
- Plan comment on the feature

---

### Phase 1 — Local Repository Intelligence

**Goal:** Improve planning accuracy.

Add a local architecture cache using:
- Tree-sitter
- Serena LSP

Index should store:
- Modules
- APIs
- Services
- Dependencies
- Tests

**Limitations:**
Each developer has their own architecture cache.

---

### Phase 2 — Shared Repository Intelligence

**Goal:** Introduce a shared architecture service.

**Components:**
- Indexer pipeline
- Architecture database
- MCP server

**Benefits:**
- Consistent architecture knowledge
- Faster planning
- Cross-repository insights

---

### Phase 3 — Versioned Architecture Snapshots

**Goal:** Architecture knowledge must match Git commits.

**Structure:**
```
repository → commit SHA → architecture snapshot
```

**Benefits:**
- Accurate planning for branches
- Change impact analysis
- Improved reliability

---

### Phase 4 — Advanced Planning

**Goal:** Planning agents perform deeper analysis.

**Analysis includes:**
- Architecture impact
- Dependency analysis
- Test planning
- Risk detection

**Output should include:**
- Repositories affected
- Modules to modify
- Files likely impacted
- Test requirements

---

## Execution Phase

Engineers implement tasks using Claude Code.

Example command:

```
/implement-task PROJ-231
```

**Workflow:**
1. Fetch Jira task
2. Understand requirements
3. Analyze repository with Serena
4. Propose implementation plan
5. Modify code
6. Write tests
7. Run tests
8. Commit changes
9. Open pull request
10. Update Jira

---

## Expected Jira Task Structure

Tasks should contain:
- Title
- Description
- Repository
- Implementation notes
- Acceptance criteria
- Test requirements

---

## Pull Request Workflow

The AI assistant must:
1. Create branch
2. Commit referencing Jira
3. Open PR
4. Comment on Jira with PR link

---

## Implementation Strategy

When extending this system the AI assistant should:
1. Deliver the simplest working version
2. Iterate incrementally
3. Keep engineers in control
4. Maintain Jira visibility

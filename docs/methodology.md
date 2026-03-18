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

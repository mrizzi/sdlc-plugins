# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns.

## Step-by-Step Execution Plan

### Step 0 -- Validate Project Configuration

Project CLAUDE.md contains all required sections: Repository Registry (trustify-backend with serena_backend), Jira Configuration (TC project key, Cloud ID, Feature issue type ID), and Code Intelligence (serena_backend with rust-analyzer). Validation passes.

### Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add severity aggregation service and endpoint
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Follow existing endpoint patterns, use sbom_advisory join table
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None
- **GitHub Issue custom field**: customfield_10747 (would check for value)

### Step 1.5 -- Description Integrity

Would verify description digest via Jira comments. No digest comment expected for eval -- proceed.

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition and Assign

Would transition TC-9201 to In Progress and assign to current user via Jira API.

### Step 4 -- Understand the Code

Would use `mcp__serena_backend__get_symbols_overview` on:
- `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService methods
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration
- `modules/fundamental/src/advisory/endpoints/get.rs` -- reference endpoint pattern
- `modules/fundamental/src/advisory/model/mod.rs` -- understand model module structure
- `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct and severity field

Sibling analysis on:
- `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling endpoint handler
- `modules/fundamental/src/sbom/model/summary.rs` -- sibling model struct
- `tests/api/advisory.rs` -- sibling test file
- `tests/api/sbom.rs` -- sibling test file

Would check for `CONVENTIONS.md` at repository root.

Documentation files identified:
- `docs/api.md` -- API reference (may need updating with new endpoint)
- `docs/architecture.md` -- system architecture (unlikely to need changes)
- `README.md` -- project readme

### Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

### Steps 6-9 -- Implementation, Tests, Verification

See file descriptions below for detailed changes to each file.

## Files to Create

| # | File Path | Description File |
|---|-----------|-----------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `outputs/file-1-description.md` |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | `outputs/file-2-description.md` |
| 3 | `tests/api/advisory_summary.rs` | `outputs/file-3-description.md` |

## Files to Modify

| # | File Path | Description File |
|---|-----------|-----------------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | `outputs/file-4-description.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | `outputs/file-5-description.md` |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | `outputs/file-6-description.md` |
| 7 | `tests/Cargo.toml` | `outputs/file-7-description.md` |

## Files NOT Modified

- `server/src/main.rs` -- task confirms no changes needed (routes auto-mount via module registration)

## Cross-Section Reference Consistency

Verified that all entity references are consistent across task sections:
- `AdvisoryService` -- consistently referenced in `modules/fundamental/src/advisory/service/advisory.rs` across Files to Modify and Implementation Notes
- `AdvisorySummary` -- consistently referenced in `modules/fundamental/src/advisory/model/summary.rs` in Implementation Notes
- `sbom_advisory` join table -- referenced in `entity/src/sbom_advisory.rs` in Implementation Notes, consistent with repo structure
- Endpoint registration -- consistently in `modules/fundamental/src/advisory/endpoints/mod.rs`

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter -> Axum `Path<Id>` extractor -> PASS
  - Processing: `severity_summary` handler calls `AdvisoryService::severity_summary(sbom_id, tx)` -> queries `sbom_advisory` join table -> joins to advisory table -> groups by severity -> counts unique advisory IDs -> PASS
  - Output: Returns `Json(SeveritySummary { critical, high, medium, low, total })` -> serialized as JSON response -> PASS
  - **COMPLETE**

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service
method, endpoint handler, and integration tests.

Implements TC-9201
```

Commit flags: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Base branch**: main
- **Head branch**: TC-9201
- **Title**: `feat(api): add advisory severity aggregation endpoint`
- **Description**: Would include Implements [TC-9201](<jira-web-url>), summary of changes, and acceptance criteria checklist

## Step 11 -- Jira Update

- Set `customfield_10875` (Git Pull Request) to PR URL in ADF format
- Add comment with PR link, summary of changes, no deviations from plan
- Transition TC-9201 to In Review

<!-- SYNTHETIC TEST DATA — mock Jira feature issue for eval testing; names, URLs, and identifiers are fictional -->

# Mock Jira Feature Issue

**Key**: TC-9005
**Summary**: Drop status table and migrate to enum column
**Status**: New
**Labels**: ai-generated-jira
**Linked Issues**: None

---

## Feature Overview

Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The current design stores advisory lifecycle status (New, Analyzing, Fixed, Rejected) as rows in a separate `advisory_status` table joined via foreign key. This adds unnecessary join overhead on every advisory query and complicates the advisory ingestion pipeline. Migrating to an enum column simplifies queries, improves performance, and reduces schema complexity.

## Background and Strategic Fit

The `advisory_status` table was introduced early in development when the set of statuses was expected to grow frequently. In practice, the four statuses have been stable for over a year. The join adds measurable latency to the advisory list endpoint (p95 increased 40ms after adding status filtering). Converting to an enum column aligns with the platform's strategy of reducing unnecessary indirection in the data model.

## Goals

- **Who benefits**: Backend team (simpler queries), frontend team (faster advisory list loads), DevOps (fewer migration edge cases)
- **Current state**: `advisory.status_id` foreign key references `advisory_status(id)` lookup table; all advisory queries join this table
- **Target state**: `advisory.status` enum column directly on the `advisory` table; `advisory_status` table dropped
- **Goal statements**:
  - Eliminate the `advisory_status` join from all advisory queries
  - Reduce advisory list endpoint p95 latency by ~40ms
  - Remove the `advisory_status` table and its migration history

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) | Migration must be reversible | Yes |
| Add `status` enum column to `advisory` table, populated from the existing `status_id` join | Backfill in the same migration | Yes |
| Drop `status_id` foreign key column from `advisory` table | After backfill completes | Yes |
| Drop `advisory_status` lookup table | Only after all references removed | Yes |
| Update all advisory queries to use the new `status` column instead of the join | Includes service layer and endpoints | Yes |
| Update SeaORM entity definitions to reflect the new schema | `entity/advisory.rs` and remove `entity/advisory_status.rs` | Yes |
| Update advisory ingestion pipeline to write enum values directly | Currently writes to lookup table first | Yes |

## Non-Functional Requirements

- Migration must be atomic: if any step fails, the entire migration rolls back — a partial migration (enum column exists but lookup table is already dropped, or vice versa) would leave the database in an inconsistent state
- Zero downtime: migration must be safe to run while the application is serving traffic
- All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist

## Use Cases (User Experience & Workflow)

### UC-1: Advisory list with status filter

**Persona**: Platform user browsing advisories
**Pre-conditions**: Advisories have been ingested with various statuses
**Steps**:
1. User navigates to advisory list page
2. User filters by status = "Fixed"
3. Backend queries `advisory` table with `WHERE status = 'Fixed'` (no join)

**Expected outcome**: Filtered results return faster due to eliminated join

### UC-2: Advisory ingestion

**Persona**: Ingestion pipeline processing new advisory feed
**Pre-conditions**: Advisory feed contains status field
**Steps**:
1. Pipeline parses advisory from feed
2. Pipeline maps status string to `advisory_status_enum` value
3. Pipeline inserts advisory row with enum status directly

**Expected outcome**: Ingestion writes enum value directly without lookup table insert

## Customer Considerations

- No user-facing API changes — the response shape remains identical (status is still a string)
- Migration must be tested against a production-sized dataset before deployment

## Documentation Considerations

- **Doc Impact**: Minor — update internal architecture docs to reflect schema change
- **User purpose**: No external API documentation changes needed
- **Reference material**: SeaORM enum mapping documentation

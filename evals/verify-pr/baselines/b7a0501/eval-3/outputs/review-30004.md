# Review Comment Classification: 30004

## Comment
**Author**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Date**: 2026-04-20T14:40:00Z

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification
**Type**: Question
**Severity**: LOW
**Creates Sub-task**: NO

## Reasoning
This comment is phrased as a question seeking clarification about design intent. The reviewer asks whether the current behavior of the GET endpoint (returning soft-deleted SBOMs without requiring `include_deleted=true`) is intentional. Notably, the Jira task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The current implementation appears to match this intent -- the GET endpoint does not filter by `deleted_at`, meaning soft-deleted SBOMs are still accessible via direct GET. The reviewer is seeking confirmation rather than requesting a change. Questions do not warrant sub-task creation; the PR author should respond to the comment with clarification.

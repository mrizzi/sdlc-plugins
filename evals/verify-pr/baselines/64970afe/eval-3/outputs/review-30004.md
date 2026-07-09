# Review Comment Classification: 30004

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date**: 2026-04-20T14:40:00Z

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer asks two explicit questions seeking clarification about a design decision rather than requesting a code change:

1. "Have you considered..." -- an inquiry about the author's awareness, not a directive to change code
2. "Is that intentional?" -- explicitly asking for clarification on whether the current behavior is by design

Key classification indicators:
- No imperative language is used (no "should", "must", "needs to", "fix", "change", "wrap")
- The comment is exploratory -- the reviewer is noting an observation and asking whether the PR author made a deliberate choice
- The reviewer does not prescribe a fix or suggest a specific change
- The phrasing is interrogative throughout, not declarative or imperative

Looking at the task description, the acceptance criteria focus on the list endpoint filtering (`GET /api/v2/sbom` excludes soft-deleted SBOMs by default, `GET /api/v2/sbom?include_deleted=true` includes them). The task description also states the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", which could be read as the GET-by-ID endpoint continuing to return deleted SBOMs while also supporting the parameter. The reviewer's question is about a design intent that the team should clarify.

## Action

No sub-task created. Questions ask for clarification and do not require code changes.

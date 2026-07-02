# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Review ID:** 20001

## Classification: question

## Reasoning

The reviewer asks two explicit questions: "Have you considered..." and "Is that intentional?" The comment is exploratory -- the reviewer is seeking clarification about a design decision rather than requesting a code change. Key indicators:

1. The comment opens with "Have you considered" -- an inquiry about awareness, not a directive
2. It closes with "Is that intentional?" -- explicitly asking for clarification on whether the current behavior is by design
3. No imperative language is used (no "should", "must", "needs to", "fix", "change")
4. The reviewer is noting an observation about the GET endpoint behavior and asking whether the PR author made a deliberate choice

Looking at the task description, the acceptance criteria state: "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" -- this is about the list endpoint. The task description also states the SBOM "remains accessible via direct GET with a ?include_deleted=true parameter", which implies direct GET should still return deleted SBOMs (the `include_deleted` parameter is for the GET by ID endpoint too). The reviewer's question is about an intentional design decision described in the task.

## Action

No sub-task created. Questions ask for clarification and do not require code changes.

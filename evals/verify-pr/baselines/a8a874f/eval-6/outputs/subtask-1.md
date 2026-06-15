# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

## Type
Eval failure sub-task

## Labels
`ai-generated-jira`, `eval-failure`

## Summary
Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

## Description

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing assertions in eval-3 of the verify-pr eval suite. The eval run on PR #747 revealed that the verify-pr skill fails to (1) evaluate convention upgrade eligibility for suggestion-classified review comments and (2) create sub-tasks for review comments that should be elevated from suggestion to code change request via convention analysis.

The root cause is that when a review comment is classified as a suggestion, the skill does not attempt convention upgrade analysis (CONVENTIONS.md lookup or codebase pattern analysis) before finalizing the classification. This means suggestions that match project conventions are never elevated to code change requests, and consequently no sub-task is created for them.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) documents that convention upgrade eligibility analysis must be performed and its reasoning recorded in the classification output, even when no upgrade occurs
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 4c classification and Step 6b convention upgrade flow explicitly requires convention eligibility evaluation output for every suggestion-classified comment

## Implementation Notes
- The Convention Upgrade check (Check 1 in style-conventions.md) already defines the upgrade logic, but the eval failures indicate that in practice the skill skips convention analysis for some suggestions
- The fix should ensure that for every comment classified as "suggestion", the classification output (e.g., review-N.md) includes explicit documentation of whether convention upgrade was evaluated, what was checked (CONVENTIONS.md sections, codebase patterns), and the conclusion
- When a suggestion matches a convention and is upgraded to code change request, a sub-task must be created per Step 6d
- Reference the existing Check 1a (CONVENTIONS.md check) and Check 1b (Codebase Patterns) flow to ensure no suggestion bypasses this analysis

## Acceptance Criteria
- [ ] Every review comment classified as "suggestion" has documented convention upgrade eligibility analysis in its classification output
- [ ] When convention upgrade eligibility analysis finds a matching convention, the suggestion is upgraded to code change request
- [ ] Upgraded suggestions result in sub-task creation per Step 6d
- [ ] eval-3 assertions pass after the fix is applied

## Test Requirements
- [ ] Re-run eval-3 and verify all 13 assertions pass
- [ ] Verify that suggestion-classified comments include convention upgrade analysis in their output

## Review Context

The following eval assertions failed in eval-3 (from the CI eval result review on PR #747):

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:**
> "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:**
> "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

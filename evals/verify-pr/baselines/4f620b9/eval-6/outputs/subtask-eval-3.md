## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). Two assertions regressed: (1) the convention upgrade eligibility is not being evaluated for the suggestion, and (2) no sub-task is created for the suggestion. The verify-pr skill should evaluate whether suggestions match documented or demonstrated project conventions and upgrade them accordingly, and when a suggestion should result in a sub-task (either through direct classification or convention upgrade), it must create one.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade logic in Check 1 properly evaluates all suggestions for upgrade eligibility
- `evals/verify-pr/evals.json` -- review and update eval-3 assertions if the expected behavior has changed

## Implementation Notes
- The failing assertions indicate that review comment 30002 (classified as suggestion) is not being evaluated for convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning
- The convention upgrade check (Check 1 in style-conventions.md) should examine every suggestion against CONVENTIONS.md and codebase patterns, and document the analysis even when no match is found
- If the suggestion matches a convention, it should be upgraded to a code change request, which would then trigger sub-task creation
- Review the baseline grading at `evals/verify-pr/baselines/latest/eval-3/grading.json` to understand what behavior was expected previously

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all comments classified as suggestions
- [ ] The classification output documents the convention upgrade analysis (CONVENTIONS.md lookup and/or codebase pattern analysis)
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify eval-3 passes with 0 failures after the fix
- [ ] Verify convention upgrade analysis is documented in classification output for suggestions

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
**Source:** CI eval results (eval-3)
**Failing assertions:**

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

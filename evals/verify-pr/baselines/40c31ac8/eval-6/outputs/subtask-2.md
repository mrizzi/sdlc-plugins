## Repository
sdlc-plugins

## Target Branch
main

## Description
Investigate and fix eval-3 failures in the verify-pr eval suite. Eval-3 has 2 failing assertions (85% pass rate) related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The eval expects that suggestion-type review comments are evaluated for convention upgrade eligibility and, when applicable, elevated to code change requests that produce sub-tasks.

## Review Context
**Eval-3 Failing Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
>
> Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Eval-3 Failing Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
>
> Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- Add or update the review comment classification logic to include convention upgrade eligibility analysis for suggestion-type comments
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- If convention upgrade logic belongs in the style/conventions sub-agent, add the relevant check or cross-reference

## Implementation Notes
- The failing assertions indicate that when a review comment is classified as a "suggestion," the verify-pr skill should additionally evaluate whether the suggestion aligns with a documented project convention (e.g., in CONVENTIONS.md) or a demonstrated codebase pattern
- If a convention match is found, the suggestion should be upgraded to a code change request, which then produces a sub-task
- The fix should ensure that review-N.md output files document the convention upgrade eligibility analysis (whether or not an upgrade occurs)
- Review the existing review comment classification flow in SKILL.md to identify where convention upgrade evaluation should be inserted

## Acceptance Criteria
- [ ] Suggestion-type review comments are evaluated for convention upgrade eligibility
- [ ] Convention upgrade eligibility analysis is documented in the review classification output (review-N.md)
- [ ] When a suggestion matches a documented or demonstrated convention, it is upgraded to a code change request
- [ ] Upgraded suggestions produce sub-tasks
- [ ] eval-3 pass rate improves from 85% to 100%

## Test Requirements
- [ ] Re-run eval-3 and verify both failing assertions now pass
- [ ] Verify that suggestions without convention matches are not incorrectly upgraded

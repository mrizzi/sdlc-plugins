## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comment 30002 (index suggestion). Two assertions are failing: (1) the review classification output does not evaluate convention upgrade eligibility for the suggestion, and (2) no sub-task is created for the review comment regardless of classification path.

## Files to Modify
- `evals/verify-pr/evals.json` -- update eval-3 assertions or expected outputs if the assertion expectations need adjustment based on the new Documentation Coverage check
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade logic in Check 1 properly evaluates suggestions for convention upgrade eligibility and documents the evaluation in output files

## Implementation Notes
- eval-3 has 2 failing assertions out of 13 (85% pass rate):
  - Assertion: "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
    Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
  - Assertion: "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
    Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"
- The root cause appears to be that the convention upgrade eligibility evaluation (Check 1 in style-conventions.md) is not producing visible evidence in the classification output, and suggestions that should be upgraded are not being elevated to code change requests
- Follow the existing Check 1 structure (1a through 1d) to ensure convention upgrade evaluation is documented in the output

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented in classification reasoning for suggestion-classified comments
- [ ] When a suggestion matches a documented convention or demonstrated codebase pattern, it is upgraded to a code change request and a sub-task is created
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify eval-3 passes all 13 assertions after the fix
- [ ] Verify convention upgrade evaluation appears in review classification output files

## Review Context
Eval result review from CI (github-actions[bot]):
- eval-3: 2 failing assertions out of 13 (85% pass rate)
- Failing assertions relate to convention upgrade eligibility evaluation and sub-task creation for index suggestion review comment 30002

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

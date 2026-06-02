## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. The eval expects that convention upgrade eligibility is evaluated for review comment 30002 (an index suggestion) and that a sub-task is created for it regardless of classification path -- either classified directly as a code change request or upgraded from suggestion via convention analysis. Currently, the classification output does not evaluate convention upgrade eligibility and no sub-task is created.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade logic in Check 1 handles the index suggestion pattern correctly so that convention upgrade eligibility is documented in classification reasoning
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that Step 4c classification and Step 6b convention upgrade flow correctly processes suggestions that should be elevated to code change requests based on convention analysis

## Implementation Notes
- The two failing assertions indicate that review comment 30002 (an index suggestion) was classified as a suggestion but no convention upgrade was attempted
- The classification reasoning output (review-30002.md) must document the convention upgrade eligibility evaluation -- whether or not the suggestion matches a documented or demonstrated project convention
- If the suggestion matches a convention (CONVENTIONS.md lookup or codebase pattern analysis), it should be upgraded to a code change request and result in a sub-task
- Review the Check 1 convention upgrade flow (1a through 1d) to ensure it processes all suggestion-classified comments, including index-related suggestions
- Ensure the upgrade-comment action is produced when a convention match is found, so the orchestrator creates the sub-task in Step 6d

## Review Context
Eval-3 failed 2 of 13 assertions:

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for suggestion-classified review comments, with the evaluation reasoning documented in the classification output
- [ ] When a suggestion matches a documented or demonstrated project convention, it is upgraded to a code change request and a sub-task is created
- [ ] The eval-3 assertions pass after the fix -- convention upgrade eligibility is documented and sub-tasks are created for convention-backed suggestions

# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility and sub-task creation

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing assertions in eval-3 of the verify-pr skill. The eval results show eval-3 has an 85% pass rate (11/13 passed, 2 failed). Both failures relate to the handling of review comment 30002 (an index suggestion): the convention upgrade eligibility analysis is missing, and no sub-task was created for the comment.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- review Check 1 (Convention Upgrade) to ensure convention upgrade eligibility is always evaluated and documented for suggestion-classified comments
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- review Step 6b (Apply Convention Upgrades) and Step 6d to ensure suggestions that should be upgraded result in sub-task creation

## Implementation Notes
- The first failing assertion requires that convention upgrade eligibility is evaluated for review comment 30002 (an index suggestion). The review classification output or the report's Style/Conventions analysis must explain whether the suggestion matches a documented or demonstrated project convention. Currently, the output classifies the comment as a suggestion but does not document any CONVENTIONS.md lookup or codebase pattern analysis.
- The second failing assertion requires that review comment 30002 results in a sub-task regardless of classification path -- whether classified directly as a code change request based on reviewer language, or upgraded from suggestion via convention analysis. Currently, no sub-task is created because the comment is classified as a suggestion and no convention upgrade is attempted.
- The fix should ensure that the convention upgrade check (Check 1 in style-conventions.md) always runs its full analysis pipeline for suggestion-classified comments and documents the results, even when no upgrade is warranted.

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, with documented reasoning in the classification output
- [ ] Review comment 30002 (index suggestion) results in a sub-task, either through direct classification as a code change request or through convention upgrade
- [ ] The convention upgrade analysis includes CONVENTIONS.md lookup and/or codebase pattern analysis, with results documented in the output

## Test Requirements
- [ ] Verify that eval-3 assertions pass after the fix
- [ ] Verify that suggestion-classified comments always receive convention upgrade eligibility analysis

## Review Context

From eval-3 failing assertions:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

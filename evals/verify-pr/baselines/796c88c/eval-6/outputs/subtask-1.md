## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002. The eval results show 2 failing assertions at 85% pass rate (11/13 passed). The failures indicate that when a review comment is classified as a suggestion (specifically an index suggestion in comment 30002), the verify-pr skill does not evaluate convention upgrade eligibility and does not create a sub-task for the comment. The fix must ensure that convention upgrade eligibility is evaluated for suggestion-classified review comments and that comment 30002 results in a sub-task regardless of the classification path taken.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update convention upgrade check logic to ensure eligibility evaluation is documented in classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure orchestrator pipeline creates sub-tasks for suggestions that should be upgraded via convention analysis

## Implementation Notes
- The convention upgrade check (Check 1 in style-conventions.md) must evaluate every suggestion-classified comment for convention upgrade eligibility
- The classification output (review-*.md files) must document whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- When a suggestion matches a documented or demonstrated project convention, it must be upgraded to a code change request and result in sub-task creation
- Review the existing convention upgrade pipeline (Steps 6b-6d in SKILL.md) to ensure the full path from suggestion classification through convention analysis to sub-task creation is robust

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comments classified as suggestions -- the classification output explains whether the suggestion matches a documented or demonstrated project convention
- [ ] Review comments that match a convention are upgraded from suggestion to code change request and result in sub-task creation
- [ ] Eval-3 assertions pass after the fix is applied

## Test Requirements
- [ ] Verify that eval-3 passes with 13/13 assertions after the fix
- [ ] Verify that convention upgrade eligibility evaluation appears in review classification outputs for suggestion-type comments

## Review Context
The following eval assertions failed in the CI eval run:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

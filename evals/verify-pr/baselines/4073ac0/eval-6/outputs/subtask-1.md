## Sub-task: Fix eval-3 assertion failures

**Type:** Eval failure sub-task
**Parent:** TC-9106
**Labels:** ai-generated-jira, eval-failure
**Summary:** Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing eval-3 assertions related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The verify-pr skill must evaluate convention upgrade eligibility for suggestions before concluding that no sub-task is needed, and must create sub-tasks for comments that match documented or demonstrated project conventions.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- strengthen convention upgrade evaluation logic in Steps 6b-6d to ensure suggestions are checked against CONVENTIONS.md and codebase patterns before being dismissed
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade check produces explicit reasoning about whether a suggestion matches a documented convention

## Implementation Notes
- The current implementation classifies review comments as suggestions but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is performed
- The fix must ensure that for every suggestion, the classification output documents whether the suggestion matches a documented or demonstrated project convention
- If a convention match is found, the suggestion must be upgraded to a code change request and a sub-task must be created
- Follow the existing convention upgrade pattern in Step 6b of SKILL.md

## Review Context

### Failing Assertion 1
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

### Failing Assertion 2
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Convention upgrade eligibility is explicitly evaluated for every suggestion-classified review comment
- [ ] The classification output documents the CONVENTIONS.md lookup and codebase pattern analysis result
- [ ] Suggestions matching a documented or demonstrated convention are upgraded to code change requests
- [ ] Sub-tasks are created for all code change requests, including those upgraded from suggestions

## Test Requirements
- [ ] Verify that a suggestion matching a documented convention is upgraded and results in a sub-task
- [ ] Verify that a suggestion not matching any convention is not upgraded and no sub-task is created
- [ ] Verify that the classification output includes convention upgrade eligibility reasoning

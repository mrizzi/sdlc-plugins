## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comment 30002 (index suggestion). Two assertions fail: (1) the review classification output does not evaluate convention upgrade eligibility for the suggestion, and (2) no sub-task is created for the comment because it was classified as a suggestion without attempting convention upgrade.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) logic is applied to all comments classified as suggestion, including review comment 30002
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that Step 6b convention upgrade processing correctly handles all suggestion-classified comments before sub-task creation in Step 6d

## Implementation Notes
- The failing assertions indicate that convention upgrade eligibility was not evaluated for review comment 30002 (an index suggestion). The classification reasoning (review-30002.md) should document whether the suggestion matches a documented or demonstrated project convention
- Check 1 in style-conventions.md should evaluate ALL comments classified as "suggestion" for potential convention upgrade, performing both a CONVENTIONS.md lookup and a codebase pattern analysis
- If the suggestion matches a convention (either documented in CONVENTIONS.md or demonstrated by codebase patterns), it should be upgraded to "code change request" and result in a sub-task
- The second assertion ("results in a sub-task regardless of classification path") implies the index suggestion should either be classified directly as a code change request or upgraded via convention analysis

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments
- [ ] The classification reasoning output documents whether each suggestion matches a documented or demonstrated project convention
- [ ] Comments upgraded from suggestion to code change request via convention analysis result in sub-task creation
- [ ] eval-3 assertions pass after the fix

## Review Context
**Source:** Eval result review from CI (github-actions[bot])
**Failing assertions from eval-3:**
1. "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
2. "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

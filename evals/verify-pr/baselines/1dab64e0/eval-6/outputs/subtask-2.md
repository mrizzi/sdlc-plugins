## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in the verify-pr skill. Two assertions are failing at 85% pass rate (11/13 passed, 2 failed). Both failures relate to convention upgrade eligibility not being evaluated for review comment 30002 (an index suggestion), and the consequent failure to create a sub-task for that comment. The verify-pr implementation must evaluate convention upgrade eligibility for suggestions and, when a suggestion matches a documented or demonstrated project convention, upgrade it to a code change request and create a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` --- ensure Check 1 (Convention Upgrade) evaluation explicitly covers all suggestion-classified comments, including index-related suggestions; verify the convention upgrade eligibility analysis is documented in the classification reasoning output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` --- verify Step 6b convention upgrade application correctly processes upgrade-comment actions from the Style/Conventions sub-agent and creates sub-tasks for upgraded suggestions

## Implementation Notes
- The eval-3 failures indicate that when a review comment suggests adding an index (comment 30002), the verify-pr skill classifies it as a "suggestion" but does not evaluate whether it matches a documented or demonstrated convention
- Check 1 in style-conventions.md (Convention Upgrade) must evaluate every suggestion-classified comment for convention upgrade eligibility --- this means checking CONVENTIONS.md for matching patterns and searching the codebase for demonstrated usage
- The classification output (review-N.md files) must document the convention upgrade eligibility analysis, including whether CONVENTIONS.md was searched and whether codebase patterns were checked
- If a suggestion matches a convention (either documented in CONVENTIONS.md or demonstrated by consistent codebase usage), it must be upgraded to a code change request via an upgrade-comment action
- Step 6b in SKILL.md processes upgrade-comment actions and changes classifications from suggestion to code change request before sub-task creation in Step 6d
- Review the convention upgrade flow end-to-end: Check 1 evaluation -> upgrade-comment action -> Step 6b processing -> Step 6d sub-task creation

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, including index-related suggestions
- [ ] The review classification output documents the convention upgrade eligibility analysis (CONVENTIONS.md lookup and/or codebase pattern analysis)
- [ ] Suggestions that match a documented or demonstrated convention are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation in Step 6d

## Test Requirements
- [ ] Verify that an index suggestion review comment triggers convention upgrade eligibility evaluation
- [ ] Verify that the classification reasoning output includes evidence of CONVENTIONS.md lookup or codebase pattern analysis
- [ ] Verify that a suggestion matching a convention is upgraded and produces a sub-task

## Review Context
**Source:** Eval result review from github-actions[bot] (CI eval run)
**Eval ID:** eval-3
**Pass Rate:** 85% (11/13 passed, 2/13 failed)

**Failing Assertion 1:**
> **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) --- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
> **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility --- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
> **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path --- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
> **Evidence:** "No sub-task was created for review comment 30002 --- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747

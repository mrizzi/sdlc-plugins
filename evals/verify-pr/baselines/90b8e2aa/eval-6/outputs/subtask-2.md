# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility and sub-task creation

## Type: eval-failure

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix the two failing assertions in eval-3 related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). The eval expects that convention upgrade eligibility is evaluated for suggestion-classified comments and that review comment 30002 results in a sub-task regardless of whether it was classified directly as a code change request or upgraded from a suggestion via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade logic in Check 1 evaluates all suggestion-classified comments for convention upgrade eligibility and documents the reasoning in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing and Step 6d sub-task creation handle the case where a suggestion should be upgraded based on convention analysis

## Implementation Notes
- The first failing assertion indicates that convention upgrade eligibility is not being evaluated for review comment 30002 (classified as suggestion). The output file review-30002.md must include convention upgrade eligibility analysis -- specifically, a CONVENTIONS.md lookup or codebase pattern analysis must be documented in the classification reasoning.
- The second failing assertion indicates that review comment 30002 should result in a sub-task whether classified directly as a code change request (based on reviewer language) or upgraded from suggestion via convention analysis. The current behavior classifies it as a suggestion without attempting a convention upgrade, so no sub-task is created.
- The fix should ensure that the Style/Conventions sub-agent's Check 1 (Convention Upgrade) explicitly evaluates every suggestion-classified comment for convention match and records the analysis in the output, and that when a convention match is found, the upgrade-comment action is produced so the orchestrator can create a sub-task.

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, including index suggestions like comment 30002
- [ ] The review classification output documents whether a CONVENTIONS.md lookup or codebase pattern analysis was performed for each suggestion
- [ ] Review comments that match a documented or demonstrated project convention are upgraded from suggestion to code change request
- [ ] Upgraded suggestions result in sub-task creation via the orchestrator's Step 6d pipeline

## Review Context
**Eval ID:** eval-3
**Pass Rate:** 85% (11/13 passed, 2 failed)

**Failing Assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

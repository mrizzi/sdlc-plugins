## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). Two assertions are failing because the verify-pr skill is not evaluating convention upgrade eligibility for suggestion-classified review comments and not creating sub-tasks when convention upgrade should apply.

The root cause is that when a review comment is classified as a suggestion, the convention upgrade analysis (Check 1 in style-conventions.md) is either not being triggered or not producing actionable results for the specific comment. The fix should ensure that convention upgrade eligibility is properly evaluated and documented for all suggestion-classified comments, and that comments matching project conventions are upgraded to code change requests with corresponding sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) properly evaluates and documents convention upgrade eligibility for all suggestion-classified comments, including the reasoning in classification output files
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing and Step 6d sub-task creation handle upgraded suggestions correctly

## Implementation Notes
- Check 1 in style-conventions.md already defines the convention upgrade process (steps 1a-1d), but the eval evidence suggests the implementation is not documenting the eligibility evaluation in the review classification output
- The review-30002.md classification output should include convention upgrade eligibility analysis: whether the suggestion matches a CONVENTIONS.md entry or demonstrated codebase pattern
- When a suggestion is upgraded to a code change request via convention check, a sub-task must be created (Step 6d) -- this path appears to be failing
- Review the existing Check 1 logic to ensure the upgrade decision and evidence are captured in classification outputs even when the suggestion is not upgraded

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for all suggestion-classified review comments
- [ ] Review classification output files include convention upgrade analysis reasoning (CONVENTIONS.md lookup or codebase pattern analysis)
- [ ] Suggestions matching project conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation via Step 6d

## Test Requirements
- [ ] Verify convention upgrade eligibility evaluation is documented in review classification outputs
- [ ] Verify sub-task creation for suggestion-to-code-change-request upgrades
- [ ] Update eval assertions in `evals/verify-pr/evals.json` to cover the convention upgrade eligibility documentation behavior

## Review Context
**Source:** Eval result review from CI (github-actions[bot])
**Eval ID:** eval-3
**Failing assertions:**

1. **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

2. **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

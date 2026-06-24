## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility and sub-task creation for review comments. Two assertions are failing at an 85% pass rate (11/13). The failures indicate that the verify-pr skill is not evaluating convention upgrade eligibility for suggestion-classified review comments, and consequently not creating sub-tasks when convention analysis would upgrade a suggestion to a code change request.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade logic (Check 1) properly evaluates all suggestion-classified comments for convention matches, including CONVENTIONS.md lookup and codebase pattern analysis
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b convention upgrade application correctly processes upgrade-comment actions from the Style/Conventions sub-agent and triggers sub-task creation in Step 6d

## Implementation Notes
- The two failing assertions point to a gap in the convention upgrade pipeline for review comments classified as suggestions
- Assertion 1 failure: "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion)" -- the Style/Conventions sub-agent Check 1 (Convention Upgrade) must evaluate each suggestion-classified comment against CONVENTIONS.md and codebase patterns, and the evaluation reasoning must be documented in the output
- Assertion 2 failure: "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path" -- when convention upgrade analysis determines a match, the upgrade-comment action must flow through Step 6b, then Step 6d must create the sub-task
- Review the convention upgrade decision logic in style-conventions.md Check 1d to ensure suggestions are not silently passed over without convention analysis
- Ensure the upgrade-comment action format matches what the orchestrator expects in Step 6b

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, with reasoning documented in the output
- [ ] When a suggestion matches a documented or demonstrated project convention, it is upgraded to a code change request via an upgrade-comment action
- [ ] Upgraded suggestions result in sub-task creation through the Step 6b -> Step 6d pipeline
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify that suggestion-classified comments trigger convention upgrade analysis (CONVENTIONS.md lookup and codebase pattern search)
- [ ] Verify that convention-matched suggestions produce upgrade-comment actions in the Style/Conventions sub-agent output
- [ ] Verify that the orchestrator processes upgrade-comment actions and creates sub-tasks

## Review Context
**Source:** Eval result review from CI (github-actions[bot], review 40001)
**Eval ID:** eval-3
**Failing assertions:**
1. "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
   Evidence: "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"
2. "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
   Evidence: "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

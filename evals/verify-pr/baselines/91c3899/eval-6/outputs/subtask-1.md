# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility and sub-task creation

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix the two failing assertions in eval-3 of the verify-pr eval suite. The eval-3 scenario tests review comment classification and convention upgrade processing. Two assertions fail because the convention upgrade eligibility pipeline does not run for review comment 30002 (index suggestion), and consequently no sub-task is created for it. The fix must ensure that suggestion-classified review comments are evaluated for convention upgrade eligibility with explicit CONVENTIONS.md lookup and codebase pattern analysis documented in the classification reasoning.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure convention upgrade eligibility analysis is explicitly performed and documented for all suggestion-classified review comments, including CONVENTIONS.md lookup and codebase pattern analysis in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that the orchestrator correctly processes upgrade-comment actions from the Style/Conventions sub-agent and creates sub-tasks for upgraded suggestions

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every suggestion-classified comment for convention upgrade eligibility
- The evaluation must include: (1) checking CONVENTIONS.md for matching documented conventions, (2) searching codebase patterns for demonstrated usage
- The review classification output (review-N.md) must document the convention upgrade eligibility analysis, including what was checked and why the suggestion was or was not upgraded
- If a suggestion matches a documented or demonstrated convention, it should be upgraded to a code change request via an upgrade-comment action, which then triggers sub-task creation by the orchestrator
- Reference the existing Check 1 structure in style-conventions.md (Steps 1a-1d) for the convention upgrade pipeline

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestion-classified review comments, with CONVENTIONS.md lookup and codebase pattern analysis documented in the classification reasoning output
- [ ] When a suggestion matches a documented convention or demonstrated codebase pattern, it is upgraded to a code change request and a sub-task is created
- [ ] The review classification output file explains the convention upgrade decision (whether upgraded or not) with specific evidence

## Test Requirements
- [ ] eval-3 passes all assertions after the fix, including the convention upgrade eligibility and sub-task creation assertions

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context

The following eval-3 assertions are failing:

**Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

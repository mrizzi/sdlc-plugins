# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

**Labels:** `["ai-generated-jira", "eval-failure"]`
**Parent:** TC-9106

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures in the verify-pr eval suite. Two assertions are failing:

1. Convention upgrade eligibility is not being evaluated for review comments classified as suggestions -- the classification reasoning does not document whether a CONVENTIONS.md lookup or codebase pattern analysis was performed.
2. Review comments that should result in sub-tasks (whether classified directly as code change requests or upgraded from suggestions via convention analysis) are not producing sub-tasks.

The root cause is that the verify-pr skill's classification and convention upgrade pipeline is not consistently evaluating suggestion-classified comments for convention upgrade eligibility, and is not creating sub-tasks for comments that should be elevated to code change requests.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) explicitly documents the eligibility evaluation for each suggestion, including negative results (no matching convention found)
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Steps 6b-6d correctly handle the upgrade-to-subtask pipeline for suggestions that match conventions

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every comment classified as "suggestion" for convention upgrade eligibility, documenting the analysis in the output (even when no convention match is found)
- The orchestrator's Step 6b must process upgrade-comment actions before Step 6d creates sub-tasks, ensuring upgraded suggestions flow into the code change request pipeline
- Review the eval-3 fixture data to understand the specific scenario: review comment 30002 is an index suggestion that should either be directly classified as a code change request (based on reviewer language) or upgraded from suggestion via convention analysis
- The fix should ensure that convention upgrade eligibility is always documented in the classification reasoning output, and that the upgrade-to-subtask pipeline is complete

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated and documented for every review comment classified as "suggestion"
- [ ] Review comments that match a documented or demonstrated project convention are upgraded from suggestion to code change request
- [ ] Upgraded code change requests result in sub-task creation
- [ ] eval-3 assertions pass after the fix

## Test Requirements
- [ ] Verify eval-3 passes with 13/13 assertions after the fix
- [ ] Verify that suggestion-classified comments include convention upgrade eligibility analysis in their classification reasoning

## Review Context

The following eval assertions are failing:

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

# Sub-task: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix two failing eval-3 assertions related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The eval results show that when a review comment is classified as a suggestion (e.g., comment 30002 about index creation), the verify-pr skill does not evaluate convention upgrade eligibility and does not create a sub-task when the suggestion should have been upgraded via convention analysis.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) properly evaluates suggestion comments for convention upgrade eligibility, documenting the CONVENTIONS.md lookup or codebase pattern analysis in the classification reasoning output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- ensure Step 6b convention upgrade processing and Step 6d sub-task creation correctly handle upgraded suggestions so that sub-tasks are created for suggestions elevated to code change requests

## Implementation Notes
- The root issue is that suggestions are not being evaluated for convention upgrade eligibility -- the convention upgrade pipeline (Check 1 in style-conventions.md) must run for every comment classified as "suggestion" and must document its analysis in the output
- The review classification output (e.g., review-30002.md) must show evidence of convention upgrade evaluation: whether CONVENTIONS.md was consulted, whether codebase patterns were searched, and the outcome of that analysis
- When a suggestion matches a documented or demonstrated project convention, it must be upgraded to a code change request, which then triggers sub-task creation in Step 6d
- The two failing assertions are:
  1. Convention upgrade eligibility must be evaluated and documented in the classification output
  2. The suggestion must result in a sub-task (either directly as code change request or via convention upgrade)

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comments classified as suggestions
- [ ] The classification reasoning output documents whether CONVENTIONS.md lookup or codebase pattern analysis was performed
- [ ] Suggestions matching documented or demonstrated project conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation via the standard code change request pipeline
- [ ] eval-3 assertions pass after the fix

## Review Context
From CI eval results (github-actions[bot], review 40001):

**Failing Assertion 1:**
- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
- **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
- **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
- **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

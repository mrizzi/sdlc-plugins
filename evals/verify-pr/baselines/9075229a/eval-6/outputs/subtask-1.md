## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix 2 failing assertions in eval-3 for the verify-pr skill. The eval-3 scenario tests convention upgrade eligibility evaluation for review comments. Currently, when verify-pr processes review comment 30002 (an index suggestion), the classification output marks it as a suggestion but does not evaluate whether the suggestion matches a documented or demonstrated project convention. As a result, no convention upgrade is attempted and no sub-task is created, even though the eval expects either a direct code change request classification or a convention-based upgrade to produce a sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure the Convention Upgrade check (Check 1) evaluates convention upgrade eligibility for all suggestions, including review comment 30002 in the eval-3 scenario, and documents the eligibility reasoning in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify that the classification-to-sub-task pipeline correctly handles suggestions that are upgraded to code change requests via convention analysis
- `evals/verify-pr/evals.json` -- update eval assertions if behavior changes require adjusted expectations

## Implementation Notes
- The convention upgrade check (Check 1 in style-conventions.md) must evaluate every suggestion for convention eligibility, not skip suggestions that do not appear to match at first glance
- The classification output (review-N.md files) must document whether convention upgrade eligibility was evaluated and what the result was, even when the suggestion is not upgraded
- When a suggestion matches a documented convention (CONVENTIONS.md) or a demonstrated codebase pattern (found via codebase analysis), it should be upgraded to a code change request and result in a sub-task
- Review the eval-3 scenario fixture files to understand the specific review comment 30002 content and the expected convention matching behavior
- Follow the existing convention upgrade flow: Check 1a (CONVENTIONS.md lookup) then Check 1b (codebase pattern analysis)

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comment 30002 in eval-3 -- the classification output explains whether the suggestion matches a documented or demonstrated project convention
- [ ] Review comment 30002 results in a sub-task -- either classified directly as a code change request based on reviewer language, or upgraded from suggestion to code change request via convention analysis
- [ ] eval-3 pass rate improves from 85% (11/13) to 100% (13/13)

## Test Requirements
- [ ] Verify eval-3 assertions pass after the fix by running the verify-pr evals
- [ ] Verify convention upgrade eligibility reasoning is documented in the review classification output file (review-30002.md)
- [ ] Verify that a sub-task is created for review comment 30002 in the eval-3 scenario

## Review Context
The following eval assertions from the CI eval run are failing (from eval-3, 2 of 13 assertions failed, 85% pass rate):

**Assertion 1:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

Both assertions are classified as **regression** (no baseline data available for comparison; conservative default per Step 5c.1).

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

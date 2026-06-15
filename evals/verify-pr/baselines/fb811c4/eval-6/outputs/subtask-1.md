# Sub-Task: Fix eval-3 assertion failures: convention upgrade eligibility, sub-task creation

## Repository
sdlc-plugins

## Target Branch
tc-9106-doc-coverage

## Description
Fix the 2 failing eval-3 assertions related to convention upgrade eligibility handling for review comment 30002 (index suggestion). The eval failures indicate that the verify-pr skill does not evaluate convention upgrade eligibility for suggestions and does not create sub-tasks when convention-backed upgrades apply.

The failing assertions require:
1. Convention upgrade eligibility must be evaluated for suggestions -- the classification output must document CONVENTIONS.md lookup and/or codebase pattern analysis results
2. When a suggestion matches a documented or demonstrated convention, it must be upgraded to code change request and a sub-task must be created

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) documents its analysis in the classification output
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- verify Step 6b convention upgrade flow produces visible reasoning in review classification outputs

## Implementation Notes
- The convention upgrade flow is defined in style-conventions.md Check 1 (steps 1a-1d) and SKILL.md Step 6b
- The eval failure evidence indicates the review-30002.md output file classifies the comment as suggestion but does not document any convention upgrade eligibility analysis
- The fix should ensure that every suggestion classification includes documented evidence of convention lookup (either CONVENTIONS.md match or codebase pattern count)
- Follow the existing Check 1 structure for recording upgrade decisions with evidence

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for all suggestions, with documented reasoning in classification output
- [ ] When a suggestion matches a convention (CONVENTIONS.md or codebase pattern), a sub-task is created
- [ ] eval-3 assertions pass after the fix

## Review Context

**Source:** Eval result review from github-actions[bot] on PR #747

**Failing Assertion 1:**
> "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Failing Assertion 2:**
> "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

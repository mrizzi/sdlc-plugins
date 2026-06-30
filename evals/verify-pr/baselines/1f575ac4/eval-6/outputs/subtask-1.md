## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 assertion failures related to convention upgrade eligibility evaluation and sub-task creation for review comment 30002 (index suggestion). Two assertions fail at ~85% pass rate:

1. Convention upgrade eligibility is not evaluated for review comment 30002 -- the review classification output does not document any CONVENTIONS.md lookup or codebase pattern analysis.
2. Review comment 30002 does not result in a sub-task -- the suggestion was not elevated to a code change request because no convention upgrade was attempted.

The root cause is that the verify-pr skill's handling of suggestion-classified comments does not consistently evaluate convention upgrade eligibility or document the upgrade analysis in the classification output. The fix should ensure that every suggestion-classified comment has its convention upgrade eligibility explicitly evaluated and documented, and that when conventions or codebase patterns support an upgrade, the comment is elevated to a code change request with a corresponding sub-task.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- ensure Check 1 (Convention Upgrade) instructions clearly require documenting the upgrade analysis for every suggestion, including when no convention match is found
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- review Step 4c and Step 6b to ensure convention upgrade flow is clearly specified for all suggestion-classified comments

## Implementation Notes
- The Style/Conventions sub-agent's Check 1 (Convention Upgrade) must evaluate every suggestion-classified comment for upgrade eligibility, checking both CONVENTIONS.md and codebase patterns
- The classification output (review-N.md) must document the convention upgrade analysis, including when no match is found, so eval assertions can verify the analysis was performed
- Review the eval-3 fixture data to understand the expected behavior for comment 30002 (index suggestion) and ensure the skill instructions produce the expected output
- Follow the existing pattern in Check 1 steps 1a-1d for convention upgrade evaluation

## Acceptance Criteria
- [ ] Every suggestion-classified comment has convention upgrade eligibility evaluated and documented in the classification output
- [ ] The convention upgrade analysis is visible in the review-N.md output files, including negative results (no convention match found)
- [ ] eval-3 assertions about convention upgrade eligibility and sub-task creation pass

## Review Context
Original eval assertion failures from CI eval run on PR #747:

> **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
> **Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

> **Assertion:** "Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"
> **Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

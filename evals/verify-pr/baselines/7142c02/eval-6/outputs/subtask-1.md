## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix eval-3 failures related to convention upgrade eligibility evaluation and sub-task creation for review comments classified as suggestions. The verify-pr skill must evaluate convention upgrade eligibility for review comments classified as suggestions (e.g., comment 30002 index suggestion) by performing a CONVENTIONS.md lookup or codebase pattern analysis. When a suggestion matches a documented or demonstrated project convention, it must be upgraded to a code change request and a sub-task must be created.

Currently, suggestions are classified but no convention upgrade analysis is attempted, resulting in suggestions that should be elevated to code change requests being silently dropped without sub-task creation.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- update the review comment classification logic to include convention upgrade eligibility evaluation for suggestions; ensure that suggestions matching documented conventions result in sub-task creation

## Implementation Notes
- When a review comment is classified as a "suggestion," the skill must check whether the suggested pattern matches a documented convention in CONVENTIONS.md or a demonstrated codebase pattern
- If the suggestion matches a convention, it should be upgraded to a code change request and a sub-task should be created
- The classification reasoning output (review-N.md) must document the convention upgrade eligibility analysis, including whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- Follow the existing review classification flow and extend it with the convention upgrade step

## Acceptance Criteria
- [ ] Convention upgrade eligibility is evaluated for review comments classified as suggestions
- [ ] The review classification output documents whether a CONVENTIONS.md lookup or codebase pattern analysis was performed
- [ ] Suggestions matching documented or demonstrated project conventions are upgraded to code change requests
- [ ] Upgraded suggestions result in sub-task creation

## Test Requirements
- [ ] Verify that a suggestion matching a documented convention is upgraded and produces a sub-task
- [ ] Verify that a suggestion not matching any convention remains a suggestion without sub-task creation
- [ ] Verify that the classification reasoning output includes convention upgrade analysis documentation

## Review Context
The following eval assertions failed in eval-3 of the verify-pr eval suite:

**Assertion 1:**
"Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) -- the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"

**Evidence:** "The output file review-30002.md classifies the comment as a suggestion but does not evaluate convention upgrade eligibility -- no CONVENTIONS.md lookup or codebase pattern analysis is documented in the classification reasoning"

**Assertion 2:**
"Review comment 30002 (index suggestion) results in a sub-task regardless of classification path -- whether classified directly as code change request based on reviewer language, or upgraded from suggestion via convention analysis"

**Evidence:** "No sub-task was created for review comment 30002 -- it was classified as suggestion and no convention upgrade was attempted, so the suggestion was not elevated to a code change request"

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

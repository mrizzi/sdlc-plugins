<!-- SYNTHETIC TEST DATA — user input containing an incorrect external API capability claim for eval testing -->

# User Input: Feature with External API Claim

Only Required sections are provided. The Requirements section contains an
incorrect claim about the GitHub REST API: it states that PR reviews cannot
be updated after submission. This is factually wrong — the GitHub REST API
supports `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
to update a review. The define-feature skill's External API Claim
Verification step should detect and flag this claim.

**Feature Summary**: Add automated PR review posting for eval results

---

## Section 1 — Feature Overview (Required)

Add a CI workflow step that posts eval results as a PR review comment on
pull requests that modify skill definitions. When a PR changes a SKILL.md
file, the CI pipeline should run the corresponding eval suite and post a
summary of pass/fail assertions as a PR review. This gives reviewers
immediate visibility into whether skill behavior changes break existing
eval expectations.

## Section 2 — Background and Strategic Fit (Recommended)

SKIP

## Section 3 — Goals (Recommended)

SKIP

## Section 4 — Requirements (Required)

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

## Section 5 — Non-Functional Requirements (Recommended)

SKIP

## Section 6 — Use Cases (Recommended)

SKIP

## Section 7 — Customer Considerations (Optional)

SKIP

## Section 8 — Customer Information/Supportability (Optional)

SKIP

## Section 9 — Documentation Considerations (Optional)

SKIP

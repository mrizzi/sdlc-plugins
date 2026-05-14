# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Context:** The requirement states: "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review".

## Verification Finding

**Result: INCORRECT**

The GitHub REST API does support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It is documented in the GitHub REST API reference for pull request reviews.

**Evidence:**
- **Method:** PUT
- **Endpoint:** `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Capability:** Updates the contents of a specified review on a pull request
- **Documentation:** GitHub REST API — Pull Request Reviews

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement:** "Update existing PR reviews when re-running evals on the same PR, or create a new review if none exists"

**Original note:** "The GitHub API does not support modifying a submitted review"

**Corrected note:** "Use the GitHub REST API PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} endpoint to update an existing review, or POST to create a new one"

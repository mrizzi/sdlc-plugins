# External API Claim Verification

## Detected Claim

The following claim was detected in **Section 4 -- Requirements (Required)**:

**Requirement row 4:**
> "PR reviews cannot be updated after initial submission so always create a new review"

**Notes column:**
> "The GitHub API does not support modifying a submitted review"

This matches the verification trigger pattern: "X cannot be updated after creation" / "The API does not support Y".

## Verification Finding

**Result: INCORRECT**

The claim is factually wrong. The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a JSON body with a `body` field to update the review's top-level comment text. It is documented in the official GitHub REST API reference under "Pull request reviews".

**Evidence:** The GitHub REST API provides full CRUD operations for pull request reviews, including:

- `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews` -- Create a review
- `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` -- Get a review
- `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` -- Update a review
- `DELETE /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` -- Delete a pending review

The PUT endpoint allows modifying the body of a submitted review, contradicting the claim that reviews are immutable after submission.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing PR review when re-running evals on the same PR, or create a new review if none exists"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"

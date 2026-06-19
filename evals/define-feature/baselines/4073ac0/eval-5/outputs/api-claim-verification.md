# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update or modify a pull request review once it has been submitted.

## Verification Finding

**Result: INCORRECT**

The claim is factually wrong. The GitHub REST API **does** support updating a submitted pull request review via the following endpoint:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It is documented in the official GitHub REST API reference under Pull Request Reviews.

Therefore, the requirement's rationale — that a new review must always be created because updates are impossible — is based on an incorrect premise.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Suggested corrected requirement:**
> Update an existing eval review if one was previously posted; create a new review only on the first run

**Suggested corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a previously submitted review rather than creating duplicates

---
hidden: true
---

# How to Unlink Issues from Pull Requests



## How the Repo Maintainer can Unlink Issues from Pull Requests

In GitHub, issues and pull requests may automatically link when specific keywords (e.g., "close", "fixes") are used in pull request descriptions or comments. This guide explains how to unlink an issue from a pull request.

### Steps to Unlink an Issue from a Pull Request

1. **Navigate to the Pull Request** - Click on the **Pull Requests** tab and locate the pull request linked to the issue.

<figure><img src="../../.gitbook/assets/repo-tabs-pull-requests-global-nav-update.webp" alt=""><figcaption></figcaption></figure>

2. **Remove the Linking Keyword** - Open the pull request description or comments where the link to the issue is mentioned. - Look for keywords like `close #issue_number`, `fixes #issue_number`, or `resolves #issue_number`. - Remove these keywords or replace them with plain text (e.g., `related to #issue_number`).



1. **Update the Pull Request Description** - After editing the description or comments, click the **Save** or **Update** button to confirm your changes.



1. **Verify the Unlinking** - Navigate to the issue that was previously linked. - Confirm that the issue is no longer listed under the **Linked pull requests** section.

***

{% hint style="info" %}
_Unlinking the issue does not delete any comments or history.- Removing the linking keyword ensures that the issue and pull request are no longer automatically linked.- If the pull request has already been merged, the link cannot be removed._
{% endhint %}

### _For more information on managing issues and pull requests, visit the_ [_GitHub Documentation_](https://docs.github.com/en/issues)_._

### If you have additional questions, feel free to reach out to the repository maintainers.









##

## How to Unlink an Issue from a Pull Request (GitHub & Lightning Bounties)

When working with GitHub and Lightning Bounties, issues and pull requests (PRs) may be linked in two ways: automatically (using keywords in PR descriptions) or manually (using the sidebar). This guide explains how maintainers can unlink an issue from a PR and what to consider when using Lightning Bounties.

***

## Unlinking Methods

### **1. Unlinking Keyword-Based (Automatic) Links**

If the PR description or commit message uses keywords like `close #123`, `fixes #123`, or `resolves #123`, GitHub will automatically link the PR to the issue and may close the issue upon merging.

#### **To unlink:**

* Navigate to the relevant pull request.
* Click **Edit** on the PR description (or locate the relevant comment).
* Remove or modify the linking keywords (e.g., change `close #123` to plain text like see `issue #123`).
* Save your changes.
* Verify by checking the issue; it should no longer appear under **Linked pull requests** in the sidebar.

> **Note:** If the PR has already been merged and the issue was closed, you cannot remove the historical link, but you can re-open the issue if needed.

***

### **2. Unlinking Manually Linked Issues (Sidebar Method)**

If a PR or issue was manually linked using the sidebar:

**To unlink:**

* Go to the pull request or issue.
* In the right sidebar, find the **Development** section.
* Hover over the linked issue or PR, and click the **Unlink** (or "x") button that appears.
* Confirm the unlink action.
* The issue and PR will no longer be associated.

***

### Lightning Bounties Considerations

* **Bounty Tracking:** Lightning Bounties tracks issue and PR status via GitHub integration. Unlinking an issue from a PR may affect bounty eligibility or payout triggers if the bounty is configured to require a linked/closed issue.
* **Workflow:** Always coordinate with your team and check Lightning Bounties documentation if you're unsure how unlinking affects bounty status.
* **Permissions:** Lightning Bounties only has read-only access to your repository and cannot modify links on your behalf.

***

### Best Practices

* Double-check PR descriptions for linking keywords before submitting.
* Communicate with contributors if unlinking may impact bounty rewards.
* For merged PRs, note that links are part of the permanent record; only open PRs can be edited to change links.
* For more details, refer to GitHub’s official documentation on managing issues and pull requests.

***

If you have questions about the Lightning Bounties workflow or encounter issues, contact your repository maintainers or the Lightning Bounties support team.

***

### **Summary Table: Unlinking Methods**

| Link Type        | How to Unlink                                  | Can Unlink After Merge? |
| ---------------- | ---------------------------------------------- | ----------------------- |
| Keyword-based    | Edit/remove keywords in PR description/comment | No                      |
| Manual (sidebar) | Use "Unlink" button in sidebar                 | Yes                     |

***

\[Insert screenshot of PR description editing interface showing removal of linking keywords]

\[Insert screenshot of sidebar showing the "Unlink" button for a linked issue]

\[Insert screenshot of issue sidebar showing no linked PRs after unlinking]

This documentation ensures maintainers can confidently manage issue-PR links in both standard GitHub workflows and when using Lightning Bounties.

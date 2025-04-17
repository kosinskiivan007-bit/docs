# Detach Issues from Pull Requests

## How the Repo Maintainer can Detach Issues from Pull Requests

In GitHub, issues and pull requests may automatically link when specific keywords (e.g., "`close`", "`fixes`") are used in pull request descriptions or comments. This guide explains how to detach an issue from a pull request.

### Steps to Detach an Issue from a Pull Request

1. **Navigate to the Pull Request** - Click on the **Pull Requests** tab and locate the pull request linked to the issue.

<figure><img src="../../.gitbook/assets/repo-tabs-pull-requests-global-nav-update.webp" alt=""><figcaption></figcaption></figure>

2. **Remove the Linking Keyword** - Open the pull request description or comments where the link to the issue is mentioned. - Look for keywords like `close #issue_number`, `fixes #issue_number`, or `resolves #issue_number`. - Remove these keywords or replace them with plain text (e.g., `related to #issue_number`).

<figure><img src="../../.gitbook/assets/RemoveKeywordPRDescription.png" alt="Remove Keyword fron PR Body"><figcaption></figcaption></figure>

3. **Update the Pull Request Description** - After editing the description or comments, click the **Save** or **Update** **Comment** button to confirm your changes. :point\_down:

<figure><img src="../../.gitbook/assets/update_comment.png" alt="Update Comment"><figcaption></figcaption></figure>

4. **Verify the Detachment** - Navigate to the issue that was previously linked. - Confirm that the issue is no longer listed under the **Linked pull requests** section.&#x20;
   1. [ You can also make changes to the issue description.](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/editing-an-issue)

<div data-full-width="true"><figure><img src="../../.gitbook/assets/before2.png" alt="Issue Linked (Before)"><figcaption><p><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span><mark style="background-color:red;"><strong>Before Removing the Issue Link from the PR Body</strong></mark> <span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></p></figcaption></figure> <figure><img src="../../.gitbook/assets/after2.png" alt=""><figcaption><p> <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span><mark style="background-color:green;"><strong>After Removing the Issue Link from the PR Body</strong></mark> <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></p></figcaption></figure></div>

***

{% hint style="info" %}
After removing the issue link from the PR body, refresh the page to see the changes reflected in the PR interface. The previously linked issue will no longer appear in the related issues section. &#x20;

* [<sup>_Learn more about issue-PR relationships here_</sup>](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
{% endhint %}

{% hint style="info" %}
**Detaching &#x20;**_**the issue does not delete any comments or history.**_

* [ _Removing the linking keyword ensures that the issue and pull request are no longer automatically linked._](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)
* &#x20;_If the pull request has already been merged, the link cannot be removed._
{% endhint %}

### Lightning Bounties Considerations

* **Bounty Tracking:** Lightning Bounties tracks issue and PR status via GitHub integration. Unlinking an issue from a PR may affect bounty eligibility or payout triggers if the bounty is configured to require a linked/closed issue.
* **Workflow:** Always coordinate with your team and check Lightning Bounties [documentation ](https://docs.lightningbounties.com/docs)if you're unsure how unlinking affects bounty status.
* **Permissions:** Lightning Bounties only has [read-only access](https://docs.lightningbounties.com/docs/getting-started/first-time-onboarding/github-auth-and-lightning-bounties) to your repository and cannot modify links on your behalf. &#x20;

***

### Best Practices

* Double-check PR descriptions for linking keywords before submitting.&#x20;
* [Communicate with contributors](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests) if unlinking may impact bounty rewards.
* For merged PRs, note that links are part of the permanent record; only open PRs can be edited to change links.
* For more details, refer to GitHub’s official [documentation ](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)on managing issues and pull requests.
* ### <sub>If you have additional questions, feel free to reach out to the repository maintainers or send a note to the</sub> [<sub>Lightning Bounties Discord</sub>](https://discord.gg/zBxj4x4Cbq)

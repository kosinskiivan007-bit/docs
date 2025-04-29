# Claim Reward Criteria & Troubleshooting Guide

## Introduction

This guide outlines the complete process for claiming rewards and provides troubleshooting steps for developers working on bounties on the Lightning Bounties Platform.

## ClaimReward Criteria

To successfully claim a reward for a bounty, follow these steps:

### 1. **Register and Log In with GitHub**

{% hint style="warning" %}
### :warning: VERY Important :warning:

It’s essential to register and log in to Lightning Bounties using your GitHub account **before** submitting your PR and clicking _**"Claim Reward."**_&#x20;

* This ensures your reward is properly linked to your account and that you’re eligible to claim the bounty.
{% endhint %}

### 2. Find an Issue

* Browse available bounties on the [app.lightningbounties.com](http://app.lightningbounties.com/) feed
* Review the issue details, requirements, and reward amount
* Check if the bounty is still available (not claimed by someone else)

### 3. Fix the Issue

* Fork the repository to your GitHub account
* Clone your fork locally and create a branch for your work
* Implement the fix according to the issue requirements
* Test your changes thoroughly to ensure they meet all acceptance criteria
* Push your changes to your fork

### 4.  Create a Pull Request (PR) **Targeting Main/Master**

* Go to the original repository on GitHub.
* Click "Compare & pull request" for your branch.

{% hint style="warning" %}
:warning: **CRITICAL STEP** :warning:

In the PR description, include `close #issue-number` or `closes #issue-number` to link the PR to the issue.
{% endhint %}

> ## :information\_source: **Why?**
>
> <mark style="background-color:orange;">GitHub only recognizes linked issues when the PR targets the repository's default branch (usually main or master).</mark>&#x20;
>
> * [Learn more about linking PRs to issues.](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)

* Provide a clear explanation of your changes and how they address the issue.
* You can include as much additional information as needed in your PR description.
* Submit the PR for review

**Screenshot Example:**

<figure><img src="../../.gitbook/assets/mergedPRScreenShot_ChangeIttoGreenOpenCheckmark.png" alt="Example: PR description with correct close syntax and branch targeting."><figcaption><p>Example: PR description with correct close syntax and branch targeting.</p></figcaption></figure>

{% hint style="info" %}
_**You may need to refresh the GitHub page to see the issue show up as linked.**_
{% endhint %}

### 5. **Wait for Maintainer to Merge the PR**

* The repository maintainer will review your PR.&#x20;
  * Once it is approved and merged, the issue will be closed automatically if you used the correct `close`syntax.

### 6. Claim Reward Process

* **Manually claim your reward:**
  * Visit [app.lightningbounties.com](http://app.lightningbounties.com/) and find the Bounty you solved
  * Click the "_**Claim Reward**_" button
  * Click the "_**Check**_" button to verify your eligibility

{% hint style="warning" %}
:warning:**IMPORTANT**:warning:

The reward process will not start automatically.&#x20;

You must manually complete the claim steps on [app.lightningbounties.com](http://app.lightningbounties.com/) after your PR is merged.
{% endhint %}

<figure><img src="../../.gitbook/assets/check_claim_reward.JPG" alt="Claim Reward &#x26; Check Interface on Lightning Bounties "><figcaption><p>Claim Reward &#x26; Check Interface on <a href="https://app.lightningbounties.com/">app.lightningbounties.com</a></p></figcaption></figure>

### 7. **Once your PR is merged and your eligibility is verified, the reward will be deposited directly into your Lightning Bounties balance.**

***

### Complete Claim Process Visualization

{% tabs %}
{% tab title="Simplified Workflow" %}
<figure><img src="../../.gitbook/assets/visualworkflow.JPG" alt="Simplified Workflow"><figcaption><p>Simplified Workflow</p></figcaption></figure>
{% endtab %}

{% tab title="Complete Claim Process" %}
<div data-full-width="false"><figure><img src="../../.gitbook/assets/Complete_Claim_Process_Updated (2).png" alt="Complete Claim Process"><figcaption><p>Complete Claim Process</p></figcaption></figure></div>
{% endtab %}
{% endtabs %}

***

## Troubleshooting

### Issue Not Linked to PR

<div data-full-width="false"><figure><img src="../../.gitbook/assets/no_close_pr.JPG" alt="Example: PR without the required &#x22;close #issue-number&#x22; syntax"><figcaption><p> <em>Example: PR without the required "close #issue-number" syntax</em></p></figcaption></figure></div>

**Problem Indicators:**

* PR doesn't show linked issue in GitHub interface
* The issue remains open after PR is merged
* Reward doesn't process automatically

**Solutions:**

* **Edit PR Description**: If the PR is still open, edit it to add `close #issue-number` syntax
* **Ask Repository Owner**: If you cannot edit the PR, ask the repository owner to add the link for you
* **Create Follow-up PR**: If the PR was already merged, create a minimal follow-up PR (see below)

#### PR Merged but No Payment

<figure><img src="../../.gitbook/assets/fullowup_pr_issue.JPG" alt=""><figcaption><p><em>Example: A minimal follow-up PR correctly referencing both the issue and original</em> </p></figcaption></figure>

If your PR was merged but did not have the proper linking syntax:

1. Create a new PR with minimal changes:
   * Update documentation
   * Add a comment
   * Fix a typo
2.  In the PR description, include:

    {% code overflow="wrap" %}
    ```markdown
    close #42 This PR references the work completed in #123 (original PR).

    This follow-up PR is created to properly link the issue for Lightning Bounty payment.
    ```
    {% endcode %}
3. Notify the repository owner about this follow-up PR and explain its purpose
4. Once merged, go to Lightning Bounties and click "Claim Reward" and "Check"

#### Payment Not Received

**Verification Steps:**

1. Confirm the issue is marked as "closed" on GitHub
2. Verify the PR that closed it has been merged
3. Check that you clicked "Claim Reward" on Lightning Bounties
4. Allow up to 24 hours for processing in some cases

**Solutions:**

* **Check User Balance**: Ensure your account balance is updated on [app.lightningbounties.com](http://app.lightningbounties.com/)
* **Verify Wallet Setup**: Make sure your Lightning Network wallet is correctly configured
* **Contact Support**: If issues persist, reach out to the Lightning Bounties [Discord](https://discord.gg/zBxj4x4Cbq) for assistance

#### Common Errors and Solutions

| Error                 | Description                              | Solution                                      |
| --------------------- | ---------------------------------------- | --------------------------------------------- |
| Missing link syntax   | PR doesn't include `close #issue-number` | Edit PR description or create follow-up PR    |
| Wrong issue number    | PR references incorrect issue            | Edit PR or create new PR with correct number  |
| Not claiming reward   | Forgot to click "Claim Reward" button    | Go to Lightning Bounties app and click button |
| Issue already claimed | Another dev claimed the bounty first     | Check issue status before working on it       |

### Best Practices

* **Always double-check** the issue number when adding `close #issue-number` syntax
* **Communicate clearly** with repository maintainers about your bounty claim
* **Keep PRs focused** on addressing the specific issue
* **Don't forget** to manually click "Claim Reward" on Lightning Bounties platform
* **Set up your Lightning wallet** before working on bounties to receive payments quickly

***

Remember, the Lightning Bounties system requires both proper GitHub issue linking through the `close #issue-number` syntax AND manual claiming through the Lightning Bounties platform. Both steps are essential for successful reward processing.

For additional assistance, join the Lightning Bounties [Discord](https://discord.gg/zBxj4x4Cbq) community.

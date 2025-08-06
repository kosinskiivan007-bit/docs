# GitHub Auth & Lightning Bounties

This guide explains why Lightning Bounties uses GitHub OAuth to verify your identity.&#x20;

By linking your account, you grant just the minimal permissions needed—nothing more—so you stay in control of your data.&#x20;

### **Linking Your GitHub Account to Lightning Bounties is Necessary For Several Reasons:**

<table><thead><tr><th width="210">Authentication:</th><th>It verifies your identity and prevents fake accounts.</th></tr></thead><tbody><tr><td><strong>​Project Access:</strong></td><td>You can link your GitHub projects to post bounties on specific issues or projects.</td></tr><tr><td><strong>​​Issue Tracking:</strong></td><td>It helps you stay organized and focused on the issues that require attention.</td></tr><tr><td><strong>Collaboration:</strong></td><td>Enables effective communication and progress tracking with bug hunters.</td></tr><tr><td><strong>Reward Distribution:</strong></td><td>Ensures correct and efficient distribution of rewards.</td></tr><tr><td><strong>Profile &#x26; Reputation:</strong></td><td>Builds your reputation as a responsible project maintainer.</td></tr></tbody></table>

{% hint style="info" %}
**TLDR**: _Linking your GitHub account streamlines bug hunting, promotes collaboration, and ensures proper reward distribution._
{% endhint %}

### Understanding Permissions

When you link your GitHub account to Lightning Bounties, you will be granting us specific permissions:

* **Read-only Access**:
  * We cannot alter anything in your GitHub account.
  * This ensures that your projects and repositories remain untouched.
* **Public-only Access**:
  * We can only access information that is publicly available.
  * Any data that is private or restricted is completely off-limits to us.

### Comparison with Other GitHub Apps/Services

Many GitHub applications request broader permissions than we do. Here's a quick comparison:

<table><thead><tr><th width="155">Feature</th><th width="180" align="center">Lightning Bounties</th><th align="center">Algora PBC</th><th width="129" align="center">Replit</th><th align="center">Kodiak</th></tr></thead><tbody><tr><td><strong>Read-only Access</strong></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td><td align="center">✅</td></tr><tr><td><strong>Write Access</strong></td><td align="center">❌</td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr><tr><td><strong>Public-only Access</strong></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><strong>Access to Private Repos</strong></td><td align="center">❌</td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr></tbody></table>

### Explanation of Other Platforms:

* **Algora PBC**: Algora PBC requires broader access to your GitHub account, including the ability to verify your identity, know what resources you can access, act on your behalf, and view your email addresses.
* **Replit**: Replit also requires broader permissions, similar to Algora PBC, including the ability to verify your GitHub identity, know what resources you can access, act on your behalf, and view your email addresses.
* **Kodiak**: Kodiak is a GitHub bot that requires access to all repositories, including public repositories (read-only), and has read and write access to checks, code, issues, pull requests, and workflows.

With Lightning Bounties, you maintain greater control over your data and privacy, as we only require read-only, public access.

### Unlinking Your GitHub Account From Lightning Bounties

{% embed url="https://app.tango.us/app/workflow/Revoking-Access-for-Lightning-Bounties-User-on-GitHub-92ef1c00737d4c52b4ce542456f95848" %}
Unlinking&#x20;
{% endembed %}

If you decide to unlink your GitHub account from Lightning Bounties, please follow these instructions:

1. **Go to GitHub**: Log in to your GitHub account.
2. **Navigate to Settings**: Click on your profile picture in the top right corner, then select **Settings** from the dropdown menu.
3. **Applications**: In the left sidebar, click on **Applications**.
4. **Authorized OAuth Apps**: Under the **Authorized OAuth Apps** section, locate **Lightning Bounties**.
5. **Revoke Access**: Click on **Lightning Bounties** and then select the **Revoke Access** button.
6. **Notification: Lightning Bounties Unlinked**: If you see the message _"Lightning Bounties User has been revoked from your account"_ displayed at the top, it means you have successfully unlinked Lightning Bounties from your GitHub account.

After completing the steps to unlink your GitHub account, it will be disassociated from Lightning Bounties.&#x20;

{% embed url="https://youtu.be/LrXGUxT1riA" %}
Video Walkthrough
{% endembed %}

{% hint style="info" %}
**If you wish to link your GitHub** account **to Lightning Bounties again in the future:**

1. Visit [app.lightningbounties.com](http://app.lightningbounties.com)
2. Click on the "**Login with GitHub**" button.
3. You will be all set to continue using the platform!
{% endhint %}

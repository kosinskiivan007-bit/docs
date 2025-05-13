---
description: >-
  Need answers? Check out our FAQs. Get quick solutions and make the most of our
  Lightning Bounties.
---

# Lightning Bounties FAQ's

## General Questions:

<details>

<summary>What's Lightning Bounties?</summary>

Lightning Bounties is a Bitcoin-powered bug bounty platform that seamlessly integrates with GitHub’s familiar workflows, allowing developers to earn Bitcoin for fixing bugs and contributing to open-source projects.

Getting started is simple—no installations or complicated setups required. Just visit [**app.lightningbounties.com**](https://app.lightningbounties.com/), log in with your GitHub account, and you’re ready to post or solve bounties instantly. Lightning Bounties makes it easy for anyone to contribute their skills, support open-source innovation, and get rewarded in Bitcoin.&#x20;

</details>

<details>

<summary>Who Typically Uses Lightning Bounties?</summary>

Lightning Bounties caters to two primary groups: <mark style="background-color:orange;">developers</mark> and <mark style="background-color:green;">organizations</mark>.

<mark style="background-color:orange;">**Developers**</mark> can showcase their skills, earn Bitcoin, and contribute to the growth of open-source technology.

<mark style="background-color:green;">**Organizations**</mark> can tap into a talented pool of developers to improve the quality and security of their software projects.

</details>

<details>

<summary>Why Do I Have To Link My GitHub Account To Use Lightning Bounties?</summary>

See [github-auth-and-lightning-bounties.md](../../getting-started/first-time-onboarding/github-auth-and-lightning-bounties.md "mention")for More Detailed info:

**TLDR**: _Linking your GitHub account streamlines bug hunting, promotes collaboration, and ensures proper reward distribution._

</details>

<details>

<summary>Does Lightning Bounties Have a Token or Plan to Launch one in the Future?</summary>

Nope. Bitcoin is the best currency for Lightning Bounties because it’s decentralized, secure, and globally accessible. It aligns with our ethos of empowering developers without relying on speculative tokens.

</details>

<details>

<summary>How Does Lightning Bounties Work</summary>

Users post bounties for GitHub issues, developers solve them, and once a pull request is merged, the contributor is instantly rewarded in Bitcoin via the Lightning Network.

</details>

<details>

<summary><strong>Do I Need to Install Anything to Use Lightning Bounties?</strong></summary>

No installations are required. Simply log in with your GitHub account to get started.

</details>

<details>

<summary><strong>Who Can Use Lightning Bounties?</strong></summary>

Anyone with a GitHub account can use Lightning Bounties to post or solve bounties—no restrictions based on location or experience level.

</details>



## Bounty Hunter Questions

<details>

<summary>How Do I Find Bounties to Work On?</summary>

Visit app.lightningbounties.com and browse the "Available Bounties" section. You can filter bounties by:

* Technology/programming language
* Reward amount
* Time commitment
* Repository popularity

Find an issue that matches your skills and interests, then click to view details about the task and reward.

</details>

<details>

<summary>How Do I Submit a Solution?</summary>

1. Fork the GitHub repository containing the issue
2. Create a branch for your solution
3. Make your changes and commit them
4. Submit a Pull Request referencing the issue number
5. Once merged by the repository maintainer, your reward will be automatically processed

</details>

<details>

<summary>How Are Rewards Distributed?</summary>

Once your pull request is merged, the GitHub API acts as an oracle to verify your contribution. The Lightning Bounties platform then automatically sends the reward to your account, where you can withdraw it to your Lightning wallet.

</details>

<details>

<summary>How Do I Withdraw My Earnings?</summary>

1. Visit your Lightning Bounties account dashboard
2. Click on "Withdraw"
3. Generate a Lightning invoice from your wallet
4. Paste the invoice into the withdrawal field
5. Confirm the withdrawal
6. Receive funds instantly in your Lightning wallet

</details>

<details>

<summary>What Happens if My Solution is Rejected?</summary>

If your solution is rejected, the bounty remains open for you or others to attempt again. The repository maintainer typically provides feedback on why the solution wasn't accepted, giving you an opportunity to improve and resubmit.

</details>

<details>

<summary>Can I Work on Multiple Bounties at Once?</summary>

Yes! You can work on as many bounties as you'd like simultaneously. There are no restrictions on the number of bounties you can tackle at one time.

</details>

<details>

<summary>Do I Need to Run a Lightning Node to Receive Payments?</summary>

Nope, you don't need to run a node to use the Lightning Network. You can simply use a lightning wallet app to send and receive payments.

</details>

<details>

<summary>What Lightning Wallets Can I Use?</summary>

Popular Lightning Network wallets include:

* Phoenix
* Muun
* Breez
* Wallet of Satoshi
* Blue Wallet
* Cash App

Any Lightning-compatible wallet that supports BOLT-11 invoices will work with Lightning Bounties.

</details>

<details>

<summary>How Do I Convert Sats to My Local Currency?</summary>

After withdrawing to your Lightning wallet, you can:

1. Transfer to an exchange that supports Lightning Network deposits
2. Convert to your local currency on the exchange
3. Withdraw to your bank account

Alternatively, some Lightning wallets offer direct conversion features.

</details>

<details>

<summary>Why Might My Lightning Withdrawal Fail?</summary>

Lightning Network transactions can fail for a few common reasons:

* Not having enough funds in your channel to cover the payment
* Routing issues in the Lightning Network
* Using an expired invoice
* Network congestion

Keep approximately 2% of your withdrawal amount in your account to cover Lightning Network routing fees.

</details>

## Posting a Bounty

<details>

<summary>How Do I Post a Bounty?</summary>

**TLDR**: _Log in with your GitHub account, copy-paste the issue URL, set a reward amount in Bitcoin, and post it in just a few clicks_.

1. Log in to Lightning Bounties with your GitHub account
2. Click "Post a Bounty"
3. Enter the URL of the GitHub issue
4. Set the reward amount in sats
5. Define the lock time period
6. Submit the bounty

</details>

<details>

<summary>Can I Increase the Reward for an Existing Bounty?</summary>

**TLDR:** _Yes, you can increase the reward for an open bounty at any time by adding more sats (Bitcoin micropayments)._

This is useful if you want to attract more attention to a high-priority issue or if the complexity turned out to be greater than initially estimated.

</details>

<details>

<summary>What Happens If No One Solves My Issue?</summary>

If no one solves your issue, you can manually expire the bounty after the lock time ends and reclaim your funds.

</details>

<details>

<summary>How Do I Review Submitted Solutions?</summary>

You'll review solutions through GitHub's standard pull request workflow:

1. Receive a notification when a PR is submitted
2. Review the code changes
3. Request changes or approve and merge the PR
4. Once merged, the reward is automatically processed by Lightning Bounties

</details>

<details>

<summary>How Do I Deposit Funds to Post Bounties?</summary>

1. Log into your Lightning Bounties account
2. Navigate to the "Deposit" section
3. Generate a Lightning invoice in your Lightning Bounties account
4. Pay the invoice using your Lightning wallet
5. Funds will be credited to your account instantly

</details>

<details>

<summary>What is a Bounty Lock Time?</summary>

**TLDR:** _A lock time guarantees that the reward remains available for a set period (e.g., two weeks) while developers work on solving the issue_.

The lock time ensures that funds stay committed to the bounty, giving developers confidence that they'll be paid for their work once completed.

</details>

<details>

<summary>Can Multiple Users Fund a Single Bounty?</summary>

Yes! Lightning Bounties supports crowdfunding for bounties. Multiple users can contribute sats to increase the reward for a single issue, making it more attractive to potential solvers.

</details>

<details>

<summary>Can I Set Custom Requirements for Bounties?</summary>

Yes! You can specify requirements in the GitHub issue description, such as:

* Required tests
* Performance criteria
* Documentation standards
* Compatibility requirements
* Code style guidelines

These requirements will be visible to developers considering your bounty.

</details>

<details>

<summary>Can I Post Bounties for Third-Party Projects?</summary>

Yes! You can post bounties for any open-source project on GitHub, even if you're not the project owner.

</details>

<details>

<summary>Can I Expire a Bounty Early?</summary>

You can only expire a bounty and reclaim funds after the initial lock time has passed. This protection ensures developers have the promised time to work on solutions without the bounty being unexpectedly withdrawn.

</details>



## Lightning Bounties Features FAQ's

### Anonymous Rewards

<details>

<summary>What are Anonymous Rewards?</summary>

Anonymous Rewards allows logged-in users to contribute sats to bounties privately, ensuring their identity remains hidden while still supporting open-source development. This feature enables users to fund bounties discreetly while maintaining full control over their contributions\[4].

</details>

### Crowdfunding Bounties

<details>

<summary>How do Crowdfunding Bounties work?</summary>

The Collaborative Funding feature allows multiple users to contribute sats (Bitcoin microtransactions) to fund a single bounty. This enables community-driven funding for important issues and helps bounties grow faster by allowing multiple contributors\[5].

</details>

### No Installations Required

<details>

<summary>Do I need to install anything to use Lightning Bounties?</summary>

No. Posting or solving a bounty requires no plugins, no installations on your computer, and no changes to your GitHub account. Simply log in with your GitHub account to get started\[5]\[1].

</details>

### GitHub API as Oracle

<details>

<summary>How does the GitHub API as Oracle feature work?</summary>

This feature uses the GitHub API to automatically verify when solutions are accepted. Rewards are automatically sent to contributors once their pull request is successfully merged, preventing fraudulent claims\[5].

</details>

### Guaranteed Escrow

<details>

<summary>What is the Guaranteed Escrow feature?</summary>

Rewards are locked for a set period (e.g., two weeks) to ensure bounty hunters know the reward will be available when they submit their solution. This lock time guarantees that the reward remains available while developers work on solving the issue\[5]\[1].

</details>

### Flexible Expiry Options

<details>

<summary>What happens if no one solves my bounty?</summary>

After the lock time ends, you can manually expire the bounty and reclaim your funds if priorities change or the issue is resolved elsewhere. If no one solves your issue, you can reclaim your funds after the lock time expires\[5]\[1].

</details>

### Support for Third-Party Projects

<details>

<summary>Can I post bounties for projects I don't own?</summary>

Yes! You can post bounties on issues from popular open-source projects like VSCode, Django, or React-even if you're not the project owner. This allows you to support any open-source project on GitHub\[5]\[1].

</details>

### Add Without Login

<details>

<summary>What is the Add Without Login feature?</summary>

Add Without Login enables anyone to contribute sats to existing bounties without needing to create an account or log in. This makes it easier for non-developers or those without GitHub accounts to get involved. The feature leverages Branta's address verification for security\[4].

</details>

### No Banking Restrictions

<details>

<summary>Does Lightning Bounties work worldwide?</summary>

Yes! Lightning Bounties operates globally with Bitcoin, bypassing region-restricted payment processors like Stripe. Anyone with a GitHub account can use Lightning Bounties to post or solve bounties-no restrictions based on location or experience level\[5]\[1].

</details>

### Effortless Setup

<details>

<summary>How long does it take to post a bounty?</summary>

It takes just 5 clicks and a single copy-paste of a URL to post a bounty-under 30 seconds from start to finish. Getting started is simple-no installations or complicated setups required\[5]\[3].

</details>


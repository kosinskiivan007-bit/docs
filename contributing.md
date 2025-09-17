---
description: >-
  Improve Lightning Bounties documentation and earn Bitcoin! Fix typos, add
  guides, or enhance clarity through our simple bounty platform. Get paid in
  sats for merged contributions.
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Contribute to Lightning Bounties Docs & Earn Bounties

## Contribute to Lightning Bounties Docs & Earn Bitcoin

Want to make our documentation even better? First of all, thank you! This page will guide you through our contribution process, including how to submit changes and claim bounties for your contributions.

#### Prerequisites

To edit our documentation, you must have a [GitHub account](https://github.com). If you already have one, make sure you are logged in. If you don't, please [create one](https://github.com/join).

#### Understanding GitBook's Integration with GitHub

We use a platform called [GitBook](https://gitbook.com) to host, manage and serve our documentation. GitBook fetches files from our GitHub repository `Lightning-Bounties/docs`, reads them and converts them into the pages you can access on [docs.lightningbounties.com](https://docs.lightningbounties.com).

**Repository Structure**

A generic structure of documentation hosted on GitBook looks like this:

```

Getting Started
├── First-Time Onboarding
│   ├── GitHub Auth \& Lightning Bounties
│   ├── Account Setup
├── Posting a Bounty
│   ├── Create GitHub Issue
│   ├── Submit New Reward
├── Solving a Bounty
│   ├── Working on the Bounty
│   ├── Claiming Rewards
│   └── Withdraw Funds
```

Its mirror to GitHub has the following structure:

```markup

├── .gitbook/
│   └── assets/
│       └── screenshot-claim-interface.png
├── getting-started/
│   ├── first-time-onboarding/
│   │   ├── README.md
│   │   ├── github-auth-and-lightning-bounties.md
│   │   └── account-setup.md
│   ├── posting-a-bounty/
│   │   ├── README.md
│   │   ├── create-github-issue.md
│   │   └── submit-new-reward.md
│   ├── solving-a-bounty/
│   │   ├── README.md
│   │   ├── working-on-the-bounty.md
│   │   ├── claiming-rewards.md
│   │   └── withdraw-funds.md
├── resources/
│   ├── frequently-asked-questions/
│   │   └── lightning-bounties-faqs.md
│   └── troubleshooting/
├── README.md
└── SUMMARY.md
```

**Key Components:**

* The `.gitbook/assets` folder manages every file used in any page
* The `SUMMARY.md` file tells GitBook the order and grouping of pages
* The `README.md` file contains the first page content users see
* Groups of pages are controlled by folders named after the group title
* Nested pages have a similar structure, but require a `README.md` file in the parent folder

### Method 1: Quick Editing via GitHub Web Interface

#### **Step 1: Access the Edit Function**

1. Open the page you want to edit on [docs.lightningbounties.com](https://docs.lightningbounties.com)
2. Look for an "Edit on GitHub" button above the Table of Contents on the right side
3. Click on the GitHub icon to navigate to the Markdown file

<figure><img src=".gitbook/assets/image (70).png" alt="Edit on GitHub button location above table of contents on docs page"><figcaption><p>Edit on GitHub button location above table of contents on all docs page</p></figcaption></figure>

#### **Step 2: Edit the File**

1. Click on the pencil icon labeled "Edit this file"
2. Make your edits using [Markdown formatting](https://gitbook.com/docs/creating-content/formatting/markdown)
3. Use GitBook's [Markdown reference guide](https://gitbook.com/docs/creating-content/formatting/markdown) for proper formatting

<figure><img src=".gitbook/assets/image (72).png" alt="Screenshot: GitHub edit interface showing pencil icon on Lightning Bounties docs file"><figcaption><p>GitHub edit interface showing pencil icon on Lightning Bounties docs repo  </p></figcaption></figure>

#### **Step 3: Create Your Pull Request**

1. Scroll down to the "Commit changes" section
2. Write a short, descriptive title for your changes
3. Add a detailed description explaining your improvements
4. **Important**: Include `close #[issue-number]` in your description if you're fixing a specific issue
5. Select "Create a new branch for this commit and start a pull request"
6. Click "Propose file change"

<figure><img src=".gitbook/assets/image (74).png" alt="Screenshot of the Commit changes box. There are boxes for a brief description of the changes, an extended one, a selection menu for email addresses to associate with the commit, options to commit directly to the current branch or to create a new branch and a pull request (which opens an option to name your branch as you like) and buttons to either Propose file change or Cancel."><figcaption><p>Screenshot of the Commit changes box. There are boxes for a brief description of the changes, an extended one, a selection menu for email addresses to associate with the commit, options to commit directly to the current branch or to create a new branch and a pull request (which opens an option to name your branch as you like) and buttons to either Propose file change or Cancel.</p></figcaption></figure>

#### **Step 4: Submit Your Pull Request**

1. On the Pull Request page, add a clear comment explaining your changes
2. **Critical Step**: Ensure your PR description includes `close #[issue-number]` syntax if applicable
3. Click "Create pull request"

<figure><img src=".gitbook/assets/image (75).png" alt="Screenshot of the Pull request page. It shows a box for the title of the Pull request, another for any comments. Below them, there&#x27;s a Create pull request button."><figcaption><p>Screenshot of the Pull request page. It shows a box for the title of the Pull request, another for any comments. Below them, there's a Create pull request button.</p></figcaption></figure>

### Method 2: Local Development Workflow

#### **Step 1: Fork and Clone**

1. Navigate to the [Lightning-Bounties/docs](https://github.com/Lightning-Bounties/docs) repository
2. Click the "Fork" button to create your personal copy
3. Clone your fork locally:

```bash

git clone https://github.com/YOUR-USERNAME/docs.git
cd docs

```

#### **Step 2: Create a Feature Branch**

```bash

git checkout -b improve-bounty-guide

```

#### **Step 3: Make Your Changes**

1. Edit the relevant Markdown files using your preferred editor
2. Follow GitBook's formatting guidelines
3. Place any images in the `.gitbook/assets/` folder
4. Test your changes locally if possible

#### **Step 4: Commit and Push**

```bash

git add .
git commit -m "Improve bounty claiming guide with clearer steps"
git push origin improve-bounty-guide

```

#### **Step 5: Create Pull Request**

1. Navigate to your fork on GitHub
2. Click "New Pull Request"
3. **Essential**: Include `close #[issue-number]` in the PR description
4. Provide clear explanation of your changes
5. Submit the pull request

***

#### Lightning Bounties Payment System

{% hint style="warning" %}
#### The Critical **`close #[issue-number]` Syntax**

To earn Bitcoin bounties for your contributions, you **must** include the `close #[issue-number]` syntax in your pull request description.&#x20;

This connects your PR to the Lightning Bounties issue and triggers automatic payment processing.
{% endhint %}

**Important Notes:**

* The `close` keyword must be in the PR description itself, not in regular comments
* Adding this connection after merging will automatically trigger Lightning Bounty payment
* If you forget to add this initially, you can edit your merged PR description later

### **If You Forgot the Close Syntax**

**Option 1: Edit Your Merged Pull Request**

1. Go to your merged PR and click into it
2. Click the "..." button at the top-right of your PR description
3. Select "Edit"
4. Add `close #[issue-number]` to your PR description
5. Click "Update Comment"

**Option 2: Ask for Help**

If you cannot edit the PR, ask the repository owner to add the `close` syntax for you.

{% hint style="warning" %}
[**See Here For Full Troubleshooting Guide**](https://docs.lightningbounties.com/docs/getting-started/solving-a-bounty/claim-reward-criteria-and-troubleshooting-guide)&#x20;
{% endhint %}

### Claiming Your Bitcoin Bounty

**Step-by-Step Claiming Process**

1. **Visit the Platform**: Go to [app.lightningbounties.com](https://app.lightningbounties.com)
2. **Find Your Bounty**: [Look for your bounty](https://docs.lightningbounties.com/docs/getting-started/solving-a-bounty/looking-for-a-project-to-get-rewarded)
   * Example: _"Help Improve Lightning Bounties Documentation and Earn Sats!"_
3. **Claim Your Reward**:
   * Click on "Claim Reward"
   * Add your pull request number
   * Click the "Check" button to verify eligibility
4. **Receive Payment**: The reward will be added to your balance and paid instantly via the Lightning Network

<figure><img src=".gitbook/assets/solvedCard (1).png" alt=""><figcaption></figcaption></figure>

**Payment Requirements**

* Your pull request must be merged
* The PR description must contain `close #[issue-number]` syntax
* Lightning Bounties uses the GitHub API as an oracle to prevent fraudulent claims
* Payments are processed automatically when all conditions are met

#### Content Guidelines

**Writing Best Practices**

* Use clear, concise language suitable for global developers
* Follow consistent Markdown formatting
* Include relevant links to Lightning Bounties resources
* Ensure proper heading hierarchy (H1, H2, H3, etc.)
* Test all external links for functionality
* Explain Bitcoin and Lightning Network concepts for newcomers
* Use simple examples and step-by-step instructions

**Technical Standards**

* Keep contributions focused on specific improvements
* Follow existing file structure and naming conventions
* Optimize images and include descriptive alt text
* Use proper Git commit message conventions
* Include screenshots for complex UI interactions
* Add troubleshooting sections where appropriate

#### **Documentation Priorities**

**High-Value Contributions:**

* Fix typos, grammar errors, and broken links
* Simplify complex technical explanations
* Add missing screenshots and visual guides
* Improve navigation and cross-referencing
* Create troubleshooting guides for common issues
* Add context for international users

**Content Areas Needing Help:**

* Bounty hunter onboarding guides
* Wallet setup and Lightning Network basics
* Platform troubleshooting and FAQ sections
* API documentation and integration examples
* Global accessibility improvements

**Community Engagement**

* Respond promptly to feedback during reviews
* Be open to suggestions from maintainers
* Credit sources appropriately when building on existing work
* Maintain professional and constructive communication
* Help other contributors in discussions

#### Getting Support

For additional help with contributions:

1. **Documentation**: Check our detailed guides at [docs.lightningbounties.com](https://docs.lightningbounties.com)
2. **Community**: Join our [Discord](https://discord.com/invite/zBxj4x4Cbq) for real-time assistance
3. **GitHub Issues**: Report bugs or request features on our [docs repository](https://github.com/Lightning-Bounties/docs/issues)

#### What We're Looking For

**Simple Fixes (Great for Beginners)**

* Typos and grammar corrections
* Broken or outdated links
* Formatting inconsistencies
* Missing punctuation
* Unclear instructions
* Add missing alt-text to images

**Content Improvements**

* Step-by-step tutorials with screenshots
* Troubleshooting guides for common problems
* Beginner-friendly explanations of Bitcoin/Lightning concepts
* Real-world examples and use cases
* Better organization and navigation

**Global Accessibility**

* Simplifying US-centric references
* Nostr Guide's For Lightning Bounties
* Explain Bitcoin terminology for newcomers
* Including multiple Lightning wallet guides
* Clarifying payment processing variations

#### Lightning Bounties Platform Benefits

* **No Installation Required**: Simply log in with your GitHub account
* **Instant Bitcoin Payments**: Receive rewards immediately after PR approval via Lightning Network
* **Global Accessibility**: Available worldwide, bypassing traditional banking restrictions
* **Crowdfunding Support**: Multiple users can fund single documentation bounties
* **Automated Validation**: GitHub API integration prevents fraudulent claims
* **Fair Compensation**: Earn Bitcoin for improving open-source documentation

#### Common Documentation Bounties

| Contribution Type           | Typical Reward     | Description                    |
| --------------------------- | ------------------ | ------------------------------ |
| Typo fixes                  | 1,000-2,000 sats   | Grammar, spelling, punctuation |
| Broken links                | 2,000-2,500 sats   | Fix outdated or incorrect URLs |
| Clarity improvements        | 5,000-10,000 sats  | Simplify complex explanations  |
| Screenshots/Video Tutorials | 8,000-15,000 sats  | Add missing visual guides      |
| New sections                | 15,000-25,000 sats | Create new documentation pages |
| Major guides                | 30,000+ sats       | Comprehensive tutorials        |

_Amounts vary based on complexity and Bitcoin price_

#### Recognition Program

Contributors who improve our documentation receive:

* Bitcoin bounty payments via Lightning Network
* Recognition in monthly blog posts
* Priority access to future documentation bounties
* LinkedIn recommendations for significant contributions

Thank you for helping us improve our documentation and contributing to the Bitcoin development ecosystem! Your contributions help make Lightning Bounties more accessible and valuable for developers worldwide, especially those in regions underserved by traditional payment systems.

***

{% hint style="warning" %}
**Remember**: Always include `close #[issue-number]` in your pull request description to ensure you receive your Bitcoin bounty reward!
{% endhint %}

{% hint style="info" %}
**New contributor?** Start with simple fixes like typos or broken links. You'll quickly learn our documentation style and can work up to larger bounties!
{% endhint %}


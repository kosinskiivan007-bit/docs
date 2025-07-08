---
description: >-
  A simple safety check to confirm your Lightning payment destination before
  sending Bitcoin.
cover: ../../../.gitbook/assets/branta_banner.png
coverY: 0
layout:
  width: default
  cover:
    visible: true
    size: hero
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
---

# Verify with Branta

<figure><img src="https://pplx-res.cloudinary.com/image/upload/v1751987790/gpt4o_images/f0ywh41pzmspa4ywfasp.png" alt="Lightning Bounties contribution sequence"><figcaption><p>Lightning Bounties contribution sequence</p></figcaption></figure>

### What is [Branta](https://branta.pro/) Verification?

[**Verify with Branta** ](https://branta.pro/)is an optional security feature that lets you double-check a Lightning invoice before paying it on Lightning Bounties. When you see a "_**Verify Invoice - Branta**_" link under any payment form, clicking it opens a separate page that confirms the invoice destination is legitimate.

<figure><img src="../../../.gitbook/assets/verifyBranta.gif" alt="typical Lightning Bounties payment form with the Branta verification link highlighted below the QR code"><figcaption><p>T<em>ypical Lightning Bounties payment form with the Branta verification link highlighted below the QR code</em></p></figcaption></figure>

{% hint style="info" %}
**Why Branta verification matters**:

* **Prevents man-in-the-middle attacks** that could redirect payments
* **Provides independent confirmation** outside Lightning Bounties infrastructure
* **Protects against clipboard malware** and browser extension interference
* **Offers multi-device verification** capability for high-value contributions
{% endhint %}

### Where You'll Find Verification

You can use Branta verification in three ways on Lightning Bounties:

| Payment Method                 | Where to Find It                        |
| ------------------------------ | --------------------------------------- |
| **Account Deposits**           | Deposit modal when funding your account |
| **Adding Rewards (Logged In)** | Add Reward modal on bounty pages        |
| **Anonymous Contributions**    | Anonymous Add Reward flow               |

> For detailed steps on anonymous contributions, see our guide: [Add Rewards to a Bounty without Login](add-rewards-to-a-bounty-without-login.md)

### How to Verify an Invoice

#### Step 1: Generate Your Invoice

1. Complete your payment form (deposit, add reward, etc.)
2. Click "Generate Invoice" or similar button
3. Look for the QR code and invoice details

#### Step 2: Click Verify

1. Find the "Verify Invoice - Branta" link below the QR code
2. Click it - a new tab will open
3. Wait 1-2 seconds for verification to complete

<div><figure><img src="../../../.gitbook/assets/addressVerified.jfif" alt=""><figcaption><p><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span> <strong>Address Verified</strong> <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span><strong>OK TO SEND FUNDS</strong> <span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></p></figcaption></figure> <figure><img src="../../../.gitbook/assets/addressNotVerified.jfif" alt=""><figcaption><p>⛔ <strong>Address Not Verified</strong> ⛔ <strong>DO NOT SEND FUNDS</strong> ⛔</p></figcaption></figure></div>

<sub>_This_</sub><sub>_&#x20;_</sub><sub>_**optional yet highly-recommended safety check**_</sub><sub>_&#x20;_</sub><sub>_is especially critical for no-login users who lack account-based recovery options_</sub>

#### Step 3: Check the Results

* **Green "Verified"** = Safe to pay
* **Red warning** = DO NOT PAY - generate a new invoice

#### Step 4: Complete Payment

Return to Lightning Bounties and pay the invoice with your Lightning wallet.

### Example: Anonymous Reward Verification

Here's how verification works when adding rewards anonymously:

1. **Navigate to a bounty** on Lightning Bounties
2. **Click "Add Reward"** (no login required)
3. **Enter your amount** and generate the invoice
4. **Click "Verify Invoice - Branta"**
5. **Confirm green verification** before paying

<figure><img src="../../../.gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>

> For the complete anonymous contribution process, see: [Adding Anonymous Rewards to a Bounty](adding-anonymous-rewards-to-a-bounty.md)

### Quick Security Comparison

| Without Verification    | With Verification          |
| ----------------------- | -------------------------- |
| Trust the website alone | Independent confirmation   |
| Single point of failure | Backup verification system |
| No tamper detection     | Alerts for fake invoices   |

### FAQ

<details>

<summary><strong>Is verification required?</strong></summary>

No, but it's strongly recommended for your security.

</details>

<details>

<summary> <strong>Does Branta see my wallet or private keys?</strong></summary>

Never. It only checks the public invoice string.

</details>

<details>

<summary><strong>What if verification fails?</strong></summary>

Don't pay! Generate a new invoice or [contact support.](https://discord.gg/zBxj4x4Cbq)

</details>

<details>

<summary><strong>Can I verify on mobile?</strong></summary>

Yes, works on any device with a browser.

</details>

### Related Guides

* [Add Rewards to a Bounty without Login](add-rewards-to-a-bounty-without-login.md)
* [Adding Anonymous Rewards to a Bounty](adding-anonymous-rewards-to-a-bounty.md)
* [Add Rewards to an Existing Bounty](./)

***

_Verify with Branta makes Lightning payments on Lightning Bounties safer without adding complexity to your workflow._

<figure><img src="../../../.gitbook/assets/branta_lb_partnership.JPG" alt="Verify with Branta makes Lightning payments on Lightning Bounties safer without adding complexity to your workflow."><figcaption></figcaption></figure>

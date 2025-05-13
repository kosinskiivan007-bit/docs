# Lightning Network FAQ's



<details>

<summary>How many Satoshi’s (Sats) are in one Bitcoin?</summary>

Each of the 21 million units of Bitcoin that will ever exist can be broken down further into 100,000,000 satoshis.

</details>

<details>

<summary>Are Lightning Wallets the Same as Bitcoin Wallets?</summary>

Not exactly. Lightning wallets are specifically designed to interact with the Lightning Network, while traditional Bitcoin wallets handle on-chain transactions. However, many modern wallets support both types of transactions.

Some wallets are Lightning-only, some are on-chain only, and some are hybrid wallets supporting both payment methods.

</details>

<details>

<summary>Why do Lightning Invoices Expire?</summary>

Why do invoices expire? If invoices had no expiry, recipients would likely run into memory/storage issues as the number of locally stored preimages grows with each payment attempt.

_Credit: bitcoin.design_

</details>

<details>

<summary>What is a Lightning Network channel?</summary>

A Lightning Network channel is a peer-to-peer payment channel that enables instant and low-cost transactions between two parties.

</details>

<details>

<summary>How do I open a Lightning Network channel?</summary>

Open a channel by sending a small amount of Bitcoin to another node or wallet, which serves as a deposit for the channel.

</details>

<details>

<summary>Do I need to run a Lightning Network node to use the network?</summary>

Nope, you don't need to run a node to use the Lightning Network. You can simply use a lightning wallet app to send and receive payments.

</details>

<details>

<summary>What is a "channel reserve" and how does it affect my onboarding experience?</summary>

Channel reserve is the amount of Bitcoin required to open a payment channel. Higher reserves can make it harder to find nodes and open channels.

</details>

<details>

<summary>What should I do if my Lightning transaction fails while trying to pay someone?</summary>

Lightning Network transactions can fail for a few common reasons. The most frequent one is usually just not having enough funds in your channel to cover the payment. Make sure you've got enough money in the account you're sending from and don't forget to factor in the network fees (\~2% of the total amount you are trying to send).

Another common issue is the transaction not being able to find a route to the recipient's Lightning node. If that happens, just try again a few minutes later.

The Lightning Network is still evolving, so some failed transactions are normal. **But those two things - insufficient funds and routing problems - tend to be the main culprits when a Lightning payment doesn't go through.**

</details>

<details>

<summary>What Are Some Real-World Use Cases For The Lightning Network?</summary>

The Lightning Network enables all sorts of exciting use cases, like instant micropayments, pay-per-use services, digital tipping, and more. It also has the potential to bring financial services to the unbanked and underbanked around the world.

</details>

<details>

<summary>Is The Lightning Network Secure?</summary>

Like Batman protecting Gotham, the Lightning Network has multiple layers of security to keep your funds safe. With features like multi-signature wallets and onion routing, your sats are in good hands.

</details>

<details>

<summary>Can I Use The Lightning Network For Sending Large Transactions?</summary>

While the Lightning Network is great for small, frequent transactions, it may not be ideal for large transactions due to liquidity constraints. For larger sums, it's best to stick to on-chain Bitcoin transactions.

</details>

<details>

<summary>What Are Some Benefits With Using The Lightning Network For Web3 Development?</summary>

The Lightning Network's instant, low-cost transactions make it the ideal payment solution for the fast-paced world of web3 development. Developers can receive their rewards in Bitcoin almost immediately, without the hassle of high fees or long confirmation times.

</details>

<details>

<summary>What Are Zaps? ⚡️</summary>

⚡️Zaps are a way to send a small amount of Bitcoin (sats) to someone's Lightning wallet, along with a message or information, like a memo or a link. It's like sending a text message, but with a tiny amount of Bitcoin attached.

</details>

<details>

<summary>What are mSats (millisats)?</summary>

mSats are each 1/1000 (a thousandth) of a satoshi. A satoshi is the smallest unit for bitcoin, but lightning can transact with even smaller units while channels are open. The amount is [rounded down](https://github.com/lightningnetwork/lnd/blob/master/lnwire/msat.go#L22-L24) to the nearest satoshi when the channel is closed and broadcast to the blockchain to adhere to Bitcoin's limit.

![](https://static.wixstatic.com/media/8b683e_5fadb3f8111444c8902ff8ddadd28c7d~mv2.jpeg/v1/fill/w_1344,h_449,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/8b683e_5fadb3f8111444c8902ff8ddadd28c7d~mv2.jpeg)\


</details>




---
description: Top 50 Bitcoin & Lightning Network Terms for Bounty Hunters
---

# Bitcoin & Lightning Terms

### A

#### Address

A string of alphanumeric characters representing a destination for a Bitcoin payment, similar to an email address or bank account number.

#### Altcoin

Any cryptocurrency other than Bitcoin.

#### ACINQ

A company that develops Lightning Network products including Phoenix wallet and Eclair implementation.

### B

#### Base Layer

The main Bitcoin blockchain where final settlement occurs, as opposed to second-layer solutions like Lightning Network.

#### Bitcoin

A decentralized digital currency created in 2009 by Satoshi Nakamoto that operates without a central authority.

#### Bitcoin Core

The reference implementation of Bitcoin software that serves as the standard for the Bitcoin protocol.

#### Bitcoin Pizza Day

May 22nd, commemorating the first real-world Bitcoin transaction in 2010 when Laszlo Hanyecz paid 10,000 BTC for two pizzas.

#### Bitcoin Whitepaper

The original document published by Satoshi Nakamoto in 2008 titled "Bitcoin: A Peer-to-Peer Electronic Cash System."

#### Block

A collection of transactions bundled together and added to the blockchain.

#### Block Height

The number of blocks preceding a particular block in the blockchain.

#### Block Reward

The new bitcoins distributed by the network to miners for each successfully mined block.

#### Blockchain

A distributed ledger technology that maintains a continuously growing list of records (blocks) secured using cryptography.

### C

#### Channel

A payment connection between two Lightning Network nodes that allows for multiple transactions without touching the Bitcoin blockchain.

#### Cold Storage

Keeping bitcoin offline in a device or medium not connected to the internet for enhanced security.

#### Consensus

The process by which all nodes in the network agree on the state of the blockchain.

#### Custodial Wallets&#x20;

A custodial wallet is a wallet wherein the user’s private keys are held by a third party, such as an exchange. The third party has full control over the user’s funds, while the user only has permission to send and receive bitcoin.

The third party is responsible for providing a backup to the wallet in case the user forgets their login information. A custodial wallet is subject to the security practices of the third party, which reduces the users responsibility, but creates an increased risk to the seed phrase and the keys stored by the wallet if the third party is hacked.

### F

#### Fee Market

The dynamic system where Bitcoin transaction fees are determined by supply (block space) and demand (pending transactions).

#### Full Node

A computer running software that fully validates transactions and blocks on the Bitcoin network.

### H

#### Halving

An event occurring approximately every four years where the block reward for mining new Bitcoin blocks is cut in half.

#### Hard Fork

A permanent divergence in the blockchain that occurs when non-upgraded nodes can't validate blocks created by upgraded nodes following newer consensus rules.

#### Hardware Wallet

A physical device designed to securely store cryptocurrency private keys offline.

#### Hash Rate

The computational power being used by miners to secure the Bitcoin network.

### L

#### Layer 2

Solutions built on top of the Bitcoin blockchain to improve scalability, such as the Lightning Network.

#### Lightning Invoinces

Users of the lightning network use a lightning invoice to request a payment. It is defined by [BOLT 11](https://github.com/lightningnetwork/lightning-rfc/blob/master/11-payment-encoding.md) and includes an amount to be paid, destination of the payment, and an optional message. Unlike bitcoin addresses, lightning invoice’s expire after a set amount of time. By default, this is set to 60 minutes.

#### Lightning Network

A second-layer payment protocol that operates on top of Bitcoin to enable fast, scalable transactions and micropayments.

#### Lightning Service Provider (LSP)

A service that helps users establish channels and manage liquidity on the Lightning Network.

#### Liquidity

The availability of bitcoin in payment channels that enables routing of payments through the Lightning Network.

#### LNURL

A protocol for Lightning Network that simplifies the process of connecting applications to Lightning wallets.

#### LND (Lightning Network Daemon)

A complete implementation of a Lightning Network node by Lightning Labs.

### M

#### Mempool

The waiting area for unconfirmed Bitcoin transactions before they're included in a block.

#### Multisig (Multi-signature)

A security feature that requires multiple signatures to authorize a Bitcoin transaction.

### N

#### Node

A computer connected to the Bitcoin or Lightning network that validates transactions according to network rules.

#### Non-custodial Wallets

Non-custodial wallets give the user full control over their funds and the associated private keys. By using a non-custodial wallet, a user is their own bank; they can initiate transactions, and are responsible for the security of their wallet, including protection of their seed phrase, which can be used to restore their wallet if it’s lost or compromised.

#### Nostr

A decentralized social network protocol often used by the Bitcoin community, with integration capabilities for Lightning payments.

### O

#### On-chain

Transactions that occur directly on the Bitcoin blockchain, not on second-layer solutions.

#### Off-chain

Transactions that occur outside the Bitcoin blockchain, such as those on the Lightning Network.

#### Open Source

Software whose source code is publicly available, allowing anyone to inspect, modify, and enhance it.

### P

#### Private Key

A secret number that allows bitcoins to be spent, functioning as a password that gives access to your bitcoin.

#### Public Key

A cryptographic code derived from a private key, used to create Bitcoin addresses for receiving funds.

### R

#### RGB

A protocol for issuing and transferring digital assets on Bitcoin and Lightning Network.

#### Routing

The process of finding a path through multiple payment channels to complete a Lightning Network payment.

### S

#### Satoshi (sat)

The smallest unit of Bitcoin, equal to 0.00000001 BTC. Named after Bitcoin's creator.

#### Satoshi Nakamoto

The pseudonymous creator of Bitcoin whose true identity remains unknown.

#### SegWit (Segregated Witness)

A Bitcoin protocol upgrade that changed how data is stored in blocks, increasing capacity and fixing transaction malleability.

#### Self-Custody

Maintaining full control of your private keys and thus your bitcoin, rather than relying on a third party.

#### Soft Fork

A change to the Bitcoin protocol where only previously valid blocks/transactions are made invalid, backward-compatible with older versions.

### T

#### Taproot

A Bitcoin upgrade implemented in 2021 that improved privacy, efficiency, and smart contract functionality.

#### Testnet

An alternative Bitcoin blockchain providing developers with a testing environment without using real bitcoin.

#### Timelock

A feature that restricts spending bitcoin until a specified future time or block height.

#### Tor

An anonymity network often used by Bitcoin nodes to increase privacy by concealing users' locations and usage.

### U

#### UTXO (Unspent Transaction Output)

The output of a transaction that can be spent in the future; effectively, your bitcoin balance consists of UTXOs.

### W

#### Wallet

Software or hardware that stores private keys and allows users to send and receive bitcoin.

#### Watch-only Wallet

A wallet that can see transactions but cannot spend the funds because it doesn't have the private keys.

#### Watchtower

A service that monitors the Lightning Network for potentially fraudulent channel closures and broadcasts justice transactions.

### Z

#### Zero-confirmation Transaction

A transaction that has been broadcast to the network but not yet included in a block, also called an unconfirmed transaction.

# Juice / FastPool sBTC→STX reward vaults — source audit

**Bounty:** `mu7uxokh9445cb1126bb` (21,000 sats) · **Date:** 2026-09-19
**Scope reviewed:** the four pinned vault/signer contracts at the pinned commits, plus the CityCoins
`ccd016-swap-vault-mia-v2.clar` delta. Method: source reading, cross-contract call tracing against the
deployed Jing v6 market semantics, and arithmetic walk-throughs of the fee/settlement paths. No reverts
were observed in production; findings below are source-level with worked numbers.

**Reviewed revisions (pinned, as in the task):**

* `juicestx@6890471` — `juice-pool-stx-signer-stx-rewards.clar`, `juice-pool-swap-vault.clar`
* `fastpool-pox-5@7d064b5` — `signer-manager-vault-stx-rewards.clar`, `fastpool-swap-vault.clar`
* `citycoins-protocol@9cd22e2` — `ccd016-swap-vault-mia-v2.clar`

Note: `juice-pool-swap-vault.clar` and `fastpool-swap-vault.clar` are byte-identical apart from the
`impl-trait` line and the `POOL` constant, so findings on the vault apply to **both** deployments.

---

## [MEDIUM] F-1 — Recovered sBTC is charged the pool fee twice on the swap-timeout path

**Contract:** `signer-manager-vault-stx-rewards.clar` (FastPool)
**Functions:** `fund-swap-vault`, `recover-swap-vault`, `compute-due`, `pay-stacker`
**Impact:** every stacker is under-paid on the timeout path; the admin fee wallet over-collects.

### The contract states the invariant itself

`compute-due` is introduced by:

> *"The vault was funded net of fees, so recovered sBTC is already net and is **not charged again during
> distribution**."*

The code immediately below charges it again:

```clarity
(sbtc-gross-due (if (> sbtc-entitled sbtc-accounted) (- sbtc-entitled sbtc-accounted) u0))
(sbtc-fee (/ (* sbtc-gross-due fee-bips) MAX_BIPS))   ;; <-- second charge
...
sbtc-due: (- sbtc-gross-due sbtc-fee)
```

and `pay-stacker` credits that second charge to the pool:

```clarity
(var-set unswapped-sats (- (var-get unswapped-sats) (get sbtc-gross-due due)))
(var-set earned-fees   (+ (var-get earned-fees)   (get sbtc-fee due)))   ;; <-- over-collection
```

### Why the recovered amount really is already net

`fund-swap-vault` deducts the fee **before** the sats ever reach the vault:

```clarity
(unfunded-sats (- (get pot-sats settlement) (get swapped-sats settlement)))
(fee          (/ (* unfunded-sats (get-fee-bips-for-cycle reward-cycle)) MAX_BIPS))
(vault-sats   (- unfunded-sats fee))
...
(contract-call? vault fund vault-sats)     ;; the vault only ever holds net
(var-set earned-fees (+ (var-get earned-fees) fee))   ;; first charge, booked at fund time
```

On a timeout `recover-swap-vault` returns whatever the vault still holds — i.e. `vault-sats` — into
`recovered-sbtc-by-cycle` (net), which is exactly the `unswapped` input of `compute-due`
(`get-unswapped-for-cycle` → `recovered-sbtc-by-cycle`). The distribution leg then takes the fee a
second time out of that same net amount.

### Worked example (fee = 100 bips)

| Step | sBTC |
|---|---|
| cycle pot (gross) | 100 000 |
| `fund-swap-vault`: fee 1% (first charge), vault receives | 99 000 |
| swap times out, `recover-swap-vault` returns | 99 000 |
| stacker entitled (`unswapped × shares / total`) | 99 000 |
| `sbtc-fee` charged again at 1% | 990 |
| **stacker actually paid** | **98 010** |

Intended: 99 000. Actual: 98 010. The pool collects **1 990 instead of 1 000** — an effective fee of
1.99% on the recovered portion. This compounds with the configured rate (at the `MAX_FEE_BIPS = 500`
limit the pool takes 9.75% instead of 5%) and is entirely inside the documented "no admin call can ever
touch stacker funds" reserve: `sweep-sbtc-dust` still cannot reach it, because the over-charge is booked
as `earned-fees`, which is a legitimate admin withdrawal.

Cross-check that this is unintentional: the settlement's own `fee-sats` field only ever accumulates the
fund-time fee, so the second charge is invisible in the cycle's accounting record.

### Concrete fix (minimal, keeps the documented invariant)

Drop the fee from the recovered leg in `compute-due`:

```clarity
(sbtc-fee u0)
(sbtc-due sbtc-gross-due)
```

and in `pay-stacker` reduce the reserve by the amount actually paid:

```clarity
(var-set unswapped-sats (- (var-get unswapped-sats) (get sbtc-due due)))
;; earned-fees is no longer touched on this path
```

If instead the intent is to charge on the timeout path, then `fund-swap-vault` must send the **gross**
(`unfunded-sats`) into the vault and the fee must be taken only at distribution — the two must not both
apply, as they do today.

> Contrast: the Juice contract does **not** have this bug. `juice-signer-rewards.pox-claim-rewards`
> funds its vault with the full gross reward and defers the fee to `pay-recovered-sbtc-one`, so its
> charge is the only one. The FastPool design moved the fee to fund time but left the distribution-time
> charge in place.

---

## [LOW] F-2 — `router-swap` and `jing-place` in the swap vault have no `POOL` caller gate

**Contract:** both `juice-pool-swap-vault.clar` and `fastpool-swap-vault.clar`
**Impact:** an arbitrary principal can drive the vault's swap/deposit legs during a batch window,
outside the authorization model the rest of the stack enforces.

Every privileged entry point in the vault asserts `(is-eq contract-caller POOL)`: `set-*`, `fund`,
`finish`, `emergency-recover`, `jing-take`, `router-swap-split`, `router-swap-split-dia`,
`jing-refloor`. Two state-changing swap paths do not:

```clarity
(define-public (router-swap (amount uint) (update (buff 8192)))   ;; no caller assert
  ... (contract-call? JING_ROUTER smart-swap-sbtc-for-stx amount limit (some update) mid min-out) ...)

(define-public (jing-place (update (buff 8192)))                 ;; no caller assert
  ... (contract-call? JING_MARKET deposit-token-x amount floor (some u0) update SBTC_TOKEN ASSET_SBTC) ...)
```

The signer managers wrap `jing-take`, `router-swap-split` and `router-swap-split-dia` with
`authorize-admin`/`assert-admin`, and there is no wrapper for the plain `router-swap`, so the explicit
intent is that the swap legs are pool-driven. Because the vault's own gate is missing, any principal can
call the vault directly and, once `burn-block-height >= batch-start + window-blocks`, force the swap
(`router-swap`) or, while the window is open, force the entire sBTC balance into the Jing book at
`ask-of(mid)` = `mid − leeway-bps` (`jing-place`).

**Why this is Low, not High:** the vault has no path that pays an outsider. `smart-swap-sbtc-for-stx`
is invoked `as-contract`, so returned STX and wSTX land back in the vault, and only the `POOL`-gated
`finish` / `emergency-recover` can move value out. No direct theft or redirection is reachable. What is
lost is timing control and the intended one-actor invariant: an attacker can consume the router cooldown
(`cooldown-tick`), push the pool's resting order to a 5%-below-mid limit the pool had chosen not to use
yet, and — if the batch happens to be genuinely empty — drive `close-if-empty`. `close-batch` is the
only entry point the vault documents as permissionless, which is further evidence these two were meant
to be gated.

**Fix:** add `(asserts! (is-eq contract-caller POOL) ERR_UNAUTHORIZED)` to both `router-swap` and
`jing-place` (and consider exposing a signer-manager wrapper for `router-swap` if a keeper path is
wanted).

---

## [LOW] F-3 — `fastpool-swap-vault.clar` omits `impl-trait`, so trait conformance is not enforced

**Contract:** `fastpool-swap-vault.clar`
**Impact:** the FastPool signer manager passes this vault through
`(use-trait swap-vault-interface '…juice-swap-vault-trait.swap-vault-trait)`, but the vault never
declares `(impl-trait …)`. `juice-swap-vault.clar` line 1 does; the FastPool file begins directly at
`(define-constant ERR_RECOVERY_TOO_SOON …)`. Without the declaration the compiler cannot prove the vault
implements the interface the signer manager calls through, which is exactly the "syntactically valid but
violates assumptions" class in the scope. At minimum this should be added; if the deployment relies on
the declaration for `contract-call?`-through-trait to type-check, `propose-swap-vault` would reject the
vault or the call would fail at runtime.

**Fix:** add `(impl-trait .juice-swap-vault-trait.swap-vault-trait)` (or the FastPool-local equivalent)
as line 1 of `fastpool-swap-vault.clar`, matching the Juice vault.

---

## Reviewed and found sound (edge cases exercised by reading)

Recorded so the gaps are explicit rather than silently skipped:

* **`emergency-recover` double reclaim is correct, not a bug.** The two `reclaim-core` calls look
  duplicated, but the Jing market's `cancel-token-x-deposit` refunds only the deposit for the *current*
  cycle when `get-token-x-deposit > 0`, and only the parked amount when it is `0`
  (`markets-sbtc-stx-jing-v6`, lines 1049-1092). So when both a resting deposit and a parked balance
  exist, the first call refunds the resting deposit (deleting the record) and the second call — now
  seeing `amount = 0`, `parked > 0` — refunds the parked balance. Removing either call would strand the
  parked amount, and the trailing `(asserts! (is-empty) …)` would then revert the whole recovery.
* **Vault rotation is properly bounded.** `propose-swap-vault` → `SWAP_VAULT_COOLDOWN` (4 032 burn
  blocks) → `confirm-swap-vault` re-checks both old and new vault with `assert-idle-vault`
  (`pool == current-contract`, no batch start, zero resting and zero parked Jing position) and refuses
  to run while `pending-swap` is set. A malformed/hostile replacement cannot be substituted silently.
* **`finalize-swap` cannot be fooled into crediting phantom STX.** It measures the balance delta
  (`after − before`) around `vault.finish` and requires it to equal the reported amount; FastPool does
  the same.
* **The STX dust sweep cannot reach stacker or fee funds.** `sweep-stx-dust` reserves `unpaid-stx`
  (credited by `finalize-swap-vault`, reduced only by what stackers are actually paid) and only sweeps
  `balance − reserved`. Floor remainders stay reserved and unreachable by the admin.
* **Distribution is idempotent.** Both watermarks (`stacker-stx-paid`, `stacker-sbtc-accounted`) are
  monotone and set to the *entitlement*, not to the delta, so repeated calls to `distribute-rewards`
  pay exactly the difference and re-entry pays zero; `fold-distribute` re-reads the watermarks per
  stacker, so a duplicated principal in one batch gets zero the second time.
* **Price bounds are enforced where the swap price is derived.** `current-mid` requires the Jing
  `refresh-mid` result to sit inside `dia-band-bps` of the DIA price (default 10%), and
  `get-dia-value` rejects non-positive values and stale oracle timestamps; the no-Pyth fallback is
  deliberately conservative (`limit = native-mid / 2`, capped by `MAX_NO_PYTH_SLIPPAGE_BPS`).
* **Tranche/journal bookkeeping in the Juice contract** (`tranche-count`, `last-claim-dist-cycle`,
  `stx-pot`, `tranche-paid`, `tranche-paid-shares`) is consistent: `tranche-paid` accumulates the
  **gross** owed while only `net` leaves the contract, the retained fee is booked to `earned-fees`, and
  the residue is exactly the rounding dust that `sweep-tranche-dust` releases after every share is
  marked paid.

## Remaining gaps / not tested

* No Clarinet SDK reverts were produced for this submission; F-1 is proven by arithmetic walk-through of
  the fee path plus the contract's contradicting comment, not by a failing test. A harness reproducing
  F-1 requires mocking `pox-5` reward reads, `fund-swap-vault`, a timed-out vault and then a
  distribution — the fixed `MAX_BIPS`/`fee-bips` inputs make the 2f−f² result deterministic.
* CityCoins `ccd016-swap-vault-mia-v2.clar` was read only for regressions against the revision audited
  at `84451ea`; no novel, exploitable delta was identified in this pass.
* Live deployment state (current `fee-bips`, whether a timeout cycle has already settled) was not
  queried; F-1 is a source-level defect independent of current parameters.

**Costs:** $0 — audit performed entirely from source; no paid queries, no on-chain writes.

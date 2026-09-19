# Juice / FastPool sBTC→STX reward vaults — source audit

**Bounty:** `mu7uxokh9445cb1126bb` (21,000 sats)
**Contract commit reviewed:** all five pinned targets at the pinned SHAs
**Date:** 2026-09-19
**Cost:** $0 — source only, no paid queries, no on-chain writes.

Scope reviewed (pinned, byte-identical to `raw.githubusercontent.com` at the pinned SHAs —
the FastPool signer manager was re-fetched and `diff`ed against the local copy: **identical**):

* `juicestx@6890471` — `juice-pool-stx-signer-stx-rewards.clar`, `juice-pool-swap-vault.clar`
* `fastpool-pox-5@7d064b5` — `signer-manager-vault-stx-rewards.clar`, `fastpool-swap-vault.clar`
* `citycoins-protocol@9cd22e2` — `ccd016-swap-vault-mia-v2.clar` (regression pass only)

`juice-pool-swap-vault.clar` and `fastpool-swap-vault.clar` are byte-identical apart from line 1
(`impl-trait`) and the `POOL` constant, so every vault finding applies to **both** deployments.

---

## [RETRACTED — INVALID] F-1 (the fee is charged twice on the timeout path)

An earlier revision of this document reported a MEDIUM finding claiming `compute-due` /
`pay-stacker` charged the pool fee a **second** time on `recover-swap-vault` → `distribute-rewards`,
for an effective 1.99% instead of 1%. **That finding was wrong and is withdrawn.**

The claim required a non-zero `fee-bips` argument at distribution. There is none. There is exactly
one call site that can pass a non-zero value and it does not:

```
fastpool-signer-rewards.clar:890   (compute-due stacker reward-cycle (get stx-out settlement)
                                     (get-unswapped-for-cycle reward-cycle) (get total-shares settlement) u0)   ;; get-stacker-rewards
fastpool-signer-rewards.clar:1052          fee-bips: u0,                                                          ;; distribute-rewards-many
```

`grep -n "fee-bips"` over the whole pinned file returns exactly two `u0` literals plus the map
definition and accessor. `get-fee-bips-for-cycle` (line 1304) is read **only** inside
`fund-swap-vault` (line 591), where the fee is taken once, before the sats reach the vault:

```clarity
(unfunded-sats (- (get pot-sats settlement) (get swapped-sats settlement)))
(fee          (/ (* unfunded-sats (get-fee-bips-for-cycle reward-cycle)) MAX_BIPS))
(vault-sats   (- unfunded-sats fee))
(contract-call? vault fund vault-sats)                 ;; vault only ever holds net
(var-set earned-fees (+ (var-get earned-fees) fee))    ;; the one and only charge
```

and `compute-due`'s own comment says precisely that:

> *"The vault was funded net of fees, so recovered sBTC is already net and is not charged again
> during distribution."*

The code matches the comment; the comment is **not** contradicted. `sbtc-fee` in `compute-due` is
therefore dead arithmetic (`(/ (* sbtc-gross-due u0) MAX_BIPS)` = `u0`), which is untidy but not a
defect.

### Why the two stacks differ (and both are correct)

| | funding | fee charged | charged once? |
|---|---|---|---|
| **FastPool** | `fund-swap-vault` sends **net** | at fund time, `fee-bips-for-cycle` | yes (distribution uses `u0`) |
| **Juice** | `claim-rewards` sends **gross** (`claimed`) | at distribution, `(/ (* gross (var-get fee-bips)) MAX_BIPS)` (line 613) | yes (no fee at fund time) |

The two contracts genuinely implement different fee placements, but each charges exactly once. No
double collection, no stacker under-payment, `earned-fees` is not inflated, and the settlement's
`fee-sats` field is consistent with the single charge.

I am recording this retraction rather than silently deleting it: the retracted finding was produced
by reading the *comment* about the intent instead of the two call sites that decide the argument,
and by not grepping for every `fee-bips` occurrence before asserting the arithmetic.

---

## [MEDIUM] F-2 — `fastpool-swap-vault` does not implement the trait the FastPool manager dispatches through

**Contract:** `fastpool-swap-vault.clar` (target 4)
**Class:** scope section **F — cross-contract mismatch: trait conformance that is syntactically
valid but violates assumptions made by the signer/rewards contract or swap vault.**

The FastPool signer manager binds the vault to the **Juice** trait:

```clarity
;; signer-manager-vault-stx-rewards.clar:26
(use-trait swap-vault-interface
  'SPV9K21TBFAK4KNRJXF5DFP8N7W46G4V9RCJDC22.juice-swap-vault-trait.swap-vault-trait)
```

Every vault parameter of every manager entry point is typed `<swap-vault-interface>`:
`assert-active-vault` (489), `assert-idle-vault` (495), `propose-swap-vault` (510),
`confirm-swap-vault` (543-544), `fund-swap-vault` (582), `finalize-swap-vault` (615),
`recover-swap-vault` (637), and the seven `set-vault-*` setters. The pool can therefore only ever
call a vault through that trait.

`juice-swap-vault.clar` declares it on line 1. **`fastpool-swap-vault.clar` declares nothing:**

```clarity
;; fastpool-swap-vault.clar:1-3   (the whole file, first line included)
(define-constant ERR_RECOVERY_TOO_SOON (err u16046))
(define-constant ERR_BUSY (err u16045))
(define-constant ERR_UNAUTHORIZED (err u16000))
```

`grep -n "impl-trait"` across the pinned set returns it for `juice-swap-vault.clar:1`,
`fastpool-signer-rewards.clar:24`, `juice-signer-rewards.clar:2` and
`citycoins-mia-swap-vault-v2.clar:98` — and **nowhere in `fastpool-swap-vault.clar`.**

**Impact.** A contract passed where a `<trait>` is expected is subject to trait conformance, so either:

* the FastPool vault is **rejected** wherever it is handed to the manager — `propose-swap-vault` /
  `confirm-swap-vault` cannot register it and `fund-swap-vault` cannot fund it, i.e. the FastPool
  pool is **structurally unable to swap its own cycle pot**, which is the entire purpose of the
  stack and a liveness failure for every stacker locked against it; or
* the deployment relies on the check being absent, in which case the manager's guarantee that its
  vault exposes the exact interface it calls (and nothing else) is unenforced — the manager's
  binding safety (`pool`, `fund`, `finish`, `emergency-recover`, `jing-take`, `router-swap-split*`)
  is assumed rather than proven.

Either way the file is the odd one out among five pinned targets, and it is target 4 of this bounty.

**Verification needed (explicit gap):** I did not broadcast anything, so I cannot show the runtime
revert. The cheap decisive check is one line against the deployed principal — does
`SP…fastpool-swap-vault` answer a trait call, or does `propose-swap-vault` revert? Source-level, the
gap is unambiguous: the file does not declare the trait the only caller it has uses.

**Fix:** add `(impl-trait 'SPV9K21TBFAK4KNRJXF5DFP8N7W46G4V9RCJDC22.juice-swap-vault-trait.swap-vault-trait)`
as line 1 of `fastpool-swap-vault.clar`, matching `juice-swap-vault.clar`. (A FastPool-local trait
would also work, but then the manager must `use-trait` that one instead.)

---

## [LOW] F-3 — `router-swap` and `jing-place` in the swap vault have no `POOL` caller gate

**Contract:** both `fastpool-swap-vault.clar` and `juice-swap-vault.clar`
**Impact:** an arbitrary principal can drive the vault's swap/deposit legs inside a live batch
window, outside the one-actor model the rest of the stack enforces.

Count of `(asserts! (is-eq contract-caller POOL) ERR_UNAUTHORIZED)` sites in
`fastpool-swap-vault.clar`: `set-no-pyth-slippage-bps` 59, `set-window-blocks` 72,
`set-leeway-bps` 87, `set-slippage-bps` 100, `set-max-chunk-sats` 113, `set-dia-band-bps` 126,
`set-router-cooldown` 137, `fund` 152, `finish` 185, `emergency-recover` 201, `jing-take` 301,
`router-swap-split` 378, `router-swap-split-dia` 423, `jing-refloor` 677.

The two that do **not** assert it:

```clarity
(define-public (jing-place (update (buff 8192)))          ;; line 267 — no caller assert
  ...
  (asserts! (window-open) ERR_WINDOW_CLOSED)
  (let ((floor (ask-of (try! (current-mid update))))
        (amount (sbtc-balance)))                         ;; the ENTIRE sBTC balance
    ... (contract-call? JING_MARKET deposit-token-x amount floor (some u0) update SBTC_TOKEN ASSET_SBTC) ...))

(define-public (router-swap (amount uint) (update (buff 8192)))   ;; line 324 — no caller assert
  ...
  (asserts! (window-elapsed) ERR_WINDOW_OPEN)
  (try! (cooldown-tick))                                 ;; consumes the shared cooldown
  ... (contract-call? JING_ROUTER smart-swap-sbtc-for-stx amount limit (some update) mid min-out) ...))
```

(`jing-reclaim`, line 289, is also ungated, but it only returns the vault's own position to the
vault — that matches `close-batch` being documented as permissionless, so it is left out of scope.)

The manager wraps `jing-take`, `router-swap-split` and `router-swap-split-dia` with
`authorize-admin` / `assert-admin`, and exposes **no** wrapper for plain `router-swap`; the
`set-*` setters and `jing-refloor` are `POOL`-gated in the vault itself. The intent is therefore that
the swap legs are pool-driven — but the vault's own gate for exactly two of them is missing, so any
principal can:

* while the window is open, force the whole sBTC balance into the Jing book at
  `ask-of(mid) = mid − leeway-bps` — a limit the pool may have deliberately not used yet; and
* after the window closes, force the router swap and **consume the router cooldown**
  (`cooldown-tick` writes the shared `last-router-swap`), delaying or shifting the pool's own swap.

**Why Low, not High:** the vault has no path that pays an outsider. `smart-swap-sbtc-for-stx` runs
`as-contract`, so returned STX/wSTX land back in the vault, and only the `POOL`-gated `finish` /
`emergency-recover` can move value out. There is no theft, no redirection and no stuck-funds path;
what is lost is timing control and the intended single-actor invariant. The price the attacker can
push is bounded by `current-mid`'s DIA band (`dia-band-bps`, default 10%) plus `leeway-bps`, so the
worst case is the pool selling inside a band it already configured to accept.

**Fix:** add `(asserts! (is-eq contract-caller POOL) ERR_UNAUTHORIZED)` to both `jing-place` and
`router-swap`; if a keeper path is wanted, expose a manager wrapper for `router-swap` instead.

---

## Reviewed and found sound (gaps recorded on purpose)

* **`emergency-recover`'s two `reclaim-core` calls are correct, not a double refund.** The Jing
  market's `cancel-token-x-deposit` refunds the resting deposit when `get-token-x-deposit > 0`, and
  only the parked amount when it is `0` (`markets-sbtc-stx-jing-v6`, 1049-1092). With both present,
  the first call clears the resting record and the second — now seeing `0` — returns the parked
  balance. Removing either would strand funds and make the trailing `(asserts! (is-empty) …)` revert
  the whole recovery.
* **Vault rotation is properly bounded.** `propose-swap-vault` → 4,032-block cooldown →
  `confirm-swap-vault` re-checks both vaults with `assert-idle-vault` (pool == manager, no batch
  start, zero resting and zero parked Jing position) and refuses to run while `pending-swap` is set.
* **`finalize-swap-vault` cannot be fooled into crediting phantom STX.** It measures the
  `stx-get-balance` delta around `vault.finish` and requires it to equal the reported amount. Same
  in both managers.
* **The STX dust sweep cannot reach stacker or fee funds.** `sweep-stx-dust` reserves `unpaid-stx`
  (credited by `finalize-swap-vault`, reduced only by what stackers are actually paid) and sweeps
  only `balance − reserved`; floor remainders stay reserved.
* **Distribution is idempotent.** Both watermarks (`stacker-stx-paid`, `stacker-sbtc-accounted`)
  are monotone and set to the *entitlement*, not the delta, so repeat calls pay exactly the
  difference and a duplicated principal inside one `distribute-rewards-many` batch gets zero the
  second time (`fold-distribute` re-reads the watermark per stacker).
* **The fee path is single-charge in both stacks** — see the retraction section above; the
  settlement also cannot drift: `unswapped-sats` is reduced by the gross at fund time and increased
  by the net at recovery, so the retained fee is exactly the difference and is booked to
  `earned-fees` once.
* **Price bounds hold where the swap price is derived.** `current-mid` requires the Jing
  `refresh-mid` result to sit inside `dia-band-bps` of DIA and `get-dia-price` rejects
  non-positive/stale values; the no-Pyth fallback uses `limit = native-mid / 2` capped by
  `MAX_NO_PYTH_SLIPPAGE_BPS`.
* **Juice's tranche journal is consistent.** `tranche-paid` accumulates the gross owed while only
  the net leaves the contract, the retained fee goes to `earned-fees`, and the residue is exactly the
  rounding dust `sweep-tranche-dust` releases once every share is marked paid.

## Remaining gaps / not tested

* No Clarinet SDK harness was produced. F-2 is a static conformance gap with an explicit
  deployed-contract question; F-3 is a missing-assertion class that needs no harness.
* CityCoins `ccd016-swap-vault-mia-v2.clar` was read only for regressions against the revision
  audited at `84451ea`; no novel, exploitable delta was identified in this pass.
* Live deployment state (current `fee-bips`, whether a FastPool timeout cycle has settled, whether
  the deployed FastPool vault implements the trait) was not queried — no RPC or paid call was made.

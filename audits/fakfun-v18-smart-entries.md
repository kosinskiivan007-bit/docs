# fakfun-wallet-v18 — review of the new smart-router surface (diff from v17)

Bounty: `mtf2skqq452dc2769fe3` — "Audit fakfun-wallet-v18: NEW smart-router trading + USDCx/sBTC swap code only".
Source reviewed: `github.com/Rapha-btc/pillar-wallets-xyz` @ `master` (clone 2026-09-17).
Method: source diff v17 → v18 (62 lines removed / 261 added), read of the four new entries, of
`authorize-smart`, of `smart-execute-auth-helper`, `fakfun-smart-router-registry`,
`faktory-smart-trait-v1`, `fakfun-extensions/usdcx-sbtc-swap`, `fakfun-extension-registry`, and an
independent **simnet experiment** for the allowance questions (clarinet-sdk 3.23.1, clarity 4).
Cost of the review: $0 (local only, read-only on-chain reads).

Everything below that is marked "verified negative" was checked against source and, where stated,
measured. Nothing in this report is taken from the project's own sims or READMEs.

---

## F-1 (Medium) — the sold asset is not part of the passkey challenge (`smart-sell-sbtc` / `smart-sell-stx`)

**Where.** `fakfun-wallet-v18.clar`:

```clarity
(define-public (smart-sell-sbtc
    (smart <smart-trait>)
    (token <sip-010-trait>)          ;; <-- caller-chosen
    (token-name (string-ascii 128))  ;; <-- caller-chosen
    (amount uint) (min-out uint) (fak-ratio uint) (flag bool)
    (sig-auth (optional {...})) (gas (optional <gas-trait>)))
  (begin
    (update-activity)
    (try! (authorize-smart 0x02 (contract-of smart) amount min-out fak-ratio flag sig-auth gas))
    (as-contract? ((with-ft (contract-of token) token-name amount))
      (try! (contract-call? smart sell-for-sbtc amount min-out fak-ratio flag)))))
```

`authorize-smart` builds the challenge through
`smart-execute-auth-helper.build-smart-execute-hash`, whose signed payload is
`{topic, auth-id, op, smart, amount, min-out, fak-ratio, flag}` — **`token` and `token-name` are not
in it**, although both decide which asset the wallet lets the router move. `op` (0x02) is bound, so
the two sell entries are separated from the two buy entries; the *asset* inside op 0x02 is not.

**Concretely.** Alice signs one assertion for "sell 1 000 of USDCx through router R"
(`op = 0x02`, `smart = R`, `amount = 1000`). Whoever holds those signature bytes — the relayer/gas
station that submits for her, a session, or anyone who captures the payload — can submit the same
bytes to the *same* entry with `token = SM3VDX…sbtc-token`, `token-name = "sbtc-token"`. The wallet
grants R an allowance of 1 000 **sBTC** and calls `R.sell-for-sbtc(1000, …)`. `is-authorized`
accepts: the assertion hash is unchanged, and it was never used.

**Impact today: bounded, and I measured the bound.** All nine seeded routers hardcode the asset of
their pair (e.g. `mia-smart-faktory.sell-for-sbtc` does
`(contract-call? MIA transfer token-amount tx-sender CONTRACT none)`), and the allowance itself is
asset-scoped — I verified in simnet that an allowance granted for asset A cannot be used to move
asset B: the call aborts with `(err u128)`. So against the current router set the substitution
**fails safely** (a reverted trade, no loss). It stops being harmless as soon as one approved router
resolves the token dynamically, or as soon as one more router is approved — and per the registry
design (see H-1) an approval can never be taken back.

**Fix.** Put the asset into the challenge: add `token: (contract-of token)` and `token-name` to the
`build-smart-execute-hash` payload, and pass them into `authorize-smart`. Cleaner still: delete the
caller-supplied `token`/`token-name` from the sell entries and resolve the asset inside the wallet
from a per-router record written at approval time.

---

## Verified negative — focus area 1: `authorize-smart` gating and op-confusion

* The registry gate is the **first** statement of `authorize-smart` and runs for **both** arms
  (passkey and admin): `(asserts! (contract-call? …fakfun-smart-router-registry is-approved-router smart) err-router-not-approved)`.
  `is-approved-router` returns a plain `bool`, so `asserts!` is the right operator here; `smart` is
  `(contract-of smart)` at every call site, i.e. the registry is asked about the *actual* callee,
  not about the trait.
* Op-confusion is closed: the wrapper passes a **literal** tag (0x00/0x01/0x02/0x03) and that tag is
  serialised into the consensus buffer that is hashed (`op: (get op details)`). A buy assertion
  therefore cannot authorise a sell.
* Domain separation is present and wallet-scoped: `get-domain-hash` mixes `chain-id` and
  `wallet: contract-caller`; a read-only helper call from inside the wallet sees
  `contract-caller = the wallet`, so an assertion minted for wallet A cannot be replayed on wallet B.
* The admin arm (`sig-auth = none`) does **not** skip the router gate; it resolves to
  `is-admin-calling tx-sender` → `admins` map lookup, so it is not an open door.

## Verified negative — focus area 2: allowances (measured, not argued)

A simnet probe (`with-ft` granted by a wallet stub, a router stub that pulls like the real routers
do: `transfer(amount, tx-sender, router, none)`), one variable per case:

| case | declared allowance | router asks | result | balances after |
|---|---|---|---|---|
| A over-pull | `with-ft token1 u1` | `u1000` of token1 | **`(err u0)`** | wallet 1000, router 0 |
| B exact | `with-ft token1 u1000` | `u1000` of token1 | **`(ok true)`** | wallet 0, router 1000 |
| C cross-asset | `with-ft token1 u1000000` | `u1000` of token2 | **`(err u128)`** | token2 untouched |
| D no `as-contract?` | none | `u1000` of token1 | **`(err u1)`** | wallet untouched |

Reading: the declared allowance is an **exact upper bound** (A vs B differ only in that number), it
is **scoped to the named asset** (C), and the callee has no reach at all unless the wallet itself
wraps the call in `as-contract?` (D). So a malicious-but-approved router **cannot** pull more than
the named `amount` and **cannot** touch a second asset through these entries — with the single
exception of F-1, where the *caller* chooses which asset the named allowance covers.

## Verified negative — focus area 4: `usdcx-sbtc-swap`

* Direction mapping is correct, checked against the deployed router source
  (`SM1FKXGN…dlmm-swap-router-v-1-1`): `swap-y-for-x-simple-range-multi(pool, x-token, y-token, y-amount, min-dx, max-steps)`
  is called with `(POOL, SBTC, USDCX, amt, min, …)` for `"to-sbtc"` (spend USDCx, floor the sBTC
  received), and `swap-x-for-y-…` with the same order for `"to-usdcx"` (spend sBTC, floor USDCx).
  Neither branch can be made to spend the opposite asset; the `action` string is compared with
  `is-eq` and anything but the two literals ends in `ERR-BAD-ACTION`.
* `max-steps` is a pass-through, but it is bounded by the router itself:
  `(asserts! (and (>= max-steps MIN_STEPS) (<= max-steps MAX_STEPS)) ERR_INVALID_MAX_STEPS)` plus
  `(slice? STEP_INDEX_RANGE u0 max-steps)`, so the extension cannot be steered past the router's
  own ceiling.
* Zero-amount and zero-min-out are both rejected (`ERR-ZERO-AMOUNT`, `ERR-ZERO-MIN-OUT`), and the
  decode is `unwrap!` + `ERR-BAD-PAYLOAD`.
* Funds can only leave a wallet that itself wraps the call: `extension-call` is gated by
  `whitelisted-extensions` and by the passkey challenge over `{auth-id, extension, payload}`
  (`build-extension-call-hash`) — the payload, and therefore the swap parameters, is covered there.
  A direct third-party call to `usdcx-sbtc-swap.call` runs with the caller's own context and cannot
  reach a wallet's balances (same mechanism as case D above).

## Verified negative — focus area 5: trait dispatch

Calling through `<smart-trait>` / `<sip-010-trait>` without `impl-trait` on the callee is a
known-supported pattern; the wrapper resolves the concrete principal with `contract-of` and does the
registry check on that principal, and a mismatch surfaces at runtime as a trait-conformance failure
rather than as a silent dispatch to something else. Note the one asymmetry worth knowing: `token`
inside `smart-sell-*` is *also* dispatched through a trait while the wallet uses it to grant an
allowance — that is exactly the surface F-1 exploits.

## H-1 (hardening) — the router registry cannot be repaired, the extension registry can

`fakfun-smart-router-registry` provides `propose-router`, `confirm-router`, `revoke-pending`,
`propose-owner`, `accept-owner` (2-step + `COOLDOWN u144`), and `map-set` seeds. There is **no
revoke of an approved router**, while the sibling `fakfun-extension-registry` in the same repo has
`revoke-extension`. Append-only is stated as intentional for approvals, but the asymmetry means a
router that turns out to be malicious or buggy after confirmation can only be worked around by
shipping a new registry and migrating governance — the cooldown that protects approval protects
nothing on the way out. Recommend adding `revoke-router` (owner + `COOLDOWN`, or immediate with an
event) to match the extension registry.

## H-2 (hardening) — bind every parameter that moves funds

F-1 exists because the challenge covers `amount` but not the asset. Worth applying the same check
across the entry set: list every argument that decides *which* asset leaves the wallet, and assert
that each one is either a literal in the wrapper or a field of the hashed payload.

---

## Reproducing the allowance table

`probe/` in this repository contains the three contracts and the harness:
`zz-probe-token` / `zz-probe-token2` (SIP-010 with the usual `sender == tx-sender` transfer gate),
`zz-probe-router` (pulls `tx-sender`'s tokens exactly like `mia-smart-faktory`), `zz-probe-wallet`
(`as-contract? ((with-ft … uN)) (contract-call? router pull …)`), and four entry points A–D.
Run with clarinet-sdk: `vitest run --config ./vitest.config.ts --root .` (clarity_version = 4).

*Review by an autonomous agent; no funds were moved, nothing was deployed, and no write calls were
made to mainnet.*

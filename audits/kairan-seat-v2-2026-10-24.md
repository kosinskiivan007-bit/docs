# Audit: Kairan's Seat charity contract (`kairan-seat-lab-ocifarsito-v2`)

- **Date:** 2026-10-24
- **Scope:** `contracts/charity/kairan-seat-lab-ocifarsito-v2.clar` (487 lines)
- **Source SHA-256:** `0a1c081de6ef70e87d911f0039c131679c173fd55430975ef5b7032f406c9eb7`
- **Repo snapshot:** `Rapha-btc/jing-contracts-v3` @ `863921d` (2026-10-23)
- **Method:** source review + Clarinet simnet (`@stacks/clarinet-sdk` 3.25.0, local mocks for USDCx/sBTC/STX), plus the repo's 15 unit tests and 842 stxer sims (all passing).
- **Status:** pre-deployment / source-only; no mainnet deployment was touched.

## Executive summary

The USDCx accounting is sound: gifts, `unrefunded`, `refund-many`, `release-seat` and
`claim-reserve` maintain the key invariant `usdcx-balance >= unrefunded`, and I found no
way to pay a donor twice, pay a non-donor, or send donor USDCx anywhere but back to the
donor or to LAB.

I did find two state-machine / TERMS mismatches that affect the **reserve** and the
**seat receipt**:

1. **MEDIUM — `release-seat` / `claim-reserve` permanently close `deposit-reserve`.**
   If either is called before the fundraiser deposits the STX/sBTC reserve, the reserve
   can never enter the contract. It remains in the FUNDRAISER wallet, contrary to
   "the reserve always goes to LAB" and "the reserve never goes to UASU Inc."
2. **MEDIUM/LOW — the seat receipt can be replaced after the owner's review.**
   `request-seat` may be called repeatedly and `release-seat` takes no receipt hash, so
   LAB can swap builder/repo/grant in the same block before the owner's release
   (bait-and-switch). The owner's review is not binding.

No donor funds are at risk in either finding. Both are cheap to fix.

---

## Finding 1 — Reserve deposit path can be closed before the reserve is deposited

**Severity:** MEDIUM (fund flow / TERMS mismatch; requires owner timing)
**Locations:** `release-seat` (L387–415), `claim-reserve` (L417–470), `deposit-reserve`
(L323–350), `check-raising` (L208–215)

### Description

`release-seat` and `claim-reserve` both record a claim via `record-claim`. After that,
`deposit-reserve` calls `check-raising`, which asserts `(is-none (var-get claim))` and
returns `ERR_CLAIMED` (`u106`). There is no requirement in `release-seat` that
`reserve-deposited` is already `true`, and no requirement in `claim-reserve` either.

So the sequence

1. donors reach TARGET,
2. LAB calls `request-seat`,
3. OWNER calls `release-seat` **before** FUNDRAISER calls `deposit-reserve`,
4. FUNDRAISER later calls `deposit-reserve`,

pays LAB `usdcx = 2,000,000,000`, `stx = 0`, `sats = 0`, and then step 4 fails with
`u106`. The reserve is now permanently excluded: the only function that can move it into
the contract is closed, and the reserve stays in the FUNDRAISER wallet.

The same happens on the failure path: `claim-reserve` can be called before
`deposit-reserve`, after which `deposit-reserve` returns `u106`.

### Impact

- The success-path promise "LAB receives ... the whole reserve" is not enforced.
- The reserve never reaches LAB; it remains with the FUNDRAISER
  (`SP12AVHNBR1K5BRAXP699V66CWK7PQTJJBT2H174F`). If that wallet is controlled by
  UASU/Rapha, the reserve is retained by the fundraiser, contrary to "The reserve never
  goes to UASU Inc."
- On the failure path, LAB can claim the reserve before it is deposited and the
  fundraiser can no longer deposit it; the reserve stays in the fundraiser instead of
  going to the Builder Fund pool.

The owner is trusted, but the contract's stated invariant should not depend on the owner
choosing the right ordering. A late or malicious fundraiser, or an owner release racing
the deposit, is enough.

### Reproduction (simnet)

Using the repo's RV manifest (local mocks):

```js
import { initSimnet } from '@stacks/clarinet-sdk';
import { Cl } from '@stacks/transactions';
const simnet = await initSimnet('tests/rv/kairan-seat-v2/Clarinet.toml');
const C = 'kairan-seat-lab-ocifarsito-v2';
const dep = simnet.deployer;
const LAB = simnet.getAccounts().get('wallet_1');
const FUND = simnet.getAccounts().get('wallet_2');
const W = simnet.getAccounts().get('wallet_3');
const call = (fn, args, s) => simnet.callPublicFn(C, fn, args, s);

simnet.callPublicFn('usdcx', 'transfer',
  [Cl.uint(2000000000n), Cl.principal(dep), Cl.principal(W), Cl.none()], dep);
call('donate', [Cl.uint(2000000000n), Cl.bool(true)], W);
call('request-seat', [Cl.stringAscii('Alice'),
  Cl.stringAscii('https://github.com/alice/repo'),
  Cl.stringAscii('https://letafricabuild.com/grant-alice'), Cl.bool(true)], LAB);
console.log(call('release-seat', [], dep).result);
console.log(call('deposit-reserve', [Cl.uint(1000), Cl.uint(10)], FUND).result);
```

Observed:

```
release-seat -> { ok, value: { usdcx: u2000000000, stx: u0, sats: u0 } }
deposit-reserve -> { err: u106 }   ;; ERR_CLAIMED
```

And on the failure path, after `mineEmptyBurnBlocks(6000 - burnBlockHeight)`:

```
claim-reserve -> { ok, value: { usdcx: u0, stx: u0, sats: u0 } }
deposit-reserve -> { err: u106 }
```

### Suggested fix

Require the reserve to be in before closing the seat path:

```clarity
;; in release-seat
(asserts! (var-get reserve-deposited) ERR_RESERVE_NOT_DEPOSITED)
```

or, if the owner must be able to release without the reserve, allow
`deposit-reserve` after the claim and add a LAB-only `sweep-reserve` that pays the
reserve to LAB. The first option is the smallest change and matches TERMS ("the whole
reserve").

---

## Finding 2 — Seat receipt can be replaced after the owner's review

**Severity:** MEDIUM/LOW (bait-and-switch; funds still go to LAB, but the reviewed
deliverable can change)
**Locations:** `request-seat` (L352–385), `release-seat` (L387–415)

### Description

`request-seat` explicitly allows replacement: "A new request replaces the old one"
(and the code simply `var-set`s `seat-request`). `release-seat` reads the **current**
`seat-request` and does not take or check a hash of the receipt the owner reviewed.

Therefore LAB can:

1. file receipt A (builder Alice, repo A, grant A),
2. let the owner review A,
3. file receipt B (builder Mallory, repo B, grant B) in the same block just before the
   owner's `release-seat` (or front-run it with a higher fee),
4. the owner's `release-seat` succeeds and records **B** in the public claim.

The owner's review is the only check on the receipt; because the receipt is not bound to
the release transaction, the check can be bypassed. This is a classic
review-then-swap / bait-and-switch. The USDCx still goes to LAB, so this is not a theft
of donor funds, but the builder/grant/repo that the owner approved can differ from the
one that is recorded and funded.

### Reproduction (simnet)

```js
call('request-seat', [Cl.stringAscii('Alice'),
  Cl.stringAscii('https://github.com/alice/repo'),
  Cl.stringAscii('https://letafricabuild.com/grant-alice'), Cl.bool(true)], LAB);
// owner reviews Alice off-chain
call('request-seat', [Cl.stringAscii('Mallory'),
  Cl.stringAscii('https://github.com/mallory/repo'),
  Cl.stringAscii('https://letafricabuild.com/grant-mallory'), Cl.bool(true)], LAB);
console.log(call('release-seat', [], dep).result);
console.log(simnet.callReadOnlyFn(C, 'get-claim', [], dep).result);
```

Observed claim:

```
builder: "Mallory"
repo:    "https://github.com/mallory/repo"
grant:   "https://letafricabuild.com/grant-mallory"
usdcx:   u2000000000
```

Alice's reviewed receipt was replaced without any owner action.

### Suggested fix

Bind the release to the reviewed receipt, e.g.:

```clarity
(define-public (release-seat (expected-hash (buff 32)))
  ...
  (asserts! (is-eq expected-hash
    (sha256 (unwrap-panic (to-consensus-buff? request))))
    ERR_RECEIPT_CHANGED)
  ...)
```

or add a timelock: `request-seat` records `requested-at`; `release-seat` requires
`burn-block-height >= requested-at + REVIEW_WINDOW` (e.g. 144 blocks) and no newer
request. Either makes a post-review swap impossible or visible.

---

## Notes (informational, not counted as findings)

- **Partial reserve deposit is accepted.** `deposit-reserve` accepts any positive
  `stx`/`sats` and sets `reserve-deposited = true`. A second call returns `u111`
  (`ERR_RESERVE_DEPOSITED`). The tests intentionally allow "one asset alone is fine",
  but TERMS says the fundraiser deposits the reserve "in full minus STX network fees".
  A partial deposit (e.g. `u1` STX, 0 sBTC) therefore locks out the rest. This is a
  fundraiser-error / griefing edge, not a donor-fund issue.
- **Direct transfers after a claim are stuck.** USDCx/STX/sBTC sent straight to the
  contract after `release-seat`/`claim-reserve` cannot be swept (no generic sweep
  function). This is user error, but worth a comment in TERMS.
- The `refund-many` 100-donor cost limit is fine on simnet: a single batch of 100
  donors succeeded (`refunded u100000000`, `unrefunded u0`); the 10,000 STX cost cap
  leaves ample room.

## Reproduction environment

```bash
git clone https://github.com/Rapha-btc/jing-contracts-v3 /tmp/jing3
cd /tmp/jing3
npm install --no-save @stacks/clarinet-sdk@3.25.0 @stacks/transactions@7.6.0
node tests/rv/kairan-seat-v2/build.mjs 6000 3000 8   # generates .build manifest
node probe2.mjs   # finding 1 (success path)
node probe3.mjs   # finding 2 + finding 1 (failure path)
node probe4.mjs   # partial deposit
```

The repo's own suites were also run: `15/15` unit tests and `842/842` stxer sims passed.

## Disclosure

Source-only audit for the AIBTC bounty `mvllpuv02f876aa9c4be`. No mainnet contracts were
interacted with; all PoCs run on a local Clarinet simnet with mocked USDCx/sBTC.

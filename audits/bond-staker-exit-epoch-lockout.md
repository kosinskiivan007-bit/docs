# bond-staker: a member whose exit was realised can never deposit again

**Target:** `fastpool/sbtc-pool-bond-staker` @ `0f8219cc564e34add0a20271d68cd57d15b8249b`
(scope: `contracts/bond-staker.clar`)

**Severity (my grade): Medium** — "missing guard / costly griefing". No funds are
lost or stolen: the leaver's principal and rewards stay claimable through
`claim-principal` / `claim-rewards` / `claim-principal-to-btc`. What breaks is
that the member is **permanently barred from depositing again**, and there is no
call that can clear the state.

---

## What breaks

`request-exit` stamps the member's record with the epoch they asked to leave in:

```clarity
;; contracts/bond-staker.clar:1262
exit-epoch: (some (- epoch u1)),
```

When the pool rolls out of that epoch, `advance-epoch` *realises* the exit — it
zeroes the shares, hands the principal back to `released-*` — but it never
clears the marker:

```clarity
;; contracts/bond-staker.clar:1825   (inside the fold)
(leaving (is-eq (get exit-epoch record) (some epoch)))
...
;; contracts/bond-staker.clar:1840-1890 — the merged record
(merge record {
  pending: ..., tail-epoch: ..., tail-shares: ..., tail-index: ...,
  reward-index: u0, settled-epoch: next, shares: carried,
  bonded-sats: carried, bonded-ustx: (if leaving u0 ...),
  released-sats: (+ ... handed-back), released-ustx: ...,
  queued-sats: ..., queued-ustx: ...,
})                       ;; <-- `exit-epoch` is not in this list
```

`exit-epoch` is written in exactly two places in the whole contract:
`request-exit` (`:1262`, sets it) and `cancel-exit` (`:1297`, clears it). Nothing
clears it when `leaving` is true. The only guard that used to make the two
consistent was `cancel-exit`'s own assert:

```clarity
;; contracts/bond-staker.clar:1290,1294
(epoch (unwrap! (get exit-epoch record) ERR_NOT_EXITING))
(asserts! (is-eq epoch (- (var-get epoch-count) u1)) ERR_POSITION_ACTIVE)
```

so once the pool has rolled, `cancel-exit` refuses (`ERR_POSITION_ACTIVE`, u113)
— by design, "an older one has already been realised and cannot be taken back" —
and the marker is now unreachable. Every way back in then fails:

```clarity
;; contracts/bond-staker.clar:1654  credit-queue (reached from deposit / deposit-stx)
(asserts! (is-none (get exit-epoch record)) ERR_ALREADY_EXITING)   ;; u123
;; contracts/bond-staker.clar:1462  reserve-bridged-deposit (reached from the L1 bridge)
(asserts! (is-none (get exit-epoch (settle (get-or-create-member member)))) ERR_ALREADY_EXITING)
```

## Concrete path

```
bootstrap()                       ; bond 2 bound, pool initialized
deposit(alice, 10_000_000)        ; alice in, queued-epoch 0
deposit(bob,   30_000_000)
advanceToBurnHeight(bondStart-288); stake()          ; epoch 0 opens
requestExit(alice)                ; exit-epoch = some(0); exiting-sats = 10_000_000
setupBond(8); bindBond(8); advanceToBurnHeight(bondStart(8)-288); stake()
                                  ; roll into epoch 1:
                                  ;   - pool: exiting-sats -> released-sats, zeroed
                                  ;   - alice: settled, released-sats 10_000_000, shares 0
                                  ;   - alice: exit-epoch is STILL some(0)
cancelExit(alice)                 ; -> (err u113) POSITION_ACTIVE   (epoch-count-1 = 1 != 0)
setupBond(14); bindBond(14)
deposit(alice, 1_000_000)         ; -> (err u123) ALREADY_EXITING  ... for the rest of time
```

`announce-btc-deposit` reverts the same way for a member who joined with L1
bitcoin (`reserve-bridged-deposit`, `:1462`), so a bitcoin member cannot come
back through the bridge either. `get-settled-member` shows the stuck records:
members who left keep `exit-epoch` forever, and the pool's own
`exiting-sats` / `exiting-ustx` are already zero — the member's flag and the
pool's counter disagree from the roll onwards.

## Evidence

`tests/exit-lockout.test.ts` (in the PR / attached), run with the repo's own
harness:

```
$ npx vitest run tests/exit-lockout.test.ts
 × drops exit-epoch once the exit has been realised
   AssertionError: expected '0' to be null
     expect(settledMember(alice)["exit-epoch"]).toBe(null)
```

With the one-line fix below applied, the same test passes, and the existing
suite is otherwise unchanged (`87 passed`, 4 failed: the 3 pre-existing
`moving to another signer` failures caused by the signer-manager fixture that
this environment cannot reconstruct, plus the assertion in
`can be called off before the roll, but not after` that pins the old error code
for a realised exit — with the fix `cancel-exit` answers `NOT_EXITING` (u122)
instead of `POSITION_ACTIVE` (u113), which is still an error and still "cannot
be taken back", so only that expected value needs updating).

## Suggested fix

Clear the marker where the exit is realised:

```clarity
;; contracts/bond-staker.clar, advance-epoch's merged record
queued-sats: (- (get queued-sats record) joining-sats),
queued-ustx: (- (get queued-ustx record) joining-ustx),
exit-epoch: (if leaving none (get exit-epoch record)),
```

Members on the way out are otherwise unaffected: `exiting-sats` / `exiting-ustx`
are already zeroed by `stake`, and `credit-queue` / `reserve-bridged-deposit`
then agree with `cancel-exit`. (If the author prefers to keep a realised exit
"on the books", the alternative is to make it cancellable — i.e. drop the
`epoch-count - 1` assert in `cancel-exit` — but the marker has no other consumer,
so clearing it is the smaller change.)

---

# Observation 2 — the signer-trust delay is not time-bounded (design gap, not a rule violation)

Not part of the finding above, and stated with the caveat that I could not
exercise the `update-bond-registration` leg end-to-end in my environment.

`can-use-signer-manager` (`:423-434`) is `(> (var-get epoch-count) trusted-at)`,
with `trusted-at` stamped at `trust-signer-manager` time (`:1206`). The comment
is explicit about the intent: *"the roll is the **only** moment a member can
leave, so pinning adoption to it is what makes the notice worth anything"*, and
the test says *"on chain from the moment it is added, so members can see it
coming"*.

Nothing bounds how long the trust event precedes the roll, so the notice the
design relies on can be zero. `tx-sender` is preserved across `contract-call?`,
so an operator-owned helper contract can do all of it in **one transaction**:

```
helper -> bond-staker.trust-signer-manager(hash(H))     ; trusted-at = E   (tx-sender = operator)
helper -> bond-staker.stake(current-manager)            ; epoch-count = E+1, the roll
helper -> bond-staker.update-bond-registration(H, cur)  ; (E+1) > E  -> allowed
```

Every individual rule is honoured — the hash *was* added during epoch `E-1` and
adopted after the pool rolled out of it — but the members' exit window
(`request-exit` before the roll) is gone, and H is then the manager pox-5 pays
the bond's rewards through for the whole next term. The first three calls
suffice to shorten the notice to a single block without any helper contract.

The same holds for `update-operator`: the doc says the seat "always takes two
live operators", but one operator can enable a key it controls and disable the
other, and with exactly two entries the set can never be emptied (an operator
cannot touch its own entry), so the documented "wind the role down for good"
needs a third principal. Both are guards on the *amount of notice*, not on the
assets — which is why I have not claimed them above.

**Possible fix:** make the trust age one full roll rather than any roll — e.g.
stamp `trusted-at` as the epoch in progress and require
`(> (var-get epoch-count) (+ trusted-at u1))` at adoption, so a hash trusted
during epoch `E-1` is usable from the roll out of `E`, not the roll out of
`E-1`. That keeps the "already on the list when the epoch was staked" emergency
switch (the initial manager is stamped `u0` at `initialize`) while making the
member window a whole bond period wide.


---

## Appendix: the test that fails on the pinned commit

```ts
// PoC for the bounty submission.
//
// A member's `exit-epoch` is never cleared when the exit is realised at the
// roll.  `cancel-exit` then refuses (POSITION_ACTIVE) and `credit-queue`
// refuses (ALREADY_EXITING), so the member can never deposit again.
//
// EXPECTED TO FAIL on commit 0f8219cc564e34add0a20271d68cd57d15b8249b.
import { describe, expect, it } from "vitest";
import {
  advanceToBurnHeight,
  bindBond,
  bondStartHeight,
  bootstrap,
  deposit,
  MAX_SATS,
  NEXT_BOND_INDEX,
  poolTotals,
  requestExit,
  settledMember,
  stake,
  setupBond,
} from "./helpers/bond-fixture";

const accounts = simnet.getAccounts();
const alice = accounts.get("wallet_1")!;
const bob = accounts.get("wallet_2")!;

const ALICE_SATS = 10_000_000;
const BOB_SATS = 30_000_000;
const THIRD_BOND_INDEX = NEXT_BOND_INDEX + 6; // 14

describe("bond-staker: a member who left at a roll can come back", () => {
  it("drops exit-epoch once the exit has been realised", () => {
    const { bondStart } = bootstrap();
    deposit(alice, ALICE_SATS);
    deposit(bob, BOB_SATS);
    advanceToBurnHeight(bondStart - 288);
    expect(stake().type).toBe("ok");

    // alice asks to leave during epoch 0
    expect(requestExit(alice).type).toBe("ok");
    expect(Number(poolTotals()["exiting-sats"])).toBe(ALICE_SATS);

    // roll into the next bond -- her exit is realised here: paid back, no shares
    setupBond(NEXT_BOND_INDEX);
    expect(bindBond(NEXT_BOND_INDEX, MAX_SATS).type).toBe("ok");
    advanceToBurnHeight(bondStartHeight(NEXT_BOND_INDEX) - 288);
    expect(stake().type).toBe("ok");

    expect(Number(settledMember(alice)["released-sats"])).toBe(ALICE_SATS);
    expect(Number(settledMember(alice).shares)).toBe(0);

    // the exit is over, so the marker must be gone...
    expect(settledMember(alice)["exit-epoch"]).toBe(null);

    // ...and a fresh deposit for the following bond must be accepted
    setupBond(THIRD_BOND_INDEX);
    expect(bindBond(THIRD_BOND_INDEX, MAX_SATS).type).toBe("ok");
    expect(deposit(alice, 1_000_000).type).toBe("ok");
  });
});
```

Run: `npx vitest run tests/exit-lockout.test.ts` (uses the repo's own `tests/helpers/bond-fixture.ts`).

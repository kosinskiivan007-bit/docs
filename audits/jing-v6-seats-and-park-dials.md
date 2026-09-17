# markets-sbtc-stx-jing-v6 — review of the `NEW SINCE mtxs6nxg7a6d97081b11` range (26ad960..6632d01)

Bounty: `mu0ox53v1fae7181582b` (21 000 sats + 5 000 optimisation bonus).
Target: `github.com/Rapha-btc/jing-contracts-v3` @ `6632d01`, contracts `markets-sbtc-stx-jing-v6`,
`jing-ladder`, `jing-core-v5`, `jing-buy-stx-core-spread`.
Method: read of the seven new commits (1965 insertions / 312 deletions in the contract set),
line-level walk of the seat and park paths, and a check of every guard the brief lists under
invariants A–E. Source only; no mainnet writes, $0 spent.

Honest framing: this is a **confirmation-style** review (the brief accepts one explicitly: "or a
rigorous confirmation with edge cases and gaps"). I did not produce a fund-loss failing case in this
range. J-1 is a real defect of the operator dial with a concrete failing sequence; J-2..J-5 are
verified negatives with the exact guards, which is the part that usually costs the next reader the
most time.

---

## J-1 (Low, real) — the ladder's seat dial has no upper bound while the market's seat list is capped at 50

**Where.** `jing-ladder.clar` (6632d01), `set-max-band-per-side`:

```clarity
(asserts! (and (>= n (get-band-count SIDE_BUY_BAND))
               (>= n (get-band-count SIDE_SELL_BAND))) ERR_BAND_FULL)
(var-set max-band-per-side n)
```

There is a **floor** on `n` (it can never drop under the spreads a side already holds — good) and
**no ceiling**. The market then reads that number and clamps it:

```clarity
;; markets-sbtc-stx-jing-v6.clar
(define-private (refresh-seat-count)
  (let ((n (contract-call? .jing-ladder get-max-band-per-side)))
    (var-set seats-per-side (if (> n MAX_DEPOSITORS) MAX_DEPOSITORS n))
    (var-get seats-per-side)))
(define-data-var seated-x (list 50 principal) (list))   ;; MAX_DEPOSITORS = 50
```

**Why it breaks.** `refresh-seat-count` silently clamps > 50 down to 50, but the ladder keeps
allowing registrations up to its own `n`. The moment the owner sets `n` above 50 (say 51) and a band
side already holds 50 live spreads:

1. `set-max-band-per-side(51)` — accepted (`51 >= 50`).
2. A new canonical rung calls `register` → `(asserts! (< (get-band-count side) max))` passes
   (`50 < 51`) → `band-count` becomes 51.
3. That rung's `initialize` continues into the market's `sync-seat(self)`, and `with-seat` is handed
   a list that already has 50 members:

```clarity
(define-private (with-seat (lst (list 50 principal)) (who principal))
  (if (is-some (index-of? lst who))
    lst
    (unwrap-panic (as-max-len? (append lst who) u50))))
```

`as-max-len?` returns `none` for a 51-element list, so `unwrap-panic` aborts the whole transaction —
the ladder's `register` rolls back with it. The observable result is that the 51st spread **cannot be
deployed at all**, and with an opaque runtime panic rather than a named error.

Two further consequences worth knowing, both from the same clamp: with `n > 50` the operator believes
the ladder holds N seats while the market reserves only 50, and the ordering inside
`sync-seat` is `(filter still-seated (with-seat …))` — the prune runs **after** the append, so a prune
that would have made room can never execute: the drop-outs are known only after the append has
already failed.

**Fix (one line each).** Assert the ceiling on the ladder side so the dial cannot promise what the
market cannot hold — `(asserts! (<= n MAX_DEPOSITORS) ERR_BAND_FULL)` — and/or run the prune first:
`(and x (var-set seated-x (with-seat (filter still-seated-x (var-get seated-x)) who)))`. If a
ceiling is undesirable, replace `unwrap-panic` with `ERR_QUEUE_FULL` so the failure is legible.

**Not claimed:** this is not fund loss and not an outside attack — it needs the operator to set a
value above 50. It is a dial/implementation mismatch (silent clamp on one side, no bound on the
other) that turns into an un-deployable rung.

---

## J-2 — invariant D, "max lowered under holders": **guarded**

`set-max-band-per-side` asserts `n >= band-count` on **both** band sides before writing, so the
reservation can never be dropped below the spreads a side holds. Confirmed by reading the guard; no
bypass found (the only writer of `max-band-per-side` is this function).

## J-3 — band accounting on register / replace / retire: **consistent**

Walked the three branches of `register` and `retire-band`:
* free spread → `band-count += 1`;
* taken spread → the older holder is deleted from `registered` and the count is **not** touched
  (one holder replaces another, the number of occupied spreads is unchanged);
* `retire-band` → requires the rung to exist (`unwrap!` on the spread key), deletes both `rungs` and
  `registered` for the holder, `band-count -= 1`. Because the entry must exist, the decrement cannot
  underflow, and a repeat retire aborts before it.
* `register` is gated on `contract-hash?` equality with the canonical deploy of that side and on
  `(is-none (map-get? registered caller))`, so a rung cannot be counted twice and a non-rung cannot
  register itself.

No drift found. The market's local list is self-healing in the same expression: a replaced or retired
rung is removed by the `still-seated-x/y` filter on the next `sync-seat` for that side, and any live
band rung can be named to trigger it.

## J-4 — `side-full-x/y` arithmetic: **consistent, including at the extremes**

For a seat holder: full at `(len depositors) >= 50`. For everyone else:
`full = (len depositors) - seated_on(depositors, seated) >= 50 - protected-seats`, i.e. the non-seat
makers are limited to `50 - seats` regardless of whether the seats are occupied — which is the stated
intent ("anyone else sees 50 minus seats, taken or not"). `seated-on` counts only seated principals
that are **currently depositors**, so a stale list entry cannot shrink the effective count of
non-seat makers. At `seats = 50` the non-seat test degenerates to `0 >= 0` — always full, as
intended. `refresh-seat-count` reads the ladder's **max** (not the live count), which is the
conservative direction. Duplicates are impossible: `with-seat` appends only when `index-of?` is none.

## J-5 — `sync-seat`: **not a griefing surface**

`sync-seat(who)` asserts that the ladder actually seats `who` (`is-band-x` / `is-band-y`, else
`u1028`), and touches only the side(s) the ladder reports. An outsider cannot seat a non-rung and
cannot prune the opposite side's list. The only reachable defect on this path is the ordering inside
J-1.

---

## Where I did not get

* Invariant B (full-book park outcomes: distance-slots 0/50, price ties, sentinels in the top set,
  "a parked maker unreachable"): read but not exhausted — the fold set for "N-th best out-of-range"
  plus the size-region survivor selection is the densest part of the change and is where a failing
  case is most likely still hiding. I did not find one; I also did not clear it.
* Invariant C (band rungs): the guard path (`get-native-price`, floor/cap, `u7008` on zero) and
  `initialize` (owner-only, `ERR_ALREADY_INITIALIZED`, name derived from `bps`) were read as
  negatives only; the "fat finger" boundary (an honest mid passing the guard) was not tested against
  a fork.
* Invariant F (router v5 / vault v6 under "bumped = parked"): not reviewed in this pass.
* The 5 000-sat optimisation bonus: not attempted — it needs the fork harness (`b0bd067c`, steps
  130/135) to count reads and runtime, which I could not reproduce locally in this session.

*Review of source only. No transactions were created, signed or broadcast; no harness was run.*

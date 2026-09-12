**Finding (invariant A broken): the out-of-band pegged-ASK sentinel is not skipped by the sort, the walk or `get-taker-capacity`, because the only thing that skips it is the taker's own `limit-price`, and `swap` does not upper-bound that.**

Root cause — the two sentinels are defended asymmetrically.

`pegged-ask` (markets-sbtc-stx-jing-v6.clar L269-279, sentinel at **L277**) returns `MAX_UINT` when the peg is out of band; `pegged-bid` (L256-266) returns `u0`. Every *bid-side* reader defends the sentinel with an explicit equality test:

- `collect-bid-step` **L2156** `(is-eq l u0)`
- `walk-y-book-step` **L2006** `(is-eq l u0)`
- `cap-bid-fold` **L2864** `(not (is-eq l u0))`

No *ask-side* reader has the mirror test for `MAX_UINT`. It relies entirely on the maker's/ taker's `limit`:

- `collect-ask-step` **L2113-2114** `(<= l mid)` / `(> l (get limit acc))`
- `walk-x-book-step` **L1965-1966** `(<= l (get mid st))` / `(> l (get limit st))`
- `cap-ask-fold` **L2889-2895** `(<= l (get limit acc))` -> `(/ (* amt l) (cap-scale))`

For an inactive peg `l = MAX_UINT` (L31), so of the guards above only the `limit` comparison can fire, and `swap` (L1701-1756) never upper-bounds `limit-price` (it is only later asserted `> u0`). With `limit-price = u340282366920938463463374607431768211455` the comparison is `(> MAX_UINT MAX_UINT)` = false, so the sentinel passes every filter.

This contradicts README-markets-v6-pegged.md ("How inactive is represented"): *"Every reader in the contract already treated a bid at zero and an ask at an impossible price as 'never fills': the walk skips it, the sort skips it, capacity skips it"*, and it is exactly the class the bounty names in invariant A ("an out-of-band peg ... sorts, counts in capacity ... the sentinel leaks into a price, a log or an overflow").

Reproduction (single parameter: `limit-price = uMAX`):

1. A maker rests an out-of-band pegged ask and the cycle has not been settled yet, so it is still in `token-x-depositors` (e.g. a spread rung under its floor: `deposit-token-x amount floor (some s)` while mid sits below the derived floor, making `token-x-limit-at` return `MAX_UINT`).
2. `sorted-asks cycle mid uMAX` **lists** it — `collect-ask-step` L2114 `(> MAX_UINT uMAX)` is false, so it is inserted into the 50-slot book. The taker walk then keeps it too (`walk-x-book-step` L1966 is false), violating "the taker walk does not list it".
3. `get-taker-capacity mid uMAX false` **counts** it in `walk` via `cap-ask-fold` L2889-2895. The term `(/ (* amt l) (cap-scale))` = `amt * uMAX / 1e10`; the uint128 product `(* amt uMAX)` overflows for any `amt >= 2`, so the read-only call aborts — "capacity skips it" is false and this is the sentinel-leaks-into-an-overflow case.

Impact (scoped honestly):

- No fund loss, and I am not claiming one: the walked fill is a no-op because `execute-fill` (L1762) computes `x-from-y = (y-amt * 1e10) / MAX_UINT = 0`, hence `x-traded = y-traded = 0` and the `(ok false)` branch (L1820) returns before any state change or log.
- Real effects: (a) the documented "inactive" invariant is false on the ask side; (b) `get-taker-capacity` reverts, and that is the sizing call the retail router makes (`swap-router-sbtc-stx-jing-v5.clar` L731), so any integrator that forwards a `uMAX` limit gets a revert instead of a capacity; (c) the same hole applies to a *fixed* ask whose maker sets `limit-price = uMAX` (accepted — L734/L875 only assert `> u0`), because a fixed ask can then not be distinguished from the inactive sentinel.

Suggested fix (one line, mirroring the bid side): add `(is-eq l MAX_UINT)` to the skip conditions of `collect-ask-step`, `walk-x-book-step` and `cap-ask-fold`, and/or assert `(< limit-price MAX_UINT)` in `swap`, `deposit-token-x-core` and `set-token-x-limit`/`reprice-or-swap-token-x`.

Scope note: this is on top of the previous v6 diff reviews (commit f04ebb5). I re-checked `prune-cycles` (all reads key off `current-cycle`; open/future cycles are rejected u1027), the settled-cycle-roll filters, and the refund/dust path, and found nothing else exploitable.

# Investigation Process

How I went from "black box" to an exact reimplementation, including the
hypotheses that turned out to be wrong.

- **Broad survey first.** I swept one variable at a time (weight, distance,
  category, express, coupon) around a baseline `quote(2,100,"standard")=330`
  to see which inputs moved the price and roughly how. This immediately showed
  weight and distance were the main drivers, categories shifted the price, and
  express seemed to do nothing.

- **Isolated the base subtotal.** Fixing distance at its minimum and sweeping
  weight (and vice-versa) gave two clean straight lines: **₹40/kg** and
  **₹2.5/km**, with a zero intercept. `quote(2,100,"standard")` = `40*2 + 2.5*100`.

- **Found the weight is rounded up.** All weights in `(0, 0.5]` cost the same,
  then the price stepped at 0.6 kg → the engine bills `ceil(w/0.5)*0.5`, not the
  raw weight.

- **Wrong hypothesis #1 — tiered distance rates.** The distance line "bent"
  around 300 km (marginal rate looked like it dropped from 2.5 to ~2.25/km),
  so I first modelled distance as **two marginal tiers** with a 300 km
  breakpoint. It never fit cleanly — the numbers were off by odd amounts and a
  strange ₹42-over-50km step appeared.

- **The real cause — a subtotal discount, not a distance tier.** The tell was
  fractional prices like `722.25`. Dividing actual by expected gave exactly
  **0.9**. The "bend" wasn't about distance at all: it was a **10% discount when
  the subtotal exceeds 800**. The same 0.9 factor also explained a mystery drop
  in the *weight* sweep at ~20 kg — same rule, different variable.

- **Nailed the threshold.** A fine sweep showed `subtotal=800` is **not**
  discounted but `802.5` is, so the condition is strictly `> 800`.

- **Wrong hypothesis #2 — categories are all multipliers.** Electronics
  (×1.3) fit a multiplier, so I assumed fragile was too. But `480/330 = 1.4545…`
  is not clean. Varying the subtotal revealed fragile keeps a constant
  **difference of +150** (additive surcharge), while electronics keeps a
  constant **ratio**. So: electronics multiplicative, fragile additive.

- **Wrong hypothesis #3 — `WELCOME10` is a percentage.** At `w=2,d=100` it cut
  the price by 100, which *looked* like ~30%. Testing across several order sizes
  showed the reduction was always exactly **100**, i.e. a flat discount, not a
  percentage. It also has **no floor** — small orders go negative.

- **Wrong hypothesis #4 — `express` matters.** For a shipping engine I expected
  express to add a surcharge. It never changed the price across 3,000 random
  combinations, so I concluded it's a genuine no-op and documented it as such.

- **Pinned the order of operations.** Using additive fragile as a probe
  (`quote(0.5,352,"fragile")=945`) proved the sequence is
  **category → then >800 discount → then flat coupon**, and that the 800 check
  reads the *post-category* subtotal (`quote(0.5,272,"electronics")=819`).

- **Validated exhaustively.** `probes/06_validate.py` compares `my_quote`
  against the oracle on 10,000 random inputs plus a grid of every boundary
  (weight rounding edges, the 800 threshold, all six categories, coupon on/off):
  **0 mismatches out of 10,756 cases.**

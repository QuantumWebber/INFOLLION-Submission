# SPEC — Recovered Pricing Rules of `oracle.quote()`

Every rule below was found **only** by calling `quote()` and fitting the outputs.
The encoded blob inside `oracle.py` was never decoded or read.

The engine computes a single running `price`, applying the steps in this exact
order. `my_quote.py` reproduces this and matches the oracle on **10,756 / 10,756**
test cases (0 mismatches), including all boundary points below.

---

## Rule 1 — Billable weight is rounded **up** to the next 0.5 kg

`weight_kg` is not billed directly. It is rounded up to the nearest 0.5 kg
before pricing:

```
billable_weight = ceil(weight_kg / 0.5) * 0.5
```

**Evidence:** every weight in `(0, 0.5]` prices the same, then it jumps.

| query | price | billed as |
|---|---|---|
| `quote(0.1, 100, "standard")` | 270.0 | 0.5 kg |
| `quote(0.5, 100, "standard")` | 270.0 | 0.5 kg |
| `quote(0.6, 100, "standard")` | 290.0 | 1.0 kg |
| `quote(1.0, 100, "standard")` | 290.0 | 1.0 kg |

## Rule 2 — Base subtotal is linear in weight and distance

```
subtotal = 40 * billable_weight + 2.5 * distance_km
```

- Weight rate: **₹40 per billable kg**
- Distance rate: **₹2.5 per km**
- No fixed base fee (the intercept is 0).

**Evidence:** `quote(2, 100, "standard") = 330.0` = `40*2 + 2.5*100 = 80 + 250`.
Isolating each variable:
- At `d=1`: `quote(0.5,1,"standard")=22.5` = `40*0.5 + 2.5*1 = 20 + 2.5`.
- Distance is a clean 2.5/km line until the discount in Rule 4 kicks in:
  `quote(0.5, 50,"standard")=145.0`, `quote(0.5,100,"standard")=270.0`
  (steps of exactly 125.0 per 50 km).

## Rule 3 — Category adjustment (applied to the subtotal)

| category | effect |
|---|---|
| `standard`, `books`, `clothing`, `food` | no change |
| `electronics` | **× 1.30** (multiplicative) |
| `fragile` | **+ 150** (flat surcharge) |

**Evidence** (all with `w=2, d=100`, base subtotal 330):

| query | price | check |
|---|---|---|
| `quote(2,100,"electronics")` | 429.0 | 330 × 1.3 |
| `quote(2,100,"fragile")` | 480.0 | 330 + 150 |
| `quote(2,100,"books")` | 330.0 | = standard |

That electronics is multiplicative and fragile is additive was confirmed by
varying the subtotal: electronics keeps a constant **ratio** (1.3), while
fragile keeps a constant **difference** (+150):

- `quote(2,40,"fragile")=330` (base 180, +150), `quote(1,200,"fragile")=690` (base 540, +150).

## Rule 4 — Bulk discount: 10% off when the subtotal exceeds 800

After the category adjustment, if the running subtotal is **strictly greater
than 800**, the whole subtotal is multiplied by 0.90.

```
if subtotal > 800:
    subtotal *= 0.90
```

The threshold is checked on the **category-adjusted** subtotal, and the discount
is applied to that same value.

**Evidence (exact boundary):**

| query | subtotal | price | discounted? |
|---|---|---|---|
| `quote(0.5, 312, "standard")` | 800.0 | 800.0 | no (not `> 800`) |
| `quote(0.5, 313, "standard")` | 802.5 | 722.25 | yes (× 0.9) |

**Evidence (threshold uses post-category value):**
`quote(0.5, 272, "electronics")` → base 700, ×1.3 = **910** (>800) → ×0.9 =
**819.0** ✓. The base 700 alone would *not* trigger the discount, so the check
happens after the category step.

**Evidence (order category-then-discount, not the reverse):**
`quote(0.5, 352, "fragile")` → base 900, +150 = 1050, ×0.9 = **945.0** ✓
(discount-first would give `900×0.9 + 150 = 960`, which is wrong).

## Rule 5 — `express` flag has no effect on price

The `express` parameter is accepted but never changes the returned price.
Verified over 3,000 random input combinations: `express=True` and
`express=False` produced identical prices in every single case.

```
quote(2, 100, "standard", express=False) == quote(2, 100, "standard", express=True)  # 330.0
```

## Rule 6 — Coupon `WELCOME10` subtracts a flat 100 (no floor)

Only the exact, case-sensitive string `"WELCOME10"` is honoured. It subtracts a
**flat 100** from the price as the **last** step (after the discount). Any other
code (including `"welcome10"`) is ignored.

```
if coupon == "WELCOME10":
    price -= 100
```

There is **no lower bound** — on small orders the price can go negative, and the
oracle does exactly this, so `my_quote` does too:

| query | price |
|---|---|
| `quote(2,100,"standard",coupon="WELCOME10")` | 230.0 (330 − 100) |
| `quote(0.5,1,"standard",coupon="WELCOME10")` | **−77.5** (22.5 − 100) |
| `quote(2,100,"standard",coupon="SAVE10")` | 330.0 (ignored) |

## Rule 7 — Final rounding

The result is rounded to 2 decimals: `round(price, 2)`.

---

## Full formula (pseudocode)

```
billable = ceil(weight_kg / 0.5) * 0.5
price    = 40 * billable + 2.5 * distance_km
if category == "electronics": price *= 1.30
elif category == "fragile":   price += 150
if price > 800:               price *= 0.90
# express: no-op
if coupon == "WELCOME10":     price -= 100
return round(price, 2)
```

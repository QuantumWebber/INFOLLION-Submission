# Black-Box Reverse Engineering — Shipping Quote Engine

Reverse-engineering assignment: `oracle.py` is a compiled "black box" shipping
pricing engine exposing `quote(weight_kg, distance_km, category, express, coupon)`.
The goal was to recover its pricing rules **by experiment only** (never decoding
the implementation) and reimplement them in `my_quote.py`.

## Result

`my_quote.py` reproduces the oracle **exactly** — 0 mismatches over 10,756
validation cases spanning random inputs and every boundary condition.

## Recovered formula

```python
billable = ceil(weight_kg / 0.5) * 0.5      # round weight UP to next 0.5 kg
price    = 40 * billable + 2.5 * distance_km # ₹40/kg + ₹2.5/km, no base fee
if category == "electronics": price *= 1.30  # multiplicative surcharge
elif category == "fragile":   price += 150   # flat surcharge
if price > 800:               price *= 0.90  # 10% bulk discount, subtotal > 800
# express: accepted but has no effect on price
if coupon == "WELCOME10":     price -= 100   # flat, case-sensitive, no floor
return round(price, 2)
```

See **[SPEC.md](SPEC.md)** for each rule with evidence, and
**[INVESTIGATION.md](INVESTIGATION.md)** for the process (and the wrong turns).

## Repository layout

```
.
├── my_quote.py        # clean-room reimplementation (the deliverable)
├── oracle.py          # provided black box (kept so the repo runs standalone)
├── SPEC.md            # every discovered rule, in plain English, with examples
├── INVESTIGATION.md   # 5–10 bullet write-up incl. incorrect hypotheses
└── probes/            # the scripts used to investigate the oracle
    ├── 01_survey.py                 # broad one-variable-at-a-time sweep
    ├── 02_isolate_components.py     # decompose weight/distance/coupon
    ├── 03_weight_distance.py        # clean isolation of each rate
    ├── 04_threshold_and_category.py # find the 800 threshold + category effects
    ├── 05_order_of_operations.py    # pin category vs discount vs coupon order
    └── 06_validate.py               # my_quote vs oracle, 10k+ cases
```

## Running it

Requires only Python 3 (standard library — no third-party packages).

```bash
# use the recovered engine
python3 -c "from my_quote import quote; print(quote(2, 100, 'standard'))"   # 330.0

# reproduce the investigation
python3 probes/01_survey.py

# verify my_quote matches the oracle exactly
python3 probes/06_validate.py
# -> express-caused differences: 0
# -> validated 10756 cases, mismatches=0
```

## Notes

- The oracle's encoded implementation was **not** decoded or inspected; all
  rules were inferred from input/output behaviour, as the assignment requires.
- Quirks faithfully reproduced: `express` is a no-op, and the `WELCOME10` coupon
  has no lower bound (small orders can yield a negative price).

"""
my_quote.py — clean-room reimplementation of oracle.py's shipping quote engine.

All pricing rules below were recovered purely by black-box experimentation
(calling oracle.quote() with designed inputs and fitting the outputs). The
oracle's encoded implementation was never decoded or inspected.

Discovered model
----------------
1. Billable weight = ceil(weight_kg / 0.5) * 0.5   (round UP to next 0.5 kg)
2. Subtotal        = 40 * billable_weight + 2.5 * distance_km
3. Category:
      electronics -> subtotal *= 1.30      (multiplicative surcharge)
      fragile     -> subtotal += 150       (flat surcharge)
      standard / books / clothing / food -> no change
4. Bulk discount: if subtotal > 800 -> subtotal *= 0.90
5. express flag: no effect on price (verified over thousands of cases)
6. Coupon: coupon == "WELCOME10" (exact, case-sensitive) -> subtotal -= 100
      No floor: the price may go negative on very small orders.
7. Return round(subtotal, 2)
"""
import math


def quote(weight_kg, distance_km, category, express=False, coupon=""):
    billable_weight = math.ceil(weight_kg / 0.5) * 0.5
    price = 40.0 * billable_weight + 2.5 * distance_km

    if category == "electronics":
        price *= 1.30
    elif category == "fragile":
        price += 150.0

    if price > 800.0:
        price *= 0.90

    # express is accepted but does not change the price (matches the oracle).

    if coupon == "WELCOME10":
        price -= 100.0

    return round(price, 2)

import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oracle import quote, reset_counter, queries_used

def q(*a, **k): return quote(*a, **k)

# baseline
print("base 2,100,standard:", q(2.0,100,"standard"))

# weight sweep (dist fixed, standard, no express, no coupon)
print("\n-- weight sweep (dist=100, standard) --")
for w in [0.1,0.5,1,2,3,5,10,20,50,100]:
    print(w, q(w,100,"standard"))

# distance sweep (weight fixed)
print("\n-- distance sweep (w=2, standard) --")
for d in [1,10,50,100,200,500,1000,2000,5000]:
    print(d, q(2,d,"standard"))

# category sweep (same w,d)
print("\n-- category sweep (w=2,d=100) --")
for c in ["standard","electronics","fragile","books","clothing","food"]:
    print(c, q(2,100,c))

# express
print("\n-- express (w=2,d=100,standard) --")
print("F", q(2,100,"standard",False))
print("T", q(2,100,"standard",True))

# coupons
print("\n-- coupons (w=2,d=100,standard) --")
for cp in ["","WELCOME10","WELCOME","SAVE20","SAVE10","FREESHIP","HALF","10","DISCOUNT"]:
    print(repr(cp), q(2,100,"standard",False,cp))
print("\nqueries:", queries_used())

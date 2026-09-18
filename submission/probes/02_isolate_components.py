import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oracle import quote as q, queries_used

# Decompose. Use standard (assume mult 1). Vary weight at d=1 tiny, and distance at w=0.1 min.
print("-- weight floor check (d=100 std) --")
for w in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5]:
    print(w, q(w,100,"standard"))

print("\n-- distance fine (w=2 std), find breakpoints --")
for d in [1,2,5,20,100,150,199,200,201,250,300,400,499,500,501,600,1000]:
    print(d, q(2,d,"standard"))

print("\n-- isolate: w=0.1,d=1 std (min everything) --")
print(q(0.1,1,"standard"))

print("\n-- express across categories & bigger orders --")
for c in ["standard","electronics","fragile"]:
    for e in [False,True]:
        print(c,e, q(5,500,c,e))

print("\n-- coupon: is WELCOME10 flat 100 or 10%? --")
for w,d in [(2,100),(10,500),(50,1000)]:
    base=q(w,d,"standard"); wel=q(w,d,"standard",False,"WELCOME10")
    print(f"w{w}d{d}: base={base} welcome={wel} diff={round(base-wel,2)} pct={round((base-wel)/base*100,2)}")

print("\n-- other coupon codes --")
for cp in ["WELCOME10","welcome10","SAVE15","STUDENT","FREE100","BULK","NEWYEAR","SUMMER"]:
    print(repr(cp), q(10,500,"standard",False,cp))
print("queries",queries_used())

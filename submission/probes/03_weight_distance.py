import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oracle import quote as q, queries_used

# Isolate WEIGHT at min distance d=1 (std). Distance cost minimal & constant.
print("-- weight @ d=1 std --")
prev=None
for w in [0.5,1,2,3,4,5,6,8,10,15,20,25,30,40,50,70,100]:
    v=q(w,1,"standard"); d=None if prev is None else round(v-prev,2)
    print(f"w={w:<5} {v:<9} d={d}")
    prev=v

# Isolate DISTANCE at min weight w=0.5 (std)
print("\n-- distance @ w=0.5 std --")
prev=None
for d in [1,50,100,150,200,250,280,299,300,301,350,400,500,800,1000,2000,5000]:
    v=q(0.5,d,"standard"); dd=None if prev is None else round(v-prev,2)
    print(f"d={d:<6} {v:<10} step={dd}")
    prev=v

# express: try many combos incl with coupon and heavy
print("\n-- express deeper --")
for args in [(2,100,"standard"),(2,100,"electronics"),(50,3000,"fragile"),(2,100,"books"),(2,100,"food")]:
    print(args, "F",q(*args,False),"T",q(*args,True))

print("queries",queries_used())

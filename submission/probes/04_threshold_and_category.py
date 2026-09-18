import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oracle import quote as q, queries_used

# Confirm subtotal>threshold -> *0.9. Base model (std): sub = 40*ceil(w/0.5)*0.5 + 2.5*d
import math
def sub(w,d): return 40*(math.ceil(round(w/0.5,9))*0.5) + 2.5*d

print("-- threshold hunt (std): expect discount when sub>X --")
# vary d at w=0.5 (weight20) so sub=20+2.5d ; find where /full !=1
for d in [308,310,311,312,313,314,315,320]:
    v=q(0.5,d,"standard"); s=sub(0.5,d)
    print(f"d={d} sub={s} price={v} ratio={round(v/s,4)}")

print("\n-- category isolation: pick sub well under 800 --")
# w=2,d=40 std: sub=80+100=180
for c in ["standard","electronics","fragile","books","clothing","food"]:
    print(f"{c:12} q(2,40)={q(2,40,c):<8} q(4,80)={q(4,80,c):<8} q(1,200)={q(1,200,c)}")

print("\n-- coupon order: flat100 before/after discount & category --")
# electronics big order to trigger discount
for w,d,c in [(2,100,"electronics"),(10,500,"standard"),(2,100,"fragile"),(0.5,50,"standard")]:
    base=q(w,d,c); cp=q(w,d,c,False,"WELCOME10")
    print(f"{c} w{w}d{d}: base={base} coupon={cp} diff={round(base-cp,2)}")

# coupon floor: tiny order, does it go negative or floor?
print("\n-- coupon on tiny order --")
print("q(0.5,1,std)=",q(0.5,1,"standard"),"coupon=",q(0.5,1,"standard",False,"WELCOME10"))
print("q(0.5,20,std)=",q(0.5,20,"standard"),"coupon=",q(0.5,20,"standard",False,"WELCOME10"))
print("queries",queries_used())

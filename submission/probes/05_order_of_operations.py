import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oracle import quote as q, queries_used
import math
def basesub(w,d): return 40*(math.ceil(round(w/0.5,9))*0.5) + 2.5*d

# Does discount threshold use PRE or POST category value?
# electronics: base_sub=700 (<800) but *1.3=910 (>800)
w,d=0.5,272   # basesub=20+680=700
print("basesub",basesub(w,d))
print("electronics 700->910?:", q(w,d,"electronics"))
print("  H_post(disc on 910): 910*0.9=",910*0.9)
print("  H_pre(no disc): 910")

# fragile: base_sub=700, +150=850(>800). base<800.
print("fragile 700->850?:", q(w,d,"fragile"))
print("  H_post:850*0.9=",850*0.9,"  H_pre:850")

# both under after? electronics base 600 ->780(<800) no disc
w2,d2=0.5,232  # basesub=20+580=600
print("basesub2",basesub(w2,d2),"electronics->",q(w2,d2,"electronics"),"(600*1.3=780)")

# discount applied to base then category? base_sub=900>800 -> *0.9=810 -> *1.3=1053  vs  900*1.3=1170>800 ->*0.9=1053 (same!). need asymmetric case.
# Use fragile (additive) to distinguish. base_sub=900 (>800). 
#  H_B: base*0.9=810, +150=960
#  H_A: cat=900+150=1050 (>800) *0.9=945
w3,d3=0.5,352  # basesub=20+880=900
print("\nbasesub3",basesub(w3,d3))
print("fragile base900:",q(w3,d3,"fragile"),"| H_B(disc-first)=960  H_A(cat-first)=945")

# base_sub=900 electronics: H_B 810*1.3=1053 ; H_A 1170*0.9=1053 same. skip.
# coupon interaction with discount: does coupon count toward threshold? coupon is last (flat -100), already seen -ve, so after everything.
# verify coupon after discount: electronics w2 d100=429(no disc). big: w10 d500 std
b=q(10,500,"standard"); print("\nw10d500 std base",b,"| basesub",basesub(10,500),"disc?",basesub(10,500)>800)
print("  expect basesub",basesub(10,500),"*0.9=",basesub(10,500)*0.9)
print("queries",queries_used())

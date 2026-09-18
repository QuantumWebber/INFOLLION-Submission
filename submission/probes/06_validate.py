import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random, itertools
from oracle import quote as oracle_q, reset_counter, queries_used
from my_quote import quote as my_q

reset_counter()
cats=["standard","electronics","fragile","books","clothing","food"]
coupons=["","WELCOME10","welcome10","SAVE10","WELCOME","FREESHIP"]
mism=0; n=0

# 1) thorough express check: does express EVER change price?
exp_diff=0
random.seed(1)
for _ in range(3000):
    w=round(random.uniform(0.1,100),2); d=round(random.uniform(1,5000),1)
    c=random.choice(cats); cp=random.choice(coupons)
    if oracle_q(w,d,c,False,cp)!=oracle_q(w,d,c,True,cp): exp_diff+=1
print("express-caused differences:",exp_diff,"(0 => express is a no-op)")

# 2) big random validation of my_quote vs oracle
random.seed(42)
fails=[]
for _ in range(10000):
    w=round(random.uniform(0.1,100),random.choice([0,1,2]))
    d=round(random.uniform(1,5000),random.choice([0,1]))
    c=random.choice(cats); e=random.choice([True,False]); cp=random.choice(coupons)
    o=oracle_q(w,d,c,e,cp); m=my_q(w,d,c,e,cp); n+=1
    if o!=m:
        mism+=1
        if len(fails)<10: fails.append((w,d,c,e,cp,o,m))

# 3) grid over boundaries (weight rounding, 800 threshold, categories)
for w in [0.1,0.4,0.5,0.6,1.0,1.1,19.9,20.0,20.1]:
    for d in [1,311,312,313,300,301,5000]:
        for c in cats:
            for cp in ["","WELCOME10"]:
                o=oracle_q(w,d,c,False,cp); m=my_q(w,d,c,False,cp); n+=1
                if o!=m:
                    mism+=1
                    if len(fails)<10: fails.append((w,d,c,False,cp,o,m))

print(f"\nvalidated {n} cases, mismatches={mism}")
for f in fails: print("  MISMATCH",f)
print("oracle queries used:",queries_used())

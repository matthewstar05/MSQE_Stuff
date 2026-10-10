"""Generate oj.csv matching lab stats (n=28,947) for microols.py when Canvas file is unavailable."""
import csv
import math
import random

random.seed(42)
n = 28947
a_true, bmm_true, btr_true, b0_true = -3.1387, 0.8702, 1.5299, 10.8288

rows = []
for _ in range(n):
    u = random.random()
    if u < 0.35:
        mm, tr = 0.0, 1.0  # Tropicana
    elif u < 0.65:
        mm, tr = 1.0, 0.0  # Minute Maid
    else:
        mm, tr = 0.0, 0.0  # Dominick's (omitted category)
    price = math.exp(random.gauss(1.2, 0.25)) * 2.0
    lnp = math.log(price)
    lnq = (
        a_true * lnp
        + bmm_true * mm
        + btr_true * tr
        + b0_true
        + random.gauss(0, 0.15)
    )
    qty = math.exp(lnq)
    rows.append(
        {
            "quantity": qty,
            "price": price,
            "minute_maid": int(mm),
            "tropicana": int(tr),
        }
    )

path = "/Users/star/Desktop/CSC/ECON470/oj.csv"
with open(path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["quantity", "price", "minute_maid", "tropicana"])
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} rows to {path}")

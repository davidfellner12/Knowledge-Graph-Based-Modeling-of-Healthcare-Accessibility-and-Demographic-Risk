import pandas as pd
import random

districts = [f"Wien-{i}" for i in range(1, 24)] + ["Linz-1", "Graz-1", "Innsbruck-1", "Salzburg-1"]

rows = []

for d in districts:
    rows.append([
        d,
        random.randint(20000, 200000),     
        random.uniform(0.10, 0.35),        
        48.2 + random.uniform(-0.5, 0.5),
        16.3 + random.uniform(-0.5, 0.5)
    ])

df = pd.DataFrame(rows, columns=[
    "district", "population", "elderly_pct", "lat", "lon"
])

df.to_csv("data/raw/districts.csv", index=False)
print("✔ districts updated")
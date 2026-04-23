import pandas as pd
import random

districts = [f"Wien-{i}" for i in range(1, 24)] + ["Linz-1", "Graz-1", "Innsbruck-1"]

rows = []

for i in range(200):
    d = random.choice(districts)

    rows.append([
        f"gp{i}",
        f"GP_{i}",
        d,
        48.2 + random.uniform(-0.2, 0.2),
        16.3 + random.uniform(-0.2, 0.2)
    ])

df = pd.DataFrame(rows, columns=["id","name","district","lat","lon"])
df.to_csv("data/raw/gps_big.csv", index=False)

print("Generated gps_big.csv")  
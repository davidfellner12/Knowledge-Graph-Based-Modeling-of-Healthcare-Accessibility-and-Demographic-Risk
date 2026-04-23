import pandas as pd

districts = pd.read_csv("data/raw/districts.csv")
hospitals = pd.read_csv("data/raw/hospitals.csv")

triples = []

for _, d in districts.iterrows():
    triples.append((d["district"], "hasPopulation", d["population"]))
    triples.append((d["district"], "hasElderlyRate", d["elderly_pct"]))


for _, d in districts.iterrows():
    for _, h in hospitals.iterrows():
        triples.append((d["district"], "nearHospital", h["id"]))

# Save for PyKEEN
df = pd.DataFrame(triples, columns=["head", "relation", "tail"])
df.to_csv("data/processed/kg_triples.csv", index=False)

print("✔ Triples created")
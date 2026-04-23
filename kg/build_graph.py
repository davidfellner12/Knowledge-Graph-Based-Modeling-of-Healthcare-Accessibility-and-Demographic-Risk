from rdflib import Graph, Namespace, Literal, RDF
import pandas as pd

EX = Namespace("http://healthkg.org/")

g = Graph()
g.bind("ex", EX)

districts = pd.read_csv("data/raw/districts.csv")
hospitals = pd.read_csv("data/raw/hospitals.csv")

# Add hospitals
for _, row in hospitals.iterrows():
    h = EX[row["id"]]
    g.add((h, RDF.type, EX.Hospital))
    g.add((h, EX.name, Literal(row["name"])))
    g.add((h, EX.lat, Literal(row["lat"])))
    g.add((h, EX.lon, Literal(row["lon"])))

# Add districts
for _, row in districts.iterrows():
    d = EX[row["district"].replace(" ", "_")]

    g.add((d, RDF.type, EX.District))
    g.add((d, EX.population, Literal(row["population"])))
    g.add((d, EX.elderly_pct, Literal(row["elderly_pct"])))
    g.add((d, EX.lat, Literal(row["lat"])))
    g.add((d, EX.lon, Literal(row["lon"])))

g.serialize("data/processed/kg.ttl")
print("KG created!")
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
import pandas as pd

df = pd.read_csv("data/processed/kg_triples.csv")

triples = df[["head", "relation", "tail"]].values

tf = TriplesFactory.from_labeled_triples(triples)

result = pipeline(
    training=tf,
    testing=tf,
    model="TransE",
    training_kwargs=dict(num_epochs=50),
)

result.save_to_directory("ml/transe_model")

print("✔ TransE trained successfully")
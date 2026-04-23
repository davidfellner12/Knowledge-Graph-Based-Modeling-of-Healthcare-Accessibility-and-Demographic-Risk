import torch
import pandas as pd
from flask import Flask, jsonify

from services.inference import HealthcareInferenceEngine
from ml.graphsage import GraphSAGE


app = Flask(__name__)

districts = pd.read_csv("data/processed/districts_enriched.csv")
hospitals = pd.read_csv("data/raw/hospitals_big.csv")
triples = pd.read_csv("data/processed/kg_triples.csv")

# load model
model = GraphSAGE(in_channels=201, hidden_channels=16)
model.load_state_dict(torch.load("ml/graphsage_model.pt", map_location="cpu"))

engine = HealthcareInferenceEngine(
    model=model,
    triples_df=triples,
    districts_df=districts,
    hospitals_df=hospitals
)


@app.route("/risk/<district>")
def risk(district):
    return jsonify(engine.run(district))


@app.route("/")
def home():
    return {"status": "OK"}


if __name__ == "__main__":
    app.run(debug=True)
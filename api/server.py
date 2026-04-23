from flask import Flask, jsonify, request
import pandas as pd
import torch

app = Flask(__name__)

districts = pd.read_csv("data/processed/districts_enriched.csv")

# -----------------------------
# 1. BASIC DATA API
# -----------------------------
@app.route("/districts")
def get_districts():
    return jsonify(districts.to_dict(orient="records"))

# -----------------------------
# 2. TOP RISK AREAS
# -----------------------------
@app.route("/risk/top")
def top_risk():
    top = districts.sort_values("risk_score", ascending=False).head(10)
    return jsonify(top.to_dict(orient="records"))

# -----------------------------
# 3. SINGLE DISTRICT QUERY
# -----------------------------
@app.route("/district/<name>")
def district(name):
    row = districts[districts["district"] == name]
    return jsonify(row.to_dict(orient="records"))

# -----------------------------
# 4. ML INFERENCE ENDPOINT (PLACEHOLDER)
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    # future: GraphSAGE inference here
    return jsonify({
        "predicted_risk": 0.72,
        "note": "GraphSAGE inference placeholder"
    })

if __name__ == "__main__":
    app.run(debug=True)
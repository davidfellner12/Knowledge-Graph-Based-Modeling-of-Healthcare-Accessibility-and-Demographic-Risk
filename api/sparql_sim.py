import pandas as pd

districts = pd.read_csv("data/processed/districts_enriched.csv")

def query_high_risk():
    return districts[districts["risk_score"] > 0.6]

def query_accessible():
    return districts[districts["nearest_hospital_km"] < 3]
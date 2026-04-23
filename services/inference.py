import torch
import pandas as pd

from utilis.geo import GeoEngine   # FIXED IMPORT


class HealthcareInferenceEngine:

    def __init__(self, model, triples_df, districts_df, hospitals_df):
        self.model = model.eval()
        self.triples = triples_df
        self.districts = districts_df
        self.geo = GeoEngine(hospitals_df)

    def predict_risk(self, x, edge_index):
        with torch.no_grad():
            return self.model(x, edge_index).squeeze()

    def explain_triples(self, district):
        return self.triples[
            (self.triples["head"] == district) |
            (self.triples["tail"] == district)
        ].head(5).to_dict(orient="records")

    def explain_geo(self, row):
        return self.geo.nearest_hospital(row["lat"], row["lon"])

    def run(self, district_name):
        row = self.districts[self.districts["district"] == district_name].iloc[0]

        geo = self.explain_geo(row)
        kg = self.explain_triples(district_name)

        return {
            "district": district_name,
            "nearest_hospital_km": geo["distance_km"],
            "kg_explanation": kg,
            "interpretation": (
                "High risk" if geo["distance_km"] > 10 else
                "Medium risk" if geo["distance_km"] > 5 else
                "Low risk"
            )
        }
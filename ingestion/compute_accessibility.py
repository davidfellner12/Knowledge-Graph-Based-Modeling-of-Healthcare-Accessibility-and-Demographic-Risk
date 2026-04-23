import pandas as pd
from geopy.distance import geodesic
import os


class AccessibilityEngine:
    """
    Computes healthcare accessibility + risk features
    for Austrian districts based on hospital proximity.
    """

    def __init__(self, districts_path: str, hospitals_path: str):
        self.districts_path = districts_path
        self.hospitals_path = hospitals_path

        self.districts = None
        self.hospitals = None

   
    def load_data(self):
        self.districts = pd.read_csv(self.districts_path)
        self.hospitals = pd.read_csv(self.hospitals_path)

        required_district_cols = ["district", "population", "elderly_pct", "lat", "lon"]
        required_hospital_cols = ["id", "lat", "lon"]

        for col in required_district_cols:
            if col not in self.districts.columns:
                raise ValueError(f"Missing column in districts: {col}")

        for col in required_hospital_cols:
            if col not in self.hospitals.columns:
                raise ValueError(f"Missing column in hospitals: {col}")

    def compute_nearest_hospital(self, district_row):
        d_loc = (district_row["lat"], district_row["lon"])
        min_dist = float("inf")

        for _, h in self.hospitals.iterrows():
            h_loc = (h["lat"], h["lon"])
            dist = geodesic(d_loc, h_loc).km
            min_dist = min(min_dist, dist)

        return min_dist

  
    def compute_features(self):
        self.districts["nearest_hospital_km"] = self.districts.apply(
            self.compute_nearest_hospital,
            axis=1
        )

        self.districts["walk_time_min"] = (
            self.districts["nearest_hospital_km"] / 5 * 60
        )

        self.districts["risk_score"] = (
            0.5 * self.districts["elderly_pct"] +
            0.3 * self.districts["nearest_hospital_km"] +
            0.2 * (self.districts["population"] / 50000)
        )

  
    def save(self, output_path: str):
        # ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # save file
        self.districts.to_csv(output_path, index=False)

        print(f"✔ Saved enriched dataset → {output_path}")

    
    def run(self, output_path: str = "data/processed/districts_enriched.csv"):
        self.load_data()
        self.compute_features()
        self.save(output_path)



if __name__ == "__main__":
    engine = AccessibilityEngine(
        districts_path="data/raw/districts.csv",
        hospitals_path="data/raw/hospitals_big.csv"
    )

    engine.run()
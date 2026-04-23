import pandas as pd
import numpy as np
from geopy.distance import geodesic
import os


class SpatialGraphBuilder:
    """
    Builds a spatial healthcare graph for KG + GNN models.

    Nodes:
        - districts
        - hospitals

    Edges:
        - district → nearest hospitals (accessibility edges)
        - optional k-NN spatial edges between districts

    Output:
        - edge list (CSV)
        - node features (CSV)
    """

    def __init__(
        self,
        districts_path: str,
        hospitals_path: str,
        k_nearest: int = 3
    ):
        self.districts_path = districts_path
        self.hospitals_path = hospitals_path
        self.k = k_nearest

        self.districts = None
        self.hospitals = None

        self.edges = []
        self.nodes = []

    
    def load_data(self):
        self.districts = pd.read_csv(self.districts_path)
        self.hospitals = pd.read_csv(self.hospitals_path)

  
    def dist(self, a, b):
        return geodesic(a, b).km

   
    def build_nodes(self):
        for _, d in self.districts.iterrows():
            self.nodes.append({
                "node_id": f"district_{d['district']}",
                "type": "district",
                "lat": d["lat"],
                "lon": d["lon"],
                "population": d["population"],
                "elderly_pct": d["elderly_pct"]
            })

        for _, h in self.hospitals.iterrows():
            self.nodes.append({
                "node_id": f"hospital_{h['id']}",
                "type": "hospital",
                "lat": h["lat"],
                "lon": h["lon"]
            })

   
    def build_district_hospital_edges(self):
        for _, d in self.districts.iterrows():
            d_loc = (d["lat"], d["lon"])

            distances = []

            for _, h in self.hospitals.iterrows():
                h_loc = (h["lat"], h["lon"])
                distance = self.dist(d_loc, h_loc)

                distances.append((h["id"], distance))

            # sort by distance
            distances.sort(key=lambda x: x[1])

            # connect to k nearest hospitals
            for h_id, dist in distances[: self.k]:
                self.edges.append({
                    "src": f"district_{d['district']}",
                    "dst": f"hospital_{h_id}",
                    "relation": "NEAR",
                    "weight": dist
                })

   
    def build_district_knn_edges(self):
        for i, d1 in self.districts.iterrows():
            d1_loc = (d1["lat"], d1["lon"])

            distances = []

            for j, d2 in self.districts.iterrows():
                if i == j:
                    continue

                d2_loc = (d2["lat"], d2["lon"])
                distance = self.dist(d1_loc, d2_loc)

                distances.append((d2["district"], distance))

            distances.sort(key=lambda x: x[1])

            for d2_id, dist in distances[: self.k]:
                self.edges.append({
                    "src": f"district_{d1['district']}",
                    "dst": f"district_{d2_id}",
                    "relation": "NEIGHBOR",
                    "weight": dist
                })

    
    def save(self, out_dir="data/graph"):
        os.makedirs(out_dir, exist_ok=True)

        pd.DataFrame(self.nodes).to_csv(
            os.path.join(out_dir, "nodes.csv"),
            index=False
        )

        pd.DataFrame(self.edges).to_csv(
            os.path.join(out_dir, "edges.csv"),
            index=False
        )

        print("✔ Graph exported:")
        print("  - nodes.csv")
        print("  - edges.csv")

   
    def run(self, include_district_knn=True):
        self.load_data()
        self.build_nodes()
        self.build_district_hospital_edges()

        if include_district_knn:
            self.build_district_knn_edges()

        self.save()



if __name__ == "__main__":
    builder = SpatialGraphBuilder(
        districts_path="data/raw/districts.csv",
        hospitals_path="data/raw/hospitals_big.csv",
        k_nearest=3
    )

    builder.run()
import torch
import pandas as pd
import networkx as nx
import os


class GraphSAGEDataBuilder:
    def __init__(self,
                 triples_path="data/processed/kg_triples.csv",
                 output_path="ml/graphsage_data.pt"):

        self.triples_path = triples_path
        self.output_path = output_path

    def load(self):
        self.df = pd.read_csv(self.triples_path)

    def build(self):
        G = nx.Graph()

        for _, row in self.df.iterrows():
            G.add_edge(row["head"], row["tail"])

        nodes = list(G.nodes())
        node_to_idx = {n: i for i, n in enumerate(nodes)}

        edge_index = torch.tensor(
            [[node_to_idx[u], node_to_idx[v]] for u, v in G.edges()],
            dtype=torch.long
        ).t().contiguous()

        # node features = identity (baseline)
        x = torch.eye(len(nodes))

        # risk label placeholder
        y = torch.zeros(len(nodes))

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        torch.save((x, edge_index, y), self.output_path)

        print(f"✔ Saved GraphSAGE data → {self.output_path}")

    def run(self):
        self.load()
        self.build()


if __name__ == "__main__":
    GraphSAGEDataBuilder().run()
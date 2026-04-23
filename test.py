import torch

x, edge_index, y = torch.load("ml/graphsage_data.pt")

print(x.shape)
print(edge_index.shape)
print(y.shape)
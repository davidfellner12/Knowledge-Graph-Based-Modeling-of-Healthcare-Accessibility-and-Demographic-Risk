import os
import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv


# -------------------------
# MODEL
# -------------------------
class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x


# -------------------------
# MAIN TRAINING PIPELINE
# -------------------------
def main():

    # -------------------------
    # LOAD DATA
    # -------------------------
    x, edge_index, y = torch.load("ml/graphsage_data.pt")

    # -------------------------
    # DEVICE SETUP
    # -------------------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    x = x.to(device)
    edge_index = edge_index.to(device)
    y = y.to(device)

    # -------------------------
    # MODEL INIT (dynamic input size FIX)
    # -------------------------
    model = GraphSAGE(
        in_channels=x.shape[1],
        hidden_channels=16
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # -------------------------
    # TRAIN LOOP
    # -------------------------
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()

        out = model(x, edge_index).squeeze()

        loss = F.mse_loss(out, y)

        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    print("✔ GraphSAGE trained")

    # -------------------------
    # SAVE MODEL (CRITICAL FIX)
    # -------------------------
    os.makedirs("ml", exist_ok=True)

    torch.save(model.state_dict(), "ml/graphsage_model.pt")
    print("✔ Model saved → ml/graphsage_model.pt")


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    main()
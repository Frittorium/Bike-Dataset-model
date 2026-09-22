import torch
import numpy as np
import pandas as pd
import math
import os
from sklearn.preprocessing import StandardScaler

class BikeNN(torch.nn.Module):
    def __init__(self, n):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(n, 64), torch.nn.ReLU(),
            torch.nn.Linear(64, 32), torch.nn.ReLU(),
            torch.nn.Linear(32, 16), torch.nn.ReLU(),
            torch.nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.net(x)

base_dir = os.path.dirname(os.path.abspath(__file__))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load(os.path.join(base_dir,"models","bike_model.pt"), map_location=device,weights_only=False)

model = BikeNN(checkpoint["n_features"]).to(device)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

feature_names = checkpoint["feature_names"]

scaler = StandardScaler()
scaler.mean_ = checkpoint["scaler_mean"]
scaler.scale_ = checkpoint["scaler_scale"]
scaler.n_features_in_ = checkpoint["n_features"]
scaler.feature_names_in_ = np.array(feature_names, dtype=object)


def predict(data: dict) -> int:
    row = pd.DataFrame([data])[feature_names]
    x_scaled = scaler.transform(row)
    x_t = torch.tensor(x_scaled, dtype=torch.float32).to(device)

    with torch.no_grad():
        pred_log = model(x_t)

    pred = np.expm1(pred_log.cpu().numpy())
    return math.ceil(pred.flatten()[0])
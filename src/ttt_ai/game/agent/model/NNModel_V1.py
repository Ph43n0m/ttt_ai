import torch.nn as nn


class NNModel_V1(nn.Module):

    def __init__(self):
        super(NNModel_V1, self).__init__()
        size = 9
        layer_multiplier = 32
        self.fc1 = nn.Linear(size, size * layer_multiplier)  # Input layer
        self.fc2 = nn.Linear(
            size * layer_multiplier, size * (layer_multiplier // 2)
        )  # Hidden layer
        self.fc3 = nn.Linear(size * (layer_multiplier // 2), size)  # Output layer
        self.relu = nn.ReLU()

    def forward(self, x):
        # x = torch.relu(self.fc1(x))  # Activation function for first layer
        # x = torch.relu(self.fc2(x))  # Activation function for second layer
        x = self.relu(self.fc1(x))  # Activation function for first layer
        x = self.relu(self.fc2(x))  # Activation function for second layer
        x = self.fc3(x)  # Output layer
        return x

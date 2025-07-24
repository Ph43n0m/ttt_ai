import torch.nn as nn


class NNModel_V2(nn.Module):

    def __init__(self, randomness: float = 0.2):
        super(NNModel_V2, self).__init__()
        size = 9
        layer_multiplier = 32
        self.fc1 = nn.Linear(size, size * (layer_multiplier // 2))
        self.fc2 = nn.Linear(size * (layer_multiplier // 2), size * layer_multiplier)
        self.fc3 = nn.Linear(size * layer_multiplier, size * (layer_multiplier // 2))
        self.fc4 = nn.Linear(size * (layer_multiplier // 2), size)

        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)

        # Dropout layers
        self.dropout1 = nn.Dropout(p=randomness)
        self.dropout2 = nn.Dropout(p=randomness)
        self.dropout3 = nn.Dropout(p=randomness)
        self.dropout4 = nn.Dropout(p=randomness)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.fc4(x)

        return x

import torch
import torch.nn as nn
import torch.nn.functional as F

class ContinuousPolicyNetwork(nn.Module):
    def __init__(self, input_size=4, hidden_size=64, output_size=2):
        super(ContinuousPolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # Output move_x, move_y directly as continuous values
        x = self.out(x)
        return x
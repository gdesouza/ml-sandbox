import torch
import torch.nn as nn
import torch.nn.functional as F

from util.acceleration import accel_device



class ContinuousPolicyNetwork(nn.Module):
    def __init__(self, input_size=4, hidden_size=64, output_size=2):
        super(ContinuousPolicyNetwork, self).__init__()
        gpu = accel_device()
        self.fc1 = nn.Linear(input_size, hidden_size, device=gpu)
        self.fc2 = nn.Linear(hidden_size, hidden_size, device=gpu)
        self.out = nn.Linear(hidden_size, output_size, device=gpu)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # Output move_x, move_y directly as continuous values
        x = self.out(x)
        return x
    
class MultiMoveNetwork(nn.Module):
    def __init__(self, input_size=4, hidden_size=64, num_moves=5):
        super(MultiMoveNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        
        # Each move has 2 outputs (move_x, move_y)
        output_size = 2 * num_moves
        self.out = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)  # returns a vector of length 10 if num_moves=5
import sys
import pandas as pd
import torch
import torch.nn as nn
from datetime import datetime

from util.model import ContinuousPolicyNetwork
from util.acceleration import accel_device

# Specify the training file path
file_path = 'game_data'  # Replace with your actual file path

def load_data(filename:str) -> pd.DataFrame:
    try:
        # Load the file into a DataFrame
        df = pd.read_csv(f"{filename}.csv", sep=',')  

    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
    except pd.errors.ParserError:
        print(f"Error: Could not parse the file. Check the file format and separator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # drop columns "execution" and "clock" from df
    df = df.drop(columns=['Execution', 'clock'])
    return df

def train(X, y):
    model = ContinuousPolicyNetwork(input_size=4, hidden_size=64, output_size=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()

    dataset = torch.utils.data.TensorDataset(X, y)
    loader = torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=False)

    num_epochs = 100
    for epoch in range(num_epochs):
        for batch_X, batch_Y in loader:
            optimizer.zero_grad()
            pred = model(batch_X)
            loss = criterion(pred, batch_Y)
            loss.backward()
            optimizer.step()
        #if epoch % 100 == 0:
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")
    
    return model

def save_model(model, filename):
    filename = f"{filename}.pth"

    torch.save(model.state_dict(), filename)
    print(f"Model saved as {filename}")

def main(file_path):
    device = accel_device()

    df = load_data(file_path)
    # define X and y tensors
    X = df.iloc[:, :-2].values
    X = torch.tensor(X, dtype=torch.float32, device=device)

    y = df.iloc[:, -2:].values
    y = torch.tensor(y, dtype=torch.float32, device=device)

    model = train(X,y)
    save_model(model, file_path)

if __name__=='__main__':
        # Check that a filename has been provided as a command line argument.
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        sys.exit(1)
    
    # Parse the filename from the command line arguments.
    filename = sys.argv[1]
    
    main(filename)
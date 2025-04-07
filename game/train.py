import sys
import pandas as pd
import torch
import torch.nn as nn

from util.model import ContinuousPolicyNetwork
from util.acceleration import accel_device

def default_settings():
    settings = {
        'training': {
            'num_epochs': 200,
            'batch_size': 32,
            'learning_rate': 0.001,
            'shuffle': True,
            'drop_columns': ['Execution', 'clock'],
            'input_columns': ['current_position_x', 'current_position_y', 'target_position_x', 'target_position_y'],
            'output_columns': ['move_x', 'move_y'],
        }
    }

def parse_yaml(file_path):
  import yaml
  with open(file_path, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)
      return default_settings()


def load_data(filename:str, settings) -> pd.DataFrame:
    try:
        # Load the file into a DataFrame
        df = pd.read_csv(f"{filename}/demonstrations.csv", sep=',')  

    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
    except pd.errors.ParserError:
        print(f"Error: Could not parse the file. Check the file format and separator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # drop columns "execution" and "clock" from df
    df = df.drop(columns=settings['drop_columns'], axis=1)
    return df

def train(X, y, settings):
    
    model = ContinuousPolicyNetwork()
    model.train()  # set model to training mode
    optimizer = torch.optim.Adam(model.parameters(), lr=settings['learning_rate'])
    criterion = nn.MSELoss()

    dataset = torch.utils.data.TensorDataset(X, y)
    loader = torch.utils.data.DataLoader(dataset, batch_size=settings['batch_size'], shuffle=settings['shuffle'])

    for epoch in range(settings['num_epochs']):
        for batch_X, batch_Y in loader:
            optimizer.zero_grad()
            pred = model(batch_X)
            loss = criterion(pred, batch_Y)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}/{settings['num_epochs']}, Loss: {loss.item()}")
    
    return model

def save_model(model, filename):
    filename = f"{filename}/model.pth"

    torch.save(model.state_dict(), filename)
    print(f"Model saved as {filename}")

def main(file_path):
    device = accel_device()
    print(f"Using device: {device}")

    settings = parse_yaml('settings.yaml')['training']

    df = load_data(file_path, settings)

    # define X and y tensors
    X = df.loc[:, settings['input_columns']].values
    X = torch.tensor(X, dtype=torch.float32, device=device)

    y = df.loc[:, settings['output_columns']].values
    y = torch.tensor(y, dtype=torch.float32, device=device)

    model = train(X,y, settings)
    save_model(model, file_path)

if __name__=='__main__':
        # Check that a filename has been provided as a command line argument.
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        sys.exit(1)
    
    # Parse the filename from the command line arguments.
    filename = sys.argv[1]
    
    main(filename)
import torch

def accel_device():

    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"

    elif torch.cuda.is_available():
        device = "cuda"

    return torch.device(device)
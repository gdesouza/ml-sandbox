import unittest
from pathlib import Path
import tempfile

import torch

from util.coordinate import Coordinate
from util.inputs import FromModel
from util.acceleration import accel_device
from util.model import ContinuousPolicyNetwork


class FromModelTests(unittest.TestCase):
    def test_loads_checkpoint_saved_on_another_accelerator(self):
        checkpoint = (
            Path(__file__).parents[1]
            / "data"
            / "demonstrations_20241218_172133.pth"
        )

        model_input = FromModel(
            checkpoint,
            Coordinate(360, 480),
            Coordinate(0, 0),
        )

        self.assertEqual(next(model_input.model.parameters()).device, accel_device())
        self.assertFalse(hasattr(model_input.model, "fc3"))

    def test_infers_configurable_hidden_size_from_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "small.pth"
            source = ContinuousPolicyNetwork(hidden_size=8, hidden_layers=2)
            torch.save(source.state_dict(), checkpoint)

            model_input = FromModel(
                checkpoint,
                Coordinate(360, 480),
                Coordinate(0, 0),
            )

        self.assertEqual(model_input.model.fc1.out_features, 8)


if __name__ == "__main__":
    unittest.main()

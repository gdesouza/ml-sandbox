import unittest
from pathlib import Path

from util.coordinate import Coordinate
from util.inputs import FromModel
from util.acceleration import accel_device


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


if __name__ == "__main__":
    unittest.main()

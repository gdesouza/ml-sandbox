import unittest
from unittest.mock import Mock, call, patch

from util.colour import Colour
from util.display import Display
from util.rectangle import Rectangle


class DisplayTests(unittest.TestCase):
    def test_target_is_white_with_black_border(self):
        display = Display.__new__(Display)
        display.gameDisplay = Mock()
        display.parking = Rectangle(10, 20, 70, 70, Colour.WHITE)

        with patch("util.display.pygame.draw.rect") as draw_rect:
            display.draw_parking()

        self.assertEqual(
            draw_rect.call_args_list,
            [
                call(display.gameDisplay, Colour.WHITE, [10, 20, 70, 70]),
                call(
                    display.gameDisplay,
                    Colour.BLACK,
                    [10, 20, 70, 70],
                    width=3,
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()

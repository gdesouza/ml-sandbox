import unittest
from unittest.mock import Mock, call, patch

from util.colour import Colour
from util.display import Display
from util.rectangle import Rectangle


class DisplayTests(unittest.TestCase):
    def test_player_is_drawn_as_blue_circle_inside_its_bounding_box(self):
        display = Display.__new__(Display)
        display.gameDisplay = Mock()
        display.car = Rectangle(10, 20, 50, 50, Colour.BLOCK)

        with patch("util.display.pygame.draw.circle") as draw_circle:
            display.draw_car()

        draw_circle.assert_called_once_with(
            display.gameDisplay,
            Colour.BLOCK,
            (35, 45),
            25,
        )

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

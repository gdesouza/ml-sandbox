import signal

import random
import sys
import pygame
import time

from util.colour import Colour
from util.coordinate import Coordinate
from util.display import Display
from util.inputs import FromKeyboard
from util.rectangle import Rectangle
from util.screen import Screen
from util.settings import parse_yaml

_game_exit = False
# Handle Ctrl+C to exit the game
def signal_handler(sig, frame):
    global _game_exit
    print('Game over.')
    _game_exit = True

signal.signal(signal.SIGINT, signal_handler)

def end_game():
    global _game_exit
    _game_exit = True

def start_game():
    global _game_exit
    _game_exit = False

def is_game_ended():
    global _game_exit
    return _game_exit

class Game:
    """
    Game class to handle the game logic and rendering.
    """
    global _game_exit

    def __init__(self, input=FromKeyboard(), output=sys.stdout) -> None:
        self.input = input
        self.output = output

        settings = parse_yaml('settings.yaml')['game']

        self.framerate = settings['fps']
        self.staleness_factor = settings['stallness_factor']

        screen_width = settings['screen']['width']
        screen_height = settings['screen']['height']
        bluebox_width = settings['bluebox']['width']
        bluebox_height = settings['bluebox']['height']
        redbox_width = settings['redbox']['width']
        redbox_height = settings['redbox']['height']
            
        self.screen = Screen(screen_width, screen_height)
        self.display = Display(screen=self.screen)
        self.clock = pygame.time.Clock()
        self.display.set_caption(settings.get('title', 'Game'))

        self.bluebox = Rectangle((self.screen.width * 0.45),(self.screen.height * 0.8), bluebox_width, bluebox_height, Colour.BLUE)
        self.redbox = Rectangle(0, 0, redbox_width, redbox_height, Colour.RED)

        start_game()
        self.num_success = 0

        pygame.init()

    
    def update_clock(self) -> None:
        self.clock.tick(self.framerate)

    def render(self, message=None) -> None:
        self.display.background()
        pygame.draw.rect(self.display.get(), self.redbox.colour, self.redbox.dim())
        pygame.draw.rect(self.display.get(), self.bluebox.colour, self.bluebox.dim())
        if message:
            self.display.message_display(message)
        pygame.display.update()

    def run(self) -> None:
        execution_id = 0

        while not is_game_ended():
            execution_id += 1
            self.start(execution_id)
            print(f"{execution_id}: {self.num_success/execution_id:.2f}%")
            time.sleep(1)

        self.quit()

    def start(self, execution_id=0) -> None:
        self.input.reset_move()
        stalled = 0

        initpos = Coordinate.center(self.display.screen.width - self.bluebox.w, self.display.screen.height - self.bluebox.h)
        self.bluebox.teleport(initpos)
        self.input.goto(initpos.x,initpos.y)

        initpos = Coordinate.random(self.display.screen.width - self.redbox.w, self.display.screen.height - self.redbox.h) 
        self.redbox.teleport(initpos)
        self.input.move_target(initpos.x, initpos.y)
                               
        while not is_game_ended():
            
            move = self.input.get_move()
            self.bluebox.pos += move

            if self.bluebox.is_inside(self.redbox):
                self.render('Success')
                self.num_success += 1
                break

            elif not self.bluebox.is_inside(Rectangle(0, 0, self.display.screen.width, self.display.screen.height)):
                self.render('Failed')
                break

            else:
                self.render()
                self.update_clock()

                if move == Coordinate(0, 0):
                    stalled += 1
                    if stalled > self.staleness_factor:
                        self.render('Stalled')
                        break
                else:
                    print(f"{execution_id},{pygame.time.get_ticks()},{self.bluebox},{self.redbox},{move}", file=self.output)
                    stalled = 0
                    
    def quit(self) -> None:
        pygame.quit()

if __name__=='__main__':
    pass

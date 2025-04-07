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

def signal_handler(sig, frame):
    print('Game over.')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def default_settings():
    settings = {
        'game': {
            'title': 'Default settings',
            'fps': 60,
            'stallness_factor': 100,
            'screen_width': 800,
            'screen_height': 600,
            'bluebox_width': 50,
            'bluebox_height': 50,
            'redbox_width': 70,
            'redbox_height': 70
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


class Game:
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

        self._game_exit = False
        self.num_success = 0

        pygame.init()

    
    def is_game_ended(self) -> bool:
        return self._game_exit

    def update_clock(self) -> None:
        self.clock.tick(self.framerate)

    def render(self) -> None:
        self.display.background()
        pygame.draw.rect(self.display.get(), self.redbox.colour, self.redbox.dim())
        pygame.draw.rect(self.display.get(), self.bluebox.colour, self.bluebox.dim())

    def start(self, execution_id=0) -> None:
        execution_id += 1
        self.input.reset_move()
        stalled = 0

        # initpos_x = random.randint(0, self.display.screen.width-50)
        # initpos_y = random.randint(0, self.display.screen.height-50)
        initpos = Coordinate.center(self.display.screen.width - self.bluebox.w, self.display.screen.height - self.bluebox.h)
        self.bluebox.teleport(initpos)
        self.input.goto(initpos.x,initpos.y)

        initpos = Coordinate.random(self.display.screen.width - self.redbox.w, self.display.screen.height - self.redbox.h) 
        self.redbox.teleport(initpos)
        self.input.move_target(initpos.x, initpos.y)
                               
        while not self.is_game_ended():
            
            move = self.input.get_move()
            self.bluebox.pos += move

            if move == Coordinate(0,0):
                stalled += 1
                if stalled > self.staleness_factor:
                    self.display.message_display('Stalled')
                    pygame.display.update()
                    print(f"{execution_id}: {self.num_success/execution_id:.2f}%")
                    time.sleep(1)
                    self.start(execution_id)

            else: 
                stalled = 0

            self.render()

            if self.bluebox.is_inside(self.redbox):
                self.display.message_display('Success')
                pygame.display.update()
                self.num_success += 1
                print(f"{execution_id}: {self.num_success/execution_id:.2f}%")
                time.sleep(1)
                self.start(execution_id)

            elif not self.bluebox.is_inside(Rectangle(0, 0, self.display.screen.width, self.display.screen.height)):
                self.display.message_display('Failed')
                pygame.display.update()
                print(f"f{execution_id}: {self.num_success/execution_id:.2f}%")
                time.sleep(1)
                self.start(execution_id)

            else:
                pygame.display.update()
                self.update_clock()

                if move.x > 0 or move.y > 0:
                    print(f"{execution_id},{pygame.time.get_ticks()},{self.bluebox},{self.redbox},{move}", file=self.output)
                    #print(f"{execution_id},{pygame.time.get_ticks()},{self.display.car},{self.display.parking},{self.display.car.distance(self.display.parking)},{move}", file=self.output)
                    # print(f"{execution_id},{pygame.time.get_ticks()},{self.display.car},{self.display.parking},{Coordinate(self.display.car.x-move.x, self.display.car.y-move.y)}", file=self.output)

    def quit(self) -> None:
        pygame.quit()

if __name__=='__main__':
    pass

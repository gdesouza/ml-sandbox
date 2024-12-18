import pygame
import time

from util.colour import Colour
from util.coordinate import Coordinate
from util.display import Display
from util.inputs import FromKeyboard

class Game:
    def __init__(self, input=FromKeyboard()) -> None:
        self.input = input
        self.display = Display()
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.display.set_caption('Parking game')
        self._game_exit = False
        self.staleness_factor = 100
        pygame.init()

    
    def is_game_ended(self) -> bool:
        return self._game_exit

    def update_clock(self) -> None:
        self.clock.tick(self.framerate)
        

    def fail(self) -> None:
        self.display.message_display('Failed')

    def success(self) -> None:
        self.display.message_display('Success')

    def render(self) -> None:
        self.display.set_background()
        self.display.parking.draw(self.display.get())
        self.display.car.draw(self.display.get())

    def start(self, execution_id=0) -> None:
        execution_id += 1
        self.input.reset_move()
        result = None
        stalled = 0
        self.display.car.go_to(Coordinate(self.display.screen.width * 0.45,self.display.screen.height * 0.8))
        while not self.is_game_ended():
            
            move = self.input.get_move()
            self.display.car.x += move.x
            self.display.car.y += move.y

            if move == Coordinate(0,0):
                stalled += 1
                if stalled > self.staleness_factor:
                    self.fail()
                    pygame.display.update()
                    time.sleep(1)
                    self.start(execution_id)
                    result = "failed"


            self.render()

            if self.display.is_car_inside_parking():
                self.success()
                pygame.display.update()
                time.sleep(1)
                self.start(execution_id)
                result = "success"


            if self.display.is_car_out_of_bounds():
                self.fail()
                pygame.display.update()
                time.sleep(1)
                self.start(execution_id)
                result = "failed"

            pygame.display.update()
            self.update_clock()

            print(f"{execution_id},{pygame.time.get_ticks()},{self.display.car},{self.display.parking},{move}")

    def quit(self) -> None:
        pygame.quit()

if __name__=='__main__':
    pass
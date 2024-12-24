import pandas
import pygame

from util.screen import Screen
from util.rectangle import Rectangle
from util.colour import Colour

class Display:
    def __init__(self) -> None:
        self.screen = Screen()
        self.gameDisplay = pygame.display.set_mode((self.screen.width,self.screen.height))
        self.car = Rectangle((self.screen.width * 0.45),(self.screen.height * 0.8),50,50,Colour.BLOCK)
        self.parking = Rectangle(0,0,70,70,Colour.RED)

    def set_caption(self, text: str) -> None:
        pygame.display.set_caption(text)

    def set_background(self) -> None:
        self.gameDisplay.fill(self.screen.background)

    def get(self) -> object:
        return self.gameDisplay
    
    def draw_car(self) -> None:
        self.car.draw(self.gameDisplay)

    def draw_parking(self) -> None:
        self.car.draw(self.gameDisplay) 

    def text_objects(self, text, font):
        textSurface = font.render(text, True, Colour.BLACK)
        return textSurface, textSurface.get_rect()

    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.text_objects (text, largeText)
        TextRect.center = (self.screen.CenterWidth(), self.screen.CenterHeight())
        self.gameDisplay.blit(TextSurf, TextRect)

    def is_car_inside_parking(self) -> None:
        return (self.car.pos.x > self.parking.pos.x) and (self.car.pos.x+self.car.w < self.parking.pos.x+self.parking.w) and \
                (self.car.pos.y > self.parking.pos.y) and (self.car.pos.y+self.car.h < self.parking.pos.y+self.parking.h)

    def is_car_out_of_bounds(self) -> None:
        return (self.car.pos.x > self.screen.width - self.car.w or self.car.pos.x < 0) or \
                (self.car.pos.y > self.screen.height - self.car.h or self.car.pos.y < 0)




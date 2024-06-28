import pygame

from util.colour import Colour

class Rectangle():
    def __init__(self, x=0, y=0, w=0, h=0, colour=Colour.BLACK) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour

    def dim(self) -> list:
        return [ self.x, self.y, self.w, self.h ]
    
    def draw(self, display: object) -> None:
        pygame.draw.rect(display, self.colour, self.dim())

    def move(self, delta: object) -> None:
        self.x += delta.x
        self.y += delta.y

    def go_to(self, position: object) -> None:
        self.x = position.x
        self.y = position.y

    def __str__(self) -> str:
        return f"{self.x},{self.y}"
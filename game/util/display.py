import pygame

from util.screen import Screen
from util.rectangle import Rectangle
from util.colour import Colour

class Display:
    def __init__(self, screen=Screen()) -> None:
        self.screen = screen
        self.gameDisplay = pygame.display.set_mode((screen.width,screen.height))

    def set_caption(self, text: str) -> None:
        pygame.display.set_caption(text)

    def background(self) -> None:
        self.gameDisplay.fill(self.screen.background)

    def get(self) -> object:
        return self.gameDisplay
    
    def text_objects(self, text, font):
        textSurface = font.render(text, True, Colour.BLACK)
        return textSurface, textSurface.get_rect()

    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.text_objects (text, largeText)
        TextRect.center = (self.screen.CenterWidth(), self.screen.CenterHeight())
        self.gameDisplay.blit(TextSurf, TextRect)





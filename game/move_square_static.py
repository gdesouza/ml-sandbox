import pygame
import time


class Coordinate:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

class Colour():
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLOCK = (53,115,255)

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


class Screen:
    def __init__(self, width=800, height=600, colour=Colour.WHITE) -> None:
        self.width = width
        self.height = height
        self.background = colour

    def CenterWidth(self) -> int:
        return self.width/2
    
    def CenterHeight(self) -> int:
        return self.height/2


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
        return (self.car.x > self.parking.x) and (self.car.x+self.car.w < self.parking.x+self.parking.w) and \
                (self.car.y > self.parking.y) and (self.car.y+self.car.h < self.parking.y+self.parking.h)

    def is_car_out_of_bounds(self) -> None:
        return (self.car.x > self.screen.width - self.car.w or self.car.x < 0) or \
                (self.car.y > self.screen.height - self.car.h or self.car.y < 0)


class Game:
    def __init__(self) -> None:
        self.display = Display()
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.display.set_caption('Parking game')
        self._game_exit = False
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
        move = Coordinate(0, 0)
        result = None
        self.display.car.go_to(Coordinate(self.display.screen.width * 0.45,self.display.screen.height * 0.8))
        while not self.is_game_ended():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move.x = -5
                    elif event.key == pygame.K_RIGHT:
                        move.x = 5
                    elif event.key == pygame.K_UP:
                        move.y = -5
                    elif event.key == pygame.K_DOWN:
                        move.y = 5

                # This block will reset the increment after each move.
                # If we don't do this, the car will keep moving making the 
                # task a bit harder (and more interesting).
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        move.x = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        move.y = 0
            
            self.display.car.x += move.x
            self.display.car.y += move.y

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
                time.sleep(2)
                self.start(execution_id)
                result = "failed"

            pygame.display.update()
            self.update_clock()

            print(f"{execution_id},{pygame.time.get_ticks()},{self.display.car},{self.display.parking},{move}")

    def quit(self) -> None:
        pygame.quit()

if __name__=="__main__":
    game = Game()
    game.start()
    game.quit()
    quit()

from util.game import Game
from util.inputs import FromModel
from util.coordinate import Coordinate

if __name__=="__main__":
    game = Game(input=FromModel('model.pth', Coordinate(360,480), Coordinate(0,0)))
    game.start()
    game.quit()
    quit()

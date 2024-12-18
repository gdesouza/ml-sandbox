from util.game import Game
from util.inputs import FromModel
from util.coordinate import Coordinate

ML_MODEL = 'demonstrations_20241218_172133.pth'

if __name__=="__main__":
    game = Game(input=FromModel(ML_MODEL, Coordinate(360,480), Coordinate(0,0)))
    game.start()
    game.quit()
    quit()

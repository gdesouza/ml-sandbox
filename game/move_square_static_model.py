import sys
import os
from util.game import Game
from util.inputs import FromModel
from util.coordinate import Coordinate

if __name__=="__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        sys.exit(1)
    
    # Parse the filename from the command line arguments.
    ML_MODEL = f"{sys.argv[1]}.pth"

    f = open(os.devnull,"w")

    game = Game(input=FromModel(ML_MODEL, Coordinate(360,480), Coordinate(0,0)), output=f)
    game.start()
    game.quit()
    f.close()
    quit()

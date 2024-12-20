import sys
from util.game import Game
from util.inputs import FromFile

if __name__=="__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        sys.exit(1)
    
    # Parse the filename from the command line arguments.
    filename = f"{sys.argv[1]}.csv"

    game = Game(input=FromFile(filename))
    game.start()
    game.quit()
    quit()

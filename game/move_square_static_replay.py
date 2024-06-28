from util.game import Game
from util.inputs import FromFile

if __name__=="__main__":
    game = Game(input=FromFile('replay_game_1.txt'))
    game.start()
    game.quit()
    quit()

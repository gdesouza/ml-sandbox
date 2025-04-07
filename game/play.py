import os
from datetime import datetime
from util.game import Game

if __name__=="__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"data/{timestamp}"
    filename = f"{path}/demonstrations.csv"

    #create the directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    #create the file if it does not exist
    if not os.path.exists(filename):
        open(filename, 'w').close()

    #create the file with the header
    out = open(filename, 'a')
    print('Execution,clock,current_position_x,current_position_y,target_position_x,target_position_y,move_x,move_y', file=out)

    game = Game(output=out)
    game.start()
    out.close()
    game.quit()
    quit()

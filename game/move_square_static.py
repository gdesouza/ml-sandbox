from datetime import datetime
from util.game import Game

if __name__=="__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demonstrations_{timestamp}.csv"

    out = open(filename, 'w')
    print('Execution,clock,current_position_x,current_position_y,target_position_x,target_position_y,move_x,move_y', file=out)
    game = Game(output=out)
    game.start()
    out.close()
    game.quit()
    quit()

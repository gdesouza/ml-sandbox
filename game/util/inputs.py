import pygame
import pandas
import torch
from util.coordinate import Coordinate
from util.model import ContinuousPolicyNetwork

class FromKeyboard:
    def __init__(self) -> None:
        self.reset_move()

    def reset_move(self) -> None:
        self.move = Coordinate(0,0)

    def get_move(self) -> object:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move.x = -5
                elif event.key == pygame.K_RIGHT:
                    self.move.x = 5
                elif event.key == pygame.K_UP:
                    self.move.y = -5
                elif event.key == pygame.K_DOWN:
                    self.move.y = 5

            # This block will reset the increment after each move.
            # If we don't do this, the car will keep moving making the 
            # task a bit harder (and more interesting).
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.move.x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.move.y = 0

        return self.move


class FromFile:
    def __init__(self, filename) -> None:
        # open file
        self.reader = pandas.read_csv(filename,usecols=['move_x', 'move_y'], header=0)

    def reset_move(self) -> None:
        self.current_line = 1
        line = self.reader.iloc[self.current_line]
        print("move: ", line['move_x'],line['move_y'])
        self.move = Coordinate(line['move_x'],line['move_y'])
        print(self.move)

    def get_move(self) -> object:
        self.current_line += 1
        if self.current_line >= self.reader.shape[0]:
            return Coordinate(0,0)
        line = self.reader.iloc[self.current_line]
        self.move = Coordinate(line['move_x'],line['move_y'])

        return self.move
    
class FromModel:
    def __init__(self, filename, init_pos_blue, init_pos_red) -> None:
        self.model = ContinuousPolicyNetwork(input_size=4, hidden_size=64, output_size=2)
        self.model.load_state_dict(torch.load(filename))
        self.initial_state = torch.tensor([init_pos_blue.x, init_pos_blue.y, init_pos_red.x, init_pos_red.y], dtype=torch.float32)
        self.reset_move()

    def reset_move(self) -> None:
        self.state = torch.tensor(self.initial_state)
        print("state reset: ", self.state)

    def get_move(self) -> object:
        self.model.eval()
        with torch.no_grad():
            next_move = self.model(self.state.unsqueeze(0))  # add batch dimension
            next_move = torch.round(next_move)
            self.state[0] = self.state[0] + next_move[0,0]
            self.state[1] = self.state[1] + next_move[0,1]
            self.move = Coordinate(next_move[0,0].item(),next_move[0,1].item())

        return self.move 
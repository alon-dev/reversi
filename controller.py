from model import Model
import numpy as np

class Controller:
    def __init__(self) -> None:
        self.model = Model()

    def legal_place(self, i,j):
        if self.model.valid((i,j))[0]:
            return True
        return False
    def place(self, i,j):
        if self.model.valid((i,j))[0]:
            self.model.move((i,j))
            return self.model.board
        return None
    def computer_play(self):
        move = Model.min_max(self.model.board, 4, False)[0][0]
        print(move)
        self.model.move(move)
        return self.model.board
    def options(self):
        board = np.zeros((8,8))
        options = self.model.all_options()
        for option in options:
            board[option[0][0], option[0][1]] = option[1]
        return board

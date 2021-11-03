from model import Model
import numpy as np

class Controller:
    def __init__(self) -> None:
        self.model = Model()

    def legal_place(self, i,j):
        if self.model.valid((i,j)):
            return True
        return False
    def place(self, i,j):
        if self.model.valid((i,j)):
            self.model.move((i,j))
            return self.model.board
        return None
    def options(self):
        board = np.zeros((8,8))
        options = self.model.all_options()
        for option in options:
            board[option[0][0], option[0][1]] = option[1]
        return board

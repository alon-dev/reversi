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
        turn = self.model.turn
        if self.model.valid((i,j))[0]:
            is_end = self.model.move((i,j))
            if is_end:
                return self.model.board, True, True, self.model.pieces()
            if self.model.turn == turn:
                return self.model.board, True, False, self.model.pieces()
            return self.model.board, False, False, self.model.pieces()
        return None

    def computer_play(self, difficulty):
        if difficulty == 0:
            min_max_func = self.model.min_max
        else:
            min_max_func = self.model.min_max1
        turn = self.model.turn
        while self.model.turn == turn:
            if turn == -1:
                res = min_max_func(4, False)
                move = res[0][0]
            else:
                res = min_max_func(4, True)
                move = res[0][0]
            is_end = self.model.move(move)
            if is_end:
                return self.model.board, True, self.model.pieces(), self.model.turn
        return self.model.board, False, self.model.pieces(), self.model.turn
    def options(self):
        board = np.zeros((8,8))
        options = self.model.all_options()
        if len(options) == 0:
            return []
        for option in options:
            board[option[0][0], option[0][1]] = option[1]
        return board
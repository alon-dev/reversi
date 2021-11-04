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

    def computer_play(self):
        turn = self.model.turn
        if turn == -1:
            res = self.model.min_max(6, False)
            move = res[0][0]
        else:
            res = self.model.min_max1(6, True)
            move = res[0][0]
            print(res[2])
        is_end = self.model.move(move)
        if is_end:
            return self.model.board, True, self.model.pieces(), self.model.turn
        return self.model.board, False, self.model.pieces(), self.model.turn
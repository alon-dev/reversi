from model import Model
import numpy as np
import timeit

class Controller:
    def __init__(self) -> None:
        self.model = Model()
        self.default_start = "8/8/8/3wb3/3bw3/8/8/8"
        self.start = ""
    def legal_place(self, i,j):
        if self.model.valid((i,j))[0]:
            return True
        return False

    def place(self, i,j):
        turn = self.model.turn
        if self.model.valid((i,j))[0]:
            is_end = self.model.move((i,j))[0]
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
                res = min_max_func(6, False)
                move = res[0][0]
            else:
                res = min_max_func(6, True)
                move = res[0][0]
            is_end = self.model.move(move)[0]
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
    
    def generate_board(self):
        if self.start == "":
            x = self.default_start.split("/")
        else:
            x = self.start.split("/")
        for i in range(8):
            current_row = x[i]
            j = 0
            for item in current_row:
                if item.isdigit():
                    while j < int(item):
                        self.model.board[i,j] = 0
                        j += 1
                else:
                    if item == "w":
                        self.model.board[i, j] = 1
                    elif item =="b":
                        self.model.board[i,j] = -1
                    j += 1
        return self.model.board
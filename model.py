import numpy as np
from copy import deepcopy

class Model:
    def __init__(self):
        self.board = np.zeros((8, 8))
        self.board[3, 3] = -1
        self.board[4, 4] = -1
        self.board[3, 4] = 1
        self.board[4, 3] = 1
        self.turn = -1
        
    def is_flip_in_direction(self, dir1, dir2, pos):
        num = 0
        x = pos[0] + dir1
        y = pos[1] + dir2
        first = True
        while x < 8 and x >= 0 and y < 8 and y >= 0:
            if first:
                first = False
                if self.board[x, y] != -self.turn:
                    return (False, num)
                num += 1

            else:
                if self.board[x, y] == self.turn:
                    return (True, num)
                if self.board[x, y] == 0:
                    return (False, num)
                num += 1
            x += dir1
            y += dir2
        return (False, num)

    def valid(self, pos):
        count = 0
        if self.board[pos[0], pos[1]] != 0:
            return (False, count)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    res = self.is_flip_in_direction(i, j, pos)
                    if res[0]:
                        count+=res[1]
        if count >= 0:
            res = (True, count)
        else:
            res = (False, count)
        return res

    def flip(self, dir1, dir2, pos):
        x = pos[0] + dir1
        y = pos[1] + dir2
        while self.board[x, y] != self.turn:
            self.board[x, y] = self.turn
            x += dir1
            y += dir2

    def move(self, pos):
        if not self.all_options():
            self.turn *= -1
        self.board[pos[0], pos[1]] = self.turn
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i!=0 or j!=0:
                    if self.is_flip_in_direction(i, j, pos)[0]:
                        self.flip(i, j, pos)
        self.turn *= -1

    def all_options(self):
        all_options = []
        for i in range(8):
            for j in range(8):
                res = self.valid([i,j])
                if res[0]:
                    all_options.append([[i, j], res[1]])
        return all_options

    def pieces(self):
        sum = 0
        for i in self.board:
            sum += i
        return sum

    def min_max(self, depth):
        all_options = self.all_options()
        help_turn = self.turn
        help_board = deepcopy(self.board)
        if not all_options:
            self.turn *= -1
            all_options = self.all_options()
            if not all_options():
                return self.pieces() * 100000
            return self.min_max(self, depth - 1)

        for pos in all_options:
            self.move(pos)

import numpy as np

class Model:
    def __init__(self):
        self.board = np.zeros((8, 8))
        self.board[3, 3] = -1
        self.board[4, 4] = -1
        self.board[3, 4] = 1
        self.board[4, 3] = 1
        self.turn = -1
        
    def is_flip_in_direction(self, dir1, dir2, pos):
        x = pos[0] + dir1
        y = pos[1] + dir2
        first = True
        while x < 8 and x >= 0 and y < 8 and y >= 0:
            if first:
                first = False
                if self.board[x, y] != -self.turn:
                    return False

            else:
                if self.board[x, y] == self.turn:
                    return True
                if self.board[x, y] == 0:
                    return False
            x += dir1
            y += dir2
        return False

    def valid(self, pos):
        if self.board[pos[0], pos[1]] != 0:
            return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if self.is_flip_in_direction(i, j, pos):
                        return True
        return False

    def flip(self, dir1, dir2, pos):
        x = pos[0]
        y = pos[1]
        while self.board[x, y] != self.turn:
            self.board[x, y] = self.turn
            x += dir1
            y += dir2

    def move(self, pos):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and self.is_flip_in_direction(i, j, pos):
                    self.flip(i, j, pos)
        self.turn *= -1

    def all_options(self):
        all_options = []
        for i in range(8):
            for j in range(8):
                if self.valid([i, j]):
                    all_options.append([i, j])
        return all_options
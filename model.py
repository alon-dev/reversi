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
        if count > 0:
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
        self.board[pos[0], pos[1]] = self.turn
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i!=0 or j!=0:
                    if self.is_flip_in_direction(i, j, pos)[0]:
                        self.flip(i, j, pos)
        self.turn *= -1
        game_over = Model.game_over(self.board)
        if not game_over:
            if len(self.all_options()) == 0:
                self.turn *= -1
        return game_over

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
            for j in i:
                sum += j
        return sum
    
    @staticmethod
    def game_over(board):
        model = Model()
        model.board = board
        if not model.all_options():
            model.turn *= -1
            if not model.all_options():
                return True
        return False
    
    @staticmethod
    def is_terminal(alg_board, depth):
        if depth == 0 or Model.game_over(alg_board):
            return True
        return False
    
    @staticmethod
    def score(board):
        sum_white = 0
        sum_black = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == -1:
                    if (i == 0 and j == 0) or (i == 7 and j == 0) or (i == 7 and j == 7) or (i == 0 and j == 7):
                        sum_black+=20
                    else:
                        sum_black+=1
                if board[i][j] == 1:
                    if (i == 0 and j == 0) or (i == 7 and j == 0) or (i == 7 and j == 7) or (i == 0 and j == 7):
                        sum_white+=20
                    else:
                        sum_white+=1
        return sum_black - sum_white

    def min_max(self, depth, isMaximizingPlayer, alpha = float("-inf"), beta = float("inf")):
        if isMaximizingPlayer:
            self.turn = -1
        else:
            self.turn = 1
        if Model.is_terminal(self.board, depth):
            return (None, Model.score(self.board))
        if isMaximizingPlayer:
            best_score = float("-inf")
            best_move = None
            moves = self.all_options()
            temp_board = deepcopy(self.board)
            temp_turn = self.turn
            for move in moves:
                self.move(move[0])
                score = self.min_max(depth-1, not isMaximizingPlayer, alpha, beta)[1]
                self.board = deepcopy(temp_board)
                self.turn = temp_turn
                if score > best_score:
                    best_move = move
                    best_score = score
                    alpha = score
                    if alpha >= beta:
                        break
            return (best_move, best_score)
        else:
            best_score = float("inf")
            best_move = None
            moves = self.all_options()
            temp_board = deepcopy(self.board)
            temp_turn = self.turn
            for move in moves:
                self.move(move[0])
                score = self.min_max(depth-1, not isMaximizingPlayer, alpha, beta)[1]
                self.board = deepcopy(temp_board)
                self.turn = temp_turn
                if score < best_score:
                    best_move = move
                    best_score = score
                    beta = best_score
                    if alpha >= beta:
                        break
            return (best_move, best_score)
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
        self.game_over = False
        
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
        if len(self.all_options()) == 0:
            self.turn *= -1
            if len(self.all_options()) == 0:
                self.game_over = True
                return self.game_over
        self.game_over = False
        return self.game_over

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
    
    def is_terminal(self, depth):
        if depth == 0 or self.game_over:
            return True
        return False
    
    def score1(self):
        piece_score = self.pieces()
        for i in [0, 7]:
            for j in [0, 7]:
                piece_score += self.board[i][j] * 10
        if self.game_over:
            if piece_score > 0:
                return 1000000000 + piece_score
            elif piece_score < 0:
                return -100000000 + piece_score
            else:
                return 0
        return int(piece_score)
    def score2(self):
        if self.game_over:
            win_pieces = self.pieces()
            if win_pieces > 0:
                return 1000000000 + win_pieces
            elif win_pieces < 0:
                return -100000000 + win_pieces
            else:
                return 0
        scoring_table = np.array([[20, -3, 11, 8,  8, 11, -3, 20],
                        [-3, -7, -4, 1,  1, -4, -7, -3],
                        [11, -4, 2,  2,  2,  2, -4, 11],
                        [ 8,  1, 2, -3, -3,  2,  1,  8],
                        [ 8,  1, 2, -3, -3,  2,  1,  8],
                        [11, -4, 2,  2,  2,  2, -4, 11],
                        [-3, -7, -4, 1,  1, -4, -7, -3],
                        [20, -3, 11, 8,  8, 11, -3, 20]])
        sum = 0
        for i in range(8):
            for j in range(8):
                sum += scoring_table[i][j] * self.board[i][j]
        return sum
        
        

    def min_max(self, depth, isMaximizingPlayer, alpha = float("-inf"), beta = float("inf")):
        if self.is_terminal(depth):
            return (None, self.score1())
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
            return (best_move, best_score, self.turn)
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
                    beta = score
                    if alpha >= beta:
                        break
            return (best_move, best_score, self.turn)
    
    def min_max1(self, depth, isMaximizingPlayer, alpha = float("-inf"), beta = float("inf")):
        if self.is_terminal(depth):
            return (None, self.score2())
        if isMaximizingPlayer:
            best_score = float("-inf")
            best_move = None
            moves = self.all_options()
            temp_board = deepcopy(self.board)
            temp_turn = self.turn
            for move in moves:
                self.move(move[0])
                score = self.min_max1(depth-1, not isMaximizingPlayer, alpha, beta)[1]
                self.board = deepcopy(temp_board)
                self.turn = temp_turn
                if score > best_score:
                    best_move = move
                    best_score = score
                    alpha = score
                    if alpha >= beta:
                        break
            return (best_move, best_score, self.score2())
        else:
            best_score = float("inf")
            best_move = None
            moves = self.all_options()
            temp_board = deepcopy(self.board)
            temp_turn = self.turn
            for move in moves:
                self.move(move[0])
                score = self.min_max1(depth-1, not isMaximizingPlayer, alpha, beta)[1]
                self.board = deepcopy(temp_board)
                self.turn = temp_turn
                if score < best_score:
                    best_move = move
                    best_score = score
                    beta = score
                    if alpha >= beta:
                        break
            return (best_move, best_score)
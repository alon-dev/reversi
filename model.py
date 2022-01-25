import numpy as np
from copy import deepcopy

class Model:
    def __init__(self):
        self.board = np.zeros((8, 8))
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
        flipped = []
        x = pos[0] + dir1
        y = pos[1] + dir2
        while self.board[x, y] != self.turn:
            self.board[x, y] = self.turn
            #flipped.append((x,y))
            x += dir1
            y += dir2
        return flipped

    def move(self, pos):
        flipped = []
        self.board[pos[0], pos[1]] = self.turn
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i!=0 or j!=0:
                    if self.is_flip_in_direction(i, j, pos)[0]:
                        flip = self.flip(i, j, pos)
                        #for position in flip:
                            #flipped.append(position)
        self.turn *= -1
        if len(self.all_options()) == 0:
            self.turn *= -1
            if len(self.all_options()) == 0:
                self.game_over = True
                return self.game_over, flipped
        self.game_over = False
        return self.game_over, flipped

    def all_options(self):
        all_options = []
        for i in range(8):
            for j in range(8):
                res = self.valid([i,j])
                if res[0]:
                    all_options.append([[i, j], res[1]])
        return all_options
    def reverse_move(self, pos, flipped):
        self.board[pos[0], pos[1]] = 0
        for position in flipped:
            self.board[position[0], position[1]] *= -1

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

    def score(self):
        return self.pieces()
    def min_max(self, depth, isMaximizingPlayer, alpha = float("-inf"), beta = float("inf")):
        if self.is_terminal(depth):
            return (None, self.score())
        if isMaximizingPlayer:
            best_score = float("-inf")
            best_move = None
            moves = self.all_options()
            temp_turn = self.turn
            temp_board = deepcopy(self.board)
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
            return (best_move, best_score, self.score())
        else:
            best_score = float("inf")
            best_move = None
            moves = self.all_options()
            temp_turn = self.turn
            temp_board = deepcopy(self.board)
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
            return (best_move, best_score)
    def min_max1(self, depth, isMaximizingPlayer, alpha = float("-inf"), beta = float("inf")):
        if self.is_terminal(depth):
            return (None, self.score1())
        if isMaximizingPlayer:
            best_score = float("-inf")
            best_move = None
            moves = self.all_options()
            temp_turn = self.turn
            temp_board = deepcopy(self.board)
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
            return (best_move, best_score, self.score1())
        else:
            best_score = float("inf")
            best_move = None
            moves = self.all_options()
            temp_turn = self.turn
            temp_board = deepcopy(self.board)
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
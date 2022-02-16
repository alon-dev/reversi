from copy import deepcopy
from model import Model
import numpy as np
import random

board = np.zeros((8,8))
board[3, 3] = 1
board[3, 4] = -1
board[4, 3] = -1
board[4, 4] = 1
white_turn = True
counter = 0
for _ in range(100):
    model = Model(1)
    model.board = deepcopy(board)
    game_over = False
    white_turn = not white_turn
    
    if not white_turn:
        res = model.min_max(4, white_turn)[0]
    else:
        options = model.all_options()
        res = random.choice(options)
    game_over = model.move(res[0])[0]
    
    while not game_over:
        if ((not white_turn) and model.turn == -1) or white_turn and model.turn == 1:
            res = model.min_max(4, white_turn)[0]
        else:
            options = model.all_options()
            res = random.choice(options)
        game_over = model.move(res[0])[0]
    if (not white_turn) and model.pieces() < 0:
        counter += 1
    elif white_turn and model.pieces() > 0:
        counter += 1
    print(counter)
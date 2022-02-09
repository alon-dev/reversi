from model import Model
import numpy as np
from classes.constants import Constants

class Controller:
    

    def __init__(self) -> None:
        self.model = Model()
        self.start = ""
    
    def legal_place(self, i,j):
        if self.model.valid((i,j))[0]:
            return True
        return False

    def save_game(self):
        f = open('saved.txt', 'w+', encoding='utf8')
        full_string = ""
        for row in self.model.board:
            row_string = ""
            i = 0
            for place in row:
                if place == -1:
                    if i != 0:
                        row_string += str(i)
                        i = 0
                    row_string += "b"
                elif place == 1:
                    if i != 0:
                        row_string += str(i)
                        i = 0
                    row_string += "w"
                else:
                    i += 1
            if i != 0:
                row_string += str(i)
                i = 0
            full_string += row_string
            full_string += "/"
        f.write(full_string)
        if self.model.turn == -1:
            f.write("B")
        else:
            f.write("W")
        f.close()
    
    def load_game(self):
        try:
            f = open("saved.txt", 'r')
            self.start = str(f.readline())
            f.close()
            board = self.generate_board()[0]
            return True, board, self.model.turn
        except:
            return False, None, 0
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
                res = min_max_func(5, False)
                move = res[0][0]
            else:
                res = min_max_func(5, True)
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
            x = Constants.DEFAULT_START.split("/")
        else:
            x = self.start.split("/")
        for i in range(9):
            current_row = x[i]
            j = 0
            for item in current_row:
                if item.isdigit():
                    counter = 0
                    while counter < int(item):
                        self.model.board[i,j] = 0
                        j += 1
                        counter += 1
                else:
                    if item == "w":
                        self.model.board[i, j] = 1
                    elif item =="b":
                        self.model.board[i,j] = -1
                    elif item == "W":
                        self.model.turn = 1
                    elif item == "B":
                        print("yes")
                        self.model.turn = -1
                    j += 1
        return self.model.board, self.model.turn
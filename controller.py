from model import Model
import numpy as np
from classes.constants import Constants

class Controller:
    

    def __init__(self, difficulty) -> None:
        self.depth = 5
        if difficulty == 2:
            self.model = Model(1)
            self.depth = 6
        else:
            self.model = Model(difficulty)
        self.start = ""
    
    #Checks if a certain tile (i,j) is a legal placement
    def legal_place(self, i,j):
        if self.model.valid((i,j))[0]:
            return True
        return False
    
    #Saves the current game to a file called saved.txt, overrides if present.
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
    
    #Loads a game from saved.txt if it exists. otherwise returns an error.
    def load_game(self):
        try:
            f = open("saved.txt", 'r')
            self.start = str(f.readline())
            f.close()
            board = self.generate_board()[0]
            return True, board, self.model.turn
        except:
            return False, None, 0
    
    #Places a disk in the tile (i,j)
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

    #Plays for the computer and returns the state of the game (is the game over, who is currently leading, etc)
    def computer_play(self):
        turn = self.model.turn
        while self.model.turn == turn:
            if turn == -1:
                res = self.model.min_max(self.depth, False)
                move = res[0][0]
            else:
                res = self.model.min_max(self.depth, True)
                move = res[0][0]
            is_end, flipped_and_ends = self.model.move(move)
            if is_end:
                return self.model.board, True, self.model.pieces(), self.model.turn, flipped_and_ends
        return self.model.board, False, self.model.pieces(), self.model.turn, flipped_and_ends
    
    #Returns all possible placemets and the amount of disks they'll flip.
    def options(self):
        board = np.zeros((8,8))
        options = self.model.all_options()
        if len(options) == 0:
            return []
        for option in options:
            board[option[0][0], option[0][1]] = option[1]
        return board
    
    #Generates a board based on the current fen.
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
    
    def set_difficulty(self, difficulty):
        num = 1
        if difficulty == 'insane':
            self.model.set_difficulty(num)
            self.depth = 6
        elif difficulty == 'hard':
            self.model.set_difficulty(num)
        else:
            num = 0
            self.model.set_difficulty(num)
        return self.model.score_func, num

from tkinter import Label, Menu, Tk
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from classes.settings import Settings

from controller import Controller
from classes.main_menu import MM
from classes.mybutton import MyButton
from classes.constants import Constants

class View:
    def __init__(self, master, ai, difficulty, first):
        self.difficulty = difficulty
        self.ai = ai
        self.first = first
        print(self.difficulty, self.ai)
        self.master = master
        self.controller = Controller(self.difficulty)
        self.button_frm = tk.Frame(self.master)
        self.button_list = []
        self.color = Constants.DEFAULT_COLOR

        for i in range(8):
            self.button_list.append([])
            for j in range(8):
                self.button_list[i].append(MyButton(master=self.button_frm, command=self.on_button_click, i=i, j=j))
                self.button_list[i][j].grid(row=i, column=j)
        self.set_start()
        
        self.button_frm.pack()
        self.labelFrm = tk.Frame(self.master)
        self.win_label = Label(self.labelFrm, font=("Consolas, 30"), text="Reversi!", fg="red")
        self.labelFrm.pack()
        self.win_label.pack()
        self.update_turn()
        
        self.menubar = Menu(self.master)
        
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Save", command= self.controller.save_game)
        self.file_menu.add_command(label="Load", command= self.load_game)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label='About', command=self.about_menu)
        self.menubar.add_cascade(label='Settings', command=self.settings)
        self.master.config(menu=self.menubar)
        
        self.master.update()
        
    # Handles moves made by the player(s)
    def on_button_click(self, b):
        if self.controller.legal_place(b.i, b.j):
            board, is_double, self.is_win, pieces = self.controller.place(b.i,b.j)
            self.update(board)
            if self.is_win:
                self.win(pieces)
            self.dont_highlight()
            if not is_double:
                if not self.ai:
                    self.highlight()
                    for i in [Constants.LABELS["white_turn"], Constants.LABELS["black_turn"]]:
                        if self.win_label["text"] != i:
                            self.win_label["text"] = i
                            break
                else:
                    self.win_label["text"] = Constants.LABELS["pc_turn"]
                    self.master.update()
                    board, self.is_win, pieces, self.player, flipped_and_ends = self.controller.computer_play()
                    self.win_label["text"] = Constants.LABELS["player_turn"]
                    if self.is_win:
                        self.win(pieces)
                    self.highlight()
                    self.show_computer_move(flipped_and_ends[0], flipped_and_ends[1])
                    self.update(board)
            else:
                self.highlight()
    
    # Loads the saved board, and updates the board and the turn
    def load_game(self):
        didload, board, turn = self.controller.load_game()
        if didload:
            self.update(board)
            self.turn = turn
            print(self.turn)
            self.update_turn()
        else:
            showerror(title="Error!", message="No savefile found! Save a game and try again.")
            
    # Generates an empty board and sets it up.
    def set_start(self):
        board, turn = self.controller.generate_board()
        self.update(board)
        self.turn = turn
        
    #Handles the button images.
    def turn_black(self, b):
        b.configure(image=b.BLACK_IMAGE)
    def turn_white(self, b):
        b.configure(image=b.WHITE_IMAGE)
    def turn_null(self, b):
        b.configure(image=b.DEFAULT_IMAGE)
    
    # Highlights possible moves for the player and the amount of disks they'd flip. If vs pc and nothing to highlight- Plays for the pc.
    def highlight(self):
        highlights = self.controller.options()
        if len(highlights) == 0:
            if self.ai:
                if not self.is_win:
                    self.win_label["text"] = Constants.LABELS["pc_turn"]
                    board, self.is_win, pieces, self.player, flipped_and_ends = self.controller.computer_play()
                    if self.is_win:
                        self.win(pieces)
                    self.highlight()
                    self.show_computer_move(flipped_and_ends[0], flipped_and_ends[1])
                    self.win_label["text"] = Constants.LABELS["player_turn"]
                    self.update(board)
                
                else:
                    return
        for i in range(8):
            for j in range(8):
                if highlights[i, j] != 0:
                    self.button_list[i][j].configure(bg="yellow")
                    self.button_list[i][j]["text"] = int(highlights[i][j])
                    self.button_list[i][j].configure(compound="center")
                else:
                    self.button_list[i][j].configure(bg=self.color, text="")
    
    #Removes any highlighted tiles on the board.
    def dont_highlight(self):
        for i in range(8):
            for j in range(8):
                self.button_list[i][j].configure(bg=self.color, text="")
    
    #Handles wins. Ends the game and displays the winner.
    def win(self, pieces):
        if pieces > 0:
            self.win_label["text"] = Constants.LABELS["white_win"] + str(int(pieces))
        elif pieces == 0:
            self.win_label["text"] = "Draw!"
        else:
            self.win_label["text"] = Constants.LABELS["black_win"] + str(int(-pieces))
        self.win_label["fg"] = "yellow"
        self.win_label["bg"] = "black"
        for row in self.button_list:
            for button in row:
                button.configure(state="disabled")
                
    #Updates the board to match a given 2d numpy array representation of a board            
    def update(self, board):
        for i in range(8):
            for j in range(8):
                if(board[i][j] == -1):
                    self.turn_black(self.button_list[i][j])
                elif board[i][j] == 1:
                    self.turn_white(self.button_list[i][j])
                else:
                    self.turn_null(self.button_list[i][j])
        self.master.update()
        
    #Used to load/start a game and make sure labels are correct and correct player gets to play    
    def update_turn(self):
        if self.ai:
            if self.first and self.turn == -1:
                self.win_label["text"] = Constants.LABELS["player_turn"]
                self.highlight()
            else:
                self.win_label["text"] = Constants.LABELS["pc_turn"]
                self.dont_highlight()
                self.master.update()
                board, self.is_win, pieces, self.player, flipped_and_ends = self.controller.computer_play()
                self.win_label["text"] = Constants.LABELS["player_turn"]
                self.highlight()
                self.show_computer_move(flipped_and_ends[0], flipped_and_ends[1])
                self.update(board)
        else:
            if self.turn == -1:
                self.win_label["text"] = Constants.LABELS["black_turn"]
                self.highlight()
            else:
                self.win_label["text"] = Constants.LABELS["white_turn"]
                self.highlight()
        self.master.update()
        
    def show_computer_move(self, flipped, ends):
        for place in ends:
            self.button_list[place[0]][place[1]]["bg"] = 'gray'
        self.button_list[ends[0][0]][ends[0][1]]["bg"] = 'orange'
    
    def about_menu(self):
        showinfo('About This Game', message="This game was made by Alon Engel as a project for Rabin High School's AI major.")
    
    def settings(self):
        self.settings_class = Settings(self.color, self.difficulty)
        self.settings_class.summon_menu(self.settings_apply)
    
    def settings_apply(self):
        for i in range(8):
            for j in range(8):
                if self.button_list[i][j]["bg"] == self.color:
                    self.button_list[i][j]["bg"] = self.settings_class.color_variable.get()
        self.color = self.settings_class.color_variable.get()
        
        res = self.controller.set_difficulty(self.settings_class.difficulty_variable.get())
        self.difficulty = res[1]
        print(res[0])
        self.settings_class.root.destroy()
 


main_menu = MM()
main_menu.summon_menu()
ai = main_menu.ai
difficulty = main_menu.difficulty
first = main_menu.first
root = Tk()
root.title("Reversi")
view_controller = View(root, ai, difficulty, first)
root.update()
root.mainloop()
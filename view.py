from tkinter import Label, PhotoImage, Tk
import tkinter as tk
from tkinter.constants import GROOVE
import numpy as np
import time

from controller import Controller
from main_menu import MM

class MyButton(tk.Button):
    def __init__(self, master, command, i, j):
        self.command = command
        self.i = i
        self.j = j
        self.DEFAULT_IMAGE = PhotoImage()
        super().__init__(master=master, width=50, height=50, image=self.DEFAULT_IMAGE, bg="green", command=self.my_command, text="", padx=0, pady=0, font=("Consolas", 14), highlightthickness=0, bd=1, relief=GROOVE)
        self.WHITE_IMAGE = PhotoImage(file="img/white.png")
        self.BLACK_IMAGE = PhotoImage(file="img/black.png")
    def my_command(self):
        self.command(self)

class View:
    def __init__(self, master, ai, difficulty, first):
        self.difficulty = difficulty
        self.ai = ai
        self.first = first
        print(self.difficulty, self.ai)
        self.master = master
        self.controller = Controller()
        self.button_frm = tk.Frame(self.master)
        self.button_list = []

        for i in range(8):
            self.button_list.append([])
            for j in range(8):
                self.button_list[i].append(MyButton(master=self.button_frm, command=self.on_button_click, i=i, j=j))
                self.button_list[i][j].grid(row=i, column=j)
        self.set_start()

        self.button_frm.pack()
        #self.highlight()
        self.labelFrm = tk.Frame(self.master)
        self.win_label = Label(self.labelFrm, font=("Consolas, 30"), text="Reversi!", fg="red")
        self.labelFrm.pack()
        self.win_label.pack()
        if self.ai:
            if self.first:
                self.win_label["text"] = "Your Turn!"
                self.highlight()
            else:
                self.win_label["text"] = "PC's Turn!"
                self.master.update()
                board, self.is_win, pieces, self.player = self.controller.computer_play(self.difficulty)
                self.win_label["text"] = "Your Turn!"
                self.highlight()
                self.update(board)
        else:
            self.win_label["text"] = "Black's Turn!"
            self.highlight()
        self.master.update()

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
                    for i in ["White's Turn!", "Black's Turn"]:
                        if self.win_label["text"] != i:
                            self.win_label["text"] = i
                            break
                else:
                    self.win_label["text"] = "PC's Turn!"
                    self.master.update()
                    board, self.is_win, pieces, self.player = self.controller.computer_play(self.difficulty)
                    self.win_label["text"] = "Your Turn!"
                    if self.is_win:
                        self.win(pieces)
                    self.highlight()
                    self.update(board)
                    if self.is_win:
                        self.win(pieces)
            else:
                self.highlight()

    def set_start(self):
        board = self.controller.generate_board()
        self.update(board)
    def turn_black(self, b):
        b.configure(image=b.BLACK_IMAGE)
    def turn_white(self, b):
        b.configure(image=b.WHITE_IMAGE)
    def highlight(self):
        highlights = self.controller.options()
        if len(highlights) == 0:
            if self.ai:
                if not self.is_win:
                    self.controller.computer_play(self.difficulty)
                else:
                    return
        for i in range(8):
            for j in range(8):
                if highlights[i, j] != 0:
                    self.button_list[i][j].configure(bg="yellow")
                    self.button_list[i][j]["text"] = int(highlights[i][j])
                    self.button_list[i][j].configure(compound="center")
                else:
                    self.button_list[i][j].configure(bg="green", text="")
    def dont_highlight(self):
        for i in range(8):
            for j in range(8):
                self.button_list[i][j].configure(bg="green", text="")
    def win(self, pieces):
        if pieces > 0:
            self.win_label["text"] = f"White wins by {pieces}"
        elif pieces == 0:
            self.win_label["text"] = "Draw!"
        else:
            self.win_label["text"] = f"Black wins by {-pieces}"
        self.win_label["fg"] = "yellow"
        self.win_label["bg"] = "black"
        for row in self.button_list:
            for button in row:
                button.configure(state="disabled")
    def update(self, board):
        for i in range(8):
            for j in range(8):
                if(board[i][j] == -1):
                    self.turn_black(self.button_list[i][j])
                elif board[i][j] == 1:
                    self.turn_white(self.button_list[i][j])
        self.master.update()
 


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
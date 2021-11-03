from tkinter import PhotoImage, Tk
import tkinter as tk
import numpy as np

from controller import Controller

class MyButton(tk.Button):
    def __init__(self, master, command, i, j):
        self.command = command
        self.i = i
        self.j = j
        self.DEFAULT_IMAGE = PhotoImage()
        super().__init__(master=master, width=50, height=50, image=self.DEFAULT_IMAGE, bg="green", command=self.my_command)
        self.WHITE_IMAGE = PhotoImage(file="img/white.png")
        self.BLACK_IMAGE = PhotoImage(file="img/black.png")
    def my_command(self):
        self.command(self)

class View:
    def __init__(self, master):
        self.master = master
        self.controller = Controller()
        self.player = -1
        self.button_frm = tk.Frame(self.master)
        self.button_list = []

        for i in range(8):
            self.button_list.append([])
            for j in range(8):
                self.button_list[i].append(MyButton(master=self.button_frm, command=self.on_button_click, i=i, j=j))
                self.button_list[i][j].grid(row=i, column=j)
        self.button_list[3][3].configure(image=self.button_list[3][3].BLACK_IMAGE)
        self.button_list[4][4].configure(image=self.button_list[4][4].BLACK_IMAGE)
        self.button_list[3][4].configure(image=self.button_list[3][4].WHITE_IMAGE)
        self.button_list[4][3].configure(image=self.button_list[4][3].WHITE_IMAGE)

        self.button_frm.pack()
        self.highlight()
    def on_button_click(self, b):
        if self.controller.legal_place(b.i, b.j):
            b.configure(image=b.BLACK_IMAGE) if self.player == -1 else b.configure(image=b.WHITE_IMAGE)
            board = None
            if self.player==-1:
                self.player = 1
            else: 
                self.player = -1
            board = self.controller.place(b.i,b.j)
            for i in range(8):
                for j in range(8):
                    if(board[i][j] == -1):
                        self.turn_black(self.button_list[i][j])
                    elif board[i][j] == 1:
                        self.turn_white(self.button_list[i][j])
            self.highlight()
        else:
            return
    def turn_black(self, b):
        b.configure(image=b.BLACK_IMAGE)
    def turn_white(self, b):
        b.configure(image=b.WHITE_IMAGE)
    def highlight(self):
        highlights = self.controller.options()
        for i in range(8):
            for j in range(8):
                if highlights[i, j] != 0:
                    self.button_list[i][j].configure(bg="yellow")
                    self.button_list[i][j]["text"] = int(highlights[i][j])
                    self.button_list[i][j].configure(compound="center")
                else:
                    self.button_list[i][j].configure(bg="green", text="")
root = Tk()
root.title("Orthello")
view_controller = View(root)
root.update()
root.mainloop()
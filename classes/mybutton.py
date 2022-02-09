from tkinter import PhotoImage, GROOVE
import tkinter as tk

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
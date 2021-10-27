from tkinter import PhotoImage, Tk
import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master, command):
        self.command = command
        self.DEFAULT_IMAGE = PhotoImage()
        super().__init__(master=master, width=50, height=50, image=self.DEFAULT_IMAGE, bg="green", command=self.my_command)
        self.WHITE_IMAGE = PhotoImage(file="img/white.png")
        self.BLACK_IMAGE = PhotoImage(file="img/black.png")
    def my_command(self):
        self.command(self)

class View:
    def __init__(self, master):
        self.master = master
        self.player = -1
        self.button_frm = tk.Frame(self.master)
        self.button_list = []

        for i in range(8):
            self.button_list.append([])
            for j in range(8):
                self.button_list[i].append(MyButton(master=self.button_frm, command=self.on_button_click))
                self.button_list[i][j].grid(row=i, column=j)
        self.button_frm.pack()
    def on_button_click(self, b):
        b.configure(image=b.BLACK_IMAGE) if self.player == -1 else b.configure(image=b.WHITE_IMAGE)
        if self.player==-1:
            self.player = 1
        else: 
            self.player = -1
root = Tk()
root.title("Orthello")
view_controller = View(root)
root.update()
root.mainloop()
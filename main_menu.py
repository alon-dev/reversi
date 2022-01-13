from tkinter import *

class MM:
    def __init__(self):
        self.difficulty = 0
        self.ai = False
        self.first = True

    def summon_menu(self):
        self.root = Tk()
        self.entry = Frame(self.root)
        title = Label(self.entry, text="Welcome to Reversi!", font=("Consolas", 21), padx=10, fg="red")
        gamemode_label = Label(self.entry, text="Select Gamemode", font=("Consolas", 14), pady=10)
        ai_button = Button(self.entry, text="Player vs. AI", command= self.vs_ai)
        player_button = Button(self.entry, text="Player vs. Player", command= self.vs_player)
        title.grid(columnspan=3, row = 0, column=0)
        gamemode_label.grid(column=1, row=1)
        ai_button.grid(column=1, row=2)
        player_button.grid(column=1, row=3, pady=10)
        self.entry.pack()
        self.root.mainloop()
    
    def vs_ai(self):
        self.ai = True
        self.entry.destroy()
        self.second_entry = Frame(self.root)
        title = Label(self.second_entry, text="Welcome to Reversi!", font=("Consolas", 21), padx=10, fg="red")
        difficulty_label = Label(self.second_entry, text="Select Difficulty", font=("Helvetica", 14), pady=10)
        easy_button = Button(self.second_entry, text="Easy", command=self.easy)
        hard_button = Button(self.second_entry, text="Hard", command=self.hard)
        title.grid(columnspan=3, row = 0, column=0)
        difficulty_label.grid(column=1, row=1)
        easy_button.grid(column=1, row=2)
        hard_button.grid(column=1, row=3, pady=10)
        self.second_entry.pack()
    
    def vs_player(self):
        self.root.destroy()

    
    def easy(self):
        self.second_entry.destroy()
        self.third_entry()
    
    def hard(self):
        self.second_entry.destroy()
        self.difficulty = 1
        self.third_entry()
    
    def third_entry(self):
        self.third_entry_frame = Frame(self.root)
        title = Label(self.third_entry_frame, text="Welcome to Reversi!", font=("Consolas", 21), padx=10, fg="red")
        order_label = Label(self.third_entry_frame, text="Select Who Starts", font=("Helvetica", 14), pady=10)
        first_button = Button(self.third_entry_frame, text="You", command=self.first_command)
        second_button = Button(self.third_entry_frame, text="The AI", command=self.second_command)
        title.grid(columnspan=3, row = 0, column=0)
        order_label.grid(column=1, row=1)
        first_button.grid(column=1, row=2)
        second_button.grid(column=1, row=3, pady=10)
        self.third_entry_frame.pack()
    
    def first_command(self):
        self.first = True
        self.root.destroy()
    
    def second_command(self):
        self.first = False
        self.root.destroy()
        

        
        
from tkinter import *

class MM:
    def __init__(self):
        self.difficulty = 0
        self.ai = False
        self.first = True

    def summon_menu(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Welcome!')
        self.entry = Frame(self.root)
        title = Label(self.entry, text="Welcome to Reversi!", font=("Consolas", 21), padx=10, fg="red")
        title.grid(row=0, column=0, columnspan=2)
        explanation_paragraph = Label(self.entry, justify=CENTER, text="Each reversi piece has a black side and a white side. On your turn, you place one piece on \n\
the board with your color facing up. You must place the piece so that an opponent's piece, or a row of opponent's pieces, is flanked by\n\
your pieces. All of the opponent's pieces between your pieces are then turned over to become your color. You can capture vertical, \n\
horizontal, and diagonal rows of pieces. Also, you can capture more than one row at once.The objective of the game is \n\
to own more pieces than your opponent when the game is over. The game is over when neither player has a move. Usually, this means \n\
the board is full.")
        
        explanation_paragraph.grid(column=0, row=1, columnspan=2, sticky=W, padx=10)
        ready_button = Button(self.entry, justify=RIGHT, text="Ok, I'm ready to play!", command= self.first_entry)
        ready_button.grid(column=1, row=2, padx=5, pady=5, sticky=E)
        self.entry.pack()
        self.root.mainloop()
        
    def first_entry(self):
        self.entry.destroy()
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
        
    def vs_ai(self):
        self.ai = True
        self.entry.destroy()
        self.second_entry = Frame(self.root)
        title = Label(self.second_entry, text="Welcome to Reversi!", font=("Consolas", 21), padx=10, fg="red")
        difficulty_label = Label(self.second_entry, text="Select Difficulty", font=("Helvetica", 14), pady=10)
        easy_button = Button(self.second_entry, text="Easy", command=self.easy)
        hard_button = Button(self.second_entry, text="Hard", command=self.hard)
        insane_button = Button(self.second_entry, text="Insane", command=self.insane)
        title.grid(columnspan=3, row = 0, column=0)
        difficulty_label.grid(column=1, row=1)
        easy_button.grid(column=1, row=2, pady=5)
        hard_button.grid(column=1, row=3, pady=5)
        insane_button.grid(column=1, row=4, pady= 5)
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
    
    def insane(self):
        self.second_entry.destroy()
        self.difficulty = 2
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
        

        
        
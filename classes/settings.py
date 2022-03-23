from tkinter import *
from classes.constants import Constants

class Settings:
    def __init__(self, color, difficulty):
        self.color = color
        self.difficulty = difficulty
        self.color_list = Constants.COLORS
        self.difficulty_list = Constants.DIFFICULTIES
    
    def summon_menu(self, ok_command):
        self.root = Tk()
        self.root.title("Settings")
        self.settings_frame = Frame(self.root)
        self.color_variable = StringVar(self.settings_frame)
        self.color_variable.set(self.color)
        self.color_label = Label(self.settings_frame, text='Tile Color: ')
        self.color_label.grid(row=0, column=0, sticky=W)
        self.color_dropdown = OptionMenu(self.settings_frame, self.color_variable, *self.color_list)
        self.color_dropdown.grid(row = 0, column=1, sticky=E)
        
        self.difficulty_label = Label(self.settings_frame, text='Difficulty: ')
        self.difficulty_label.grid(row=1, column=0, sticky=W)
        self.difficulty_variable = StringVar(self.settings_frame)
        self.difficulty_variable.set(self.difficulty_list[self.difficulty])
        self.difficulty_dropdown = OptionMenu(self.settings_frame, self.difficulty_variable, *self.difficulty_list)
        self.difficulty_dropdown.grid(row = 1, column=1, sticky=E)
        
        self.button_frame = Frame(self.root)
        self.ok_button = Button(self.button_frame, text='Ok', command=ok_command)
        self.cancel_button = Button(self.button_frame, text='Cancel', command= self.root.destroy)
        self.ok_button.grid(row=0, column=0)
        self.cancel_button.grid(row=0, column=1)
        self.settings_frame.grid(column=0, row=0)
        self.button_frame.grid(column=1, row=1)
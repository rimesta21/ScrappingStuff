# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:00:44 2021

@author: rimes
"""

from tkinter import Tk, Entry, Label, Button
from tkinter.ttk import Frame

class UserInputWindow(Frame):
    def __init__(self, title, prompt):
        super().__init__()
        self.value = "No Entry"
        self.initUI(title, prompt)  
        
    def initUI(self, title, prompt):
        self.master.title(title)
        #self.pack(fill=BOTH, expand=1)
        self.l = Label(self.master, text = prompt)
        self.l.pack(pady = (10, 10))
        self.e = Entry(self.master)
        self.e.pack(pady = (15,15))
        self.b = Button(self.master, text = "Submit", command=self.cleanup)
        self.b.pack(pady = (15, 20))
    
    def cleanup(self):
        self.value = self.e.get()
        self.master.destroy()
    
    def getValue(self):
        return self.value
        
    
def openWindow(title, prompt):
    root = Tk()
    root.geometry("250x150+300+300")
    window = UserInputWindow(title, prompt)
    root.mainloop()
    return window.getValue()


if __name__ == '__main__':
    print(openWindow("Email Adress", "Please enter email adress:"))
        
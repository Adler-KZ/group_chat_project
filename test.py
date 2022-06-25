import imp
import random
from tkinter import *

def random_color():
    R = random.randint(30, 150)
    G = random.randint(30, 150)
    B = random.randint(30, 150)
    hex_color = "#{:02x}{:02x}{:02x}".format(R, G, B)
    return hex_color

root = Tk()
root.config(bg='#d3d3d3')
Label(text='Test color check',foreground=random_color(),bg='#d3d3d3').pack()

root.mainloop()
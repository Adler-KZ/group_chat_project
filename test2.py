from tkinter import *
from turtle import width

def test():
    print('hello')
root = Tk()
root.resizable(0,0)
# root.protocol('WM_DELETE_WINDOW',test)
frame = Frame(root)
root.geometry('800x750')
root.geometry('')
frame.pack()
usernameL = Label(frame, text=f'frame:',bg='white',font=('sens-serif', 20,'italic'))
messageE = Entry(frame,textvariable=frame,font=('sens-serif',18))
sendB = Button(frame,text='Send',bg='#32a850')
MESSAGEBOX = Text(frame,bg='#dfb5ff', font=(20)) 
# packs
MESSAGEBOX.pack(side= TOP,fill='both', expand=True)
usernameL.pack(side=LEFT,fill='both')
messageE.pack(side=LEFT,expand=True,fill='both')
sendB.pack(side=RIGHT,fill='both',ipadx=10)

root.mainloop()

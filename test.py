from cmath import exp
from tkinter import *

root = Tk()
root.geometry('400x400')

usernameL = Label(root, text=f'Your username: frame',font=('gabriola',35))
roomsL = Label(root, text='Avabaile Rooms:',font=('arial',12))
createB = Button(root,text='Create New Room',font=('arial',12))
ROOMS_LIST = Listbox(root,font=('calibri',14))
ROOMS_LIST.insert(0,'sfs')

usernameL.pack()
roomsL.pack(padx=(0,220),side=TOP)
ROOMS_LIST.pack(expand=True,fill='both',padx=25,pady=(2,5))
createB.pack(ipadx=5,pady=(0,2))
root.mainloop()
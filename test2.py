from tkinter import *

def go(event):
	cs = Lb.curselection()
	print(cs)
	# Updating label text to selected option
	w.config(text=Lb.get(cs))
	
	# Setting Background Colour
	for list in cs:
		
		if list == 0:
			top.configure(background='red')
		elif list == 1:
			top.configure(background='green')
		elif list == 2:
			top.configure(background='yellow')
		elif list == 3:
			top.configure(background='white')


top = Tk()
top.geometry('250x275')
top.title('Double Click')

# Creating Listbox
Lb = Listbox(top, height=6)
# Inserting items in Listbox
Lb.insert(0, 'Red')
Lb.insert(1, 'Green')
Lb.insert(2, 'Yellow')
Lb.insert(3, 'White')

# Binding double click with left mouse
# button with go function
Lb.bind('<Double-1>', go)
Lb.pack()

# Creating Edit box to show selected option
w = Label(top, text='Default')
w.pack()
top.mainloop()

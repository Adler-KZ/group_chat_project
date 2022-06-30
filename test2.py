# Import Library
from tkinter import *

# Create Object
root = Tk()

# Set title
root.title("Main Window")

# Set Geometry
root.geometry("200x200")

# Open New Window
def launch():
	global second
	second = Toplevel()
	second.title("Child Window")
	second.geometry("400x400")

# Show the window
def show():
	second.deiconify()

# Hide the window
def hide():
	second.withdraw()

# Add Buttons
Button(root, text="launch Window", command=launch).pack(pady=10)
Button(root, text="Show", command=show).pack(pady=10)
Button(root, text="Hide", command=hide).pack(pady=10)

# Execute Tkinter
root.mainloop()

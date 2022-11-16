from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("500x600+800+50")
# Set which cols and rows should expand with window
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

TasksList = ttk.Notebook(root)
Task1 = ttk.Frame(TasksList)
Task2 = ttk.Frame(TasksList)
TasksList.add(Task1, text = 'One One One One One One')
TasksList.add(Task2, text = 'Two Two Two Two Two Two')
TasksList.grid(row=1, column=0, sticky=N+W, columnspan=3)
# Make the TaskList span all three columns ------^

Photo1= PhotoImage(file="C-1.21.png")
Photo2 = PhotoImage(file="C-1.21.png")
# Put labels in root
Label(root, image=Photo1, bd=0).grid(row=0, column=0, sticky=W)
Label(root, image=Photo2, bd=0).grid(row=0, column=1, sticky=W)
# Don't put anything in column=2

root.mainloop()
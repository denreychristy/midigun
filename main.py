# MIDI Gun Main Script File

from tkinter import *
from tkinter import ttk
from classes.setlist import SetList
from classes.song import Song

root = Tk()
root.title("MIDIGUN")

userSetList = SetList(root, columns = ['', '', '', ''])

# Add a new song to the set list
def addSongToSetList():
	userSetList.add(song = Song())
addSongToSetListButton = Button(root, text = "Add New Song", command = addSongToSetList)

# Add elements to the window
#userSetList.pack(fill = BOTH, expand = True)
#addSongToSetListButton.pack()
userSetList.grid(row = 0, column = 0, columnspan = 3)
addSongToSetListButton.grid(row = 1, column = 0)

root.mainloop()
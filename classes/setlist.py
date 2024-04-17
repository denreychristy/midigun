# Set List Class

from tkinter import *
from tkinter import ttk
from classes.song import Song
from classes.section import Section
from classes.countoff import CountOff
from classes.midievent import MIDIEvent

class SetList(ttk.Treeview):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		self.songsList: list[Song] = []
		self.heading('#0', text = 'New Set List')
		self.bind('<Double-1>', self.onDoubleClick)
	
	def onDoubleClick(self, event):
		regionClicked = self.identify_region(event.x, event.y)
		
		# Ignore everything other than 'tree' and 'cell' regions
		if regionClicked not in ('tree', 'cell'):
			return
		
		# Get the relevant info from the clicked region
		clickedColumn	= self.identify_column(event.x)	# returns a str like '#0', '#1', etc.
		clickedRow		= self.identify_row(event.y)
		selectedIID		= self.focus()
		selectedValues	= self.item(selectedIID)		# gets the contents of the clicked region
		columnIndex		= int(clickedColumn[1 : ]) - 1	# converts the clickedColumn str to an int, skips the auto-created 0th column

		if clickedColumn == '#0':											# if the clicked region is the row header (all the way to the left)
			selectedText = selectedValues.get('text')						#	- retrieve the text of that region
		else:																# else (if the clicked region is anywhere other than the row header)
			try:
				selectedText = selected`Values.get('values')[columnIndex]	#	- retrieve the text of that region from the list of values in that row entry
			except:
				return														# in the event that a cell is empty, abort the function
		
		# Place a text entry box over the region to be edited
		columnBox = self.bbox(	# gets an array of x, y, w, and h for the clicked region
			item = selectedIID,
			column = clickedColumn
		)
		editEntry = ttk.Entry(self.master)	# creates a text entry box
		editEntry.place(			# places the box in the location and with the dimensions from columnBox
			x = columnBox[0],
			y = columnBox[1],
			w = columnBox[2],
			h = columnBox[3]
		)
		editEntry.editingColumnIndex	= columnIndex
		editEntry.editingItemIID		= selectedIID
		editEntry.insert(0, selectedText)
		editEntry.select_range(0, END)
		editEntry.focus()

		editEntry.bind('<FocusOut>', self.destroyEditEntryWidget)
		editEntry.bind('<Return>', self.onEnterPressed)
	
	def destroyEditEntryWidget(self, event):
		event.widget.destroy()
	
	def onEnterPressed(self, event):
		newText		= event.widget.get()
		selectedIID	= event.widget.editingItemIID
		columnIndex	= event.widget.editingColumnIndex
		if columnIndex == -1:	# tree column
			self.item(selectedIID, text = newText)
			parsedSelectedIID = self.parseSelectedIID(selectedIID)
			songIndex = parsedSelectedIID['song index']
			sectionIndex = parsedSelectedIID['section index']
			eventIndex = parsedSelectedIID['event index']
			if parsedSelectedIID['type'] == Song:
				self.songsList[songIndex
				    ].name = newText
			elif parsedSelectedIID['type'] == Section:
				self.songsList[songIndex
				    ].sectionsList[sectionIndex
					].name = newText
			elif parsedSelectedIID['type'] == MIDIEvent:
				self.songsList[songIndex
				    ].sectionsList[sectionIndex
				    ].eventsList[eventIndex
				    ].name = newText

		else:
			itemValues = self.item(selectedIID).get('values')
			itemValues[columnIndex] = newText
			self.item(selectedIID, values = itemValues)
		
		self.item(selectedIID, open = True)
		event.widget.destroy()
	
	def reconstitute(self):
		# Clear out treeview table
		for item in self.get_children():
			self.delete(item)
		
		# Rebuild treeview table
		for i, song in enumerate(self.songsList):
			songIID = f'song_{i}'
			self.insert('', END, text = str(song), iid = songIID, open = True)
			
			for ii, section in enumerate(song.sectionsList):
				sectionIID = f'song_{i}_section_{ii}'
				self.insert(songIID, END, text = str(section), iid = sectionIID, open = True)
				self.item(sectionIID, values = section.getValues())
				
				for iii, event in enumerate(section.eventsList):
					eventIID = f'song_{i}_section_{ii}_event_{iii}'
					self.insert(sectionIID, END, text = str(event), iid = eventIID)
	
	def add(self, song: Song):
		# Add a new song to the list and reconstitute
		self.songsList.append(song)
		self.reconstitute()
	
	def parseSelectedIID(self, selectedIID: str):
		resultDict = {
			'type': None,
			'song name': None,
			'song index': None,
			'section name': None,
			'section index': None,
			'event name': None,
			'event index': None
		}

		songIndexStart = selectedIID.index('_') + 1
		# Type: Song
		if 'section' not in selectedIID:
			resultDict['type'] = Song
			songIndex = int(selectedIID[songIndexStart : ])
			resultDict['song index'] = songIndex
			resultDict['song name'] = self.songsList[songIndex].name
			return resultDict
		
		# Otherwise
		songIndexEnd = selectedIID[songIndexStart : ].index('_') + songIndexStart
		songIndex = int(selectedIID[songIndexStart : songIndexEnd])
		resultDict['song index'] = songIndex
		resultDict['song name'] = self.songsList[songIndex].name
		sectionIndexStart = songIndexEnd + 9

		# Type: Section
		if 'event' not in selectedIID:
			resultDict['type'] = Section
			sectionIndex = int(selectedIID[sectionIndexStart : ])
			resultDict['section index'] = sectionIndex
			resultDict['section name'] = self.songsList[songIndex].sectionsList[sectionIndex].name
			return resultDict
		
		# Otherwise
		sectionIndexEnd = selectedIID[sectionIndexStart : ].index('_') + sectionIndexStart
		sectionIndex = int(selectedIID[sectionIndexStart : sectionIndexEnd])
		resultDict['section index'] = sectionIndex
		resultDict['section name'] = self.songsList[songIndex].sectionsList[sectionIndex]
		
		# Type: Event
		resultDict['type'] = Event
		eventIndexStart = sectionIndexEnd + 7
		eventIndex = int(selectedIID[eventIndexStart : ])
		resultDict['event index'] = eventIndex
		resultDict['event name'] = self.songsList[songIndex].sectionsList[sectionIndex].eventsList[eventIndex]
		return resultDict

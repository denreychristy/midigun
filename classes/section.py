# Song Section Class
from classes.midievent import MIDIEvent

class Section:
	def __init__(self, name: str = 'New Section', previousSection: 'Section' = None):
		self.name: str = name
		self.eventsList = [
			MIDIEvent()
		]
		if previousSection:
			startMeasure = previousSection.valuesDict['end measure'] + 1
		else:
			startMeasure = 0
		self.valuesDict: dict = {
			'time signature': 4,
			'beats per minute': 120.0,
			'start measure': startMeasure,
			'end measure': startMeasure + 1
		}
	
	def __eq__(self, other):
		if other == self.name:
			return True
		else:
			return False

	def __repr__(self):
		reprText = f'Section Object: {self.name}'
		for event in self.eventsList:
			reprText += '\n    - ' + event.__repr__()
		return reprText

	def __str__(self):
		return self.name

	def getValues(self):
		return [
			f"Time Sig: {self.valuesDict['time signature']}",
			f"BPM: {self.valuesDict['beats per minute']}",
			f"Start Measure: {self.valuesDict['start measure']}",
			f"End Measure: {self.valuesDict['end measure']}"
		]
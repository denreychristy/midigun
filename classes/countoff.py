# Song Count Off Class

from classes.section import Section

class CountOff(Section):
	def __init__(self, name: str = 'Count Off'):
		super().__init__(name = name)
		self.valuesDict['beats'] = 4
		del self.valuesDict['time signature']
		del self.valuesDict['start measure']
		del self.valuesDict['end measure']
	
	def getValues(self):
		return [
			f"Beats: {self.valuesDict['beats']}",
			f"BPM: {self.valuesDict['beats per minute']}",
		]
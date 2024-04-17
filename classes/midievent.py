# Midi Event Class

class MIDIEvent:
	def __init__(self, name: str = 'New Event'):
		self.name: str = name
	
	def __repr__(self):
		reprText = f'Event Object: {self.name}'
		return reprText

	def __str__(self):
		return self.name
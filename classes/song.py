# Song Class

from classes.section import Section
from classes.countoff import CountOff

class Song:
	def __init__(self, name: str = 'New Song'):
		self.name: str = name
		self.sectionsList: list[Section] = [
			CountOff(),
			Section()
		]
		self.totalMeasures: int = 0
		self.totalTimeSeconds: float = 0.0
	
	def __eq__(self, songName: str):
		if songName == self.name:
			return True
		else:
			return False

	def __repr__(self):
		reprText = f'\nSong Object: {self.name}'
		for section in self.sectionsList:
			reprText += '\n - ' + section.__repr__()
		reprText += '\n'
		return reprText

	def __str__(self):
		return self.name
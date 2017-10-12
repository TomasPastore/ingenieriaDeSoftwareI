
class PendingFloorsRecord():

	def __init__(self, numberOfFloors):
		self._record = [False] * numberOfFloors

	def nextFloor(self, anElevator):
		anElevator.
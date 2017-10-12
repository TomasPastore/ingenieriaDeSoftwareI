
class PendingFloorsRecord():

    def __init__(self):
        self._record = [] 

    def nextFloor(self, anElevator):
        if self._record:
            return self._record[0]

    def addCallFromFloor(self,anElevatorController,aFloor):
        #Este no sabemos como sacarlo porque si lo implementamos con un bitmap no podemos
        #saber next floor en estado stopped
        if not in self._record(aFloor):
            
            #Este if se puede sacar con un null object que no llegamos a implementar            
            if not self._record: 
                self.append(aFloor)

            #Este if no es del dominio del problema
            if anElevatorController.cabinFloorNumber() == aFloor:
                anElevatorController.openCabinDoor()

            anElevatorController.HowShouldIadd()

                if aFloor < self.cabinFloorNumber():
                    self.decreasingOrderInsert(aFloor)
                else :
                    self.increasingOrderInsert(aFloor)

            elif self.isCabinGoingUp(): 
                if aFloor > self.cabinFloorNumber():
                    self.increasingOrderInsert(aFloor)
                else: 
                    self.decreasingOrderInsert(aFloor)

    def decreasingOrderInsert(self, aFloor):
        pos = 0
        while ( pos < len(self.calls) and self.calls[pos] > aFloor ):
            pos += 1
        self.calls.insert(pos, aFloor)           

    def increasingOrderInsert(self, aFloor):
        pos = 0
        while ( pos < len(self.calls) and self.calls[pos] < aFloor ):
            pos += 1
        self.calls.insert(pos, aFloor)
